"""
Test AFAT helpers
"""

# Standard Library
from datetime import timedelta
from unittest.mock import MagicMock, patch

# Django
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.user import get_main_character_name_from_user

# Alliance Auth AFAT
from afat.helper.fatlinks import get_esi_fleet_information_by_user
from afat.helper.time import get_time_delta
from afat.helper.views import (
    _cached_main_character_name,
    _get_request_cache,
    _perm_flags,
    convert_fatlinks_to_dict,
    convert_fats_to_dict,
)
from afat.models import Fat, FatLink, get_hash_on_save
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import (
    add_character_to_user,
    create_user_from_evecharacter,
)

MODULE_PATH = "afat.views.fatlinks"


class TestHelpers(BaseTestCase):
    """
    Test Helpers
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup the test class

        :return:
        :rtype:
        """

        super().setUpClass()

        cls.factory = RequestFactory()

        # given
        cls.character_1001 = EveCharacter.objects.get(character_id=1001)
        cls.character_1002 = EveCharacter.objects.get(character_id=1002)
        cls.character_1003 = EveCharacter.objects.get(character_id=1003)
        cls.character_1004 = EveCharacter.objects.get(character_id=1004)
        cls.character_1005 = EveCharacter.objects.get(character_id=1005)
        cls.character_1101 = EveCharacter.objects.get(character_id=1101)

        cls.user_with_add_fatlink, _ = create_user_from_evecharacter(
            character_id=cls.character_1001.character_id,
            permissions=["afat.basic_access", "afat.add_fatlink"],
        )

        add_character_to_user(
            user=cls.user_with_add_fatlink, character=cls.character_1101
        )

        cls.user_with_manage_afat, _ = create_user_from_evecharacter(
            character_id=cls.character_1002.character_id,
            permissions=["afat.basic_access", "afat.manage_afat"],
        )

        add_character_to_user(
            user=cls.user_with_add_fatlink, character=cls.character_1003
        )

    def test_helper_get_esi_fleet_information_by_user(self):
        """
        Test helper get_esi_fleet_information_by_user

        :return:
        :rtype:
        """

        fatlink_hash_fleet_1 = get_hash_on_save()
        fatlink_1 = FatLink.objects.create(
            created=timezone.now(),
            fleet="April Fleet 1",
            creator=self.user_with_add_fatlink,
            character=self.character_1001,
            hash=fatlink_hash_fleet_1,
            is_esilink=True,
            is_registered_on_esi=True,
            esi_fleet_id="3726458287",
        )

        fatlink_hash_fleet_2 = get_hash_on_save()
        fatlink_2 = FatLink.objects.create(
            created=timezone.now(),
            fleet="April Fleet 2",
            creator=self.user_with_add_fatlink,
            character=self.character_1101,
            hash=fatlink_hash_fleet_2,
            is_esilink=True,
            is_registered_on_esi=True,
            esi_fleet_id="372645827",
        )

        self.client.force_login(user=self.user_with_add_fatlink)

        response = get_esi_fleet_information_by_user(user=self.user_with_add_fatlink)

        self.assertDictEqual(
            d1=response,
            d2={
                "has_open_esi_fleets": True,
                "open_esi_fleets_list": [fatlink_1, fatlink_2],
            },
        )

    def test_helper_get_time_delta(self):
        """
        Test helper get_time_delta

        :return:
        :rtype:
        """

        duration = 1812345
        now = timezone.now()
        expires = timedelta(minutes=duration) + now

        self.client.force_login(user=self.user_with_add_fatlink)

        total = get_time_delta(then=now, now=expires)
        years = get_time_delta(then=now, now=expires, interval="years")
        days = get_time_delta(then=now, now=expires, interval="days")
        hours = get_time_delta(then=now, now=expires, interval="hours")
        minutes = get_time_delta(then=now, now=expires, interval="minutes")
        seconds = get_time_delta(then=now, now=expires, interval="seconds")

        self.assertEqual(
            first=total, second="3 years, 163 days, 13 hours, 45 minutes and 0 seconds"
        )
        self.assertEqual(first=years, second=3)
        self.assertEqual(first=days, second=1258)
        self.assertEqual(first=hours, second=30205)
        self.assertEqual(first=minutes, second=1812345)
        self.assertEqual(first=seconds, second=108740700)

    def test_helper_convert_fatlinks_to_dict(self):
        """
        Test helper convert_fatlinks_to_dict

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)
        request = self.factory.get(path=reverse(viewname="afat:dashboard"))
        request.user = self.user_with_manage_afat

        fatlink_hash_fleet_1 = get_hash_on_save()
        fatlink_1_created = FatLink.objects.create(
            created=timezone.now(),
            fleet="April Fleet 1",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
            hash=fatlink_hash_fleet_1,
            is_esilink=True,
            is_registered_on_esi=True,
            esi_fleet_id="3726458287",
            doctrine="Ships",
        )
        Fat.objects.create(
            character=self.character_1101, fatlink=fatlink_1_created, shiptype="Omen"
        )

        fatlink_hash_fleet_2 = get_hash_on_save()
        fatlink_2_created = FatLink.objects.create(
            created=timezone.now(),
            fleet="April Fleet 2",
            creator=self.user_with_add_fatlink,
            character=self.character_1101,
            hash=fatlink_hash_fleet_2,
            fleet_type="CTA",
            doctrine="Ships",
        )
        Fat.objects.create(
            character=self.character_1001, fatlink=fatlink_2_created, shiptype="Omen"
        )

        fatlink_1 = FatLink.objects.select_related_default().get(
            hash=fatlink_hash_fleet_1
        )
        close_esi_tracking_url = reverse(
            viewname="afat:fatlinks_close_esi_fatlink", args=[fatlink_1.hash]
        )
        edit_url_1 = reverse(
            viewname="afat:fatlinks_details_fatlink", args=[fatlink_1.hash]
        )
        delete_url_1 = reverse(
            viewname="afat:fatlinks_delete_fatlink", args=[fatlink_1.hash]
        )

        fatlink_2 = FatLink.objects.select_related_default().get(
            hash=fatlink_hash_fleet_2
        )
        edit_url_2 = reverse(
            viewname="afat:fatlinks_details_fatlink", args=[fatlink_2.hash]
        )
        delete_url_2 = reverse(
            viewname="afat:fatlinks_delete_fatlink", args=[fatlink_2.hash]
        )

        result_1 = convert_fatlinks_to_dict(request=request, fatlink=fatlink_1)
        result_2 = convert_fatlinks_to_dict(request=request, fatlink=fatlink_2)

        fleet_time_1 = fatlink_1.created
        fleet_time_timestamp_1 = fleet_time_1.timestamp()
        creator_main_character_1 = get_main_character_name_from_user(
            user=fatlink_1.creator
        )

        self.maxDiff = None

        self.assertDictEqual(
            d1=result_1,
            d2={
                "pk": fatlink_1.pk,
                "fleet_name": (
                    'April Fleet 1<span class="badge text-bg-success afat-label ms-2">ESI</span>'
                ),
                "creator_name": creator_main_character_1,
                "fleet_type": "",
                "doctrine": "Ships",
                "fleet_time": {
                    "time": fleet_time_1,
                    "timestamp": fleet_time_timestamp_1,
                },
                "fats_number": fatlink_1.number_of_fats,
                "hash": fatlink_1.hash,
                "is_esilink": True,
                "esi_fleet_id": 3726458287,
                "is_registered_on_esi": True,
                "actions": (
                    '<a class="btn btn-afat-action btn-primary btn-sm m-1" '
                    'title="Stop automatic tracking '
                    'through ESI for this fleet and close the associated FAT link." '
                    'data-bs-toggle="modal" '
                    'data-bs-target="#cancelEsiFleetModal" '
                    'data-bs-tooltip="afat" '
                    f'data-url="{close_esi_tracking_url}" '
                    'data-body-text="<p>Are you sure you want to close ESI '
                    'fleet with ID 3726458287 from Bruce Wayne?</p>" '
                    'data-confirm-text="Stop tracking"><i class="fa-solid '
                    'fa-times"></i></a><a class="btn btn-info btn-sm m-1" '
                    f'href="{edit_url_1}"><span class="fa-solid '
                    'fa-eye"></span></a><a class="btn btn-danger btn-sm" '
                    'data-bs-toggle="modal" data-bs-target="#deleteFatLinkModal" '
                    f'data-url="{delete_url_1}" '
                    'data-confirm-text="Delete" data-body-text="<p>Are you '
                    "sure you want to delete FAT link April Fleet "
                    '1?</p>"><i class="fa-solid fa-trash-can fa-fw"></i></a>'
                ),
                "via_esi": "Yes",
            },
        )

        fleet_time_2 = fatlink_2.created
        fleet_time_timestamp_2 = fleet_time_2.timestamp()
        creator_main_character_2 = get_main_character_name_from_user(
            user=fatlink_2.creator
        )

        self.assertDictEqual(
            d1=result_2,
            d2={
                "pk": fatlink_2.pk,
                "fleet_name": "April Fleet 2",
                "creator_name": creator_main_character_2,
                "fleet_type": "CTA",
                "doctrine": "Ships",
                "fleet_time": {
                    "time": fleet_time_2,
                    "timestamp": fleet_time_timestamp_2,
                },
                "fats_number": fatlink_2.number_of_fats,
                "hash": fatlink_2.hash,
                "is_esilink": False,
                "esi_fleet_id": None,
                "is_registered_on_esi": False,
                "actions": (
                    '<a class="btn btn-info btn-sm m-1" '
                    f'href="{edit_url_2}"><span '
                    'class="fa-solid fa-eye"></span></a><a class="btn btn-danger '
                    'btn-sm" data-bs-toggle="modal" '
                    'data-bs-target="#deleteFatLinkModal" '
                    f'data-url="{delete_url_2}" '
                    'data-confirm-text="Delete" data-body-text="<p>Are you sure you '
                    'want to delete FAT link April Fleet 2?</p>"><i class="fa-solid '
                    'fa-trash-can fa-fw"></i></a>'
                ),
                "via_esi": "No",
            },
        )

    def test_helper_convert_fats_to_dict(self):
        """
        Test helper convert_fats_to_dict

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)
        request = self.factory.get(path=reverse(viewname="afat:dashboard"))
        request.user = self.user_with_manage_afat

        fatlink_hash = get_hash_on_save()
        fatlink_created = FatLink.objects.create(
            created=timezone.now(),
            fleet="April Fleet 1",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
            hash=fatlink_hash,
            is_esilink=True,
            is_registered_on_esi=True,
            esi_fleet_id="3726458287",
            fleet_type="CTA",
            doctrine="Ships",
        )
        fat = Fat.objects.create(
            character=self.character_1101, fatlink=fatlink_created, shiptype="Omen"
        )

        result = convert_fats_to_dict(request=request, fat=fat)

        esi_marker = '<span class="badge text-bg-success afat-label ms-2">ESI</span>'
        fleet_time = fat.fatlink.created
        fleet_time_timestamp = fleet_time.timestamp()

        button_delete_fat = reverse(
            viewname="afat:fatlinks_delete_fat", args=[fat.fatlink.hash, fat.id]
        )
        button_delete_text = "Delete"
        modal_body_text = (
            "<p>Are you sure you want to remove "
            f"{fat.character.character_name} from this FAT link?</p>"
        )

        self.assertDictEqual(
            d1=result,
            d2={
                "system": fat.system,
                "ship_type": fat.shiptype,
                "character_name": fat.character.character_name,
                "doctrine": "Ships",
                "fleet_name": fat.fatlink.fleet + esi_marker,
                "fleet_time": {"time": fleet_time, "timestamp": fleet_time_timestamp},
                "fleet_type": "CTA",
                "via_esi": "Yes",
                "actions": (
                    '<a class="btn btn-danger btn-sm" data-bs-toggle="modal" '
                    'data-bs-target="#deleteFatModal" '
                    f'data-url="{button_delete_fat}" '
                    f'data-confirm-text="{button_delete_text}" '
                    f'data-body-text="{modal_body_text}">'
                    '<i class="fa-solid fa-trash-can fa-fw"></i></a>'
                ),
            },
        )


