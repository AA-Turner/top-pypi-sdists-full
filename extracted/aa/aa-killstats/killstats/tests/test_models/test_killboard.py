# AA Killstats
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import KillmailFactory

MODULE_PATH = "killstats.models.killstatsaudit"


class TestKillstatsAuditModel(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.killmail = KillmailFactory(
            killmail_id=1,
            killmail_date="2023-01-30 00:00:00",
            victim__id=1001,
            victim__name="Gneuten",
            victim_ship__id=10001,
            victim_ship__name="Victim Ship I",
            victim_corporation_id=2001,
        )
        cls.killmail2 = KillmailFactory(
            victim_alliance_id=3001,
        )

    def test_str(self):
        self.assertEqual(
            str(self.killmail),
            "Killmail 1 - 2023-01-30 00:00:00 - Gneuten - Victim Ship I (10001)",
        )

    def test_get_victim_name(self):
        expected_url = "Gneuten"
        self.assertEqual(self.killmail.get_or_unknown_victim_name(), expected_url)

    def test_get_victim_ship_name(self):
        expected_url = "Victim Ship I"
        self.assertEqual(self.killmail.get_or_unknown_victim_ship_name(), expected_url)

    def test_evaluate_zkb_link(self):
        expected_url = "https://zkillboard.com/character/1001/"
        self.assertEqual(self.killmail.evaluate_zkb_link(), expected_url)

        self.killmail.victim.category = "corporation"
        expected_url = "https://zkillboard.com/corporation/2001/"
        self.assertEqual(self.killmail.evaluate_zkb_link(), expected_url)

        self.killmail2.victim.category = "alliance"
        expected_url = "https://zkillboard.com/alliance/3001/"
        self.assertEqual(self.killmail2.evaluate_zkb_link(), expected_url)
