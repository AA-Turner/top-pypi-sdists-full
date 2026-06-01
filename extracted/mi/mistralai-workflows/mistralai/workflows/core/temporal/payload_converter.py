import types
from typing import Any, Type, Union, get_args, get_origin

import structlog
import temporalio.api.common.v1
from pydantic import TypeAdapter
from pydantic_core import from_json
from temporalio.contrib.pydantic import PydanticJSONPlainPayloadConverter
from temporalio.converter import (
    CompositePayloadConverter,
    DefaultPayloadConverter,
    EncodingPayloadConverter,
    JSONPlainPayloadConverter,
)

from mistralai.workflows.core.encoding import CUSTOM_ENCODING_FORMAT, LEGACY_ENCODING_FORMAT
from mistralai.workflows.models import PayloadMetadataKeys, PayloadWithContext

logger = structlog.get_logger(__name__)


class WithContextJSONPayloadConverter(EncodingPayloadConverter):
    """Custom payload converter for the "json/wf_v1" encoding format.

    Handles PayloadWithContext values: deserializes the inner payload
    to the requested type hint, while preserving the surrounding context.
    Workers unwrap the payload before forwarding it to the activity.
    """

    @property
    def encoding(self) -> str:
        return CUSTOM_ENCODING_FORMAT

    def _allows_none(self, type_hint: Type | None) -> bool:
        if type_hint is None:
            return True
        if type_hint is type(None):
            return True
        if get_origin(type_hint) is Union:
            return type(None) in get_args(type_hint)
        if isinstance(type_hint, types.UnionType):
            return type(None) in type_hint.__args__
        return False

    def from_payload(
        self,
        payload: temporalio.api.common.v1.Payload,
        type_hint: Type | None = None,
    ) -> Any:
        try:
            payload_with_context = PayloadWithContext.model_validate_json(payload.data)
        except ValueError:
            return None

        # Always deserialize JSON payload to Python object
        python_obj = from_json(payload_with_context.payload)
        if type_hint is not None:
            # Allow null values to be deserialized
            if python_obj is None and not self._allows_none(type_hint):
                python_obj = {}
            payload_with_context.payload = TypeAdapter(type_hint).validate_python(python_obj)
        else:
            payload_with_context.payload = python_obj
        return payload_with_context

    def to_payload(self, value: Any) -> temporalio.api.common.v1.Payload | None:
        if not isinstance(value, PayloadWithContext):
            return None
        return temporalio.api.common.v1.Payload(
            metadata={PayloadMetadataKeys.ENCODING: CUSTOM_ENCODING_FORMAT.encode()},
            data=value.model_dump_json().encode(),
        )


class LegacyWithContextJSONPayloadConverter(WithContextJSONPayloadConverter):
    """Read-only converter for the legacy "json/abraxas_v1" encoding.

    Supports decoding payloads created with the old encoding format,
    but always returns None from to_payload to prevent creating new
    payloads with the legacy encoding.
    """

    @property
    def encoding(self) -> str:
        return LEGACY_ENCODING_FORMAT

    def to_payload(self, value: Any) -> temporalio.api.common.v1.Payload | None:
        return None


class MistralWorkflowsPayloadConverter(CompositePayloadConverter):
    def __init__(self) -> None:
        converters: list[EncodingPayloadConverter] = []
        for converter in DefaultPayloadConverter.default_encoding_payload_converters:
            if isinstance(converter, JSONPlainPayloadConverter):
                converters.extend(
                    [
                        WithContextJSONPayloadConverter(),
                        LegacyWithContextJSONPayloadConverter(),
                        PydanticJSONPlainPayloadConverter(),
                    ]
                )
            else:
                converters.append(converter)

        super().__init__(*converters)
