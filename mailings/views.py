from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailings.forms import MessageForm, NewsletterForm, RecipientForm
from mailings.models import MailingAttempt, Message, Newsletter, Recipient


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "mailings/recipient_detail.html"


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailings/recipient_list.html"

    def get_queryset(self, *args, **kwargs):
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailings:recipient_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailings:recipient_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailings/message_detail.html"


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"

    def get_queryset(self, *args, **kwargs):
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailings:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    template_name = "mailings/newsletter_detail.html"


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = "mailings/newsletter_list.html"

    def get_queryset(self, *args, **kwargs):
        if (
            self.request.user.is_superuser
            or self.request.user.groups.filter(name="Менеджеры").exists()
        ):
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailings:newsletter_list")

    def form_valid(self, form):
        newsletter = form.save()
        newsletter.owner = self.request.user
        newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailings:newsletter_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy("mailings:newsletter_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
            self.object.owner != self.request.user
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied
        return self.object


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailings/mailingattempt_list.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get_queryset()
        elif self.request.user.groups.filter(name="Пользователи").exists():
            return super().get_queryset().filter(owner=self.request.user)
        raise PermissionDenied


class HomeTemplateView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["len_newsletter"] = len(Newsletter.objects.all())
        context_data["len_launched_newsletter"] = len(
            Newsletter.objects.filter(status="launched")
        )
        context_data["len_recipients"] = len(Recipient.objects.all())
        return context_data
