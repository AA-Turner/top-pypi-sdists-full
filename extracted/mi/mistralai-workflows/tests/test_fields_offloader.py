from unittest.mock import Mock, patch

import pytest
from mistralai.extra.workflows.encoding.config import StorageProvider
from pydantic import BaseModel

from mistralai.workflows.core.config.config import BlobStorageConfig, PayloadOffloadingConfig
from mistralai.workflows.core.encoding.fields_offloader import (
    FieldsOffloader,
    OffloadableField,
    OffloadableModel,
)
from tests.test_helpers import InMemoryBlobStorage


class FakePydanticModel(BaseModel):
    value: str = "model_value_123456789"


class FakeOffloadableModel(OffloadableModel):
    non_offloaded_field: str = "non_offloaded_field"

    field_str: OffloadableField[str] = OffloadableField[str](value="str_1234567890")
    field_model: OffloadableField[FakePydanticModel] = OffloadableField[FakePydanticModel](value=FakePydanticModel())

    field_list_1: OffloadableField[list[int]] = OffloadableField[list[int]](value=[1, 2, 3])
    field_list_2: OffloadableField[list[FakePydanticModel]] = OffloadableField[list[FakePydanticModel]](
        value=[FakePydanticModel()]
    )

    field_dict_1: OffloadableField[dict[str, str]] = OffloadableField[dict[str, str]](value={"key": "value"})
    field_dict_2: OffloadableField[dict[str, FakePydanticModel]] = OffloadableField[dict[str, FakePydanticModel]](
        value={"key": FakePydanticModel()}
    )


@pytest.fixture
def mock_blob_storage():
    return InMemoryBlobStorage()


@pytest.fixture
def offloading_config():
    return PayloadOffloadingConfig(
        min_size_bytes=10,
        storage_config=BlobStorageConfig(
            storage_provider=StorageProvider.AZURE,
            container_name="abraxas-temporal-payload",
            azure_connection_string="XXX",
        ),
    )


@pytest.fixture
def fields_offloader(offloading_config):
    return FieldsOffloader(offloading_config)


# Tests
class TestFieldsOffloader:
    @pytest.mark.asyncio
    async def test_offload_if_needed_disabled(self) -> None:
        obj = FakeOffloadableModel()
        disabled_offloader = FieldsOffloader(offloading_config=None)
        result = await disabled_offloader.offload_if_needed(obj, namespace="namespace", run_id="run_1234")
        assert result == obj

    @pytest.mark.asyncio
    async def test_offload_if_needed_too_small(self, fields_offloader, mock_blob_storage: InMemoryBlobStorage):
        obj = FakeOffloadableModel()
        fields_offloader.offloading_config.min_size_bytes = 10000
        with patch(
            "mistralai.workflows.core.encoding.fields_offloader.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            result = await fields_offloader.offload_if_needed(obj, namespace="namespace", run_id="run_1234")
            assert result == obj

            result = await fields_offloader.restore_if_needed(result)
            assert result == obj

    @pytest.mark.asyncio
    async def test_offloading(self, fields_offloader, mock_blob_storage: InMemoryBlobStorage) -> None:
        with patch(
            "mistralai.workflows.core.encoding.fields_offloader.get_blob_storage",
            side_effect=Mock(return_value=mock_blob_storage),
        ):
            obj = FakeOffloadableModel()
            result = await fields_offloader.offload_if_needed(obj, namespace="namespace", run_id="run_1234")

            assert result.field_str.value is None
            assert result.field_model.value is None
            assert result.field_list_1.value is None
            assert result.field_list_2.value is None
            assert result.field_dict_1.value is None
            assert result.field_dict_2.value is None

            assert result.field_str.blob_ref is not None
            assert result.field_model.blob_ref is not None
            assert result.field_list_1.blob_ref is not None
            assert result.field_list_2.blob_ref is not None
            assert result.field_dict_1.blob_ref is not None
            assert result.field_dict_2.blob_ref is not None

            result = await fields_offloader.restore_if_needed(result)
            assert result == obj
