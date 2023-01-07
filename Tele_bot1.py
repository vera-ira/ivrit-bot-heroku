# ПЕРВЫЕ ШАГИ РАБОТЫ С БОТОМ
#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
import telebot
from alphabet_detector import AlphabetDetector  # библеотека опрелеяет тип букв. Мне нужны иврит и кириллица
import xlrd
import json
import os

import constants1
from telebot_utils import log
from telebot_utils import alert_new_user
from telebot_utils import send_table
from telebot_utils import always_open_file
from telebot_utils import make_batton_imper
from telebot_utils import make_battons
from telebot_utils import pool_answers
from telebot_utils import pool_lists


"""
тут прописываю, все, что должно выполняться при каждом запуске скрипта
"""

server = Flask(__name__) #эта чсть нужна для вебхука
bot = telebot.TeleBot(constants1.token) #эта чать создает объект бот
bot.send_message(115496560, 'Бот перезагрузился') # оповещает админа о перезагрузке
#list = always_open_file()#это функция, которая открывает файл с глаголами. нужно это делать в самом начале, иначе ужодит время на его закрузку. Ниже две строки и открывают этот файл.
words_verb = xlrd.open_workbook('./Pealim_FINAL1.xlsx')
list = words_verb.sheet_by_index(0)

#audio = open('test.mp3', "rb")
#audio2 = open('CQADAgAD6gEAAr81gEsnVEWpXkjmWwI', "rb")
#bot.send_audio(chat_id=115496560, audio="CQADAgAEAwAC-gW4S9fRNse-pNeqAg")

#audio=@audio.mp3;type=audio/mpeg'
#thumb = open("111.jpeg","rb")
#thumb=@example.jpeg;type=image/jpeg'
#i = {file_id:"AgADAgADVqoxG2pjSEi_6Ui-I7UONPqqUQ8ABGuJL3LWD_86iBUBAAEC", width:100, height:60}
#bot.send_audio(chat_id=115496560, audio=audio,performer="performer",title="title", thumb="111.jpeg")
#bot.send_message(chat_id=115496560,text="текст"+"[.](https://habrastorage.org/r/w60/webt/5b/64/28/5b6428dc0f25c575004839.jpeg)",parse_mode='Markdown')

"""
ниже три строки для получения данных о последнем обновлении
"""
#upd = bot.get_updates()
#last_upd = upd[-1]
#print(last_upd)

@bot.message_handler(commands=['info'])
def handle_text(message):
    alert_new_user(message, bot)
    answer = 'Я бот. И знаю почти все глаголы в иврите. Люблю делиться знаниями. Если у тебя есть предложения или вопросы к моему создателю, напиши сюда - @vera_ira.'
    bot.send_message(message.chat.id, answer)
    log(message, answer)

