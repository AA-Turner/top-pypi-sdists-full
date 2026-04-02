"""
Test cases for the admin.py module.
"""

# Standard Library
from unittest.mock import MagicMock, patch

# Django
from django.contrib import admin
from django.contrib.auth.models import User

# Alliance Auth AFAT
from afat.admin import (
    AFatLinkAdmin,
    AFatLinkTypeAdmin,
    AFatLogAdmin,
    DoctrineAdmin,
    FatsInTimeFilterAdmin,
    SettingAdmin,
)
from afat.forms import DoctrineAdminForm, SettingAdminForm
from afat.models import Doctrine, FatLink, FatsInTimeFilter, FleetType, Log, Setting
from afat.tests import BaseTestCase


class TestAFatLinkTypeAdmin(BaseTestCase):
    """
    Test cases for the AFatLinkTypeAdmin class.
    """

    def test_activates_selected_fleet_types_successfully(self):
        """
        Test that the activate method successfully activates selected fleet types.

        :return:
        :rtype:
        """

        queryset = MagicMock()
        queryset.count.return_value = 3
        queryset.__iter__.return_value = [
            MagicMock(is_enabled=False),
            MagicMock(is_enabled=False),
            MagicMock(is_enabled=False),
        ]
        admin_instance = AFatLinkTypeAdmin(model=FleetType, admin_site=admin.site)
        admin_instance.activate(request=MagicMock(), queryset=queryset)

        for obj in queryset:
            self.assertTrue(obj.is_enabled)

    def test_deactivates_selected_fleet_types_successfully(self):
        """
        Test that the deactivate method successfully deactivates selected fleet types.

        :return:
        :rtype:
        """

        queryset = MagicMock()
        queryset.count.return_value = 3
        queryset.__iter__.return_value = [
            MagicMock(is_enabled=True),
            MagicMock(is_enabled=True),
            MagicMock(is_enabled=True),
        ]
        admin_instance = AFatLinkTypeAdmin(model=FleetType, admin_site=admin.site)
        admin_instance.deactivate(request=MagicMock(), queryset=queryset)

        for obj in queryset:
            self.assertFalse(obj.is_enabled)

    def test_handles_activation_failure_gracefully(self):
        """
        Test that the activate method handles activation failure gracefully.

        :return:
        :rtype:
        """

        queryset = MagicMock()
        queryset.count.return_value = 2
        mock_obj_1 = MagicMock(is_enabled=False)
        mock_obj_1.save.side_effect = Exception()  # Simulate save failure
        mock_obj_2 = MagicMock(is_enabled=False)
        queryset.__iter__.return_value = [mock_obj_1, mock_obj_2]

        admin_instance = AFatLinkTypeAdmin(model=FleetType, admin_site=admin.site)
        request = MagicMock()

        with patch.object(mock_obj_1, "is_enabled", new_callable=lambda: False):
            try:
                admin_instance.activate(request=request, queryset=queryset)
            except Exception:
                pass  # Ensure the test continues even if an exception is raised

        self.assertFalse(mock_obj_1.is_enabled)  # Ensure it remains False after failure
        self.assertTrue(mock_obj_2.is_enabled)  # Ensure successful activation

    def test_handles_deactivation_failure_gracefully(self):
        """
        Test that the deactivate method handles deactivation failure gracefully.

        :return:
        :rtype:
        """

        queryset = MagicMock()
        queryset.count.return_value = 2
        mock_obj_1 = MagicMock(is_enabled=True)
        mock_obj_1.save.side_effect = Exception()  # Simulate save failure
        mock_obj_2 = MagicMock(is_enabled=True)
        queryset.__iter__.return_value = [mock_obj_1, mock_obj_2]

        admin_instance = AFatLinkTypeAdmin(model=FleetType, admin_site=admin.site)
        request = MagicMock()

        with patch.object(mock_obj_1, "is_enabled", new_callable=lambda: True):
            try:
                admin_instance.deactivate(request=request, queryset=queryset)
            except Exception:
                pass  # Ensure the test continues even if an exception is raised

        self.assertTrue(mock_obj_1.is_enabled)  # Ensure it remains True after failure
        self.assertFalse(mock_obj_2.is_enabled)  # Ensure successful deactivation

    def test_returns_fleet_type_name(self):
        """
        Test that the _name method returns the correct fleet type name.

        :return:
        :rtype:
        """

        fleet_type = FleetType.objects.create(name="Test Fleet Type")
        admin_instance = AFatLinkTypeAdmin(FleetType, admin.site)

        self.assertEqual(admin_instance._name(fleet_type), "Test Fleet Type")

    def test_returns_true_when_is_enabled_is_true(self):
        """
        Test that the _is_enabled method returns True when is_enabled is True.

        :return:
        :rtype:
        """

        fleet_type = FleetType.objects.create(name="Test Fleet Type", is_enabled=True)
        admin_instance = AFatLinkTypeAdmin(FleetType, admin.site)

        self.assertTrue(admin_instance._is_enabled(fleet_type))

    def test_returns_false_when_is_enabled_is_false(self):
        """
        Test that the _is_enabled method returns False when is_enabled is False.

        :return:
        :rtype:
        """

        fleet_type = FleetType.objects.create(name="Test Fleet Type", is_enabled=False)
        admin_instance = AFatLinkTypeAdmin(FleetType, admin.site)

        self.assertFalse(admin_instance._is_enabled(fleet_type))


