from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)
        kwargs.pop('test_set', None)  # Убираем аргумент test_set из kwargs
        super(TestForm, self).__init__(*args, **kwargs)

        if questions is not None:
            for question in questions:
                choices = [(answer.id, answer.text) for answer in question.answer_set.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect,
                    required=True
                )

    def clean(self):
        cleaned_data = super().clean()
        questions = [field_name for field_name in cleaned_data if field_name.startswith('question_')]
        for question_id in questions:
            selected_answer_id = cleaned_data[question_id]
            question = Question.objects.get(id=question_id.split('_')[1])
            correct_answer = question.answer_set.filter(is_correct=True).first()
        return cleaned_data
