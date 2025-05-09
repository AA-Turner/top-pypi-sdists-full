# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...requests.custom_attribute_definition import CustomAttributeDefinitionParams
from ...core.request_options import RequestOptions
from ...core.http_response import HttpResponse
from ...types.create_order_custom_attribute_definition_response import CreateOrderCustomAttributeDefinitionResponse
from ...core.serialization import convert_and_respect_annotation_metadata
from ...core.unchecked_base_model import construct_type
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...types.retrieve_order_custom_attribute_definition_response import RetrieveOrderCustomAttributeDefinitionResponse
from ...core.jsonable_encoder import jsonable_encoder
from ...types.update_order_custom_attribute_definition_response import UpdateOrderCustomAttributeDefinitionResponse
from ...types.delete_order_custom_attribute_definition_response import DeleteOrderCustomAttributeDefinitionResponse
from ...core.client_wrapper import AsyncClientWrapper
from ...core.http_response import AsyncHttpResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RawCustomAttributeDefinitionsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create(
        self,
        *,
        custom_attribute_definition: CustomAttributeDefinitionParams,
        idempotency_key: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[CreateOrderCustomAttributeDefinitionResponse]:
        """
        Creates an order-related custom attribute definition.  Use this endpoint to
        define a custom attribute that can be associated with orders.

        After creating a custom attribute definition, you can set the custom attribute for orders
        in the Square seller account.

        Parameters
        ----------
        custom_attribute_definition : CustomAttributeDefinitionParams
            The custom attribute definition to create. Note the following:
            - With the exception of the `Selection` data type, the `schema` is specified as a simple URL to the JSON schema
            definition hosted on the Square CDN. For more information, including supported values and constraints, see
            [Specifying the schema](https://developer.squareup.com/docs/customer-custom-attributes-api/custom-attribute-definitions#specify-schema).
            - If provided, `name` must be unique (case-sensitive) across all visible customer-related custom attribute definitions for the seller.
            - All custom attributes are visible in exported customer data, including those set to `VISIBILITY_HIDDEN`.

        idempotency_key : typing.Optional[str]
            A unique identifier for this request, used to ensure idempotency.
            For more information, see [Idempotency](https://developer.squareup.com/docs/build-basics/common-api-patterns/idempotency).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[CreateOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            "v2/orders/custom-attribute-definitions",
            method="POST",
            json={
                "custom_attribute_definition": convert_and_respect_annotation_metadata(
                    object_=custom_attribute_definition, annotation=CustomAttributeDefinitionParams, direction="write"
                ),
                "idempotency_key": idempotency_key,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    CreateOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=CreateOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get(
        self, key: str, *, version: typing.Optional[int] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[RetrieveOrderCustomAttributeDefinitionResponse]:
        """
        Retrieves an order-related [custom attribute definition](entity:CustomAttributeDefinition) from a Square seller account.

        To retrieve a custom attribute definition created by another application, the `visibility`
        setting must be `VISIBILITY_READ_ONLY` or `VISIBILITY_READ_WRITE_VALUES`. Note that seller-defined custom attributes
        (also known as custom fields) are always set to `VISIBILITY_READ_WRITE_VALUES`.

        Parameters
        ----------
        key : str
            The key of the custom attribute definition to retrieve.

        version : typing.Optional[int]
            To enable [optimistic concurrency](https://developer.squareup.com/docs/build-basics/common-api-patterns/optimistic-concurrency)
            control, include this optional field and specify the current version of the custom attribute.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[RetrieveOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/orders/custom-attribute-definitions/{jsonable_encoder(key)}",
            method="GET",
            params={
                "version": version,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    RetrieveOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=RetrieveOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update(
        self,
        key: str,
        *,
        custom_attribute_definition: CustomAttributeDefinitionParams,
        idempotency_key: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[UpdateOrderCustomAttributeDefinitionResponse]:
        """
        Updates an order-related custom attribute definition for a Square seller account.

        Only the definition owner can update a custom attribute definition. Note that sellers can view all custom attributes in exported customer data, including those set to `VISIBILITY_HIDDEN`.

        Parameters
        ----------
        key : str
            The key of the custom attribute definition to update.

        custom_attribute_definition : CustomAttributeDefinitionParams
            The custom attribute definition that contains the fields to update. This endpoint supports sparse updates,
            so only new or changed fields need to be included in the request.  For more information, see
            [Updatable definition fields](https://developer.squareup.com/docs/orders-custom-attributes-api/custom-attribute-definitions#updatable-definition-fields).

            To enable [optimistic concurrency](https://developer.squareup.com/docs/build-basics/common-api-patterns/optimistic-concurrency) control, include the optional `version` field and specify the current version of the custom attribute definition.

        idempotency_key : typing.Optional[str]
            A unique identifier for this request, used to ensure idempotency.
            For more information, see [Idempotency](https://developer.squareup.com/docs/build-basics/common-api-patterns/idempotency).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[UpdateOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/orders/custom-attribute-definitions/{jsonable_encoder(key)}",
            method="PUT",
            json={
                "custom_attribute_definition": convert_and_respect_annotation_metadata(
                    object_=custom_attribute_definition, annotation=CustomAttributeDefinitionParams, direction="write"
                ),
                "idempotency_key": idempotency_key,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    UpdateOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=UpdateOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, key: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[DeleteOrderCustomAttributeDefinitionResponse]:
        """
        Deletes an order-related [custom attribute definition](entity:CustomAttributeDefinition) from a Square seller account.

        Only the definition owner can delete a custom attribute definition.

        Parameters
        ----------
        key : str
            The key of the custom attribute definition to delete.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[DeleteOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/orders/custom-attribute-definitions/{jsonable_encoder(key)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DeleteOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=DeleteOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncRawCustomAttributeDefinitionsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create(
        self,
        *,
        custom_attribute_definition: CustomAttributeDefinitionParams,
        idempotency_key: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[CreateOrderCustomAttributeDefinitionResponse]:
        """
        Creates an order-related custom attribute definition.  Use this endpoint to
        define a custom attribute that can be associated with orders.

        After creating a custom attribute definition, you can set the custom attribute for orders
        in the Square seller account.

        Parameters
        ----------
        custom_attribute_definition : CustomAttributeDefinitionParams
            The custom attribute definition to create. Note the following:
            - With the exception of the `Selection` data type, the `schema` is specified as a simple URL to the JSON schema
            definition hosted on the Square CDN. For more information, including supported values and constraints, see
            [Specifying the schema](https://developer.squareup.com/docs/customer-custom-attributes-api/custom-attribute-definitions#specify-schema).
            - If provided, `name` must be unique (case-sensitive) across all visible customer-related custom attribute definitions for the seller.
            - All custom attributes are visible in exported customer data, including those set to `VISIBILITY_HIDDEN`.

        idempotency_key : typing.Optional[str]
            A unique identifier for this request, used to ensure idempotency.
            For more information, see [Idempotency](https://developer.squareup.com/docs/build-basics/common-api-patterns/idempotency).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[CreateOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v2/orders/custom-attribute-definitions",
            method="POST",
            json={
                "custom_attribute_definition": convert_and_respect_annotation_metadata(
                    object_=custom_attribute_definition, annotation=CustomAttributeDefinitionParams, direction="write"
                ),
                "idempotency_key": idempotency_key,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    CreateOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=CreateOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get(
        self, key: str, *, version: typing.Optional[int] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[RetrieveOrderCustomAttributeDefinitionResponse]:
        """
        Retrieves an order-related [custom attribute definition](entity:CustomAttributeDefinition) from a Square seller account.

        To retrieve a custom attribute definition created by another application, the `visibility`
        setting must be `VISIBILITY_READ_ONLY` or `VISIBILITY_READ_WRITE_VALUES`. Note that seller-defined custom attributes
        (also known as custom fields) are always set to `VISIBILITY_READ_WRITE_VALUES`.

        Parameters
        ----------
        key : str
            The key of the custom attribute definition to retrieve.

        version : typing.Optional[int]
            To enable [optimistic concurrency](https://developer.squareup.com/docs/build-basics/common-api-patterns/optimistic-concurrency)
            control, include this optional field and specify the current version of the custom attribute.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[RetrieveOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/orders/custom-attribute-definitions/{jsonable_encoder(key)}",
            method="GET",
            params={
                "version": version,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    RetrieveOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=RetrieveOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update(
        self,
        key: str,
        *,
        custom_attribute_definition: CustomAttributeDefinitionParams,
        idempotency_key: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[UpdateOrderCustomAttributeDefinitionResponse]:
        """
        Updates an order-related custom attribute definition for a Square seller account.

        Only the definition owner can update a custom attribute definition. Note that sellers can view all custom attributes in exported customer data, including those set to `VISIBILITY_HIDDEN`.

        Parameters
        ----------
        key : str
            The key of the custom attribute definition to update.

        custom_attribute_definition : CustomAttributeDefinitionParams
            The custom attribute definition that contains the fields to update. This endpoint supports sparse updates,
            so only new or changed fields need to be included in the request.  For more information, see
            [Updatable definition fields](https://developer.squareup.com/docs/orders-custom-attributes-api/custom-attribute-definitions#updatable-definition-fields).

            To enable [optimistic concurrency](https://developer.squareup.com/docs/build-basics/common-api-patterns/optimistic-concurrency) control, include the optional `version` field and specify the current version of the custom attribute definition.

        idempotency_key : typing.Optional[str]
            A unique identifier for this request, used to ensure idempotency.
            For more information, see [Idempotency](https://developer.squareup.com/docs/build-basics/common-api-patterns/idempotency).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[UpdateOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/orders/custom-attribute-definitions/{jsonable_encoder(key)}",
            method="PUT",
            json={
                "custom_attribute_definition": convert_and_respect_annotation_metadata(
                    object_=custom_attribute_definition, annotation=CustomAttributeDefinitionParams, direction="write"
                ),
                "idempotency_key": idempotency_key,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    UpdateOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=UpdateOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete(
        self, key: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[DeleteOrderCustomAttributeDefinitionResponse]:
        """
        Deletes an order-related [custom attribute definition](entity:CustomAttributeDefinition) from a Square seller account.

        Only the definition owner can delete a custom attribute definition.

        Parameters
        ----------
        key : str
            The key of the custom attribute definition to delete.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[DeleteOrderCustomAttributeDefinitionResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/orders/custom-attribute-definitions/{jsonable_encoder(key)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DeleteOrderCustomAttributeDefinitionResponse,
                    construct_type(
                        type_=DeleteOrderCustomAttributeDefinitionResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
