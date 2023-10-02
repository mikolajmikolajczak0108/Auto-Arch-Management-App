import hashlib
import json
from datetime import datetime, timedelta
from django.contrib.auth import login, logout
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import AddProjectMemberForm, MessageForm, \
    AddProjectCommentForm, EmployeeForm, AddProjectForm, AddInvestorForm
from .models import Projects, Users, FileTypes, FileExtensions, Files, ProjectFiles, Investors, Messages, \
    MessageAttachments, ProjectMembers, ProjectComments
from django.db.models import Q, F
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from .utils import get_or_create_file_type, get_or_create_file_extension, custom_guess_type, ExtendedEncoder
from django.db.models import Count
from django.utils import timezone


def welcome(request):
    logout_message = request.GET.get('logout', '')
    return render(request, 'welcome.html', {'logout_message': logout_message})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Users.objects.get(username=username)
            # Wylicz hash SHA-256 na podstawie hasła wprowadzonego przez użytkownika
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if user.password_hash == password_hash:
                # Hasło jest poprawne, zaloguj użytkownika
                user_django = get_user_model().objects.get(username=username)
                login(request, user_django)

                # Ustaw czas ostatniej aktywności użytkownika w sesji
                request.session['last_activity'] = str(datetime.now())

                # Przekierowanie na stronę projektów, jeśli użytkownik jest administratorem lub dyrektorem
                if user.user_role in ['administrator', 'dyrektor']:
                    return redirect('project_list')  # Zmień na odpowiednią nazwę URL-a projektów
                else:
                    return redirect('worker_project_list')   # Przekierowanie na inną stronę dla innych użytkowników
            else:
                # Obsłuż błąd logowania, na przykład wyświetl błąd na stronie
                error_message = "Błędny login lub hasło. Spróbuj ponownie."
                return render(request, 'login.html', {'error_message': error_message})
        except Users.DoesNotExist:
            # Użytkownik o podanej nazwie nie istnieje
            error_message = "Błędny login lub hasło. Spróbuj ponownie."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # Sprawdź, czy istnieje sesja i czy minęło już 15 minut od ostatniej aktywności
        last_activity = request.session.get('last_activity')
        if last_activity:
            last_activity = datetime.fromisoformat(last_activity)
            now = datetime.now()
            if now - last_activity > timedelta(minutes=15):
                # Sesja wygasła z powodu braku aktywności przez 15 minut, wyloguj użytkownika
                request.session.flush()
                return render(request, 'login.html', {'error_message': 'Sesja wygasła, zaloguj się ponownie.'})

        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/?logout=true")


@login_required
def project_list_view(request):
    user = request.user

    if user.user_role in ['administrator', 'dyrektor']:
        projects = Projects.objects.all()

        filter_time = request.GET.get('filter_time', '')
        filter_priority = request.GET.get('filter_priority', '')
        search_term = request.GET.get('search_term', '')

        if filter_time == "half_year":
            six_months_ago = datetime.now() - timedelta(days=180)
            projects = projects.filter(start_date__gte=six_months_ago)
        elif filter_time == "year":
            one_year_ago = datetime.now() - timedelta(days=365)
            projects = projects.filter(start_date__gte=one_year_ago)
        elif filter_time == "archival":
            projects = projects.filter(is_completed=True)

        if filter_priority:
            projects = projects.filter(priority=filter_priority)

        if search_term:
            projects = projects.filter(
                Q(project_name__icontains=search_term) |
                Q(description__icontains=search_term)
            )

        add_project_form = AddProjectForm()
        return render(request, 'Director/projects_list.html',
                      {'projects': projects, 'add_project_form': add_project_form})

    else:
        return render(request, 'access_denied.html')

@login_required
def add_project_view(request):
    if request.method == 'POST':
        form = AddProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('project_list'))
        return redirect(reverse('project_list'))

