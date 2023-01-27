import re

from Elements import *
from Errors import *


def lexer_1(characters: str):  # lexer
    position = 0
    pos = 0  # for re
    commands = []
    while pos < len(characters):
        # print(f"pos >> {pos}")
        match = None
        for token_exp in el_expression:  # token_expression from Tokens.py
            pattern, tag = token_exp
            regex = re.compile(pattern)  # use reg
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                # print(f"{match=}")
                if tag:
                    element = Element(tag, text, position)  # Object
                    # print(element)  # element.toString()
                    commands.append(element)
                    position += 1
                break
        if not match:
            # print('Illegal character: %s\n' % characters[pos])
            text = f"Неизвестный символ на {position} позиции: {characters[pos]}"
            return text
        else:
            pos = match.end(0)  # new pos
    return commands


def lexer(characters: str):  # lexer_1 - using
    characters = characters.replace(',', ' ').strip().split()
    position = 0
    commands = []
    for character in characters:
        match = None
        for token_exp in el_expression:  # token_expression from Elements.py
            pattern, tag = token_exp
            character_lower = character.lower()
            match = re.fullmatch(pattern, character_lower)
            if match:
                # print(f"{match=}, {match[0]}, {match.end(0)}")  # Is text match
                if tag:
                    element = Element(tag, character, position)  # Object
                    # print(element)  # element.toString()
                    commands.append(element)
                    position += 1
                break
        if not match:
            text_er = f"Неизвестная команда на {position} позиции: {character}\n"
            text_er += f"Для вывода подсказки по вводу команд введите help cmd"
            return Error("LexerNotFound", text_er)
    return commands


def research_select(cmd_list: list):
    return cmd_list


def parser(cmd_list: list, cur_dir: str):
    first_cmd = cmd_list[0].getTypeToken()
    len_cmd = len(cmd_list)
    if first_cmd == 'LS':
        if len_cmd == 1:
            return print('just ls')
        elif len_cmd == 2 and cmd_list[1].getTypeToken() == 'PATH':
            return print('ls path')
        elif cmd_list[1].getTypeToken() == 'SELECT':
            return research_select(cmd_list[1:])
        else:
            text_er = f"Команда 'ls' введена неправильно!\nДля вывода подсказки по написанию команды введите help ls"
            return Error("CmdLS", text_er)
    elif first_cmd == 'CD':
        pass
    elif first_cmd == 'INFO':
        pass
    elif first_cmd == 'SIZE':
        pass
    elif first_cmd == 'COUNT':
        pass
    elif first_cmd == 'TREE':
        pass
    elif first_cmd == 'WALK':
        pass
    elif first_cmd == 'SELECT':
        pass
    elif first_cmd == 'INSERT':
        pass
    elif first_cmd == 'HELP':
        pass
    elif first_cmd == 'SEND':
        pass
    else:
        text_er = f"Нет команды, начинающийся с этой с этой: {cmd_list[0].getValue()}\n"
        text_er += f"Для вывода подсказки по написанию команд введите help cmd"
        return Error("ParserNotFound", text_er)


if __name__ == '__main__':
    while True:
        com = input("Com line >>> ")
        if not com:
            break
        cmds = lexer(com)
        if isinstance(cmds, list):
            print('\t', cmds)
            cmds = parser(cmds, '')
            if isinstance(cmds, list):
                print('\t', cmds)
