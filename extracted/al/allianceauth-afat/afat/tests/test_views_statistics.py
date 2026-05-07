# Standard Library
from datetime import datetime
from http import HTTPStatus

# Third Party
from eve_sde.models import ItemType
from pytz import utc

# Django
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.models import Fat, FatLink
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import (
    RequestStub,
    add_character_to_user,
    create_user_from_evecharacter,
)
from afat.views.statistics import _calculate_year_stats

MODULE_PATH = "afat.views.statistics"


def response_content_to_str(response) -> str:
    """
    Convert response content to string

    :param response:
    :type response:
    :return:
    :rtype:
    """

    return response.content.decode(response.charset)


class TestStatistics(BaseTestCase):
    """
    Test the statistics views
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

        add_character_to_user(
            user=cls.user_with_basic_access, character=cls.character_1101
        )

        cls.user_with_manage_afat, _ = create_user_from_evecharacter(
            character_id=cls.character_1003.character_id,
            permissions=["afat.basic_access", "afat.manage_afat"],
        )

        cls.user_with_stats_corporation_other, _ = create_user_from_evecharacter(
            character_id=cls.character_1004.character_id,
            permissions=["afat.basic_access", "afat.stats_corporation_other"],
        )

        cls.user_with_stats_corporation_own, _ = create_user_from_evecharacter(
            character_id=cls.character_1005.character_id,
            permissions=["afat.basic_access", "afat.stats_corporation_own"],
        )

        # Generate some FAT links and FATs
        afat_link_april_1 = FatLink.objects.create(
            fleet="April Fleet 1",
            hash="1231",
            creator=cls.user_with_basic_access,
            character=cls.character_1001,
            created=datetime(year=2020, month=4, day=1, tzinfo=utc),
        )
        afat_link_april_2 = FatLink.objects.create(
            fleet="April Fleet 2",
            hash="1232",
            creator=cls.user_with_basic_access,
            character=cls.character_1001,
            created=datetime(year=2020, month=4, day=15, tzinfo=utc),
        )
        afat_link_september = FatLink.objects.create(
            fleet="September Fleet",
            hash="1233",
            creator=cls.user_with_basic_access,
            character=cls.character_1001,
            created=datetime(year=2020, month=9, day=1, tzinfo=utc),
        )
        # Ensure SDE ItemType instances exist and assign them to the Fat.ship FK
        omen = ItemType.objects.get_or_create(
            id=7001, defaults={"name": "Omen", "published": 1}
        )[0]
        thorax = ItemType.objects.get_or_create(
            id=7002, defaults={"name": "Thorax", "published": 1}
        )[0]
        guardian = ItemType.objects.get_or_create(
            id=7003, defaults={"name": "Guardian", "published": 1}
        )[0]

        Fat.objects.create(
            character=cls.character_1101,
            fatlink=afat_link_april_1,
            shiptype="Omen",
            ship=omen,
        )
        Fat.objects.create(
            character=cls.character_1001,
            fatlink=afat_link_april_1,
            shiptype="Omen",
            ship=omen,
        )
        Fat.objects.create(
            character=cls.character_1002,
            fatlink=afat_link_april_1,
            shiptype="Omen",
            ship=omen,
        )
        Fat.objects.create(
            character=cls.character_1003,
            fatlink=afat_link_april_1,
            shiptype="Omen",
            ship=omen,
        )
        Fat.objects.create(
            character=cls.character_1004,
            fatlink=afat_link_april_1,
            shiptype="Omen",
            ship=omen,
        )
        Fat.objects.create(
            character=cls.character_1005,
            fatlink=afat_link_april_1,
            shiptype="Omen",
            ship=omen,
        )

        Fat.objects.create(
            character=cls.character_1101,
            fatlink=afat_link_april_2,
            shiptype="Omen",
            ship=omen,
        )
        Fat.objects.create(
            character=cls.character_1004,
            fatlink=afat_link_april_2,
            shiptype="Thorax",
            ship=thorax,
        )
        Fat.objects.create(
            character=cls.character_1002,
            fatlink=afat_link_april_2,
            shiptype="Thorax",
            ship=thorax,
        )
        Fat.objects.create(
            character=cls.character_1003,
            fatlink=afat_link_april_2,
            shiptype="Omen",
            ship=omen,
        )

        Fat.objects.create(
            character=cls.character_1001,
            fatlink=afat_link_september,
            shiptype="Omen",
            ship=omen,
        )
        Fat.objects.create(
            character=cls.character_1004,
            fatlink=afat_link_september,
            shiptype="Guardian",
            ship=guardian,
        )
        Fat.objects.create(
            character=cls.character_1005,
            fatlink=afat_link_september,
            shiptype="Omen",
            ship=omen,
        )

    def test_should_only_show_my_chars_and_only_those_with_fat_links(self):
        """
        Test that the overview page only shows the characters of the user that have FAT links.

        :return:
        :rtype:
        """

        result = _calculate_year_stats(
            request=RequestStub(user=self.user_with_basic_access), year=2020
        )

        self.assertDictEqual(
            d1=result,
            d2={
                "total": {4: 4},
                "characters": [
                    ("Clark Kent", {4: 2}, 1002),
                    ("Lex Luther", {4: 2}, 1101),
                ],
            },
        )

    def test_should_show_statistics_dashboard(self):
        """
        Test should show statistics dashboard

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(viewname="afat:statistics_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_statistics_dashboard_for_year(self):
        """
        Test should show statistics dashboard for year

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(viewname="afat:statistics_overview", kwargs={"year": 2020})
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_statistics_dashboard_for_user_with_stats_corporation_other(
        self,
    ):
        """
        Test should show statistics dashboard for user with stats_corporation_other

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(viewname="afat:statistics_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_statistics_dashboard_for_user_with_stats_corporation_own(self):
        """
        Test should show statistics dashboard for user with stats_corporation_own

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_own)

        url = reverse(viewname="afat:statistics_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_statistics_dashboard_for_user_without_access(self):
        """
        Test should not show statistics dashboard for user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_without_access)

        url = reverse(viewname="afat:statistics_overview")
        res = self.client.get(path=url)

        self.assertNotEqual(first=res.status_code, second=HTTPStatus.OK)
        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)
        self.assertEqual(
            first=res.url,
            second="/account/login/?next=/fleet-activity-tracking/statistics/",
        )

    def test_should_show_own_character_stats(self):
        """
        Test should show own character stats

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(
            viewname="afat:statistics_character",
            kwargs={
                "charid": self.user_with_basic_access.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_other_character_stats_for_user_with_stats_corporation_own(
        self,
    ):
        """
        Test should show other character stats for user with stats_corporation_own

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_own)

        url = reverse(
            viewname="afat:statistics_character",
            kwargs={
                "charid": self.user_with_basic_access.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_other_character_stats_for_user_with_stats_corporation_other(
        self,
    ):
        """
        Test should show other character stats for user with stats_corporation_other

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(
            viewname="afat:statistics_character",
            kwargs={
                "charid": self.user_with_basic_access.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_other_character_stats_for_user_with_manage_afat(self):
        """
        Test should show other character stats for user with manage_afat

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:statistics_character",
            kwargs={
                "charid": self.user_with_basic_access.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_other_character_stats_for_user(self):
        """
        Test should not show other character stats for user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(
            viewname="afat:statistics_character",
            kwargs={
                "charid": self.user_with_stats_corporation_other.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_should_show_own_corp_stats_for_user_with_stats_corporation_own(self):
        """
        Test should show own corp stats for user with stats_corporation_own

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_own)

        url = reverse(
            viewname="afat:statistics_corporation",
            kwargs={
                "corpid": self.user_with_stats_corporation_own.profile.main_character.corporation_id
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_other_corp_stats_for_user_with_stats_corporation_other(self):
        """
        Test should show other corp stats for user with stats_corporation_other

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(
            viewname="afat:statistics_corporation",
            kwargs={
                "corpid": self.user_with_basic_access.profile.main_character.corporation_id
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_other_corp_stats_for_user_with_manage_afat(self):
        """
        Test should show other corp stats for user with manage_afat

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:statistics_corporation",
            kwargs={
                "corpid": self.user_with_basic_access.profile.main_character.corporation_id
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_own_corp_stats_for_user(self):
        """
        Test should not show own corp stats for user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(
            viewname="afat:statistics_corporation",
            kwargs={
                "corpid": self.user_with_basic_access.profile.main_character.corporation_id
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_should_not_show_other_corp_stats_for_user(self):
        """
        Test should not show other corp stats for user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(
            viewname="afat:statistics_corporation",
            kwargs={
                "corpid": self.user_with_stats_corporation_other.profile.main_character.corporation_id
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_should_show_all_corp_stats_for_user_with_stats_corporation_other(self):
        """
        Test should show all corp stats for user with stats_corporation_other

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(
            viewname="afat:statistics_corporation",
            kwargs={"corpid": 2002, "year": 2020},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_all_corp_stats_with_month_for_user_with_stats_corporation_other(
        self,
    ):
        """
        Test should show all corp stats with month for user with stats_corporation_other

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(
            viewname="afat:statistics_corporation",
            kwargs={"corpid": 2002, "year": 2020, "month": 4},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_all_corp_stats_for_user_with_stats_corporation_own(self):
        """
        Test should not show all corp stats for user with stats_corporation_own

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_own)

        url = reverse(viewname="afat:statistics_corporation", kwargs={"corpid": 2002})
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)
        self.assertEqual(first=res.url, second="/fleet-activity-tracking/")

    def test_should_show_all_alliance_stats_with_for_user_with_stats_corporation_other(
        self,
    ):
        """
        Test should show all alliance stats for user with stats_corporation_other

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(
            viewname="afat:statistics_alliance",
            kwargs={"allianceid": 3001},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_all_alliance_stats_with_for_user_with_manage_afat(
        self,
    ):
        """
        Test should show all alliance stats for user with manage_afat

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:statistics_alliance",
            kwargs={"allianceid": 3001},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_all_alliance_stats_with_year_for_user_with_stats_corporation_other(
        self,
    ):
        """
        Test should show all alliance stats with year for user with stats_corporation_other

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(
            viewname="afat:statistics_alliance",
            kwargs={"allianceid": 3001, "year": 2020},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_all_alliance_stats_with_year_for_user_with_manage_afat(
        self,
    ):
        """
        Test should show all alliance stats with year for user with manage_afat

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:statistics_alliance",
            kwargs={"allianceid": 3001, "year": 2020},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_all_alliance_stats_with_month_for_user_with_stats_corporation_other(
        self,
    ):
        # given
        self.client.force_login(user=self.user_with_stats_corporation_other)

        # when
        url = reverse(
            viewname="afat:statistics_alliance",
            kwargs={"allianceid": 3001, "year": 2020, "month": 4},
        )
        res = self.client.get(path=url)

        # then
        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_all_alliance_stats_with_month_for_user_with_manage_afat(
        self,
    ):
        """
        Test should show all alliance stats with month for user with manage_afat

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:statistics_alliance",
            kwargs={"allianceid": 3001, "year": 2020, "month": 4},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_all_alliance_stats_for_user(
        self,
    ):
        """
        Test should not show all alliance stats for user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(
            viewname="afat:statistics_alliance",
            kwargs={"allianceid": 3001},
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_should_show_main_details_for_user_with_manage_perms(self):
        """
        Test that a user with the required permissions can access the view

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(
            viewname="afat:statistics_ajax_get_monthly_fats_for_main_character",
            kwargs={
                "corporation_id": self.user_with_basic_access.profile.main_character.corporation_id,
                "character_id": self.user_with_basic_access.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_main_details_for_user_with_corporation_other_perms(self):
        """
        Test that a user with the required permissions can access the view (corporation_other)

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_stats_corporation_other)

        url = reverse(
            viewname="afat:statistics_ajax_get_monthly_fats_for_main_character",
            kwargs={
                "corporation_id": self.user_with_basic_access.profile.main_character.corporation_id,
                "character_id": self.user_with_basic_access.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_main_details_for_user_without_perms(self):
        """
        Test that a user without the required permissions cannot access the view

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(
            viewname="afat:statistics_ajax_get_monthly_fats_for_main_character",
            kwargs={
                "corporation_id": self.user_with_basic_access.profile.main_character.corporation_id,
                "character_id": self.user_with_basic_access.profile.main_character.character_id,
                "year": 2020,
                "month": 4,
            },
        )
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)
        self.assertEqual(
            first=response_content_to_str(response=res),
            second="",
        )
