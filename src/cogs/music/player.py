# -*- coding: utf-8 -*-
# created by zrx.

import enum
import typing
import asyncio
import datetime
import discord
import async_timeout

from discord.ext import commands
from wavelink import Player, filters
from cogs.music.controller import InteractiveController

# from .view import InteractiveController

class RepeatMode(enum.Enum):
    NONE = 0
    ONE = 1
    ALL = 2
    
    
class MyFilters:
    def __init__(self) -> filters.Filter:
        self.NONE = filters.Filter(None)
        self.NIGHTCORE = filters.Filter(timescale=filters.Timescale(speed=1.2, pitch=1.1, rate=1.2))
        self.KARAOKE = filters.Filter(karaoke=filters.Karaoke(level=1.0, mono_level=1.0, filter_band=220.0, filter_width=100.0))
        self.EQUALIZER_FLAT = filters.Filter(equalizer=filters.Equalizer.flat())
        self.EQUALIZER_BOOST = filters.Filter(equalizer=filters.Equalizer.boost())
        self.EQUALIZER_METAL = filters.Filter(equalizer=filters.Equalizer.metal())
        self.EQUALIZER_PIANO = filters.Filter(equalizer=filters.Equalizer.piano())


class Player(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.repeat_mode = 0
        self.controller = None
        self.waiting = False
        self.updating = False
        self.previous_tracks = asyncio.Queue()
        self.track = None
        self.ctx: commands.Context = None
        self.dj: discord.Member = None

        self.last_action: dict = dict()

    @property
    def set_repeat(self) -> None:
        """ Функция, которая устанавливает режим повтора (повтор 1 трека, повтор всей очереди или без повтора). """

        if self.repeat_mode == 0:
            # Поставить режим повторения - ТЕКУЩИЙ
            self.repeat_mode = 1

        elif self.repeat_mode == 1:
            # Поставить режим повторения - ОЧЕРЕДЬ
            self.repeat_mode = 2

        elif self.repeat_mode == 2:
            # Поставить режим повторения - ОТКЛЮЧЁН
            self.repeat_mode = 0

    def get_entries(self) -> typing.Optional[list]:
        """ Возвращает очередь. """
        return list(self.queue._queue)

    def get_track_title_with_uri_str(self, track) -> str:
        """ Возвращает строку, содержащую в себе обрезанное название трека и ссылку на него. """
        return f'[{track.title[:28]}{"..." if len(track.title) >= 28 else ""}]({track.uri})'
    
    def get_current_and_total_duration_str(self) -> typing.Optional[str]:
        """ Возвращает строку, содержащую в себе общую длину трека и текущую позицию. """
        current_duration = str(datetime.timedelta(milliseconds=self.position))[:-7]
        total_duration = str(datetime.timedelta(milliseconds=self._current.duration))
        
        return f'{current_duration}/{total_duration}'
    
    def get_total_duration_str(self, track) -> typing.Optional[str]:
        """ Возвращает строку, содержащую в себе полную длину трека. """
        total_duration = str(datetime.timedelta(milliseconds=track.duration))

        return f'`{total_duration}`'

    def visual_duration(self) -> typing.Optional[str]:
        """ Возвращает сгенерированный progress bar. """

        def progressbar_1(value, maxValue, size):
            value = 1 if value == 0 else value
            percentage = value / maxValue
            progress = round(size * percentage)
            emptyProgress = size - progress
            progressText = "▢" * progress
            radioButton = "▣"
            emptyProgressText = "▢" * emptyProgress
            percentageText = str(round(percentage * 100)) + "%"

            Bar = progressText + radioButton + emptyProgressText#—▬
            return Bar, percentageText

        playerCurrentSecondsLength = self._current.length / 1000
        playerCurrentPosition = self.position / 1000
        progressbar1, percentageText1 = progressbar_1(playerCurrentPosition, playerCurrentSecondsLength, 10)

        def progressbar(value:int, max_value:int, size:int):
            """ 
            Генерирует progress bar
            
            :param value: текущая позиция воспроизведения трека
            :param max_value: общая длинма трека
            :param size: длина progress-бара в символах
            :return: str
            """

            # Предотвращение деления на ноль
            value = 1 if value == 0 else value

            bar_begin = '<:bar_begin_full:1145735887125225532>' if value >= max_value // value else '<:bar_begin:1146194551623651338>'
            bar_end = '<:bar_end_full:1146216084307988663>' if value >= max_value else '<:bar_end:1145726388477898793>'

            # Процентное соотношение (например, уже проиграно 80% трека)
            percentage = value / max_value
            # Округляем значение и получаем заполненное количество символов
            progress = round(size * percentage)
            # Количество пустых символов
            emptyProgress = size - progress
            # Обрабатываем и получаем текст с заполненными символами
            progressText = "<:bar_middle_full:1145736093526917150>" * (progress)
            # radioButton = "▣"
            # Обрабатываем и получаем текст с пустыми символами
            emptyProgressText = "<:bar_middle:1145726392936439839>" * (emptyProgress)
            # Процентное значение
            percentageText = str(round(percentage * 100)) + "%"

            # Итоговая строка
            Bar = bar_begin + progressText + emptyProgressText + bar_end
            return Bar, percentageText

        player_current_length = self._current.length / 1000
        player_current_position = self.position / 1000
        progressbar, percentageText = progressbar(player_current_position, player_current_length, 9)

        return progressbar1
    
    def get_visual_repeat_mode(self):
        """ Возвращает строку, содержащую в себе отображение текущего режима повтора трека. """
        if self.repeat_mode == 0:
            return 'Очередь  Текущий  **[**Ничего**]**'

        elif self.repeat_mode == 1:
            return 'Очередь  **[**Текущий**]**  Ничего'

        elif self.repeat_mode == 2:
            return '**[**Очередь**]**  Текущий  Ничего'

    def get_visual_eq_mode(self):
        """ Возвращает строку, содержащую в себе отображение текущего режима эквалайзера. """
        return '**[**Flat**]**  Boost  Piano  Metal'

    async def do_next(self, ctx, bot) -> None:
        """ Функция для перехода к следующему треку """
        try:
            self.waiting = True
            with async_timeout.timeout(300):
                track = self.queue.get()
        except asyncio.TimeoutError:
            # Если плеер не работал в течении 5 минут, то произойдет отключение плеера
            return await self.teardown()

        # Запуск трека
        await self.play(track)
        self.waiting = False

        # Запуск контроллера
        await self.invoke_controller(self.ctx, bot)

    async def invoke_controller(self, ctx: commands.Context, bot) -> None:
        """ Функция для вызова контроллера с кнопками """

        while ctx.voice_client:
            if self.updating:
                return

            self.updating = True
            # view = Controller()

            if not self.controller:
                # Если нету сообщения с кнопочками, то создаём новое
                self.controller = InteractiveController(ctx=ctx, bot=bot, embed=self.build_embed())
                await self.controller.start()

            elif not await self.is_position_fresh(ctx):
                # Если текущее сообщение с кнопочками не актуально
                try:
                    # Удалить текущее сообщение
                    await self.controller.message.delete()
                except:
                    pass

                # Построить новый эмбед, запустить новый контроллер
                embed = self.build_embed()
                self.controller = InteractiveController(ctx=ctx, bot=bot, embed=self.build_embed())
                await ctx.send(f'плеер потерялся, отправляю новый', delete_after=5)
                await self.controller.start()

            else:
                # В любом другом случае
                # Построить новый эмбед
                embed = self.build_embed()
                try:
                    # Обновить сообщение с новым ембедом
                    await self.controller.message.edit(content=None, embed=embed)
                except:
                    pass

            self.updating = False
            await asyncio.sleep(2)

    def build_embed(self) -> typing.Optional[discord.Embed]:
        """ Функция, которая возвращает эмбед плеера """

        if self._current is not None and self.is_paused():
            state = f'**[ПАУЗА]({self._current.uri})**'
        elif self._current is not None and self.is_playing():
            state = f'**[ИГРАЕТ]({self._current.uri})**'
        else:
            state = f'**[НЕ ИГРАЕТ](https://nespace.ru)**'

        if self._current is not None:
            thumbnail_parse_preview = self._current.thumb
        else:
            thumbnail_parse_preview = None

        # Отображение основной информации о плеере
        line = ''
        # line += f'{chr(8291)}⠀<:RINO_music_dj:1145505160718733322> **Диджей**: `N/A`\n'
        line += f'{chr(8291)}⠀ 🔹 **Громкость**: {int(self._volume)}%\n'
        line += f'{chr(8291)}⠀ 🔹 **Эквалайзер**: {self.get_visual_eq_mode()}\n'
        line += f'{chr(8291)}⠀ 🔹 **Повторение**: {self.get_visual_repeat_mode()}\n'

        # Красивое отображение названия трека и его длительности, а также requester'а
        line += '\n'
        line += f'{chr(8291)}⠀{state} **➨** {self.get_track_title_with_uri_str(self._current) if self.is_playing() or self.is_paused() else "_очередь пуста..._"}\n'
        line += f'{chr(8291)}⠀`{self.get_current_and_total_duration_str() if self.is_playing() or self.is_paused() else "--:--:--/--:--:--"} {self.visual_duration() if self.is_playing() or self.is_paused() else ""}`\n'
        # if self.is_playing() or self.is_paused():
        #     line += f'{chr(8291)}⠀_Добавил:_ `N/A`\n'
        
        # Обработка очереди треков
        line += '\n'
        line += f'{chr(8291)}⠀ ◯ **СЛЕДУЮЩИЕ**: \n'
        if len(self.get_entries()) == 0:
            line += f'{chr(8291)}⠀⠀⠀_очередь пуста..._\n'
        else:
            if len(self.get_entries()) > 5:
                for track_in_queue in range(5):
                    _entrie = self.get_entries()[track_in_queue]
                    line += f'{chr(8291)}⠀{self.get_total_duration_str(_entrie)} [{_entrie.title[:28]}{"..." if len(_entrie.title) >= 29 else ""}]({_entrie.uri})\n'
                line += f'{chr(8291)}⠀⠀⠀⠀_И ещё {len(self.get_entries())-5}_\n'
            else:
                for _entrie in self.get_entries():
                    line += f'{chr(8291)}⠀{self.get_total_duration_str(_entrie)} [{_entrie.title[:28]}{"..." if len(_entrie.title) >= 29 else ""}]({_entrie.uri})\n'

        # Последние действия
        line += '\n'
        line += f'{chr(8291)}⠀ ◯ **ПОСЛЕДНИЕ ДЕЙСТВИЯ**:\n'
        if len(self.last_action) == 0:
            line += f'{chr(8291)}⠀⠀⠀_тут ничего нет..._\n'
        else:
            # Переворачиваем словарь
            reversed_data = dict(reversed(self.last_action.items()))

            # Если сохранено более 5 действий
            if len(reversed_data) > 5:
                count = 0
                for key, value in reversed_data.items():
                    if count < 5:
                        line += f'{value}\n'
                        count += 1
                    else:
                        break
                line += f'{chr(8291)}⠀⠀⠀⠀_И ещё {len(reversed_data)-5}_\n'
            # Если сохранено менее 5 действий
            else:
                all_items = [reversed_data[i] for i in reversed_data]
                for item in all_items:
                    line += f'{item}\n'

        # Генерация эмбеда
        embed = discord.Embed()
        embed.color = discord.Color.from_str('#2b2d31')
        embed.description = line
        embed.set_author(name='RINO Music Player v0.8.1', icon_url='https://imgur.com/INvVb0h.gif')
        embed.set_footer(text=f'version: 1.3.2⠀⠀⠀⠀⠀⠀dev: z3r0x1ch⠀⠀⠀⠀⠀⠀ping: {self._ping}')
        # embed.set_image(url='https://i.imgur.com/aBeQrmQ.gif')
        embed.set_thumbnail(url=thumbnail_parse_preview)

        return embed

    async def is_position_fresh(self, ctx) -> bool:
        """ Функция для проверки актуальности текущего сообщения с кнопочками. """
        try:
            async for message in ctx.channel.history(limit=3):
                if message.id == self.controller.message.id:
                    return True
        except (discord.HTTPException, AttributeError):
            return False

        return False

    async def teardown(self):
        """ Функция, которая полностью останавливает воспроизведение музыки и плеер. """
        self.queue.clear()
        await self.disconnect(force=True)
        await self.controller.message.delete()