class TestHelperCachedMainCharacterName(BaseTestCase):
    """
    Test _cached_main_character_name function
    """

    def test_returns_cached_name_if_present(self):
        """
        Test that the function returns the cached name if present.

        :return:
        :rtype:
        """

        request = MagicMock()
        request._afat_cache = {"main_char_names": {1: "Cached Character"}}
        user = MagicMock(pk=1)

        with patch("afat.helper.views.get_main_character_name_from_user") as mock_get:
            result = _cached_main_character_name(request, user)

            self.assertEqual(result, "Cached Character")
            mock_get.assert_not_called()

    @patch("afat.helper.views.get_main_character_name_from_user")
    def test_fetches_and_caches_name_if_not_present(self, mock_get):
        """
        Test that the function fetches and caches the name if not present.

        :param mock_get:
        :type mock_get:
        :return:
        :rtype:
        """

        request = MagicMock()
        request._afat_cache = {"main_char_names": {}}
        user = MagicMock(pk=2)
        mock_get.return_value = "New Character"

        result = _cached_main_character_name(request, user)

        self.assertEqual(result, "New Character")
        self.assertEqual(request._afat_cache["main_char_names"][2], "New Character")
        mock_get.assert_called_once_with(user=user)

    @patch("afat.helper.views.get_main_character_name_from_user")
    def test_handles_user_without_pk(self, mock_get):
        """
        Test that the function handles users without a primary key.

        :param mock_get:
        :type mock_get:
        :return:
        :rtype:
        """

        request = MagicMock()
        request._afat_cache = {"main_char_names": {}}
        user = MagicMock(pk=None)
        mock_get.return_value = "Anonymous"

        result = _cached_main_character_name(request, user)

        self.assertEqual(result, "Anonymous")
        self.assertIn(None, request._afat_cache["main_char_names"])
        self.assertEqual(request._afat_cache["main_char_names"][None], "Anonymous")


