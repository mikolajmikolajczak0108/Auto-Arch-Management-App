# Generated by Django 4.2.5 on 2023-09-18 12:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("MainApp", "0009_users_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="last_activity",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]