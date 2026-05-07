"""
Test fatlinks views
"""

# Standard Library
from datetime import datetime, timedelta
from http import HTTPStatus
from types import SimpleNamespace
from unittest.mock import ANY, MagicMock, Mock, patch

# Third Party
# Eve SDE
from eve_sde.models import ItemType, SolarSystem
from pytz import utc

# Django
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.db import IntegrityError
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.models import Duration, Fat, FatLink, Log
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import create_fake_user, create_user_from_evecharacter
from afat.views import fatlinks as fatlinks_module

MODULE_PATH = "afat.views.fatlinks"


class FatlinksViewTestCase(BaseTestCase):
    """
    Base test class for fatlinks views
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

        # Generate some FAT links and FATs
        cls.afat_link_april_1 = FatLink.objects.create(
            fleet="April Fleet 1",
            hash="1231",
            creator=cls.user_with_basic_access,
            character=cls.character_1001,
            created=datetime(year=2020, month=4, day=1, tzinfo=utc),
        )
        cls.afat_link_april_2 = FatLink.objects.create(
            fleet="April Fleet 2",
            hash="1232",
            creator=cls.user_with_basic_access,
            character=cls.character_1001,
            created=datetime(year=2020, month=4, day=15, tzinfo=utc),
        )
        cls.afat_link_september = FatLink.objects.create(
            fleet="September Fleet",
            hash="1233",
            creator=cls.user_with_basic_access,
            character=cls.character_1001,
            created=datetime(year=2020, month=9, day=1, tzinfo=utc),
        )
        cls.afat_link_september_no_fats = FatLink.objects.create(
            fleet="September Fleet 2",
            hash="1234",
            creator=cls.user_with_basic_access,
            character=cls.character_1001,
            created=datetime(year=2020, month=9, day=1, tzinfo=utc),
        )

        Fat.objects.create(
            character=cls.character_1101,
            fatlink=cls.afat_link_april_1,
            shiptype="Omen",
        )
        Fat.objects.create(
            character=cls.character_1001,
            fatlink=cls.afat_link_april_1,
            shiptype="Omen",
        )
        Fat.objects.create(
            character=cls.character_1002,
            fatlink=cls.afat_link_april_1,
            shiptype="Omen",
        )
        Fat.objects.create(
            character=cls.character_1003,
            fatlink=cls.afat_link_april_1,
            shiptype="Omen",
        )
        Fat.objects.create(
            character=cls.character_1004,
            fatlink=cls.afat_link_april_1,
            shiptype="Omen",
        )
        Fat.objects.create(
            character=cls.character_1005,
            fatlink=cls.afat_link_april_1,
            shiptype="Omen",
        )

        Fat.objects.create(
            character=cls.character_1001,
            fatlink=cls.afat_link_april_2,
            shiptype="Omen",
        )
        Fat.objects.create(
            character=cls.character_1004,
            fatlink=cls.afat_link_april_2,
            shiptype="Thorax",
        )
        Fat.objects.create(
            character=cls.character_1002,
            fatlink=cls.afat_link_april_2,
            shiptype="Thorax",
        )
        Fat.objects.create(
            character=cls.character_1003,
            fatlink=cls.afat_link_april_2,
            shiptype="Omen",
        )

        Fat.objects.create(
            character=cls.character_1001,
            fatlink=cls.afat_link_september,
            shiptype="Omen",
        )
        Fat.objects.create(
            character=cls.character_1004,
            fatlink=cls.afat_link_september,
            shiptype="Guardian",
        )
        Fat.objects.create(
            character=cls.character_1002,
            fatlink=cls.afat_link_september,
            shiptype="Omen",
        )


class TestOverview(FatlinksViewTestCase):
    """
    Test overview
    """

    def test_should_show_fatlnks_overview(self):
        """
        Test should show fatlnks overview

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(viewname="afat:fatlinks_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_fatlnks_overview_with_year(self):
        """
        Test should show fatlnks overview with year

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(viewname="afat:fatlinks_overview", kwargs={"year": 2020})
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)


class TestAddFatlink(FatlinksViewTestCase):
    """
    Test add fatlink
    """

    def test_should_show_add_fatlink_for_user_with_manage_afat(self):
        """
        Test should show add fatlink for user with manage afat

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(viewname="afat:fatlinks_add_fatlink")
        res = self.client.get(url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_add_fatlink_for_user_with_add_fatlinkt(self):
        """
        Test should show add fatlink for user with add fatlinkt

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_add_fatlink)

        url = reverse(viewname="afat:fatlinks_add_fatlink")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_fatlink_details_for_user_with_manage_afat(self):
        """
        Test should show fatlink details for user with manage afat

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:fatlinks_details_fatlink",
            kwargs={"fatlink_hash": self.afat_link_april_1.hash},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)


class TestDetailsFatlink(FatlinksViewTestCase):
    """
    Test details fatlink
    """

    def test_should_show_fatlink_details_for_user_with_add_fatlinkt(self):
        """
        Test should show fatlink details for user with add fatlinkt

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_add_fatlink)

        url = reverse(
            viewname="afat:fatlinks_details_fatlink",
            kwargs={"fatlink_hash": self.afat_link_april_1.hash},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_fatlink_details_for_non_existing_fatlink(self):
        """
        Test should not show fatlink details for non existing fatlink

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:fatlinks_details_fatlink",
            kwargs={"fatlink_hash": "foobarsson"},
        )
        res = self.client.get(path=url)

        self.assertNotEqual(first=res.status_code, second=HTTPStatus.OK)
        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

        messages = list(get_messages(request=res.wsgi_request))

        self.assertRaises(expected_exception=FatLink.DoesNotExist)
        self.assertEqual(first=len(messages), second=1)
        self.assertEqual(
            first=str(messages[0]),
            second="<h4>Warning!</h4><p>The hash provided is not valid.</p>",
        )

    @patch("afat.views.fatlinks.FatLink.objects.select_related_default")
    @patch("afat.views.fatlinks.Duration.objects.get")
    @patch("afat.views.fatlinks.get_time_delta")
    def test_details_fatlink_renders_correctly_for_valid_fatlink(
        self, mock_get_time_delta, mock_get_duration, mock_select_related_default
    ):
        """
        Test details fatlink renders correctly for valid fatlink

        :param mock_get_time_delta:
        :type mock_get_time_delta:
        :param mock_get_duration:
        :type mock_get_duration:
        :param mock_select_related_default:
        :type mock_select_related_default:
        :return:
        :rtype:
        """

        mock_fatlink = Mock()
        mock_fatlink.is_esilink = False
        mock_fatlink.reopened = False
        mock_fatlink.created = timezone.now()
        mock_fatlink.fleet = "Test Fleet"
        mock_fatlink.hash = "valid_hash"
        mock_fatlink.is_registered_on_esi = False

        # Make select_related_default().get(...) return the mock fatlink
        mock_qs = Mock()
        mock_qs.get.return_value = mock_fatlink
        mock_select_related_default.return_value = mock_qs

        mock_duration = Mock()
        mock_duration.duration = 60
        mock_get_duration.return_value = mock_duration

        mock_get_time_delta.return_value = 10

        self.client.force_login(user=self.user_with_manage_afat)
        response = self.client.get(
            reverse(
                "afat:fatlinks_details_fatlink", kwargs={"fatlink_hash": "valid_hash"}
            )
        )

        # Ensure the patched path was used
        self.assertTrue(mock_select_related_default.called)
        mock_qs.get.assert_called_once_with(hash="valid_hash")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response, "afat/view/fatlinks/fatlinks-details-fatlink.html"
        )
        self.assertIn("link", response.context)
        self.assertTrue(response.context["link_ongoing"])
        self.assertTrue(response.context["manual_fat_can_be_added"])

    @patch("afat.views.fatlinks.FatLink.objects.select_related_default")
    @patch("afat.views.fatlinks.Duration.objects.get")
    def test_details_fatlink_handles_expired_fatlink(
        self, mock_get_duration, mock_select_related_default
    ):
        """
        Test details fatlink handles expired fatlink

        :param mock_get_duration:
        :type mock_get_duration:
        :param mock_select_related_default:
        :type mock_select_related_default:
        :return:
        :rtype:
        """

        mock_fatlink = Mock()
        mock_fatlink.is_esilink = False
        mock_fatlink.reopened = False
        mock_fatlink.created = timezone.now() - timedelta(days=2)

        # Make select_related_default().get(...) return the mock fatlink
        mock_qs = Mock()
        mock_qs.get.return_value = mock_fatlink
        mock_select_related_default.return_value = mock_qs

        mock_duration = Mock()
        mock_duration.duration = 60
        mock_get_duration.return_value = mock_duration

        self.client.force_login(self.user_with_add_fatlink)
        response = self.client.get(
            reverse("afat:fatlinks_details_fatlink", args=["expired_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context["link_ongoing"])
        self.assertFalse(response.context["manual_fat_can_be_added"])

    @patch("afat.views.fatlinks.FatLink.objects.select_related_default")
    @patch("afat.views.fatlinks.Duration.objects.get")
    def test_details_fatlink_allows_reopening_within_grace_period(
        self, mock_get_duration, mock_select_related_default
    ):
        """
        Test details fatlink allows reopening within grace period

        :param mock_get_duration:
        :type mock_get_duration:
        :param mock_select_related_default:
        :type mock_select_related_default:
        :return:
        :rtype:
        """

        mock_fatlink = Mock()
        mock_fatlink.is_esilink = False
        mock_fatlink.reopened = False
        mock_fatlink.created = timezone.now() - timedelta(hours=1)

        # Make select_related_default().get(...) return the mock fatlink
        mock_qs = Mock()
        mock_qs.get.return_value = mock_fatlink
        mock_select_related_default.return_value = mock_qs

        mock_duration = Mock()
        mock_duration.duration = 60
        mock_get_duration.return_value = mock_duration

        self.client.force_login(self.user_with_add_fatlink)
        response = self.client.get(
            reverse("afat:fatlinks_details_fatlink", args=["grace_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context["link_can_be_reopened"])


class TestProcessFatlinkNameChange(FatlinksViewTestCase):
    """
    Test process fatlink name change
    """

    def test_process_fatlink_name_change_updates_fleet_name(self):
        """
        Test process fatlink name change updates fleet name

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="testhash",
            fleet="Old Fleet Name",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        url = reverse("afat:fatlinks_process_fatlink_name_change", args=[fatlink.hash])
        form_data = {"fleet": "New Fleet Name"}

        response = self.client.post(url, data=form_data)

        fatlink.refresh_from_db()
        self.assertEqual(fatlink.fleet, "New Fleet Name")

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Fleet name successfully changed." in str(m) for m in messages)
        )

    def test_process_fatlink_name_change_invalid_form_shows_error(self):
        """
        Test process fatlink name change invalid form shows error

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="testhash",
            fleet="Old Fleet Name",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        url = reverse("afat:fatlinks_process_fatlink_name_change", args=[fatlink.hash])
        form_data = {"fleet": ""}  # Invalid form data

        response = self.client.post(url, data=form_data)

        fatlink.refresh_from_db()
        self.assertEqual(fatlink.fleet, "Old Fleet Name")

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Something went wrong!" in str(m) for m in messages))

    def test_process_fatlink_name_change_invalid_hash_redirects_with_warning(self):
        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse("afat:fatlinks_process_fatlink_name_change", args=["invalidhash"])
        form_data = {"fleet": "New Fleet Name"}

        response = self.client.post(url, data=form_data)

        self.assertRedirects(response, reverse("afat:dashboard"))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("The hash provided is not valid." in str(m) for m in messages)
        )


class TestProcessManualFat(FatlinksViewTestCase):
    """
    Test process manual fat addition
    """

    @patch("afat.views.fatlinks.ItemType.objects")
    @patch("afat.views.fatlinks.SolarSystem.objects.get")
    @patch("afat.views.fatlinks.get_or_create_character")
    def test_manual_fat_adds_new_character_successfully(
        self, mock_get_or_create_character, mock_solar_get, mock_item_objects
    ):
        """
        Test manual fat adds new character successfully

        :param mock_get_or_create_character:
        :type mock_get_or_create_character:
        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="testhash",
            fleet="Test Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        mock_character = self.character_1101
        mock_get_or_create_character.return_value = mock_character

        # Ensure SDE lookups in the view succeed for system and ship type
        # Return a real SolarSystem model instance instead of a MagicMock so
        # assigning to Fat.solar_system works during Fat.objects.create
        mock_solar_get.return_value = SolarSystem.objects.get_or_create(
            id=5000, defaults={"name": "Test System"}
        )[0]
        # Use a real ItemType instance so FK assignment to Fat.ship succeeds
        shiptype_instance = ItemType(id=7000, name="Test Ship", published=1)
        shiptype_instance.save()
        mock_item_objects.filter.return_value.get.return_value = shiptype_instance

        form_data = {
            "character": mock_character.character_name,
            "system": "Test System",
            "shiptype": "Test Ship",
        }
        url = reverse("afat:fatlinks_process_manual_fat", args=[fatlink.hash])

        response = self.client.post(url, data=form_data)

        self.assertTrue(
            Fat.objects.filter(fatlink=fatlink, character=mock_character).exists()
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                f"{mock_character.character_name} has been added flying a {form_data['shiptype']} in {form_data['system']}"
                in str(m)
                for m in messages
            )
        )

    @patch("afat.views.fatlinks.ItemType.objects")
    @patch("afat.views.fatlinks.SolarSystem.objects.get")
    @patch("afat.views.fatlinks.get_or_create_character")
    def test_manual_fat_character_already_registered_shows_info(
        self, mock_get_or_create_character, mock_solar_get, mock_item_objects
    ):
        """
        Test manual fat character already registered shows info

        :param mock_get_or_create_character:
        :type mock_get_or_create_character:
        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="testhash",
            fleet="Test Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        mock_character = self.character_1001
        mock_get_or_create_character.return_value = mock_character

        # Ensure SDE lookups succeed so the view reaches the duplicate branch
        mock_solar_get.return_value = SolarSystem.objects.get_or_create(
            id=5000, defaults={"name": "Test System"}
        )[0]
        # Use a real ItemType instance so FK assignment to Fat.ship succeeds
        shiptype_instance = ItemType(id=7000, name="Test Ship", published=1)
        shiptype_instance.save()
        mock_item_objects.filter.return_value.get.return_value = shiptype_instance

        Fat.objects.create(
            fatlink=fatlink,
            character=mock_character,
            system="Test System",
            shiptype="Test Ship",
        )

        form_data = {
            "character": mock_character.character_name,
            "system": "Test System",
            "shiptype": "Test Ship",
        }
        url = reverse("afat:fatlinks_process_manual_fat", args=[fatlink.hash])

        response = self.client.post(url, data=form_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                "Pilot is already registered for this FAT link." in str(m)
                for m in messages
            )
        )

    @patch("afat.views.fatlinks.get_or_create_character")
    def test_manual_fat_invalid_character_shows_error(
        self, mock_get_or_create_character
    ):
        """
        Test manual fat invalid character shows error

        :param mock_get_or_create_character:
        :type mock_get_or_create_character:
        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="testhash",
            fleet="Test Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        mock_get_or_create_character.return_value = None

        form_data = {
            "character": "Unknown Pilot",
            "system": "Test System",
            "shiptype": "Test Ship",
        }
        url = reverse("afat:fatlinks_process_manual_fat", args=[fatlink.hash])

        response = self.client.post(url, data=form_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                "The character name you entered was not found." in str(m)
                for m in messages
            )
        )

    def test_manual_fat_invalid_fatlink_hash_redirects_with_warning(self):
        """
        Test manual fat invalid fatlink hash redirects with warning

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse("afat:fatlinks_process_manual_fat", args=["invalidhash"])
        form_data = {
            "character": "Test Character",
            "system": "Test System",
            "shiptype": "Test Ship",
        }

        response = self.client.post(url, data=form_data)

        self.assertRedirects(response, reverse("afat:dashboard"))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("The hash provided is not valid." in str(m) for m in messages)
        )

    def test_manual_fat_shows_warning_when_system_not_found(self):
        """
        Test manual_fat shows warning when system is not found.

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="mf1",
            fleet="Manual Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        request = RequestFactory().post(
            path=reverse("afat:fatlinks_process_manual_fat", args=[fatlink.hash]),
            data={"character": "Some", "system": "NoSuchSystem", "shiptype": "Test"},
        )
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_manage_afat
        request._messages = FallbackStorage(request)

        with (
            patch(
                "afat.views.fatlinks.get_or_create_character",
                return_value=self.character_1001,
            ),
            patch(
                "afat.views.fatlinks.SolarSystem.objects.get",
                side_effect=fatlinks_module.SolarSystem.DoesNotExist,
            ),
        ):
            response = fatlinks_module.process_manual_fat.__wrapped__.__wrapped__(
                request, fatlink.hash
            )

        self.assertEqual(
            response.url,
            reverse(
                "afat:fatlinks_details_fatlink", kwargs={"fatlink_hash": fatlink.hash}
            ),
        )
        messages = list(get_messages(request))
        self.assertTrue(
            any(
                "The system name you entered cannot be found" in str(m)
                for m in messages
            )
        )

    def test_manual_fat_shows_warning_when_shiptype_not_found(self):
        """
        Test manual_fat shows warning when shiptype is not found.

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="mf2",
            fleet="Manual Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        request = RequestFactory().post(
            path=reverse("afat:fatlinks_process_manual_fat", args=[fatlink.hash]),
            data={
                "character": "Some",
                "system": "Test System",
                "shiptype": "NoSuchShip",
            },
        )
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_manage_afat
        request._messages = FallbackStorage(request)

        # SolarSystem exists, ItemType lookup raises DoesNotExist
        with (
            patch(
                "afat.views.fatlinks.get_or_create_character",
                return_value=self.character_1001,
            ),
            patch(
                "afat.views.fatlinks.SolarSystem.objects.get",
                return_value=SolarSystem.objects.get_or_create(
                    id=5000, defaults={"name": "Test System"}
                )[0],
            ),
            patch("afat.views.fatlinks.ItemType.objects") as mock_item_objects,
        ):
            mock_item_objects.filter.return_value.get.side_effect = (
                fatlinks_module.ItemType.DoesNotExist
            )
            response = fatlinks_module.process_manual_fat.__wrapped__.__wrapped__(
                request, fatlink.hash
            )

        self.assertEqual(
            response.url,
            reverse(
                "afat:fatlinks_details_fatlink", kwargs={"fatlink_hash": fatlink.hash}
            ),
        )
        messages = list(get_messages(request))
        self.assertTrue(
            any("The ship type you entered cannot be found" in str(m) for m in messages)
        )


class TestReopenFatlink(FatlinksViewTestCase):
    """
    Test reopen fatlink
    """

    @patch("afat.views.fatlinks.Duration.objects.get")
    @patch("afat.views.fatlinks.Setting.get_setting")
    @patch("afat.views.fatlinks.write_log")
    def test_reopens_fatlink_successfully(
        self, mock_write_log, mock_get_setting, mock_duration_get
    ):
        """
        Test reopens fatlink successfully

        :param mock_write_log:
        :type mock_write_log:
        :param mock_get_setting:
        :type mock_get_setting:
        :param mock_duration_get:
        :type mock_duration_get:
        :return:
        :rtype:
        """

        mock_duration = MagicMock()
        mock_duration.fleet.reopened = False
        mock_duration.fleet.created = datetime(2023, 1, 1, 12, 0, 0)
        mock_duration.fleet.hash = "test_hash"
        mock_get_setting.return_value = 60
        mock_duration_get.return_value = mock_duration

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_reopen_fatlink", args=["test_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse(
                "afat:fatlinks_details_fatlink", kwargs={"fatlink_hash": "test_hash"}
            ),
            target_status_code=HTTPStatus.FOUND,
        )
        mock_duration.save.assert_called_once()
        mock_write_log.assert_called_once()

    @patch("afat.views.fatlinks.Duration.objects.get")
    def test_shows_error_when_fatlink_does_not_exist(self, mock_duration_get):
        """
        Test shows error when fatlink does not exist

        :param mock_duration_get:
        :type mock_duration_get:
        :return:
        :rtype:
        """

        mock_duration_get.side_effect = Duration.DoesNotExist

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_reopen_fatlink", args=["invalid_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("afat:dashboard"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                "The hash you provided does not match with any FAT link." in str(m)
                for m in messages
            )
        )

    @patch("afat.views.fatlinks.Duration.objects.get")
    def test_shows_warning_when_fatlink_already_reopened(self, mock_duration_get):
        """
        Test shows warning when fatlink already reopened

        :param mock_duration_get:
        :type mock_duration_get:
        :return:
        :rtype:
        """

        mock_duration = MagicMock()
        mock_duration.fleet.reopened = True
        mock_duration_get.return_value = mock_duration

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.post(
            reverse("afat:fatlinks_reopen_fatlink", args=["test_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse(
                "afat:fatlinks_details_fatlink",
                kwargs={"fatlink_hash": "test_hash"},
            ),
            target_status_code=HTTPStatus.FOUND,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("This FAT link has already been re-opened." in str(m) for m in messages)
        )


class TestCloseEsiFatlink(FatlinksViewTestCase):
    """
    Test close esi fatlink
    """

    @patch("afat.views.fatlinks.FatLink.objects.get")
    def test_closes_esi_fatlink_successfully(self, mock_get_fatlink):
        """
        Test closes esi fatlink successfully

        :param mock_get_fatlink:
        :type mock_get_fatlink:
        :return:
        :rtype:
        """

        mock_fatlink = MagicMock()
        mock_get_fatlink.return_value = mock_fatlink

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_close_esi_fatlink", args=["test_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("afat:dashboard"))
        mock_fatlink.save.assert_called_once()
        self.assertFalse(mock_fatlink.is_registered_on_esi)

    @patch("afat.views.fatlinks.FatLink.objects.get")
    def test_handles_nonexistent_fatlink_gracefully(self, mock_get_fatlink):
        """
        Test handles nonexistent fatlink gracefully

        :param mock_get_fatlink:
        :type mock_get_fatlink:
        :return:
        :rtype:
        """

        mock_get_fatlink.side_effect = FatLink.DoesNotExist

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_close_esi_fatlink", args=["nonexistent_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("afat:dashboard"))


