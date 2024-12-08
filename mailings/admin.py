from django.contrib import admin

from mailings.models import MailingAttempt, Message, Newsletter, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "letter_header", "letter_text")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "massage")
    list_filter = ("status", "recipients")


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "mail_server_response", "newsletter")
    list_filter = ("newsletter",)
