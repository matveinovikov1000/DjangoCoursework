from django.contrib.auth.views import LoginView
from django.urls import path

from user.apps import UserConfig
from user.services import block_user, email_verification
from user.views import (PasswordRecoveryView, UserDetailView, UserListView,
                        UserRegisterView, UserUpdateView, logout_view)

app_name = UserConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("user-profile/<int:pk>/", UserDetailView.as_view(), name="user-profile"),
    path("user_update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path(
        "password_recovery/", PasswordRecoveryView.as_view(), name="password_recovery"
    ),
    path("block_user/<int:pk>", block_user, name="block_user"),
    path("user_list", UserListView.as_view(), name="user_list"),
]
