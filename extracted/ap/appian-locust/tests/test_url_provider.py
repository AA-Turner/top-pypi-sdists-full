from appian_locust.utilities.url_provider import URL_PROVIDER_V1, URL_PATTERN_V1
from appian_locust.objects import Page, PageType
from unittest.mock import patch, MagicMock
from unittest import TestCase


class TestUrlProvider(TestCase):

    def setUp(self) -> None:
        self.sample_page = Page("test_page", PageType.INTERFACE, "site_stub")
        self.sample_nested_page = Page("test_page", PageType.INTERFACE, "site_stub", "group_name")

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_page_nav_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_page_nav_path(self.sample_page)

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-nav-top-level-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_page_nav_path_with_group(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_page_nav_path(self.sample_nested_page)

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-nav-nested-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_report_link_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_report_link_path(self.sample_page, "report_stub")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-top-level-report-link"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_record_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_record_path(self.sample_page, "opaque_id", "view")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-top-level-record-instance-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_record_path_with_group(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_record_path(self.sample_nested_page, "opaque_id", "view")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-nested-record-instance-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_record_page_path(self, expand_mock: MagicMock) -> None:
        sample_record_page = Page("test_page", PageType.RECORD, "site_stub")
        URL_PROVIDER_V1.get_page_path(sample_record_page)

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-top-level-record-type-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_report_page_path(self, expand_mock: MagicMock) -> None:
        sample_record_page = Page("test_page", PageType.REPORT, "site_stub")
        URL_PROVIDER_V1.get_page_path(sample_record_page)

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-top-level-report-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_action_page_path(self, expand_mock: MagicMock) -> None:
        sample_record_page = Page("test_page", PageType.ACTION, "site_stub")
        URL_PROVIDER_V1.get_page_path(sample_record_page)

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-top-level-action-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_interface_page_path(self, expand_mock: MagicMock) -> None:
        sample_record_page = Page("test_page", PageType.INTERFACE, "site_stub")
        URL_PROVIDER_V1.get_page_path(sample_record_page)

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-top-level-interface-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_task_attributes_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_task_attributes_path("task_id")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-task-attributes"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_task_status_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_task_status_path("task_id")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-task-status"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_task_form_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_task_form_path("task_id")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-task-form"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_site_page_redirect_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_site_page_redirect_path("site_name", "page_name")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-page-redirect"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_site_start_process_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_site_start_process_path(self.sample_page, "opaque_id", "cache_key")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-top-level-start-process-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_site_nested_page_start_process_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_site_start_process_path(self.sample_nested_page, "opaque_id", "cache_key")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-nested-start-process-page"])

    @patch("appian_locust.utilities.url_provider.expand")
    def test_get_site_nav_path(self, expand_mock: MagicMock) -> None:
        URL_PROVIDER_V1.get_site_nav_path("site_name")

        args, _ = expand_mock.call_args_list[0]
        self.assertEqual(args[0], URL_PATTERN_V1["x-data-request-site-nav"])
