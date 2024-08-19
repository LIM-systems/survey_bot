import logging
import pathlib

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import env

path = pathlib.Path().absolute()
bot = Bot(token=env.TOKEN_2, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# logger = logging.getLogger(__name__)
# logging.basicConfig(
#     filename='logs/bot_logs.log',
#     level=logging.ERROR,
#     format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
# )
# logger.addHandler(logging.StreamHandler())
rate_buttons = ['1🌟', '2🌟', '3🌟', '4🌟', '5🌟']
yon = ['Да ✅', 'Нет ❌']
