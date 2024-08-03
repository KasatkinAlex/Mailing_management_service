import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from main1.models import Newsletter, MailingAttemptLog


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Newsletter.objects.filter(status='Запущена')

        for mailing in mailings:
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
