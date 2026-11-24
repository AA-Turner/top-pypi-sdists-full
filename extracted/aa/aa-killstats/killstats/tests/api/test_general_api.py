"""Unit tests for the general API endpoints (menu and user)."""

# Standard Library
from http import HTTPStatus

# Third Party
from ninja.testing import TestClient

# AA Killstats
from killstats.api import api
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import UserMainFactory


class TestGeneralApi(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = UserMainFactory(
            permissions__=["killstats.basic_access", "killstats.admin_access"]
        )

    def setUp(self):
        super().setUp()
        self.client = TestClient(api)

    def test_get_menu_should_return_links_with_the_contract_fields(self):
        # Test Action
        response = self.client.get("/menu/", user=self.user)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(set(data), {"left_links", "right_links"})
        for link in data["left_links"]:
            self.assertEqual(
                set(link),
                {"name", "link", "badge", "is_external", "has_errors"},
            )
            self.assertIsNone(link["badge"])
            self.assertFalse(link["has_errors"])
        self.assertEqual(data["right_links"], [])

    def test_get_menu_should_return_admin_links_with_admin_access(self):
        # Test Action
        response = self.client.get("/menu/", user=self.admin)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertTrue(all(link["is_external"] for link in data["right_links"]))
        self.assertEqual(len(data["right_links"]), 2)

    def test_get_user_should_return_is_admin_false_without_admin_access(self):
        # Test Action
        response = self.client.get("/user/", user=self.user)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(data["user_id"], self.user.id)
        self.assertFalse(data["is_admin"])

    def test_get_user_should_return_is_admin_true_with_admin_access(self):
        # Test Action
        response = self.client.get("/user/", user=self.admin)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json()["is_admin"])
