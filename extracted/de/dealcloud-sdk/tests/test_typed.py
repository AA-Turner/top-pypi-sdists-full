"""Unit tests for dealcloud_sdk.data.typed (typed_read_data, typed_insert_data, typed_update_data)."""

import logging
from typing import Optional

import pytest
from pydantic import BaseModel, ValidationError
from unittest.mock import MagicMock, patch

from dealcloud_sdk.data.dealcloud_data import DealCloudData
from dealcloud_sdk.data.models import BatchResult, ReferenceFormat


class CompanyModel(BaseModel):
    """Minimal Pydantic model for tests."""
    EntryId: Optional[int] = None
    Name: str
    Industry: Optional[str] = None


class TestTypedReadData:
    """Tests for typed_read_data."""

    @patch('dealcloud_sdk.data.typed.read.read_data')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_typed_read_data_returns_list_of_models(self, mock_client_class, mock_read_data):
        mock_read_data.return_value = [
            {"EntryId": 1, "Name": "Acme", "Industry": "Tech"},
            {"EntryId": 2, "Name": "Beta", "Industry": "Finance"},
        ]
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        result = data.typed_read_data(CompanyModel, object_id="Company")

        assert len(result) == 2
        assert result[0].Name == "Acme"
        assert result[0].EntryId == 1
        assert result[1].Name == "Beta"
        mock_read_data.assert_called_once()
        call_kw = mock_read_data.call_args[1]
        assert call_kw["output"] == "list"
        assert call_kw["object_id"] == "Company"

    @patch('dealcloud_sdk.data.typed.read.read_data')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_typed_read_data_skip_validation_errors_skips_bad_row(self, mock_client_class, mock_read_data):
        mock_read_data.return_value = [
            {"EntryId": 1, "Name": "Acme", "Industry": "Tech"},
            {"EntryId": 2, "BadField": "invalid"},  # missing Name
        ]
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        result = data.typed_read_data(
            CompanyModel, object_id="Company", skip_validation_errors=True
        )

        assert len(result) == 1
        assert result[0].Name == "Acme"

    @patch('dealcloud_sdk.data.typed.read.read_data')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_typed_read_data_validation_error_raises_when_not_skipped(
        self, mock_client_class, mock_read_data
    ):
        mock_read_data.return_value = [{"EntryId": 1}]  # missing required Name
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        with pytest.raises(ValidationError, match="Name"):
            data.typed_read_data(CompanyModel, object_id="Company", skip_validation_errors=False)

    @patch("dealcloud_sdk.data.typed.read.read_data")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_read_data_passes_explicit_fields(
        self, mock_client_class, mock_read_data
    ):
        mock_read_data.return_value = [{"EntryId": 1, "Name": "Acme", "Industry": "Tech"}]
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        data.typed_read_data(
            CompanyModel, object_id="Company", fields=["EntryId", "Name"]
        )

        assert mock_read_data.call_args[1]["fields"] == ["EntryId", "Name"]


class TestTypedReadDataPolars:
    @patch("dealcloud_sdk.data.typed.read.read_data")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_read_data_polars_lazy_flag(self, mock_client_class, mock_read_data):
        mock_read_data.return_value = "lazy-frame"
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        out = data.typed_read_data_polars(CompanyModel, object_id="Co", lazy=True)
        assert out == "lazy-frame"
        assert mock_read_data.call_args[1]["output"] == "polars_lazy"

    @patch("dealcloud_sdk.data.typed.read.read_data")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_read_data_polars_eager(self, mock_client_class, mock_read_data):
        mock_read_data.return_value = "df"
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        out = data.typed_read_data_polars(CompanyModel, object_id="Co", lazy=False)
        assert out == "df"
        assert mock_read_data.call_args[1]["output"] == "polars"


class TestTypedReadDataStreaming:
    @patch("dealcloud_sdk.data.typed.streaming.read_data_streaming")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_read_data_streaming_yields_models(self, mock_client_class, mock_stream):
        mock_stream.return_value = iter(
            [[{"EntryId": 1, "Name": "A", "Industry": None}]]
        )
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        rows = list(data.typed_read_data_streaming(CompanyModel, object_id="Company"))
        assert len(rows) == 1
        assert rows[0].Name == "A"

    @patch("dealcloud_sdk.data.typed.streaming.read_data_streaming")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_read_data_streaming_skip_invalid(
        self, mock_client_class, mock_stream, caplog
    ):
        mock_stream.return_value = iter(
            [
                [{"EntryId": 1, "Name": "ok", "Industry": None}],
                [{"EntryId": 2, "Industry": "x"}],  # missing Name
            ]
        )
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        with caplog.at_level(logging.WARNING):
            rows = list(
                data.typed_read_data_streaming(
                    CompanyModel, object_id="Company", skip_validation_errors=True
                )
            )
        assert len(rows) == 1
        assert "Validation error" in caplog.text

    @patch("dealcloud_sdk.data.typed.streaming.read_data_streaming")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_read_data_streaming_validation_error_raises(
        self, mock_client_class, mock_stream
    ):
        mock_stream.return_value = iter([[{"EntryId": 9}]])
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        with pytest.raises(ValidationError):
            list(
                data.typed_read_data_streaming(
                    CompanyModel, object_id="Company", skip_validation_errors=False
                )
            )

    @patch("dealcloud_sdk.data.references.apply_reference_format")
    @patch("dealcloud_sdk.data.typed.streaming.read_data_streaming")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_read_data_streaming_applies_reference_format(
        self, mock_client_class, mock_stream, mock_apply
    ):
        mock_stream.return_value = iter(
            [[{"EntryId": 1, "Name": "raw", "Industry": None}]]
        )
        mock_apply.return_value = [{"EntryId": 1, "Name": "resolved", "Industry": None}]
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        rows = list(
            data.typed_read_data_streaming(
                CompanyModel,
                object_id="Company",
                reference_format=ReferenceFormat.NAME,
            )
        )
        assert rows[0].Name == "resolved"
        mock_apply.assert_called()


