# -*- coding: utf-8 -*-
# created by zrx.

import random
import discord
from discord.ext import commands
from database import create_user, create_guild, get_user_info, get_guild_settings_notifications
from modules.utils import convert_message
from modules.logs import logger


class RinoOnMemberJoinEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        create_user(member)

        if member.bot:
            logger.debug(f'к серверу {member.guild.name} присоединился бот {member.name}')
            return

        if member.guild.id == 764486596543250452:
            channel = self.bot.get_channel(874080432088576071) 
            user_info = get_user_info(member.id, member.guild.id)
            if user_info is not None:
                await channel.send(f'{member.mention}, c возвращением! Все твои настройки и роли будут возвращены в ближайшее время, я уже занимаюсь этим!')
            else:
                await channel.send(f'{member.mention}, привет! Похоже, что ты тут новенький, я тебя раньше не видел. **Чувствуй себя как дома!**')
            return
        
        guild_id = member.guild.id
        settings = get_guild_settings_notifications(guild_id)
        
        if settings is None:
            create_guild(member.guild)

        is_welcome_guild = settings.is_welcome_guild
        is_welcome_dm = settings.is_welcome_dm
        welcome_channel_message = settings.welcome_channel_message
        welcome_dm_message = settings.welcome_dm_message
        welcome_channel_id = settings.welcome_channel_id

        if is_welcome_guild is True:
            channel = self.bot.get_channel(welcome_channel_id)

            if channel is None:
                return

            text = convert_message(member=member, text=welcome_channel_message)
            await channel.send(text)


async def setup(bot):
    await bot.add_cog(RinoOnMemberJoinEvent(bot))
