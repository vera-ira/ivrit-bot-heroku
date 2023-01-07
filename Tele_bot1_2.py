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


server = Flask(__name__)
bot = telebot.TeleBot(constants1.token)
words_verb = xlrd.open_workbook('./Pealim_FINAL1.xlsx')
list = words_verb.sheet_by_index(0)

bot.send_message(115496560, 'Бот перезагрузился')
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

def send_table(message, row, kind_of_table):
    """
    Эта функция формирует ответ со всеми формамт
    глагола в виде таблицы.
    """
    row = int(row)
    def part2(colum, row):
        """
        Эта функция выполняет проверку на наличие
        в базе вторых вариантов написания одного глагола,
        написания с огласовками и транскрипции.
        """
        print('Вошли в def part2')
        i = ''
        if '~' in list.row(row)[colum + 1].value:
            i = (list.row(row)[colum + 1].value + ' {' + list.row(row)[colum + 2].value + '}')
        else:
            i = (' {' + list.row(row)[colum + 2].value + '}')
        ii = ''
        if list.row(row)[colum + 3].value != '':
            if '~' in list.row(row)[colum + 4].value:
                ii = ('; ' + list.row(row)[colum + 3].value + list.row(row)[colum + 4].value + ' {' + list.row(row)[colum + 5].value + '}')
            else:
                ii = ('; ' + list.row(row)[colum + 3].value + ' {' + list.row(row)[colum + 5].value + '}')
        return i + ii