@bot.message_handler(commands=['start'])
def handle_text(message):
    alert_new_user(message, bot)
    user_markup = telebot.types.ReplyKeyboardMarkup(True,False)
    user_markup.row('/start','/info')
    hi_name = str('Привет, '+message.from_user.first_name+'!\nОтправляй мне любой глагол.')
    bot.send_message(message.chat.id, hi_name, reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handle_text(message):
    """
    это временно отключено
    """
    alert_new_user(message, bot)
    remove_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Клавиатуру свернули, Но ты ее всегда можешь развернуть обратно.', reply_markup = remove_markup)

@bot.message_handler(content_types=['audio'])
def handle_text(message):
    """
    это временно отключено
    """
    print(message)

@bot.message_handler(content_types=['text'])
def handle_text(message, list=list):
    print(message)
    alert_new_user(message, bot)
    ad = AlphabetDetector()

    if '*' in message.text:
        bot.send_message(message.chat.id, 'Я не знаю такого символа * . Введите запрос заново.', parse_mode='Markdown')

    elif ad.is_cyrillic(message.text) == False and ad.is_hebrew(message.text) == False:
        answer = 'Извините, я еще не знаю глагола "*' + message.text + '*".\nВы ввели текст на неизвестном мне языке.\nЯ понимаю Русский и עברית. Попробуй снова.'
        bot.send_message(message.chat.id, answer, parse_mode='Markdown')
        log(message, answer)

    elif ad.is_cyrillic(message.text) == True:#на кириллице
        status_searching = 'Ответа в файле нет.'#это удалить?
        id_answer_links = pool_lists(message.text, list, language="ru").get("id_answer_links")#pool_lists функция возвращает словарь с двумя списками и get получает нужный список
        id_maybe_answer_links = pool_lists(message.text, list, language="ru").get("id_maybe_answer_links")#pool_lists функция возвращает словарь с двумя списками и get получает нужный список
        pool_answers(message, message.text, id_answer_links, id_maybe_answer_links, status_searching, telebot, bot, list)

    elif ad.is_hebrew(message.text) == True:
        if ',' in message.text:
            answer = 'Вы написали несколько слов через запятую ",". Я могу найти только один глагол в одном запросе. Попробуй снова сделать запрос.'
            bot.send_message(message.chat.id, answer, parse_mode='Markdown')
            log(message, answer)
        else:
            status_searching = 'Ответа в файле нет.'  # это удалить?
            all_lists = pool_lists(message.text, list, language="he")#эта функция возвращает словарь с двумя списками.
            id_answer_links = all_lists.get("id_answer_links")
            id_maybe_answer_links = all_lists.get("id_maybe_answer_links")
            pool_answers(message, message.text, id_answer_links, id_maybe_answer_links, status_searching, telebot, bot, list)#функция, которая объединяет все ответы и отправляет нужное сообщение


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    этот декоратор обрабатывает все нажатые кнопки

    на это нужно обратить внимание. call.message указывает 
    на нажатую кнопку из чата с ботом а не инлайн (из другого чата)
    """
    if call.message:
        if call.data == '88888888':
            wrong_verb = call.message.json.get('text')[call.message.json.get('entities')[0].get('offset'):call.message.json.get('entities')[0].get('offset')+call.message.json.get('entities')[0].get('length')]
            text_after_button = 'Я запомнил "*'+wrong_verb+'*" и если такой глагол существует, я внесу в мой словарь в ближайшие дни.'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text_after_button,parse_mode='Markdown')
            """
            ниже уведомили админа
            """
            bot.send_message(chat_id=115496560, text="Пользователь "+call.message.from_user.first_name+" (id: "+str(call.message.from_user.id)+ " не нашел в нашей базе глагол -"+wrong_verb)

        elif 'id_botr' in call.data:
            call_data = call.data.split("-")#изначальнов кнопку вложили данные в формате id_botr-123456-test-123456. Поэтому сплитовали через тире и получили 4 объекта
            namber_id_botr = call_data[1]
            namber_id_msg_for_find = call_data[3]
            file = open("many_battons.json", "r")
            all_story_buttons = json.load(file)
            meter = 0
            for request in all_story_buttons:#тут будем искать нужный нам словарь с даными о собранных ответах в джейсоне
                if str(request["message.message_id"]) == str(namber_id_msg_for_find) and meter == 0:
                    status_searching = str(request["info_buttons"]["status_searching"])
                    id_maybe_answer_links = request["info_buttons"]["id_maybe_answer_links"]
                    key = make_battons(call.message, id_maybe_answer_links, status_searching, int(namber_id_botr), telebot, list)
                    meter += 1
                    continue
            if status_searching == 'Ответ в файле есть.':
                answer_for_report = 'Есть несколько подходящих ответов (борт-'+namber_id_botr+':\n-' + str(id_maybe_answer_links) + '\n'
                answer = "Есть несколько подходящих ответов:"
            else:
                answer = "Извините, я еще не знаю этого глагола. Возможно вы искали:"
                answer_for_report = 'Извините, я еще не знаю этого глагола. Возможно вы искали(борт-' + namber_id_botr + ':\n-' + str(id_maybe_answer_links) + '\n'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=answer, reply_markup=key)
            log(call.message, answer_for_report)

        elif "py_hy" in call.data:
            call_data = call.data.split("-")#изначальнов кнопку вложили данные в формате id_botr-123456-test-123456. Поэтому сплитовали через тире и получили 4 объекта
            id_py_hy = call_data[1]
            row = id_py_hy
            answer = send_table(row, list=list, kind_of_table="long+pyal_hyfal")
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=answer,
                                  parse_mode='Markdown',
                                  disable_web_page_preview=True)
            log(call.message, answer)

        elif 'id_imper' in call.data:
            ts_and_id = str(call.data[8:])
            row = int(ts_and_id)
            answer = send_table(row, list=list, kind_of_table="long")
            """
            если у глагола есть пассивная форма, 
            формируем кнопку для пассива иначе без кнопок
            """
            if str(list.row(int(ts_and_id))[179].value) != "":#тут проверяю, нужно ли мне снова присылкть кнопку пассива или нет.
                key = make_batton_imper(telebot, ts_and_id, add_buttons="passiva")
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=answer,
                                      reply_markup=key,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=answer,
                                      parse_mode='Markdown',
                                      disable_web_page_preview=True)
            log(call.message, answer)
        elif 'id_pay_audio' in call.data:
            audio_id = str(call.data[13:])
            bot.send_message(chat_id=call.message.chat.id, text="Функция прослушивания на стадии разработки.",parse_mode='Markdown')
            #bot.send_audio(chat_id=call.message.chat.id, audio=audio_id)
            #audio.close()
            #data_but_pay_audio = str("id_pay_audio-" + str("CQADAgAD6gEAAr81gEsnVEWpXkjmWwI"))
        else:
            ts = constants1.table_start
            ts_and_id = int(ts)+int(call.data)
            answer = send_table(ts_and_id, list=list, kind_of_table="short")
            if str(list.row(int(ts_and_id))[179].value) != "":
                key = make_batton_imper(telebot, str(ts_and_id), add_buttons="all")
            else:
                key = make_batton_imper(telebot, str(ts_and_id), add_buttons="imper")
            bot.send_message(call.message.chat.id, text=answer, reply_markup=key, parse_mode='Markdown',disable_web_page_preview=True)
            log(call.message, answer)


"""
НИЖЕ ЭТО ВСЕ ДЛЯ РАБОТЫ НА HEROKU
"""
@server.route('/' + constants1.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ivrit-bot.herokuapp.com/' + constants1.token)
    return "?", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #bot.polling(none_stop=True, interval=0)  # Функция, которая обновляет постоянно информацю с сервера.

"""
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)  # Функция, которая обновляет постоянно информацю с сервера.
"""

