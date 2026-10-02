"""Unit tests for killstats Celery tasks."""

# Standard Library
from unittest.mock import MagicMock, patch

# Django
from django.db import IntegrityError

# AA Killstats
from killstats.tasks import (
    check_and_import_alliance_killmails_task,
    check_and_import_corporation_killmails_task,
)
from killstats.tests import AuthTestCase

MODULE_PATH = "killstats.tasks"


class TestMissingKillmailsTasks(AuthTestCase):
    @patch(f"{MODULE_PATH}.Killmail.objects.create_from_killmail")
    @patch(f"{MODULE_PATH}.Killmail.objects.check_missing_killmails")
    def test_check_and_import_corporation_killmails_task_should_import_successfully(
        self, mock_check_missing, mock_create
    ):
        # Test Data
        mock_km = MagicMock()
        mock_check_missing.return_value = [mock_km]

        # Test Action
        check_and_import_corporation_killmails_task(corporation_id=98000001, pages=3)

        # Expected Result
        mock_check_missing.assert_called_once_with(corporation_id=98000001, pages=3)
        mock_create.assert_called_once_with(mock_km)

    @patch(f"{MODULE_PATH}.Killmail.objects.create_from_killmail")
    @patch(f"{MODULE_PATH}.Killmail.objects.check_missing_killmails")
    def test_check_and_import_corporation_killmails_task_should_catch_integrity_error(
        self, mock_check_missing, mock_create
    ):
        # Test Data
        mock_km = MagicMock()
        mock_km.esi.killmail_id = 12345
        mock_check_missing.return_value = [mock_km]
        mock_create.side_effect = IntegrityError("Duplicate entry for key 'hash'")

        # Test Action - should not raise IntegrityError
        check_and_import_corporation_killmails_task(corporation_id=98000001, pages=3)

        # Expected Result
        mock_create.assert_called_once_with(mock_km)

    @patch(f"{MODULE_PATH}.Killmail.objects.create_from_killmail")
    @patch(f"{MODULE_PATH}.Killmail.objects.check_missing_killmails")
    def test_check_and_import_alliance_killmails_task_should_catch_integrity_error(
        self, mock_check_missing, mock_create
    ):
        # Test Data
        mock_km = MagicMock()
        mock_km.esi.killmail_id = 12345
        mock_check_missing.return_value = [mock_km]
        mock_create.side_effect = IntegrityError("Duplicate entry for key 'hash'")

        # Test Action - should not raise IntegrityError
        check_and_import_alliance_killmails_task(alliance_id=99000001, pages=3)

        # Expected Result
        mock_create.assert_called_once_with(mock_km)
