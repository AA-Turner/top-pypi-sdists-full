"""Unit tests for KillboardAdminApiEndpoints."""

# Standard Library
from unittest.mock import patch

# Third Party
# EVE SDE & Alliance Auth Factories
from evesde_factory.allianceauth import (
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
)

# Django Ninja
from ninja.testing import TestClient

# AA Killstats
from killstats.api import api
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import (
    AlliancesAuditFactory,
    CorporationsAuditFactory,
    UserMainFactory,
)

MODULE_PATH = "killstats.api.admin"


class TestKillboardAdminApi(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(api)

    def test_get_corporation_admin_should_return_corporation_dict_when_authorized(
        self,
    ):
        # Test Data
        corp = EveCorporationInfoFactory()
        char = EveCharacterFactory(corporation=corp)
        user = UserMainFactory(main_character__character=char)
        CorporationsAuditFactory(corporation=corp, owner=char)

        # Test Action
        response = self.client.get("/killboard/corporation/admin/", user=user)

        # Expected Result
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("corporation", data[0])
        corp_str_id = str(corp.corporation_id)
        self.assertIn(corp_str_id, data[0]["corporation"])
        self.assertEqual(
            data[0]["corporation"][corp_str_id]["corporation_id"],
            corp.corporation_id,
        )

    def test_get_corporation_admin_should_return_403_when_corporations_is_none(self):
        # Test Data
        user = UserMainFactory()

        # Test Action
        with patch.object(CorporationsAudit.objects, "visible_to", return_value=None):
            response = self.client.get("/killboard/corporation/admin/", user=user)

        # Expected Result
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), "Permission Denied")

    def test_get_alliance_admin_should_return_alliance_dict_when_authorized(self):
        # Test Data
        alliance = EveAllianceInfoFactory()
        corp = EveCorporationInfoFactory(alliance=alliance)
        char = EveCharacterFactory(corporation=corp)
        user = UserMainFactory(main_character__character=char)
        AlliancesAuditFactory(alliance=alliance, owner=char)

        # Test Action
        response = self.client.get("/killboard/alliance/admin/", user=user)

        # Expected Result
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("alliance", data[0])
        alliance_str_id = str(alliance.alliance_id)
        self.assertIn(alliance_str_id, data[0]["alliance"])
        self.assertEqual(
            data[0]["alliance"][alliance_str_id]["alliance_id"],
            alliance.alliance_id,
        )

    def test_get_alliance_admin_should_return_403_when_alliances_is_none(self):
        # Test Data
        user = UserMainFactory()

        # Test Action
        with patch.object(AlliancesAudit.objects, "visible_to", return_value=None):
            response = self.client.get("/killboard/alliance/admin/", user=user)

        # Expected Result
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), "Permission Denied")
