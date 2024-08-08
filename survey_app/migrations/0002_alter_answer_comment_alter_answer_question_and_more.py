# Generated by Django 5.0.8 on 2024-08-07 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='rate',
            field=models.IntegerField(blank=True, null=True, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.user', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='commoneventrate',
            name='rate',
            field=models.FloatField(blank=True, null=True, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='commonquestionsrate',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='commonquestionsrate',
            name='rate',
            field=models.FloatField(blank=True, null=True, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='commonusersrate',
            name='rate',
            field=models.FloatField(blank=True, null=True, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='commonusersrate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.user', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_view',
            field=models.IntegerField(choices=[(0, 'Оценка'), (1, 'Текст')], default=0, verbose_name='Вид ответа'),
        ),
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='reason',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Причина отсутствия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tg_id',
            field=models.BigIntegerField(verbose_name='Телеграм ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='was_in',
            field=models.BooleanField(blank=True, null=True, verbose_name='Был(а) на мероприятии'),
        ),
    ]
