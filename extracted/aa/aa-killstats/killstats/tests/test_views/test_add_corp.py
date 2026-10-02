# Standard Library
from http import HTTPStatus
from unittest.mock import Mock, patch

# Django
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

# AA Killstats
from killstats.models.killstatsaudit import CorporationsAudit
from killstats.tests import AuthTestCase
from killstats.views import (
    add_corp,
)

MODULE_PATH = "killstats.views"


@patch(MODULE_PATH + ".messages")
class KillstatsAuditTest(AuthTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def _add_corporation(self, user, token):
        request = self.factory.get(reverse("killstats:add_corp"))
        request.user = user
        request.token = token
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        orig_view = add_corp.__wrapped__.__wrapped__.__wrapped__
        return orig_view(request, token)

    def test_add_corp_success(self, mock_messages):
        # Test Data
        user = self.user
        token = self.user.token_set.first()

        # Test Action
        response = self._add_corporation(user, token)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            response.url,
            reverse("killstats:corporation", kwargs={"entity_id": 98000001}),
        )
        self.assertEqual(mock_messages.info.call_count, 1)
        self.assertTrue(
            CorporationsAudit.objects.filter(
                corporation__corporation_id=98000001
            ).exists()
        )

    def test_add_corp_npc_corporation_rejected(self, mock_messages):
        # Test Data
        user = self.user
        token = self.user.token_set.first()
        self.user.profile.main_character.corporation_id = (
            1000125  # NPC Corporation (CONCORD)
        )
        self.user.profile.main_character.save()
        # Test Action
        response = self._add_corporation(user, token)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("killstats:react_base"))
        self.assertEqual(mock_messages.error.call_count, 1)
        self.assertFalse(
            CorporationsAudit.objects.filter(
                corporation__corporation_id=1000125
            ).exists()
        )
