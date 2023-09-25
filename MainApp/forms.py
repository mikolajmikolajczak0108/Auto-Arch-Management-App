from django import forms
from .models import Users, Projects, ProjectMembers, ProjectComments
from .models import Users, ProjectUserRoles
import hashlib

class CustomMultiFileInput(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'multiple': 'multiple'})


class MessageForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=Users.objects.all(), label="Do:")
    project = forms.ModelChoiceField(queryset=Projects.objects.all(), label="Projekt:")
    message = forms.CharField(widget=forms.Textarea, label="Wiadomość:")
    attachments = forms.FileField(label="Dodaj plik:", required=False)

class AddProjectMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Users.objects.all())
    project = forms.ModelChoiceField(queryset=Projects.objects.all())

    class Meta:
        model = ProjectMembers
        fields = ('user', 'project')


class RemoveProjectMemberForm(forms.ModelForm):
    project_member = forms.ModelChoiceField(queryset=ProjectMembers.objects.all())

    class Meta:
        model = ProjectMembers
        fields = ('project_member',)


class UpdateProjectMemberRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=ProjectUserRoles.objects.all())

    class Meta:
        model = ProjectMembers
        fields = ('role',)


class AddProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComments
        fields = ['comment_text']

class ChangeRoleForm(forms.ModelForm):
    new_role = forms.ChoiceField(choices=Users.ROLE_CHOICES)

    class Meta:
        model = Users
        fields = ['new_role']

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Hasło'
    )

    class Meta:
        model = Users
        fields = ['username', 'password', 'avatar', 'user_role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control-file custom-file-input',  # dodanie klasy custom-file-input
                'accept': '.jpg,.png,.bmp',
                'style': 'display: none;',  # ukrycie oryginalnego inputu
                'id': 'fileInput'
            }),
            'user_role': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nazwa użytkownika',
            'avatar': 'Wybierz plik',
            'user_role': 'Rola użytkownika',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user.password_hash = hashed_password
        if commit:
            user.save()
        return user