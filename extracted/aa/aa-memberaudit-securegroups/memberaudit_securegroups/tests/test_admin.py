from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from app_utils.testdata_factories import EveCorporationInfoFactory, UserFactory
from memberaudit.models import CharacterRole

from memberaudit_securegroups.models import (
    CorporationRoleFilter,
    CorporationTitleFilter,
    TimeInCorporationFilter,
)


class TestCorporationRoleFilter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.corporation = EveCorporationInfoFactory()
        cls.user = UserFactory(is_staff=True, is_superuser=True)
        cls.admin_add_url = reverse(
            "admin:memberaudit_securegroups_corporationrolefilter_add"
        )

    def test_should_create_new_filter(self):
        # given
        self.client.force_login(self.user)
        data = {
            "description": "dummy",
            "role": CharacterRole.Role.DIRECTOR,
            "corporations": f"{self.corporation.id}",
        }
        # when
        response = self.client.post(self.admin_add_url, data)
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        obj = CorporationRoleFilter.objects.first()
        self.assertEqual(obj.role, CharacterRole.Role.DIRECTOR)
        self.assertEqual(
            {self.corporation.corporation_id},
            set(obj.corporations.values_list("corporation_id", flat=True)),
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
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestCorporationTitleFilter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.corporation = EveCorporationInfoFactory()
        cls.user = UserFactory(is_staff=True, is_superuser=True)
        cls.admin_add_url = reverse(
            "admin:memberaudit_securegroups_corporationtitlefilter_add"
        )

    def test_should_create_new_filter(self):
        # given
        self.client.force_login(self.user)
        data = {
            "description": "dummy",
            "title": "Alpha",
            "corporations": f"{self.corporation.id}",
        }
        # when
        response = self.client.post(self.admin_add_url, data)
        # then
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        obj = CorporationTitleFilter.objects.first()
        self.assertEqual(obj.title, "Alpha")
        self.assertEqual(
            {self.corporation.corporation_id},
            set(obj.corporations.values_list("corporation_id", flat=True)),
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
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestTimeInCorpFilter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = UserFactory(is_staff=True, is_superuser=True)
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
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        obj = TimeInCorporationFilter.objects.first()
        self.assertEqual(obj.minimum_days, 45)
