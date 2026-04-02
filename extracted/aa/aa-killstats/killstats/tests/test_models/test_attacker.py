# Django
from django.test import TestCase
from django.utils import timezone

# Alliance Auth (External Libs)
from eve_sde.models.types import ItemType

# AA Killstats
from killstats.models.general import EveEntity
from killstats.tests.testdata.eveentity import load_eveentity
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import create_attacker, create_killmail

MODULE_PATH = "killstats.models.killstatsaudit"


class TestAttackertModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_allianceauth()
        load_eveentity()
        cls.killmail = create_killmail(
            killmail_id=119303113,
            killmail_date=timezone.now(),
            victim=EveEntity.objects.get(id=1001),
            victim_ship=ItemType.objects.get(id=670),
            victim_corporation_id=2001,
            victim_alliance_id=3001,
            hash="hash",
            victim_total_value=1000,
            victim_fitted_value=500,
            victim_destroyed_value=500,
            victim_dropped_value=500,
            victim_region_id=1001,
            victim_solar_system_id=2001,
            victim_position_x=1.0,
            victim_position_y=1.0,
            victim_position_z=1.0,
        )
        cls.attacker = create_attacker(
            killmail=cls.killmail,
            character=EveEntity.objects.get(id=1000),
            corporation=EveEntity.objects.get(id=1000125),
            alliance=EveEntity.objects.get(id=3001),
            ship=ItemType.objects.get(id=670),
            damage_done=500,
            final_blow=True,
        )

    def test_evaluate_attacker_id(self):
        self.assertEqual(self.attacker.evaluate_attacker(), (1000, "CONCORD"))
        self.attacker.character = None
        self.assertEqual(self.attacker.evaluate_attacker(), (1000125, "CONCORD"))
        self.attacker.corporation = None
        self.assertEqual(self.attacker.evaluate_attacker(), (3001, "Voices of War"))
        self.attacker.alliance = None
        self.assertEqual(self.attacker.evaluate_attacker(), (0, "Unknown"))
