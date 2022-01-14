import os

from flask import Flask, request

import telebot

TOKEN = '1657187067:AAEpRHjY-I547iBQ0G10ALlImyip-GbiSR8'
bot = telebot.TeleBot(TOKEN) #,threaded=False)
server = Flask(__name__)



from typing import Text
# import telebot
from telebot import types
from telebot.util import user_link


from baza import *
#from aiogram.dispatcher import FSMContext
reg_dict = {}


class Reg:
    def __init__(self):
        self.org = None
        self.sendorg = None
        self.sendfio = None
        self.theme = None
        self.link =None
# bot = telebot.TeleBot("1657187067:AAEpRHjY-I547iBQ0G10ALlImyip-GbiSR8")

@bot.message_handler(commands=["start"])
def start_message(message):
    if (len(select_lang(message.chat.id))==0):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonA = types.KeyboardButton("Uzbek")
        buttonB = types.KeyboardButton("Русский")
        markup.row(buttonA, buttonB)
        bot.send_message(message.chat.id, "Tilni tanlang\nВыберите язык", reply_markup=markup)
    else:
        for u in select_lang(message.chat.id):
            if (u[0]=='uzbek'):
                markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttonA1 = types.KeyboardButton("Xat yaratish")
                buttonB1 = types.KeyboardButton("Nusxasini yuborish")
                markup1.add(buttonA1).add(buttonB1)
                for emp in select_employees_from_id(message.chat.id):
                    fio=emp[1]
                bot.send_message(message.chat.id, fio +"\nXatlarni registratsiya qilish botiga\n Xush kelibsiz!", reply_markup=markup1)
            elif (u[0]=='русский'):
                markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
                buttonA1 = types.KeyboardButton("Создать письмо")
                buttonB1 = types.KeyboardButton("Отправить копию")
                markup2.add(buttonA1).add(buttonB1)
                for emp in select_employees_from_id(message.chat.id):
                    fio=emp[1]
                bot.send_message(message.chat.id, fio+ "\n Привет! Добро пожаловать на наш бот! ", reply_markup=markup2)



    


