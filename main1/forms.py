from django.forms import BooleanField, ModelForm

from main1.models import Client, Message, Newsletter


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ("user_creator",)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("created_at", "updated_at", "user_creator")


class NewsletterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        exclude = ("status", "user_creator", "created_at")


class NewsletterManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = ("status",)
