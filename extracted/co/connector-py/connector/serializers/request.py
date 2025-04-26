import typing as t
from dataclasses import dataclass
from enum import Enum

import pydantic


class FieldType(str, Enum):
    SECRET = "SECRET"
    HIDDEN = "HIDDEN"
    MULTI_LINES = "MULTI_LINES"


SemanticType = t.Literal[
    "account-id", "aws-external-id", "password", "key-pair", "custom-attributes"
]


@dataclass
class Discriminator:
    field: str
    expected_value: t.Any


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
    **kwargs,
):
    """
    A Pydantic Model Field that will add Lumos-specific JSON Schema extensions to the model's
    JSON Schema. See the Pydantic Field documentation for more information on kwargs.

    :param group: The title of the group for the settings of this field. Lets you group fields in the UI under a heading. Sets `x-field_group`.
    :param multiline: Whether the field is a multi-line text field. Sets `x-multiline`.
    :param secret: Whether the field should be shown to the user, but obscured ala password. Sets `x-secret`.
    :param primary: Whether the field should be considered the "primary" value, e.g. email or user id. Sets `x-primary`.
    :param semantic_type: The semantic type of the field. Currently only "account-id" is supported. Sets `x-semantic`.
    :param hidden: Whether the field should be hidden from the user.
    :param discriminator: The field should be hidden from the user if the discriminator field doesn't have the expected value.

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
        json_schema_extra["x-semantic"] = semantic_type
    if hidden:
        json_schema_extra["x-field_type"] = FieldType.HIDDEN
        json_schema_extra["x-hidden"] = True
    if discriminator:
        json_schema_extra["x-discriminator"] = {
            "field": discriminator.field,
            "expected_value": discriminator.expected_value,
        }
    return pydantic.Field(*args, json_schema_extra=json_schema_extra, **kwargs)


class AwsServiceAccount(pydantic.BaseModel):
    access_key_id: str = AnnotatedField(
        title="Account Access Key ID",
        description="The access key id of the AWS service account.",
        default="",
        hidden=True,
        secret=True,
    )
    secret_access_key: str = AnnotatedField(
        title="Account Secret Access Key",
        description="The secret access key of the AWS service account.",
        default="",
        hidden=True,
        secret=True,
    )
