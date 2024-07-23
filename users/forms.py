from django.contrib.auth.forms import UserCreationForm

from main.forms import StyleFormMixin
from users.models import Users


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'password1', 'password2')
