import os
import glob
import linecache

def is_code_line(line):
    stripped_line = line.strip()
    return stripped_line and not stripped_line.startswith('#')

def count_lines(file_path):
    """
    Подсчитывает количество строк кода в файле, как с учетом, так и без учета комментариев.
    
    :param file_path: Путь к файлу.
    :return: Количество строк кода с комментариями, Количество строк кода без комментариев.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        total_lines = len(lines)
        code_lines = [line for line in lines if is_code_line(line)]
        code_lines_count = len(code_lines)
        return total_lines, code_lines_count

def count_lines_in_directory(directory, extension='.py'):
    """
    Подсчитывает общее количество строк кода с учетом и без учета комментариев
    во всех файлах с определенным расширением в директории и поддиректориях.
    
    :param directory: Путь к директории.
    :param extension: Расширение файлов для подсчета строк кода.
    :return: Общее количество строк кода с комментариями,
             Общее количество строк кода без комментариев.
    """
    total_lines_with_comments = 0
    total_lines_without_comments = 0

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(extension):
                file_path = os.path.join(root, file_name)
                lines_with_comments, lines_without_comments = count_lines(file_path)
                total_lines_with_comments += lines_with_comments
                total_lines_without_comments += lines_without_comments

    return total_lines_with_comments, total_lines_without_comments

def count_characters(file_path):
    """
    Подсчитывает общее количество символов в файле, как с учетом, так и без учета комментариев.
    
    :param file_path: Путь к файлу.
    :return: Количество символов с комментариями, Количество символов без комментариев.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return len(content), len(remove_comments(content))

def count_characters_in_directory(directory, extension='.py'):
    """
    Подсчитывает общее количество символов с учетом и без учета комментариев
    во всех файлах с определенным расширением в директории и поддиректориях.
    
    :param directory: Путь к директории.
    :param extension: Расширение файлов для подсчета символов.
    :return: Общее количество символов с комментариями,
             Общее количество символов без комментариев.
    """
    total_characters_with_comments = 0
    total_characters_without_comments = 0

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(extension):
                file_path = os.path.join(root, file_name)
                chars_with_comments, chars_without_comments = count_characters(file_path)
                total_characters_with_comments += chars_with_comments
                total_characters_without_comments += chars_without_comments

    return total_characters_with_comments, total_characters_without_comments

def remove_comments(code):
    """
    Удаляет комментарии из кода и возвращает код без комментариев.
    
    :param code: Код с комментариями.
    :return: Код без комментариев.
    """
    lines = code.split('\n')
    code_without_comments = []
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith('#'):
            code_without_comments.append(line)
    
    return '\n'.join(code_without_comments)


total_characters = count_characters_in_directory(r'C:\Users\arsen\OneDrive\Документы\DISCORD BOT')
total_lines = count_lines_in_directory(r'C:\Users\arsen\OneDrive\Документы\DISCORD BOT')