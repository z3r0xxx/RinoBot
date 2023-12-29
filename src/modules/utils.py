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


def word_form(value:int=None, words:list=None) -> None:
    """
    Функция для определения падежа текста в зависимости от заданного числа

    :param value: Число, в зависимости от которого будет определяться падеж текста
    :param words: Список слов
    :return: None
    """

    # words = ['серверов', 'сервер', 'сервера']
    if (value % 100 in (11, 12, 13, 14)) or (value % 10 in (5, 6, 7, 8, 9, 0)):
        return words[0]
    return words[1] if (value % 10 == 1) else words[2]
