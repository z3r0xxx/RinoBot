# -*- coding: utf-8 -*-
# created by zrx.

import re
import enum
import discord
import wavelink
import datetime
from discord.ext import commands
from modules.logs import logger
from cogs.music.player import Player

class RepeatMode(enum.Enum):
    """ Класс, который хранит в себе информацию о режимах повтора трека/очереди. """
    NONE = 0
    ONE = 1
    ALL = 2


# class Track(Track):
#     __slots__ = ('requester', )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args)
#         self.requester: discord.Member = kwargs.get('requester')

URL_REG = re.compile(r'https?://(?:www\.)?.+')
URL_REG_SPOTIFY = re.compile('https://open.spotify.com?.+playlist/([a-zA-Z0-9]+)')

class RinoCogMusic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ctx = None

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        """ Ивент, который срабатывает когда заканчивается воспроизведение трека """

        player = payload.player
        # https://discord.com/channels/@me/692703311131967518/944484268992757780

        # await player.previous_tracks.put(Track(track.id, track.info, requester=player.bot.user))

        # if player.repeat_mode == RepeatMode.ONE:
        #     # Повторение: текущий трек

        #     print('выполнилось условие')
        #     player.queue.put_at_front(Track(track.id, track.info))
        #     return await player.play(player.queue.get())
        
        # elif player.repeat_mode == RepeatMode.ALL:
            # Повторение: текущая очередь
        # 	player.queue.put(Track(track.id, track.info, requester=player.bot.user))
        # 	return await player.play(player.queue.get())
        # else:

        if not player.queue.is_empty:
            # track = player.queue.get()
            # track.thumbnail_parse_preview = await track.fetch_thumbnail()
            # player.track = track

            return await player.do_next(self.ctx, self.bot)
        else:
            await self.context.send('воспроизведение закончилось, удаляю плеер...', delete_after=5)
            return await player.teardown()


    @commands.command(
        name='play',
        help='Добавить в очередь трек для воспроизведения',
        aliases=['p', 'п']
    )
    async def play(self, ctx:commands.Context, *, query:str):     
        """ Пользовательская команда для запуска воспроизведения музыки и самого плеера, либо для добавления трека в очередь. """

		# Удаляем сообщение пользователя
        await ctx.message.delete()

        if ctx.guild.id == 764486596543250452 and ctx.channel.id != 927931678498893864:
            return await ctx.send(f'Музыкальные команды можно использовать только в чате <#927931678498893864>!')
        if not ctx.author.voice:
            return await ctx.send(f"{ctx.author.mention} Вы должны находиться в голосовом канале!")
        
        if not ctx.voice_client:
            player: Player = await ctx.author.voice.channel.connect(cls=Player)
        else:
            player: Player = ctx.voice_client

        if not URL_REG.match(query):

            tracks = await wavelink.YouTubeTrack.search(query)
            if not tracks:
                await ctx.send(f'У меня не получилось найти треки по Вашему запросу!\n`{query}`', delete_after=10)
                return
            
            try:
                track = tracks[0]

                duration_time = str(datetime.timedelta(milliseconds=int(track.length))) # Длительность трека, преобразованная в нормальный читабельный вид
                title = track.title # Название трека
                channel_author = track.author # Автор трека
                thumbnail_parse_preview = await track.fetch_thumbnail()

                line = '\n'
                line += f'**Название трека**: {title}\n'
                line += f'**Автор**: `{channel_author}`\n'
                line += f'**Заказал трек**: {ctx.author.mention}\n'
                line += f'**Длительность**: `{duration_time}`\n'

                embed = discord.Embed(title="Добавлено в очередь")
                embed.color = discord.Color.from_str('#2b2d31')
                embed.description = line
                embed.set_thumbnail(url=thumbnail_parse_preview)

                # Если ничего не играет
                if not player.is_playing():
                    # Помещаем трек в очередь
                    player.ctx = ctx
                    player.dj = ctx.author
                    player.queue.put(track)
                    # Отправляем сгенерированный ембед
                    await ctx.send(embed=embed, delete_after=10)

                    # Сохраняем контекст для дальнейшего использования сообщения-плеера
                    self.ctx = ctx

                    # Запускаем следующий в очереди трек
                    await player.do_next(ctx, self.bot)
                else:
                    # Помещаем трек в очередь
                    player.queue.put(track)

                    # Отправляем сгенерированный ембед
                    await ctx.send(embed=embed, delete_after=10)

                # Добавляем последнее действие
                player.last_action[len(player.last_action)] = f'{chr(8291)}⠀ ▬ Добавлен трек'
            
            # Обработка ошибки
            except Exception as e:
                import traceback
                traceback_content = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                print(traceback_content)

        else:
            # Ссылка на плейлист spotify - https://open.spotify.com/playlist/4yXtxGVKg9TORvUxWT1QTS?si=14dead0603f04ad6
            # Ссылка на трек spotify - https://open.spotify.com/track/7EZC6E7UjZe63f1jRmkWxt?si=eb1407cbc31644a9
            # Ссылка на альбом spotify -  https://open.spotify.com/album/57CTEtNP8nNrGsJuzAkAvX?si=Tz9bbHkfQPaHfDDUzTMyAQ
            # Ссылка на плейлист y.music - https://music.yandex.ru/users/arsenykvasov/playlists/1000
            # Ссылка на трек y.music - https://music.yandex.ru/album/10502584/track/65057131
            # Ссылка на альбом y.music - https://music.yandex.ru/album/20067897

            # Ссылка на плейлист youtube - https://www.youtube.com/playlist?list=PLoMRqdQDW4fzczoc12mokMFlRdGcBBi5x
            if 'youtube' and 'playlist' in query:
                try:
                    playlist = await wavelink.YouTubePlaylist.search(query, node=player.current_node)
                    # player.queue.extend(elem for elem in playlist.tracks)

                    if not playlist:
                        await ctx.send(f'У меня не получилось найти плейлист по Вашему запросу!\n`{query}`', delete_after=10)
                        return

                    line = '\n'
                    line += f'**Название плейлиста**: {playlist.name}\n'
                    line += f'**Количество треков**: {len(playlist.tracks)}\n'
                    line += f'**Заказал трек**: {ctx.author.mention}\n'

                    embed = discord.Embed(title="Добавлено в очередь")
                    embed.color = discord.Color.from_str('#2b2d31')
                    embed.description = line

                    # Если ничего не играет
                    if not player.is_playing():
                        # Помещаем трек в очередь
                        player.ctx = ctx
                        player.dj = ctx.author
                        player.queue.extend(elem for elem in playlist.tracks)
                        # Отправляем сгенерированный ембед
                        await ctx.send(embed=embed, delete_after=10)

                        # Сохраняем контекст для дальнейшего использования сообщения-плеера
                        self.ctx = ctx

                        # Запускаем следующий в очереди трек
                        await player.do_next(ctx, self.bot)
                    else:
                        # Помещаем трек в очередь
                        player.queue.extend(elem for elem in playlist.tracks)

                        # Отправляем сгенерированный ембед
                        await ctx.send(embed=embed, delete_after=10)

                    # Добавляем последнее действие
                    player.last_action[len(player.last_action)] = f'{chr(8291)}⠀ Добавлен плейлист ({len(playlist.tracks)} треков)'

                except Exception as e:
                    import traceback
                    traceback_content = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    print(traceback_content)
            
            # Ссылка на трек youtue - https://www.youtube.com/watch?v=L3wKzyIN1yk
            elif 'youtube' in query:
                tracks = await wavelink.YouTubeTrack.search(query)
                if not tracks:
                    await ctx.send(f'У меня не получилось найти треки по Вашему запросу!\n`{query}`', delete_after=10)
                    return
                
                try:
                    track = tracks[0]

                    duration_time = str(datetime.timedelta(milliseconds=int(track.length))) # Длительность трека, преобразованная в нормальный читабельный вид
                    title = track.title # Название трека
                    channel_author = track.author # Автор трека
                    thumbnail_parse_preview = await track.fetch_thumbnail()

                    line = '\n'
                    line += f'**Название трека**: {title}\n'
                    line += f'**Автор**: `{channel_author}`\n'
                    line += f'**Заказал трек**: {ctx.author.mention}\n'
                    line += f'**Длительность**: `{duration_time}`\n'

                    embed = discord.Embed(title="Добавлено в очередь")
                    embed.color = discord.Color.from_str('#2b2d31')
                    embed.description = line
                    embed.set_thumbnail(url=thumbnail_parse_preview)

                    # Если ничего не играет
                    if not player.is_playing():
                        # Помещаем трек в очередь
                        player.ctx = ctx
                        player.dj = ctx.author
                        player.queue.put(track)
                        # Отправляем сгенерированный ембед
                        await ctx.send(embed=embed, delete_after=10)

                        # Сохраняем контекст для дальнейшего использования сообщения-плеера
                        self.ctx = ctx

                        # Запускаем следующий в очереди трек
                        await player.do_next(ctx, self.bot)
                    else:
                        # Помещаем трек в очередь
                        player.queue.put(track)

                        # Отправляем сгенерированный ембед
                        await ctx.send(embed=embed, delete_after=10)

                    # Добавляем последнее действие
                    player.last_action[len(player.last_action)] = f'{chr(8291)}⠀  ⠀Добавлен трек'
                
                # Обработка ошибки
                except Exception as e:
                    import traceback
                    traceback_content = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    print(traceback_content)


    @commands.command(
        name='connect',
        help='Подключиться к голосовому каналу',
    )
    async def connect(self, ctx: commands.Context) -> None:
        """ Пользовательская команда для подключения к голосовому каналу. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        return await ctx.send('сори бро, команда пока не работает, используй `!play`', delete_after=10)


    @commands.command(
        name='repeat',
        help='Изменить режим повторения композиции',
    )
    async def repeat(self, ctx: commands.Context) -> None:
        """ Пользовательская команда для изменения режима повторения. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        return await ctx.send('сори бро, команда пока не работает', delete_after=10)


    @commands.command(
        name='volume',
        help='Изменить громкость плеера',
    )
    async def volume(self, ctx: commands.Context, value:str=None) -> None:
        """ Пользовательская команда для изменения громкости плеера. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        if ctx.guild.id == 764486596543250452 and ctx.channel.id != 927931678498893864:
            return await ctx.send(f'Музыкальные команды можно использовать только в чате <#927931678498893864>!')

        if value is None:
            return await ctx.send('Укажи новую громоксть в пределах от `0%` до `100%`!', delete_after=10)
        try:
            int(value)
        except:
            return await ctx.send('**Нужно отправить число!**', delete_after=10)
        
        if not 0 < int(value) < 100:
            return await ctx.send('Укажи новую громоксть в пределах от `0%` до `100%`!', delete_after=10)
        
        if not ctx.voice_client:
            return await ctx.send(f'Сейчас ничего не играет!', delete_after=5)
        else:
            player: Player = ctx.voice_client
        
        await player.set_volume(int(value))
        return await ctx.send(f'Установлена новая громкость `{int(value)}%`', delete_after=5)


    @commands.command(
        name='stop',
        help='Остановить воспроизведение музыки',
        aliases=['s', 'с']
    )
    async def stop(self, ctx: commands.Context) -> None:
        """ Пользовательская команда для остановки воспроизведения музыки и самого плеера. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        if ctx.guild.id == 764486596543250452 and ctx.channel.id != 927931678498893864:
            return await ctx.send(f'Музыкальные команды можно использовать только в чате <#927931678498893864>!')

        if not ctx.voice_client:
            return await ctx.send(f'Сейчас ничего не играет!', delete_after=5)
        else:
            player: Player = ctx.voice_client

        await ctx.send('останавливаю плеер...', delete_after=5)
        await player.teardown()


    @commands.command(
        name='skip',
        help='Включить следующий трек в очереди',
        aliases=['n']
    )
    async def skip(self, ctx: commands.Context) -> None:
        """ Пользовательская команда для пропуска трека. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        if ctx.guild.id == 764486596543250452 and ctx.channel.id != 927931678498893864:
            return await ctx.send(f'Музыкальные команды можно использовать только в чате <#927931678498893864>!')

        if not ctx.voice_client:
            return await ctx.send(f'Сейчас ничего не играет!', delete_after=5)
        else:
            player: Player = ctx.voice_client

        # Добавляем последнее действие
        player.last_action[len(player.last_action)] = f'{chr(8291)}⠀  ⠀Пропущен трек '
        
        await ctx.send('пропускаю трек...', delete_after=5)
        await player.stop()


    @commands.command(
        name='seek',
        help='Позволяет перемотать текущий трек'
    )
    async def seek(self, ctx: commands.Context, *, position=None) -> None:
        """ Пользовательская команда для перемотки трека. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        if ctx.guild.id == 764486596543250452 and ctx.channel.id != 927931678498893864:
            return await ctx.send(f'Музыкальные команды можно использовать только в чате <#927931678498893864>!')

        if not ctx.voice_client:
            return await ctx.send(f'Сейчас ничего не играет!', delete_after=5)
        else:
            player: Player = ctx.voice_client

        if position is None:
            current_position = player.position
            await player.seek(current_position + 15000)
        else:
            current_position = player.position
            await player.seek(current_position + int(position)*1000)

        await ctx.send('перематываю...', delete_after=5)


    @commands.command(
        name='pause',
        help='Приостановить воспроизведение музыки',
    )
    async def pause(self, ctx:commands.Context):
        """ Пользовательская команда для приостановки плеера. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        if ctx.guild.id == 764486596543250452 and ctx.channel.id != 927931678498893864:
            return await ctx.send(f'Музыкальные команды можно использовать только в чате <#927931678498893864>!')

        if not ctx.voice_client:
            return await ctx.send(f'Сейчас ничего не играет!', delete_after=5)
        else:
            player: Player = ctx.voice_client
        
        await player.pause()
        # Добавляем последнее действие
        player.last_action[len(player.last_action)] = f'{chr(8291)}⠀  ⠀Приостановлено'
        await ctx.send('поставил воспроизведение на паузу...', delete_after=5)


    @commands.command()
    async def resume(self, ctx:commands.Context):
        """ Пользовательская команда для продолжения воспроизведения музыки. """

        # Удаляем сообщение пользователя
        await ctx.message.delete()

        if ctx.guild.id == 764486596543250452 and ctx.channel.id != 927931678498893864:
            return await ctx.send(f'Музыкальные команды можно использовать только в чате <#927931678498893864>!')

        if not ctx.voice_client:
            return await ctx.send(f'Сейчас ничего не играет!', delete_after=5)
        else:
            player: Player = ctx.voice_client
        
        await player.resume()
        # Добавляем последнее действие
        player.last_action[len(player.last_action)] = f'{chr(8291)}⠀  ⠀Возобновлено'
        await ctx.send('продолжил воспроизведение музычки...', delete_after=5)


async def setup(bot):
    await bot.add_cog(RinoCogMusic(bot))
