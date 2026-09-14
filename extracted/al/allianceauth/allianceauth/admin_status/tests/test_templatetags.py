from types import SimpleNamespace
from unittest.mock import patch, MagicMock

import requests_mock
from packaging.version import Version as Pep440Version

from allianceauth.admin_status.templatetags import admin_status
from allianceauth.admin_status.templatetags.admin_status import decimal_widthratio
from allianceauth.utils.testing import NoSocketsTestCase

MODULE_PATH = "allianceauth.admin_status.templatetags.admin_status"


class TestCurrentVersionSummary(NoSocketsTestCase):
    def test_handles_empty_stored_versions_and_returns_false_flags(self):
        dummy = type(
            "S", (), {"latest_stable_version": "", "latest_development_version": ""}
        )()

        with (
            patch(MODULE_PATH + ".SoftwareVersion.get_solo", return_value=dummy),
            patch(MODULE_PATH + ".__version__", "2.0.0"),
        ):
            from allianceauth.admin_status.templatetags.admin_status import (
                _current_version_summary,
            )

            result = _current_version_summary()
            self.assertEqual(result["latest_patch"], False)
            self.assertEqual(result["latest_beta"], False)
            self.assertEqual(result["current_version"], "2.0.0")
            self.assertIsNone(result["latest_patch_version"])
            self.assertIsNone(result["latest_beta_version"])

    def test_reports_latest_patch_when_current_is_at_or_above_stable(self):
        dummy = type(
            "S",
            (),
            {"latest_stable_version": "2.0.0", "latest_development_version": ""},
        )()

        with (
            patch(MODULE_PATH + ".SoftwareVersion.get_solo", return_value=dummy),
            patch(MODULE_PATH + ".__version__", "2.0.1"),
        ):
            from allianceauth.admin_status.templatetags.admin_status import (
                _current_version_summary,
            )

            result = _current_version_summary()
            self.assertTrue(result["latest_patch"])
            self.assertEqual(result["latest_patch_version"], Pep440Version("2.0.0"))
            self.assertIsNone(result["latest_beta_version"])

    def test_reports_beta_when_dev_present_and_current_is_at_or_below_dev_and_dev_is_after_stable(
        self,
    ):
        dummy = type(
            "S",
            (),
            {
                "latest_stable_version": "1.0.0",
                "latest_development_version": "2.0.0a1",
            },
        )()

        with (
            patch(MODULE_PATH + ".SoftwareVersion.get_solo", return_value=dummy),
            patch(MODULE_PATH + ".__version__", "1.5.0"),
        ):
            from allianceauth.admin_status.templatetags.admin_status import (
                _current_version_summary,
            )

            result = _current_version_summary()
            self.assertTrue(result["latest_beta"])
            self.assertEqual(result["latest_patch_version"], Pep440Version("1.0.0"))
            self.assertEqual(result["latest_beta_version"], Pep440Version("2.0.0a1"))

    def test_ignores_invalid_version_strings_and_does_not_raise(self):
        dummy = type(
            "S",
            (),
            {
                "latest_stable_version": "invalid",
                "latest_development_version": "also-invalid",
            },
        )()
        with (
            patch(MODULE_PATH + ".SoftwareVersion.get_solo", return_value=dummy),
            patch(MODULE_PATH + ".__version__", "1.0.0"),
        ):
            from allianceauth.admin_status.templatetags.admin_status import (
                _current_version_summary,
            )

            result = _current_version_summary()
            self.assertFalse(result["latest_patch"])
            self.assertFalse(result["latest_beta"])
            self.assertIsNone(result["latest_patch_version"])
            self.assertIsNone(result["latest_beta_version"])


class TestDecimalWidthRatio(NoSocketsTestCase):
    def test_decimal_widthratio_returns_zero_when_max_value_is_zero(self):
        self.assertEqual(decimal_widthratio(5, 0, 10), "0")

    def test_decimal_widthratio_calculates_and_rounds_for_integer_inputs(self):
        expected = str(round(2 / 4 * 100, 2))
        self.assertEqual(decimal_widthratio(2, 4, 100), expected)

    def test_decimal_widthratio_handles_float_inputs_and_rounds_two_decimals(self):
        expected = str(round(1.234 / 3.0 * 50.0, 2))
        self.assertEqual(decimal_widthratio(1.234, 3.0, 50.0), expected)

    def test_decimal_widthratio_handles_negative_max_value(self):
        expected = str(round(1 / -2 * 100, 2))
        self.assertEqual(decimal_widthratio(1, -2, 100), expected)


