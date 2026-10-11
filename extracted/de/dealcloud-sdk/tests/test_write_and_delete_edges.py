"""Edge-case unit tests for write.validate_field_mapping, insert/update progress, delete_data."""

from unittest.mock import MagicMock, patch

import pytest

from intapp_rest_client.exceptions import HttpError
from dealcloud_sdk.data.dealcloud_data import DealCloudData
from dealcloud_sdk.data.models import BatchResult
from dealcloud_sdk.data import write as write_mod
from intapp_rest_client.models import ErrorHandling


def _schema_client():
    mock_client = MagicMock()
    mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
    mock_client.get.return_value = [
        {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
    ]
    return mock_client


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestValidateFieldMappingListColumns:
    def test_accepts_list_of_column_names(self, mock_client_class):
        mock_client_class.return_value = _schema_client()
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        assert write_mod.validate_field_mapping(dc, "Company", ["Name", "EntryId"]) is True


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestInsertUpdateProgressCallbackFailures:
    def test_insert_data_progress_callback_failure_logged(self, mock_client_class):
        mock_client = _schema_client()
        mock_client.post.return_value = [{"EntryId": 1, "Success": True}]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        dc._logger = MagicMock()

        def boom(cur, tot):
            raise RuntimeError("progress")

        dc.insert_data("Company", [{"Name": "A"}], progress_callback=boom)
        dc._logger.warning.assert_called()

    def test_update_data_progress_callback_failure_logged(self, mock_client_class):
        mock_client = _schema_client()
        mock_client.put.return_value = [{"EntryId": 1, "Success": True}]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        dc._logger = MagicMock()

        def boom(cur, tot):
            raise RuntimeError("progress")

        dc.update_data(
            "Company",
            [{"EntryId": 1, "Name": "U"}],
            progress_callback=boom,
        )
        dc._logger.warning.assert_called()


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestDeleteDataEdges:
    def test_empty_records_collect_returns_batch_result(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        out = dc.delete_data(
            "Company",
            [],
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.total_requested == 0

    def test_page_size_capped_with_warning(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = [{"ok": True}]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with pytest.warns(UserWarning, match="page_size .* exceeds maximum"):
            dc.delete_data("Company", [1], page_size=50000)
        call_kw = mock_client.delete.call_args[1]
        assert len(call_kw["json"]) == 1

    def test_page_size_below_one_raises(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with pytest.raises(ValueError, match="page_size must be at least"):
            dc.delete_data("Company", [1], page_size=0)

    def test_single_batch_progress_callback_failure_logged(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = [{"deleted": [1]}]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        dc._logger = MagicMock()

        def boom(a, b):
            raise RuntimeError("cb")

        dc.delete_data("Company", [1], progress_callback=boom)
        dc._logger.warning.assert_called()

    def test_single_batch_non_list_delete_result_wrapped(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = {"raw": True}
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        out = dc.delete_data("Company", [1])
        assert out == [{"raw": True}]

    def test_multi_batch_parallel_delete_fail_fast(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = [[{"a": 1}], [{"b": 2}], [{"c": 3}]]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        out = dc.delete_data("Company", [1, 2, 3], page_size=1)
        assert isinstance(out, list)
        assert len(out) == 3

    def test_multi_batch_collect_with_payload_index_errors(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        def delete_side(url, json=None, **kwargs):
            if json == [30, 40]:
                raise HttpError(429, "Rate limited", {}, {})
            return [{"ok": True}]

        mock_client.delete.side_effect = delete_side
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        out = dc.delete_data(
            "Company",
            [10, 20, 30, 40],
            page_size=2,
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert out.total_failed == 2

    def test_multi_batch_progress_callback_failure(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = [[{"x": 1}], [{"x": 2}]]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        dc._logger = MagicMock()

        def boom(a, b):
            raise RuntimeError("cb")

        dc.delete_data(
            "Company",
            [1, 2],
            page_size=1,
            progress_callback=boom,
            error_handling=ErrorHandling.COLLECT,
        )
        dc._logger.warning.assert_called()

    def test_multi_batch_fail_fast_progress_callback_failure(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = [[{"a": 1}], [{"b": 2}], [{"c": 3}]]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        dc._logger = MagicMock()

        def boom(_a, _b):
            raise RuntimeError("cb")

        dc.delete_data(
            "Company",
            [1, 2, 3],
            page_size=1,
            progress_callback=boom,
            error_handling=ErrorHandling.FAIL_FAST,
        )
        dc._logger.warning.assert_called()

    def test_multi_batch_collect_mixed_list_and_scalar_results(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.side_effect = [[{"ok": True}], {"raw": True}]
        mock_client_class.return_value = mock_client
        dc = DealCloudData(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        out = dc.delete_data(
            "Company",
            [1, 2],
            page_size=1,
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(out, BatchResult)
        assert len(out.results) == 2
