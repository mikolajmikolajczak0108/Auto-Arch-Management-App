from django.contrib import admin
from .models import Users, FileTypes, FileExtensions, Files, Projects, ProjectFiles, Investors, Messages
from .models import Projects, ProjectMembers  # i inne modele, które masz


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'user_role')

@admin.register(FileTypes)
class FileTypesAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'file_type')

@admin.register(FileExtensions)
class FileExtensionsAdmin(admin.ModelAdmin):
    list_display = ('extension_id', 'extension')

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('file_id', 'file_name', 'user_id', 'file_type_id', 'extension_id')

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'start_date')

@admin.register(Investors)
class InvestorsAdmin(admin.ModelAdmin):
    list_display = ('investor_id', 'investor_name', 'project_id')

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender_id', 'receiver_id', 'project_id', 'send_date', 'is_read')

admin.site.register(ProjectFiles)