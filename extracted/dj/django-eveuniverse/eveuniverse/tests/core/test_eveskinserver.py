from django.test import TestCase

from eveuniverse.core import eveskinserver


class TestEveSkinServer(TestCase):
    """unit test for eveskinserver"""

    def test_default(self):
        """when called without size, will return url with default size"""
        self.assertEqual(
            eveskinserver.type_icon_url(42),
            "https://eveskinserver.kalkoken.net/skin/42/icon?size=32",
        )

    def test_valid_size(self):
        """when called with valid size, will return url with size"""
        self.assertEqual(
            eveskinserver.type_icon_url(42, size=64),
            "https://eveskinserver.kalkoken.net/skin/42/icon?size=64",
        )

    def test_invalid_size(self):
        """when called with invalid size, will raise exception"""
        with self.assertRaises(ValueError):
            eveskinserver.type_icon_url(42, size=22)
