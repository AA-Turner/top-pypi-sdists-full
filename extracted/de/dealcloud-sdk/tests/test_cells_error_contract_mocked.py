"""Unit mock tests for Cells write error-handling parity with Rows."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from intapp_rest_client.exceptions import HttpError
from intapp_rest_client.models import ErrorHandling

from dealcloud_sdk.cells.dealcloud_cells import DealCloudCells
from dealcloud_sdk.data.models import BatchResult, RowsWriteResult
from dealcloud_sdk.utils.process_response_errors import DealCloudValidationError

from tests.fixtures.row_api_responses import SCHEMA_FIELDS_GET_RESPONSE
from tests.test_row_error_contract_mocked import _schema_get_side_effect

pytestmark = pytest.mark.row_error_contract

SITE = "test.dealcloud.com"

UPDATE_OK_WITH_ORPHAN_ERROR = [
    {"EntryId": 100, "Name": "Acme"},
    {"EntryId": 200, "Errors": [{"field": "X", "code": 1, "description": "fail"}]},
]

UPDATE_IN_BATCH_ERROR = [
    {"EntryId": 100, "Errors": [{"field": "Name", "code": 5009, "description": "fail"}]},
]


def _cells_client(mock_class: MagicMock, mock_client: MagicMock) -> DealCloudCells:
    mock_class.return_value = mock_client
    dc = DealCloudCells(site_url=SITE, client_id="cid", client_secret="sec")
    dc._schema = MagicMock()
    return dc


def _field_mock(api_name: str, field_id: int):
    field = MagicMock()
    field.id = field_id
    field.apiName = api_name
    return field


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestWriteCellsRowErrorContract:
    def _setup(self, mock_class, put_return):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.put.return_value = put_return
        dc = _cells_client(mock_class, mock_client)
        dc.get_field_by_api_name = MagicMock(
            side_effect=lambda _oid, name: _field_mock(name, 10 if name == "Name" else 11)
        )
        return dc

    @patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
    def test_write_cells_mixed_batch_default_list(self, _v, mock_class):
        dc = self._setup(mock_class, UPDATE_OK_WITH_ORPHAN_ERROR)
        result = dc.write_cells(
            "Company",
            [{"EntryId": 100, "Name": "x"}],
            mode="update",
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["EntryId"] == 100

    @patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
    def test_write_cells_raise_on_row_errors(self, _v, mock_class):
        dc = self._setup(mock_class, UPDATE_IN_BATCH_ERROR)
        with pytest.raises(DealCloudValidationError):
            dc.write_cells(
                "Company",
                [{"EntryId": 100, "Name": "x"}],
                mode="update",
                raise_on_row_errors=True,
            )

    @patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
    def test_write_cells_write_result(self, _v, mock_class):
        dc = self._setup(mock_class, UPDATE_IN_BATCH_ERROR)
        result = dc.write_cells(
            "Company",
            [{"EntryId": 100, "Name": "x"}],
            mode="update",
            output="write_result",
        )
        assert isinstance(result, RowsWriteResult)
        assert result.has_row_errors

    @patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
    def test_write_cells_collect_batch_result(self, _v, mock_class):
        dc = self._setup(mock_class, UPDATE_IN_BATCH_ERROR)
        result = dc.write_cells(
            "Company",
            [{"EntryId": 100, "Name": "x"}],
            mode="update",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(result, BatchResult)
        assert len(result.row_errors) == 1

    @patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
    def test_write_cells_collect_transport_error(self, _v, mock_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        err = HttpError(502, "bad gateway", {"message": "bad gateway"}, {})
        mock_client.put.side_effect = err
        dc = _cells_client(mock_class, mock_client)
        dc.get_field_by_api_name = MagicMock(return_value=_field_mock("Name", 10))

        result = dc.write_cells(
            "Company",
            [{"EntryId": 100, "Name": "x"}],
            mode="update",
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(result, BatchResult)
        assert len(result.errors) == 1


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestDeleteCellsRowErrorContract:
    def test_delete_cells_raise_on_row_errors(self, mock_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.delete.return_value = [
            {"EntryId": 100},
            {"EntryId": 200, "Errors": [{"code": 5009, "description": "fail"}]},
        ]
        dc = _cells_client(mock_class, mock_client)

        with pytest.raises(DealCloudValidationError):
            dc.delete_cells("Company", [100, 200], raise_on_row_errors=True)

    def test_delete_cells_collect_returns_batch_result(self, mock_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        err = HttpError(502, "bad gateway", {"message": "bad gateway"}, {})
        mock_client.delete.side_effect = err
        dc = _cells_client(mock_class, mock_client)

        result = dc.delete_cells(
            "Company",
            [100, 200],
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(result, BatchResult)
        assert len(result.errors) == 1