class TestStatusOverviewAdditional(NoSocketsTestCase):
    @patch(MODULE_PATH + "._current_notifications")
    @patch(MODULE_PATH + "._current_version_summary")
    @patch(MODULE_PATH + "._celery_stats")
    def test_status_overview_merges_all_sections_and_handles_empty_notifications(
        self, mock_celery, mock_version, mock_notifications
    ):
        mock_notifications.return_value = {"notifications": []}
        mock_version.return_value = {"current_version": "9.9.9", "latest_patch": True}
        mock_celery.return_value = {
            "tasks_succeeded": 1,
            "tasks_retried": 0,
            "tasks_failed": 0,
            "tasks_total": 1,
            "tasks_hours": 24,
            "earliest_task": None,
        }

        from allianceauth.admin_status.templatetags.admin_status import status_overview

        result = status_overview()
        self.assertIn("notifications", result)
        self.assertEqual(result["notifications"], [])
        self.assertEqual(result["current_version"], "9.9.9")
        self.assertTrue(result["latest_patch"])
        self.assertEqual(result["tasks_succeeded"], 1)

    def test_status_overview_honors_display_debug_setting(self):
        with (
            patch(
                MODULE_PATH + "._current_notifications",
                return_value={"notifications": []},
            ),
            patch(MODULE_PATH + "._current_version_summary", return_value={}),
            patch(MODULE_PATH + "._celery_stats", return_value={}),
            patch(MODULE_PATH + ".settings") as mock_settings,
        ):
            mock_settings.DISPLAY_DEBUG = False
            mock_settings.DEBUG = True
            from allianceauth.admin_status.templatetags.admin_status import (
                status_overview,
            )

            result = status_overview()

            self.assertIn("debug", result)
            self.assertFalse(result["debug"])


class TestCeleryStatsHelpers(NoSocketsTestCase):
    def test_returns_mapped_task_stats_from_dashboard_results_with_custom_hours_setting(
        self,
    ):
        dummy = SimpleNamespace(
            succeeded=5,
            retried=1,
            failed=2,
            total=8,
            hours=12,
            earliest_task="2020-01-01T00:00:00",
        )
        with (
            patch(MODULE_PATH + ".dashboard_results", return_value=dummy) as mock_dr,
            patch(MODULE_PATH + ".settings") as mock_settings,
        ):
            mock_settings.ALLIANCEAUTH_DASHBOARD_TASKS_MAX_HOURS = 12
            from allianceauth.admin_status.templatetags.admin_status import (
                _celery_stats,
            )

            result = _celery_stats()
            mock_dr.assert_called_once_with(hours=12)
            self.assertEqual(result["tasks_succeeded"], 5)
            self.assertEqual(result["tasks_retried"], 1)
            self.assertEqual(result["tasks_failed"], 2)
            self.assertEqual(result["tasks_total"], 8)
            self.assertEqual(result["tasks_hours"], 12)
            self.assertEqual(result["earliest_task"], "2020-01-01T00:00:00")

    def test_uses_default_hours_when_setting_missing_and_calls_dashboard_results_with_default(
        self,
    ):
        dummy = SimpleNamespace(
            succeeded=0, retried=0, failed=0, total=0, hours=24, earliest_task=None
        )
        with (
            patch(MODULE_PATH + ".dashboard_results", return_value=dummy) as mock_dr,
            patch(MODULE_PATH + ".settings") as mock_settings,
        ):
            # ensure the attribute is not present on settings
            if hasattr(mock_settings, "ALLIANCEAUTH_DASHBOARD_TASKS_MAX_HOURS"):
                delattr(mock_settings, "ALLIANCEAUTH_DASHBOARD_TASKS_MAX_HOURS")
            from allianceauth.admin_status.templatetags.admin_status import (
                _celery_stats,
            )

            result = _celery_stats()
            mock_dr.assert_called_once_with(hours=24)
            self.assertEqual(result["tasks_total"], 0)
            self.assertEqual(result["tasks_hours"], 24)


