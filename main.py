import telebot
import traceback

from config import *
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.reply_to(message,
                 f"<Бот поможет узнать нынешний курс следующих валют>\n<для более подробной информации введите: /help")

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    bot.reply_to(message, f"Чтобы начать работу, введите комманду в следующем формате:<имя валюты>"
                          f"<в какую валюту перевести><количество первой валюты>"
                          f"<Чтобы посмотреть список доступных валют введите: /values>")

@bot.message_handler(commands=['values'])
def available_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for keys in exchanges.keys():
        text = '\n'.join((text, keys))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = f"Выберите валюту из которой конвертировать: "
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, base_hundler)

def base_hundler(message: telebot.types.Message):
    base = message.text.strip()
    text = f"Выберите валюту в которую конвертировать: "
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, sym_hundler, base)

def sym_hundler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = f"Введите сумму для конвертации: "
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_hundler, base, sym)

def amount_hundler(message: telebot.types.Message, base, sym):
    amount = message.text
    try:
        new_price = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: {e}")
    else:
        text = f"Цена {amount} {base} в {sym} : {new_price}"
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converteur(message: telebot.types.Message):
    commands = message.text.split()
    try:
        if len(commands) != 3:
            raise APIException("Неверное количество параметров!")
        answer = Converter.get_price(*commands)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде: \n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка: \n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling(none_stop=True)

# бот работает
# для себя хотел добавить кнопки, до конца дедлайна не хватает времени :(
# кусок с этим кодом я обрезал, потом доработаю
