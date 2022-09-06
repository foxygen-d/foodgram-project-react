from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Имя',
        help_text='Имя',
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        help_text='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        help_text='Фамилия',
    )
    email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name='Электронная почта',
        help_text='Адрес электронной почты',
    )
    password = models.CharField(
        max_length=50,
        verbose_name='Пароль',
        help_text='Пароль',
    )

    class Meta:
        ordering=['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