class TestCurrentNotifications(NoSocketsTestCase):
    def test_returns_notifications_from_applicationannouncement_objects_all(self):
        mock_ann = MagicMock()
        mock_list = [mock_ann]
        with patch(MODULE_PATH + ".ApplicationAnnouncement") as mock_model:
            # The implementation calls .objects.annotate(...).order_by(...)
            mock_model.objects.annotate.return_value.order_by.return_value = mock_list
            result = admin_status._current_notifications()

            expected_notifications = [
                {
                    "application_name": mock_ann.application_name,
                    "announcements": [
                        {
                            "announcement_number": mock_ann.announcement_number,
                            "announcement_text": mock_ann.announcement_text,
                            "announcement_url": mock_ann.announcement_url,
                            "hide_announcement": mock_ann.hide_announcement,
                        }
                    ],
                }
            ]

            self.assertIn("notifications", result)
            self.assertEqual(result["notifications"], expected_notifications)

    def test_returns_empty_notifications_when_none_saved(self):
        with patch(MODULE_PATH + ".ApplicationAnnouncement") as mock_model:
            mock_model.objects.annotate.return_value.order_by.return_value = []
            result = admin_status._current_notifications()
            self.assertIn("notifications", result)
            self.assertEqual(list(result["notifications"]), [])

    def test_if_name_not_in_grouped_is_false_on_second_iteration(self):
        ann1 = MagicMock()
        ann1.application_name = "Same App"
        ann1.announcement_number = 5
        ann1.announcement_text = "First"

        ann2 = MagicMock()
        ann2.application_name = "Same App"
        ann2.announcement_number = 4
        ann2.announcement_text = "Second"

        with patch(MODULE_PATH + ".ApplicationAnnouncement") as mock_model:
            mock_model.objects.annotate.return_value.order_by.return_value = [
                ann1,
                ann2,
            ]
            result = admin_status._current_notifications()
            self.assertIn("notifications", result)
            notifications = result["notifications"]
            # the grouped logic should produce a single application entry (if condition false on second)
            self.assertEqual(len(notifications), 1)
            self.assertEqual(notifications[0]["application_name"], "Same App")
            # and both announcements should be present under that single application
            self.assertEqual(len(notifications[0]["announcements"]), 2)
            self.assertEqual(
                [a["announcement_number"] for a in notifications[0]["announcements"]],
                [5, 4],
            )


class TestFetchTagsFromGitlab(NoSocketsTestCase):
    @requests_mock.mock()
    def test_fetch_tags_from_gitlab_returns_tags(self, requests_mocker):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_tags_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        tags = [{"name": "v1.0.0"}, {"name": "v1.1.0"}]
        requests_mocker.get(GITLAB_AUTH_REPOSITORY_TAGS_URL, json=tags)
        result = _fetch_tags_from_gitlab()
        self.assertEqual(result, tags)

    @requests_mock.mock()
    def test_fetch_tags_from_gitlab_returns_empty_on_error(self, requests_mocker):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_tags_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        requests_mocker.get(GITLAB_AUTH_REPOSITORY_TAGS_URL, status_code=500)
        result = _fetch_tags_from_gitlab()
        self.assertEqual(result, [])

    @requests_mock.mock()
    def test_fetch_tags_from_gitlab_combines_paginated_results(self, requests_mocker):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_tags_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        all_tags = [{"name": "v1.0.0"}, {"name": "v1.1.0"}, {"name": "v2.0.0"}]

        def callback(request, context):
            page = int(request.qs.get("page", ["1"])[0])
            per_page = 1
            start = (page - 1) * per_page
            end = start + per_page
            context.headers["x-total-pages"] = "3"
            return all_tags[start:end]

        requests_mocker.get(GITLAB_AUTH_REPOSITORY_TAGS_URL, json=callback)
        result = _fetch_tags_from_gitlab()
        self.assertEqual(result, all_tags)


