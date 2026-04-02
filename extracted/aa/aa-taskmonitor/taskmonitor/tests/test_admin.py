from django.contrib.admin.sites import AdminSite

from app_utils.testing import NoSocketsTestCase

from taskmonitor import admin
from taskmonitor.models import TaskLog

from .factories import TaskLogFactory


class TestTaskLogAdmin(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.modeladmin = admin.TaskLogAdmin(model=TaskLog, admin_site=AdminSite())

    def test_should_format_runtime(self):
        # given
        log = TaskLogFactory()
        log.runtime = 0.2
        # when/then
        self.assertEqual(self.modeladmin._runtime(log), "0.2")

    def test_should_handle_no_runtime(self):
        # given
        log = TaskLogFactory()
        log.runtime = None
        # when/then
        self.assertIsNone(self.modeladmin._runtime(log))
