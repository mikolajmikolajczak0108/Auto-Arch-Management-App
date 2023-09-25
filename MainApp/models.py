from django.contrib.sessions.models import Session
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from AutoArch.settings import STATIC_DIR


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

def user_avatar_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/static/users/<username>/<filename>
    return 'static/media/users/{0}/{1}'.format(instance.username, filename)

class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    password_hash = models.CharField(max_length=100, null=False)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)
    date_joined = models.DateField(default=timezone.now())
    ROLE_CHOICES = [
        ('dyrektor', 'Dyrektor'),
        ('projektant', 'Projektant'),
        ('ksiegowy', 'Księgowy'),
        ('administrator', 'Administrator'),
    ]

    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    @property
    def is_online(self):
        if self.last_login:
            now = timezone.now()
            return now - self.last_login < timezone.timedelta(minutes=5)
        return False

    def __str__(self):
        return self.username

    def set_avatar(self):
        _avatar = self.avatar
        if not _avatar:
            pass


class FileTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    file_type = models.CharField(max_length=20, unique=True, null=False)


class FileExtensions(models.Model):
    extension_id = models.AutoField(primary_key=True)
    extension = models.CharField(max_length=10, unique=True, null=False)


class Files(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255, null=False)
    upload_date = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    file_type_id = models.ForeignKey(FileTypes, on_delete=models.CASCADE)
    extension_id = models.ForeignKey(FileExtensions, on_delete=models.CASCADE)


class ProjectPriority(models.Model):
    level = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.level


class Projects(models.Model):
    PRIORITIES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    #  priority = models.ForeignKey(ProjectPriority, null=True, blank=True, on_delete=models.SET_NULL)  # Using ForeignKey to another model
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='medium')  # Using CharField with choices

    def __str__(self):
        return self.project_name


class ProjectUserRoles(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class ProjectMembers(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.ForeignKey(ProjectUserRoles, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} as {self.role.role} in {self.project.project_name}"


class ProjectFiles(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    file = models.FileField(upload_to=str(STATIC_DIR) + '/media/projects/project_files')
    name = models.CharField(max_length=255)
    description = models.TextField()
    file_type = models.ForeignKey(FileTypes, on_delete=models.CASCADE)  # Nowa relacja
    extension = models.ForeignKey(FileExtensions, on_delete=models.CASCADE)  # Nowa relacja




class ProjectComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} commented on {self.project.project_name}"


class Investors(models.Model):
    investor_id = models.AutoField(primary_key=True)
    investor_name = models.CharField(max_length=255, null=False)
    investor_address = models.CharField(max_length=255)
    investor_phone = models.CharField(max_length=20)
    investor_email = models.EmailField(max_length=100)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)


class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(Users, related_name='sent_messages', on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(Users, related_name='received_messages', on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    message_text = models.TextField()
    send_date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


class MessageAttachments(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    message_id = models.ForeignKey(Messages, related_name='attachments', on_delete=models.CASCADE)
    file_id = models.ForeignKey(Files, on_delete=models.CASCADE)

