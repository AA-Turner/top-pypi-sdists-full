"""Annotate Pydantic models for use alongside ``UploadFile``.

Provides :func:`file_upload_body` which builds a three-layer ``Annotated``
type that preserves model fields in OpenAPI, attaches examples for the
Swagger UI plugin, and aliases the form field with the model name.

Also provides :func:`unwrap_json_schema` which fixes Pydantic's
``Json[Model]`` wrapping so Swagger UI renders the model's fields instead
of a plain string input.
"""

from typing import Annotated

from pydantic import BaseModel
from pydantic.json_schema import GetJsonSchemaHandler, JsonSchemaValue
from pydantic_core import CoreSchema


def unwrap_json_schema(example: dict | None = None):
    """Pydantic JSON schema override that unwraps ``contentSchema``.

    When a field is typed as ``Json[Model]``, Pydantic wraps the schema
    in a ``contentSchema`` envelope.  Swagger UI doesn't understand that
    wrapper and renders a plain string input.  This override inlines the
    inner schema so Swagger renders the model's fields directly.
    """

    class _NotAsJson:
        @classmethod
        def __get_pydantic_json_schema__(
            cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
        ) -> JsonSchemaValue:
            json_schema = handler(core_schema)
            return {
                **(json_schema.get("contentSchema", json_schema)),
                **({"example": example} if example is not None else {}),
            }

    return _NotAsJson


def file_upload_body(
    model: type[BaseModel],
    examples: dict,
    default_key: str | None = None,
    name: str | None = None,
):
    """Annotate a Pydantic model for use alongside ``UploadFile``.

    When a FastAPI endpoint accepts both a JSON body **and** a file
    upload, the request must be sent as ``multipart/form-data``.
    FastAPI requires the JSON portion to be wrapped in ``Json[...]``
    and sent as a form field, but that breaks Swagger UI's schema
    rendering and example dropdown.  This factory builds the correct
    three-layer ``Annotated`` type that:

    1. Preserves the model's fields in the OpenAPI schema
       (via :func:`unwrap_json_schema`)
    2. Attaches ``openapi_examples`` so the file upload plugin can
       render them in Swagger UI
    3. Aliases the form field with the model name (camelCase)

    Parameters
    ----------
    model:
        The Pydantic model class for the JSON body.
    examples:
        A dict of ``{key: Example(...)}`` for the Swagger UI dropdown.
    default_key:
        Key in *examples* whose ``value`` is shown as the inline
        schema example before the user opens the dropdown.  ``None``
        omits the inline example.
    name:
        Schema name for the generated body wrapper in OpenAPI's
        ``components/schemas``.  If ``None`` (default), derived from
        the model class name (e.g. ``DocumentRequest`` →
        ``DocumentRequestBody``).  The schema patcher renames the
        auto-generated ``Body_*`` key to this value.

    Returns
    -------
    type
        An ``Annotated`` type suitable for use as an endpoint parameter.

    Example
    -------
    ::

        from fastapi.openapi.models import Example

        my_examples = {
            "basic": Example(
                summary="Basic request",
                value={"name": "Acme"},
            ),
        }
        MyRequest = file_upload_body(MyModel, my_examples, "basic")

        @router.post("/upload")
        async def upload(
            request: MyRequest,
            file: Optional[UploadFile] = None,
        ):
            ...
    """
    from fastapi import Body, Form
    from pydantic import Json

    schema_name = name or f"{model.__name__}Body"
    field_alias = model.__name__[0].lower() + model.__name__[1:]
    default_value = dict(examples[default_key]).get("value") if default_key else None
    body = Annotated[model, Body(openapi_examples=examples)]  # type: ignore[valid-type]
    return Annotated[  # type: ignore[return-value]
        Json[body],  # type: ignore[valid-type,misc]
        unwrap_json_schema(default_value),
        Form(
            alias=field_alias,
            openapi_examples=examples,
            json_schema_extra={"x-schema-name": schema_name},
        ),
    ]
