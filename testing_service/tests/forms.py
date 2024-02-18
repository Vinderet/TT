from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)
        kwargs.pop('test_set', None)
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
        # Remove the 'current_question_index' field from the cleaned data
        cleaned_data.pop('current_question_index', None)
        return cleaned_data





