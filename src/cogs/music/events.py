# -*- coding: utf-8 -*-
# created by zrx.

import wavelink
from discord.ext import commands
from modules.logs import logger

class RinoCogMusicEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node:wavelink.Node) -> None:
        """ on_wavelink_node_ready """
        logger.info(f"Подключение к ноде: {node.id}(RU) выполнено и готово к использованию.")
    
    @commands.Cog.listener()
    async def on_wavelink_track_event(self, payload:wavelink.TrackEventPayload) -> None:
        """ on_wavelink_track_event """
        pass
    
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload:wavelink.TrackEventPayload) -> None:
        """ on_wavelink_track_start """
        logger.info(f"Сервер {payload.player.guild.id} Воспроизведён трек {payload.player.current}")
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload:wavelink.TrackEventPayload) -> None:
        """ on_wavelink_track_end """
        # https://discord.com/channels/@me/692703311131967518/944484268992757780
        logger.info(f"Сервер {payload.player.guild.id} event track end")
    
    @commands.Cog.listener()
    async def on_wavelink_websocket_closed(self, payload:wavelink.TrackEventPayload) -> None:
        """ on_wavelink_websocket_closed """
        logger.info(f"Сервер {payload.player.guild.id} Воспроизведение закончилось, плеер отключён")


async def setup(bot):
    await bot.add_cog(RinoCogMusicEvents(bot))