#     эту чать ниже стоит пересмотреть. Стоит ли ее вызывать каждый раз в строчке?
#    def form_one_line(pronoun, indent, index):
#        return pronoun + indent + '*' + list.row(row)[index].value + '*' + part2(index, row)

    I = 'אֲנִי'
    YOU_M = 'אַתָּה'
    YOU_W = 'אַתְּ'
    HE = 'הוּא'
    SHE = 'הִיא'
    WE = 'אֲנַחְנוּ'
    YOU_MM = 'אַתֶּם'
    YOU_WW = 'אַתֶּן'
    THEY_MM = 'הֵם'
    THEY_WW = 'הֵן'
    Z = 'ז.'
    N = 'נ.'
    ZR = 'ז"ר'
    NR = 'ז"ר'
    answer1 = ('ע"ב ' + "[@ivrit_bot](https://t.me/ivrit_bot)\n"
            + '*' + list.row(row)[3].value + '*' + '\n' +
            'инфинитив: ' + '*' + list.row(row)[4].value + '*' + part2(4,row) + '\n'+
            #'инфинитив: *%s*%s\n' % (list.row(row)[4].value, part2(4,row))+
            'биньян: ' + '*' + list.row(row)[10].value+ '*' + '\n'+
            'корень: ' + '*' + list.row(row)[11].value + '*' + '\n'+
            '*наст. вр.*:' + '\n'
            + Z + '-       ' + '*' + list.row(row)[17].value + '*' + part2(17,row)+'\n'
            + N + '-       ' + '*' + list.row(row)[23].value + '*' + part2(23,row)+'\n'
            + ZR + '-     ' + '*' + list.row(row)[29].value + '*' + part2(29,row)+'\n'
            + NR + '-     ' + '*' + list.row(row)[35].value + '*' + part2(35,row)+'\n'
            '*прошед. вр.*:' + '\n'
            + I + '-      ' + '*' + list.row(row)[41].value + '*' + part2(41,row)+ '\n'
            + YOU_M + '-   ' + '*' + list.row(row)[47].value + '*' + part2(47,row)+ '\n'
            + YOU_W + '-      ' + '*' + list.row(row)[53].value + '*' + part2(53,row)+ '\n'
            + HE + '-     ' + '*' + list.row(row)[59].value + '*' + part2(59,row)+ '\n'
            + SHE + '-     ' + '*' + list.row(row)[65].value + '*' + part2(65,row)+ '\n'
            + WE + '-  ' + '*' + list.row(row)[71].value + '*' + part2(71,row)+ '\n'
            + YOU_MM + '-   ' + '*' + list.row(row)[77].value + '*' + part2(77,row)+ '\n'
            + YOU_WW + '-     ' + '*' + list.row(row)[83].value + '*' + part2(83,row)+ '\n'
            + THEY_MM + '/' + THEY_WW + '- ' + '*' + list.row(row)[89].value + '*' + part2(89,row)+ '\n'
            '*буд. вр.*:' + '\n'
            + I + '-     ' + '*' + list.row(row)[95].value + '*' + part2(95,row)+ '\n'
            + YOU_M + '-   ' + '*' + list.row(row)[101].value + '*' + part2(101,row)+ '\n'
            + YOU_W + '-      ' + '*' + list.row(row)[107].value + '*' + part2(107,row)+ '\n'
            + HE + '-     ' + '*' + list.row(row)[113].value + '*' + part2(113,row)+ '\n'
            + SHE + '-     ' + '*' + list.row(row)[119].value + '*' + part2(119,row)+ '\n'
            + WE + '-  ' + '*' + list.row(row)[125].value + '*' + part2(125,row)+ '\n'
            + YOU_MM + '-   ' + '*' + list.row(row)[131].value + '*' + part2(131,row)+ '\n'
            + YOU_WW + '-     ' + '*' + list.row(row)[137].value + '*' + part2(137,row)+ '\n'
            + THEY_MM + '/' + THEY_WW + '- ' + '*' + list.row(row)[143].value + '*' + part2(143,row) + '\n')
    answer2 = ('*пов. накл.*:' + '\n'
            + Z + '-       ' + '*' + list.row(row)[155].value.replace("!", "") + '*' + part2(155,row).replace("!", "")+'\n'#при помощи .replace("!", "") убираем восклицательный знак
            + N + '-       ' + '*' + list.row(row)[161].value.replace("!", "") + '*' + part2(161,row).replace("!", "")+'\n'#при помощи .replace("!", "") убираем восклицательный знак
            #+ ZR + '-     ' + '*' + list.row(row)[167].value.replace("!", "") + '*' + part2(167,row).replace("!", "")+'\n'#при помощи .replace("!", "") убираем восклицательный знак
            + NR + '-     ' + '*' + list.row(row)[173].value.replace("!", "") + '*' + part2(173,row).replace("!", "")+'\n')#при помощи .replace("!", "") убираем восклицательный знак
            #newstr = oldstr.replace("M", "")

    footer = ('\n' +'_Сообщить об ошибке -_'+"[@vera_ira](https://t.me/vera_ira)")
    if kind_of_table == 'short':
        answer = answer1
    elif kind_of_table == 'long':
        answer = answer1+answer2+footer
    elif kind_of_table == 'long+pyal_hyfal':
        id_py_hy = str(list.row(row)[179].value)
        for row_py_hy in range(4502, 5714):
            if str(list.row(row_py_hy)[2].value) == str(id_py_hy):
                answer3 = ('*страдательный залог:*\n'
                    '*биньян*: ' + list.row(row_py_hy)[10].value + '\n'
                    '*наст. вр.*:' + '\n'
                    + Z + '-       ' + '*' + list.row(row_py_hy)[17].value + '*' + part2(17,row_py_hy) + '\n'
                    + N + '-       ' + '*' + list.row(row_py_hy)[23].value + '*' + part2(23,row_py_hy) + '\n'
                    + ZR + '-     ' + '*' + list.row(row_py_hy)[29].value + '*' + part2(29,row_py_hy) + '\n'
                    + NR + '-     ' + '*' + list.row(row_py_hy)[35].value + '*' + part2(35,row_py_hy) + '\n'
                    '*прошед. вр.*:' + '\n'
                    + I + '-      ' + '*' + list.row(row_py_hy)[41].value + '*' + part2(41,row_py_hy) + '\n'
                    + YOU_M + '-   ' + '*' + list.row(row_py_hy)[47].value + '*' + part2(47,row_py_hy) + '\n'
                    + YOU_W + '-      ' + '*' + list.row(row_py_hy)[53].value + '*' + part2(53,row_py_hy) + '\n'
                    + HE + '-     ' + '*' + list.row(row_py_hy)[59].value + '*' + part2(59,row_py_hy) + '\n'
                    + SHE + '-     ' + '*' + list.row(row_py_hy)[65].value + '*' + part2(65,row_py_hy) + '\n'
                    + WE + '-  ' + '*' + list.row(row_py_hy)[71].value + '*' + part2(71,row_py_hy) + '\n'
                    + YOU_MM + '-   ' + '*' + list.row(row_py_hy)[77].value + '*' + part2(77,row_py_hy) + '\n'
                    + YOU_WW + '-     ' + '*' + list.row(row_py_hy)[83].value + '*' + part2(83,row_py_hy) + '\n'
                    + THEY_MM + '/' + THEY_WW + '- ' + '*' + list.row(row_py_hy)[89].value + '*' + part2(89,row_py_hy) + '\n'
                    '*буд. вр.*:' + '\n'
                    + I + '-     ' + '*' + list.row(row_py_hy)[95].value + '*' + part2(95,row_py_hy) + '\n'
                    + YOU_M + '-   ' + '*' + list.row(row_py_hy)[101].value + '*' + part2(101,row_py_hy) + '\n'
                    + YOU_W + '-      ' + '*' + list.row(row_py_hy)[107].value + '*' + part2(107,row_py_hy) + '\n'
                    + HE + '-     ' + '*' + list.row(row_py_hy)[113].value + '*' + part2(113,row_py_hy) + '\n'
                    + SHE + '-     ' + '*' + list.row(row_py_hy)[119].value + '*' + part2(119,row_py_hy) + '\n'
                    + WE + '-  ' + '*' + list.row(row_py_hy)[125].value + '*' + part2(125,row_py_hy) + '\n'
                    + YOU_MM + '-   ' + '*' + list.row(row_py_hy)[131].value + '*' + part2(131,row_py_hy) + '\n'
                    + YOU_WW + '-     ' + '*' + list.row(row_py_hy)[137].value + '*' + part2(137,row_py_hy) + '\n'
                    + THEY_MM + '/' + THEY_WW + '- ' + '*' + list.row(row_py_hy)[143].value + '*' + part2(143,row_py_hy) + '\n')
        answer = answer1 + answer2 + answer3 + footer
    return answer

