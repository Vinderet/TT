from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('tests/', views.tests_list, name='tests_list'),
    path('test/<int:test_set_id>/', views.take_test, name='take_test'),
    path('test/result/<int:test_set_id>/<int:correct_answers>/<int:total_questions>/', views.test_result,
         name='test_result'),
]
