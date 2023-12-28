# -*- coding: utf-8 -*-
# created by zrx.

import io 
import time
import discord
from discord.ext import commands
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
from database import get_user_leveling


class RinoCommandRankCard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['xp', 'ранг', 'rank', 'хп'])
    async def rank_card_command(self, ctx:commands.Context, member:discord.Member=None):
        """ Пользовательская команда для получения свой ранговой карточки или карточки другого участника сервера. """

        start_time = time.time()
        bot_latency = self.bot.latency*1000

        try:

            async with ctx.typing():
                font1 = ImageFont.truetype("cards/fonts/MONTSERRAT-REGULAR.TTF", size=66)
                font2 = ImageFont.truetype("cards/fonts/MONTSERRAT-REGULAR.TTF", size=25)
                font3 = ImageFont.truetype("cards/fonts/MONTSERRAT-ITALIC.TTF", size=35)

                width, height = 700, 639
                background_color = (255, 255, 255, 0)
                blank_image = Image.new("RGBA", (width, height), background_color)

                user_nick = ctx.author.display_name
                user_name = ctx.author.name
                if member is not None:
                    user_nick = member.display_name
                    user_name = member.name
                
                if len(user_nick) > 10:
                    user_nick = user_nick[:10] + '...'
                if len(user_name) > 10:
                    user_name = user_name[:10] + '...'

                avatar = ctx.author.avatar if ctx.author.avatar is not None else ctx.author.display_avatar
                if member is not None:
                    avatar = member.avatar if member.avatar is not None else member.display_avatar
                avatar_bytes = await avatar.read()

                foreground_image = Image.open(io.BytesIO(avatar_bytes))
                foreground_image = foreground_image.resize((165, 165))

                x, y = 45, 33

                blank_image.paste(foreground_image, (x, y), foreground_image)

                overlay_image_path = "cards/blank_card_v2.png"
                overlay_image = Image.open(overlay_image_path)

                overlay_x, overlay_y = 0, 0

                blank_image.paste(overlay_image, (overlay_x, overlay_y), overlay_image)

                idraw = ImageDraw.Draw(blank_image)
                idraw.text((56, 223), user_nick, fill='white', font=font1)
                idraw.text((57, 296), user_name, fill=(161, 161, 161), font=font2)
                idraw.text((57, 385), '0/1100', fill='white', font=font3)

                # Уровень
                text_width1 = idraw.textlength('1', font=font3)
                idraw.text((640-text_width1, 385), '1', fill='white', font=font3)

                # Подключений на текущем сервере
                voice_connections = get_user_leveling(ctx.author.id, ctx.guild.id).voice_connections
                if member is not None:
                    voice_connections = get_user_leveling(member.id, ctx.guild.id).voice_connections
                text_width2 = idraw.textlength(str(voice_connections), font=font3)
                idraw.text((640-text_width2, 540), str(voice_connections), fill='white', font=font3)

                # Время в войсе
                all_voice_time_ = get_user_leveling(ctx.author.id, ctx.guild.id).all_voice_time
                if member is not None:
                    all_voice_time_ = get_user_leveling(member.id, ctx.guild.id).all_voice_time
                all_voice_time = timedelta(seconds=all_voice_time_)
                idraw.text((57, 540), str(all_voice_time), fill='white', font=font3)

                result_image_path = "cards/123.png"
                blank_image.save(result_image_path)

                foreground_image.close()
                overlay_image.close()

                end_time = time.time()
                excecution_time = end_time - start_time

                await ctx.send(file=discord.File(open(result_image_path, 'rb')))
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(RinoCommandRankCard(bot))
