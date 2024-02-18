# В файле admin.py вашего приложения

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import TestSet, Question, Answer


class TestSetAdmin(admin.ModelAdmin):
    # Определение полей, отображаемых в административной панели
    list_display = ['title']

    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'Name'

    def get_description(self, obj):
        return obj.description

    get_description.short_description = 'Description'


admin.site.register(TestSet, TestSetAdmin)


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        correct_answers_count = 0
        incorrect_answers_count = 0

        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                is_correct = form.cleaned_data.get('is_correct')
                if is_correct:
                    correct_answers_count += 1
                else:
                    incorrect_answers_count += 1

        if correct_answers_count < 1 or incorrect_answers_count < 1:
            raise ValidationError("Необходимо добавить как минимум один правильный и один неправильный ответ.")

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Количество дополнительных форм для ответов
    min_num = 4  # Минимальное количество ответов
    max_num = 4  # Максимальное количество ответов
    formset = AnswerInlineFormSet  # Использование пользовательской формы набора ответов

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test_set']
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)

