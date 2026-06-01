import asyncio
import functools
import urllib.parse
import uuid
from typing import Any, Generic, Type, TypeVar, cast, get_args, get_origin

import orjson
import structlog
import temporalio.workflow
from mistralai.extra.workflows.encoding.storage.blob_storage import get_blob_storage
from pydantic import BaseModel, TypeAdapter
from pydantic.fields import FieldInfo

from mistralai.workflows.core.config.config import PayloadOffloadingConfig

logger = structlog.get_logger(__name__)
OffloadableSingleType = BaseModel | int | str | bytes
OffloadableCompositeType = OffloadableSingleType | list[OffloadableSingleType] | dict[str, OffloadableSingleType]
OffloadableType = TypeVar("OffloadableType", bound=OffloadableCompositeType)


class OffloadableModel(BaseModel): ...


class OffloadableFieldException(Exception): ...


class OffloadableField(BaseModel, Generic[OffloadableType]):
    value: OffloadableType | None
    blob_ref: str | None = None

    def get_value(self) -> OffloadableType:
        if self.value is None:
            if temporalio.workflow.in_workflow():
                raise OffloadableFieldException("Offloadable attributes cannot be accessed in a workflow context.")
            raise OffloadableFieldException("Offloadable attribute not loaded yet.")
        return self.value

    def serialized_value(self) -> bytes:
        """Convert a Python value to bytes."""
        if isinstance(self.value, bytes):
            return self.value
        adapter = TypeAdapter(type(self.value))
        python_obj = adapter.dump_python(self.value, mode="python")
        return orjson.dumps(python_obj)

    @classmethod
    def from_serialized(
        cls,
        data: bytes,
        type_hint: Type[OffloadableType],
    ) -> "OffloadableField[OffloadableType]":
        if type_hint is None or type_hint is type(None):
            return cls(value=None)

        if type_hint is bytes:
            return cls(value=cast(OffloadableType, data))

        if isinstance(type_hint, type) and issubclass(type_hint, BaseModel):
            return cls(value=cast(OffloadableType, type_hint.model_validate_json(data)))

        deserialized = orjson.loads(data)

        origin = get_origin(type_hint)
        args = get_args(type_hint)

        if origin is list:
            if args:
                element_type = args[0]
                adapter = TypeAdapter(cast(Any, list[element_type]))  # type: ignore
                validated = adapter.validate_python(deserialized)
                return cls(value=cast(OffloadableType, validated))
            return cls(value=cast(OffloadableType, deserialized))

        if origin is dict:
            if args and len(args) == 2:
                key_type, value_type = args
                adapter = TypeAdapter(cast(Any, dict[key_type, value_type]))  # type: ignore
                validated = adapter.validate_python(deserialized)
                return cls(value=cast(OffloadableType, validated))
            return cls(value=cast(OffloadableType, deserialized))

        adapter = TypeAdapter(type_hint)
        validated = adapter.validate_python(deserialized)
        return cls(value=cast(OffloadableType, validated))


class FieldsOffloaderException(Exception): ...


class FieldsOffloader:
    """Handles offloading and restoration of large payloads at activity boundaries."""

    BLOB_STORAGE_KEY_PREFIX = "temporal-activity-payload"

    def __init__(
        self,
        offloading_config: PayloadOffloadingConfig | None,
    ):
        self.offloading_config = offloading_config
        if self.offloading_config is not None and not self.offloading_config.storage_config:
            raise FieldsOffloaderException("Blob storage config is not set for activity payload offloading")

    @staticmethod
    def blob_storage_key_prefix(namespace: str, run_id: str) -> str:
        quote = functools.partial(urllib.parse.quote, safe="")
        return "/".join(
            [
                FieldsOffloader.BLOB_STORAGE_KEY_PREFIX,
                quote(namespace),
                quote(run_id),
            ]
        )

    def _estimate_size(self, obj: OffloadableModel) -> int:
        """Estimate object size in bytes."""
        return len(obj.model_dump_json())

    async def offload_if_needed(self, obj: Any, namespace: str, run_id: str) -> Any:
        if (
            self.offloading_config is None
            or not isinstance(obj, OffloadableModel)
            or self._estimate_size(obj) < self.offloading_config.min_size_bytes
        ):
            return obj

        # Proceed to offloading
        blob_ref_prefix = f"{FieldsOffloader.blob_storage_key_prefix(namespace, run_id)}/{uuid.uuid4()}"

        assert self.offloading_config.storage_config is not None

        tasks: list[asyncio.Task] = []
        async with get_blob_storage(self.offloading_config.storage_config) as blob_storage:
            for field_name, field_info in type(obj).model_fields.items():
                field_value = getattr(obj, field_name)
                if not isinstance(field_value, OffloadableField) or field_value.value is None:
                    continue

                quoted_field_name = urllib.parse.quote(field_name, safe="")
                blob_ref = f"{blob_ref_prefix}/{quoted_field_name}"

                tasks.append(
                    asyncio.create_task(
                        blob_storage.upload_blob(
                            key=blob_ref,
                            content=field_value.serialized_value(),
                        )
                    )
                )

                setattr(
                    obj,
                    field_name,
                    OffloadableField[Any](
                        value=None,
                        blob_ref=blob_ref,
                    ),
                )
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            for task_result in task_results:
                if isinstance(task_result, Exception):
                    logger.error("An error occurred while uploading blob", exception=str(task_result))
                    raise FieldsOffloaderException("An error occurred while uploading blob") from task_result

        return obj

    async def restore_if_needed(self, obj: Any) -> Any:
        if not isinstance(obj, OffloadableModel):
            return obj

        # First check if there are any blob_refs that need to be restored
        fields_to_restore: list[tuple[str, FieldInfo, str]] = []
        for field_name, field_info in type(obj).model_fields.items():
            field_value = getattr(obj, field_name)
            if isinstance(field_value, OffloadableField) and field_value.blob_ref is not None:
                fields_to_restore.append((field_name, field_info, field_value.blob_ref))

        if not fields_to_restore:
            return obj

        if self.offloading_config is None or self.offloading_config.storage_config is None:
            raise FieldsOffloaderException("Blob storage config is not set but blob restoration is required")

        tasks: list[tuple[str, FieldInfo, asyncio.Task]] = []
        async with get_blob_storage(self.offloading_config.storage_config) as blob_storage:
            for field_name, field_info, blob_ref in fields_to_restore:
                task = asyncio.create_task(blob_storage.get_blob(blob_ref))
                tasks.append((field_name, field_info, task))

            task_results = await asyncio.gather(*[task[2] for task in tasks], return_exceptions=True)

        for (field_name, field_info, _), task_result in zip(tasks, task_results):
            if isinstance(task_result, Exception):
                logger.error("An error occurred while trying to restore blob", exception=str(task_result))
                raise FieldsOffloaderException("An error occurred while trying to restore blob") from task_result

            inner_type = bytes
            if generic_meta := getattr(field_info.annotation, "__pydantic_generic_metadata__"):
                if "args" in generic_meta and len(generic_meta["args"]) > 0:
                    inner_type = generic_meta["args"][0]

            restored_field = OffloadableField.from_serialized(task_result, inner_type)  # type: ignore
            setattr(obj, field_name, restored_field)
        return obj