class TestDeleteFat(FatlinksViewTestCase):
    """
    Test delete fat
    """

    @patch("afat.views.fatlinks.FatLink.objects.get")
    @patch("afat.views.fatlinks.Fat.objects.get")
    @patch("afat.views.fatlinks.write_log")
    def test_deletes_fat_successfully(
        self, mock_write_log, mock_get_fat, mock_get_fatlink
    ):
        """
        Test deletes fat successfully

        :param mock_write_log:
        :type mock_write_log:
        :param mock_get_fat:
        :type mock_get_fat:
        :param mock_get_fatlink:
        :type mock_get_fatlink:
        :return:
        :rtype:
        """

        mock_fatlink = MagicMock(hash="test_hash")
        mock_fat = MagicMock(character=MagicMock(character_name="Test Character"))
        mock_get_fatlink.return_value = mock_fatlink
        mock_get_fat.return_value = mock_fat

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_delete_fat", args=["test_hash", 1])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse("afat:fatlinks_details_fatlink", args=["test_hash"]),
            target_status_code=HTTPStatus.FOUND,
        )
        mock_fat.delete.assert_called_once()
        mock_write_log.assert_called_once_with(
            request=ANY,
            log_event=Log.Event.DELETE_FAT,
            log_text="The FAT for Test Character has been deleted",
            fatlink_hash="test_hash",
        )

    @patch("afat.views.fatlinks.FatLink.objects.get")
    def test_handles_delete_fat_with_nonexistent_fatlink_gracefully(
        self, mock_get_fatlink
    ):
        """
        Test handles delete fat with nonexistent fatlink gracefully

        :param mock_get_fatlink:
        :type mock_get_fatlink:
        :return:
        :rtype:
        """

        mock_get_fatlink.side_effect = FatLink.DoesNotExist

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_delete_fat", args=["invalid_hash", 1])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("afat:dashboard"))

    @patch("afat.views.fatlinks.FatLink.objects.get")
    @patch("afat.views.fatlinks.Fat.objects.get")
    def test_handles_nonexistent_fat_gracefully(self, mock_get_fat, mock_get_fatlink):
        """
        Test handles nonexistent fat gracefully

        :param mock_get_fat:
        :type mock_get_fat:
        :param mock_get_fatlink:
        :type mock_get_fatlink:
        :return:
        :rtype:
        """

        mock_fatlink = MagicMock(hash="test_hash")
        mock_get_fatlink.return_value = mock_fatlink
        mock_get_fat.side_effect = Fat.DoesNotExist

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_delete_fat", args=["test_hash", 999])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("afat:dashboard"))

    @patch("afat.views.fatlinks.FatLink.objects.get")
    @patch("afat.views.fatlinks.Fat.objects.filter")
    @patch("afat.views.fatlinks.write_log")
    def test_deletes_fatlink_and_associated_fats_successfully(
        self, mock_write_log, mock_fat_filter, mock_fatlink_get
    ):
        """
        Test deletes fatlink and associated fats successfully

        :param mock_write_log:
        :type mock_write_log:
        :param mock_fat_filter:
        :type mock_fat_filter:
        :param mock_fatlink_get:
        :type mock_fatlink_get:
        :return:
        :rtype:
        """

        mock_fatlink = MagicMock(hash="test_hash", pk=1)
        mock_fat_filter.return_value = MagicMock(delete=MagicMock())
        mock_fatlink_get.return_value = mock_fatlink

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_delete_fatlink", args=["test_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("afat:fatlinks_overview"))
        mock_fat_filter.assert_called_once_with(fatlink_id=mock_fatlink.pk)
        mock_fat_filter.return_value.delete.assert_called_once()
        mock_fatlink.delete.assert_called_once()
        mock_write_log.assert_called_once_with(
            ANY,  # Allow any request object
            log_event=Log.Event.DELETE_FATLINK,
            log_text="FAT link deleted.",
            fatlink_hash="test_hash",
        )

    @patch("afat.views.fatlinks.FatLink.objects.get")
    def test_handles_delete_fatlink_with_nonexistent_fatlink_gracefully(
        self, mock_fatlink_get
    ):
        """
        Test handles delete fatlink with nonexistent fatlink gracefully

        :param mock_fatlink_get:
        :type mock_fatlink_get:
        :return:
        :rtype:
        """

        mock_fatlink_get.side_effect = FatLink.DoesNotExist

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_delete_fatlink", args=["invalid_hash"])
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("afat:dashboard"))


