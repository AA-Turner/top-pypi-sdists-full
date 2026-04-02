from django.test import TestCase

from app_utils.testdata_factories import UserFactory

from taskmonitor.core import cached_reports, celery_queues
from taskmonitor.models import TaskStatistic
from taskmonitor.tests.factories import TaskLogFactory


class TestUI(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = UserFactory(is_staff=True, is_superuser=True)
        cls.log_1 = TaskLogFactory()
        cls.log_2 = TaskLogFactory()

    # FIXME
    # def test_should_show_reports_page(self):
    #     # given
    #     cached_reports.clear_cache()
    #     self.client.force_login(self.user)
    #     # when
    #     response = self.client.get("/taskmonitor/admin_taskmonitor_reports")
    #     # then
    #     self.assertEqual(response.status_code, 200)

    def test_should_show_tasklogs_changelist_page(self):
        # given
        cached_reports.clear_cache()
        self.client.force_login(self.user)
        # when
        response = self.client.get("/admin/taskmonitor/tasklog/")
        # then
        self.assertEqual(response.status_code, 200)

    def test_should_show_tasklogs_change_page(self):
        # given
        cached_reports.clear_cache()
        self.client.force_login(self.user)
        # when
        response = self.client.get(
            f"/admin/taskmonitor/tasklog/{self.log_1.id}/change/"
        )
        # then
        self.assertEqual(response.status_code, 200)

    def test_should_show_queuedtasks_page(self):
        # given
        celery_queues.tasks_cache.clear()
        self.client.force_login(self.user)
        # when
        response = self.client.get("/admin/taskmonitor/queuedtask/")
        # then
        self.assertEqual(response.status_code, 200)

    def test_should_show_statistics_page(self):
        # given
        TaskStatistic.objects.clear_cache()
        self.client.force_login(self.user)
        # when
        response = self.client.get("/admin/taskmonitor/taskstatistic/")
        # then
        self.assertEqual(response.status_code, 200)
