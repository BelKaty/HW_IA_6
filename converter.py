import telebot
from currency_converter import CurrencyConverter #устанавливаем нужные библиотеки
from telebot import types

bot = telebot.TeleBot('7135548839:AAFef3EcIPqP89M8TgaPatAxKJmeimrSqNg')
currency = CurrencyConverter() #создаем объект на основе класса CurrencyConverter
amount = 0

@bot.message_handler(commands=['start']) #создаем приветствие
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введите сумму.')
    bot.register_next_step_handler(message, summa)

def summa(message): #функция обработки данных пользователя
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму.')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:

        markup = types.InlineKeyboardMarkup(row_width=3) #создаем кнопки пары валют для конвертации
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data = 'usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data = 'eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data = 'usd/gbp')

        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите пару валют.', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сумма должна быть больше нуля. Введите сумму.')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True) #метод для обработки callback_data
def callback(call):
    values = call.data.upper().split('/')
    res = currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}/ Можете заново вписать сумму.')
    bot.register_next_step_handler(call.message, summa)

bot.polling(none_stop=True)