from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('tests/', views.tests_list, name='tests_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('take_test/<int:test_set_id>/', views.take_test, name='take_test'),
    path('take_test/<int:test_set_id>/question/<int:question_index>/', views.take_single_question, name='take_single_question'),

    path('test_result/<int:test_set_id>/<int:correct_answers>/<int:total_questions>/', views.test_result,
         name='test_result'),
]
