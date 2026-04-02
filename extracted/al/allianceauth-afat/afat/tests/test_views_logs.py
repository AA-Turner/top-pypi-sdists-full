"""
Test logs view
"""

# Standard Library
from datetime import datetime
from http import HTTPStatus

# Third Party
from pytz import utc

# Django
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.models import FatLink
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import create_user_from_evecharacter

MODULE_PATH = "afat.views.logs"


class TestLogsView(BaseTestCase):
    """
    Test the logs view
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

        cls.user_with_log_view, _ = create_user_from_evecharacter(
            character_id=cls.character_1004.character_id,
            permissions=["afat.basic_access", "afat.log_view"],
        )

        # Generate some FAT links and FATs
        cls.afat_link_april_1 = FatLink.objects.create(
            fleet="April Fleet 1",
            hash="1231",
            creator=cls.user_with_manage_afat,
            character=cls.character_1001,
            created=datetime(year=2020, month=4, day=1, tzinfo=utc),
        )
        cls.afat_link_april_2 = FatLink.objects.create(
            fleet="April Fleet 2",
            hash="1232",
            creator=cls.user_with_manage_afat,
            character=cls.character_1001,
            created=datetime(year=2020, month=4, day=15, tzinfo=utc),
        )

    def test_should_not_show_log_view_for_user_without_access(self):
        """
        Test should not show log view for user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_without_access)

        url = reverse(viewname="afat:logs_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_should_not_show_log_view_for_user_with_basic_access(self):
        """
        Test should not show log view for user with basic access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(viewname="afat:logs_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)

    def test_should_show_log_view_for_user_with_manage_afat_permission(self):
        """
        Test should show log view for user with manage afat permission

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_manage_afat)

        url = reverse(viewname="afat:logs_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_show_log_view_for_user_with_log_view_permission(self):
        """
        Test should show log view for user with log view permission

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_log_view)

        url = reverse(viewname="afat:logs_overview")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)
