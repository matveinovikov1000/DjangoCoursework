from django.db import models

from user.models import User


class Recipient(models.Model):
    """Модель "Получатель рассылки" """

    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите Email получателя"
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name="ФИО получателя рассылки",
        help_text="Введите ФИО получателя",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        help_text="Укажите комментарий",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="recipients",
    )

    class Meta:
        verbose_name = "Получатель рассылок"
        verbose_name_plural = "Получатели рассылок"
        ordering = ["email", "full_name", "comment", "owner"]

    def __str__(self):
        return self.email


class Message(models.Model):
    """Модель "Сообщение" """

    letter_header = models.CharField(
        max_length=100, verbose_name="Тема письма", help_text="Укажите тему письма"
    )
    letter_text = models.TextField(
        verbose_name="Текст письма", help_text="Укажите содержание письма"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="messages",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["letter_header", "letter_text", "owner"]

    def __str__(self):
        return self.letter_header


class Newsletter(models.Model):
    """Модель "Рассылка" """

    FIRST_STATUS = "created"
    SECOND_STATUS = "launched"
    THIRD_STATUS = "completed"

    MAILING_STATUS_CHOICES = [
        (FIRST_STATUS, "Создана"),
        (SECOND_STATUS, "Запущена"),
        (THIRD_STATUS, "Завершена"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15,
        choices=MAILING_STATUS_CHOICES,
        default=FIRST_STATUS,
        verbose_name="Статус рассылки",
    )
    massage = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Сообщение",
        help_text="Укажите тему сообщения",
        related_name="newsletters",
    )
    recipients = models.ManyToManyField(
        Recipient,
        blank=True,
        verbose_name="Получатели",
        help_text="Укажите получателей",
        related_name="newsletters",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="newsletters",
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["created_at", "updated_at", "status", "massage", "owner"]
        permissions = [
            ("disabling_mailings", "disabling mailings"),
        ]

    def __str__(self):
        return f"Сообщение: {self.massage} Получатели: {self.recipients} Статус сообщения: {self.status}"


class MailingAttempt(models.Model):
    """Модель "Попытка рассылки" """

    FIRST_STATUS = "successful"
    SECOND_STATUS = "not successful"

    MAILING_ATTEMPT_STATUS_CHOICES = [
        (FIRST_STATUS, "Успешно"),
        (SECOND_STATUS, "Не успешно"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=MAILING_ATTEMPT_STATUS_CHOICES,
        verbose_name="Статус рассылки",
    )
    mail_server_response = models.TextField(verbose_name="Ответ почтового сервера")
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Рассылка",
        related_name="mailing_attempts",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["created_at", "status", "mail_server_response", "newsletter"]

    def __str__(self):
        return self.status
