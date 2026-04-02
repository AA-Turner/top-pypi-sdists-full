# Standard Library
from http import HTTPStatus
from unittest.mock import Mock

# Django
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.models import Fat, FatLink
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import (
    add_character_to_user,
    create_user_from_evecharacter,
)
from afat.views.dashboard import overview

MODULE_PATH = "afat.views.dashboard"


def response_content_to_str(response) -> str:
    return response.content.decode(response.charset)


class TestDashboard(BaseTestCase):
    """
    Test the dashboard view
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

        cls.character_1001 = EveCharacter.objects.get(character_id=1001)
        cls.character_1002 = EveCharacter.objects.get(character_id=1002)
        cls.character_1101 = EveCharacter.objects.get(character_id=1101)

        cls.user, _ = create_user_from_evecharacter(
            character_id=cls.character_1001.character_id,
            permissions=["afat.basic_access"],
        )

        add_character_to_user(user=cls.user, character=cls.character_1101)

        create_user_from_evecharacter(character_id=cls.character_1002.character_id)

        cls.afat_link = FatLink.objects.create(
            fleet="Demo Fleet",
            hash="123",
            creator=cls.user,
            character=cls.character_1001,
        )

    def _page_overview_request(self, user):
        """
        Make a request to the overview page as the given user.

        :param user:
        :type user:
        :return:
        :rtype:
        """

        request = self.factory.get(path=reverse(viewname="afat:dashboard"))
        request.user = user

        middleware = SessionMiddleware(get_response=Mock())
        middleware.process_request(request=request)

        return overview(request)

    def test_should_only_show_my_chars_and_only_those_with_fat_links(self):
        """
        Test that the overview page only shows the characters of the user that have FAT links.

        :return:
        :rtype:
        """

        Fat.objects.create(character=self.character_1101, fatlink=self.afat_link)
        Fat.objects.create(character=self.character_1002, fatlink=self.afat_link)

        response = self._page_overview_request(user=self.user)

        content = response_content_to_str(response=response)

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertIn(
            member=f'<span class="d-block" id="afat-eve-character-id-{self.character_1101.character_id}">{self.character_1101.character_name}</span>',
            container=content,
        )
        self.assertNotIn(
            member=f'<span class="d-block" id="afat-eve-character-id-{self.character_1001.character_id}">{self.character_1001.character_name}</span>',
            container=content,
        )
        self.assertNotIn(
            member=f'<span class="d-block" id="afat-eve-character-id-{self.character_1002.character_id}">{self.character_1002.character_name}</span>',
            container=content,
        )

    def test_ajax_recent_get_fats_by_character_should_only_show_my_fatlinks(self):
        """
        Test that the ajax call only returns the FATs for the given character if the user has access to the character.

        :return:
        :rtype:
        """

        Fat.objects.create(character=self.character_1101, fatlink=self.afat_link)
        Fat.objects.create(character=self.character_1002, fatlink=self.afat_link)

        self.client.force_login(user=self.user)

        response_correct_char = self.client.get(
            path=reverse(
                viewname="afat:dashboard_ajax_get_recent_fats_by_character",
                kwargs={"charid": self.character_1101.character_id},
            )
        )

        response_wrong_char = self.client.get(
            path=reverse(
                viewname="afat:dashboard_ajax_get_recent_fats_by_character",
                kwargs={"charid": self.character_1002.character_id},
            )
        )

        self.assertEqual(first=response_correct_char.status_code, second=HTTPStatus.OK)
        self.assertNotEqual(first=response_correct_char.json(), second=[])

        self.assertEqual(first=response_wrong_char.status_code, second=HTTPStatus.OK)
        self.assertEqual(first=response_wrong_char.json(), second=[])
