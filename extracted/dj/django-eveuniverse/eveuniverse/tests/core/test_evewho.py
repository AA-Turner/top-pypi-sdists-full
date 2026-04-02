from django.test import TestCase

from eveuniverse.core import evewho


class TestEveWho(TestCase):
    def test_alliance_url(self):
        self.assertEqual(
            evewho.alliance_url(12345678), "https://evewho.com/alliance/12345678"
        )

    def test_corporation_url(self):
        self.assertEqual(
            evewho.corporation_url(12345678), "https://evewho.com/corporation/12345678"
        )

    def test_character_url(self):
        self.assertEqual(
            evewho.character_url(12345678), "https://evewho.com/character/12345678"
        )
