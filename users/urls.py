from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, password_reset, UserUpdateView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    path("password_reset/", password_reset, name='password_reset'),
    path("user_update/<int:pk>", UserUpdateView.as_view(), name='user_update'),
    path("user_list/", UserListView.as_view(), name='users_list')

]