@bot.message_handler(content_types='text')
def get_text_messages(message):
    #bot.send_message(message.chat.id,message.text)
    if message.text.lower() == "uzbek":
        print(message.text)
        add_lang(message.chat.id,"uzbek")
        #bot.send_message(message.chat.id,"Salom! Xatlarni ro`yxatga olish botimizga xush kelibsiz!",types.ReplyKeyboardRemove(),)
        keyboard = types.ReplyKeyboardMarkup()
        button = types.KeyboardButton("Yuborish", request_contact=True)
        keyboard.add(button)
        bot.send_message(
            message.chat.id, "Telefon raqmingizni yuboring", reply_markup=keyboard
        )
        
    if message.text.lower() == "русский":
        add_lang(user_id=message.chat.id, lang="русский")
        #bot.send_message(message.chat.id, "Привет! ", types.ReplyKeyboardRemove())
        keyboard = types.ReplyKeyboardMarkup()
        button = types.KeyboardButton("Отправить", request_contact=True)
        keyboard.add(button)
        bot.send_message(message.chat.id, "Отправьте номер телефона", reply_markup=keyboard
        )
    if message.text == "Создать письмо":
        orgss= types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        if len(select_employees_by_id(message.chat.id))>1:
            for orgs in select_employees_by_id(message.chat.id):
                #print(type(orgs[3]))
                t= orgs[3]+""
                orgss.add(types.KeyboardButton(t))
            msg=bot.send_message(message.chat.id,"Выберите организацию:",reply_markup=orgss)
            bot.register_next_step_handler(msg, process_org_step_ru)
        else:
            user =Reg()
            reg_dict[message.chat.id]=user
            for orgs in select_employees_by_id(message.chat.id):
                user.org = orgs[3]
            bot.send_message(message.chat.id,"Выбран организация:"+user.org)
            msg=bot.send_message(message.chat.id,"Кому: (Организация получателя, пример: ООО 'Фирма')")
            bot.register_next_step_handler(msg, process_send_org_step_ru)
    if message.text == "Отправить копию":
        #regss=types.InlineKeyboardMarkup()
        regss= types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        for regs in select_regs_by_bot_id(message.chat.id):
            regss.add("№ "+str(regs[3])+" ("+regs[1]+")")
        bot.send_message(message.chat.id,"Выберите письмо",reply_markup=regss)
    for regs in select_regs_by_bot_id(message.chat.id):
        if message.text == ("№ "+str(regs[3])+" ("+regs[1]+")"):
            bot.send_message(message.chat.id," № "+str(regs[3])+" от: "+str(regs[2])+"\n От: "+str(regs[1])+"\n Кому: "+str(regs[4])+"\n ФИО(кому): "+(regs[5])+"\n Тема: "+str(regs[6]))#+"\n Файл: "+str(regs[7]))
            #user = reg_dict[message.chat.id]
            #user.link = regs[3]
            msg=bot.send_message(message.chat.id,"Загрузите копию письма (в формате PDF):")
            bot.register_next_step_handler(msg, process_upload,regs[3])
                

    if message.text=="Xat yaratish":
        orgss= types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        if len(select_employees_by_id(message.chat.id))>1:
            for orgs in select_employees_by_id(message.chat.id):
                #print(type(orgs[3]))
                t= orgs[3]+""
                orgss.add(types.KeyboardButton(t))
            msg=bot.send_message(message.chat.id,"Sizning tashkilotingiz:",reply_markup=orgss)
            bot.register_next_step_handler(msg, process_org_step_uz)
        else:
            user =Reg()
            reg_dict[message.chat.id]=user
            for orgs in select_employees_by_id(message.chat.id):
                user.org = orgs[3]
            bot.send_message(message.chat.id,"Tashkilotingiz tanlandi:"+user.org)
            msg=bot.send_message(message.chat.id,"Kimga (Xatni qabul qiluvchi tashkilot: ООО 'Фирма')")
            bot.register_next_step_handler(msg, process_send_org_step_uz)
    if message.text == "Nusxasini yuborish":
        #regss=types.InlineKeyboardMarkup()
        regss= types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        for regs in select_regs_by_bot_id(message.chat.id):
            regss.add(str(regs[3])+"-xat"+"("+str(regs[1])+")")
        bot.send_message(message.chat.id,"Xatni tanlang",reply_markup=regss)
    for regs in select_regs_by_bot_id(message.chat.id):
        if message.text == (str(regs[3])+"-xat"+"("+str(regs[1])+")"):
            bot.send_message(message.chat.id,"№ "+str(regs[3])+"\n Vaqti: "+str(regs[2])+"\n Kimdan: "+str(regs[1])+"\n Kimga: "+str(regs[4])+"\n FISH(Kimga): "+str(regs[5])+"\n Mavzu: "+str(regs[6])) #+"\n Fayl: "+str(regs[7]))
            #user = reg_dict[message.chat.id]
            #user.link = regs[3]
            msg=bot.send_message(message.chat.id,"Xat nusxasini yuklang (faqat PDF shaklida):")
            bot.register_next_step_handler(msg, process_upload_uz,regs[3])

def process_upload(message,nomer):
    try:
    # получить основную информацию о файле и подготовить его к загрузке
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    # определяем путь загрузки с именем файла
        src = 'files/' + message.document.file_name
    # открываем файл для записи
        with open(src, 'wb') as new_file:
        # записываем данные в файл
            new_file.write(downloaded_file)
        add_file_link(message.document.file_name,nomer)
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonA1 = types.KeyboardButton("Создать письмо")
        buttonB1 = types.KeyboardButton("Отправить копию")
        markup2.add(buttonA1).add(buttonB1)
        bot.send_message(message.chat.id,"Ваш файл успешно отправлен!",reply_markup=markup2)
    except Exception as e:
        bot.reply_to(message, 'Ошибка. Попробуйте еще раз!')
    
