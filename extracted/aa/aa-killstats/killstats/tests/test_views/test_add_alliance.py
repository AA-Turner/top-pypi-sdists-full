# Standard Library
from http import HTTPStatus
from unittest.mock import Mock, patch

# Django
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
)

# AA Killstats
from killstats.models.killstatsaudit import AlliancesAudit
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import create_user_from_evecharacter
from killstats.views import (
    add_alliance,
)

MODULE_PATH = "killstats.views"


@patch(MODULE_PATH + ".messages")
@patch(MODULE_PATH + ".provider.get_alliance")
@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class KillstatsAllianceAuditTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()

        cls.factory = RequestFactory()
        cls.user, cls.character_ownership = create_user_from_evecharacter(
            1001,
            permissions=[
                "killstats.basic_access",
                "killstats.admin_access",
            ],
        )

    def _add_alliance(self, user, token):
        request = self.factory.get(reverse("killstats:add_alliance"))
        request.user = user
        request.token = token
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        orig_view = add_alliance.__wrapped__.__wrapped__.__wrapped__
        return orig_view(request, token)

    @patch(MODULE_PATH + ".EveAllianceInfo.objects.get_or_create")
    def test_add_ally(self, mock_alliance, mock_provider, mock_messages):
        # given
        user = self.user
        token = user.token_set.get(character_id=1001)

        alliance = EveAllianceInfo.objects.create(
            alliance_id=9999,
            alliance_name="Test Alliance",
            alliance_ticker="TEST",
            executor_corp_id=2001,
        )
        mock_alliance.return_value = (alliance, True)
        mock_provider.return_value = Mock()

        # when
        response = self._add_alliance(user, token)

        # then
        alliance_audit = AlliancesAudit.objects.get(alliance__alliance_id=9999)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("killstats:alliance", args=[9999]))
        self.assertEqual(mock_messages.info.call_count, 1)
        self.assertEqual(alliance_audit.alliance.alliance_id, 9999)