class TestAjaxGetFatsByFatlink(FatlinksViewTestCase):
    """
    Test ajax get fats by fatlink
    """

    @patch("afat.views.fatlinks.Fat.objects.select_related_default")
    @patch("afat.views.fatlinks.convert_fats_to_dict")
    def test_returns_fats_for_valid_fatlink_hash(
        self, mock_convert_fats_to_dict, mock_select_related_default
    ):
        """
        Test returns fats for valid fatlink hash

        :param mock_convert_fats_to_dict:
        :type mock_convert_fats_to_dict:
        :param mock_select_related_default:
        :type mock_select_related_default:
        :return:
        :rtype:
        """

        # Create a mock Fat object with realistic attributes
        class MockFat:
            id = 1
            shiptype = "Omen"
            system = "Jita"

            class Character:
                character_name = "Test Character"

            character = Character()

            class FatLink:
                is_esilink = True
                is_registered_on_esi = True
                hash = "test_hash"
                created = datetime(2020, 4, 1, tzinfo=utc)
                fleet = "Test Fleet"
                doctrine = "Test Doctrine"
                fleet_type = "Test Fleet Type"

            fatlink = FatLink()

        mock_fat = MockFat()

        # Mock the queryset returned by select_related_default
        mock_queryset = MagicMock()
        mock_queryset.filter.return_value = [mock_fat]
        mock_select_related_default.return_value = mock_queryset

        # Mock the convert_fats_to_dict function to return a JSON-serializable dictionary
        mock_convert_fats_to_dict.return_value = {
            "id": mock_fat.id,
            "character": mock_fat.character.character_name,
            "shiptype": mock_fat.shiptype,
        }

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(
            reverse("afat:fatlinks_ajax_get_fats_by_fatlink", args=["1231"])
        )

        # Assertions
        self.assertEqual(response.status_code, HTTPStatus.OK)
        mock_select_related_default.return_value.filter.assert_called_once_with(
            fatlink__hash="1231"
        )
        mock_convert_fats_to_dict.assert_called_once_with(request=ANY, fat=mock_fat)
        self.assertEqual(
            response.json(),
            [{"id": 1, "character": "Test Character", "shiptype": "Omen"}],
        )


