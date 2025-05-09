# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...requests.catalog_object import CatalogObjectParams
from ...core.request_options import RequestOptions
from ...core.http_response import HttpResponse
from ...types.upsert_catalog_object_response import UpsertCatalogObjectResponse
from ...core.serialization import convert_and_respect_annotation_metadata
from ...core.unchecked_base_model import construct_type
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...types.get_catalog_object_response import GetCatalogObjectResponse
from ...core.jsonable_encoder import jsonable_encoder
from ...types.delete_catalog_object_response import DeleteCatalogObjectResponse
from ...core.client_wrapper import AsyncClientWrapper
from ...core.http_response import AsyncHttpResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RawObjectClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def upsert(
        self,
        *,
        idempotency_key: str,
        object: CatalogObjectParams,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[UpsertCatalogObjectResponse]:
        """
        Creates a new or updates the specified [CatalogObject](entity:CatalogObject).

        To ensure consistency, only one update request is processed at a time per seller account.
        While one (batch or non-batch) update request is being processed, other (batched and non-batched)
        update requests are rejected with the `429` error code.

        Parameters
        ----------
        idempotency_key : str
            A value you specify that uniquely identifies this
            request among all your requests. A common way to create
            a valid idempotency key is to use a Universally unique
            identifier (UUID).

            If you're unsure whether a particular request was successful,
            you can reattempt it with the same idempotency key without
            worrying about creating duplicate objects.

            See [Idempotency](https://developer.squareup.com/docs/build-basics/common-api-patterns/idempotency) for more information.

        object : CatalogObjectParams
            A CatalogObject to be created or updated.

            - For updates, the object must be active (the `is_deleted` field is not `true`).
            - For creates, the object ID must start with `#`. The provided ID is replaced with a server-generated ID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[UpsertCatalogObjectResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            "v2/catalog/object",
            method="POST",
            json={
                "idempotency_key": idempotency_key,
                "object": convert_and_respect_annotation_metadata(
                    object_=object, annotation=CatalogObjectParams, direction="write"
                ),
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
                    UpsertCatalogObjectResponse,
                    construct_type(
                        type_=UpsertCatalogObjectResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get(
        self,
        object_id: str,
        *,
        include_related_objects: typing.Optional[bool] = None,
        catalog_version: typing.Optional[int] = None,
        include_category_path_to_root: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[GetCatalogObjectResponse]:
        """
        Returns a single [CatalogItem](entity:CatalogItem) as a
        [CatalogObject](entity:CatalogObject) based on the provided ID. The returned
        object includes all of the relevant [CatalogItem](entity:CatalogItem)
        information including: [CatalogItemVariation](entity:CatalogItemVariation)
        children, references to its
        [CatalogModifierList](entity:CatalogModifierList) objects, and the ids of
        any [CatalogTax](entity:CatalogTax) objects that apply to it.

        Parameters
        ----------
        object_id : str
            The object ID of any type of catalog objects to be retrieved.

        include_related_objects : typing.Optional[bool]
            If `true`, the response will include additional objects that are related to the
            requested objects. Related objects are defined as any objects referenced by ID by the results in the `objects` field
            of the response. These objects are put in the `related_objects` field. Setting this to `true` is
            helpful when the objects are needed for immediate display to a user.
            This process only goes one level deep. Objects referenced by the related objects will not be included. For example,

            if the `objects` field of the response contains a CatalogItem, its associated
            CatalogCategory objects, CatalogTax objects, CatalogImage objects and
            CatalogModifierLists will be returned in the `related_objects` field of the
            response. If the `objects` field of the response contains a CatalogItemVariation,
            its parent CatalogItem will be returned in the `related_objects` field of
            the response.

            Default value: `false`

        catalog_version : typing.Optional[int]
            Requests objects as of a specific version of the catalog. This allows you to retrieve historical
            versions of objects. The value to retrieve a specific version of an object can be found
            in the version field of [CatalogObject](entity:CatalogObject)s. If not included, results will
            be from the current version of the catalog.

        include_category_path_to_root : typing.Optional[bool]
            Specifies whether or not to include the `path_to_root` list for each returned category instance. The `path_to_root` list consists
            of `CategoryPathToRootNode` objects and specifies the path that starts with the immediate parent category of the returned category
            and ends with its root category. If the returned category is a top-level category, the `path_to_root` list is empty and is not returned
            in the response payload.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[GetCatalogObjectResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/catalog/object/{jsonable_encoder(object_id)}",
            method="GET",
            params={
                "include_related_objects": include_related_objects,
                "catalog_version": catalog_version,
                "include_category_path_to_root": include_category_path_to_root,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    GetCatalogObjectResponse,
                    construct_type(
                        type_=GetCatalogObjectResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, object_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[DeleteCatalogObjectResponse]:
        """
        Deletes a single [CatalogObject](entity:CatalogObject) based on the
        provided ID and returns the set of successfully deleted IDs in the response.
        Deletion is a cascading event such that all children of the targeted object
        are also deleted. For example, deleting a [CatalogItem](entity:CatalogItem)
        will also delete all of its
        [CatalogItemVariation](entity:CatalogItemVariation) children.

        To ensure consistency, only one delete request is processed at a time per seller account.
        While one (batch or non-batch) delete request is being processed, other (batched and non-batched)
        delete requests are rejected with the `429` error code.

        Parameters
        ----------
        object_id : str
            The ID of the catalog object to be deleted. When an object is deleted, other
            objects in the graph that depend on that object will be deleted as well (for example, deleting a
            catalog item will delete its catalog item variations).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[DeleteCatalogObjectResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/catalog/object/{jsonable_encoder(object_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DeleteCatalogObjectResponse,
                    construct_type(
                        type_=DeleteCatalogObjectResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncRawObjectClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def upsert(
        self,
        *,
        idempotency_key: str,
        object: CatalogObjectParams,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[UpsertCatalogObjectResponse]:
        """
        Creates a new or updates the specified [CatalogObject](entity:CatalogObject).

        To ensure consistency, only one update request is processed at a time per seller account.
        While one (batch or non-batch) update request is being processed, other (batched and non-batched)
        update requests are rejected with the `429` error code.

        Parameters
        ----------
        idempotency_key : str
            A value you specify that uniquely identifies this
            request among all your requests. A common way to create
            a valid idempotency key is to use a Universally unique
            identifier (UUID).

            If you're unsure whether a particular request was successful,
            you can reattempt it with the same idempotency key without
            worrying about creating duplicate objects.

            See [Idempotency](https://developer.squareup.com/docs/build-basics/common-api-patterns/idempotency) for more information.

        object : CatalogObjectParams
            A CatalogObject to be created or updated.

            - For updates, the object must be active (the `is_deleted` field is not `true`).
            - For creates, the object ID must start with `#`. The provided ID is replaced with a server-generated ID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[UpsertCatalogObjectResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v2/catalog/object",
            method="POST",
            json={
                "idempotency_key": idempotency_key,
                "object": convert_and_respect_annotation_metadata(
                    object_=object, annotation=CatalogObjectParams, direction="write"
                ),
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
                    UpsertCatalogObjectResponse,
                    construct_type(
                        type_=UpsertCatalogObjectResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get(
        self,
        object_id: str,
        *,
        include_related_objects: typing.Optional[bool] = None,
        catalog_version: typing.Optional[int] = None,
        include_category_path_to_root: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[GetCatalogObjectResponse]:
        """
        Returns a single [CatalogItem](entity:CatalogItem) as a
        [CatalogObject](entity:CatalogObject) based on the provided ID. The returned
        object includes all of the relevant [CatalogItem](entity:CatalogItem)
        information including: [CatalogItemVariation](entity:CatalogItemVariation)
        children, references to its
        [CatalogModifierList](entity:CatalogModifierList) objects, and the ids of
        any [CatalogTax](entity:CatalogTax) objects that apply to it.

        Parameters
        ----------
        object_id : str
            The object ID of any type of catalog objects to be retrieved.

        include_related_objects : typing.Optional[bool]
            If `true`, the response will include additional objects that are related to the
            requested objects. Related objects are defined as any objects referenced by ID by the results in the `objects` field
            of the response. These objects are put in the `related_objects` field. Setting this to `true` is
            helpful when the objects are needed for immediate display to a user.
            This process only goes one level deep. Objects referenced by the related objects will not be included. For example,

            if the `objects` field of the response contains a CatalogItem, its associated
            CatalogCategory objects, CatalogTax objects, CatalogImage objects and
            CatalogModifierLists will be returned in the `related_objects` field of the
            response. If the `objects` field of the response contains a CatalogItemVariation,
            its parent CatalogItem will be returned in the `related_objects` field of
            the response.

            Default value: `false`

        catalog_version : typing.Optional[int]
            Requests objects as of a specific version of the catalog. This allows you to retrieve historical
            versions of objects. The value to retrieve a specific version of an object can be found
            in the version field of [CatalogObject](entity:CatalogObject)s. If not included, results will
            be from the current version of the catalog.

        include_category_path_to_root : typing.Optional[bool]
            Specifies whether or not to include the `path_to_root` list for each returned category instance. The `path_to_root` list consists
            of `CategoryPathToRootNode` objects and specifies the path that starts with the immediate parent category of the returned category
            and ends with its root category. If the returned category is a top-level category, the `path_to_root` list is empty and is not returned
            in the response payload.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[GetCatalogObjectResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/catalog/object/{jsonable_encoder(object_id)}",
            method="GET",
            params={
                "include_related_objects": include_related_objects,
                "catalog_version": catalog_version,
                "include_category_path_to_root": include_category_path_to_root,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    GetCatalogObjectResponse,
                    construct_type(
                        type_=GetCatalogObjectResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete(
        self, object_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[DeleteCatalogObjectResponse]:
        """
        Deletes a single [CatalogObject](entity:CatalogObject) based on the
        provided ID and returns the set of successfully deleted IDs in the response.
        Deletion is a cascading event such that all children of the targeted object
        are also deleted. For example, deleting a [CatalogItem](entity:CatalogItem)
        will also delete all of its
        [CatalogItemVariation](entity:CatalogItemVariation) children.

        To ensure consistency, only one delete request is processed at a time per seller account.
        While one (batch or non-batch) delete request is being processed, other (batched and non-batched)
        delete requests are rejected with the `429` error code.

        Parameters
        ----------
        object_id : str
            The ID of the catalog object to be deleted. When an object is deleted, other
            objects in the graph that depend on that object will be deleted as well (for example, deleting a
            catalog item will delete its catalog item variations).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[DeleteCatalogObjectResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/catalog/object/{jsonable_encoder(object_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DeleteCatalogObjectResponse,
                    construct_type(
                        type_=DeleteCatalogObjectResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
