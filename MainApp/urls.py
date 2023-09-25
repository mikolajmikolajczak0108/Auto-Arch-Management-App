from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('director/projects/', views.project_list_view, name='project_list'),
    path('director/projects/<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('director/employees/', views.employee_panel, name='employee_panel'),
    path('director/employees/<int:user_id>/', views.employee_detail_view, name='employee_detail'),
    path('delete_employee/<int:user_id>/', views.delete_employee_view, name='delete_employee'),
    path('change_role/<int:user_id>/', views.change_role_view, name='change_role'),
    path('add_to_project/<int:user_id>/', views.add_to_project_view, name='add_to_project'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_files_for_project/<int:project_id>/', views.get_files_for_project, name='get_files_for_project'),
    path('file_viewer/', views.file_viewer, name='file_viewer'),

    # Dodaj inne URL-y tutaj
]