def make_batton_imper(message, ts_and_id, add_buttons):
    """
    Эта функция формирукт дополнительные кнопкуи
    в ответ с таблицей глагола.
    Кнопка для повелительного наклонения и пассивной формы.
    """
    key = telebot.types.InlineKeyboardMarkup(row_width=2) # задаем ее тип. Это клвиатура инлайн
    data_but_imper = str("id_imper" + str(ts_and_id))
    but_imper = telebot.types.InlineKeyboardButton(text=" + Повелительное наклонение.",
                                                   callback_data=data_but_imper)
    data_but_py_hy = str("id_py_hy-" + str(ts_and_id))
    but_py_hy = telebot.types.InlineKeyboardButton(text=" + Страдательный залог.",
                                                   callback_data=data_but_py_hy)
    data_but_pay_audio = str("id_pay_audio-" + str("CQADAgAEAwAC-gW4S9fRNse-pNeqAg"))
    but_pay_audio = telebot.types.InlineKeyboardButton(text="Слушать 🎧",
                                                       callback_data=data_but_pay_audio)

    if add_buttons == "passiva":
        key.add(but_py_hy)
    elif add_buttons == "imper":
        key.row(but_imper)
    elif add_buttons == "all":
        key.row(but_imper, but_py_hy)

    key.row(but_pay_audio)
    return key

