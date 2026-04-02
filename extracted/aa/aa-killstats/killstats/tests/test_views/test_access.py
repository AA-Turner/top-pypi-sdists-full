# Standard Library
from http import HTTPStatus
from unittest.mock import Mock, patch

# Django
from django.test import RequestFactory, TestCase
from django.urls import reverse

# AA Killstats
from killstats import views
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import create_user_from_evecharacter_with_access

MODULE_PATH = "killstats.views"


class TestViewKillstatsAccess(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_allianceauth()

        cls.factory = RequestFactory()

        cls.user, cls.character_ownership = create_user_from_evecharacter_with_access(
            1001
        )

    def test_view_killboard_index(self):
        """Test view Killstats index."""
        # given
        request = self.factory.get(reverse("killstats:index"))
        request.user = self.user
        # when
        response = views.killboard_index(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_corporation_view(self):
        """Test Corporation View."""
        # given
        request = self.factory.get(reverse("killstats:corporation", args=[2001]))
        request.user = self.user
        # when
        response = views.corporation_view(request, 2001)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_alliance_view(self):
        """Test Alliance View."""
        # given
        request = self.factory.get(reverse("killstats:alliance", args=[3001]))
        request.user = self.user
        # when
        response = views.alliance_view(request, 3001)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_corporation_admin_view(self):
        """Test Corporation Overview."""
        # given
        request = self.factory.get(reverse("killstats:corporation_admin"))
        request.user = self.user
        # when
        response = views.corporation_admin(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_alliance_admin_view(self):
        """Test Alliance Overview."""
        # given
        request = self.factory.get(reverse("killstats:alliance_admin"))
        request.user = self.user
        # when
        response = views.alliance_admin(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
