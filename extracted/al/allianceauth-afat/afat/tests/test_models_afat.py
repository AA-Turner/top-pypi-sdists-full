"""
Tests for the AFAT models
"""

# Standard Library
from unittest.mock import patch

# Django
from django.db import IntegrityError
from django.utils import timezone

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.models import Doctrine, Fat, FatLink, FleetType, get_hash_on_save
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import create_user_from_evecharacter


class TestGetHashOnSave(BaseTestCase):
    """
    Tests for the get_hash_on_save function
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup the test class

        :return:
        :rtype:
        """

        super().setUpClass()

        cls.character_1001 = EveCharacter.objects.get(character_id=1001)
        cls.character_1002 = EveCharacter.objects.get(character_id=1002)
        cls.character_1003 = EveCharacter.objects.get(character_id=1003)
        cls.character_1004 = EveCharacter.objects.get(character_id=1004)
        cls.character_1005 = EveCharacter.objects.get(character_id=1005)
        cls.character_1101 = EveCharacter.objects.get(character_id=1101)

        cls.user_without_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1001.character_id
        )

        cls.user_with_basic_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1002.character_id,
            permissions=["afat.basic_access"],
        )

        cls.user_with_manage_afat, _ = create_user_from_evecharacter(
            character_id=cls.character_1003.character_id,
            permissions=["afat.basic_access", "afat.manage_afat"],
        )

        cls.user_with_add_fatlink, _ = create_user_from_evecharacter(
            character_id=cls.character_1004.character_id,
            permissions=["afat.basic_access", "afat.add_fatlink"],
        )

    def test_get_hash_on_save_returns_30_char_unique(self):
        """
        Ensure get_hash_on_save returns a 30-character string that does not already
        exist as a FatLink.hash in the database.

        :return:
        :rtype:
        """

        result = get_hash_on_save()

        self.assertEqual(len(result), 30)
        self.assertFalse(FatLink.objects.filter(hash=result).exists())

    def test_get_hash_on_save_retries_on_collision(self):
        """
        Ensure get_hash_on_save retries when generated hashes collide with existing
        FatLink.hash values and returns the first unique value.

        :return:
        :rtype:
        """

        collide1 = "x" * 30
        collide2 = "y" * 30
        unique = "z" * 30

        FatLink.objects.create(
            created=timezone.now(),
            fleet="Collide1",
            creator=self.user_with_add_fatlink,
            character=self.character_1001,
            hash=collide1,
        )
        FatLink.objects.create(
            created=timezone.now(),
            fleet="Collide2",
            creator=self.user_with_add_fatlink,
            character=self.character_1001,
            hash=collide2,
        )

        with patch(
            "afat.models.afat.get_random_string",
            side_effect=[collide1, collide2, unique],
        ):
            result = get_hash_on_save()

        self.assertEqual(result, unique)
        self.assertFalse(FatLink.objects.filter(hash=result).exists())


class TestFleetType(BaseTestCase):
    """
    Tests for the FleetType model
    """

    def test_returns_string_representation_as_name(self):
        """
        Test that the FleetType string representation is as expected

        :return:
        :rtype:
        """

        fleet_type = FleetType.objects.create(name="Alpha Strike")

        self.assertEqual(str(fleet_type), "Alpha Strike")
        self.assertEqual(fleet_type.name, "Alpha Strike")

    def test_default_is_enabled_true_and_can_be_disabled(self):
        """
        Test that the default FleetType is enabled or disabled

        :return:
        :rtype:
        """

        ft_default = FleetType.objects.create(name="Default Enabled")
        self.assertTrue(ft_default.is_enabled)

        ft_disabled = FleetType.objects.create(
            name="Explicit Disabled", is_enabled=False
        )
        self.assertFalse(ft_disabled.is_enabled)

        # Persisted values are stored correctly in the database
        reloaded_default = FleetType.objects.get(pk=ft_default.pk)
        reloaded_disabled = FleetType.objects.get(pk=ft_disabled.pk)
        self.assertTrue(reloaded_default.is_enabled)
        self.assertFalse(reloaded_disabled.is_enabled)


