import telebot
from config import keys, TOKEN
from utils import Apiexception, Converter


bot = telebot.TeleBot(token=TOKEN)


"""Хендлер на команды start и help"""
@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = (f"Привет, {message.chat.username}, чтобы начать работу введите команду \
боту в следующем формате: \n<имя валюты><в какую валюту перевести>\
<колличество валюты>\n \
Увидеть список всех достпуных валют можно по команде /values.")
    bot.send_message(message.chat.id, text)

"""Хендлер на команду values"""
@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


"""Главный обработчик событий для типа text """
@bot.message_handler(content_types=["text"])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(" ")

        if len(values) != 3 :
            raise Apiexception(f"Вы ввели {len(values)} параметров, ведите 3 параметра.")

        quote, base, amount = values

        total_base_amount = Converter.convert(quote, base, amount)

        text = f"Цена {amount} {quote} в {base} - {total_base_amount}"

    except Apiexception as e:
        bot.reply_to(message, text = f"{e}\nВы ввели команду неверно, попробуйте снова.\nЧтобы начать работу \
введите команду боту в следующем формате: \n<имя валюты><в какую валюту перевести>\
<колличество валюты>\n\
Увидеть список всех достпуных валют можно по команде\n/values.")
    except Exception as e:
        bot.reply_to(message, text = f"Не удалось обработать команду \n{e}")
    else:
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)
#spasibo