# Standard Library
from http import HTTPStatus

# Django
from django.urls import resolve, reverse

# AA Killstats
from killstats import views
from killstats.tests import AuthTestCase

MODULE_PATH = "killstats.views"


class TestViewKillstatsAccess(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_react_base_view(self):
        """Test React base view."""
        # Test Data
        request = self.factory.get(reverse("killstats:react_base"))
        request.user = self.user

        # Test Action
        response = views.react_base(request)

        # Expected Result
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_spa_catch_all_route_resolution(self):
        """Test that arbitrary client-side paths resolve to react_base."""
        # Test Data
        url = "/killstats/arbitrary/frontend/route/"

        # Test Action
        match = resolve(url)

        # Expected Result
        self.assertEqual(match.url_name, "react_base")

    def test_client_access_overview_and_spa(self):
        """Test client GET on overview and SPA routes returns 200 OK."""
        # Test Data
        self.client.force_login(self.user)

        # Test Action
        resp_corp_overview = self.client.get("/killstats/overview/corporations/")
        resp_alli_overview = self.client.get("/killstats/overview/alliances/")
        resp_root = self.client.get("/killstats/")

        # Expected Result
        self.assertEqual(resp_corp_overview.status_code, HTTPStatus.OK)
        self.assertEqual(resp_alli_overview.status_code, HTTPStatus.OK)
        self.assertEqual(resp_root.status_code, HTTPStatus.OK)

    def test_client_access_entity_routes(self):
        """Test client GET on corporation and alliance named routes returns 200 OK."""
        # Test Data
        self.client.force_login(self.user)
        corp_url = reverse("killstats:corporation", kwargs={"entity_id": 98000001})
        alli_url = reverse("killstats:alliance", kwargs={"entity_id": 99000001})

        # Test Action
        resp_corp = self.client.get(corp_url)
        resp_alli = self.client.get(alli_url)

        # Expected Result
        self.assertEqual(resp_corp.status_code, HTTPStatus.OK)
        self.assertEqual(resp_alli.status_code, HTTPStatus.OK)