class TestFatLink(BaseTestCase):
    """
    Tests for the FatLink model
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup the test class

        :return:
        :rtype:
        """

        super().setUpClass()

        cls.character_1001 = EveCharacter.objects.get(character_id=1001)
        cls.character_1002 = EveCharacter.objects.get(character_id=1002)
        cls.character_1003 = EveCharacter.objects.get(character_id=1003)
        cls.character_1004 = EveCharacter.objects.get(character_id=1004)
        cls.character_1005 = EveCharacter.objects.get(character_id=1005)
        cls.character_1101 = EveCharacter.objects.get(character_id=1101)

        cls.user_without_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1001.character_id
        )

        cls.user_with_basic_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1002.character_id,
            permissions=["afat.basic_access"],
        )

        cls.user_with_manage_afat, _ = create_user_from_evecharacter(
            character_id=cls.character_1003.character_id,
            permissions=["afat.basic_access", "afat.manage_afat"],
        )

        cls.user_with_add_fatlink, _ = create_user_from_evecharacter(
            character_id=cls.character_1004.character_id,
            permissions=["afat.basic_access", "afat.add_fatlink"],
        )

    def test_str_returns_fleet_and_hash(self):
        """
        Test FatLink.__str__ returns the expected 'fleet - hash' string.

        :return:
        :rtype:
        """
        fatlink_hash = get_hash_on_save()
        fatlink = FatLink.objects.create(
            created=timezone.now(),
            fleet="Fleet StringTest",
            creator=self.user_with_add_fatlink,
            character=self.character_1001,
            hash=fatlink_hash,
        )

        self.assertEqual(str(fatlink), f"{fatlink.fleet} - {fatlink.hash}")

    def test_number_of_fats_reflects_related_fat_count(self):
        """
        Test number of FATs reflects related FAT count

        :return:
        :rtype:
        """

        fatlink_hash = get_hash_on_save()
        fatlink = FatLink.objects.create(
            created=timezone.now(),
            fleet="Fleet CountTest",
            creator=self.user_with_add_fatlink,
            character=self.character_1001,
            hash=fatlink_hash,
        )

        Fat.objects.create(
            character=self.character_1002, fatlink=fatlink, shiptype="ShipA"
        )
        Fat.objects.create(
            character=self.character_1003, fatlink=fatlink, shiptype="ShipB"
        )

        self.assertEqual(fatlink.number_of_fats, 2)

    def test_save_generates_hash_when_attribute_access_raises_ObjectDoesNotExist(self):
        """
        Test FatLink.save sets a hash using get_hash_on_save when accessing
        self.hash raises ObjectDoesNotExist (covers the except branch in save()).

        :return:
        :rtype:
        """

        # Django
        from django.core.exceptions import ObjectDoesNotExist

        fatlink = FatLink(
            created=timezone.now(),
            fleet="Fleet AutoHash",
            creator=self.user_with_add_fatlink,
            character=self.character_1001,
        )

        original_getattribute = FatLink.__getattribute__

        def raising_getattribute(self, name):
            """
            Mocked __getattribute__.

            :param self:
            :type self:
            :param name:
            :type name:
            :return:
            :rtype:
            """

            if name == "hash":
                # Force attribute access to raise to exercise the except branch
                raise ObjectDoesNotExist()

            return original_getattribute(self, name)

        FatLink.__getattribute__ = raising_getattribute

        try:
            # Prevent actual DB insert during this test so the overridden
            # __getattribute__ does not interfere with ORM internals.
            with (
                patch(
                    "afat.models.afat.get_hash_on_save",
                    return_value="auto_generated_hash_123",
                ),
                patch("django.db.models.Model.save", return_value=None),
            ):
                fatlink.save()

            # After save() (DB save was suppressed) the instance should have received the generated hash
            # Accessing fatlink.hash would trigger our raising_getattribute, so inspect __dict__ directly
            self.assertEqual(fatlink.__dict__.get("hash"), "auto_generated_hash_123")
        finally:
            FatLink.__getattribute__ = original_getattribute