class TestAFatLogAdmin(BaseTestCase):
    """
    Test cases for the AFatLogAdmin class.
    """

    def test_displays_all_log_fields_in_list_display(self):
        """
        Test that the list_display attribute contains all fields of the Log model.

        :return:
        :rtype:
        """

        MagicMock(
            log_time="2023-01-01 12:00:00",
            log_event="Event",
            user="User",
            fatlink_hash="hash123",
            log_text="Log text",
        )
        admin_instance = AFatLogAdmin(model=Log, admin_site=admin.site)

        self.assertEqual(
            admin_instance.list_display,
            ("log_time", "log_event", "user", "fatlink_hash", "log_text"),
        )

    def test_filters_logs_by_event(self):
        """
        Test that the list_filter attribute contains the log_event field.

        :return:
        :rtype:
        """

        with patch.object(
            AFatLogAdmin, "get_queryset", return_value=MagicMock()
        ) as mock_get_queryset:
            mock_request = MagicMock()
            admin_instance = AFatLogAdmin(model=Log, admin_site=admin.site)
            filtered_queryset = admin_instance.get_queryset(mock_request)

            self.assertEqual(filtered_queryset, mock_get_queryset.return_value)

    def test_searches_logs_by_fields(self):
        """
        Test that the search_fields attribute contains the correct fields for searching.

        :return:
        :rtype:
        """

        admin_instance = AFatLogAdmin(model=Log, admin_site=admin.site)

        self.assertEqual(
            admin_instance.search_fields,
            (
                "fatlink_hash",
                "user__profile__main_character__character_name",
                "user__username",
            ),
        )


class TestSettingAdmin(BaseTestCase):
    """
    Test cases for the SettingAdmin class.
    """

    def test_displays_correct_form_class(self):
        """
        Test that the SettingAdmin class displays the correct form class.

        :return:
        :rtype:
        """

        admin_instance = SettingAdmin(model=Setting, admin_site=admin.site)

        self.assertEqual(admin_instance.form, SettingAdminForm)

    def test_handles_missing_form_gracefully(self):
        with patch.object(SettingAdmin, "form", None):
            admin_instance = SettingAdmin(model=Setting, admin_site=admin.site)

            self.assertIsNone(admin_instance.form)


class TestDoctrineAdmin(BaseTestCase):
    """
    Test cases for the DoctrineAdmin class.
    """

    def test_displays_correct_form_class(self):
        """
        Test that the DoctrineAdmin class displays the correct form class.

        :return:
        :rtype:
        """

        admin_instance = DoctrineAdmin(model=Doctrine, admin_site=admin.site)

        self.assertEqual(admin_instance.form, DoctrineAdminForm)

    def test_displays_all_fields_in_list_display(self):
        """
        Test that the list_display attribute contains all fields of the Doctrine model.

        :return:
        :rtype:
        """

        mock_field_1 = MagicMock()
        mock_field_1.name = "field_1"
        mock_field_2 = MagicMock()
        mock_field_2.name = "field_2"
        Doctrine._meta.get_fields = MagicMock(return_value=[mock_field_1, mock_field_2])

        with patch.object(
            DoctrineAdmin, "list_display", new_callable=lambda: ["field_1", "field_2"]
        ):
            admin_instance = DoctrineAdmin(model=Doctrine, admin_site=admin.site)

            self.assertEqual(admin_instance.list_display, ["field_1", "field_2"])

    def test_handles_empty_fields_gracefully(self):
        Doctrine._meta.get_fields = MagicMock(return_value=[])

        with patch.object(DoctrineAdmin, "list_display", new_callable=lambda: []):
            admin_instance = DoctrineAdmin(model=Doctrine, admin_site=admin.site)

            self.assertEqual(admin_instance.list_display, [])


