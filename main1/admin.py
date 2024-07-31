from django.contrib import admin

from main1.models import Client, Message, Newsletter


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


# @admin.register(VersionProduct)
# class VersionProductAdmin(admin.ModelAdmin):
#     list_display = ('version_number', 'version_title', 'version_activ')
#     search_fields = ('version_title', 'version_number', 'version_activ')
