import logging
import pathlib

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import env

path = pathlib.Path().absolute()
bot = Bot(token=env.TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# logger = logging.getLogger(__name__)
# logging.basicConfig(
#     filename='logs/bot_logs.log',
#     level=logging.ERROR,
#     format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
# )
# logger.addHandler(logging.StreamHandler())


greeting = '''Друзья, всем привет!👋🏻

Очередной раз мы отлично отдохнули нашей дружной компанией на Битюге и отпраздновали наше 19-летие🎉🎉  

В следующем году нас ждет юбилей🎆
Чтобы сделать следующий праздник ещё лучше, пожалуйста, поделитесь своими впечатлениями о минувшем мероприятии.🙌🏻
'''
rate_buttons = ['1🌟', '2🌟', '3🌟', '4🌟', '5🌟']
parting = '''Спасибо, что разделили этот праздник вместе с нами🤗 
Ждем вас в следующем году на юбилее компании!🥂✨'''
