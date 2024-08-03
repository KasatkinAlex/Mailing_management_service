from django.db import models

from users.models import Users


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name="Почта клиента", help_text="Введите почту отправки сообщений")
    name = models.CharField(max_length=150, verbose_name="Ф.И.О", help_text="Введите Ф.И.О клиента")
    comment = models.TextField(verbose_name="комментарий", help_text="Введите комментарий к клиенту")
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата последнего изменения', auto_now=True)

    user_creator = models.ForeignKey(Users, verbose_name="Пользователь который создал продукт",
                                     help_text='Укажите пользователя который создал продукт',
                                     on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['created_at']


class Message(models.Model):
    name = models.CharField(max_length=200, verbose_name="тема письма", help_text="Введите тему письма")
    text = models.TextField(verbose_name="тело письма.", help_text="Введите сообщение клиенту")
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Дата последнего изменения', auto_now=True)
    user_creator = models.ForeignKey(Users, verbose_name="Пользователь который создал сообщение",
                                     help_text='Укажите пользователя который создал сообщение',
                                     on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Собщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']


class Newsletter(models.Model):

    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    periods = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    status_newsletter = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    date_time_go = models.DateTimeField(verbose_name="дата и время первой отправки рассылки",
                                        help_text="Введите дату и время первой отправки рассылки дд.мм.год час:мин:сек")
    end_time = models.DateTimeField(verbose_name='время окончания рассылки',
                                    help_text="Введите дату и время окончания рассылки дд.мм.год час:мин:сек")
    period = models.CharField(max_length=100, verbose_name="периодичность", help_text="выберите периодичность",
                              choices=periods)
    status = models.CharField(max_length=100, verbose_name="статус рассылки",
                              choices=status_newsletter, default=CREATED)
    massage = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение",
                                help_text='Выберите сообщение для отправки')
    client = models.ManyToManyField(Client, verbose_name="Клиент для отправки",
                                    help_text='Выберите клиента кому отправить')
    user_creator = models.ForeignKey(Users, verbose_name="Пользователь который создал рассылку",
                                     help_text='Укажите пользователя который создал рассылку',
                                     on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    def __str__(self):
        return f'Отправленно клиенту {self.client}, статус {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['created_at']

        permissions = [
            ("set_is_activ_user", "Может блокировать пользователей сервиса"),
            ("set_newsletter_status", "Может отключать рассылки."),
        ]


class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок", help_text="Введите название записи блога")
    slug = models.CharField(max_length=150, verbose_name="челевекочитаемая ссылка", null=True, blank=True)
    content = models.TextField(verbose_name="содержимое", help_text="Введите содержимое блога")
    image = models.ImageField(upload_to='blog_image/', verbose_name="превью (изображение)", null=True, blank=True,
                              help_text="Загрузите изображение блога")
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    publication_sign = models.BooleanField(default=True, verbose_name="признак публикации")
    views_count = models.IntegerField(default=0, verbose_name="просмотры")

    def __str__(self):
        return f'{self.title} {self.publication_sign}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['created_at']


class MailingAttemptLog(models.Model):
    SUCCESS = 'Успешно'
    FAIL = 'Неуспешно'
    STATUS_VARIANTS = [
        (SUCCESS, 'Успешно'),
        (FAIL, 'Неуспешно'),
    ]

    time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", auto_now_add=True, null=True
    )
    status = models.CharField(max_length=50, choices=STATUS_VARIANTS, verbose_name='Cтатус рассылки')
    server_response = models.CharField(
        max_length=150, verbose_name="Ответ сервера почтового сервиса", null=True, blank=True
    )
    mailing = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name="Рассылка", null=True)

    def __str__(self):
        return f"{self.mailing} {self.time} {self.status} {self.server_response}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"