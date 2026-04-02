# Django
from django.test import TestCase

# AA Killstats
from killstats.models.killstatsaudit import AlliancesAudit, CorporationsAudit
from killstats.tests.testdata.eveentity import load_eveentity
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import create_owner_from_evecharacter

MODULE_PATH = "killstats.models.killstatsaudit"


class TestKillstatsAuditModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_allianceauth()
        load_eveentity()

        cls.audit1 = create_owner_from_evecharacter(
            character_id=1001,
        )
        cls.audit2 = create_owner_from_evecharacter(
            character_id=1007, owner_type="alliance"
        )

    def test_str(self):
        self.audit = CorporationsAudit.objects.get(corporation__corporation_id=2001)
        self.assertEqual(str(self.audit), "Hell RiderZ's Killstats Data")

    def test_alliance_str(self):
        self.audit = AlliancesAudit.objects.get(alliance__alliance_id=3002)
        self.assertEqual(str(self.audit), "Eulen Sigma's Killstats Data")
