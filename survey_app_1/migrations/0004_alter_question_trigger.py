# Generated by Django 5.0.8 on 2024-08-19 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app_1', '0003_parting_alter_question_trigger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='trigger',
            field=models.IntegerField(choices=[('1,2,3', '1,2,3'), ('1,2,3,4', '1,2,3,4'), ('4,5', '4,5'), ('5', '5'), ('Да', 'Да'), ('Нет', 'Нет')], default=0, help_text='Выберите триггер по кототорому будет задаваться связанный вопрос', verbose_name='Триггер'),
        ),
    ]
