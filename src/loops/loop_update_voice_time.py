# -*- coding: utf-8 -*-
# created by zrx.

from modules.logs import logger
from discord.ext import commands, tasks
from database import create_user, add_voice_time

class RINO_update_voice_time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.on_voice_state_update_task.start()

    def cog_unload(self):
        self.on_voice_state_update_task.cancel()

    @tasks.loop(seconds=5)
    async def on_voice_state_update_task(self):
        """ Функция, которая подсчитывает количество времени, проведённого в войсе """

        for guild in self.bot.guilds:
            for member in guild.members:
                create_user(member)

                if member.bot:
                    pass

                elif member.voice:
                    # если пользователь находится в войсе
                    # if len(member.voice.channel.members) == 1:
                    # (если пользователь находится один в войсе)
                    if member.voice.afk:
                        # если пользователь находится в АФК канале
                        pass
                    else:
                        logger.info(f"пользователь {str(member)} на сервере {guild.name} получил +5")
                        add_voice_time(member.id, guild.id)
                else:
                    pass


async def setup(bot):
    await bot.add_cog(RINO_update_voice_time(bot))