def process_upload_uz(message,nomer):
    try:
    # получить основную информацию о файле и подготовить его к загрузке
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    # определяем путь загрузки с именем файла
        src = 'files/' + message.document.file_name
    # открываем файл для записи
        with open(src, 'wb') as new_file:
        # записываем данные в файл
            new_file.write(downloaded_file)
        add_file_link(message.document.file_name,nomer)
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonA1 = types.KeyboardButton("Xat yaratish")
        buttonB1 = types.KeyboardButton("Nusxasini yuborish")
        markup2.add(buttonA1).add(buttonB1)
        bot.send_message(message.chat.id,"Sizning faylingiz yuklandi!",reply_markup=markup2)
    except Exception as e:
        bot.reply_to(message, 'Xatolik. Yana bir bor urinib ko`ring!')

@bot.message_handler(content_types=["contact"])
def handle_contact(message: types.Message):
        contact = message.contact.phone_number
        print(int(contact))
        contact = int(contact)
        if len(select_employees(contact))>=1:
            for row in select_employees(contact):
                id_is_bot = row[4]
            if str(id_is_bot)=='':
                add_contact_and_bot_id(message.chat.id,contact)
                for u in select_lang(message.chat.id):
                    if (u[0]=='uzbek'):
                        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        buttonA1 = types.KeyboardButton("Xat yaratish")
                        buttonB1 = types.KeyboardButton("Nusxasini yuborish")
                        markup1.add(buttonA1).add(buttonB1)
                        for emp in select_employees(contact):
                            fio=emp[1]
                        bot.send_message(message.chat.id,fio +"\nXatlarni registratsiya qilish botiga\n Xush kelibsiz!", reply_markup=markup1)
                    if (u[0]=='русский'):
                        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        buttonA1 = types.KeyboardButton("Создать письмо")
                        buttonB1 = types.KeyboardButton("Отправить копию")
                        markup2.add(buttonA1).add(buttonB1)
                        for emp in select_employees(contact):
                            fio=emp[1]
                        bot.send_message(message.chat.id, fio+" \n Добро пожаловать на наш бот! ", reply_markup=markup2)
        else:
            for u in select_lang(message.chat.id):
                if (u[0]=='uzbek'):
                    bot.send_message(message.chat.id,"Sizning ma`lumotlaringiz bazada topilmadi. Tashkilotingiz kotibasiga murojaat qilishingizni so`raymiz!",types.ReplyKeyboardRemove())
                    delete_lang(message.chat.id)
                if (u[0]=='русский'):
                    bot.send_message(message.chat.id,"Ваш номер не найден в базе. Просим обратитьса к секретарю вашей компаний",types.ReplyKeyboardRemove())
                    delete_lang(message.chat.id)


            
            

        # fio = bot.select_employe(contact)

        # us_id = message.from_user.id
        # us_name = message.from_user.first_name
        # us_sname = message.from_user.last_name
        # username = message.from_user.username

        # db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)




