from django.urls import path
from . import views

urlpatterns = [
    path('worker_project_list/', views.worker_project_list, name='worker_project_list'),
    path('worker/projects/<int:project_id>/', views.worker_project_detail_view, name='worker_project_detail'),
    path('worker/statistics/', views.worker_statistics, name='worker_statistics'),
    ]