# -*- coding: utf-8 -*-
# created by zrx.

import discord
from discord.ext import commands


class RinoCommandAvatar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx:commands.Context, member:discord.Member=None):
        """ Пользовательская команда для получения своего аватара или аватара участника сервера. """


        avatar = str(ctx.author.avatar) if ctx.author.avatar is not None else str(ctx.author.display_avatar)
        if member is not None:
            avatar = str(member.avatar) if member.avatar is not None else str(member.display_avatar)

        avatar_as_png = str(avatar)
        avatar_as_jpg = str(avatar.replace(".png", ".jpg"))
        avatar_as_webp = str(avatar.replace(".png", ".webp"))
        embed = discord.Embed()
        embed.color = discord.Color.from_str('#2b2d31')
        embed.title = f'Аватар {str(ctx.author.name)}'
        if member is not None:
            embed.title = f'Аватар {str(member.name)}'
        embed.description = f'[png]({avatar_as_png})⠀⠀|⠀⠀[jpg]({avatar_as_jpg})⠀⠀|⠀⠀[webp]({avatar_as_webp})'
        embed.set_image(url=avatar)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RinoCommandAvatar(bot))
