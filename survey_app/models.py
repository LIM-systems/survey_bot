from django.db import models

# Create your models here.

# пользователи


class User(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    tg_id = models.BigIntegerField(verbose_name='Телеграм ID')
    was_in = models.BooleanField(
        blank=True, null=True, verbose_name='Был(а) на мероприятии')
    reason = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Причина отсутствия')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


# вопросы
class Question(models.Model):
    ANSWER_VIEW = (
        (0, 'Оценка'),
        (1, 'Текст'),
    )

    name = models.CharField(max_length=255, verbose_name='Вопрос')
    answer_view = models.IntegerField(
        choices=ANSWER_VIEW, default=0, verbose_name='Вид ответа')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.name


# ответы
class Answer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    rate = models.IntegerField(blank=True, null=True, verbose_name='Оценка')
    comment = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.question.name


# общая оценка пользователей
class CommonUsersRate(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rate = models.FloatField(blank=True, null=True, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Общая оценка пользователей'
        verbose_name_plural = 'Общие оценки пользователей'

    def __str__(self):
        return self.user.name


# общая оценка вопросов
class CommonQuestionsRate(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    rate = models.FloatField(blank=True, null=True, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Общая оценка вопросов'
        verbose_name_plural = 'Общие оценки вопросов'

    def __str__(self):
        return self.question.name


# общая оценка мероприятия
class CommonEventRate(models.Model):
    rate = models.FloatField(blank=True, null=True, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Общая оценка мероприятия'
        verbose_name_plural = 'Общая оценка мероприятия'

    def __str__(self):
        return 'Общая оценка мероприятия'
