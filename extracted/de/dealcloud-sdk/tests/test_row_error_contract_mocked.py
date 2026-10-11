"""
Unit mock TDD tests for the Rows API row-error contract.

HTTP 2xx with per-row Errors: SDK splits indexed failures, retries clean rows once,
returns committed rows only. Opt-in raise_on_row_errors after recovery.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from intapp_rest_client.exceptions import HttpError
from intapp_rest_client.models import ErrorHandling

from dealcloud_sdk import DealCloud
from dealcloud_sdk.data.dealcloud_data import DealCloudData
from dealcloud_sdk.data.models import BatchResult, RowsWriteResult
from dealcloud_sdk.data.write_recovery import recover_payload_write
from dealcloud_sdk.utils.process_response_errors import (
    DealCloudValidationError,
    map_row_errors_to_indices,
    process_errors,
    split_row_results,
)

from tests.fixtures.row_api_responses import (
    INSERT_MIXED_BATCH,
    INSERT_ROW_OK,
    MIXED_BATCH,
    ROW_ERROR_5009,
    ROW_OK,
    SCHEMA_FIELDS_GET_RESPONSE,
)

pytestmark = pytest.mark.row_error_contract

SITE = "test.dealcloud.com"
CREDS = {"site_url": SITE, "client_id": "cid", "client_secret": "sec"}

TWO_ROW_UPDATE = [
    {"EntryId": 100, "Name": "a"},
    {"EntryId": 200, "Name": "b"},
]

TWO_ROW_INSERT = [
    {"Name": "a"},
    {"Name": "b"},
]


def _dealcloud_data(mock_class: MagicMock, mock_client: MagicMock) -> DealCloudData:
    mock_class.return_value = mock_client
    return DealCloudData(
        site_url=SITE,
        client_id="cid",
        client_secret="sec",
    )


def _schema_get_side_effect(url: str):
    if "entryTypes" in url and "fields" not in url:
        return [{"id": 1, "apiName": "Company", "singularName": "C", "pluralName": "Cs"}]
    if "allfields" in url or "/fields" in url:
        return SCHEMA_FIELDS_GET_RESPONSE
    return []


class TestProcessErrorsContract:
    """Pure process_errors / split_row_results contract."""

    def test_split_row_results_mixed(self):
        ok_rows, error_rows = split_row_results(MIXED_BATCH)
        assert len(ok_rows) == 1
        assert len(error_rows) == 1
        assert ok_rows[0]["EntryId"] == 100
        assert error_rows[0]["EntryId"] == 200

    def test_process_errors_default_logs_no_raise(self):
        returned = process_errors(MIXED_BATCH, raise_on_row_errors=False)
        assert len(returned) == 1
        assert returned[0]["EntryId"] == 200

    def test_process_errors_raise_on_row_errors(self):
        with pytest.raises(DealCloudValidationError) as exc_info:
            process_errors(MIXED_BATCH, raise_on_row_errors=True)
        assert exc_info.value.row_errors == [ROW_ERROR_5009]

    def test_row_errors_preserve_entry_id_and_codes(self):
        with pytest.raises(DealCloudValidationError) as exc_info:
            process_errors([ROW_ERROR_5009], raise_on_row_errors=True)
        row = exc_info.value.row_errors[0]
        assert row["EntryId"] == 200
        assert exc_info.value.errors[0]["code"] == 5009
        assert "not unique" in exc_info.value.errors[0]["description"]

    def test_map_row_errors_to_indices_update(self):
        indices = map_row_errors_to_indices(TWO_ROW_UPDATE, [ROW_ERROR_5009], is_insert=False)
        assert indices == {1}

    def test_map_row_errors_to_indices_insert(self):
        batch = [{"Name": "a"}, {"Name": "b"}]
        err = {"EntryId": -2, "Errors": [{"field": "Name", "code": 1, "description": "bad"}]}
        indices = map_row_errors_to_indices(batch, [err], is_insert=True)
        assert indices == {1}


class TestRecoverPayloadWrite:
    def test_retry_succeeds_after_split(self):
        calls: list[list[dict]] = []

        def send_once(payload: list[dict]) -> list[dict]:
            calls.append(payload)
            if len(calls) == 1:
                return MIXED_BATCH
            return [ROW_OK]

        outcome = recover_payload_write(TWO_ROW_UPDATE, send_once, is_insert=False)
        assert len(calls) == 2
        assert len(outcome.ok_rows) == 1
        assert outcome.ok_rows[0]["EntryId"] == 100
        assert len(outcome.row_errors) == 1
        assert outcome.row_errors[0]["EntryId"] == 200

    def test_retry_batch_error_fails_all_retry_rows_no_third_call(self):
        calls: list[list[dict]] = []

        def send_once(payload: list[dict]) -> list[dict]:
            calls.append(payload)
            if len(calls) == 1:
                return MIXED_BATCH
            return MIXED_BATCH

        outcome = recover_payload_write(TWO_ROW_UPDATE, send_once, is_insert=False)
        assert len(calls) == 2
        assert outcome.ok_rows == []
        assert len(outcome.row_errors) == 2
        assert len(outcome.failed_inputs) == 2


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestUpdateDataRowErrorContract:
    """update_data: automatic split-and-retry per HTTP payload."""

    def _data(self, mock_class, put_side_effect):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.put.side_effect = put_side_effect
        return _dealcloud_data(mock_class, mock_client)

    def test_update_mixed_batch_returns_committed_rows_only(
        self, _mock_validate, mock_class
    ):
        data = self._data(mock_class, [MIXED_BATCH, [ROW_OK]])
        result = data.update_data("Company", TWO_ROW_UPDATE)
        assert len(result) == 1
        assert result[0]["EntryId"] == 100

    def test_update_mixed_batch_error_row_in_write_result(self, _mock_validate, mock_class):
        data = self._data(mock_class, [MIXED_BATCH, [ROW_OK]])
        result = data.update_data("Company", TWO_ROW_UPDATE, output="write_result")
        assert isinstance(result, RowsWriteResult)
        assert len(result.ok_rows) == 1
        assert len(result.row_errors) == 1
        assert result.row_errors[0]["Errors"][0]["code"] == 5009

    def test_update_mixed_batch_raise_on_row_errors(self, _mock_validate, mock_class):
        data = self._data(mock_class, [MIXED_BATCH, [ROW_OK]])
        with pytest.raises(DealCloudValidationError) as exc_info:
            data.update_data(
                "Company",
                TWO_ROW_UPDATE,
                raise_on_row_errors=True,
            )
        assert len(exc_info.value.row_errors) == 1
        assert exc_info.value.row_errors[0]["EntryId"] == 200

    def test_update_all_ok_no_raise(self, _mock_validate, mock_class):
        data = self._data(mock_class, [[ROW_OK]])
        result = data.update_data("Company", [{"EntryId": 100, "Name": "x"}])
        assert len(result) == 1
        assert result[0]["EntryId"] == 100
        assert "Errors" not in result[0]


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestInsertDataRowErrorContract:
    """insert_data: automatic split-and-retry via post."""

    def _data(self, mock_class, post_side_effect):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.post.side_effect = post_side_effect
        return _dealcloud_data(mock_class, mock_client)

    def test_insert_mixed_batch_returns_committed_rows_only(self, _mock_validate, mock_class):
        data = self._data(mock_class, [INSERT_MIXED_BATCH, [INSERT_ROW_OK]])
        result = data.insert_data("Company", TWO_ROW_INSERT)
        assert len(result) == 1
        assert result[0]["EntryId"] == 1001

    def test_insert_mixed_batch_raise_on_row_errors(self, _mock_validate, mock_class):
        data = self._data(mock_class, [INSERT_MIXED_BATCH, [INSERT_ROW_OK]])
        with pytest.raises(DealCloudValidationError) as exc_info:
            data.insert_data("Company", TWO_ROW_INSERT, raise_on_row_errors=True)
        assert len(exc_info.value.row_errors) == 1


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestUpdateDataCollectRowErrors:
    def test_update_collect_populates_batch_result_row_errors(
        self, _mock_validate, mock_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.put.side_effect = [MIXED_BATCH, [ROW_OK]]
        data = _dealcloud_data(mock_class, mock_client)

        result = data.update_data(
            "Company",
            TWO_ROW_UPDATE,
            error_handling=ErrorHandling.COLLECT,
        )

        assert isinstance(result, BatchResult)
        assert len(result.row_errors) == 1
        assert result.row_errors[0]["EntryId"] == 200
        assert result.total_failed >= 1
        assert result.total_succeeded == 1


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestUpsertDataRowErrorContract:
    """upsert_data: delegates to insert/update; same row-error contract."""

    def _data(self, mock_class, put_side_effect=None, post_side_effect=None):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        if put_side_effect is not None:
            mock_client.put.side_effect = put_side_effect
        if post_side_effect is not None:
            mock_client.post.side_effect = post_side_effect
        return _dealcloud_data(mock_class, mock_client)

    def test_upsert_mixed_batch_returns_committed_rows_only(self, _mock_validate, mock_class):
        data = self._data(mock_class, put_side_effect=[MIXED_BATCH, [ROW_OK]])
        result = data.upsert_data("Company", TWO_ROW_UPDATE)
        assert len(result) == 1
        assert result[0]["EntryId"] == 100

    def test_upsert_mixed_batch_raise_on_row_errors(self, _mock_validate, mock_class):
        data = self._data(mock_class, put_side_effect=[MIXED_BATCH, [ROW_OK]])
        with pytest.raises(DealCloudValidationError) as exc_info:
            data.upsert_data(
                "Company",
                TWO_ROW_UPDATE,
                raise_on_row_errors=True,
            )
        assert len(exc_info.value.row_errors) == 1

    def test_upsert_collect_returns_batch_result(self, _mock_validate, mock_class):
        data = self._data(mock_class, put_side_effect=[MIXED_BATCH, [ROW_OK]])
        result = data.upsert_data(
            "Company",
            TWO_ROW_UPDATE,
            error_handling=ErrorHandling.COLLECT,
        )
        assert isinstance(result, BatchResult)
        assert len(result.row_errors) == 1

    def test_upsert_write_result(self, _mock_validate, mock_class):
        data = self._data(mock_class, put_side_effect=[MIXED_BATCH, [ROW_OK]])
        result = data.upsert_data(
            "Company",
            TWO_ROW_UPDATE,
            output="write_result",
        )
        assert isinstance(result, RowsWriteResult)
        assert result.has_row_errors


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestDeleteDataRowErrorContract:
    """delete_data: row Errors in body; opt-in raise; COLLECT row_errors."""

    def test_delete_returns_committed_rows_only(self, _mock_validate, mock_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.delete.side_effect = [MIXED_BATCH, [ROW_OK]]
        data = _dealcloud_data(mock_class, mock_client)

        result = data.delete_data("Company", [100, 200])

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["EntryId"] == 100

    def test_delete_raise_on_row_errors(self, _mock_validate, mock_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.delete.side_effect = [MIXED_BATCH, [ROW_OK]]
        data = _dealcloud_data(mock_class, mock_client)

        with pytest.raises(DealCloudValidationError) as exc_info:
            data.delete_data("Company", [100, 200], raise_on_row_errors=True)
        assert len(exc_info.value.row_errors) == 1

    def test_delete_collect_populates_batch_result_row_errors(self, _mock_validate, mock_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.delete.side_effect = [MIXED_BATCH, [ROW_OK]]
        data = _dealcloud_data(mock_class, mock_client)

        result = data.delete_data(
            "Company",
            [100, 200],
            error_handling=ErrorHandling.COLLECT,
        )

        assert isinstance(result, BatchResult)
        assert len(result.row_errors) == 1
        assert result.row_errors[0]["EntryId"] == 200
        assert result.total_failed >= 1


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestHttpTransportContract:
    def test_update_put_502_raises_http_error(self, _mock_validate, mock_class):
        err = HttpError(502, "bad gateway", {"message": "bad gateway"}, {})
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.put.side_effect = err
        data = _dealcloud_data(mock_class, mock_client)

        with pytest.raises(HttpError) as exc_info:
            data.update_data("Company", [{"EntryId": 1, "Name": "x"}])
        assert exc_info.value.status_code == 502


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestRowsWriteResultContract:
    def test_update_output_write_result_has_row_errors_property(
        self, _mock_validate, mock_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.put.side_effect = [MIXED_BATCH, [ROW_OK]]
        mock_class.return_value = mock_client
        dc = DealCloud(**CREDS)
        dc._schema = MagicMock()

        result = dc.update_data(
            "Company",
            TWO_ROW_UPDATE,
            output="write_result",
        )
        assert isinstance(result, RowsWriteResult)
        assert len(result.ok_rows) == 1
        assert result.has_row_errors
        assert len(result.row_errors) == 1
        assert result.row_errors[0]["EntryId"] == 200
        assert len(result.failed_inputs) == 1


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
@patch("dealcloud_sdk.data.write.validate_field_mapping", return_value=True)
class TestConfigRaiseOnRowErrorsDefault:
    def test_config_default_raises_without_explicit_param(self, _mock_validate, mock_class):
        from dealcloud_sdk.models.factory_models import DealCloudConfig

        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.put.side_effect = [MIXED_BATCH, [ROW_OK]]
        mock_class.return_value = mock_client

        config = DealCloudConfig(
            siteUrl=SITE,
            clientId="cid",
            clientSecret="sec",
            raiseOnRowErrors=True,
        )
        dc = DealCloud(config=config)
        dc._schema = MagicMock()

        with pytest.raises(DealCloudValidationError):
            dc.update_data("Company", TWO_ROW_UPDATE)

    def test_per_call_false_overrides_config_default(self, _mock_validate, mock_class):
        from dealcloud_sdk.models.factory_models import DealCloudConfig

        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {}
        mock_client.get.side_effect = _schema_get_side_effect
        mock_client.put.side_effect = [MIXED_BATCH, [ROW_OK]]
        mock_class.return_value = mock_client

        config = DealCloudConfig(
            siteUrl=SITE,
            clientId="cid",
            clientSecret="sec",
            raiseOnRowErrors=True,
        )
        dc = DealCloud(config=config)
        dc._schema = MagicMock()

        result = dc.update_data(
            "Company",
            TWO_ROW_UPDATE,
            raise_on_row_errors=False,
        )
        assert len(result) == 1
