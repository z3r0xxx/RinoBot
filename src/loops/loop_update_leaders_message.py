# -*- coding: utf-8 -*-
# created by zrx.

import discord
from tabulate import tabulate
from discord.ext import commands


class RinoLoopUpdateLeadersMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1145530571196465233
        self.message_id = 1145531319057649674
        self.getEmoji = {
            1: "🥇",
            2: "🥈",
            3: "🥉",
            4: "🏅",
            5: "🏅",
            6: "🏅",
            7: "🏅",
            8: "🏅",
            9: "🏅",
            10: "🏅",
            11: "🎖️",
            12: "🎖️",
            13: "🎖️",
            14: "🎖️",
            15: "🎖️",
            16: "🎖️",
            17: "🎖️",
            18: "🎖️",
            19: "🎖️",
            20: "🎖️",
            21: "🎖️",
            22: "🎖️",
            23: "🎖️",
            24: "🎖️",
            25: "🎖️",
        }

    @commands.command()
    async def hueta(self, ctx:commands.Context):
        """ . """

        try:
            # channel = self.bot.get_channel(self.channel_id)
            # message = await channel.fetch_message(self.message_id)

            line = '\n\n'
            line += f'{chr(8291)}⠀⠀_Вся отображаемая статистика показана за 5 суток_\n'
            line += f'{chr(8291)}⠀⠀_Страница обновляется каждые 40 секунд_\n\n'

            name1 = '`zrx'.ljust(21)
            name2 = '`Махест'.ljust(21)
            table_headers = ['`NAME', 'EXP', 'MSG/EDIT/DEL', 'VOICE/JIN`']
            table_items = [[name1, 40628, '523 143 50', '128 14`'], [name2, 23190, '396 32 4', '130 4`']]
            table = tabulate(table_items, table_headers, tablefmt="plain")

            line += f'{table}'

            line_field1 = ''
            line_field1 += f'🔹 **Общий опыт:** `139325`\n'
            line_field1 += f'🔹 **Общее время в войсе:** `16 часов 3 минуты`\n'
            line_field1 += f'🔹 **Подключений к войсу:** `59`\n\n'
            line_field1 += f'🔹 **Средняя длина сообщения:** `25`\n'
            line_field1 += f'🔹 **Всего сообщений:** `4141`\n'
            line_field1 += f'🔹 **Изменённых:** `336`\n'
            line_field1 += f'🔹 **Удалённых:** `221`'

            line_field2 = ''

            embed = discord.Embed()
            embed.color = discord.Color.from_str('#2b2d31')
            embed.description = line
            embed.set_author(name='20 САМЫХ АКТИВНЫХ УЧАСТНИКОВ ИЗ 100')
            embed.add_field(name='ОБЩАЯ СТАТИСТИКА ЗА ПОСЛЕДНИЕ 5 СУТОК', value=line_field1, inline=False)
            embed.add_field(name='ОНЛАЙН | СТАТУСЫ', value=line_field2, inline=False)
            embed.set_footer(text='API: 10ms')

            await ctx.send(embed=embed)
        except Exception as e:
            print(e)


    @commands.command()
    async def lead(self, ctx:commands.Context):
        """ . """

        table = list()
        table.append([self.getEmoji[1], f"``{1:02d} ", "523", "143", "50", "128", "14   ``", "<:RINO_stop:1146953100201050183> Чашечка с залупой"])
        table.append([self.getEmoji[2], f"``{2:02d} ", "396", "32", "4", "130", "4    ``", "<:RINO_stop:1146953100201050183> Махест"])
        table.append([self.getEmoji[3], f"``{3:02d} ", "858", "52", "40", "66", "3    ``", "<:RINO_stop:1146953100201050183> Курица"])
        table.append([self.getEmoji[4], f"``{4:02d} ", "784", "44", "20", "34", "3    ``", "<:RINO_stop:1146953100201050183> MP"])
        table.append([self.getEmoji[5], f"``{5:02d} ", "330", "9", "4", "0", "0    ``", "<:RINO_stop:1146953100201050183> panniqi"])
        table.append([self.getEmoji[6], f"``{6:02d} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{7:02d} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{8:02d} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{9:02d} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{10} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{11} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{12} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{13} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{14} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{15} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{16} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{17} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{18} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{19} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])
        table.append([self.getEmoji[6], f"``{20} ", "128", "11", "5", "92", "5    ``", "<:RINO_stop:1146953100201050183> Львумба"])

        line_leaders_table = ''
        line_leaders_table += f':crown:  ‌‌‍‍‌‌**N**  **MSG**  ‌‌‍‍ ‍**EDIT**  **DEL**  ‌‌‍‍**VС** **JOIN**\n'
        line_leaders_table += f'{tabulate(table, disable_numparse=True, tablefmt="plain")}'

        line_avg_statistic = ''
        line_avg_statistic += f'🔹 **Общий опыт:** `139325`\n'
        line_avg_statistic += f'🔹 **Общее время в войсе:** `16 часов 3 минуты`\n'
        line_avg_statistic += f'🔹 **Подключений к войсу:** `59`\n\n'
        line_avg_statistic += f'🔹 **Средняя длина сообщения:** `25`\n'
        line_avg_statistic += f'🔹 **Всего сообщений:** `4141`\n'
        line_avg_statistic += f'🔹 **Изменённых:** `336`\n'
        line_avg_statistic += f'🔹 **Удалённых:** `221`'
        
        line_field2 = ''

        embed = discord.Embed()
        embed.color = discord.Color.from_str('#2b2d31')
        embed.description = line_leaders_table
        embed.set_author(name='20 САМЫХ АКТИВНЫХ УЧАСТНИКОВ ИЗ 100')
        embed.add_field(name='ОБЩАЯ СТАТИСТИКА ЗА ПОСЛЕДНИЕ 5 СУТОК', value=line_avg_statistic, inline=False)
        embed.add_field(name='ОНЛАЙН | СТАТУСЫ', value=line_field2, inline=False)
        embed.set_footer(text=f'API: {self.bot.latency * 100}s')

        await ctx.send(embed=embed)

        # def getTopUsersText(from1, to1, timeout):
        #     cursor.execute(f"SELECT user_id, user_lvl, user_xp, countMessages, editedMessages, deletedMessages, countJoin FROM guild_users WHERE guild_id = {ctx.guild.id} ORDER BY user_lvl DESC, user_xp DESC LIMIT {from1}, {to1}")
        #     members = cursor.fetchall()
        #     members_in_guild = []
        #     members_not_in_guild = []
        #     ctxguildmembers = []
        #     for i in ctx.guild.members:
        #         if not i.bot:
        #             ctxguildmembers.append(i.id)
        #     for member_obj in members:
        #         if member_obj[0] in ctxguildmembers:
        #             members_in_guild.append(member_obj)
        #         elif member_obj[0] not in ctxguildmembers:
        #             members_not_in_guild.append(member_obj)

        #     timeout = time.time() + timeout
        #     members_count = len(ctxguildmembers) if len(ctxguildmembers) < 25 else 25
        #     while len(members_in_guild) != members_count:
        #         if time.time() > timeout:
        #             raise Exception('Time is out!')
        #         cursor.execute(f"SELECT user_id, user_lvl, user_xp, countMessages, editedMessages, deletedMessages, countJoin FROM guild_users WHERE guild_id = {ctx.guild.id} ORDER BY user_lvl DESC, user_xp DESC LIMIT {len(members_in_guild) + len(members_not_in_guild)}, {to1 - len(members_not_in_guild)}")
        #         members = cursor.fetchall()
        #         for member_obj in members:
        #             if member_obj[0] in ctxguildmembers:
        #                 members_in_guild.append(member_obj)
        #                 if len(members_in_guild) == 25:
        #                     break
        #             elif member_obj[0] not in ctxguildmembers:
        #                 members_not_in_guild.append(member_obj)
        #     return members_in_guild


        # topMembersNewList = getTopUsersText(0, 25, 5)

        # table = list()

        # for counter2, i in enumerate(topMembersNewList, 1):
        #     user_id = i[0]
        #     lvl = i[1]
        #     xp = i[2]
        #     new_lvl = i[1] + 1
        #     countMessages = i[3]
        #     editedMessages = i[4]
        #     deletedMessages = i[5]
        #     countJoin = i[6]
        #     countMessages = 0 if countMessages == None else countMessages
        #     editedMessages = 0 if editedMessages == None else editedMessages
        #     deletedMessages = 0 if deletedMessages == None else deletedMessages
        #     countJoin = 0 if countJoin == None else countJoin

            # countJoinLength = len(str(countJoin))
            # if countJoinLength == 5:
            #     countJoin = f"{countJoin}"
            # elif countJoinLength == 4:
            #     countJoin = f"{countJoin} "
            # elif countJoinLength == 3:
            #     countJoin = f"{countJoin}  "
            # elif countJoinLength == 2:
            #     countJoin = f"{countJoin}   "
            # elif countJoinLength == 1:
            #     countJoin = f"{countJoin}    "

        #     user = self.bot.get_user(user_id)

        #     table.append([self.getEmoji[counter2], f"``{counter2:02d} ", f"{lvl}", f"{countMessages}", f"{editedMessages}", f"{deletedMessages}", f"{countJoin}``", f"{user.mention}"])

        # embed.description += f"{tabulate(table, disable_numparse=True, tablefmt='plain')}\n"


async def setup(bot):
    await bot.add_cog(RinoLoopUpdateLeadersMessage(bot))