@login_required
def delete_project_view(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        try:
            project = Projects.objects.get(project_id=project_id)
            project.delete()
            return JsonResponse({'success': True})
        except Projects.DoesNotExist:
            return JsonResponse({'success': False})
@login_required
def project_detail_view(request, project_id):
    user = request.user
    if user.user_role in ['administrator', 'dyrektor']:
        project = get_object_or_404(Projects, project_id=project_id)
        files = ProjectFiles.objects.filter(project_id=project)
        investors = Investors.objects.filter(project_id=project)
        project_members = ProjectMembers.objects.filter(project=project)
        add_member_form = AddProjectMemberForm(initial={'project': project})
        add_comment_form = AddProjectCommentForm()
        project_comments = ProjectComments.objects.filter(project=project).order_by('-comment_date')
        if request.method == "POST":

            if 'upload_files' in request.FILES and 'replace_file_id' not in request.POST:
                for upload_file in request.FILES.getlist('upload_files'):
                    mimetype = custom_guess_type(upload_file.name)
                    if mimetype is None:
                        return HttpResponse("Nierozpoznano pliku: " + upload_file.name, status=400)

                    file_type = get_or_create_file_type(mimetype)
                    file_extension = get_or_create_file_extension(upload_file.name)

                    project_file = ProjectFiles(project=project, file=upload_file, name=upload_file.name,
                                                description="Opis", file_type=file_type, extension=file_extension)
                    project_file.save()

            if 'delete_file_id' in request.POST:
                file_id = request.POST.get('delete_file_id')
                try:
                    file_to_delete = ProjectFiles.objects.get(id=file_id)
                    file_to_delete.file.delete()
                    file_to_delete.delete()
                except ProjectFiles.DoesNotExist:
                    pass  # Or return some error

            if 'replace_file_id' in request.POST and 'new_file' in request.FILES:
                file_id = request.POST.get('replace_file_id')
                new_file = request.FILES.get('new_file')
                mimetype = custom_guess_type(new_file.name)
                if mimetype is None:
                    return HttpResponse("Nierozpoznano pliku: " + new_file.name, status=400)

                try:
                    file_type = get_or_create_file_type(mimetype)
                    file_extension = get_or_create_file_extension(new_file.name)

                    file_to_replace = ProjectFiles.objects.get(id=file_id)
                    project_file = ProjectFiles(project=project, file=new_file, name=new_file.name,
                                                description=file_to_replace.description, file_type=file_type,
                                                extension=file_extension)

                    file_to_replace.file.delete()
                    file_to_replace.delete()
                    project_file.save()
                except ProjectFiles.DoesNotExist:
                    pass  # Lub zwróć jakiś błąd

            if 'add_comment' in request.POST:
                add_comment_form = AddProjectCommentForm(request.POST)
                if add_comment_form.is_valid():
                    new_comment = add_comment_form.save(commit=False)
                    new_comment.user = user
                    new_comment.project = project
                    new_comment.save()

            if 'remove_member_id' in request.POST:
                print("usuwam")
                member_id = request.POST.get('remove_member_id')
                ProjectMembers.objects.get(id=member_id).delete()
                return redirect(f'/director/projects/{project_id}/')

            elif 'project' in request.POST:
                print("Dzialamprojekt")
                add_member_form = AddProjectMemberForm(request.POST, initial={'project': project})
                if add_member_form.is_valid():
                    print("DzialamValid")
                    new_member = add_member_form.save(commit=False)  # Nie zapisujemy od razu
                    new_member.project = project  # Dodajemy brakujące pole
                    new_member.save()  # Teraz zapisujemy
                    return redirect(f'/director/projects/{project_id}/')
                else:
                    print("Form is invalid:", add_member_form.errors)
        add_investor_form = AddInvestorForm()
        context = {
            'project': project,
            'files': files,
            'investors': investors,
            'project_members': project_members,
            'add_member_form': add_member_form,
            'add_comment_form': add_comment_form,
            'project_comments': project_comments,
            'add_investor_form': add_investor_form
        }

        return render(request, 'Director/project_detail.html', context)

    else:
        return render(request, 'access_denied.html')

@login_required
def add_investor_view(request, project_id):
    if request.method == 'POST':
        form = AddInvestorForm(request.POST)
        if form.is_valid():
            new_investor = form.save(commit=False)
            new_investor.project_id = Projects.objects.get(project_id=project_id)
            new_investor.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = AddInvestorForm()
    return render(request, 'add_investor.html', {'form': form})
@login_required
def employee_panel(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_panel')
    else:
        form = EmployeeForm()

    employees = Users.objects.all()
    for employee in employees:
        employee.avatar_url = employee.avatar.url if employee.avatar else '/static/media/users/avatar.png'

    context = {
        'employees': employees,
        'form': form,
    }

    return render(request, 'Director/employees_panel.html', context)


@login_required
def employee_detail_view(request, user_id):
    employee = get_object_or_404(Users, user_id=user_id)
    project_members = ProjectMembers.objects.filter(user=employee)
    projects = [pm.project for pm in project_members]
    all_projects = Projects.objects.all()  # Dodajemy wszystkie dostępne projekty
    employee.avatar_url = employee.avatar.url if employee.avatar else '/static/media/users/avatar.png'
    roles = Users.ROLE_CHOICES  # Dodajemy dostępne role do kontekstu
    return render(request, 'Director/employee_detail.html', {
        'employee': employee,
        'projects': projects,
        'all_projects': all_projects,  # Dodane
        'roles': roles
    })



@login_required
def delete_employee_view(request, user_id):
    employee = get_object_or_404(Users, user_id=user_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, f'Pracownik {employee.username} został usunięty.')
        return HttpResponseRedirect(reverse('employee_panel'))  # Zaktualizowana nazwa widoku
    else:
        return HttpResponseRedirect(reverse('employee_detail', args=[user_id]))


@login_required
def change_role_view(request, user_id):
    employee = get_object_or_404(Users, user_id=user_id)
    if request.method == 'POST':
        new_role = request.POST.get('new_role')
        if new_role in dict(Users.ROLE_CHOICES):  # Sprawdzamy, czy nowa rola jest ważna
            employee.user_role = new_role
            employee.save()
            messages.success(request, f'Rola pracownika {employee.username} została zmieniona.')
    return HttpResponseRedirect(reverse('employee_detail', args=[user_id]))  # Wrócimy do strony pracownika


@login_required
def add_to_project_view(request, user_id):
    if request.method == "POST":
        project_id = request.POST.get('project_id')
        user = get_object_or_404(Users, user_id=user_id)
        project = get_object_or_404(Projects, project_id=project_id)
        ProjectMembers.objects.create(user=user, project=project)
        return redirect('employee_detail', user_id=user_id)


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            # Zapisz wiadomość w bazie danych
            sender = request.user
            recipient = form.cleaned_data['recipient']
            project = form.cleaned_data['project']
            message_text = form.cleaned_data['message']

            new_message = Messages(
                sender_id=sender,
                receiver_id=recipient,
                project_id=project,
                message_text=message_text,
                send_date=timezone.now(),
                is_read=False
            )
            print('wyslalem')
            new_message.save()

            # Zapisz załączniki w bazie danych
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                # Ustal rozszerzenie pliku
                file_name = attachment.name
                file_extension = file_name.split('.')[-1] if '.' in file_name else 'unknown'

                # Ustal typ MIME pliku
                file_mime_type = attachment.content_type

                # Ustal lub stwórz typ i rozszerzenie pliku w bazie danych
                file_type, created = FileTypes.objects.get_or_create(
                    file_type=file_mime_type,
                    defaults={'file_type': file_mime_type}  # Domyślne wartości dla nowego obiektu
                )

                extension, created = FileExtensions.objects.get_or_create(
                    extension=file_extension,
                    defaults={'extension': file_extension}  # Domyślne wartości dla nowego obiektu
                )
                new_file = Files(
                    file_name=attachment.name,
                    upload_date=timezone.now(),
                    user_id=sender,
                    file_type_id=file_type,
                    extension_id=extension
                )
                new_file.save()

                new_attachment = MessageAttachments(
                    message_id=new_message,
                    file_id=new_file
                )
                new_attachment.save()

            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})



