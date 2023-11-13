# Generated by Django 4.2.5 on 2023-10-02 17:06

import MainApp.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileExtensions",
            fields=[
                ("extension_id", models.AutoField(primary_key=True, serialize=False)),
                ("extension", models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Files",
            fields=[
                ("file_id", models.AutoField(primary_key=True, serialize=False)),
                ("file_name", models.CharField(max_length=255)),
                (
                    "upload_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "extension_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.fileextensions",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FileTypes",
            fields=[
                ("type_id", models.AutoField(primary_key=True, serialize=False)),
                ("file_type", models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProjectPriority",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("level", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Projects",
            fields=[
                ("project_id", models.AutoField(primary_key=True, serialize=False)),
                ("project_name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("is_completed", models.BooleanField(default=False)),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("low", "Low"),
                            ("medium", "Medium"),
                            ("high", "High"),
                        ],
                        default="medium",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectUserRoles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=50, unique=True)),
                ("password_hash", models.CharField(max_length=100)),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, null=True, upload_to=MainApp.models.user_avatar_path
                    ),
                ),
                (
                    "date_joined",
                    models.DateField(
                        default=datetime.datetime(
                            2023, 10, 2, 17, 6, 6, 154147, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                (
                    "user_role",
                    models.CharField(
                        choices=[
                            ("dyrektor", "Dyrektor"),
                            ("projektant", "Projektant"),
                            ("ksiegowy", "Księgowy"),
                            ("administrator", "Administrator"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectMembers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.projects",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="MainApp.projectuserroles",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectFiles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="C:\\Users\\micro\\PycharmProjects\\AutoArch\\AutoArch\\static/media/projects/project_files"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "extension",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.fileextensions",
                    ),
                ),
                (
                    "file_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.filetypes",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.projects",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectComments",
            fields=[
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("comment_text", models.TextField()),
                (
                    "comment_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.projects",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Messages",
            fields=[
                ("message_id", models.AutoField(primary_key=True, serialize=False)),
                ("message_text", models.TextField()),
                ("send_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_read", models.BooleanField(default=False)),
                (
                    "project_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.projects",
                    ),
                ),
                (
                    "receiver_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MessageAttachments",
            fields=[
                ("attachment_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "file_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="MainApp.files"
                    ),
                ),
                (
                    "message_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="MainApp.messages",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Investors",
            fields=[
                ("investor_id", models.AutoField(primary_key=True, serialize=False)),
                ("investor_name", models.CharField(max_length=255)),
                ("investor_address", models.CharField(max_length=255)),
                ("investor_phone", models.CharField(max_length=20)),
                ("investor_email", models.EmailField(max_length=100)),
                (
                    "project_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MainApp.projects",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="files",
            name="file_type_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="MainApp.filetypes"
            ),
        ),
        migrations.AddField(
            model_name="files",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
