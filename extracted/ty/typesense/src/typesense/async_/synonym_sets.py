"""Client for Synonym Sets collection operations (async)."""

import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from .synonym_set import AsyncSynonymSet
from typesense.types.synonym_set import (
    SynonymSetSchema,
)


class AsyncSynonymSets:
    resource_path: typing.Final[str] = "/synonym_sets"

    def __init__(self, api_call: AsyncApiCall) -> None:
        self.api_call = api_call

    async def retrieve(self) -> typing.List[SynonymSetSchema]:
        response: typing.List[SynonymSetSchema] = await self.api_call.get(
            AsyncSynonymSets.resource_path,
            as_json=True,
            entity_type=typing.List[SynonymSetSchema],
        )
        return response

    def __getitem__(self, synonym_set_name: str) -> AsyncSynonymSet:
        from .synonym_set import AsyncSynonymSet as PerSet

        return PerSet(self.api_call, synonym_set_name)
