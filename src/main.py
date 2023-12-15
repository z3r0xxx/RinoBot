# -*- coding: utf-8 -*-
# created by zrx.

import sys
import yaml
import time
import asyncio
import discord

from discord.ext import commands

from modules.Bot import MyBot
from modules.logs import logger
from modules.counter import total_lines, total_characters

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
exts = [
    'events.messages.on_message',
    'events.members.on_member_join',
    'events.voices.on_voice_state_update',
    'cogs.music.main',
    'cogs.music.events',
    'cogs.command_gpt',
    'cogs.command_avatar',
    'cogs.command_rank_card',
    'cogs.command_rtfm',
    'loops.loop_update_leaders_message'
]

bot = MyBot(commands.when_mentioned_or('!'), initial_extensions=exts, intents=intents)
bot.testing_guild_id = 764486596543250452
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Discord API"))


@bot.command()
async def load(ctx, cog) -> None:
    """
    Команда для загрузки кога (подмодуля) в боте.

    :param ctx: Контекст в котором вызывается команда (подробнее читать
    https://nextcordpy.readthedocs.io/en/neo-docs/ext/commands/api.html?highlight=context#nextcord.ext.commands.Context)
    :param cog: Подмодуль бота, который требуется загрузить
    :return: None
    """

    await ctx.message.delete()

    try:
        await bot.load_extension(f'{cog}')
    except Exception as e:
        await ctx.send(embed=discord.Embed(description=f'**ОШИБКА:** ```{e}```', color=0x8079fb))
    else:
        await ctx.send(embed=discord.Embed(description=f'Модуль `{cog}` успешно загружен в основную систему!',
                                           color=0x8079fb))


@bot.command()
async def unload(ctx, cog) -> None:
    """
    Команда для отгрузки кога (подмодуля) в боте.

    :param ctx: Контекст в котором вызывается команда (подробнее читать https://nextcordpy.readthedocs.io/en/neo-docs/ext/commands/api.html?highlight=context#nextcord.ext.commands.Context)
    :param cog: Подмодуль бота, который требуется отгрузить
    :return: None
    """

    await ctx.message.delete()

    try:
        await bot.unload_extension(f'{cog}')
    except Exception as e:
        await ctx.send(embed=discord.Embed(description=f'**ОШИБКА:** ```{e}```', color=0x8079fb))
    else:
        await ctx.send(embed=discord.Embed(description=f'Модуль `{cog}` успешно отключён от основной системы!',
                                        color=0x8079fb))


@bot.command()
async def reload(ctx, cog) -> None:
    """
    Команда для перезагрузки кога (подмодуля) в боте.

    :param ctx: Контекст в котором вызывается команда (подробнее читать https://nextcordpy.readthedocs.io/en/neo-docs/ext/commands/api.html?highlight=context#nextcord.ext.commands.Context)
    :param cog: Подмодуль бота, который требуется перезагрузить
    :return: None
    """

    await ctx.message.delete()

    try:
        await bot.unload_extension(f'{cog}')
        await bot.load_extension(f'{cog}')
    except Exception as e:
        await ctx.send(embed=discord.Embed(description=f'**ОШИБКА:** ```{e}```', color=0x8079fb))
    else:
        await ctx.send(embed=discord.Embed(description=f'Модуль `{cog}` успешно перезагружен!', color=0x8079fb))


@bot.event
async def on_ready():
    """ on_ready """
    logger.info(f'Бот загружен. Имя: {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("камни"))

# @bot.event
# async def on_command_error(ctx, error):
# 	"""
# 	Обработчик ошибок Дискорда.

# 	Без конструкции else игнорирует ошибки, не прописанные в обработчике
# 	С конструкцией else выводит только последнюю строку ошибки
# 	Это нужно ИСПРАВИТЬ!

# 	:param ctx: Контекст в котором вызывается команда (подробнее читать
# 	https://nextcordpy.readthedocs.io/en/neo-docs/ext/commands/api.html?highlight=context#nextcord.ext.commands.Context)
# 	:param error: Объект ошибки, которая произошла
# 	:return: None
# 	"""

# 	# await errors_handler.command_error_detection(ctx, error)


async def start():
    logger.debug(f'Python: {sys.version}')
    logger.debug(f'Discord.py: {discord.__version__}')
    
    with open('settings.yml', 'r') as file:
        data = yaml.safe_load(file)
    bot.config = data
    logger.debug('файл config.yml загружен.')
    logger.debug('найден конфиг config.yml, конфигурация загружена.')
    logger.debug('инициализация пакета source.')

    await bot.load_extension('jishaku')
    print()
    total_lines_, total_code_lines = total_lines
    total_characters_, total_code_characters_ = total_characters
    logger.info(f'Строк кода: {total_lines_}({total_code_lines}) Символов: {total_characters_}({total_code_characters_})')

    await bot.start(bot.config.get("TOKEN"))

    

if __name__ == "__main__":
    asyncio.run(start())
