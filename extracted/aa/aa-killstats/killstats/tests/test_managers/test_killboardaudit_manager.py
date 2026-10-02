"""Unit tests for CorporationsAuditManager and AlliancesAuditManager."""

# Third Party
from evesde_factory.allianceauth import (
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
    UserFactory,
)

# AA Killstats
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import (
    AlliancesAuditFactory,
    CorporationsAuditFactory,
    UserMainFactory,
)


class TestCorporationsAuditManager(AuthTestCase):
    def test_visible_to_should_return_all_corps_for_superuser(self):
        # Test Data
        audit1 = CorporationsAuditFactory()
        audit2 = CorporationsAuditFactory()

        # Test Action
        result = CorporationsAudit.objects.visible_to(self.superuser)

        # Expected Result
        self.assertIn(audit1, result)
        self.assertIn(audit2, result)

    def test_visible_to_should_return_all_corps_for_admin_access(self):
        # Test Data
        admin_user = UserMainFactory(permissions__=["killstats.admin_access"])
        audit1 = CorporationsAuditFactory()
        audit2 = CorporationsAuditFactory()

        # Test Action
        result = CorporationsAudit.objects.visible_to(admin_user)

        # Expected Result
        self.assertIn(audit1, result)
        self.assertIn(audit2, result)

    def test_visible_to_should_return_only_own_corporation_for_normal_user(self):
        # Test Data
        corp1 = EveCorporationInfoFactory()
        corp2 = EveCorporationInfoFactory()
        user = UserMainFactory(
            main_character__character=EveCharacterFactory(corporation=corp1)
        )
        audit1 = CorporationsAuditFactory(corporation=corp1)
        audit2 = CorporationsAuditFactory(corporation=corp2)

        # Test Action
        result = CorporationsAudit.objects.visible_to(user)

        # Expected Result
        self.assertIn(audit1, result)
        self.assertNotIn(audit2, result)

    def test_visible_to_should_return_none_when_user_has_no_main_character(self):
        # Test Data
        user_without_main = UserFactory()
        CorporationsAuditFactory()

        # Test Action
        result = CorporationsAudit.objects.visible_to(user_without_main)

        # Expected Result
        self.assertFalse(result.exists())


class TestAlliancesAuditManager(AuthTestCase):
    def test_visible_to_should_return_all_alliances_for_superuser(self):
        # Test Data
        audit1 = AlliancesAuditFactory()
        audit2 = AlliancesAuditFactory()

        # Test Action
        result = AlliancesAudit.objects.visible_to(self.superuser)

        # Expected Result
        self.assertIn(audit1, result)
        self.assertIn(audit2, result)

    def test_visible_to_should_return_all_alliances_for_admin_access(self):
        # Test Data
        admin_user = UserMainFactory(permissions__=["killstats.admin_access"])
        audit1 = AlliancesAuditFactory()
        audit2 = AlliancesAuditFactory()

        # Test Action
        result = AlliancesAudit.objects.visible_to(admin_user)

        # Expected Result
        self.assertIn(audit1, result)
        self.assertIn(audit2, result)

    def test_visible_to_should_return_only_own_alliance_for_normal_user(self):
        # Test Data
        alliance1 = EveAllianceInfoFactory()
        alliance2 = EveAllianceInfoFactory()
        corp1 = EveCorporationInfoFactory(alliance=alliance1)
        user = UserMainFactory(
            main_character__character=EveCharacterFactory(corporation=corp1)
        )
        audit1 = AlliancesAuditFactory(alliance=alliance1)
        audit2 = AlliancesAuditFactory(alliance=alliance2)

        # Test Action
        result = AlliancesAudit.objects.visible_to(user)

        # Expected Result
        self.assertIn(audit1, result)
        self.assertNotIn(audit2, result)

    def test_visible_to_should_return_none_when_user_has_no_main_character(self):
        # Test Data
        user_without_main = UserFactory()
        AlliancesAuditFactory()

        # Test Action
        result = AlliancesAudit.objects.visible_to(user_without_main)

        # Expected Result
        self.assertFalse(result.exists())
