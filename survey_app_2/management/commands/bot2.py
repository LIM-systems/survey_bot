from aiogram import executor
from django.core.management.base import BaseCommand

from bot2 import handlers
from bot2.loader import dp


class Command(BaseCommand):
    help = 'Опрос 2'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=False)
