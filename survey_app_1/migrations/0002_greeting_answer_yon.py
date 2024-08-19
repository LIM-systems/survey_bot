# Generated by Django 5.0.8 on 2024-08-19 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app_1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Greeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Приветственный текст')),
            ],
            options={
                'verbose_name': 'Приветственный текст',
                'verbose_name_plural': 'Приветственный текст',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='yon',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Да/Нет'),
        ),
    ]
