from django import forms
from django.contrib.auth.forms import UserCreationForm

from mailings.forms import StyleFormMixin
from user.models import User


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "avatar", "phone_number", "country")


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class PasswordRecoveryForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label="Введите email")

    def checking_mail(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email не найден")
        return email
