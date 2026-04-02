# Standard Library
from unittest.mock import MagicMock

# Django
from django.test import TestCase
from django.urls import reverse

# AA Killstats
from killstats.auth_hooks import KillstatsMenuItem, register_charlink_hook
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import create_user_from_evecharacter_with_access


class TestAuthHooks(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()

        cls.user, cls.character_ownership = create_user_from_evecharacter_with_access(
            character_id=1001, disconnect_signals=True
        )
        cls.html_menu = f"""
            <li class="d-flex flex-wrap m-2 p-2 pt-0 pb-0 mt-0 mb-0 me-0 pe-0">
                <i class="nav-link fas fa-star fa-fw fa-fw align-self-center me-3 active"></i>
                <a class="nav-link flex-fill align-self-center me-auto active" href="{reverse('killstats:index')}">
                    Killstats
                </a>
            </li>
        """

    def test_menu_hook(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("killstats:index"), follow=True
        )  # Follow redirects

        # Überprüfen, ob der Benutzer korrekt weitergeleitet wurde
        self.assertEqual(response.status_code, 200)

        # Überprüfen, ob das HTML-Menü enthalten ist
        self.assertContains(response, self.html_menu, html=True)

    def test_render_returns_empty_string_for_user_without_permission(self):
        # given
        killstats_menu_item = KillstatsMenuItem()
        mock_request = MagicMock()
        mock_request.user.has_perm.return_value = False

        # when
        result = killstats_menu_item.render(mock_request)
        # then
        self.assertEqual(
            result,
            "",
            "Expected render method to return an empty string for users without permission",
        )

    def test_register_charlink_hook(self):
        """
        Test that the register_charlink_hook function returns the expected value.

        This test calls the register_charlink_hook function and verifies that it returns
        the correct string indicating the charlink hook location.
        """
        # Test Action
        result = register_charlink_hook()

        # Expected Result
        self.assertEqual(result, "killstats.thirdparty.charlink_hook")
