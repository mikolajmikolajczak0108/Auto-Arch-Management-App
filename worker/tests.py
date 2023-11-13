from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from MainApp.models import Projects, Users, ProjectFiles, ProjectMembers, ProjectComments
from datetime import datetime

class WorkerAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username="testworker", password="testpass")

    def test_worker_project_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('worker_project_list'))
        self.assertEqual(response.status_code, 200)

    def test_worker_project_detail_view(self):
        project = Projects.objects.create(project_name="Test Project Worker", start_date=datetime.now())
        ProjectMembers.objects.create(user=self.user, project=project)
        self.client.force_login(self.user)
        response = self.client.get(reverse('worker_project_detail_view', kwargs={'project_id': project.id}))
        self.assertEqual(response.status_code, 200)

    def test_worker_statistics(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('worker_statistics'))
        self.assertEqual(response.status_code, 200)