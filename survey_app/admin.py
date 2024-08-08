from django.contrib import admin
from survey_app import models as md

# Register your models here.

# пользователи


@admin.register(md.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'tg_id', 'was_in', 'reason')
    list_filter = ('was_in',)
    search_fields = ('name', 'tg_id', 'reason')


# вопросы
@admin.register(md.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'answer_view')
    list_filter = ('answer_view',)
    search_fields = ('name',)


# ответы
@admin.register(md.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'rate', 'comment')
    list_filter = ('user', 'question', 'rate')
    search_fields = ('user', 'question', 'comment')


# общие оценки пользователей
@admin.register(md.CommonUsersRate)
class CommonUsersRateAdmin(admin.ModelAdmin):
    list_display = ('user', 'rate')
    list_filter = ('user', 'rate')
    search_fields = ('user',)


# общий оценки вопросов
@admin.register(md.CommonQuestionsRate)
class CommonQuestionsRateAdmin(admin.ModelAdmin):
    list_display = ('question', 'rate')
    list_filter = ('question', 'rate')
    search_fields = ('question',)


# общая оценка мероприятия
@admin.register(md.CommonEventRate)
class CommonEventRateAdmin(admin.ModelAdmin):
    list_display = ('rate',)
