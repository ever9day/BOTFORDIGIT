import telebot
from datetime import datetime
from telebot import types
import requests
import sqlite3

admin = {'pass':''}


dataUser = {'number':'',
            'name':'',
            'age':'',
            'adress':''}

token = '605848364:AAGLoCbxtAfF1lHFGEeA0_KnyavD2OW0d34'

bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])


def start(message):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    result = cursor.execute("Select * from users where userID="+str(message.from_user.id)+"").fetchone()
    if result is not None:
        if result[5] == 0:
            bot.send_message(message.chat.id,'Ваша заявка еще на рассмотрении')
        elif str(message.from_user.id) == 'qweasdzxc21':
            ADMIN(message)
        elif result[5] == 1:
            Menu(message)
    else:
        getNumber(message)
    conn.commit()
    conn.close()
        
    
def getNumber(message):
    buttons = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    numButton = types.KeyboardButton('Отправить номер', request_contact=True)
    buttons.add(numButton)
    bot.send_message(message.chat.id,'Добро пожаловать в бота города Астаны! Отправьте свой номер нажав на кнопку: ',reply_markup=buttons)
    bot.register_next_step_handler(message, getAdress)
    
def getAdress(message):
    dataUser['number'] = message.contact.phone_number
    bot.send_message(message.chat.id,'А теперь напишите свой адресс: ')
    bot.register_next_step_handler(message,getName)
    
def getName(message):
    dataUser['adress'] = message.text
    bot.send_message(message.chat.id,'Напишите имя: ')
    bot.register_next_step_handler(message,getAge)
    
def getAge(message):
    dataUser['name'] = message.text
    bot.send_message(message.chat.id,'Сколько вам лет: ')
    bot.register_next_step_handler(message,checkDataUser)
    
def checkDataUser(message):
    dataUser['age'] = message.text
    button = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    confirmB = types.KeyboardButton('Подтвердить')
    button.add(confirmB)

    againB = types.KeyboardButton('Заново')
    button.add(againB)
    bot.send_message(message.chat.id, 'Номер телефона: ' + dataUser['number'] + '\n' + 'Адресс: ' + dataUser['adress']
                     + '\n' + 'Имя: ' + dataUser['name']+ '\n' + 'Возраст: ' + dataUser['age'] + '\n' + '\n'+
                     'Если ваши данные вверны, нажмите Подтверждаю для регистрации нажав на кнопку',reply_markup=button)
    bot.register_next_step_handler(message,choiseUser)



def choiseUser(message):
    if message.text == 'Подтвердить':
        bot.send_message(message.chat.id, 'Запрос был отправлен, ожидайте ответа')
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('Insert into users values("'+str(message.from_user.id)+'","'+dataUser['name']+'","'+dataUser['age']+'","'+dataUser['number']+'","'+dataUser['adress']+'","0")')
        conn.commit()
        conn.close()
    elif message.text == 'Заново':
        getNumber(message)
    else:
        bot.send_message(message.from_user.id, 'Неверный ответ')

def Menu(message):

    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    projectB = types.KeyboardButton('О проекте')
    kb.add(projectB)

    messageB = types.KeyboardButton('Отправить сообщение')
    kb.add(messageB)

    myMessageB = types.KeyboardButton('Мои обращение')
    kb.add(myMessageB)

    feedbackB = types.KeyboardButton('Обратная связь')
    kb.add(feedbackB)
    bot.send_message(message.from_user.id, 'Здраствуйте, ваша заявку подтвердили', reply_markup=kb)
    bot.register_next_step_handler(message,userChoise)
    
def userChoise(message):
    if message.text == 'О проекте':
        Inline(message)
    elif message.text == 'Отправить сообщение':
        bot.register_next_step_handler(message,mesage)
    elif message.text == 'Мои обращение':
        bot.register_next_step_handler(message,myMessage)
    elif message.text == 'Обратная связь':
        pass








def mesage(message):

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    dirtB = types.KeyboardButton('Грязь и мусор')
    kb.add(dirtB)

    pitB = types.KeyboardButton('Ямы')
    kb.add(pitB)

    lightB = types.KeyboardButton('Неисправное освещение')
    kb.add(lightB)

    allCatB = types.KeyboardButton('показать все категории')
    kb.add(allCatB)

    swapB = types.KeyboardButton('Поменять избранные категории')
    kb.add(swapB)
    bot.send_message(message.from_user.id, 'Выбирете категорию', reply_markup=kb)
    bot.register_next_step_handler(message,userChoose)

def userChoose(message):
    if message.text == 'Грязь и мусор':
        bot.send_message(message.from_user.id, 'Выбор место(Во дворе/В подъезде жилого дома/На проезжей части или тротуаре/На остановке. ')
        bot.send_message(message.from_user.id, 'Напишите адресс. ')
        bot.send_message(message.from_user.id, 'Добавьте Фото или Видео. ')
        bot.send_message(message.from_user.id, 'Напишите коментарий. ')
        bot.send_message(message.from_user.id, 'Спасибо, мы осмотрим это дело. ')
    elif message.text == 'Ямы':
        bot.send_message(message.from_user.id, 'Выбор место(Во дворе/В подъезде жилого дома/На проезжей части или тротуаре/На остановке. ')
        bot.send_message(message.from_user.id, 'Напишите адресс. ')
        bot.send_message(message.from_user.id, 'Добавьте Фото или Видео. ')
        bot.send_message(message.from_user.id, 'Напишите коментарий. ')
        bot.send_message(message.from_user.id, 'Спасибо, мы осмотрим это дело. ')
    elif message.text == 'Неисправное освещение':
        bot.send_message(message.from_user.id, 'Выбор место(Во дворе/В подъезде жилого дома/На проезжей части или тротуаре/На остановке. ')
        bot.send_message(message.from_user.id, 'Напишите адресс. ')
        bot.send_message(message.from_user.id, 'Добавьте Фото или Видео. ')
        bot.send_message(message.from_user.id, 'Напишите коментарий. ')
        bot.send_message(message.from_user.id, 'Спасибо, мы осмотрим это дело. ')
    elif message.text == 'показать все категории':
        bot.send_message(message.from_user.id, 'Перейдите по этому сайту  https://www.apple.com/ru/ ')
    elif message.text == 'Поменять избранные категории':
        bot.send_message(message.from_user.id, 'Измените категорию на сайте https://www.apple.com/ru/  ')





def ADMIN(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    keyB = types.KeyboardButton('Ключевые слова')
    kb.add(keyB)

    changeB = types.KeyboardButton('Изменить Вопросы')
    kb.add(changeB)

    textB = types.KeyboardButton('Редактировать текст')
    kb.add(textB)

    devB = types.KeyboardButton('События')
    kb.add(devB)

    peopleB = types.KeyboardButton('Участники группы')
    kb.add(peopleB)
    
    vacB = types.KeyboardButton('Вакансии')
    kb.add(vacB)
    bot.send_message(message.from_user.id, 'Админка', reply_markup=kb)
    
    



def Inline(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Читать далее',callback_data='next')
    keyboard.add(button)
    bot.send_message(message.chat.id,'asasfasf',reply_markup=keyboard)

@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'next':
        bot.send_message(c.message.chat.id,'кек')
    









bot.polling(none_stop=True)








