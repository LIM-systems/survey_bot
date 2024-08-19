from django.db import models

# Create your models here.

# пользователи


class Greeting(models.Model):
    text = models.TextField(
        max_length=500, verbose_name='Приветственный текст')

    class Meta:
        verbose_name = 'Приветственный текст'
        verbose_name_plural = 'Приветственный текст'

    def __str__(self):
        return self.text


class Parting(models.Model):
    text = models.TextField(
        max_length=500, verbose_name='Завершающий текст')

    class Meta:
        verbose_name = 'Завершающий текст'
        verbose_name_plural = 'Завершающий текст'

    def __str__(self):
        return self.text


class User(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    tg_id = models.BigIntegerField(verbose_name='Телеграм ID')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


# вопросы
class Question(models.Model):
    ANSWER_VIEW = (
        (0, 'Оценочная шкала'),
        (1, 'Комментарий'),
        (2, 'Да/Нет'),
    )

    TRIGGER_POINTS = (
        ('1,2,3', '1,2,3'),
        ('1,2,3,4', '1,2,3,4'),
        ('4,5', '4,5'),
        ('5', '5'),
        ('Да', 'Да'),
        ('Нет', 'Нет'),
    )

    name = models.CharField(max_length=255, verbose_name='Вопрос')
    answer_view = models.IntegerField(
        choices=ANSWER_VIEW, default=0, verbose_name='Вид ответа')
    add_question = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Связанный вопрос')
    trigger = models.CharField(max_length=255, choices=TRIGGER_POINTS, default=0,
                               verbose_name='Триггер',
                               help_text='Выберите триггер по кототорому будет задаваться связанный вопрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.name


# ответы
class Answer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    yon = models.BooleanField(
        default=False, blank=True, null=True, verbose_name='Да/Нет')
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
