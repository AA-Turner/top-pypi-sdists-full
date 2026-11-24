"""Unit tests for killstats Celery tasks."""

# Standard Library
from http import HTTPStatus
from unittest.mock import MagicMock, patch

# Third Party
import pook
from aiopenapi3 import RequestError
from celery.exceptions import Retry
from evesde_factory.eve_sde import ItemTypeFactory

# Django
from django.core.cache import cache
from django.db import IntegrityError
from django.test import override_settings
from django.utils import timezone

# Alliance Auth
from esi.exceptions import (
    ESIErrorLimitException,
    HTTPClientError,
    HTTPServerError,
)

# AA Killstats
from killstats import tasks
from killstats.errors import DownTimeError
from killstats.models import Killmail
from killstats.providers import DOWNTIME_TIMER
from killstats.tasks import (
    check_and_import_alliance_killmails_task,
    check_and_import_corporation_killmails_task,
)
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import KillmailBodyFactory

UNIVERSE_NAMES_URL = "https://esi.evetech.net/universe/names"

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


def clear_esi_limits() -> None:
    """Remove the ESI error limit from the shared cache."""
    cache.delete("esi_error_limit_reset")


def stored_killmail_body():
    """Return a cached KillmailBody whose victim is not yet known as EveEntity."""
    killmail_body = KillmailBodyFactory()
    ItemTypeFactory(id=killmail_body.esi.victim.ship_type_id)
    killmail_body.save()
    return killmail_body


@override_settings(
    CELERY_ALWAYS_EAGER=True,
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    DISABLE_DAILY_DOWNTIME_CHECK=True,
)
@patch.object(tasks.store_killmail, "retry", side_effect=Retry)
class TestStoreKillmailEsiErrors(AuthTestCase):
    """ESI errors while storing a killmail retry the task."""

    def setUp(self):
        super().setUp()
        clear_esi_limits()
        self.addCleanup(clear_esi_limits)
        self.killmail_body = stored_killmail_body()
        self.addCleanup(self.killmail_body.delete)

    def _assert_retried(self, mock_retry, exc_type, countdown_min: float):
        mock_retry.assert_called_once()
        kwargs = mock_retry.call_args.kwargs
        self.assertIsInstance(kwargs["exc"], exc_type)
        self.assertGreaterEqual(kwargs["countdown"], countdown_min)
        self.assertFalse(
            Killmail.objects.filter(killmail_id=self.killmail_body.killmail_id).exists()
        )

    def test_should_retry_on_esi_server_errors(self, mock_retry):
        for status_code in [
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]:
            with self.subTest(status_code=status_code), pook.use():
                # Test Data
                mock_retry.reset_mock()
                pook.post(
                    UNIVERSE_NAMES_URL,
                    reply=status_code,
                    response_json={"error": status_code.phrase},
                )

                # Test Action
                with self.assertRaises(Retry):
                    tasks.store_killmail(self.killmail_body.killmail_id)

                # Expected Result
                self._assert_retried(mock_retry, HTTPServerError, DOWNTIME_TIMER)

    @pook.on
    def test_should_retry_on_the_esi_error_limit(self, mock_retry):
        # Test Data
        pook.post(
            UNIVERSE_NAMES_URL,
            reply=420,
            response_json={"error": "Error limited"},
            response_headers={"X-RateLimit-Reset": "30"},
        )

        # Test Action
        with self.assertRaises(Retry):
            tasks.store_killmail(self.killmail_body.killmail_id)

        # Expected Result
        self._assert_retried(mock_retry, ESIErrorLimitException, 30)

    @pook.on
    @patch("esi.app_settings.ESI_SERVER_ERROR_MAX_RETRIES", 1)
    def test_should_retry_on_request_errors(self, mock_retry):
        # Test Data
        pook.post(UNIVERSE_NAMES_URL).error(ConnectionError("Connection reset"))

        # Test Action
        with self.assertRaises(Retry):
            tasks.store_killmail(self.killmail_body.killmail_id)

        # Expected Result
        self._assert_retried(mock_retry, RequestError, DOWNTIME_TIMER)

    def test_should_raise_other_esi_errors_without_retry(self, mock_retry):
        for status_code, exc_type in [
            (HTTPStatus.INTERNAL_SERVER_ERROR, HTTPServerError),
            (HTTPStatus.NOT_FOUND, HTTPClientError),
        ]:
            with self.subTest(status_code=status_code), pook.use():
                # Test Data
                pook.post(
                    UNIVERSE_NAMES_URL,
                    reply=status_code,
                    response_json={"error": status_code.phrase},
                )

                # Test Action & Expected Result
                with self.assertRaises(exc_type):
                    tasks.store_killmail(self.killmail_body.killmail_id)
                mock_retry.assert_not_called()

    @override_settings(DISABLE_DAILY_DOWNTIME_CHECK=False)
    @pook.on
    def test_should_retry_during_daily_downtime(self, mock_retry):
        # Test Data: no ESI request may happen during the downtime
        with patch("killstats.providers.timezone.now") as mock_now:
            mock_now.return_value = timezone.datetime.strptime("11:05", "%H:%M")

            # Test Action
            with self.assertRaises(Retry):
                tasks.store_killmail(self.killmail_body.killmail_id)

        # Expected Result
        self._assert_retried(mock_retry, DownTimeError, DOWNTIME_TIMER)


@override_settings(
    CELERY_ALWAYS_EAGER=True,
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    DISABLE_DAILY_DOWNTIME_CHECK=True,
)
class TestImportMissingKillmailsEsiErrors(AuthTestCase):
    """ESI errors while importing missing killmails retry the task."""

    def setUp(self):
        super().setUp()
        clear_esi_limits()
        self.addCleanup(clear_esi_limits)

    @pook.on
    def test_should_retry_on_esi_server_errors(self):
        for task, kwargs, check_kwargs in [
            (
                tasks.check_and_import_corporation_killmails_task,
                {"corporation_id": 98000001},
                {"corporation_id": 98000001, "pages": 3},
            ),
            (
                tasks.check_and_import_alliance_killmails_task,
                {"alliance_id": 99000001},
                {"alliance_id": 99000001, "pages": 3},
            ),
        ]:
            with (
                self.subTest(task=task.name),
                patch.object(task, "retry", side_effect=Retry) as mock_retry,
                patch(
                    f"{MODULE_PATH}.Killmail.objects.check_missing_killmails"
                ) as mock_check_missing,
            ):
                # Test Data
                mock_check_missing.return_value = [stored_killmail_body()]
                pook.post(
                    UNIVERSE_NAMES_URL,
                    reply=HTTPStatus.BAD_GATEWAY,
                    response_json={"error": "Bad Gateway"},
                )

                # Test Action
                with self.assertRaises(Retry):
                    task(**kwargs)

                # Expected Result
                mock_check_missing.assert_called_once_with(**check_kwargs)
                mock_retry.assert_called_once()
                self.assertIsInstance(
                    mock_retry.call_args.kwargs["exc"], HTTPServerError
                )