class TestFat(BaseTestCase):
    """
    Tests for the Fat model
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup the test class

        :return:
        :rtype:
        """

        super().setUpClass()

        cls.character_1001 = EveCharacter.objects.get(character_id=1001)
        cls.character_1002 = EveCharacter.objects.get(character_id=1002)

        cls.user_with_add_fatlink, _ = create_user_from_evecharacter(
            character_id=cls.character_1001.character_id,
            permissions=["afat.basic_access", "afat.add_fatlink"],
        )

        # Create a FatLink to associate with Fat instances
        cls.fatlink = FatLink.objects.create(
            created=timezone.now(),
            fleet="FatModel Fleet",
            creator=cls.user_with_add_fatlink,
            character=cls.character_1001,
            hash=get_hash_on_save(),
        )

    def test_returns_string_representation_with_fatlink_and_character(self):
        """
        Test __str__ should return '<fatlink> - <character>'

        :return:
        :rtype:
        """

        fat = Fat.objects.create(character=self.character_1002, fatlink=self.fatlink)

        self.assertEqual(str(fat), f"{fat.fatlink} - {fat.character}")

    def test_enforces_unique_constraint_on_character_and_fatlink(self):
        """
        Test enforces unique constraint on character and fatlink.

        Creating two Fat records with the same (character, fatlink) should
        violate the unique_together constraint.

        :return:
        :rtype:
        """

        Fat.objects.create(character=self.character_1002, fatlink=self.fatlink)

        with self.assertRaises(IntegrityError):
            Fat.objects.create(character=self.character_1002, fatlink=self.fatlink)

    def test_nullable_fields_can_be_none_and_instance_saved(self):
        """
        Test that nullable fields (system, ship, shiptype) can be None and the instance can be saved.

        Fields like system, ship, solar_system and shiptype are nullable and
        saving with None values should succeed.

        :return:
        :rtype:
        """

        fat = Fat.objects.create(character=self.character_1002, fatlink=self.fatlink)

        self.assertIsNone(fat.system)
        self.assertIsNone(fat.ship)
        self.assertIsNone(fat.shiptype)


class TestDoctrineModel(BaseTestCase):
    """
    Tests for the Doctrine model
    """

    def test_str_returns_name(self):
        """
        Test __str__ should return the doctrine name string

        :return:
        :rtype:
        """

        doctrine = Doctrine.objects.create(name="Alpha Doctrine")

        self.assertEqual(str(doctrine), "Alpha Doctrine")

    def test_duplicate_name_violates_unique_constraint(self):
        """
        Test that creating two Doctrine records with the same name violates the unique constraint.

        :return:
        :rtype:
        """

        Doctrine.objects.create(name="UniqueDoctrine")

        # Django
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Doctrine.objects.create(name="UniqueDoctrine")

    def test_notes_default_and_is_enabled_default(self):
        """
        Test that the default value for notes is an empty string and is_enabled is True.

        :return:
        :rtype:
        """

        d = Doctrine.objects.create(name="NotesTest")

        self.assertEqual(d.notes, "")
        self.assertTrue(d.is_enabled)

        reloaded = Doctrine.objects.get(pk=d.pk)
        self.assertEqual(reloaded.notes, "")
        self.assertTrue(reloaded.is_enabled)

    def test_can_set_is_enabled_to_false(self):
        """
        Test that the default value for is_enabled is an empty string and is_enabled is False.

        :return:
        :rtype:
        """

        d = Doctrine.objects.create(name="DisabledDoctrine", is_enabled=False)

        self.assertFalse(d.is_enabled)

        reloaded = Doctrine.objects.get(pk=d.pk)
        self.assertFalse(reloaded.is_enabled)
