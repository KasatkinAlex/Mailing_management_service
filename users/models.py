from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    username = None

    avatar = models.ImageField(upload_to='avatar_user/', verbose_name='аватар', help_text='загрузите Ваше фото',
                               null=True, blank=True, )
    phone = models.CharField(max_length=30, verbose_name='телефон', null=True, blank=True)
    country = models.CharField(max_length=30, verbose_name='страна')

    email = models.EmailField(max_length=100, unique=True, verbose_name='почта')

    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