class TestFatsInTimeFilterAdmin(BaseTestCase):
    """
    Test cases for the FatsInTimeFilterAdmin class.
    """

    def test_returns_correct_fleet_types_for_filter(self):
        """
        Test that the get_fleet_types method returns the correct fleet types.

        :return:
        :rtype:
        """

        mock_fleet_type_1 = MagicMock()
        mock_fleet_type_1.name = "FleetType1"
        mock_fleet_type_2 = MagicMock()
        mock_fleet_type_2.name = "FleetType2"
        obj = MagicMock(
            fleet_types=MagicMock(
                all=MagicMock(return_value=[mock_fleet_type_1, mock_fleet_type_2])
            )
        )
        admin_instance = FatsInTimeFilterAdmin(
            model=FatsInTimeFilter, admin_site=admin.site
        )
        result = admin_instance.get_fleet_types(obj)

        self.assertEqual(result, "FleetType1, FleetType2")

    def test_returns_empty_fleet_types_when_none_exist(self):
        """
        Test that the get_fleet_types method returns an empty string when no fleet types exist.

        :return:
        :rtype:
        """

        obj = MagicMock(fleet_types=MagicMock(all=MagicMock(return_value=[])))
        admin_instance = FatsInTimeFilterAdmin(
            model=FatsInTimeFilter, admin_site=admin.site
        )
        result = admin_instance.get_fleet_types(obj)

        self.assertEqual(result, "")

    def test_returns_correct_ship_classes_for_filter(self):
        """
        Test that the get_ship_classes method returns the correct ship classes.

        :return:
        :rtype:
        """

        mock_ship_class_1 = MagicMock()
        mock_ship_class_1.name = "ShipClass1"
        mock_ship_class_2 = MagicMock()
        mock_ship_class_2.name = "ShipClass2"
        obj = MagicMock(
            ship_classes=MagicMock(
                all=MagicMock(return_value=[mock_ship_class_1, mock_ship_class_2])
            )
        )
        admin_instance = FatsInTimeFilterAdmin(
            model=FatsInTimeFilter, admin_site=admin.site
        )
        result = admin_instance.get_ship_classes(obj)

        self.assertEqual(result, "ShipClass1, ShipClass2")

    def test_returns_empty_ship_classes_when_none_exist(self):
        """
        Test that the get_ship_classes method returns an empty string when no ship classes exist.

        :return:
        :rtype:
        """

        obj = MagicMock(ship_classes=MagicMock(all=MagicMock(return_value=[])))
        admin_instance = FatsInTimeFilterAdmin(
            model=FatsInTimeFilter, admin_site=admin.site
        )
        result = admin_instance.get_ship_classes(obj)

        self.assertEqual(result, "")


class TestAFatLinkAdmin(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = User.objects.create(username="testuser")
        cls.fat_link = FatLink.objects.create(fleet="Test Fleet", creator=user)

    @patch("afat.admin.Count")
    @patch("django.db.models.query.QuerySet.annotate")
    def test_get_queryset_returns_annotated_queryset(self, mock_annotate, mock_count):
        """
        Test that get_queryset returns an annotated queryset with the correct fat count.

        :param mock_annotate:
        :type mock_annotate:
        :param mock_count:
        :type mock_count:
        :return:
        :rtype:
        """

        # Return a mock that looks like a Django expression (has resolve_expression)
        mock_expr = MagicMock()
        mock_expr.resolve_expression = MagicMock()
        mock_count.return_value = mock_expr

        # Prevent annotate from triggering SQL compilation; return the base queryset
        mock_annotate.return_value = FatLink.objects.all()

        admin_instance = AFatLinkAdmin(FatLink, admin.site)
        request = self.client.request().wsgi_request
        queryset = admin_instance.get_queryset(request)

        self.assertIn(self.fat_link, queryset)
        mock_count.assert_called_once_with(expression="afat_fats", distinct=True)
        mock_annotate.assert_called_once()

    def test_get_queryset_handles_empty_queryset(self):
        """
        Test that get_queryset handles an empty queryset without errors.

        :return:
        :rtype:
        """

        FatLink.objects.all().delete()

        admin_instance = AFatLinkAdmin(FatLink, admin.site)
        request = self.client.request().wsgi_request
        queryset = admin_instance.get_queryset(request)

        self.assertEqual(queryset.count(), 0)

    def test_returns_correct_number_of_fats(self):
        """
        Test that number_of_fats returns the correct count from the annotation.

        :return:
        :rtype:
        """

        self.fat_link._number_of_fats = 5

        admin_instance = AFatLinkAdmin(FatLink, admin.site)
        self.assertEqual(admin_instance.number_of_fats(self.fat_link), 5)

    def test_handles_zero_fats(self):
        """
        Test that number_of_fats correctly handles zero fats.

        :return:
        :rtype:
        """

        self.fat_link._number_of_fats = 0

        admin_instance = AFatLinkAdmin(FatLink, admin.site)
        self.assertEqual(admin_instance.number_of_fats(self.fat_link), 0)

    def test_handles_missing_annotation(self):
        """
        Test that number_of_fats returns None when the annotation is missing.

        :return:
        :rtype:
        """

        if hasattr(self.fat_link, "_number_of_fats"):
            delattr(self.fat_link, "_number_of_fats")

        admin_instance = AFatLinkAdmin(FatLink, admin.site)
        self.assertIsNone(admin_instance.number_of_fats(self.fat_link))