class TestTypedAreadDataStreaming:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    @pytest.mark.asyncio
    async def test_typed_aread_data_streaming(self, mock_client_class):
        async def fake_aread(*args, **kwargs):
            yield [{"EntryId": 1, "Name": "AsyncCo", "Industry": None}]

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        out = []
        with patch(
            "dealcloud_sdk.data.typed.streaming.aread_data_streaming", fake_aread
        ):
            async for row in data.typed_aread_data_streaming(
                CompanyModel, object_id="Company"
            ):
                out.append(row)
        assert len(out) == 1
        assert out[0].Name == "AsyncCo"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    @pytest.mark.asyncio
    async def test_typed_aread_skip_validation_errors(self, mock_client_class, caplog):
        async def fake_aread(*args, **kwargs):
            yield [{"EntryId": 1, "Name": "ok", "Industry": None}]
            yield [{"EntryId": 2, "Industry": "x"}]

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")

        out = []
        with (
            patch(
                "dealcloud_sdk.data.typed.streaming.aread_data_streaming", fake_aread
            ),
            caplog.at_level(logging.WARNING),
        ):
            async for row in data.typed_aread_data_streaming(
                CompanyModel, object_id="Company", skip_validation_errors=True
            ):
                out.append(row)
        assert len(out) == 1
        assert "Validation error" in caplog.text


class TestTypedInsertData:
    """Tests for typed_insert_data."""

    @patch('dealcloud_sdk.data.typed.write.insert_data')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_typed_insert_data_passes_models_as_dicts_and_returns_models(
        self, mock_client_class, mock_insert_data
    ):
        mock_insert_data.return_value = [
            {"EntryId": 101, "Name": "NewCo", "Industry": "Tech"},
        ]
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        models = [CompanyModel(Name="NewCo", Industry="Tech")]

        result = data.typed_insert_data("Company", models, CompanyModel)

        assert len(result) == 1
        assert result[0].EntryId == 101
        assert result[0].Name == "NewCo"
        mock_insert_data.assert_called_once()
        call_args = mock_insert_data.call_args[0]
        assert call_args[1] == "Company"  # object_id
        rows = call_args[2]  # data list
        assert rows[0]["Name"] == "NewCo"

    @patch("dealcloud_sdk.data.typed.write.insert_data")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_insert_data_batch_result(
        self, mock_client_class, mock_insert_data
    ):
        mock_insert_data.return_value = BatchResult(
            results=[{"EntryId": 200, "Name": "FromBatch", "Industry": "Tech"}]
        )
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        models = [CompanyModel(Name="FromBatch", Industry="Tech")]

        result = data.typed_insert_data("Company", models, CompanyModel)

        assert len(result) == 1
        assert result[0].EntryId == 200


class TestTypedUpdateData:
    """Tests for typed_update_data."""

    @patch('dealcloud_sdk.data.typed.write.update_data')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_typed_update_data_passes_models_and_returns_models(
        self, mock_client_class, mock_update_data
    ):
        mock_update_data.return_value = [
            {"EntryId": 1, "Name": "Acme Updated", "Industry": "Tech"},
        ]
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        models = [CompanyModel(EntryId=1, Name="Acme Updated", Industry="Tech")]

        result = data.typed_update_data("Company", models, CompanyModel)

        assert len(result) == 1
        assert result[0].EntryId == 1
        assert result[0].Name == "Acme Updated"
        mock_update_data.assert_called_once()
        call_args = mock_update_data.call_args[0]
        rows = call_args[2]  # data list (after self, object_id)
        assert rows[0]["EntryId"] == 1
        assert rows[0]["Name"] == "Acme Updated"

    @patch("dealcloud_sdk.data.typed.write.update_data")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_update_data_batch_result(
        self, mock_client_class, mock_update_data
    ):
        mock_update_data.return_value = BatchResult(
            results=[{"EntryId": 1, "Name": "Patched", "Industry": "Tech"}]
        )
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        models = [CompanyModel(EntryId=1, Name="Patched", Industry="Tech")]

        result = data.typed_update_data("Company", models, CompanyModel)

        assert result[0].Name == "Patched"


class TestTypedUpsertData:
    @patch("dealcloud_sdk.data.typed.write.upsert_data")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_typed_upsert_data_returns_models(self, mock_client_class, mock_upsert):
        mock_upsert.return_value = [
            {"EntryId": 50, "Name": "Upserted", "Industry": "Fin"},
        ]
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        data = DealCloudData(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        models = [CompanyModel(Name="Upserted", Industry="Fin")]

        result = data.typed_upsert_data(
            "Company", models, CompanyModel, "ExternalId"
        )

        assert len(result) == 1
        assert result[0].EntryId == 50
        mock_upsert.assert_called_once()
        assert mock_upsert.call_args[0][1] == "Company"
