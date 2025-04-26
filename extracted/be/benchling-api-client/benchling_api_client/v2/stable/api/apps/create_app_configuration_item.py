from typing import Any, cast, Dict, Optional, Union

import httpx

from ...client import Client
from ...extensions import UnknownType
from ...models.app_config_item_boolean_create import AppConfigItemBooleanCreate
from ...models.app_config_item_date_create import AppConfigItemDateCreate
from ...models.app_config_item_datetime_create import AppConfigItemDatetimeCreate
from ...models.app_config_item_float_create import AppConfigItemFloatCreate
from ...models.app_config_item_generic_create import AppConfigItemGenericCreate
from ...models.app_config_item_integer_create import AppConfigItemIntegerCreate
from ...models.app_config_item_json_create import AppConfigItemJsonCreate
from ...models.array_element_app_config_item import ArrayElementAppConfigItem
from ...models.bad_request_error import BadRequestError
from ...models.boolean_app_config_item import BooleanAppConfigItem
from ...models.date_app_config_item import DateAppConfigItem
from ...models.datetime_app_config_item import DatetimeAppConfigItem
from ...models.entity_schema_app_config_item import EntitySchemaAppConfigItem
from ...models.field_app_config_item import FieldAppConfigItem
from ...models.float_app_config_item import FloatAppConfigItem
from ...models.generic_api_identified_app_config_item import GenericApiIdentifiedAppConfigItem
from ...models.integer_app_config_item import IntegerAppConfigItem
from ...models.json_app_config_item import JsonAppConfigItem
from ...models.secure_text_app_config_item import SecureTextAppConfigItem
from ...models.text_app_config_item import TextAppConfigItem
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Union[
        AppConfigItemGenericCreate,
        AppConfigItemBooleanCreate,
        AppConfigItemIntegerCreate,
        AppConfigItemFloatCreate,
        AppConfigItemDateCreate,
        AppConfigItemDatetimeCreate,
        AppConfigItemJsonCreate,
        UnknownType,
    ],
) -> Dict[str, Any]:
    url = "{}/app-configuration-items".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    if isinstance(json_body, UnknownType):
        json_json_body = json_body.value
    elif isinstance(json_body, AppConfigItemGenericCreate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, AppConfigItemBooleanCreate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, AppConfigItemIntegerCreate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, AppConfigItemFloatCreate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, AppConfigItemDateCreate):
        json_json_body = json_body.to_dict()

    elif isinstance(json_body, AppConfigItemDatetimeCreate):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[
    Union[
        Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    if response.status_code == 201:

        def _parse_response_201(
            data: Union[Dict[str, Any]]
        ) -> Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ]:
            response_201: Union[
                ArrayElementAppConfigItem,
                DateAppConfigItem,
                DatetimeAppConfigItem,
                JsonAppConfigItem,
                EntitySchemaAppConfigItem,
                FieldAppConfigItem,
                BooleanAppConfigItem,
                IntegerAppConfigItem,
                FloatAppConfigItem,
                TextAppConfigItem,
                GenericApiIdentifiedAppConfigItem,
                SecureTextAppConfigItem,
                UnknownType,
            ]
            discriminator_value: str = cast(str, data.get("type"))
            if discriminator_value is not None:
                app_config_item: Union[
                    ArrayElementAppConfigItem,
                    DateAppConfigItem,
                    DatetimeAppConfigItem,
                    JsonAppConfigItem,
                    EntitySchemaAppConfigItem,
                    FieldAppConfigItem,
                    BooleanAppConfigItem,
                    IntegerAppConfigItem,
                    FloatAppConfigItem,
                    TextAppConfigItem,
                    GenericApiIdentifiedAppConfigItem,
                    SecureTextAppConfigItem,
                    UnknownType,
                ]
                if discriminator_value == "aa_sequence":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "array_element":
                    app_config_item = ArrayElementAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "boolean":
                    app_config_item = BooleanAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "box":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "box_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "container":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "container_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "custom_entity":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "date":
                    app_config_item = DateAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "datetime":
                    app_config_item = DatetimeAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "dna_oligo":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "dna_sequence":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "dropdown":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "dropdown_option":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "entity_schema":
                    app_config_item = EntitySchemaAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "entry":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "entry_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "field":
                    app_config_item = FieldAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "float":
                    app_config_item = FloatAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "folder":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "integer":
                    app_config_item = IntegerAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "json":
                    app_config_item = JsonAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "legacy_request_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "location":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "location_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "mixture":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "molecule":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "plate":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "plate_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "project":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "registry":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "result_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "rna_oligo":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "rna_sequence":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "run_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "secure_text":
                    app_config_item = SecureTextAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "text":
                    app_config_item = TextAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "workflow_task_schema":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "workflow_task_status":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item
                if discriminator_value == "worklist":
                    app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                    return app_config_item

                return UnknownType(value=data)
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = ArrayElementAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = DateAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = DatetimeAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = JsonAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = EntitySchemaAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = FieldAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = BooleanAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = IntegerAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = FloatAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = TextAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                app_config_item = SecureTextAppConfigItem.from_dict(data, strict=True)

                return app_config_item
            except:  # noqa: E722
                pass
            return UnknownType(data)

        response_201 = _parse_response_201(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[
    Union[
        Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Union[
        AppConfigItemGenericCreate,
        AppConfigItemBooleanCreate,
        AppConfigItemIntegerCreate,
        AppConfigItemFloatCreate,
        AppConfigItemDateCreate,
        AppConfigItemDatetimeCreate,
        AppConfigItemJsonCreate,
        UnknownType,
    ],
) -> Response[
    Union[
        Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: Union[
        AppConfigItemGenericCreate,
        AppConfigItemBooleanCreate,
        AppConfigItemIntegerCreate,
        AppConfigItemFloatCreate,
        AppConfigItemDateCreate,
        AppConfigItemDatetimeCreate,
        AppConfigItemJsonCreate,
        UnknownType,
    ],
) -> Optional[
    Union[
        Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    """ Create app configuration item """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Union[
        AppConfigItemGenericCreate,
        AppConfigItemBooleanCreate,
        AppConfigItemIntegerCreate,
        AppConfigItemFloatCreate,
        AppConfigItemDateCreate,
        AppConfigItemDatetimeCreate,
        AppConfigItemJsonCreate,
        UnknownType,
    ],
) -> Response[
    Union[
        Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Union[
        AppConfigItemGenericCreate,
        AppConfigItemBooleanCreate,
        AppConfigItemIntegerCreate,
        AppConfigItemFloatCreate,
        AppConfigItemDateCreate,
        AppConfigItemDatetimeCreate,
        AppConfigItemJsonCreate,
        UnknownType,
    ],
) -> Optional[
    Union[
        Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    """ Create app configuration item """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
