import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from main1.models import Newsletter, MailingAttemptLog, Message
from django.core.cache import cache

from config.settings import CASHES_ENABLED


def send_mailing():
    """
    Функция отправки рассылок
    """
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Newsletter.objects.filter(status__in=[Newsletter.STARTED, Newsletter.CREATED])

    for mailing in mailings:
        # Если достигли end_date, завершить рассылку
        if mailing.end_time <= current_datetime:
            mailing.status = Newsletter.COMPLETED
            mailing.save()
            continue  # Пропустить отправку, если end_date достигнут

        # Проверить, нужно ли отправить сообщение в текущий момент времени
        if current_datetime >= mailing.date_time_go:
            mailing.status = Newsletter.STARTED
            clients = mailing.client.all()
            try:
                server_response = send_mail(
                    subject=mailing.massage.name,
                    message=mailing.massage.text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                MailingAttemptLog.objects.create(status=MailingAttemptLog.SUCCESS,
                                                 server_response=server_response,
                                                 mailing=mailing, )
            except smtplib.SMTPException as e:
                MailingAttemptLog.objects.create(status=MailingAttemptLog.FAIL,
                                                 server_response=str(e),
                                                 mailing=mailing, )

            # Обновление времени следующей отправки
            if mailing.period == Newsletter.DAILY:
                mailing.date_time_go += timedelta(days=1)
            elif mailing.period == Newsletter.WEEKLY:
                mailing.date_time_go += timedelta(weeks=1)
            elif mailing.period == Newsletter.MONTHLY:
                mailing.date_time_go += timedelta(days=30)

            mailing.save()


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Проверка, добавлена ли задача уже
    if not scheduler.get_jobs():
        scheduler.add_job(send_mailing, 'interval', seconds=30)

    if not scheduler.running:
        scheduler.start()


def get_messages_from_cache():
    """
    Получение списка сообщений из кэша. Если кэш пуст,то получение из БД.
    """
    if not CASHES_ENABLED:
        return Message.objects.all()
    else:
        key = 'list_cache'
        messages = cache.get(key)
        if messages is not None:
            return messages
        else:
            messages = Message.objects.all()
            cache.set(key, messages)
            return messages