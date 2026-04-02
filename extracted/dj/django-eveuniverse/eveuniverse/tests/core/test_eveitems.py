from django.test import TestCase

from eveuniverse.core import eveitems


class TestEveItems(TestCase):
    def test_type_url(self):
        self.assertEqual(
            eveitems.type_url(603), "https://www.kalkoken.org/apps/eveitems/?typeId=603"
        )
