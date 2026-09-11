# Third Party
from app_utils.testdata_factories import EveCharacterFactory
from app_utils.testing import (
    NoSocketsTestCase,
    add_character_to_user,
    create_user_from_evecharacter,
)
from memberaudit.models import CharacterUpdateStatus
from memberaudit.tests.testdata.factories_2 import CharacterFactory
from memberaudit.tests.utils import create_user_from_evecharacter_with_access

# Django
from django.http import HttpResponse
from django.test import RequestFactory

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# AA Member Audit Dashboard
from madashboard.views import dashboard_memberaudit_check


class DashboardMemberAuditCheckTest(NoSocketsTestCase):
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

    def test_dashboard_memberaudit_check_user_with_ma_premission(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user_with_ma_permission
        # Test Action
        response = dashboard_memberaudit_check(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # Expected Result
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_dashboard_memberaudit_check_user_without_permission(self):
        # Test Data
        request = self.factory.get("/")
        request.user = self.user_without_permission
        # Test Action
        response = dashboard_memberaudit_check(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # Expected Result
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_dashboard_memberaudit_check_many(self):
        # Test Data
        CharacterFactory(user=self.user_with_ma_permission)
        CharacterFactory(user=self.user_with_ma_permission, is_main=False)

        request = self.factory.get("/")
        request.user = self.user_with_ma_permission
        # Test Action
        response = dashboard_memberaudit_check(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # Expected Result
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_dashboard_memberaudit_check_character_update_issues(self):
        # Test Data
        # Create a CharacterUpdateStatus with failed update for character 1001
        memberaudit = CharacterFactory(user=self.user_with_ma_permission)
        CharacterUpdateStatus.objects.create(
            character=memberaudit, is_success=False, update_finished_at=None
        )

        request = self.factory.get("/")
        request.user = self.user_with_ma_permission
        # Test Action
        response = dashboard_memberaudit_check(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # Expected Result
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )
        # Check that the character update issue icon is present
        self.assertIn(
            "<i class='fas fa-triangle-exclamation'",
            response.content.decode("utf-8"),
        )
        # Check that the issue message is present
        self.assertIn(
            "Please re-register this character, as there was an issue with the last update.",
            response.content.decode("utf-8"),
        )

    def test_dashboard_memberaudit_check_character_both_unregistered_and_issues(self):
        # Test Data
        character = CharacterFactory(user=self.user_with_ma_permission)
        EveCharacterFactory(character_id=1006)
        # Add an unregistered character (character without memberaudit record)
        add_character_to_user(
            self.user_with_ma_permission, EveCharacter.objects.get(character_id=1006)
        )
        # Create a CharacterUpdateStatus with failed update for the registered character 1001
        CharacterUpdateStatus.objects.create(
            character=character, is_success=False, update_finished_at=None
        )

        request = self.factory.get("/")
        request.user = self.user_with_ma_permission
        # Test Action
        response = dashboard_memberaudit_check(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # Expected Result
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<div id="memberaudit-check-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )
        # Check that both icons are present (registration issue and update issue)
        self.assertIn(
            "<i class='fas fa-times-circle'",
            response.content.decode("utf-8"),
        )
        self.assertIn(
            "<i class='fas fa-triangle-exclamation'",
            response.content.decode("utf-8"),
        )
