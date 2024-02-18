from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="user_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="user_permissions", blank=True
    )

    class Meta:
        permissions = [
            ("can_view_group", "Can view group"),
        ]


class TestSet(models.Model):
    # Название теста
    title = models.CharField(max_length=100)
    # Вопросы теста
    questions = models.ManyToManyField('Question', related_name='test_sets')

    def __str__(self):
        return self.title


class Question(models.Model):
    # Тест, к которому относится вопрос
    test_set = models.ForeignKey(TestSet, on_delete=models.CASCADE)
    # Текст вопроса
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    # Вопрос, к которому относится ответ
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Текст ответа
    text = models.CharField(max_length=255)
    # Флаг правильного ответа
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
