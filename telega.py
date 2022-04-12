import telebot
from pyowm import OWM
from pyowm.utils import config as cfg

bot = telebot.TeleBot('5290669059:AAGd19P6ibmhqExjuvAZEYEVq4bZ6Ka_BH0')
config = cfg.get_default_config()
config['language'] = 'ru'

owm = OWM('45dccacd7323118640d1f8cf9dc5a6af', config)

@bot.message_handler(commands=['start'])
def start_message(message):
    mess = f"Привет, {message.from_user.first_name}  {message.from_user.last_name}"
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == 'новости' or message.text == 'Новости':
        bot.send_message(message.chat.id, "https://lenta.ru")

    elif message.text == 'погода' or message.text == 'Погода':
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(message.from_user.id, "Чтобы узнать погоду (новости), напиши:  погода (новости)")

def get_weather(message):
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(message.text)
    except Exception as e:
        bot.send_message(message.from_user.id, "Данных по этому городу нет, извините")
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)
        print(e)
    w = observation.weather
    temp = w.temperature("celsius") ["temp"]
    answer = "В городе " + message.text + " сейчас " + w.detailed_status + "\n"
    answer += "Температура там около " + str(temp) + " по Цельсию" +"\n\n"
    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True, interval=0)
