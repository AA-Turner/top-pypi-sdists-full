"""Unit tests for General and EveEntity models."""

# Standard Library
import datetime
from unittest.mock import patch

# Django
from django.utils import timezone

# AA Killstats
from killstats.models.general import EveEntity, General
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import EveEntityFactory

MODULE_PATH = "killstats.models.general"


class TestGeneralModel(AuthTestCase):
    def test_general_model_meta_should_define_permissions(self):
        # Test Data & Action
        permissions = dict(General._meta.permissions)

        # Expected Result
        self.assertIn("basic_access", permissions)
        self.assertIn("admin_access", permissions)
        self.assertEqual(General._meta.verbose_name, "AA-Killstats")
        self.assertFalse(General._meta.managed)


class TestEveEntityModel(AuthTestCase):
    def test_string_representation_should_return_name(self):
        # Test Data
        entity = EveEntityFactory(name="Test Pilot")

        # Test Action
        result = str(entity)

        # Expected Result
        self.assertEqual(result, "Test Pilot")

    def test_repr_representation_should_contain_class_id_category_and_name(self):
        # Test Data
        entity = EveEntityFactory(
            id=12345, category=EveEntity.CATEGORY_CHARACTER, name="Test Pilot"
        )

        # Test Action
        result = repr(entity)

        # Expected Result
        self.assertEqual(
            result, "EveEntity(id=12345, category='character', name='Test Pilot')"
        )

    def test_is_alliance_should_return_true_for_alliance_category(self):
        # Test Data
        entity = EveEntityFactory(category=EveEntity.CATEGORY_ALLIANCE)

        # Test Action & Expected Result
        self.assertTrue(entity.is_alliance)
        self.assertFalse(entity.is_corporation)
        self.assertFalse(entity.is_character)

    def test_is_corporation_should_return_true_for_corporation_category(self):
        # Test Data
        entity = EveEntityFactory(category=EveEntity.CATEGORY_CORPORATION)

        # Test Action & Expected Result
        self.assertTrue(entity.is_corporation)
        self.assertFalse(entity.is_alliance)
        self.assertFalse(entity.is_character)

    def test_is_character_should_return_true_for_character_category(self):
        # Test Data
        entity = EveEntityFactory(category=EveEntity.CATEGORY_CHARACTER)

        # Test Action & Expected Result
        self.assertTrue(entity.is_character)
        self.assertFalse(entity.is_alliance)
        self.assertFalse(entity.is_corporation)

    @patch(f"{MODULE_PATH}.get_alliance_logo_url")
    def test_get_portrait_should_delegate_to_alliance_logo_url_for_alliance(
        self, mock_logo_url
    ):
        # Test Data
        mock_logo_url.return_value = "https://images.example/alliance/3001"
        entity = EveEntityFactory(
            id=3001, category=EveEntity.CATEGORY_ALLIANCE, name="Test Alliance"
        )

        # Test Action
        result = entity.get_portrait(size=64, as_html=False)

        # Expected Result
        self.assertEqual(result, "https://images.example/alliance/3001")
        mock_logo_url.assert_called_once_with(
            alliance_id=3001, size=64, alliance_name="Test Alliance", as_html=False
        )

    @patch(f"{MODULE_PATH}.get_corporation_logo_url")
    def test_get_portrait_should_delegate_to_corporation_logo_url_for_corporation(
        self, mock_logo_url
    ):
        # Test Data
        mock_logo_url.return_value = "https://images.example/corp/2001"
        entity = EveEntityFactory(
            id=2001, category=EveEntity.CATEGORY_CORPORATION, name="Test Corp"
        )

        # Test Action
        result = entity.get_portrait(size=128, as_html=True)

        # Expected Result
        self.assertEqual(result, "https://images.example/corp/2001")
        mock_logo_url.assert_called_once_with(
            corporation_id=2001, size=128, corporation_name="Test Corp", as_html=True
        )

    @patch(f"{MODULE_PATH}.get_character_portrait_url")
    def test_get_portrait_should_delegate_to_character_portrait_url_for_character(
        self, mock_portrait_url
    ):
        # Test Data
        mock_portrait_url.return_value = "https://images.example/char/1001"
        entity = EveEntityFactory(
            id=1001, category=EveEntity.CATEGORY_CHARACTER, name="Test Pilot"
        )

        # Test Action
        result = entity.get_portrait(size=64, as_html=False)

        # Expected Result
        self.assertEqual(result, "https://images.example/char/1001")
        mock_portrait_url.assert_called_once_with(
            character_id=1001, size=64, character_name="Test Pilot", as_html=False
        )

    def test_get_portrait_should_return_empty_string_for_unknown_category(self):
        # Test Data
        entity = EveEntityFactory.build(id=999, category="unknown", name="Other")

        # Test Action
        result = entity.get_portrait()

        # Expected Result
        self.assertEqual(result, "")

    @patch(f"{MODULE_PATH}.EveAllianceInfo.generic_logo_url")
    def test_icon_url_should_return_alliance_generic_logo_url(self, mock_logo_url):
        # Test Data
        mock_logo_url.return_value = "https://images.example/alliance/3001_128.png"
        entity = EveEntityFactory(id=3001, category=EveEntity.CATEGORY_ALLIANCE)

        # Test Action
        result = entity.icon_url(size=128)

        # Expected Result
        self.assertEqual(result, "https://images.example/alliance/3001_128.png")
        mock_logo_url.assert_called_once_with(3001, size=128)

    @patch(f"{MODULE_PATH}.EveCorporationInfo.generic_logo_url")
    def test_icon_url_should_return_corporation_generic_logo_url(self, mock_logo_url):
        # Test Data
        mock_logo_url.return_value = "https://images.example/corp/2001_128.png"
        entity = EveEntityFactory(id=2001, category=EveEntity.CATEGORY_CORPORATION)

        # Test Action
        result = entity.icon_url(size=128)

        # Expected Result
        self.assertEqual(result, "https://images.example/corp/2001_128.png")
        mock_logo_url.assert_called_once_with(2001, size=128)

    @patch(f"{MODULE_PATH}.EveCharacter.generic_portrait_url")
    def test_icon_url_should_return_character_generic_portrait_url(
        self, mock_portrait_url
    ):
        # Test Data
        mock_portrait_url.return_value = "https://images.example/char/1001_128.jpg"
        entity = EveEntityFactory(id=1001, category=EveEntity.CATEGORY_CHARACTER)

        # Test Action
        result = entity.icon_url(size=128)

        # Expected Result
        self.assertEqual(result, "https://images.example/char/1001_128.jpg")
        mock_portrait_url.assert_called_once_with(1001, size=128)

    def test_icon_url_should_raise_not_implemented_error_for_unknown_category(self):
        # Test Data
        entity = EveEntityFactory.build(id=999, category="solar_system")

        # Test Action & Expected Result
        with self.assertRaises(NotImplementedError):
            entity.icon_url()

    def test_needs_update_should_return_false_when_updated_recently(self):
        # Test Data
        entity = EveEntityFactory()
        entity.last_update = timezone.now() - datetime.timedelta(days=2)

        # Test Action & Expected Result
        self.assertFalse(entity.needs_update())

    def test_needs_update_should_return_true_when_updated_more_than_seven_days_ago(
        self,
    ):
        # Test Data
        entity = EveEntityFactory()
        entity.last_update = timezone.now() - datetime.timedelta(days=8)

        # Test Action & Expected Result
        self.assertTrue(entity.needs_update())
