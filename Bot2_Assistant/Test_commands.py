import json
import os

from LexerParser import *
from auth_data import main_directory
from colorama import Fore, Style

# colorama.init()
# Const module colorama
GREEN = Fore.LIGHTGREEN_EX
GREEN_1 = Fore.GREEN
RED = Fore.LIGHTRED_EX
YELLOW = Fore.LIGHTYELLOW_EX
WHITE = Fore.LIGHTWHITE_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
CYAN = Fore.LIGHTCYAN_EX
RESET = Style.RESET_ALL


def test_join():
    cur_dir = main_directory
    while True:
        cd = input('join >>> ')
        if not cd:
            exit()
        try:
            if cd == '..':
                cur_dir = cur_dir[:cur_dir.rfind('\\')]
                new_path = cur_dir
            else:
                new_path = os.path.join(cur_dir, cd)
            if os.path.exists(new_path):
                print(f"\t{new_path=} -> {GREEN}True{RESET}")
                print(f"{os.listdir(new_path)=}")
                cur_dir = new_path
            else:
                print(f"\t{new_path=} -> {RED}False{RESET}")
        except Exception as ex:
            print(f"Name = {type(ex).__name__}; Type = {type(ex)}; Ex = {ex}")


def test_commands() -> None:
    with open("data/test_commands.txt", "r") as read_file:
        commands_list = read_file.read().strip()
    commands_list = commands_list.split('\n')
    test_logs = dict()
    for cmd_line in commands_list:
        if cmd_line:
            line_logs = dict()
            try:
                ans = lexer(cmd_line)
                # ans = lexer_1(cmd_line)
                if isinstance(ans, list):
                    line_logs["Answer"] = True
                    list_ans = dict()
                    for item_ans in ans:
                        typ, val = item_ans.getTypeToken(), item_ans.getValue()
                        list_ans[val] = typ
                    line_logs["Returned"] = list_ans
                    print(f"{cmd_line} -> {GREEN}True{RESET}")
                    try:
                        parser(ans, '')
                    except Exception as ex:
                        pass
                else:
                    line_logs["Answer"] = False
                    line_logs["Returned"] = ans.error_des()
                    print(f"{cmd_line} -> {RED}False{RESET}")
            except Exception as ex:
                line_logs["Answer"] = False
                line_logs["Type ex"] = type(ex).__name__
                line_logs["Exception"] = str(ex)
                print(f"{cmd_line} -> {RED}False{RESET}")
                print(f"{type(ex).__name__} -> {ex}")
            finally:
                test_logs[cmd_line] = line_logs

    with open(file=r"data/test_logs.json", mode="w", encoding="utf-8") as write_file:
        json.dump(test_logs, write_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # test_join()
    test_commands()
