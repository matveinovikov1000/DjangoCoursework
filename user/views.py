import secrets

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)

from config.settings import EMAIL_HOST_USER
from user.forms import PasswordRecoveryForm, UserRegisterForm, UserUpdateForm
from user.models import User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("user:user-profile")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user/user_detail.html"


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Пройди поссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect("user:login")


class PasswordRecoveryView(FormView):
    template_name = "user/password_recovery.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = get_object_or_404(User, email=email)
        new_password = secrets.token_hex(8)
        user.set_password(new_password)
        user.save()
        send_mail(
            subject="Восстановление пароля от сервиса рассылок",
            message=f"Привет! Ваш новый пароль {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "user/user_list.html"