class TestLatestsVersions(NoSocketsTestCase):
    def test_raises_when_no_stable_versions_available(self):
        tags = [{"name": "2.1.1a1"}, {"name": "1.0.0a1"}]
        with self.assertRaises(ValueError):
            admin_status._latests_versions(tags)

    def test_raises_when_no_beta_versions_available(self):
        tags = [{"name": "2.1.1"}, {"name": "2.0.0"}]
        with self.assertRaises(ValueError):
            admin_status._latests_versions(tags)

    def test_ignores_invalid_entries_and_returns_correct_max_versions(self):
        tags = [
            {"name": "invalid"},
            {"name": "1.0.0"},
            {"name": "1.2.0a1"},
            {"name": "1.1.0"},
        ]
        latest_patch, latest_beta = admin_status._latests_versions(tags)
        self.assertEqual(
            latest_patch,
            (
                Pep440Version("1.1.0")
                if Pep440Version("1.1.0") > Pep440Version("1.0.0")
                else Pep440Version("1.0.0")
            ),
        )
        self.assertEqual(latest_beta, Pep440Version("1.2.0a1"))


class TestFetchListFromGitlab(NoSocketsTestCase):
    @requests_mock.mock()
    def test_fetch_list_from_gitlab_combines_pages_using_x_total_pages(
        self, requests_mocker
    ):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_list_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        all_items = [{"name": "v1"}, {"name": "v2"}, {"name": "v3"}]

        def callback(request, context):
            page = int(request.qs.get("page", ["1"])[0])
            per_page = 1
            start = (page - 1) * per_page
            end = start + per_page
            context.headers["x-total-pages"] = "3"
            return all_items[start:end]

        requests_mocker.get(GITLAB_AUTH_REPOSITORY_TAGS_URL, json=callback)
        result = _fetch_list_from_gitlab(GITLAB_AUTH_REPOSITORY_TAGS_URL, max_pages=10)
        self.assertEqual(result, all_items)

    @requests_mock.mock()
    def test_fetch_list_from_gitlab_returns_single_page_when_no_header(
        self, requests_mocker
    ):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_list_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        payload = [{"name": "v1"}, {"name": "v2"}]
        requests_mocker.get(GITLAB_AUTH_REPOSITORY_TAGS_URL, json=payload)
        result = _fetch_list_from_gitlab(GITLAB_AUTH_REPOSITORY_TAGS_URL)
        self.assertEqual(result, payload)
        self.assertEqual(requests_mocker.call_count, 1)

    @requests_mock.mock()
    def test_fetch_list_from_gitlab_ignores_invalid_header_and_stops(
        self, requests_mocker
    ):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_list_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        payload = [{"name": "v1"}]
        requests_mocker.get(
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
            json=payload,
            headers={"x-total-pages": "invalid"},
        )
        result = _fetch_list_from_gitlab(GITLAB_AUTH_REPOSITORY_TAGS_URL)
        self.assertEqual(result, payload)
        self.assertEqual(requests_mocker.call_count, 1)

    @requests_mock.mock()
    def test_fetch_list_from_gitlab_respects_max_pages_limit(self, requests_mocker):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_list_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        all_items = [{"name": f"v{i}"} for i in range(1, 6)]

        def callback(request, context):
            page = int(request.qs.get("page", ["1"])[0])
            per_page = 1
            start = (page - 1) * per_page
            end = start + per_page
            context.headers["x-total-pages"] = "5"
            return all_items[start:end]

        requests_mocker.get(GITLAB_AUTH_REPOSITORY_TAGS_URL, json=callback)
        result = _fetch_list_from_gitlab(GITLAB_AUTH_REPOSITORY_TAGS_URL, max_pages=2)
        self.assertEqual(result, all_items[:2])

    @requests_mock.mock()
    def test_fetch_list_from_gitlab_returns_empty_on_request_error(
        self, requests_mocker
    ):
        from allianceauth.admin_status.templatetags.admin_status import (
            _fetch_list_from_gitlab,
            GITLAB_AUTH_REPOSITORY_TAGS_URL,
        )

        requests_mocker.get(GITLAB_AUTH_REPOSITORY_TAGS_URL, status_code=500)
        result = _fetch_list_from_gitlab(GITLAB_AUTH_REPOSITORY_TAGS_URL)
        self.assertEqual(result, [])
