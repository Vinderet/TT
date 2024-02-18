from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import TestSet, Question, Answer


class TestSetAdmin(admin.ModelAdmin):
    # Определение полей, отображаемых в административной панели
    list_display = ['title']

    # Краткое название
    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'Name'

    # Краткое описание
    def get_description(self, obj):
        return obj.description

    get_description.short_description = 'Description'

    # Обработка множественных выборов
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "questions":
            kwargs["required"] = False
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(TestSet, TestSetAdmin)


class AnswerInlineFormSet(BaseInlineFormSet):
    # Проверка правильности ответов перед сохранением
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
    # Количество дополнительных форм для ответов
    extra = 4
    # Минимальное количество ответов
    min_num = 4
    # Максимальное количество ответов
    max_num = 4
    # Использование пользовательской формы набора ответов
    formset = AnswerInlineFormSet


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test_set']
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
