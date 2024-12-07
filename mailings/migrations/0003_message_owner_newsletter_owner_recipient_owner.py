# Generated by Django 5.1.3 on 2024-11-26 19:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailings", "0002_alter_message_options_alter_newsletter_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите пользователя",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="newsletter",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите пользователя",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="newsletters",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="recipient",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите пользователя",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="recipients",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
