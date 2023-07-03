token ="649588171:AAE0FXWviI4f-vh3I32tCiDQtroD7lZyIr4" #ivrir_bot
IVRIT_BOT_TOKEN = "649588171:AAE0FXWviI4f-vh3I32tCiDQtroD7lZyIr4" #ivrit_bot
token2 ="630117651:AAFO8Gbh7djd4WXu1pDld7NGDzTqNr1ggSE" #via1102...
APP_NAME = 'moment-vera-ira'

sum_buttons_on_botr=5 #Цыфра означает, какое кол-во кнопок в одно сообщение мы выводим.
table_start1 = 2 #Туту нужно вручную вписывать номер индекса строки в таблице ексель с которой начинается таблица. Т.е. Первая строка с индексом - 0, Вторая с индексом 1 ит.д. Это нужно для того чтоб в программе было проще найти нужное слово по ID. Получается положение слова это (номер id + номер старта таблицы.)
table_start = table_start1-1 #т.к расчет начинается с 0
ID_ADMIN = int(115496560)


rows_verbs_bin5 = [row for row in range(3094)]
rows_verbs_bin2 = [row for row in range(4504,5716)]
rows_verbs_bin7 = rows_verbs_bin5 + rows_verbs_bin2

columns_for_hebrew_serch = [5,8,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90,93,96,99,102,105,108,111,114,117,120,123,126,129,132,135,138,141,144,147,150,153,156,159,162,165,168,171,174,177]

#template_photo_id=

#Файл Pealim_FINAL.xlsx с таблицей слов открываем на строках примерных 54 и 297 и 466
# на 409 открывает временный файл ./words_first.xls