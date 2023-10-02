from django.urls import path
from . import views
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('director/projects/', views.project_list_view, name='project_list'),
    path('director/add_project/', views.add_project_view, name='add_project'),
    path('director/delete_project/', views.delete_project_view, name='delete_project'),
    path('director/add_investor/<int:project_id>/', views.add_investor_view, name='add_investor'),
    path('director/projects/<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('director/employees/', views.employee_panel, name='employee_panel'),
    path('director/employees/<int:user_id>/', views.employee_detail_view, name='employee_detail'),
    path('delete_employee/<int:user_id>/', views.delete_employee_view, name='delete_employee'),
    path('change_role/<int:user_id>/', views.change_role_view, name='change_role'),
    path('add_to_project/<int:user_id>/', views.add_to_project_view, name='add_to_project'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_files_for_project/<int:project_id>/', views.get_files_for_project, name='get_files_for_project'),
    path('file_viewer/', views.file_viewer, name='file_viewer'),
    path('director/statistics/', views.statistics_view, name='statistics'),
    # Dodaj inne URL-y tutaj
]
