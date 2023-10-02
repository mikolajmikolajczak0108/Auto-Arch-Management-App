from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from MainApp.models import ProjectMembers, Projects
from django.contrib.auth.decorators import login_required

from MainApp.forms import AddProjectCommentForm
from MainApp.models import ProjectFiles, Investors, ProjectComments,Files, Messages
from MainApp.utils import get_or_create_file_type, get_or_create_file_extension, custom_guess_type



@login_required
def worker_project_list(request):
    user = request.user
    project_members = ProjectMembers.objects.filter(user__username=user.username)
    projects = [member.project for member in project_members]
    return render(request, 'Worker/worker_project_list.html', {'projects': projects})


@login_required
def worker_project_detail_view(request, project_id):
    user = request.user
    project = get_object_or_404(Projects, project_id=project_id)
    files = ProjectFiles.objects.filter(project_id=project)
    investors = Investors.objects.filter(project_id=project)
    project_members = ProjectMembers.objects.filter(project=project)
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
                pass  # Or return some error

        if 'add_comment' in request.POST:
            add_comment_form = AddProjectCommentForm(request.POST)
            if add_comment_form.is_valid():
                new_comment = add_comment_form.save(commit=False)
                new_comment.user = user
                new_comment.project = project
                new_comment.save()

    context = {
        'project': project,
        'files': files,
        'investors': investors,
        'project_members': project_members,
        'add_comment_form': add_comment_form,
        'project_comments': project_comments,
    }

    return render(request, 'Worker/worker_project_details.html', context)

@login_required
def worker_statistics(request):
    current_user = request.user
    project_count = Projects.objects.filter(projectmembers__user=current_user).count()
    comment_count = ProjectComments.objects.filter(user=current_user).count()
    file_count = Files.objects.filter(user_id=current_user).count()
    message_count = Messages.objects.filter(sender_id=current_user).count()

    projects_by_date = Projects.objects.filter(projectmembers__user=current_user).order_by('-start_date')
    projects_by_month = Projects.objects.filter(projectmembers__user=current_user).annotate(month=TruncMonth('start_date')).values('month').annotate(c=Count('project_id')).values('month', 'c')

    context = {
        'project_count': project_count,
        'comment_count': comment_count,
        'file_count': file_count,
        'message_count': message_count,
        'projects_by_date': projects_by_date,
        'projects_by_month': list(projects_by_month),
        'current_user': current_user,
    }

    return render(request, 'worker/worker_statistics.html', context)
