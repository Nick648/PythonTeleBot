import requests
from datetime import datetime
import time
import telebot
from telebot import types
import json
from auth_data import token, chat_id_father, login_password
from assistant_answers import welcome_ans, help_ans, idk_ans, hiw_ans, pas_req, cor_pas

with open(r"data/authorized_users.json", "r") as read_file:
    authorized_users = json.load(read_file)


def update_data_json():
    with open(r"data/authorized_users.json", "w") as write_file:
        json.dump(authorized_users, write_file, indent=4)


def check_authorized_user(message):
    key = str(message.from_user.id)
    if key in authorized_users:
        return authorized_users[key]['verify']  # == True
    else:
        time_create = datetime.fromtimestamp(int(message.date)).strftime('%d-%m-%Y %H:%M:%S')
        print(f'{time_create} -> Create {message.from_user.id} -> {message}')
        dict_info = dict()
        dict_info['first_name'] = message.from_user.first_name
        dict_info['last_name'] = message.from_user.last_name
        dict_info['username'] = message.from_user.username
        dict_info['language_code'] = message.from_user.language_code
        dict_info['chat_type'] = message.chat.type
        dict_info['verify'] = False
        authorized_users[key] = dict_info
        update_data_json()
    return False


def change_verify_user(message, value=True):
    key = str(message.from_user.id)
    try:
        authorized_users[key]['verify'] = value
        update_data_json()
    except Exception as ex:
        print(f'Error in change_verify_user -> {type(ex).__name__} : {ex}')


def report_father(bot, message):
    if message.chat.id != chat_id_father:
        time_report = datetime.now().strftime('%d.%m.%Y %H:%M')
        report = f'Dad, at {time_report} id={message.chat.id} wrote to me\n'
        report += f'First_name: {str(message.from_user.first_name)}\n'
        report += f'Last_name: {str(message.from_user.last_name)}\n'
        report += f'Username: {str(message.from_user.username)}\n'
        report += f'Language_code: {str(message.from_user.language_code)}\n'
        report += f'Date Unix: {str(message.date)}\n'
        date_rep = datetime.fromtimestamp(int(message.date)).strftime('%d-%m-%Y %H:%M:%S')
        report += f'Date Win: {date_rep}\n'
        report += f'This is the text: {message.text}'
        bot.send_message(
            chat_id_father,
            report
        )
        # print(report)


def telegram_bot(token_bot):
    bot = telebot.TeleBot(token_bot)

    # @bot.message_handler(func=lambda m: True)
    # def echo_all(message):
    #     bot.reply_to(message, message)  # Ответ на сообщение
    #     report_father(bot, message)

    @bot.message_handler(commands=[""])  # CHECK!!!
    def start_message(message):
        bot.send_message(message.chat.id, welcome_ans)
        if not check_authorized_user(message):
            bot.send_message(message.chat.id, "Secret egg!")
        else:
            bot.send_message(message.chat.id, "Secret egg!")
        report_father(bot, message)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, welcome_ans)
        if not check_authorized_user(message):
            bot.send_message(message.chat.id, pas_req)
        else:
            bot.send_message(message.chat.id, "And again, I am glad to welcome you!")
        report_father(bot, message)

    @bot.message_handler(commands=["help"])
    def help_message(message):
        if not check_authorized_user(message):
            bot.send_message(message.chat.id, 'Maybe you should enter the password first...')
        else:
            bot.send_message(message.chat.id, help_ans)
        report_father(bot, message)

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if not check_authorized_user(message):
            bot.delete_message(message.chat.id, message.id)
            if message.text == login_password:
                for i in range(1, 4):
                    bot.send_message(message.chat.id, f"H{'m' * (i + 1)}")
                    time.sleep(i * 0.5)
                bot.reply_to(message, cor_pas)
                change_verify_user(message)
            else:
                bot.send_message(message.chat.id, "Hmm, that's the wrong answer...")
                bot.send_message(message.chat.id, "Think again!")

        text_mes = message.text.strip().lower()
        cmd_lines = message.text.strip().lower().split('\n')
        for cmd_line in cmd_lines:
            cmd_line = cmd_line.strip().split()
            research_cmd_line(cmd_line)

        if message.text == "Кто это создал?":
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("И что мне делать?")
            kb.add(btn1)
            bot.send_message(message.chat.id, hiw_ans, reply_markup=kb)

        elif message.text == "И что мне делать?":
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text='Подсказка',
                                              url='https://www.seekpng.com/png/detail/133-1335904_photo-top-secret-stamp-transparent.png')
            markup.add(btn1)
            bot.send_message(message.chat.id, "Maybe it's worth writing the word", reply_markup=markup)

        else:
            bot.send_message(message.chat.id, idk_ans)

        report_father(bot, message)
        # print(message, type(message))
        # bot.send_message(
        #     chat_id_father,
        #     message
        # )

        bot.polling()


if __name__ == '__main__':
    # print(get_exchange_rate())
    telegram_bot(token)
