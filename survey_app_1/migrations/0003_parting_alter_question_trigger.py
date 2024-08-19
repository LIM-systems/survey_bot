# Generated by Django 5.0.8 on 2024-08-19 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app_1', '0002_greeting_answer_yon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Завершающий текст')),
            ],
            options={
                'verbose_name': 'Завершающий текст',
                'verbose_name_plural': 'Завершающий текст',
            },
        ),
        migrations.AlterField(
            model_name='question',
            name='trigger',
            field=models.IntegerField(choices=[(0, '1,2,3'), (1, '1,2,3,4'), (2, '4,5'), (3, '5'), (4, 'Да'), (5, 'Нет')], default=0, help_text='Выберите триггер по кототорому будет задаваться связанный вопрос', verbose_name='Триггер'),
        ),
    ]
