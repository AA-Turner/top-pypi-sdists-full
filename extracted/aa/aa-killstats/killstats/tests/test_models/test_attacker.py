# Django
from django.utils import timezone

# Alliance Auth (External Libs)
from eve_sde.models.types import ItemType

# AA Killstats
from killstats.models.general import EveEntity
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import AttackerFactory, KillmailFactory

MODULE_PATH = "killstats.models.killstatsaudit"


class TestAttackerModel(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.killmail = KillmailFactory()
        cls.attacker = AttackerFactory(
            character__id=1000,
            character__name="Character",
            corporation__id=1000125,
            corporation__name="CONCORD",
            alliance__id=3001,
            alliance__name="Voices of War",
        )

    def test_evaluate_attacker_id(self):
        self.assertEqual(self.attacker.evaluate_attacker(), (1000, "Character"))
        self.attacker.character = None
        self.assertEqual(self.attacker.evaluate_attacker(), (1000125, "CONCORD"))
        self.attacker.corporation = None
        self.assertEqual(self.attacker.evaluate_attacker(), (3001, "Voices of War"))
        self.attacker.alliance = None
        self.assertEqual(self.attacker.evaluate_attacker(), (0, "Unknown"))
