import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from pytils.templatetags.pytils_translit import slugify

from main1.forms import ClientForm, MessageForm, NewsletterForm, NewsletterManagerForm
from main1.models import Client, Message, Newsletter, BlogPost, MailingAttemptLog


class ClientListView(ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main1:client_detail', args=[self.kwargs.get('pk')])


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main1:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.user_creator = user
        client.save()
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main1:client_list')

# РАБОТА С СООБЩЕНИЯМИ __________________________________________________________________________


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main1:message_detail', args=[self.kwargs.get('pk')])


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main1:message_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.user_creator = user
        client.save()
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main1:client_list')


# РАБОТА С РАССЫЛКАМИ___________________________________


class NewsletterListView(ListView):
    model = Newsletter


class NewsletterDetailView(DetailView):
    model = Newsletter


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    # form_class = NewsletterForm

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser or user == self.object.user_creator:
            return NewsletterForm
        elif user.groups.filter(name='Менеджер').exists():
            return NewsletterManagerForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse('main1:newsletter_detail', args=[self.kwargs.get('pk')])


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('main1:newsletter_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.user_creator = user
        client.save()
        return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('main1:client_list')


# ______________________БЛОГ_______________________________________

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ('title', 'content', 'image', 'publication_sign')
    success_url = reverse_lazy('main1:home')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'image', 'publication_sign')
    success_url = reverse_lazy('main1:home')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main1:blogpost_detail', args=[self.kwargs.get('pk')])


class BlogPostListView(ListView):
    model = BlogPost

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication_sign=True)
        return queryset


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class HomePage(TemplateView):
    template_name = "main1/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = BlogPost.objects.all()
        post_list = []
        for p in post:
            post_list.append(p)
        if len(post_list) < 3:
            post_list_sample = post_list
        else:
            post_list_sample = random.sample(post_list, 3)
        context['blogpost'] = post_list_sample

        newsletter = Newsletter.objects.all()
        context['newsletter_sum'] = len(newsletter)
        context['newsletter_activ'] = len(newsletter.filter(status="Запущена"))

        clients = Client.objects.all()
        clients_list = []
        for client in clients:
            clients_list.append(client.email)
        context['client_unique'] = len(set(clients_list))

        return context

# ____________________Попытка рассылки:_____________________


class MailingAttemptLogListView(LoginRequiredMixin, ListView):
    model = MailingAttemptLog

