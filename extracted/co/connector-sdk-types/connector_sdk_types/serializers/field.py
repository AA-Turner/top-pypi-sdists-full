import typing as t
from dataclasses import dataclass
from enum import Enum

import pydantic


class FieldType(str, Enum):
    SECRET = "SECRET"
    HIDDEN = "HIDDEN"
    MULTI_LINES = "MULTI_LINES"


class SemanticType(str, Enum):
    # Represents the ID of an account discovered by the connector
    ACCOUNT_ID = "account-id"
    # Represents the ID of an application discovered by the connector
    APPLICATION_ID = "application-id"
    # Represents the ID of an application instance discovered by the connector
    APPLICATION_INSTANCE_ID = "application-instance-id"
    # Represents an AWS external ID that can be used to authenticate with AWS
    AWS_EXTERNAL_ID = "aws-external-id"
    # Represents the ID of an entitlement discovered by the connector
    ENTITLEMENT_ID = "entitlement-id"
    # Represents the ID of a resource discovered by the connector
    RESOURCE_ID = "resource-id"
    # Represents the password of an account
    PASSWORD = "password"
    # Represents a cryptographic key pair that can be used to authenticate with a service
    KEY_PAIR = "key-pair"
    # Represents the custom attributes of an account
    CUSTOM_ATTRIBUTES = "custom-attributes"
    # Represents a client ID that can be used to authenticate with a service account
    SERVICE_ACCOUNT_CLIENT_ID = "service-account-client-id"
    # Represents a mapping from a SDK Enum to Customer provided Enum.
    ENUM_MAPPING = "enum-mapping"


@dataclass
class Discriminator:
    field: str
    expected_value: t.Any | None = None
    one_of_expected_values: list[t.Any] | None = None


def _extract_json_schema_extra(**kwargs) -> dict[str, t.Any]:
    json_schema_extra = (
        kwargs.pop("json_schema_extra") if "json_schema_extra" in kwargs else {}
    ) or {}
    return dict.copy(json_schema_extra)


def SecretField(*args, **kwargs):
    return AnnotatedField(*args, secret=True, **kwargs)


def HiddenField(*args, **kwargs):
    """
    A field we don't want a user to see + fill out, but not a secret.
    """
    return AnnotatedField(*args, hidden=True, **kwargs)


def AnnotatedField(
    *args,
    group: str | None = None,
    multiline: bool = False,
    secret: bool = False,
    primary: bool = True,
    semantic_type: SemanticType | None = None,
    hidden: bool = False,
    discriminator: Discriminator | None = None,
    enum_mapping: type[Enum] | None = None,
    unique: bool = False,
    **kwargs,
):
    """
    A Pydantic Model Field that will add Lumos-specific JSON Schema extensions to the model's
    JSON Schema. See the Pydantic Field documentation for more information on kwargs.

    :param group: The title of the group for the settings of this field. Lets you group fields in the UI under a heading. Sets `x-field_group`.
    :param multiline: Whether the field is a multi-line text field. Sets `x-multiline`.
    :param secret: Whether the field should be shown to the user, but obscured ala password. Sets `x-secret`.
    :param primary: Whether the field should be considered the "primary" value, e.g. email or user id. Sets `x-primary`.
    :param semantic_type: The semantic type of the field. See the SemanticType enum for more information. Sets `x-semantic`.
    :param hidden: Whether the field should be hidden from the user.
    :param discriminator: The field should be hidden from the user if the discriminator field doesn't have the expected value.
    :param unique: Whether this field should be used for fingerprinting/deduplication. Sets `x-unique`.

    """
    json_schema_extra = _extract_json_schema_extra(**kwargs)

    if group:
        json_schema_extra["x-field_group"] = group
    if multiline:
        json_schema_extra["x-field_type"] = FieldType.MULTI_LINES
        json_schema_extra["x-multiline"] = True
    if secret:
        json_schema_extra["x-field_type"] = FieldType.SECRET
        json_schema_extra["x-secret"] = True
    if not primary:
        json_schema_extra["x-primary"] = False
    if semantic_type:
        json_schema_extra["x-semantic"] = semantic_type.value
    if hidden:
        json_schema_extra["x-field_type"] = FieldType.HIDDEN
        json_schema_extra["x-hidden"] = True
    if enum_mapping:
        json_schema_extra["x-enum_mapping_options"] = list(enum_mapping.__members__.values())
        json_schema_extra["x-semantic"] = SemanticType.ENUM_MAPPING.value
        json_schema_extra["x-hidden"] = True
    if discriminator:
        json_schema_extra["x-discriminator"] = {
            "field": discriminator.field,
            "expected_value": discriminator.expected_value,
            "one_of_expected_values": discriminator.one_of_expected_values,
        }
    if unique:
        json_schema_extra["x-unique"] = True
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)
