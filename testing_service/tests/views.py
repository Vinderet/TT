from django.urls import reverse

from .forms import UserRegistrationForm, TestForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import TestSet, Question


def home(request):
    test_sets = TestSet.objects.all()
    return render(request, 'tests/home.html', {'test_sets': test_sets})


def tests_list(request):
    test_sets = TestSet.objects.all()
    return render(request, 'tests/tests_list.html', {'test_sets': test_sets})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'tests/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправляем пользователя на домашнюю страницу или куда-то еще после входа
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'tests/login.html')




def take_test(request, test_set_id):
    test_set = TestSet.objects.get(id=test_set_id)
    questions = Question.objects.filter(test_set=test_set)

    print("Test set:", test_set)
    print("Questions:", questions)

    if request.method == 'POST':
        form = TestForm(request.POST, test_set=test_set, questions=questions)
        if form.is_valid():
            correct_answers = 0
            total_questions = questions.count()

            # Подсчитываем количество правильных ответов
            for question in questions:
                selected_answer_id = form.cleaned_data[f'question_{question.id}']
                correct_answer = question.answer_set.filter(is_correct=True).first()
                if selected_answer_id == str(correct_answer.id):
                    correct_answers += 1

            return redirect('test_result', test_set_id=test_set_id, correct_answers=correct_answers, total_questions=total_questions)
    else:
        form = TestForm(test_set=test_set, questions=questions)

    remaining_questions = questions.count()

    return render(request, 'tests/take_test.html', {
        'form': form,
        'test_set': test_set,
        'questions': questions,
        'remaining_questions': remaining_questions
    })


def test_result(request, test_set_id, correct_answers, total_questions):
    test_set = get_object_or_404(TestSet, id=test_set_id)
    percentage_correct = round((correct_answers / total_questions) * 100 if total_questions != 0 else 0, 2)

    return render(request, 'tests/test_result.html', {
        'test_set': test_set,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'percentage_correct': percentage_correct,
        'home_url': reverse('home')
    })