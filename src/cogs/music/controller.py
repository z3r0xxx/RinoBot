from discord.ext import commands

import enum
import typing
import discord
from cogs.music.player import Player

class RINO_stop(discord.ui.Button['InteractiveController']):
    def __init__(self, ctx, bot):
        super().__init__(style=discord.ButtonStyle.red, emoji='<:RINO_stop:1146953100201050183>', custom_id='RINO_stop_button')

        self.context = ctx
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: InteractiveControllerView = self.view

        if not interaction.user.voice:
            return await interaction.response.send_message(f"{interaction.user.mention} Вы должны находиться в голосовом канале!")

        if not interaction.guild.voice_client:
            player: Player = await interaction.user.voice.channel.connect(cls=Player)
        else:
            player: Player = interaction.guild.voice_client

        if not player.is_connected():
            return

        await player.teardown()
        await interaction.response.send_message('плеер был остановлен', delete_after=10)

class RINO_pause(discord.ui.Button['InteractiveController']):
    def __init__(self, ctx, bot):
        super().__init__(style=discord.ButtonStyle.grey, emoji='<:RINO_pause:1146953094907834458>', custom_id='RINO_pause_button')

        self.context = ctx
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: InteractiveControllerView = self.view

        if not interaction.user.voice:
            return await interaction.response.send_message(f"{interaction.user.mention} Вы должны находиться в голосовом канале!")

        if not interaction.guild.voice_client:
            player: Player = await interaction.user.voice.channel.connect(cls=Player)
        else:
            player: Player = interaction.guild.voice_client

        if not player.is_connected():
            return

        if player.is_paused():
            # УБРАТЬ ПАУЗУ
            await player.resume()
            await interaction.response.send_message('отжата пауза', delete_after=5)
            return

        await player.pause()
        await interaction.response.send_message('плеер был поставлен на паузу', delete_after=10)

class RINO_next(discord.ui.Button['InteractiveController']):
    def __init__(self, ctx, bot):
        super().__init__(style=discord.ButtonStyle.grey, emoji='<:RINO_next:1146953093150421103>', custom_id='RINO_next_button')

        self.context = ctx
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: InteractiveControllerView = self.view

        if not interaction.user.voice:
            return await interaction.response.send_message(f"{interaction.user.mention} Вы должны находиться в голосовом канале!")

        if not interaction.guild.voice_client:
            player: Player = await interaction.user.voice.channel.connect(cls=Player)
        else:
            player: Player = interaction.guild.voice_client

        if not player.is_connected():
            return

        await interaction.response.send_message('был пропущен трек', delete_after=5)
        await player.stop()
        return

class RINO_shuffle(discord.ui.Button['InteractiveController']):
    def __init__(self, ctx, bot):
        super().__init__(style=discord.ButtonStyle.grey, emoji='<:RINO_shuffle:1146953098644963328>', custom_id='RINO_shuffle_button')

        self.context = ctx
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: InteractiveControllerView = self.view

        if not interaction.user.voice:
            return await interaction.response.send_message(f"{interaction.user.mention} Вы должны находиться в голосовом канале!")

        if not interaction.guild.voice_client:
            player: Player = await interaction.user.voice.channel.connect(cls=Player)
        else:
            player: Player = interaction.guild.voice_client

        if not player.is_connected():
            return

        await interaction.response.send_message('данная функция в разработке...')

class RINO_repeat(discord.ui.Button['InteractiveController']):
    def __init__(self, ctx, bot):
        super().__init__(style=discord.ButtonStyle.grey, emoji='<:RINO_repeat:1146953097281802250>', custom_id='RINO_repeat_button')

        self.context = ctx
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: InteractiveControllerView = self.view

        if not interaction.user.voice:
            return await interaction.response.send_message(f"{interaction.user.mention} Вы должны находиться в голосовом канале!")

        if not interaction.guild.voice_client:
            player: Player = await interaction.user.voice.channel.connect(cls=Player)
        else:
            player: Player = interaction.guild.voice_client

        if not player.is_connected():
            return

        if player.repeat_mode == 0:
            print(1)
            player.repeat_mode = 1

        elif player.repeat_mode == 1:
            player.repeat_mode = 2

        elif player.repeat_mode == 2:
            player.repeat_mode = 0
            
        await interaction.response.send_message('был измёнен режим повторения', delete_after=10)


class InteractiveControllerView(discord.ui.View):
    children: typing.List[RINO_stop]
    children: typing.List[RINO_pause]
    children: typing.List[RINO_next]
    children: typing.List[RINO_shuffle]
    children: typing.List[RINO_repeat]

    def __init__(self, ctx, bot):
        super().__init__(timeout=None)

        self.ctx = ctx
        self.bot = bot

        self.add_item(RINO_stop(self.ctx, self.bot))
        self.add_item(RINO_pause(self.ctx, self.bot))
        self.add_item(RINO_next(self.ctx, self.bot))
        self.add_item(RINO_shuffle(self.ctx, self.bot))
        self.add_item(RINO_repeat(self.ctx, self.bot))


class InteractiveController():
	def __init__(self, ctx, bot=None, embed=None):
		self.ctx = ctx
		self.bot = bot
		self.embed = embed

		self.message = None

	async def start(self) -> None:
		""" Запускает плеер с кнопочками. """
		
		self.message = await self.ctx.send(embed=self.embed, view=InteractiveControllerView(self.ctx, self.bot))
