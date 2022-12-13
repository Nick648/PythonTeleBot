import requests
from datetime import datetime
import time
import telebot
from telebot import types
import json
from auth_data import token, chat_id_father, login_password
from prepared_answers import welcome_ans, help_ans, idk_ans, hiw_ans, pas_req, cor_pas, err_pas_ans, sec_hint

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


def get_exchange_rate():
    course_usd = requests.get('https://cbr.ru/cursonweek/?DT=&val_id=R01235&_=1670870731958').json()
    course_eur = requests.get('https://cbr.ru/cursonweek/?DT=&val_id=R01239&_=1670870731959').json()
    course_cny = requests.get('https://cbr.ru/cursonweek/?DT=&val_id=R01375&_=1670870731960').json()
    curs_usd = course_usd[0]['curs']
    curs_eur = course_eur[0]['curs']
    curs_cny = course_cny[0]['curs']
    ans = f'The current exchange rate from the site https://cbr.ru/\n'
    ans += f"{' ' * 8}{datetime.now().strftime('%Y.%m.%d  %H:%M')}\n"
    ans += f"{' ' * 4}USD: 1$ = {curs_usd:.4f}  ->  1₽ = {1 / curs_usd:.4f}\n" \
           f"{' ' * 4}EUR: 1€ = {curs_eur:.4f}  ->  1₽ = {1 / curs_eur:.4f}\n" \
           f"{' ' * 4}CNY: 1¥ = {curs_cny / 10:.4f}  ->  1₽ = {10 / curs_cny:.4f}"
    return ans


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
    print(f'{authorized_users=}')
    count_secret = dict()
    bot = telebot.TeleBot(token_bot)

    # @bot.message_handler(func=lambda m: True)
    # def echo_all(message):
    #     bot.reply_to(message, message)  # Ответ на сообщение
    #     report_father(bot, message)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, welcome_ans)
        if not check_authorized_user(message):
            time.sleep(1)
            file_photo_tool = open('data/for_pas_1.jpg', 'rb')
            bot.send_photo(message.chat.id, file_photo_tool, '<i>Tooltip</i>', parse_mode='HTML')
            bot.send_message(message.chat.id, pas_req)
        else:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)  # , row_width=2
            btn1 = types.KeyboardButton("Кто это создал?")
            kb.add(btn1)
            bot.send_message(message.chat.id,
                             "And again, I am glad to welcome you, you have sorted out the first problem!")
            bot.send_message(message.chat.id, 'Buttons have been added to the functionality', reply_markup=kb)
        report_father(bot, message)

    @bot.message_handler(commands=["help"])
    def help_message(message):
        if not check_authorized_user(message):
            bot.send_message(message.chat.id, 'Maybe you should enter the password first...')
        else:
            bot.send_message(message.chat.id, help_ans + "\nMaybe it's worth starting over...")
        report_father(bot, message)

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        text_mes = message.text.strip().lower()
        if not check_authorized_user(message):
            if text_mes == login_password:
                for i in range(1, 4):
                    bot.send_message(message.chat.id, f"H{'m' * (i + 1)}")
                    time.sleep(i * 0.5)
                bot.reply_to(message, cor_pas)
                change_verify_user(message)
            else:
                bot.delete_message(message.chat.id, message.id)
                bot.send_message(message.chat.id, err_pas_ans)
        elif text_mes == "rate":
            try:
                bot.send_message(
                    message.chat.id,
                    get_exchange_rate()
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn...Something was wrong..."
                )
        elif message.text == "Кто это создал?":
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
        elif text_mes == "secret":
            file_photo_tool = open('data/rebus.png', 'rb')
            bot.send_photo(message.chat.id, file_photo_tool, '<i>Rebus</i>', parse_mode='HTML')
        elif text_mes == "расскажи секрет":
            key_count_secret = str(message.chat.id)
            if key_count_secret in count_secret:
                if count_secret[key_count_secret] == 3:
                    bot.send_message(message.chat.id, f"Okay, think about who did it and what you want to tell him...")
                    count_secret[key_count_secret] += 1
                elif count_secret[key_count_secret] > 3:
                    bot.send_message(message.chat.id, sec_hint)
                else:
                    count_secret[key_count_secret] += 1
                    bot.send_message(message.chat.id, f"Hmmmmm, maybe try again... I want more")
            else:
                count_secret[key_count_secret] = 1
                bot.send_message(message.chat.id, f"Hmmmmm, maybe try again... I want more")
        elif text_mes == "я тебя люблю" or text_mes == "я люблю тебя":
            bot.send_message(message.chat.id, f"Yes, you're close, but you need to be in English... "
                                              f"I told you at the beginning, you will need knowledge of English")
        elif text_mes == "i love you":
            bot.send_message(message.chat.id, f"And he loves you")
            video_file = open('data/end.mp4', 'rb')
            bot.send_video_note(message.chat.id, video_file)
            bot.send_message(message.chat.id, f"This is the end of the game, thanks for participating")
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
