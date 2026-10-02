"""Unit tests for CorporationsAudit and AlliancesAudit models."""

# Standard Library
from datetime import datetime, timezone
from unittest.mock import Mock

# AA Killstats
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import (
    AlliancesAuditFactory,
    CorporationsAuditFactory,
    KillmailBodyFactory,
)

MODULE_PATH = "killstats.models.killstatsaudit"


class TestKillstatsAuditModel(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.audit1 = CorporationsAuditFactory(
            corporation__corporation_id=2001,
            corporation__corporation_name="Hell RiderZ",
        )
        cls.audit2 = AlliancesAuditFactory(
            alliance__alliance_id=3002, alliance__alliance_name="Eulen Sigma"
        )

    def test_corporation_str_should_return_formatted_string(self):
        # Test Action
        audit = CorporationsAudit.objects.get(corporation__corporation_id=2001)

        # Expected Result
        self.assertEqual(str(audit), "Hell RiderZ's Killstats Data")

    def test_alliance_str_should_return_formatted_string(self):
        # Test Action
        audit = AlliancesAudit.objects.get(alliance__alliance_id=3002)

        # Expected Result
        self.assertEqual(str(audit), "Eulen Sigma's Killstats Data")

    def test_is_corporation_should_return_true_when_victim_matches(self):
        # Test Data
        audit = self.audit1
        killmail = KillmailBodyFactory()
        killmail.esi.victim.corporation_id = 2001

        # Test Action
        result = audit.is_corporation(killmail)

        # Expected Result
        self.assertTrue(result)

    def test_is_corporation_should_return_true_when_attacker_matches(self):
        # Test Data
        audit = self.audit1
        killmail = KillmailBodyFactory()
        killmail.esi.victim.corporation_id = 99999
        killmail.esi.attackers[0].corporation_id = 2001

        # Test Action
        result = audit.is_corporation(killmail)

        # Expected Result
        self.assertTrue(result)

    def test_is_corporation_should_return_false_when_neither_victim_nor_attacker_matches(
        self,
    ):
        # Test Data
        audit = self.audit1
        killmail = KillmailBodyFactory()
        killmail.esi.victim.corporation_id = 99999
        killmail.esi.attackers[0].corporation_id = 88888

        # Test Action
        result = audit.is_corporation(killmail)

        # Expected Result
        self.assertFalse(result)

    def test_is_alliance_should_return_true_when_victim_matches(self):
        # Test Data
        audit = self.audit2
        killmail = KillmailBodyFactory()
        killmail.esi.victim.alliance_id = 3002

        # Test Action
        result = audit.is_alliance(killmail)

        # Expected Result
        self.assertTrue(result)

    def test_is_alliance_should_return_true_when_attacker_matches(self):
        # Test Data
        audit = self.audit2
        killmail = KillmailBodyFactory()
        killmail.esi.victim.alliance_id = 99999
        killmail.esi.attackers[0].alliance_id = 3002

        # Test Action
        result = audit.is_alliance(killmail)

        # Expected Result
        self.assertTrue(result)

    def test_is_alliance_should_return_false_when_neither_victim_nor_attacker_matches(
        self,
    ):
        # Test Data
        audit = self.audit2
        killmail = KillmailBodyFactory()
        killmail.esi.victim.alliance_id = 99999
        killmail.esi.attackers[0].alliance_id = 88888

        # Test Action
        result = audit.is_alliance(killmail)

        # Expected Result
        self.assertFalse(result)

    def test_last_missing_check_field_handling(self):
        # Test Data
        audit = self.audit1
        now = datetime.now(timezone.utc)

        # Test Action
        audit.last_missing_check = now
        audit.save()
        audit.refresh_from_db()

        # Expected Result
        self.assertIsNotNone(audit.last_missing_check)
