# -*- coding: utf-8 -*-
# created by zrx.

import discord
from discord.ext import commands
from database import add_voice_connection, create_user, create_guild
from modules.logs import logger

class RinoOnVoiceStateUpdateEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
        """ . """

        create_user(member)
        create_guild(member.guild)

        # Подключился к голосовому каналу
        if before.channel is None and after.channel:
            add_voice_connection(member.id, member.guild.id)
            logger.info(f'сервер {member.guild.id} новое подключение к войсу')


async def setup(bot):
    await bot.add_cog(RinoOnVoiceStateUpdateEvent(bot))
