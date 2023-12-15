# -*- coding: utf-8 -*-
# created by zrx.

import os
import sys
import discord
import wavelink

from modules.logs import logger
from discord.ext import commands
from typing import List, Optional

TOKEN = 'NzIzMDg0NTQ4MTgyNzY5Njc1.GEXSV3.yJRTQ0Kqrj_UCtczoxhDl9CxviC_HQ6Kv36e3I'

def restart() -> None:
    """ Перезагрука проекта """
    os.execv(sys.executable, ['python'] + sys.argv)


class MyBot(commands.Bot):
    def __init__(
            self,
            *args,
            initial_extensions: List[str],
            testing_guild_id: Optional[int] = None,
            intents: discord.Intents,
            **kwargs
    ):
        super().__init__(*args, **kwargs, intents=intents)
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        self.config = None


    async def on_connect(self) -> None:
        """ on_connect """
        logger.info(f'Бот загружается.')
        logger.info(f'Соединение установлено.')

    async def setup_hook(self) -> None:
        """ setup_hook """
        
        # Подключение Wavelink Node
        node: wavelink.Node = wavelink.Node(uri='127.0.0.1:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self, nodes=[node])
        
        # Загрузка всех модулей бота
        counter = 0
        for extension in self.initial_extensions:
            # logger.debug('загружен модуль ' + str(extension))
            await self.load_extension(extension)
            counter += 1
        logger.info(f'Модули.  Загружено: {counter} из {len(self.initial_extensions)}  Сторонние: 1  Отключённые: 0')

        # Загрузка slash-команд
        # if self.testing_guild_id:
        #     guild = discord.Object(self.testing_guild_id)
        #     # We'll copy in the global commands to test with:
        #     self.tree.copy_global_to(guild=guild)
        #     # followed by syncing to the testing guild.
        #     synced = await self.tree.sync(guild=guild)
        #     logger.info(f'app_commands ({len(synced)}) успешно подключены')
