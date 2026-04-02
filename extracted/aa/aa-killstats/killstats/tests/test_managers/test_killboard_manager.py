# Standard Library
from unittest.mock import patch

# Django
from django.test import RequestFactory

# Alliance Auth (External Libs)
from eve_sde.models.types import ItemType

# AA Killstats
from killstats.helpers.killmail import (
    KillmailAttacker,
    KillmailBody,
    KillmailPosition,
    KillmailVictim,
    KillmailZkb,
)
from killstats.models.general import EveEntity
from killstats.models.killboard import Killmail
from killstats.tests import NoSocketsTestCase
from killstats.tests.testdata.esi_stub_openapi import (
    EsiEndpoint,
    create_esi_client_stub,
)
from killstats.tests.testdata.eveentity import load_eveentity
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import (
    create_killmail,
    create_user_from_evecharacter,
)

MODULE_PATH = "killstats.managers.general_manager"

KILLSTATS_EVE_ENTITY_ENDPOINTS = [
    EsiEndpoint("Universe", "PostUniverseNames", "ids"),
]


class KillstatsManagerTest(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()
        load_eveentity()
        cls.factory = RequestFactory()

        cls.killmail = create_killmail(
            killmail_id=1,
            killmail_date="2025-10-01T00:00:00Z",
            victim_corporation_id=2001,
            victim_alliance_id=3001,
            victim_region_id=1001,
            victim_solar_system_id=2001,
            victim_position_x=1.0,
            victim_position_y=1.0,
            victim_position_z=1.0,
            victim=EveEntity.objects.get(id=1001),
            victim_ship=ItemType.objects.get(id=670),
            victim_total_value=1000,
            victim_fitted_value=500,
            victim_destroyed_value=500,
            victim_dropped_value=500,
        )

    def test_visible_to_superuser(self):
        # given
        self.user, self.character_ownership = create_user_from_evecharacter(
            1001,
        )
        self.user.is_superuser = True
        self.user.save()
        # when
        result = Killmail.objects.visible_to(self.user)
        expected_result = Killmail.objects.all()
        # then
        self.assertEqual(list(result), list(expected_result))

    def test_visible_to_admin_access(self):
        # given
        self.user, self.character_ownership = create_user_from_evecharacter(
            1001,
            permissions=[
                "killstats.admin_access",
            ],
        )
        # when
        expected_result = Killmail.objects.all()
        result = Killmail.objects.visible_to(self.user)
        # then
        self.assertEqual(list(result), list(expected_result))

    def test_visible_to_no_access(self):
        # given
        self.user, self.character_ownership = create_user_from_evecharacter(
            1001,
        )
        # when
        expected_result = []
        result = Killmail.objects.visible_to(self.user)
        # then
        self.assertEqual(list(result), list(expected_result))

    def test_filter_structure_exclude_false(self):
        queryset = Killmail.objects.filter_structure(exclude=False)
        expected_count = Killmail.objects.filter(
            victim_ship__group__category_id=65
        ).count()
        self.assertEqual(queryset.count(), expected_count)

    def test_filter_structure_exclude_true(self):
        queryset = Killmail.objects.filter_structure(exclude=True)
        expected_count = Killmail.objects.exclude(
            victim_ship__group__category_id=65
        ).count()
        self.assertEqual(queryset.count(), expected_count)

    @patch(MODULE_PATH + ".esi")
    def test_create_killmail_from_killmail_body(self, mock_esi):
        # given
        killmail_body = KillmailBody(
            id=2,
            time="2025-10-01T00:00:00Z",
            victim=KillmailVictim(
                character_id=1001,
                corporation_id=2001,
                alliance_id=3001,
                ship_type_id=670,
            ),
            attackers=[
                KillmailAttacker(
                    character_id=1002,
                    corporation_id=2002,
                    alliance_id=3002,
                )
            ],
            zkb=KillmailZkb(
                hash="create_killmail",
                fitted_value=1000,
                destroyed_value=500,
                dropped_value=500,
                total_value=1000,
            ),
            solar_system_id=30004783,
            position=KillmailPosition(
                x=1.0,
                y=1.0,
                z=1.0,
            ),
        )
        # when
        created_killmail = Killmail.objects.create_from_killmail(
            killmail_body=killmail_body
        )
        # then
        self.assertEqual(created_killmail.killmail_id, 2)
        self.assertEqual(created_killmail.victim_total_value, 1000)
