from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from main1.forms import StyleFormMixin
from users.models import Users


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'password1', 'password2')


class UserUpdateForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Users
        fields = ('is_active',)
