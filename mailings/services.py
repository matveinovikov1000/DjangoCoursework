import smtplib

from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from config import settings
from mailings.models import MailingAttempt, Newsletter


def send_newsletter(request, pk):
    """Отправляет рассылки"""
    newsletter = get_object_or_404(Newsletter, id=pk)
    try:
        server_response = send_mail(
            newsletter.massage.letter_header,
            newsletter.massage.letter_text,
            settings.EMAIL_HOST_USER,
            recipient_list=[
                recipient.email for recipient in newsletter.recipients.all()
            ],
            fail_silently=False,
        )
        mailing_attempt = MailingAttempt.objects.create(
            newsletter=newsletter, mail_server_response=server_response
        )
        if server_response:
            mailing_attempt.status = "successful"
            mailing_attempt.save()
    except smtplib.SMTPException as e:
        mailing_attempt = MailingAttempt.objects.create(
            newsletter=newsletter, mail_server_response=e
        )
        mailing_attempt.status = "not successful"
        mailing_attempt.save()
    if newsletter.status == "created":
        newsletter.status = "launched"
        newsletter.save()
    return redirect("mailings:newsletter_list")


def get_mailing_from_cache():
    """Получение данных из кэша, если кэш пуст берем из БД."""
    if not settings.CACHE_ENABLED:
        return Newsletter.objects.all()
    key = "mailing_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = Newsletter.objects.all()
    cache.set(key, cache_data)
    return cache_data


def get_attempt_from_cache():
    """Получение данных из кэша, если кэш пуст берем из БД."""
    if not settings.CACHE_ENABLED:
        return MailingAttempt.objects.all()
    key = "attempt_list"
    cache_data = cache.get(key)
    if cache_data is not None:
        return cache_data
    cache_data = MailingAttempt.objects.all()
    cache.set(key, cache_data)
    return cache_data


@login_required
@permission_required("user.user_blocking")
def block_mailing(request, pk):
    mailing = Newsletter.objects.get(pk=pk)
    mailing.is_active = {mailing.is_active: False, not mailing.is_active: True}[True]
    mailing.save()
    return redirect(reverse("mailings:newsletter_list"))