class TestCreateClickableFatlink(FatlinksViewTestCase):
    """
    Test create clickable fatlink
    """

    @patch("afat.views.fatlinks.get_hash_on_save", return_value="created_testhash")
    @patch("afat.views.fatlinks.AFatClickFatForm")
    def test_should_create_clickable_fatlink_when_form_is_valid(
        self, mock_form, mock_get_hash
    ):
        """
        Test should create clickable fatlink when form is valid

        :param mock_form:
        :type mock_form:
        :param mock_get_hash:
        :type mock_get_hash:
        :return:
        :rtype:
        """

        mock_form.return_value.is_valid.return_value = True
        mock_form.return_value.cleaned_data = {
            "name": "Test Fleet",
            "type": "PvP",
            "doctrine": "Test Doctrine",
            "duration": 60,
        }
        testhash = "created_testhash"

        # Create a real initial FatLink and Duration so descriptor checks pass
        initial_fatlink = FatLink.objects.create(
            fleet="Initial Fleet",
            creator=self.user_with_basic_access,
            character=self.character_1001,
        )
        Duration.objects.create(fleet=initial_fatlink, duration=30)

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.post(reverse("afat:fatlinks_create_clickable_fatlink"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        created = FatLink.objects.get(hash=testhash)
        self.assertIsNotNone(created)
        expected_url = reverse(
            "afat:fatlinks_details_fatlink", kwargs={"fatlink_hash": testhash}
        )
        self.assertEqual(response.url, expected_url)

        # The view creates a new Duration for the created FatLink with the requested duration
        created_duration = Duration.objects.filter(fleet=created, duration=60).first()
        self.assertIsNotNone(created_duration)

    @patch("afat.views.fatlinks.AFatClickFatForm")
    def test_should_redirect_to_add_fatlink_when_form_is_invalid(self, mock_form):
        """
        Test should redirect to add fatlink when form is invalid

        :param mock_form:
        :type mock_form:
        :return:
        :rtype:

        """
        mock_form.return_value.is_valid.return_value = False

        self.client.force_login(self.user_with_manage_afat)
        response = self.client.post(reverse("afat:fatlinks_create_clickable_fatlink"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("afat:fatlinks_add_fatlink"))

    def test_should_redirect_to_add_fatlink_when_request_method_is_not_post(self):
        self.client.force_login(self.user_with_manage_afat)
        response = self.client.get(reverse("afat:fatlinks_create_clickable_fatlink"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("afat:fatlinks_add_fatlink"))


class TestAddFatView(BaseTestCase):
    """
    Test add fat view
    """

    def setUp(self):
        """
        Set up test users and fatlink

        :return:
        :rtype:
        """

        self.user_with_basic_access = create_fake_user(
            character_id=2001,
            character_name="Basic Access User",
            permissions=["afat.basic_access"],
            corporation_id=300,
            corporation_name="Basic Corp",
            corporation_ticker="BASIC",
            alliance_id=400,
            alliance_name="Basic Alliance",
            alliance_ticker="BASIC",
        )
        self.user_fatlinik_creator = create_fake_user(
            character_id=2000,
            character_name="Fatlink Creator User",
            permissions=["afat.add_fatlink"],
            corporation_id=301,
            corporation_name="Creator Corp",
            corporation_ticker="CREAT",
            alliance_id=401,
            alliance_name="Creator Alliance",
            alliance_ticker="CREAT",
        )

        # Provide a non-null fleet name and a creator to avoid IntegrityError
        self.fatlink = FatLink.objects.create(
            hash="valid_hash",
            is_esilink=False,
            created=now(),
            fleet="Test Fleet",
            creator=self.user_fatlinik_creator,
        )

        Duration.objects.create(fleet=self.fatlink, duration=60)
        self.url = reverse("afat:fatlinks_add_fat", args=["valid_hash"])
        # Ensure SDE objects exist for tests that expect real model instances
        SolarSystem.objects.get_or_create(id=5000, defaults={"name": "Test System"})
        ItemType.objects.get_or_create(
            id=6000, defaults={"name": "Test Ship", "published": 1}
        )

    @patch("afat.views.fatlinks.esi_handler.result")
    def test_redirects_to_dashboard_if_fatlink_does_not_exist(self, mock_esi_result):
        """
        Test redirects to dashboard if fatlink does not exist

        :param mock_esi_result:
        :type mock_esi_result:
        :return:
        :rtype:
        """

        # Build request for an invalid hash and attach session/messages/user
        url = reverse("afat:fatlinks_add_fat", args=["invalid_hash"])
        request = RequestFactory().get(path=url)
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_basic_access
        request._messages = FallbackStorage(request)

        # Dummy token (not used because fatlink lookup fails first)
        token_mock = MagicMock()

        # Call the underlying unwrapped view to bypass decorators
        response = fatlinks_module.add_fat.__wrapped__.__wrapped__.__wrapped__(
            request, token_mock, "invalid_hash"
        )

        # Assert redirect to dashboard and warning message added
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("afat:dashboard"))

    @patch("afat.views.fatlinks.esi_handler.result")
    def test_redirects_to_dashboard_if_fatlink_is_expired(self, mock_esi_result):
        """
        Test redirects to dashboard if fatlink is expired

        :param mock_esi_result:
        :type mock_esi_result:
        :return:
        :rtype:
        """

        # Make the fatlink expired
        self.fatlink.created = timezone.now() - timedelta(minutes=120)
        self.fatlink.save()

        url = reverse("afat:fatlinks_add_fat", args=[self.fatlink.hash])
        request = RequestFactory().get(path=url)

        # Attach session and messages
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_basic_access
        request._messages = FallbackStorage(request)

        # Dummy token (expiry check runs before token usage)
        token_mock = MagicMock()

        # Call the underlying unwrapped view to bypass decorators
        response = fatlinks_module.add_fat.__wrapped__.__wrapped__.__wrapped__(
            request, token_mock, self.fatlink.hash
        )

        # Assert redirect to dashboard and warning message added
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("afat:dashboard"))

    @patch("afat.views.fatlinks.esi_handler.result")
    @patch("afat.views.fatlinks.EveCharacter.objects.get")
    def test_redirects_to_dashboard_if_character_is_offline(
        self, mock_eve_get, mock_esi_result
    ):
        """
        Test redirects to dashboard if character is offline

        :param mock_eve_get:
        :type mock_eve_get:
        :param mock_esi_result:
        :type mock_esi_result:
        :return:
        :rtype:
        """

        # ESI reports the character as offline
        mock_esi_result.side_effect = [MagicMock(online=False)]

        # Ensure EveCharacter lookup returns a character-like object
        fake_character = MagicMock(character_name="Offline Char", character_id=12345)
        mock_eve_get.return_value = fake_character

        # Build RequestFactory request and attach session/messages/user
        url = reverse("afat:fatlinks_add_fat", args=[self.fatlink.hash])
        request = RequestFactory().get(path=url)
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_basic_access
        request._messages = FallbackStorage(request)

        # Create a token-like mock
        token_mock = MagicMock(character_id=fake_character.character_id)
        token_mock.is_valid.return_value = True
        token_mock.scopes = [
            "esi-location.read_location.v1",
            "esi-location.read_ship_type.v1",
            "esi-location.read_online.v1",
        ]

        # Build a tiny fake esi object that won't perform network calls when attributes are accessed
        fake_location_api = SimpleNamespace(
            GetCharactersCharacterIdOnline=lambda character_id, token: MagicMock()
        )
        fake_client = SimpleNamespace(Location=fake_location_api)
        fake_esi = SimpleNamespace(client=fake_client)

        # Patch the module-level esi to the fake object for the duration of the call
        with patch.object(fatlinks_module, "esi", fake_esi):
            response = fatlinks_module.add_fat.__wrapped__.__wrapped__.__wrapped__(
                request, token_mock, self.fatlink.hash
            )

        # Assert redirect to dashboard and warning message added
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("afat:dashboard"))

    @patch("afat.views.fatlinks.ItemType.objects.get")
    @patch("afat.views.fatlinks.SolarSystem.objects.get")
    @patch("afat.views.fatlinks.esi")
    @patch("afat.views.fatlinks.esi_handler.result")
    def test_creates_fat_and_redirects_on_success(
        self, mock_esi_result, mock_esi, mock_get_solar, mock_get_type
    ):
        """
        Test creates fat and redirects on success

        :param mock_esi_result:
        :type mock_esi_result:
        :param mock_esi:
        :type mock_esi:
        :param mock_get_solar:
        :type mock_get_solar:
        :param mock_get_type:
        :type mock_get_type:
        :return:
        :rtype:
        """

        # Prepare ESI responses: online, location, ship
        location_solar_system_id = 5000
        ship_type_id = 6000

        esi_online_resp = MagicMock(online=True)
        esi_location_resp = MagicMock(solar_system_id=location_solar_system_id)
        esi_ship_resp = MagicMock(ship_type_id=ship_type_id)

        mock_esi_result.side_effect = [
            esi_online_resp,
            esi_location_resp,
            esi_ship_resp,
        ]

        # Ensure the model lookups return real model instances so created Fat
        # objects can be assigned correctly.
        solar_system = SolarSystem.objects.get_or_create(
            id=location_solar_system_id, defaults={"name": "SolarSystemName"}
        )[0]
        mock_get_solar.return_value = solar_system

        ship = ItemType.objects.get_or_create(
            id=ship_type_id, defaults={"name": "ShipTypeName", "published": 1}
        )[0]
        mock_get_type.return_value = ship

        # Build request and attach session, messages and user
        url = self.url  # set in setUp
        request = RequestFactory().get(path=url)
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_basic_access
        request._messages = FallbackStorage(request)

        # Token for the user that will be registered
        # Use an existing EveCharacter from the test setup (created by create_fake_user)
        eve_char = EveCharacter.objects.get(character_id=2001)
        token_mock = MagicMock(character_id=eve_char.character_id)

        # Call the underlying unwrapped view to bypass decorators
        response = fatlinks_module.add_fat.__wrapped__.__wrapped__.__wrapped__(
            request, token_mock, self.fatlink.hash
        )

        # Response should redirect to dashboard
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("afat:dashboard"))

        # Ensure the model lookups were called with the expected IDs
        mock_get_solar.assert_called_once_with(id=location_solar_system_id)
        mock_get_type.assert_called_once_with(id=ship_type_id)

        # Verify a Fat was created for this fatlink and character
        created_fat = Fat.objects.filter(
            fatlink=self.fatlink, character__character_id=eve_char.character_id
        ).first()
        self.assertIsNotNone(created_fat)
        # The view sets the foreign keys; assert the FK relationships are set
        self.assertEqual(created_fat.solar_system, solar_system)
        self.assertEqual(created_fat.ship, ship)

        # Check that a success message was added
        messages = list(get_messages(request))
        self.assertTrue(
            any("Success" in str(m) or "FAT registered" in str(m) for m in messages)
        )

    @patch("afat.views.fatlinks.ItemType.objects.get")
    @patch("afat.views.fatlinks.SolarSystem.objects.get")
    @patch("afat.views.fatlinks.Fat.objects.create")
    @patch("afat.views.fatlinks.EveCharacter.objects.get")
    @patch("afat.views.fatlinks.esi")
    @patch("afat.views.fatlinks.esi_handler.result")
    def test_does_not_create_duplicate_fat(
        self,
        mock_esi_result,
        mock_esi,
        mock_eve_get,
        mock_fat_create,
        mock_get_solar,
        mock_get_type,
    ):
        """
        Test does not create duplicate fat

        :param mock_esi_result:
        :type mock_esi_result:
        :param mock_esi:
        :type mock_esi:
        :param mock_eve_get:
        :type mock_eve_get:
        :param mock_fat_create:
        :type mock_fat_create:
        :param mock_get_solar:
        :type mock_get_solar:
        :param mock_get_type:
        :type mock_get_type:
        :return:
        :rtype:
        """

        # Prepare ESI responses: online, location, ship
        location_solar_system_id = 5000
        ship_type_id = 6000

        esi_online_resp = MagicMock(online=True)
        esi_location_resp = MagicMock(solar_system_id=location_solar_system_id)
        esi_ship_resp = MagicMock(ship_type_id=ship_type_id)

        mock_esi_result.side_effect = [
            esi_online_resp,
            esi_location_resp,
            esi_ship_resp,
        ]

        # Ensure the model lookups return single model-like instances (not tuples)
        solar_mock = MagicMock()
        solar_mock.name = "SolarSystemName"
        mock_get_solar.return_value = solar_mock

        shiptype_mock = MagicMock()
        shiptype_mock.name = "ShipTypeName"
        mock_get_type.return_value = shiptype_mock

        # Simulate duplicate creation raising IntegrityError
        mock_fat_create.side_effect = IntegrityError

        # Ensure EveCharacter lookup returns a character-like object
        fake_character = MagicMock(
            character_name="Dup User",
            character_id=2001,
            corporation_id=300,
            alliance_id=400,
        )
        mock_eve_get.return_value = fake_character

        # Build request and attach session, messages and user
        url = self.url  # set in setUp
        request = RequestFactory().get(path=url)
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_basic_access
        request._messages = FallbackStorage(request)

        # Token for the user that will be registered
        token_mock = MagicMock(character_id=fake_character.character_id)

        # Call the underlying unwrapped view to bypass decorators
        response = fatlinks_module.add_fat.__wrapped__.__wrapped__.__wrapped__(
            request, token_mock, self.fatlink.hash
        )

        # Response should redirect to dashboard
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("afat:dashboard"))

        # Ensure the model lookups were called with the expected IDs
        mock_get_solar.assert_called_once_with(id=location_solar_system_id)
        mock_get_type.assert_called_once_with(id=ship_type_id)

        # Fat.create should have been attempted and raised IntegrityError
        self.assertTrue(mock_fat_create.called)

        # Check that a warning about duplicate registration was added
        messages = list(get_messages(request))
        self.assertTrue(any("already registered" in str(m) for m in messages))


