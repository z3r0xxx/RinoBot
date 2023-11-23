# -*- coding: utf-8 -*-
# created by zrx.

import random
import discord
from discord import app_commands
from discord.ext import commands
from database import create_user, create_guild
from modules.logs import logger

class RinoOnMessageEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return

        create_user(message.author)
        create_guild(message.guild)

        if message.attachments:
            if random.randint(0, 2) == 2:
                logger.debug(f'рандом выпал на сервере {message.guild.name}')
                await message.reply(f'{message.author.mention}', file=discord.File(fp=open('gif.gif', 'rb')))
            return


async def setup(bot):
    await bot.add_cog(RinoOnMessageEvent(bot))
