import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: :\n<имя валюты, цену которой Вы хотите узнать>\
<имя валюты, в которой Вы хотите узнать цену первой валюты>\
<количество первой валюты>\nУвидеть список всех доступных валют: \n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values)!= 3:
            raise ConvertionException('Не верное количество параметров')

        quote, base, amount = values
        total_base = float(amount) * float(CryptoConverter.get_price(quote, base, amount))

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base}: {total_base}{base}'
        bot.send_message(message.chat.id, text)

bot.polling()
