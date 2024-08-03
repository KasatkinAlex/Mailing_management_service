from django.contrib import admin

from main1.models import Client, Message, Newsletter, MailingAttemptLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'created_at', 'user_creator',)
    list_filter = ('created_at',)
    search_fields = ('name', 'created_at')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'status', 'user_creator', 'period', 'date_time_go')
    search_fields = ('status', 'user_creator', 'client')


@admin.register(MailingAttemptLog)
class MailingAttemptLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'time', 'status', 'mailing', 'server_response')
    search_fields = ('status', 'time')

