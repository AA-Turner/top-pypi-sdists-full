from typing import Optional
from unittest import TestCase
from unittest.mock import Mock, call, patch

import click
from box import Box, BoxList

from montecarlodata.common.data import MonolithResponse
from montecarlodata.data_exports.data_exports import DataExportService
from montecarlodata.queries.data_exports import GET_DATA_EXPORT_URL
from montecarlodata.utils import GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG

SAMPLE_RAW = "loki"
SAMPLE_DATA_EXPORT = "MONITORS"
SAMPLE_DATA_EXPORT_URL = "https://montecarlodata.com"
SAMPLE_S3_DESTINATION = "s3://bucket/prefix/object"
SAMPLE_FS_DESTINATION = "file://folder1/folder2/object"


class MockRequest:
    raw = SAMPLE_RAW


class DataExportServiceTest(TestCase):
    def setUp(self) -> None:
        self._request_wrapper_mock = Mock(autospec=GqlWrapper)
        self._service = DataExportService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
        )

    @patch("montecarlodata.data_exports.data_exports.click")
    def test_echo_data_exports(self, click_mock):
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data=BoxList(
                [
                    {
                        "name": "MONITORS",
                        "title": "Monitors",
                        "description": "All monitors with aggregated properties, excluding deleted monitors.",
                    },
                    {
                        "name": "ASSETS",
                        "title": "Assets",
                        "description": "All assets with aggregated properties, excluding deleted assets.",
                    },
                    {
                        "name": "ALERTS",
                        "title": "Alerts",
                        "description": "All alerts in the last 90 days with aggregated properties.",
                    },
                    {
                        "name": "EVENTS",
                        "title": "Events",
                        "description": "All events in the last 90 days with aggregated properties.",
                    },
                ]
            ),
            errors=None,
        )

        self._service.echo_data_exports(table_format="plain")
        click_mock.echo.assert_called_once_with(
            "Data Export (Name)    Description\n"
            "Monitors (MONITORS)   "
            "All monitors with aggregated properties, excluding deleted monitors.\n"
            "Assets (ASSETS)       "
            "All assets with aggregated properties, excluding deleted assets.\n"
            "Alerts (ALERTS)       "
            "All alerts in the last 90 days with aggregated properties.\n"
            "Events (EVENTS)       "
            "All events in the last 90 days with aggregated properties."
        )

    def test_get_data_export_with_bad_scheme(self):
        with self.assertRaises(click.exceptions.Abort):
            self._service.get_data_export(data_export=SAMPLE_DATA_EXPORT, destination="foo")

        with self.assertRaises(click.exceptions.Abort):
            self._service.get_data_export(data_export=SAMPLE_DATA_EXPORT, destination="http://foo")

    @patch.object(DataExportService, "_save_data_export_to_disk")
    @patch.object(DataExportService, "_save_data_export_to_s3")
    def test_get_data_export_routing_s3(self, save_to_s3_mock, save_to_disk_mock):
        with self.assertRaises(click.exceptions.Abort):
            self._test_get_data_export_routing(destination=SAMPLE_S3_DESTINATION)

        save_to_disk_mock.assert_not_called()
        save_to_s3_mock.assert_not_called()

        self._test_get_data_export_routing(destination=SAMPLE_S3_DESTINATION, aws_profile="foo")

        save_to_disk_mock.assert_not_called()
        save_to_s3_mock.assert_called_once_with(
            data_export_url=SAMPLE_DATA_EXPORT_URL,
            destination="bucket/prefix/object",
            aws_profile="foo",
        )

    @patch.object(DataExportService, "_save_data_export_to_disk")
    @patch.object(DataExportService, "_save_data_export_to_s3")
    def test_get_data_export_routing_fs(self, save_to_s3_mock, save_to_disk_mock):
        self._test_get_data_export_routing(destination=SAMPLE_FS_DESTINATION)

        save_to_disk_mock.assert_called_once_with(
            data_export_url=SAMPLE_DATA_EXPORT_URL,
            destination="folder1/folder2/object",
            aws_profile=None,
        )
        save_to_s3_mock.assert_not_called()

    @patch("montecarlodata.data_exports.data_exports.click")
    @patch.object(DataExportService, "_get_data_export_url")
    @patch.object(DataExportService, "_save_data_export_to_disk")
    @patch.object(DataExportService, "_save_data_export_to_s3")
    def test_get_data_export_dry(self, save_to_s3_mock, save_to_disk_mock, get_mock, mock_click):
        get_mock.return_value = SAMPLE_DATA_EXPORT_URL

        service = DataExportService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
        )
        service.get_data_export(
            data_export=SAMPLE_DATA_EXPORT, destination=SAMPLE_FS_DESTINATION, dry=True
        )
        get_mock.assert_called_once_with(data_export=SAMPLE_DATA_EXPORT)
        mock_click.echo.assert_called_once_with(SAMPLE_DATA_EXPORT_URL)

        save_to_disk_mock.assert_not_called()
        save_to_s3_mock.assert_not_called()

    @patch("montecarlodata.data_exports.data_exports.click")
    @patch.object(DataExportService, "_get_data_export_url")
    def _test_get_data_export_routing(
        self, get_mock, click_mock, destination: str, aws_profile: Optional[str] = None
    ):
        get_mock.return_value = SAMPLE_DATA_EXPORT_URL

        service = DataExportService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
        )
        service.get_data_export(
            data_export=SAMPLE_DATA_EXPORT, destination=destination, aws_profile=aws_profile
        )
        get_mock.assert_called_once_with(data_export=SAMPLE_DATA_EXPORT)
        click_mock.echo.assert_has_calls(
            [
                call(f"Saving data export to '{destination}'."),
                call("Complete. Have a nice day!"),
            ]
        )
        self.assertEqual(click_mock.echo.call_count, 2)

    def test_get_data_export_url(self):
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data=Box({"url": SAMPLE_DATA_EXPORT_URL})
        )
        self.assertEqual(
            self._service._get_data_export_url(data_export=SAMPLE_DATA_EXPORT),
            SAMPLE_DATA_EXPORT_URL,
        )

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=GET_DATA_EXPORT_URL,
            operation="getDataExportUrl",
            service="data_exports_service",
            variables=dict(data_export_name=SAMPLE_DATA_EXPORT),
        )

    def test_get_data_export_url_not_available(self):
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data=Box({"url": None})
        )

        with self.assertRaises(click.exceptions.Abort):
            self._service._get_data_export_url(data_export=SAMPLE_DATA_EXPORT)

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=GET_DATA_EXPORT_URL,
            operation="getDataExportUrl",
            service="data_exports_service",
            variables=dict(data_export_name=SAMPLE_DATA_EXPORT),
        )

    @patch("montecarlodata.data_exports.data_exports.urllib")
    @patch("montecarlodata.data_exports.data_exports.mkdirs")
    def test_save_data_export_to_disk(self, mkdir_mock, urllib_mock):
        destination = "folder1/folder2/object"
        self._service._save_data_export_to_disk(
            data_export_url=SAMPLE_DATA_EXPORT_URL, destination=destination
        )
        mkdir_mock.assert_called_once_with("folder1/folder2")
        urllib_mock.request.urlretrieve.assert_called_once_with(SAMPLE_DATA_EXPORT_URL, destination)

    @patch("montecarlodata.data_exports.data_exports.urllib")
    @patch("montecarlodata.data_exports.data_exports.mkdirs")
    def test_save_data_export_to_disk_with_no_destination(self, mkdir_mock, urllib_mock):
        with self.assertRaises(click.exceptions.Abort):
            self._service._save_data_export_to_disk(
                data_export_url=SAMPLE_DATA_EXPORT_URL, destination=None
            )
        mkdir_mock.assert_not_called()
        urllib_mock.request.urlretrieve.assert_not_called()

    @patch("montecarlodata.data_exports.data_exports.AwsClientWrapper")
    @patch("montecarlodata.data_exports.data_exports.requests")
    def test_save_data_export_to_s3(self, request_mock, utils_mock):
        destination = "bucket/prefix/object"
        request_mock.get.return_value = MockRequest

        self._service._save_data_export_to_s3(
            data_export_url=SAMPLE_DATA_EXPORT_URL, destination=destination
        )
        request_mock.get.assert_called_once_with(SAMPLE_DATA_EXPORT_URL, stream=True)
        utils_mock().upload_stream_to_s3.assert_called_once_with(
            data=SAMPLE_RAW, bucket="bucket", key="prefix/object"
        )

    @patch("montecarlodata.data_exports.data_exports.AwsClientWrapper")
    @patch("montecarlodata.data_exports.data_exports.requests")
    def test_save_data_export_to_s3_with_bad_destination(self, request_mock, utils_mock):
        with self.assertRaises(click.exceptions.Abort):
            self._service._save_data_export_to_s3(
                data_export_url=SAMPLE_DATA_EXPORT_URL, destination="bucket"
            )
        request_mock.assert_not_called()
        utils_mock.assert_not_called()

        request_mock.reset_mock()
        utils_mock.reset_mock()

        with self.assertRaises(click.exceptions.Abort):
            self._service._save_data_export_to_s3(
                data_export_url=SAMPLE_DATA_EXPORT_URL, destination="bucket/"
            )
        request_mock.assert_not_called()
        utils_mock.assert_not_called()
