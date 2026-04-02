# Standard Library
from unittest.mock import MagicMock

# Django
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

# Alliance Auth (External Libs)
from app_utils.testing import create_user_from_evecharacter

# AA Member Audit Dashboard
from madashboard.auth_hooks import MemberCheckDashboardHook, register_membercheck_hook
from madashboard.tests.testdata.load_allianceauth import load_allianceauth
from madashboard.tests.testdata.load_memberaudit import load_memberaudit


class TestAuthHooks(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()
        load_memberaudit()
        cls.factory = RequestFactory()
        cls.user_without_permission, cls.character_ownership = (
            create_user_from_evecharacter(character_id=1002)
        )
        cls.user_with_ma_permission, cls.character_ownership = (
            create_user_from_evecharacter(
                character_id=1001,
                permissions=["memberaudit.basic_access"],
            )
        )

    def test_render_returns_empty_string_for_user_without_permission(self):
        # given
        request = self.factory.get("/")
        request.user = self.user_without_permission
        rendered_item = MemberCheckDashboardHook()

        # when
        response = rendered_item.render(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_render_returns_widget_for_user_with_permission(self):
        # given
        request = self.factory.get("/")
        request.user = self.user_with_ma_permission
        rendered_item = MemberCheckDashboardHook()

        # when
        response = rendered_item.render(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_register_membercheck_hook(self):
        # given
        hooks = register_membercheck_hook()

        # then
        self.assertIsInstance(hooks, MemberCheckDashboardHook)
