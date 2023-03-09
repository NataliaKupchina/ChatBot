import telebot
from config import keys,TOKEN
from extentions import Converter, ConvertionException
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Здравствуйте! Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты, цену которой Вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) != 3:
                raise ConvertionException('Неверное количество параметров!')

        answer = Converter.convert(*values)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, answer)

bot.polling()