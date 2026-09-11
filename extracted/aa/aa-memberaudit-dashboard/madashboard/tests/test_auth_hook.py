# Third Party
from app_utils.testdata_factories import EveCharacterFactory
from app_utils.testing import create_user_from_evecharacter
from memberaudit.tests.utils import create_user_from_evecharacter_with_access

# Django
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

# AA Member Audit Dashboard
from madashboard.auth_hooks import MemberCheckDashboardHook, register_membercheck_hook


class TestAuthHooks(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.factory = RequestFactory()
        EveCharacterFactory(character_id=1001)
        EveCharacterFactory(character_id=1002)

        cls.user_without_permission, cls.character_ownership = (
            create_user_from_evecharacter(character_id=1002)
        )
        cls.user_with_ma_permission, cls.character_ownership = (
            create_user_from_evecharacter_with_access(character_id=1001)
        )

    def test_render_returns_empty_string_for_user_without_permission(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user_without_permission
        rendered_item = MemberCheckDashboardHook()

        # Test Action
        response = rendered_item.render(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # Expected Result
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_render_returns_widget_for_user_with_permission(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user_with_ma_permission
        rendered_item = MemberCheckDashboardHook()

        # Test Action
        response = rendered_item.render(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # Expected Result
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_register_membercheck_hook(self):
        # Test Data
        hooks = register_membercheck_hook()
        # Expected Result
        self.assertIsInstance(hooks, MemberCheckDashboardHook)