def process_org_step_uz(message):
    try:
        #chat_id = message.chat.id
        #org_name = message.text
        #
        user =Reg()
        reg_dict[message.chat.id]=user
        user.org = message.text
        msg=bot.send_message(message.chat.id,"Kimga (Xatni qabul qiluvchi tashkilot: ООО 'Firma')")
        bot.register_next_step_handler(msg, process_send_org_step_uz)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_send_org_step_uz(message):
    try:
        #chat_id = message.chat.id
        #org_name = message.text
        #
        user = reg_dict[message.chat.id]
        user.sendorg = message.text
        msg = bot.reply_to(message, 'Qabul qiluvchining FISH?')
        bot.register_next_step_handler(msg, process_send_fio_step_uz)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_send_fio_step_uz(message):
    try:
        user = reg_dict[message.chat.id]
        user.sendfio = message.text
        #markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #.add('Male', 'Female')
        msg = bot.reply_to(message, 'Xatning mavzusi:')
        bot.register_next_step_handler(msg, process_theme_step_uz)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_theme_step_uz(message):
    try:
        user = reg_dict[message.chat.id]
        user.theme = message.text
        #markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #.add('Male', 'Female')
        nomer = add_reg_and_get_nomer(message.chat.id,user.sendorg,user.sendfio,user.theme,user.org)
        print(nomer)
        bot.send_message(message.chat.id,"Yangi raqam ro`yxatdan o`tdi:\n № "+str(nomer) +"  "+str(datetime.now()))
        #print("Зарегистрирован новый номер:№ ")
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonA1 = types.KeyboardButton("Xat yaratish")
        buttonB1 = types.KeyboardButton("Nusxasini yuborish")
        markup2.add(buttonA1).add(buttonB1)
        bot.send_message(message.chat.id,'Sizning tashkilotingiz: ' + str(user.org) + '\n Kimga: ' + str(user.sendorg) + '\n FISH: ' + str(user.sendfio) + '\n Mavzu: ' + str(user.theme),reply_markup=markup2)
        f = open("Шаблон ИП.docx","rb")
        bot.send_document(message.chat.id,f)
        #msg = bot.reply_to(message, 'Ведите тема писмы')
        #bot.register_next_step_handler(msg, process_theme_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')





def process_org_step_ru(message):
    try:
        #chat_id = message.chat.id
        #org_name = message.text
        #
        user =Reg()
        reg_dict[message.chat.id]=user
        user.org = message.text
        msg=bot.send_message(message.chat.id,"Кому: (Организация получателя, пример: ООО 'Фирма')")
        bot.register_next_step_handler(msg, process_send_org_step_ru)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_send_org_step_ru(message):
    try:
        #chat_id = message.chat.id
        #org_name = message.text
        #
        user = reg_dict[message.chat.id]
        user.sendorg = message.text
        msg = bot.reply_to(message, 'ФИО получателя:')
        bot.register_next_step_handler(msg, process_send_fio_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_send_fio_step(message):
    try:
        user = reg_dict[message.chat.id]
        user.sendfio = message.text
        #markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #.add('Male', 'Female')
        msg = bot.reply_to(message, 'Тема письма:')
        bot.register_next_step_handler(msg, process_theme_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_theme_step(message):
    try:
        user = reg_dict[message.chat.id]
        user.theme = message.text
        #markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #.add('Male', 'Female')
        nomer = add_reg_and_get_nomer(message.chat.id,user.sendorg,user.sendfio,user.theme,user.org)
        print(nomer)
        now = datetime.now()
        now= str(now.strftime("%d-%m-%Y %H:%M:%S"))
        # print(now)
        bot.send_message(message.chat.id,"Зарегистрирован новый номер:\n № "+str(nomer) +" oт "+now)
        #print("Зарегистрирован новый номер:№ ")
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonA1 = types.KeyboardButton("Создать письмо")
        buttonB1 = types.KeyboardButton("Отправить копию")
        markup2.add(buttonA1).add(buttonB1)
        bot.send_message(message.chat.id,'От: ' + str(user.org) + '\n Koму: ' + str(user.sendorg) + '\n ФИО получателя: ' + str(user.sendfio) + '\n Тема: ' + str(user.theme),reply_markup=markup2)
        f = open("Шаблон ИП.docx","rb")

        bot.send_document(message.chat.id,f)
        bot.send_message(message.chat.id,"Не забудьте загрузить копию письма.")
        #msg = bot.reply_to(message, 'Ведите тема писмы')
        #bot.register_next_step_handler(msg, process_theme_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')



bot.polling(none_stop=True)


# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     bot.reply_to(message, message.text)


# @server.route('/' + TOKEN, methods=['POST'])
# def getMessage():
#     json_string = request.get_data().decode('utf-8')
#     update = telebot.types.Update.de_json(json_string)
#     bot.process_new_updates([update])
#     return "!", 200


# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='http://10.171.160.142:5000/' + TOKEN)
#     return "!", 200


# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))