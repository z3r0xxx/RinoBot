# -*- coding: utf-8 -*-
# created by zrx.

import time
import openai
import random
import discord
from discord import app_commands
from discord.ext import commands
from modules.logs import logger
from modules.Bot import MyBot


class RinoCommandGpt(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.openai_API_KEY = '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'
        openai.api_key = self.openai_API_KEY

    @app_commands.command(name="ask-gpt", description="Спросите что-нибудь у ChatGPT-3.5")
    @app_commands.rename(q='вопрос')
    async def ping(self, interaction:discord.Interaction, *, q:str):     
        # await interaction.response.send_message(content='*Пожалуйста, подожди 10-20 секунд, я пишу ответ на твой запрос...*')
        await interaction.response.defer()
        wh = interaction.followup

        start_time = time.time()
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": q}])
        end_time = time.time()
        execution_time = end_time - start_time

        embed = discord.Embed()
        embed.color = discord.Color.from_str('#2b2d31')
        embed.description = chat_completion.choices[0].message.content
        embed.set_author(name='Ответ от ChatGPT', icon_url='https://i.imgur.com/HgG5NLE.png')
        embed.set_footer(text=f'Время выполнения: {execution_time:.2f}с')

        await wh.send(content=f'**Запрос**: {q}', embed=embed)


async def setup(bot):
    await bot.add_cog(RinoCommandGpt(bot))