class TestHelperPermFlags(BaseTestCase):
    """
    Test _perm_flags function
    """

    def test_returns_cached_flags_if_present(self):
        """
        Test that the function returns the cached flags if present.

        :return:
        :rtype:
        """

        request = MagicMock()
        request._afat_cache = {"perm_flags": {"manage": True, "add": False}}

        result = _perm_flags(request)

        self.assertEqual(result, {"manage": True, "add": False})

    def test_fetches_and_caches_flags_if_not_present(self):
        """
        Test that the function fetches and caches the flags if not present.

        :return:
        :rtype:
        """

        request = MagicMock()
        request._afat_cache = {}
        user = MagicMock()
        user.has_perm.side_effect = lambda perm: perm == "afat.manage_afat"
        request.user = user

        result = _perm_flags(request)

        self.assertEqual(result, {"manage": True, "add": False})
        self.assertEqual(
            request._afat_cache["perm_flags"], {"manage": True, "add": False}
        )

    def test_handles_request_without_user(self):
        """
        Test that the function handles requests without a user.

        :return:
        :rtype:
        """

        request = MagicMock()
        request._afat_cache = {}
        request.user = None

        result = _perm_flags(request)

        self.assertEqual(result, {"manage": False, "add": False})
        self.assertEqual(
            request._afat_cache["perm_flags"], {"manage": False, "add": False}
        )


class TestHelperGetRequestCache(BaseTestCase):
    """
    Test _get_request_cache function
    """

    def test_returns_existing_cache_if_present(self):
        """
        Test that the function returns the existing cache if present.

        :return:
        :rtype:
        """

        request = MagicMock()
        request._afat_cache = {"key": "value"}

        result = _get_request_cache(request)

        self.assertEqual(result, {"key": "value"})

    def test_creates_new_cache_if_not_present(self):
        """
        Test that the function creates a new cache if not present.

        :return:
        :rtype:
        """

        request = MagicMock()
        delattr(request, "_afat_cache")

        result = _get_request_cache(request)

        self.assertEqual(result, {})
        self.assertTrue(hasattr(request, "_afat_cache"))
        self.assertEqual(request._afat_cache, {})
