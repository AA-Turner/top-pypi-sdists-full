from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Optional, Type, TypeVar, Union

from benchling_api_client.v2.stable.extensions import NotPresentError
from benchling_api_client.v2.types import UNSET, Unset
from dataclasses_json import DataClassJsonMixin

from benchling_sdk.models import CustomFields, Field, Fields, SchemaFieldsQueryParam

D = TypeVar("D", bound="DeserializableModel")
T = TypeVar("T")


@dataclass
class SerializableModel(DataClassJsonMixin):
    """
    Provide an interface for serialization of a custom model.

    For serializing models when using raw API calls (e.g., Benchling.api).
    Override serialize() for customized behavior.
    """

    # Not named to_dict() to avoid conflicts with DataClassJsonMixin
    def serialize(self) -> Dict[str, Any]:
        """Serialize the class attributes into a dict."""
        all_values = super().to_dict()
        # Filter out any Unset values
        return {key: value for key, value in all_values.items() if not isinstance(value, Unset)}


@dataclass
class DeserializableModel(DataClassJsonMixin):
    """
    Provide an interface for deserialization to a custom model.

    For deserializing models when using raw API calls (e.g., Benchling.api)
    Override deserialize() for customized behavior.
    """

    # Not named from_dict() to avoid conflicts with DataClassJsonMixin
    @classmethod
    def deserialize(cls: Type[D], source_dict: Dict[str, Any]) -> D:
        """Deserialize the input dictionary into the model."""
        return cls.from_dict(source_dict)


@dataclass
class DeserializableModelNoContent(DeserializableModel):
    """Provide an interface deserialization to a custom model when the response may be empty."""

    pass


def optional_array_query_param(inputs: Optional[Iterable[str]]) -> Optional[str]:
    """
    Collapse an Iterable to a comma-separated string if present.

    Add leading and trailing quotes if the item contains "," and not quoted
    """
    return array_query_param(inputs) if inputs is not None else None


def array_query_param(inputs: Iterable[str]) -> str:
    """
    Collapse an Iterable to a comma-separated string.

    Add leading and trailing quotes if the item contains "," and not quoted
    """
    quoted_inputs = ['"' + item + '"' if "," in item and item[0] != '"' else item for item in inputs]
    return ",".join(quoted_inputs)


def fields(source: Dict[str, Dict[str, Any]]) -> Fields:
    """Marshal a dictionary into a Fields object."""
    deserialized_fields = Fields()
    for field_name, field_dict in source.items():
        # BNCH-22297: Workaround to deal with the fact that `Field` is not correctly deserialized.
        deserialized_fields[field_name] = Field(value=field_dict["value"])
    return deserialized_fields


def custom_fields(source: Dict[str, Any]) -> CustomFields:
    """Marshal a dictionary into a CustomFields object."""
    return CustomFields.from_dict(source)


def unset_as_none(attr_fn: Callable[[], T]) -> Optional[T]:
    """Given an attribute accessor that may raise a NotPresentError, produces an Optional[] where the NotPresentError will be treated as None."""
    try:
        return attr_fn()
    except NotPresentError:
        return None


def schema_fields_query_param(schema_fields: Optional[Dict[str, Any]]) -> Optional[SchemaFieldsQueryParam]:
    """Prefix keys with 'schemaField' for querying fields in list endpoints."""
    return (
        SchemaFieldsQueryParam.from_dict(
            {f"schemaField.{field}": value for field, value in schema_fields.items()}
        )
        if schema_fields
        else None
    )


def none_as_unset(val: Optional[T]) -> Union[T, Unset]:
    """Convert a value to UNSET if None safely."""
    return UNSET if val is None else val
