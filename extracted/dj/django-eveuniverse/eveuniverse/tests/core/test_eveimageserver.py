from django.test import TestCase

from eveuniverse.core import eveimageserver


class TestEveImageServer(TestCase):
    """unit test for eveimageserver"""

    def test_sizes(self):
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42
            ),
            "https://images.evetech.net/characters/42/portrait?size=32",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42, size=32
            ),
            "https://images.evetech.net/characters/42/portrait?size=32",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42, size=64
            ),
            "https://images.evetech.net/characters/42/portrait?size=64",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42, size=128
            ),
            "https://images.evetech.net/characters/42/portrait?size=128",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42, size=256
            ),
            "https://images.evetech.net/characters/42/portrait?size=256",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42, size=512
            ),
            "https://images.evetech.net/characters/42/portrait?size=512",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42, size=1024
            ),
            "https://images.evetech.net/characters/42/portrait?size=1024",
        )
        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CORPORATION, 42, size=-5
            )

        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CORPORATION, 42, size=0
            )

        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CORPORATION, 42, size=31
            )

        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CORPORATION, 42, size=1025
            )

        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CORPORATION, 42, size=2048
            )

    def test_variant(self):
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER,
                42,
                variant=eveimageserver.ImageVariant.PORTRAIT,
            ),
            "https://images.evetech.net/characters/42/portrait?size=32",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.ALLIANCE,
                42,
                variant=eveimageserver.ImageVariant.LOGO,
            ),
            "https://images.evetech.net/alliances/42/logo?size=32",
        )
        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER,
                42,
                variant=eveimageserver.ImageVariant.LOGO,
            )

    def test_categories(self):
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.ALLIANCE, 42
            ),
            "https://images.evetech.net/alliances/42/logo?size=32",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CORPORATION, 42
            ),
            "https://images.evetech.net/corporations/42/logo?size=32",
        )
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42
            ),
            "https://images.evetech.net/characters/42/portrait?size=32",
        )
        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url("invalid", 42)  # type: ignore

    def test_tenants(self):
        self.assertEqual(
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER,
                42,
                tenant=eveimageserver.EsiTenant.TRANQUILITY,
            ),
            "https://images.evetech.net/characters/42/portrait?size=32&tenant=tranquility",
        )
        with self.assertRaises(ValueError):
            eveimageserver._eve_entity_image_url(
                eveimageserver.EsiCategory.CHARACTER, 42, tenant="xxx"  # type: ignore
            )

    def test_alliance_logo_url(self):
        expected = "https://images.evetech.net/alliances/42/logo?size=128"
        self.assertEqual(eveimageserver.alliance_logo_url(42, 128), expected)

    def test_corporation_logo_url(self):
        expected = "https://images.evetech.net/corporations/42/logo?size=128"
        self.assertEqual(eveimageserver.corporation_logo_url(42, 128), expected)

    def test_character_portrait_url(self):
        expected = "https://images.evetech.net/characters/42/portrait?size=128"
        self.assertEqual(eveimageserver.character_portrait_url(42, 128), expected)

    def test_faction_logo_url(self):
        expected = "https://images.evetech.net/corporations/42/logo?size=128"
        self.assertEqual(eveimageserver.faction_logo_url(42, 128), expected)

    def test_type_icon_url(self):
        expected = "https://images.evetech.net/types/42/icon?size=128"
        self.assertEqual(eveimageserver.type_icon_url(42, 128), expected)

    def test_type_render_url(self):
        expected = "https://images.evetech.net/types/42/render?size=128"
        self.assertEqual(eveimageserver.type_render_url(42, 128), expected)

    def test_type_bp_url(self):
        expected = "https://images.evetech.net/types/42/bp?size=128"
        self.assertEqual(eveimageserver.type_bp_url(42, 128), expected)

    def test_type_bpc_url(self):
        expected = "https://images.evetech.net/types/42/bpc?size=128"
        self.assertEqual(eveimageserver.type_bpc_url(42, 128), expected)
