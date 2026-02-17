"""Client for single Synonym Set operations (async)."""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from typesense.types.synonym_set import (
    SynonymItemDeleteSchema,
    SynonymItemSchema,
    SynonymSetCreateSchema,
    SynonymSetDeleteSchema,
    SynonymSetRetrieveSchema,
)


class AsyncSynonymSet:
    def __init__(self, api_call: AsyncApiCall, name: str) -> None:
        self.api_call = api_call
        self.name = name

    @property
    def _endpoint_path(self) -> str:
        from .synonym_sets import AsyncSynonymSets

        return "/".join([AsyncSynonymSets.resource_path, self.name])

    async def retrieve(self) -> SynonymSetRetrieveSchema:
        response: SynonymSetRetrieveSchema = await self.api_call.get(
            self._endpoint_path,
            as_json=True,
            entity_type=SynonymSetRetrieveSchema,
        )
        return response

    async def upsert(self, set: SynonymSetCreateSchema) -> SynonymSetCreateSchema:
        response: SynonymSetCreateSchema = await self.api_call.put(
            self._endpoint_path,
            entity_type=SynonymSetCreateSchema,
            body=set,
        )
        return response

    async def delete(self) -> SynonymSetDeleteSchema:
        response: SynonymSetDeleteSchema = await self.api_call.delete(
            self._endpoint_path,
            entity_type=SynonymSetDeleteSchema,
        )
        return response

    @property
    def _items_path(self) -> str:
        return "/".join([self._endpoint_path, "items"])  # /synonym_sets/{name}/items

    async def list_items(
        self,
        *,
        limit: typing.Union[int, None] = None,
        offset: typing.Union[int, None] = None,
    ) -> typing.List[SynonymItemSchema]:
        params: typing.Dict[str, typing.Union[int, None]] = {
            "limit": limit,
            "offset": offset,
        }
        clean_params: typing.Dict[str, int] = {
            k: v for k, v in params.items() if v is not None
        }
        response: typing.List[SynonymItemSchema] = await self.api_call.get(
            self._items_path,
            as_json=True,
            entity_type=typing.List[SynonymItemSchema],
            params=clean_params or None,
        )
        return response

    async def get_item(self, item_id: str) -> SynonymItemSchema:
        response: SynonymItemSchema = await self.api_call.get(
            "/".join([self._items_path, item_id]),
            as_json=True,
            entity_type=SynonymItemSchema,
        )
        return response

    async def upsert_item(
        self, item_id: str, item: SynonymItemSchema
    ) -> SynonymItemSchema:
        response: SynonymItemSchema = await self.api_call.put(
            "/".join([self._items_path, item_id]),
            body=item,
            entity_type=SynonymItemSchema,
        )
        return response

    async def delete_item(self, item_id: str) -> SynonymItemDeleteSchema:
        # API returns {"id": "..."} for delete; openapi defines SynonymItemDeleteResponse with name but for items it's id
        response: SynonymItemDeleteSchema = await self.api_call.delete(
            "/".join([self._items_path, item_id]), entity_type=SynonymItemDeleteSchema
        )
        return response
