from django.contrib import admin
from survey_app_1 import models as md

# Register your models here.


@admin.register(md.Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(md.Parting)
class PartingAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(md.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'tg_id',)
    list_filter = ('name', 'tg_id',)


# вопросы
@admin.register(md.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'answer_view', 'add_question')
    list_filter = ('answer_view', 'add_question')
    search_fields = ('name',)


# ответы
@admin.register(md.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'yon', 'rate', 'comment')
    list_filter = ('user', 'question', 'yon', 'rate')
    search_fields = ('user', 'question', 'comment')
