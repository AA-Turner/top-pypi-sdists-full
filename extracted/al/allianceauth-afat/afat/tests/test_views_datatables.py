"""
Tests for DataTables views.
"""

# Django
from django.http import HttpRequest
from django.test import RequestFactory
from django.utils import timezone

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.models import FatLink, Log
from afat.tests import BaseTestCase
from afat.tests.fixtures.utils import create_user_from_evecharacter
from afat.views.datatables import FatLinksTableView, LogsTableView


class DataTableBaseTestCase(BaseTestCase):
    """
    Base test setup for DataTable tests.
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

        cls.user_without_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1001.character_id
        )

        cls.user_with_basic_access, _ = create_user_from_evecharacter(
            character_id=cls.character_1002.character_id,
            permissions=["afat.basic_access"],
        )

        cls.user_with_manage_afat, _ = create_user_from_evecharacter(
            character_id=cls.character_1003.character_id,
            permissions=["afat.manage_afat"],
        )

        cls.user_with_log_view, _ = create_user_from_evecharacter(
            character_id=cls.character_1004.character_id,
            permissions=["afat.log_view"],
        )

        cls.user_with_manage_and_log, _ = create_user_from_evecharacter(
            character_id=cls.character_1005.character_id,
            permissions=["afat.manage_afat", "afat.log_view"],
        )


class TestFatLinksTableView(DataTableBaseTestCase):
    """
    Tests for FatLinksTableView.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup the test class

        :return:
        :rtype:
        """

        super().setUpClass()

        # Setup some FAT links
        cls.fatlink1 = FatLink.objects.create(
            created="2023-03-15",
            fleet="Fleet Alpha",
            creator=cls.user_with_basic_access,
            hash="abc123",
        )
        cls.fatlink2 = FatLink.objects.create(
            created="2022-11-20",
            fleet="Fleet Beta",
            creator=cls.user_with_basic_access,
            hash="def456",
        )
        cls.fatlink3 = FatLink.objects.create(
            created="2023-07-05",
            fleet="Fleet Gamma",
            creator=cls.user_with_basic_access,
            hash="ghi789",
        )
        cls.fatlink_current_year1 = FatLink.objects.create(
            created=timezone.now(),
            fleet="Fleet Delta",
            creator=cls.user_with_basic_access,
            hash="jkl012",
        )
        cls.fatlink_current_year2 = FatLink.objects.create(
            created=timezone.now(),
            fleet="Fleet Epsilon",
            creator=cls.user_with_basic_access,
            hash="mno345",
        )

    def test_returns_correct_queryset_for_current_year(self):
        """
        Test returns correct queryset for current year

        :return:
        :rtype:
        """

        request = RequestFactory().get("/")
        view = FatLinksTableView()
        qs = view.get_model_qs(request)

        self.assertEqual(qs.count(), 2)

    def test_returns_correct_queryset_for_specific_year(self):
        """
        Test returns correct queryset for specific year

        :return:
        :rtype:
        """

        request = RequestFactory().get("/")
        view = FatLinksTableView()
        qs = view.get_model_qs(request, year=2022)

        self.assertEqual(qs.count(), 1)


class TestLogsTableView(DataTableBaseTestCase):
    """
    Tests for LogsTableView.
    """

    def setUp(self):
        self.request = HttpRequest()
        self.view = LogsTableView()
        self.view.request = self.request

    def test_grants_access_with_manage_afat_permission(self):
        """
        Test grants access with manage afat permission

        :return:
        :rtype:
        """

        self.request.user = self.user_with_manage_afat
        self.assertTrue(self.view.has_permission())

    def test_grants_access_with_log_view_permission(self):
        """
        Test grants access with log view permission

        :return:
        :rtype:
        """

        self.request.user = self.user_with_log_view
        self.assertTrue(self.view.has_permission())

    def test_grants_access_with_both_permissions(self):
        """
        Test grants access with both permissions

        :return:
        :rtype:
        """

        self.request.user = self.user_with_manage_and_log
        self.assertTrue(self.view.has_permission())

    def test_denies_access_with_basic_access_permission(self):
        """
        Test denies access with basic access permission

        :return:
        :rtype:
        """

        self.request.user = self.user_with_basic_access
        self.assertFalse(self.view.has_permission())

    def test_denies_access_without_permissions(self):
        """
        Test denies access without permissions

        :return:
        :rtype:
        """

        self.request.user = self.user_without_access
        self.assertFalse(self.view.has_permission())

    def test_returns_queryset_with_fatlink_exists_annotation(self):
        """
        Test returns queryset with fatlink_exists annotation

        :return:
        :rtype:
        """

        Log.objects.create(log_time="2023-01-01 00:00:00", log_text="Test log")

        queryset = self.view.get_model_qs(self.request)

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(hasattr(queryset.first(), "fatlink_exists"))
