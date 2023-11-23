import os
import json
import discord
import datetime

def convert_message(member:discord.Member=None, message:discord.Message=None, text:str=None):
    guild = member.guild if member is not None else message.guild
    user = member if member is not None else message.author

    result = text.replace('{{member}}', f'{str(user)}')
    result = result.replace('{{member.id}}', f'{user.id}')
    result = result.replace('{{member.mention}}', f'{user.mention}')

    return result
