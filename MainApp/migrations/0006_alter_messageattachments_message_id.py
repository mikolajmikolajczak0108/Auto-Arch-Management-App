# Generated by Django 4.2.5 on 2023-09-17 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("MainApp", "0005_rename_project_id_projectfiles_project_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="messageattachments",
            name="message_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attachments",
                to="MainApp.messages",
            ),
        ),
    ]