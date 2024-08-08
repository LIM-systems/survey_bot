import math

from asgiref.sync import sync_to_async
from django.db.models import Avg
from survey_app import models as mdl


@sync_to_async()
def add_user(tg_id, name):
    '''Запись пользователя в бд'''
    mdl.User.objects.get_or_create(tg_id=tg_id, name=name)


@sync_to_async()
def set_was_in(tg_id, answer):
    user = mdl.User.objects.get(tg_id=tg_id)
    user.was_in = answer
    user.save()


@sync_to_async()
def set_was_in_reason(tg_id, reason):
    user = mdl.User.objects.get(tg_id=tg_id)
    user.reason = reason
    user.save()


@sync_to_async()
def get_questions():
    '''Получение вопросов'''
    questions = mdl.Question.objects.all()
    return [
        {**question.__dict__, 'answered': False}
        for question in questions
    ]


@sync_to_async()
def save_result(tg_id, answers):
    '''Сохранение ответов'''
    user = mdl.User.objects.get(tg_id=tg_id)

    # счестчик для расчёта оценки
    total_user_rate = 0
    count = 0

    # сохраняем ответы
    questions = []
    for answer in answers:
        rate = answer.get('rate', None)
        if rate:
            total_user_rate += rate
            count += 1
        question = mdl.Question.objects.get(id=answer['id'])
        questions.append(question)
        db_answer, created = mdl.Answer.objects.get_or_create(
            user=user,
            question=question,
        )
        db_answer.rate = rate
        db_answer.comment = answer.get('comment')
        db_answer.save()

    # рассчитываем среднюю оценку пользователя
    avg_user_rate = total_user_rate / count
    user_rate, created = mdl.CommonUsersRate.objects.get_or_create(user=user)
    user_rate.rate = math.floor(avg_user_rate * 10) / 10
    user_rate.save()

    # рассчитываем средннюю оценку вопроса
    for question in questions:
        avg_question_rate = mdl.Answer.objects.filter(
            question=question).aggregate(avg=Avg('rate'))['avg'] or 0.0
        common_q_rate, created = mdl.CommonQuestionsRate.objects.get_or_create(
            question=question
        )
        common_q_rate.rate = math.floor(avg_question_rate * 10) / 10
        common_q_rate.save()

    # рассчитываем общую оценку
    avg_rate = mdl.CommonUsersRate.objects.aggregate(avg=Avg('rate'))[
        'avg'] or 0.0
    event_rate, created = mdl.CommonEventRate.objects.get_or_create()
    event_rate.rate = math.floor(avg_rate * 10) / 10
    event_rate.save()
