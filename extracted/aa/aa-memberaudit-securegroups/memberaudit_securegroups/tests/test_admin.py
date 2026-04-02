# Django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import EveCorporationInfo

# Member Audit
from memberaudit.models import CharacterRole
from memberaudit.tests.testdata.load_entities import load_entities

# Memberaudit Securegroups
from memberaudit_securegroups.models import (
    CorporationRoleFilter,
    CorporationTitleFilter,
    TimeInCorporationFilter,
)


class TestCorporationRoleFilter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.corporation_2001 = EveCorporationInfo.objects.get(corporation_id=2001)
        cls.corporation_2101 = EveCorporationInfo.objects.get(corporation_id=2101)
        cls.user = User.objects.create(
            username="superman", is_staff=True, is_superuser=True
        )
        cls.admin_add_url = reverse(
            "admin:memberaudit_securegroups_corporationrolefilter_add"
        )

    def test_should_create_new_filter(self):
        # given
        self.client.force_login(self.user)
        data = {
            "description": "dummy",
            "role": CharacterRole.Role.DIRECTOR,
            "corporations": f"{self.corporation_2001.id}",
        }
        # when
        response = self.client.post(self.admin_add_url, data)
        # then
        self.assertEqual(response.status_code, 302)
        obj = CorporationRoleFilter.objects.first()
        self.assertEqual(obj.role, CharacterRole.Role.DIRECTOR)
        self.assertEqual(
            {2001}, set(obj.corporations.values_list("corporation_id", flat=True))
        )

    def test_should_not_allow_creating_filter_without_defining_at_least_one_corporation(
        self,
    ):
        # given
        self.client.force_login(self.user)
        data = {"description": "dummy", "role": CharacterRole.Role.DIRECTOR}
        # when
        response = self.client.post(self.admin_add_url, data)
        # then
        self.assertEqual(response.status_code, 200)


class TestCorporationTitleFilter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.corporation_2001 = EveCorporationInfo.objects.get(corporation_id=2001)
        cls.corporation_2101 = EveCorporationInfo.objects.get(corporation_id=2101)
        cls.user = User.objects.create(
            username="superman", is_staff=True, is_superuser=True
        )
        cls.admin_add_url = reverse(
            "admin:memberaudit_securegroups_corporationtitlefilter_add"
        )

    def test_should_create_new_filter(self):
        # given
        self.client.force_login(self.user)
        data = {
            "description": "dummy",
            "title": "Alpha",
            "corporations": f"{self.corporation_2001.id}",
        }
        # when
        response = self.client.post(self.admin_add_url, data)
        # then
        self.assertEqual(response.status_code, 302)
        obj = CorporationTitleFilter.objects.first()
        self.assertEqual(obj.title, "Alpha")
        self.assertEqual(
            {2001}, set(obj.corporations.values_list("corporation_id", flat=True))
        )

    def test_should_not_allow_creating_filter_without_defining_at_least_one_corporation(
        self,
    ):
        # given
        self.client.force_login(self.user)
        data = {"description": "dummy", "title": "Alpha"}
        # when
        response = self.client.post(self.admin_add_url, data)
        # then
        self.assertEqual(response.status_code, 200)


class TestTimeInCorpFilter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create(
            username="superman", is_staff=True, is_superuser=True
        )
        cls.admin_add_url = reverse(
            "admin:memberaudit_securegroups_timeincorporationfilter_add"
        )

    def test_should_create_new_filter(self):
        # given
        self.client.force_login(self.user)
        data = {
            "description": "dummy",
            "minimum_days": 45,
        }
        # when
        response = self.client.post(self.admin_add_url, data)
        # then
        self.assertEqual(response.status_code, 302)
        obj = TimeInCorporationFilter.objects.first()
        self.assertEqual(obj.minimum_days, 45)
