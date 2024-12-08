from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.services import block_mailing, send_newsletter
from mailings.views import (HomeTemplateView, MailingAttemptListView,
                            MessageCreateView, MessageDeleteView,
                            MessageDetailView, MessageListView,
                            MessageUpdateView, NewsletterCreateView,
                            NewsletterDeleteView, NewsletterDetailView,
                            NewsletterListView, NewsletterUpdateView,
                            RecipientCreateView, RecipientDeleteView,
                            RecipientDetailView, RecipientListView,
                            RecipientUpdateView)

app_name = MailingsConfig.name

urlpatterns = [
    path(
        "recipient/<int:pk>/",
        cache_page(60)(RecipientDetailView.as_view()),
        name="recipient",
    ),
    path(
        "recipient_list/",
        cache_page(60)(RecipientListView.as_view()),
        name="recipient_list",
    ),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipient_update/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient_delete/<int:pk>/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path(
        "message/<int:pk>/", cache_page(60)(MessageDetailView.as_view()), name="message"
    ),
    path(
        "message_list/", cache_page(60)(MessageListView.as_view()), name="message_list"
    ),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path(
        "newsletter/<int:pk>/",
        cache_page(60)(NewsletterDetailView.as_view()),
        name="newsletter",
    ),
    path(
        "newsletter_list/",
        cache_page(60)(NewsletterListView.as_view()),
        name="newsletter_list",
    ),
    path(
        "newsletter_create/", NewsletterCreateView.as_view(), name="newsletter_create"
    ),
    path(
        "newsletter_update/<int:pk>/",
        NewsletterUpdateView.as_view(),
        name="newsletter_update",
    ),
    path(
        "newsletter_delete/<int:pk>/",
        NewsletterDeleteView.as_view(),
        name="newsletter_delete",
    ),
    path("send_message/<int:pk>/", send_newsletter, name="send_message"),
    path(
        "mailing_list/",
        cache_page(60)(MailingAttemptListView.as_view()),
        name="mailing_list",
    ),
    path("home/", HomeTemplateView.as_view(), name="home"),
    path("block_mailing/<int:pk>/", block_mailing, name="block_mailing"),
]
