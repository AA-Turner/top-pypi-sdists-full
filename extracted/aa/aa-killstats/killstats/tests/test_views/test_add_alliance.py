# Standard Library
from http import HTTPStatus
from unittest.mock import Mock, patch

# Third Party
from evesde_factory.allianceauth import (
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
)

# Django
from django.test import override_settings
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
)

# AA Killstats
from killstats.models.killstatsaudit import AlliancesAudit
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import UserMainFactory
from killstats.views import (
    add_alliance,
)

MODULE_PATH = "killstats.views"


@patch(MODULE_PATH + ".messages")
@override_settings(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class KillstatsAllianceAuditTest(AuthTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def _add_alliance(self, user, token):
        request = self.factory.get(reverse("killstats:add_alliance"))
        request.user = user
        request.token = token
        self._middleware_process_request(request)
        orig_view = add_alliance.__wrapped__.__wrapped__.__wrapped__
        return orig_view(request, token)

    def test_add_alliance(self, mock_messages):
        # Test Data
        user = UserMainFactory(
            permissions__=["killstats.admin_access"],
            main_character__character=EveCharacterFactory(
                corporation=EveCorporationInfoFactory(),
            ),
        )
        token = user.token_set.first()
        char = user.profile.main_character
        alliance, _ = EveAllianceInfo.objects.get_or_create(
            alliance_id=char.alliance_id,
            defaults={
                "alliance_name": char.alliance_name,
                "alliance_ticker": char.alliance_ticker,
                "executor_corp_id": char.corporation_id,
            },
        )

        # Test Action
        response = self._add_alliance(user, token)

        # Expected Result
        alliance_audit = AlliancesAudit.objects.get(alliance=alliance)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            response.url,
            reverse("killstats:alliance", kwargs={"entity_id": char.alliance_id}),
        )
        self.assertEqual(mock_messages.info.call_count, 1)
        self.assertEqual(alliance_audit.alliance.alliance_id, char.alliance_id)

    def test_add_alliance_not_found_in_auth(self, mock_messages):
        # Test Data
        user = UserMainFactory(
            permissions__=["killstats.admin_access"],
            main_character__character=EveCharacterFactory(
                corporation=EveCorporationInfoFactory(create_alliance=False),
                alliance_id=99000999,  # Valid player alliance ID not present in DB
                alliance_name="Ghost Alliance",
            ),
        )
        token = user.token_set.first()
        char = user.profile.main_character

        # Test Action
        response = self._add_alliance(user, token)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("killstats:react_base"))
        self.assertEqual(mock_messages.warning.call_count, 1)
        self.assertFalse(
            AlliancesAudit.objects.filter(
                alliance__alliance_id=user.profile.main_character.alliance_id
            ).exists(),
            AlliancesAudit.objects.filter(
                alliance__alliance_id=char.alliance_id
            ).exists(),
        )
        self.assertEqual(mock_messages.warning.call_count, 1)

    def test_add_alliance_npc_corporation_rejected(self, mock_messages):
        # Test Data
        user = UserMainFactory(
            permissions__=["killstats.admin_access"],
            main_character__character=EveCharacterFactory(
                corporation=EveCorporationInfoFactory(
                    corporation_id=1000125,  # NPC Corp
                    create_alliance=False,
                ),
                alliance_id=99000001,
            ),
        )
        token = user.token_set.first()

        # Test Action
        response = self._add_alliance(user, token)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("killstats:react_base"))
        self.assertEqual(mock_messages.error.call_count, 1)
        self.assertFalse(
            AlliancesAudit.objects.filter(
                alliance__alliance_id=user.profile.main_character.alliance_id
            ).exists(),
            AlliancesAudit.objects.filter(alliance__alliance_id=99000001).exists(),
        )

    def test_add_alliance_no_alliance_rejected(self, mock_messages):
        # Test Data
        user = UserMainFactory(
            permissions__=["killstats.admin_access"],
            main_character__character=EveCharacterFactory(
                corporation=EveCorporationInfoFactory(
                    create_alliance=False,  # No alliance for this corporation
                ),
            ),
        )
        token = user.token_set.first()

        # Test Action
        response = self._add_alliance(user, token)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("killstats:react_base"))
        self.assertEqual(mock_messages.error.call_count, 1)
        self.assertFalse(
            AlliancesAudit.objects.filter(alliance__alliance_id=99000001).exists()
        )

    def test_add_alliance_npc_executor_rejected(self, mock_messages):
        # Test Data
        user = UserMainFactory(
            permissions__=["killstats.admin_access"],
            main_character__character=EveCharacterFactory(
                corporation=EveCorporationInfoFactory(
                    alliance=EveAllianceInfoFactory(
                        alliance_id=1_000_000,  # NPC Alliance (< 10_000_000)
                    ),
                ),
            ),
        )
        token = user.token_set.first()

        # Test Action
        response = self._add_alliance(user, token)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("killstats:react_base"))
        self.assertEqual(mock_messages.error.call_count, 1)
        self.assertFalse(
            AlliancesAudit.objects.filter(alliance__alliance_id=1_000_000).exists()
        )
