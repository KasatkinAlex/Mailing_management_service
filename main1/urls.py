from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from main1.apps import MainConfig
from main1.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MessageListView, MessageDeleteView, MessageUpdateView, MessageCreateView, MessageDetailView, NewsletterCreateView, \
    NewsletterListView, NewsletterDetailView, NewsletterUpdateView, NewsletterDeleteView

app_name = MainConfig.name


urlpatterns = [
    path('', ClientListView.as_view(), name="client_list"),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name="client_detail"),
    path('client_create', ClientCreateView.as_view(), name="client_create"),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name="client_update"),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name="client_delete"),

    path('message_list', MessageListView.as_view(), name="message_list"),
    path('message_detail/<int:pk>', MessageDetailView.as_view(), name="message_detail"),
    path('message_create', MessageCreateView.as_view(), name="message_create"),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name="message_update"),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name="message_delete"),

    path('newsletter_list', NewsletterListView.as_view(), name="newsletter_list"),
    path('newsletter_detail/<int:pk>', NewsletterDetailView.as_view(), name="newsletter_detail"),
    path('newsletter_update/<int:pk>', NewsletterUpdateView.as_view(), name="newsletter_update"),
    path('newsletter_delete/<int:pk>', NewsletterDeleteView.as_view(), name="newsletter_delete"),
    path('newsletter_create', NewsletterCreateView.as_view(), name="newsletter_create"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
