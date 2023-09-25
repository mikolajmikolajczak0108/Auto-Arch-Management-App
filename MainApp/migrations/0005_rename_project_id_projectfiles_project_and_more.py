# Generated by Django 4.2.5 on 2023-09-13 10:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MainApp", "0004_projectcomments"),
    ]

    operations = [
        migrations.RenameField(
            model_name="projectfiles",
            old_name="project_id",
            new_name="project",
        ),
        migrations.RemoveField(
            model_name="projectfiles",
            name="file_id",
        ),
        migrations.RemoveField(
            model_name="projectfiles",
            name="project_file_id",
        ),
        migrations.AddField(
            model_name="projectfiles",
            name="description",
            field=models.TextField(default="something"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projectfiles",
            name="file",
            field=models.FileField(
                default="something",
                upload_to="C:\\Users\\micro\\PycharmProjects\\AutoArch\\AutoArch\\static/media/projects/project_files",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projectfiles",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=0,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projectfiles",
            name="name",
            field=models.CharField(default="test", max_length=255),
            preserve_default=False,
        ),
    ]
