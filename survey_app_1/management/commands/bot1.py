from aiogram import executor
from django.core.management.base import BaseCommand

from bot1 import handlers
from bot1.loader import dp


class Command(BaseCommand):
    help = 'Опрос 1'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=False)
