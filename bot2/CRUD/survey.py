import math

from asgiref.sync import sync_to_async
from django.db.models import Avg
from survey_app_2 import models as mdl


@sync_to_async()
def get_greeting():
    '''Получение приветствия'''
    greeting = mdl.Greeting.objects.first()
    if not greeting:
        return 'Добро пожаловать!'
    return greeting.text


@sync_to_async()
def get_parting():
    '''Получение приветствия'''
    parting = mdl.Parting.objects.first()
    if not parting:
        return 'Спасибо за Ваши ответы!'
    return parting.text


@sync_to_async()
def add_user(tg_id, name):
    '''Запись пользователя в бд'''
    mdl.User.objects.get_or_create(tg_id=tg_id, name=name)


@sync_to_async()
def get_questions():
    '''Получение вопросов'''
    questions = mdl.Question.objects.all()
    return [
        {**question.__dict__, 'answered': False}
        for question in questions
    ]


@sync_to_async()
def get_question(id):
    '''Получение вопроса'''
    question = mdl.Question.objects.filter(id=id).first()
    return question


@sync_to_async()
def save_result(tg_id, answers):
    '''Сохранение ответов'''
    user = mdl.User.objects.get(tg_id=tg_id)

    # сохраняем ответы
    questions = []
    for answer in answers:
        rate = answer.get('rate', None)
        question = mdl.Question.objects.get(id=answer['id'])
        questions.append(question)
        db_answer, created = mdl.Answer.objects.get_or_create(
            user=user,
            question=question,
        )
        db_answer.rate = rate
        db_answer.yon = answer.get('yon')
        db_answer.comment = answer.get('comment')
        db_answer.save()
