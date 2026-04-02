"""
Test cases for the smart filter model.
"""

# Standard Library
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

# Django
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership
from allianceauth.authentication.signals import assign_state_on_active_change

# Alliance Auth AFAT
from afat.models.smart_filter import FatsInTimeFilter, _get_threshold_date
from afat.tests import BaseTestCase


class TestGetThresholdDate(BaseTestCase):
    """
    Test cases for the _get_threshold_date function.
    """

    def test_returns_correct_threshold_date_for_positive_days(self):
        """
        Test that the function returns the correct threshold date for positive days.

        :return:
        :rtype:
        """

        days = 10
        expected_date = datetime.now(timezone.utc) - timedelta(days=days)
        result = _get_threshold_date(days)

        self.assertAlmostEqual(result, expected_date, delta=timedelta(seconds=1))

    def test_returns_correct_threshold_date_for_zero_days(self):
        """
        Test that the function returns the correct threshold date for zero days.

        :return:
        :rtype:
        """

        days = 0
        expected_date = datetime.now(timezone.utc)
        result = _get_threshold_date(days)

        self.assertAlmostEqual(result, expected_date, delta=timedelta(seconds=1))


class TestFatsInTimeFilter(BaseTestCase):
    """
    Test cases for the FatsInTimeFilter class.
    """

    @patch("afat.models.smart_filter._get_threshold_date")
    @patch("afat.models.smart_filter.Fat.objects.filter")
    def test_returns_true_when_user_meets_fats_needed(
        self, mock_fat_filter, mock_get_threshold_date
    ):
        """
        Test that the process_filter method returns True when the user meets the fats needed.

        :param mock_fat_filter:
        :type mock_fat_filter:
        :param mock_get_threshold_date:
        :type mock_get_threshold_date:
        :return:
        :rtype:
        """

        mock_get_threshold_date.return_value = datetime.now(timezone.utc) - timedelta(
            days=30
        )
        mock_fat_filter.return_value.count.return_value = 10
        user = User.objects.create(username="testuser")  # Save the user to the database
        filter_instance = FatsInTimeFilter(days=30, fats_needed=10)
        filter_instance.save()  # Save the filter instance to the database

        self.assertTrue(filter_instance.process_filter(user))

    @patch("afat.models.smart_filter._get_threshold_date")
    @patch("afat.models.smart_filter.Fat.objects.filter")
    def test_returns_false_when_user_does_not_meet_fats_needed(
        self, mock_fat_filter, mock_get_threshold_date
    ):
        """
        Test that the process_filter method returns False when the user does not meet the fats needed.

        :param mock_fat_filter:
        :type mock_fat_filter:
        :param mock_get_threshold_date:
        :type mock_get_threshold_date:
        :return:
        :rtype:
        """

        mock_get_threshold_date.return_value = datetime.now(timezone.utc) - timedelta(
            days=30
        )
        mock_fat_filter.return_value.count.return_value = 5
        user = User.objects.create(username="testuser")  # Save the user to the database
        filter_instance = FatsInTimeFilter(days=30, fats_needed=10)
        filter_instance.save()  # Save the filter instance to the database

        self.assertFalse(filter_instance.process_filter(user))

    @patch("afat.models.smart_filter._get_threshold_date")
    @patch("afat.models.smart_filter.Fat.objects.filter")
    def test_returns_false_when_user_has_no_characters(
        self, mock_fat_filter, mock_get_threshold_date
    ):
        """
        Test that the process_filter method returns False when the user has no characters.

        :param mock_fat_filter:
        :type mock_fat_filter:
        :param mock_get_threshold_date:
        :type mock_get_threshold_date:
        :return:
        :rtype:
        """

        mock_get_threshold_date.return_value = datetime.now(timezone.utc) - timedelta(
            days=30
        )
        mock_fat_filter.side_effect = CharacterOwnership.DoesNotExist
        user = User.objects.create(username="testuser")  # Save the user to the database
        filter_instance = FatsInTimeFilter(days=30, fats_needed=10)
        filter_instance.save()  # Save the filter instance to the database

        self.assertFalse(filter_instance.process_filter(user))

    @patch("afat.models.smart_filter._get_threshold_date")
    @patch("afat.models.smart_filter.Fat.objects.filter")
    def test_returns_correct_audit_results_when_users_have_no_fats(
        self, mock_fat_filter, mock_get_threshold_date
    ):
        """
        Test that the audit_filter method returns the correct results when users have no fats.

        :param mock_fat_filter:
        :type mock_fat_filter:
        :param mock_get_threshold_date:
        :type mock_get_threshold_date:
        :return:
        :rtype:
        """

        mock_get_threshold_date.return_value = datetime.now(timezone.utc) - timedelta(
            days=30
        )

        mock_queryset = MagicMock()
        mock_queryset.select_related.return_value = mock_queryset
        mock_queryset.filter.return_value = mock_queryset
        mock_queryset.values_list.return_value = []
        mock_fat_filter.return_value = mock_queryset

        # Disconnect the signal to avoid triggering it during user creation
        pre_save.disconnect(assign_state_on_active_change, sender=User)

        user1 = User.objects.create(pk=1, username="user1")
        user2 = User.objects.create(pk=2, username="user2")

        # Reconnect the signal after user creation
        pre_save.connect(assign_state_on_active_change, sender=User)

        users = [user1, user2]
        filter_instance = FatsInTimeFilter(days=30, fats_needed=2)
        filter_instance.save()
        result = filter_instance.audit_filter(users)

        self.assertEqual(result[1]["message"], 0)
        self.assertFalse(result[1]["check"])
        self.assertEqual(result[2]["message"], 0)
        self.assertFalse(result[2]["check"])
