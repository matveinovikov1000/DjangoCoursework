from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите ваш Email"
    )
    avatar = models.ImageField(
        upload_to="user/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите изображения для аватара",
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Укажите ваш номер телефона",
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна пребывания",
        blank=True,
        null=True,
        help_text="Укажите страну пребывания",
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "email",
            "phone_number",
            "country",
        ]
        permissions = [
            ("user_blocking", "user blocking"),
        ]

    def __str__(self):
        return self.email