class TestprocessFleetSnapshot(BaseTestCase):
    """
    Tests for process_fleetsnapshot
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

    def test_processes_valid_fleet_snapshot_creates_expected_fats(self):
        """
        Test processing valid fleet snapshot creates expected fats

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="snap1",
            fleet="Snapshot Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        raw = "Rounon Dax\tDO6H-Q\tMetamorphosis\tFrigate\tFleet Commander (Boss)\t5 - 5 - 5\t\t"

        # Ensure SDE lookups succeed for the system and ship class used in the
        # fleet snapshot so the view can resolve them to real model instances.
        SolarSystem.objects.get_or_create(
            id=5002, name_en="DO6H-Q", defaults={"name": "DO6H-Q"}
        )
        ItemType.objects.get_or_create(
            id=6002,
            name_en="Metamorphosis",
            defaults={"name": "Metamorphosis", "published": 1},
        )

        request = RequestFactory().post(
            path=reverse("afat:fatlinks_process_fleetsnapshot", args=[fatlink.hash]),
            data={"fleet_composition": raw},
        )
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_manage_afat
        request._messages = FallbackStorage(request)

        with (
            patch(
                "afat.views.fatlinks.get_or_create_character",
                return_value=self.character_1001,
            ),
            patch("afat.views.fatlinks.Fat.objects.bulk_create") as mock_bulk,
        ):
            response = fatlinks_module.process_fleetsnapshot.__wrapped__.__wrapped__(
                request, fatlink.hash
            )

        # bulk_create should be called once with one created Fat instance
        self.assertTrue(mock_bulk.called)
        objs = mock_bulk.call_args[1]["objs"]
        self.assertEqual(len(objs), 1)

        # Redirects to details view and adds a success message
        expected_url = reverse(
            "afat:fatlinks_details_fatlink", kwargs={"fatlink_hash": fatlink.hash}
        )
        self.assertEqual(response.url, expected_url)
        messages = list(get_messages(request))
        self.assertTrue(any("Fleet snapshot processed" in str(m) for m in messages))

    def test_skips_lines_when_character_not_found(self):
        """
        Test skips lines when character not found

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="snap2",
            fleet="Snapshot Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        raw = (
            "Known Pilot\tSYS\tClass\tType\tPos\t5 - 5 - 5\t\t\n"
            "Unknown Pilot\tSYS\tClass\tType\tPos\t5 - 5 - 5\t\t"
        )

        request = RequestFactory().post(
            path=reverse("afat:fatlinks_process_fleetsnapshot", args=[fatlink.hash]),
            data={"fleet_composition": raw},
        )
        # Ensure SDE lookups for the system and ship class used in this
        # snapshot are available so the view can resolve them.
        SolarSystem.objects.get_or_create(
            id=5003, name_en="SYS", defaults={"name": "SYS"}
        )
        ItemType.objects.get_or_create(
            id=6003, name_en="Class", defaults={"name": "Class", "published": 1}
        )
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_manage_afat
        request._messages = FallbackStorage(request)

        # First call returns a character, second returns None
        with (
            patch(
                "afat.views.fatlinks.get_or_create_character",
                side_effect=[self.character_1001, None],
            ),
            patch("afat.views.fatlinks.Fat.objects.bulk_create") as mock_bulk,
        ):
            fatlinks_module.process_fleetsnapshot.__wrapped__.__wrapped__(
                request, fatlink.hash
            )

        self.assertTrue(mock_bulk.called)
        objs = mock_bulk.call_args[1]["objs"]
        # Only one valid character line should result in one Fat to create
        self.assertEqual(len(objs), 1)

        messages = list(get_messages(request))
        self.assertTrue(any("Fleet snapshot processed" in str(m) for m in messages))

    def test_invalid_fleet_composition_shows_error_and_redirects(self):
        """
        Test invalid fleet composition shows error and redirects

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        fatlink = FatLink.objects.create(
            hash="snap3",
            fleet="Snapshot Fleet",
            creator=self.user_with_manage_afat,
            character=self.character_1001,
        )

        # This string should not match the expected fleet composition regex
        invalid_raw = "INVALID FLEET DATA THAT DOES NOT MATCH"

        request = RequestFactory().post(
            path=reverse("afat:fatlinks_process_fleetsnapshot", args=[fatlink.hash]),
            data={"fleet_composition": invalid_raw},
        )
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_manage_afat
        request._messages = FallbackStorage(request)

        with (
            patch("afat.views.fatlinks.get_or_create_character"),
            patch("afat.views.fatlinks.Fat.objects.bulk_create") as mock_bulk,
        ):
            response = fatlinks_module.process_fleetsnapshot.__wrapped__.__wrapped__(
                request, fatlink.hash
            )

        # bulk_create should not be called for invalid format
        self.assertFalse(mock_bulk.called)

        # Redirect to details view and error message present
        expected_url = reverse(
            "afat:fatlinks_details_fatlink", kwargs={"fatlink_hash": fatlink.hash}
        )
        self.assertEqual(response.url, expected_url)
        messages = list(get_messages(request))
        self.assertTrue(
            any(
                "Please make sure to paste the fleet composition here" in str(m)
                for m in messages
            )
        )

    def test_invalid_hash_redirects_to_dashboard_with_warning(self):
        """
        Test invalid hash redirects to dashboard with warning

        :return:
        :rtype:
        """

        request = RequestFactory().post(
            path=reverse("afat:fatlinks_process_fleetsnapshot", args=["nope"]),
            data={"fleet_composition": "x"},
        )
        SessionMiddleware(get_response=lambda req: None).process_request(request)
        request.session.save()
        request.user = self.user_with_manage_afat
        request._messages = FallbackStorage(request)

        # Patch FatLink.objects.get to raise DoesNotExist
        with patch(
            "afat.views.fatlinks.FatLink.objects.get", side_effect=FatLink.DoesNotExist
        ):
            response = fatlinks_module.process_fleetsnapshot.__wrapped__.__wrapped__(
                request, "nope"
            )

        self.assertEqual(response.url, reverse("afat:dashboard"))
        messages = list(get_messages(request))
        self.assertTrue(
            any("The hash provided is not valid" in str(m) for m in messages)
        )
