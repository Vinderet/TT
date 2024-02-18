from django.urls import reverse

from .forms import UserRegistrationForm, TestForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import TestSet, Question, Answer


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

    if request.method == 'POST':
        form = TestForm(request.POST, test_set=test_set, questions=questions)
        if form.is_valid():
            correct_answers = 0
            total_questions = 0
            for question_id, answer_id in form.cleaned_data.items():
                if question_id.startswith('question_'):
                    question_id = int(question_id.split('_')[1])
                    question = questions.get(id=question_id)
                    if Answer.objects.filter(question=question, id=answer_id, is_correct=True).exists():
                        correct_answers += 1
                    total_questions += 1
            return redirect('test_result', test_set_id=test_set_id, correct_answers=correct_answers, total_questions=total_questions)
    else:
        form = TestForm(test_set=test_set, questions=questions)

    remaining_questions = questions.count()

    # If this is the first time the user is taking the test, redirect to the first question
    if request.method == 'GET' and request.session.get('current_question_index') is None:
        request.session['current_question_index'] = 0

    # If the user has answered all the questions, redirect to the test result page
    if request.method == 'POST' and request.session.get('current_question_index') == questions.count() - 1:
        correct_answers = request.session.get('correct_answers', 0)
        total_questions = request.session.get('total_questions', 0) + len(questions)
        return redirect('test_result', test_set_id=test_set_id, correct_answers=correct_answers,
                        total_questions=total_questions)

    # If the user has answered the last question, increment the current question index
    if request.method == 'POST' and request.session.get('current_question_index') < questions.count() - 1:
        request.session['current_question_index'] += 1
        return redirect('take_single_question', test_set_id=test_set_id,
                        question_index=request.session.get('current_question_index'))

    # If the user is taking the test for the first time or has answered the previous question,
    # render the template for the current question
    if request.method == 'GET' or request.method == 'POST':
        current_question_index = request.session.get('current_question_index')
        current_question = questions[current_question_index]

        if request.method == 'POST':
            form = TestForm(request.POST, test_set=test_set, questions=[current_question])
        else:
            form = TestForm(test_set=test_set, questions=[current_question])

        return render(request, 'tests/take_test.html', {
            'form': form,
            'current_question': current_question,
            'remaining_questions': remaining_questions - current_question_index - 1
        })


def take_single_question(request, test_set_id, question_index):
    test_set = TestSet.objects.get(id=test_set_id)
    questions = Question.objects.filter(test_set=test_set)
    current_question = questions[question_index]

    if request.method == 'POST':
        form = TestForm(request.POST, test_set=test_set, questions=[current_question])
        if form.is_valid():
            correct_answers = 0
            total_questions = 0
            for question_id, answer_id in form.cleaned_data.items():
                if question_id.startswith('question_'):
                    question_id = int(question_id.split('_')[1])
                    question = questions.get(id=question_id)
                    if Answer.objects.filter(question=question, id=answer_id, is_correct=True).exists():
                        correct_answers += 1
                    total_questions += 1
            request.session['correct_answers'] = correct_answers
            request.session['total_questions'] = total_questions
            return redirect('test_result', test_set_id=test_set_id)
    else:
        form = TestForm(test_set=test_set, questions=[current_question])

    return render(request, 'tests/take_test.html', {
        'form': form,
        'current_question': current_question,
        'remaining_questions': len(questions) - question_index - 1
    })


def test_result(request, test_set_id, correct_answers, total_questions):
    test_set = TestSet.objects.get(id=test_set_id)
    correct_answers = request.session.get('correct_answers', 0)
    total_questions = request.session.get('total_questions', 0)
    percentage_correct = round((correct_answers / total_questions) * 100 if total_questions != 0 else 0, 2)

    return render(request, 'tests/test_result.html', {
        'test_set': test_set,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'percentage_correct': percentage_correct,
        'home_url': reverse('home')
    })


