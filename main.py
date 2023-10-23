import time
import telebot
from telebot import types
import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="analogi_of_game",
    user="postgres",
    password="1"
)

# Создание курсора
cursor = conn.cursor()
bot = telebot.TeleBot("6800569429:AAH5aWH8molv8lLJA7u74MzWXKMgjNB6EN4")


@bot.message_handler(commands=["start", "Start", "Старт", "старт"])
def first_zapusk(message):
    # Проверка, есть ли идентификатор пользователя в таблице "Users"
    cursor.execute("SELECT * FROM Users WHERE user_id = %s", (message.chat.id,))
    row = cursor.fetchone()
    if row is None:
        # Если пользователя нет в таблице, добавляем его
        cursor.execute("INSERT INTO Users (user_id) VALUES (%s)", (message.chat.id,))
        conn.commit()
        bot.send_message(message.chat.id, "Приветствую тебя, пользователь!\n"
                                          "Данный бот предназначен для поиска аналогов игр\n"
                                          "Для продолжения действий вам требуется ввести ваш логин\n")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы в системе!")
        bot.send_message(message.chat.id, "В данном боте вам доступны в основном меню следующие возможности\n"
                                          "Поиск аналогов, предназначен для поиска аналога игры\n"
                                          "Предложения, предназначены для вывода предложений на платформах\n")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.lower() == "поиск аналогов" or message.text.lower() == "Поиск аналогов":
        bot.send_message(message.chat.id, "Введите название игры")
        bot.register_next_step_handler(message, process_search)
        # Выполнение SQL-запроса
        cursor.execute("SELECT * FROM game")
        rows = cursor.fetchall()
        if len(rows) == 0:
            bot.send_message(message.chat.id, "Пока нет предложений")
        else:
            for row in rows:
                message_text = "\n".join(str(cell) for cell in row)
                bot.send_message(message.chat.id, message_text)
    elif message.text.lower() == "предложения":
        # Выполнение SQL-запроса
        cursor.execute("SELECT * FROM game")
        rows = cursor.fetchall()
        if len(rows) == 0:
            bot.send_message(message.chat.id, "Пока нет предложений")
        else:
            for row in rows:
                message_text = "\n".join(str(cell) for cell in row)
                bot.send_message(message.chat.id, message_text)
    elif message.text.lower() == "изменить поиск" or message.text.lower() == "Изменить поиск":
        bot.send_message(message.chat.id, "Введите новое название")
    elif message.text.lower() == "найти больше" or message.text.lower() == "найти больше":
        # Выполнение SQL-запроса
        cursor.execute("SELECT * FROM game")
        rows = cursor.fetchall()
        if len(rows) == 0:
            bot.send_message(message.chat.id, "Пока нет предложений")
        else:
            for row in rows:
                message_text = "\n".join(str(cell) for cell in row)
                bot.send_message(message.chat.id, message_text)
    elif message.text.lower() == "назад":
        menu(message)


def process_search(message):
    # Здесь можно выполнить поиск аналогов игры на основе введенного запроса
    # и отправить результаты пользователю
    bot.send_message(message.chat.id, "Результаты поиска аналогов игры")

    # После отправки результатов поиска, вызовите функцию menu для изменения меню
    search_menu(message)


def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poisk_analofov = types.KeyboardButton("Поиск аналогов")
    predlozhenia = types.KeyboardButton("Предложения")
    markup.add(poisk_analofov, predlozhenia)
    bot.send_message(message.chat.id, "Для поиска аналогов, требуется нажать на кнопку Поиск аналогов\n"
                                      "Для просмотра предложений требуется нажать на кнопку Предложения\n",
                     reply_markup=markup)


def search_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    nazad = types.KeyboardButton("Найти больше")
    izmenit_poisk = types.KeyboardButton("Изменить поиск")
    naiti_bolshe = types.KeyboardButton("Назад")
    markup.add(nazad, izmenit_poisk, naiti_bolshe)
    bot.send_message(message.chat.id, "Вы находитесь в меню поиска аналогов игры\n"
                                      "Для возврата в главное меню нажмите на кнопку Назад\n"
                                      "Для изменения поиска нажмите на кнопку Изменить поиск\n"
                                      "Для поиска большего количества нажмите на кнопку Найти больше\n",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == "назад")
def handle_back(message):
    menu(message)


bot.polling()
cursor.close()
conn.close()