#kb1 = Types.InlineKeyboardMarkup(row_width=1) # самая длинная кнопка
#kb2 = Types.InlineKeyboardMarkup(row_width=2) # деление пополам
#kb3 = Types.InlineKeyboardMarkup(row_width=3) # деление на три равных кнопки
def make_battons(message, id_maybe_answer_links, status_searching, namber_bort):
    """
    Эта функция нужна в случае если в базе найдено
    несколько подходящих ответов.
    Функция формирует список подходящих ответов.

    """
    sb = constants1.sum_buttons_on_botr
    if (int(namber_bort*sb))<=(int(len(id_maybe_answer_links))): #определяем сколько на этом борту напечатать кнопок. Если борт не последний, то печатаем кол-во sb. Оно забито в константах и изменить его можно там.
        botr = sb
    else:
        botr = sb-((int(namber_bort * sb))-(int(len(id_maybe_answer_links)))) #Если это последний борт, то тогда из sb вычитаем кол-во пустыхх мест.
    """
    ниже определим, с какой кнопки начнем и какой закончим.
    """
    start = (int(namber_bort*sb)-int(sb))
    stop = (start+botr)
    key = telebot.types.InlineKeyboardMarkup()#задаем ее тип. Это клвиатура инлайн
    """
    тут начиная с кнопки start и заканчивая stop делаем кнопки.
    """
    for nomer in range(start,stop):
        #str(id_maybe_answer_links[nomer])) #- это извлекли Id глагола из списка преданного.
        #str(list.row((int(id_maybe_answer_links[int(nomer)])) + int(constants1.table_start))[4].value)) #"- так мы из таблицы достали инфинитив глагола на иврите. 4 столбик. constants1.table_start - это номер начал таблицы. нужен для поиска глагола
        #str(list.row((int(id_maybe_answer_links[int(nomer)])) + int(constants1.table_start))[3].value)) # -  так мы из таблицы извлекли перевод на русский язык в инфинитиве. 3 столбик
        but = telebot.types.InlineKeyboardButton(
            text=str(str(list.row((int(id_maybe_answer_links[int(nomer)]))+int(constants1.table_start))[4].value) + '- '+ str(list.row((int(id_maybe_answer_links[int(nomer)])) + int(constants1.table_start))[3].value)),
            callback_data=str(id_maybe_answer_links[nomer]))
        key.add(but)  # добавляем каждую в клавиатуру, которую задали ранее
    """
    тут сделаем кнопки нижние, если кол-во элементов 
    для вывода больше sd(заданное кол-во кнопок на на одном выводе\борту)
    
    ниже будем добавлять кнопки прокрутки, если они нужны.
    """
    next = len(id_maybe_answer_links)-stop
    text_but_next = (str(next)+">>")
    n = int(namber_bort)+1
    data_but_next = ("id_botr-" + str(n) + "-id_msg_for_find-" + str(message.message_id))
    but_next = telebot.types.InlineKeyboardButton(text=text_but_next, callback_data=data_but_next)
    befor = int(start)
    text_but_befor = ("<<"+str(befor))
    b = int(namber_bort)-1
    data_but_befor = ("id_botr-" + str(b) + "-id_msg_for_find-" + str(message.message_id))
    but_befor = telebot.types.InlineKeyboardButton(text=text_but_befor, callback_data=data_but_befor)
    """
    если кнопки не уместятся на 1 борту, 
    то делаем доп. кнопки прокрутки.  
    """
    if (len(id_maybe_answer_links)/sb)>1:
        if namber_bort == 1:#если мы в первом ботру, то...
            key.row(but_next)#так добавили кнопку , через row
        elif (len(id_maybe_answer_links))/sb <= namber_bort:#если мы в последнем ботру, то...
            key.row(but_befor)#так добавили кнопку , через row
        else: #иначе мы в середнем борту,то...
            key.row(but_befor, but_next)#так добавили обе кнопки

    """
    Ниже новый вариант записи данных чере- json
    Дальше создаю словарь с данными о результатах 
    поиска в базе. Это передам в кнопку.  
    """
    for_group_buttons = {
        "message.message_id": message.message_id,
        "info_buttons":{
            "status_searching": status_searching,
            "namber_bort": namber_bort,
            "id_maybe_answer_links": id_maybe_answer_links
        }
    }
    """
    тут проверяю, есть ли такой объект и файл уже 
    (на случай если я его удалю). Если есть, то работает с ним.
    """
    try:
        many_battons = json.load(open("many_battons.json"))
    except:
        """
        если такоего объекта и файла нет, 
        то создает новый список. пока пустой
        """
        many_battons = []
    many_battons.append(for_group_buttons) #тут добавляет в json файл новый
    with open("many_battons.json", "w") as file:
        json.dump(many_battons, file, ensure_ascii=True)
    return key  # эта строка должна быть в конце функции всей


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