@login_required
def get_files_for_project(request, project_id):
    print(project_id)
    files = ProjectFiles.objects.filter(project_id=project_id)
    print(files)
    files_list = [{'id': file.id, 'name': file.name} for file in files]
    print(files_list)
    return JsonResponse(files_list, safe=False)



@login_required
def file_viewer(request):
    selected_project_id = request.GET.get('project')
    selected_file_id = request.GET.get('file')
    print(request.GET.get('project'))
    projects = Projects.objects.all()
    if selected_file_id:
        if selected_project_id:
            files = ProjectFiles.objects.filter(project_id=selected_project_id)
        else:
            files = ProjectFiles.objects.filter(project_id=1)
        selected_file = get_object_or_404(ProjectFiles, id=selected_file_id)
        file_type = selected_file.file_type.file_type  # uzyskaj właściwy typ pliku
    else:
        files = []
        selected_file = None
        file_type = None
    if selected_file_id:
        selected_file = get_object_or_404(ProjectFiles, id=selected_file_id)
    else:
        selected_file = None

    current_url = request.get_full_path().split('?')[0]  # bierze bieżący URL bez parametrów
    image_types = ['image/jpg', 'image/jpeg', 'image/png', 'image/gif']

    return render(request, 'file_viewer.html', {
        'projects': projects,
        'files': files,
        'selected_file': selected_file,
        'file_type': file_type,
        'current_url': current_url,
        'image_types': image_types  # Dodaj to
    })



@login_required
def statistics_view(request):
    if request.method == "GET":
        ongoing_projects = Projects.objects.filter(is_completed=False).annotate(month=TruncMonth('start_date')).values(
            'month').annotate(count=Count('project_id')).order_by('month')
        user_projects = Projects.objects.filter(is_completed=False).values('projectmembers__user_id').annotate(
            count=Count('project_id'),
            username=F('projectmembers__user__username')
        ).order_by('projectmembers__user_id')
        project_files = ProjectFiles.objects.values('project__project_name').annotate(
            count=Count('file'),
            project_name=F('project__project_name')  # Include project_name in the output
        ).order_by('project__project_name')
        completed_projects_time = Projects.objects.filter(is_completed=True).annotate(
            time=F('end_date') - F('start_date'))
        investor_projects = Investors.objects.values('investor_name').annotate(count=Count('project_id')).order_by(
            'investor_name')
        print(json.dumps(list(user_projects.values()), cls=ExtendedEncoder))
        context = {
            'ongoing_projects': json.dumps(list(ongoing_projects.values()), cls=ExtendedEncoder),
            'user_projects': json.dumps(list(user_projects.values()), cls=ExtendedEncoder),
            'project_files': json.dumps(list(project_files.values()), cls=ExtendedEncoder),
            'completed_projects_time': json.dumps(list(completed_projects_time.values()), cls=ExtendedEncoder),
            'investor_projects': json.dumps(list(investor_projects.values()), cls=ExtendedEncoder),
        }
        if 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
            return JsonResponse(context)
        else:
            return render(request, 'Director/statistics.html')
