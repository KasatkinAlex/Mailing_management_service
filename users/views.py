import random
import secrets

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import Users

from config.settings import EMAIL_HOST_USER


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Users
    success_url = reverse_lazy('users:users_list')

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            return UserUpdateForm
        raise PermissionDenied


class UserCreateView(CreateView):
    model = Users
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    # def get_form_class(self):
    #     user = self.request.user
    #     if user.is_superuser or user.groups.filter(name='Менеджер').exists():
    #         return UserUpdateForm
    #     else:
    #         return UserRegisterForm

    """верификация пользователя по почте"""
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = Users


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Users


def email_verification(request, token):
    user = get_object_or_404(Users, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(Users, email=email)
        digits = '0123456789abcdfABCDF'
        new_password = ''.join(random.sample(digits, 8))
        user.password = make_password(new_password)
        user.save()
        send_mail(
            subject="Востановление пароля",
            message=f"Здравствуйте, Ваш новый пароль на сайт {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
    return render(request, 'users/password_reset.html')


