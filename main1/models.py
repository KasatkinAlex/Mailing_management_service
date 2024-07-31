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
    periods = (
        ("ЕЖЕДНЕВНО", "раз в день"),
        ("ЕЖЕНЕДЕЛЬНО", "раз в неделю"),
        ("Ежемесячно", "раз в месяц")
    )
    status_newsletter = (
        ("завершена", "завершена"),
        ("создана", "создана"),
        ("запущена", "запущена")
    )

    date_time_go = models.DateField(verbose_name="дата и время первой отправки рассылки",
                                        help_text="Введите дату и время первой отправки рассылки")
    period = models.CharField(max_length=100, verbose_name="периодичность", help_text="выберите периодичность",
                              choices=periods)
    status = models.CharField(max_length=100, verbose_name="статус рассылки",
                              choices=status_newsletter, default="создана")
    massage = models.ManyToManyField(Message, verbose_name="Сообщение",
                                     help_text='Выберите сообщение для отправки')
    client = models.ManyToManyField(Client, verbose_name="Клиент для отправки",
                                    help_text='Выберите клиента кому отправить')
    user_creator = models.ForeignKey(Users, verbose_name="Пользователь который создал рассылку",
                                     help_text='Укажите пользователя который создал рассылку',
                                     on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)
    publication_sign = models.BooleanField(default=True, verbose_name="признак активности рассылки")

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

