"""
Test access to the AFAT module
"""

# Standard Library
from http import HTTPStatus

# Django
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import create_user_from_evecharacter

MODULE_PATH = "afat.views.statistics"


class TestAccesss(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        """
        Setup the test class

        :return:
        :rtype:
        """

        super().setUpClass()

        # given
        cls.character_1001 = EveCharacter.objects.get(character_id=1001)
        cls.character_1002 = EveCharacter.objects.get(character_id=1002)

        cls.user_without_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1001.character_id
        )

        cls.user_with_basic_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1002.character_id,
            permissions=["afat.basic_access"],
        )

    def test_should_show_afat_dashboard_for_user_with_basic_access(self):
        """
        Test should show afat dashboard for user with basic access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_with_basic_access)

        url = reverse(viewname="afat:dashboard")
        res = self.client.get(path=url)

        self.assertEqual(first=res.status_code, second=HTTPStatus.OK)

    def test_should_not_show_afat_dashboard_for_user_without_access(self):
        """
        Test should not show afat dashboard for user without access

        :return:
        :rtype:
        """

        self.client.force_login(user=self.user_without_access)

        url = reverse(viewname="afat:dashboard")
        res = self.client.get(path=url)

        self.assertNotEqual(first=res.status_code, second=HTTPStatus.OK)
        self.assertEqual(first=res.status_code, second=HTTPStatus.FOUND)
        self.assertEqual(
            first=res.url, second="/account/login/?next=/fleet-activity-tracking/"
        )