"""
это временно отключено
"""
@bot.message_handler(commands=['stop'])
def handle_text(message):
    alert_new_user(message, bot)
    remove_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Клавиатуру свернули, Но ты ее всегда можешь развернуть обратно.', reply_markup = remove_markup)

@bot.message_handler(content_types=['audio'])
def handle_text(message):
    print(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    print(message)
    alert_new_user(message, bot)
    ad = AlphabetDetector()

    if '*' in message.text:
        bot.send_message(message.chat.id, 'Я не знаю такого символа * . Введите запрос заново.', parse_mode='Markdown')

    elif ad.is_cyrillic(message.text) == False and ad.is_hebrew(message.text) == False:
        answer = 'Извините, я еще не знаю глагола "*' + message.text + '*".\nВозможно вы ввели текст на неизвестном мне языке.\nЯ понимаю Русский и עברית. Попробуй снова.'
        bot.send_message(message.chat.id, answer, parse_mode='Markdown')
        log(message, answer)

    elif ad.is_cyrillic(message.text) == True:#на кириллице
        status_searching = 'Ответа в файле нет.'
        mes = message.text
        mes = mes.lower()#Все буквы меняем на мленькие
        mes = mes.split(',')#разделяем по запятой смс-запрос
        id_maybe_answer_links = []
        tx_maybe_answer_links = []
        id_answer_links = []#Это нужный список, туда будем добавлять, все верное.
        for one_word in mes:
            one_word = one_word.lstrip()#убрали пробелы вначале текста в смс-запросе
            for row in range(2, 4307): # Открываем каждую строку поочереди начиная со третей строки (шапку не читаем). Сейчас строк всего 4310.
                if one_word in list.row(row)[3].value:   # Если значение в столбце под индексом 3 (толбец с переводом), соответствует переменной mes, то
                    id_maybe_answer_links.append(int(list.row(row)[2].value)) #добавляет его id в список возможных

                    # --------------это можно куда-то перенести в другое место
                    tx_maybe_answer_links.append(list.row(row)[4].value+'- '+list.row(row)[3].value) # тут составили текст, который будет отображаться на кнопке
                    if len(tx_maybe_answer_links[-1]) > 35:
                        print('Знаков на кнопке больше 35 - ',tx_maybe_answer_links[-1])
                    # --------------это можно куда-то перенести в другое место

                    ru_trans = list.row(row)[3].value.split(',')#разделяем по запятой значения с ответами
                    sum_verbs_in_the_row = 0#Тут будем считать сколько подходящих нам слов в этой строке. Пока - 0.
                    for word in ru_trans:
                        word = word.lstrip() # убрали пробелы вначале текста в строке
                        if word[0: len(one_word)] == one_word and sum_verbs_in_the_row == 0: # если первые символы каждого слова(слово имеется ввиду, текст между запятыми) равны смс-запросу. И это первая проверка в строке, то
                            id_answer_links.append(int(list.row(row)[2].value)) #добавляем id перевода который, точно подходит. Верный перевод.
                            sum_verbs_in_the_row += 1#Увеличиваем счетчик слов в строке на 1

        """
        Сначала определим есть ли подходящие ответы. 
        Если нет, то тогда предоставим примерные ответы по запросу.
        """
        if len(id_answer_links) != 0:
            id_maybe_answer_links = id_answer_links #если подходящие ответы есть, то дальше будем делать все манипуляции с этим списком ответов
            status_searching = 'Ответ в файле есть.'
        if len(id_maybe_answer_links) == 1:
            row = int(constants1.table_start)+int(id_maybe_answer_links[0]) #constants1.table_start - это начало таблицы. помогает быстро найти строку в таблиуе. Для поска прибавляем эту констунту к id глагола
            """
            ниже определяем, печатать ли в ответе 
            дополнительные кнопки с пассивной формой
            """
            if str(list.row(int(row))[179].value) != "":
                key = make_batton_imper(message, str(row),add_buttons="all")
            else:
                key = make_batton_imper(message, str(row), add_buttons="imper")
            answer = send_table(message, row, kind_of_table="short")#тут срабатывет функция send_table
            bot.send_message(message.chat.id, answer, reply_markup=key, parse_mode='Markdown',disable_web_page_preview=True) # disable_web_page_preview=True - это для того, чтоб сниппет не отправлялся
            log(message, send_table(message, row, kind_of_table="short"))
        elif len(id_maybe_answer_links) > 1:
            namber_bort = 1
            key = make_battons(message, id_maybe_answer_links, status_searching, int(namber_bort))
            if status_searching == 'Ответа в файле нет.':
                answer_for_report = 'Извините, я еще не знаю этого глагола. Возможно вы искали(борт-' + str(namber_bort) + ':\n-' + str(id_maybe_answer_links) + '\n'
                answer = "Извините, я еще не знаю этого глагола. Возможно вы искали:"
            elif status_searching == 'Ответ в файле есть.':
                answer_for_report = 'Есть несколько подходящих ответов(борт-'+str(namber_bort)+':\n-' + str(id_maybe_answer_links) + '\n'
                answer = "Есть несколько подходящих ответов:"
            bot.send_message(message.chat.id, text=answer, reply_markup=key)
            log(message, answer_for_report)

        else:
            """
            если нет ответов совсем
            """
            answer = 'Извините, я еще не знаю глагола "*'+message.text+'*"\n_Если Вы считаете, что он важен, отправь этот глагол на проверку. И я проверю его очень быстро._Так же Вы можете проверить Ваш запрос, возможно в слове есть очепятки.'
            key = telebot.types.InlineKeyboardMarkup()
            but = telebot.types.InlineKeyboardButton(text='Отправить глагол.',callback_data='88888888')
            key.add(but)
            bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=key)
            log(message, answer)

    elif ad.is_hebrew(message.text) == True:
        """
        если завпрос на иврите. 
        Тут буду искть только точное совпадение.
        """
        if ',' in message.text:
            answer = 'Вы написали несколько слов через запятую ",". Я могу найти только один глагол в одном запросе. Попробуй снова сделать запрос.'
            bot.send_message(message.chat.id, answer, parse_mode='Markdown')
            log(message, answer)
        else:
            mes = message.text
            mes = mes.strip()#убрали пробелы вначале и вконце текста
            status_searching = 'Ответа в файле нет.' # это возможно можно убрать
            id_maybe_answer_links = []
            id_answer_links = []#Это нужный список, туда будем добавлять, все верное.
            for row in constants1.rows_verbs_bin5:#Открываем каждую строку поочереди начиная со третей строки (шапку не читаем). Сейчас строк всего 4310.
                if str(mes) in str(list.row(row)[int(180)].value):#если похожее слово в ячейке и ранее мф еще не нашли других похожих слов в этой строке, то...
                    if list.row(row)[2].value not in id_maybe_answer_links:
                        id_maybe_answer_links.append(int(list.row(row)[2].value))#добавляет его id в список возможных
                    verb_all_forms = list.row(row)[180].value.split(',')#разделяем по запятой значения с ответами
                    for word in verb_all_forms:
                        word = word.strip("~")#убрали лишние символы
                        word = word.strip()#убрали пробелы вначале и вконце текста в каждом слове
                        if word == mes:#если первые символы каждой формы слова(слово имеется ввиду, текст между запятыми) равны смс-запросу. И это первая проверка в строке, то
                            if list.row(row)[2].value not in id_answer_links:
                                id_answer_links.append(int(list.row(row)[2].value))#добавляем id перевода который, точно подходит. Верный перевод.

            if len(id_answer_links) == 0:
                answer = "Извините, нет ни одного глагола ни в одном спряжении ни в одном времени в таком написании - "+mes+".\nВозможно в слове есть опечатка. Сделайте запрос снова."
                bot.send_message(message.chat.id, answer, parse_mode='Markdown')#, #reply_markup=key)
                log(message, answer)

            elif len(id_answer_links) == 1:
                row = int(id_answer_links[0])+constants1.table_start
                if str(list.row(int(row))[179].value) != "":
                    key = make_batton_imper(message, str(row), add_buttons="all")
                else:
                    key = make_batton_imper(message, str(row), add_buttons="imper")
                answer = send_table(message, row, kind_of_table="short")#тут срабатывет функция send_table
                bot.send_message(message.chat.id, answer, reply_markup=key, parse_mode='Markdown',disable_web_page_preview=True)#disable_web_page_preview=True - это для того, чтоб сниппет не отправлялся
                log(message, send_table(message, row, kind_of_table="short"))
            else:
                status_searching = 'Ответ в файле есть.' #убрать
                id_maybe_answer_links = id_answer_links
                key = telebot.types.InlineKeyboardMarkup()
                for one_id in id_maybe_answer_links:
                    call_data = str(one_id)
                    row = int(one_id + constants1.table_start)
                    text = mes+"- "+str(list.row(row)[int(3)].value)
                    but = telebot.types.InlineKeyboardButton(text=text, callback_data=call_data)
                    key.add(but)
                answer = "Вот, что удалось найти в базе знаний:"
                bot.send_message(message.chat.id, answer, parse_mode='Markdown', reply_markup=key)
                log(message, answer)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    этот декоратор обрабатывает все нажатые кнопки
    """
    print(call.message)

    """
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
                    key = make_battons(call.message, id_maybe_answer_links, status_searching, int(namber_id_botr))
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
            answer = send_table(call.message, row, kind_of_table="long+pyal_hyfal")
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=answer,
                                  parse_mode='Markdown',
                                  disable_web_page_preview=True)
            log(call.message, answer)

        elif 'id_imper' in call.data:
            ts_and_id = str(call.data[8:])
            row = int(ts_and_id)
            answer = send_table(call.message, row, kind_of_table="long")
            """
            если у глагола есть пассивная форма, 
            формируем кнопку для пассива иначе без кнопок
            """
            if str(list.row(int(ts_and_id))[179].value) != "":#тут проверяю, нужно ли мне снова присылкть кнопку пассива или нет.
                key = make_batton_imper(call.message, ts_and_id, add_buttons="passiva")
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
            answer = send_table(call.message, ts_and_id, kind_of_table="short")
            if str(list.row(int(ts_and_id))[179].value) != "":
                key = make_batton_imper(call.message, str(ts_and_id), add_buttons="all")
            else:
                key = make_batton_imper(call.message, str(ts_and_id), add_buttons="imper")
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

