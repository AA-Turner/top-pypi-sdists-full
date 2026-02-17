"""
This module provides async functionality for managing aliases in Typesense.

It contains the AsyncAliases class, which allows for creating, updating, retrieving, and
accessing individual aliases asynchronously.

Classes:
    AsyncAliases: Manages aliases in the Typesense API (async).

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.async_alias: Provides the AsyncAlias class for individual alias operations.
    - typesense.types.alias: Provides AliasCreateSchema, AliasSchema, and AliasesResponseSchema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

from .api_call import AsyncApiCall
from .alias import AsyncAlias
from typesense.types.alias import AliasCreateSchema, AliasSchema, AliasesResponseSchema

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing


class AsyncAliases:
    """
    Manages aliases in the Typesense API (async).

    This class provides async methods to create, update, retrieve, and access individual aliases.

    Attributes:
        resource_path (str): The API endpoint path for alias operations.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        aliases (Dict[str, AsyncAlias]): A dictionary of AsyncAlias instances, keyed by alias name.
    """

    resource_path: typing.Final[str] = "/aliases"

    def __init__(self, api_call: AsyncApiCall):
        """
        Initialize the AsyncAliases instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        """
        self.api_call = api_call
        self.aliases: typing.Dict[str, AsyncAlias] = {}

    def __getitem__(self, name: str) -> AsyncAlias:
        """
        Get or create an AsyncAlias instance for a given alias name.

        This method allows accessing aliases using dictionary-like syntax.
        If the AsyncAlias instance doesn't exist, it creates a new one.

        Args:
            name (str): The name of the alias.

        Returns:
            AsyncAlias: The AsyncAlias instance for the specified alias name.

        Example:
            >>> aliases = AsyncAliases(async_api_call)
            >>> company_alias = aliases["company_alias"]
        """
        if not self.aliases.get(name):
            self.aliases[name] = AsyncAlias(self.api_call, name)
        return self.aliases[name]

    async def upsert(self, name: str, mapping: AliasCreateSchema) -> AliasSchema:
        """
        Create or update an alias.

        Args:
            name (str): The name of the alias.
            mapping (AliasCreateSchema): The schema for creating or updating the alias.

        Returns:
            AliasSchema: The created or updated alias.

        Example:
            >>> aliases = AsyncAliases(async_api_call)
            >>> alias = await aliases.upsert(
            ...     "company_alias", {"collection_name": "companies"}
            ... )
        """
        response: AliasSchema = await self.api_call.put(
            self._endpoint_path(name),
            body=mapping,
            entity_type=AliasSchema,
        )
        return response

    async def retrieve(self) -> AliasesResponseSchema:
        """
        Retrieve all aliases.

        Returns:
            AliasesResponseSchema: The schema containing all aliases.

        Example:
            >>> aliases = AsyncAliases(async_api_call)
            >>> all_aliases = await aliases.retrieve()
            >>> for alias in all_aliases["aliases"]:
            ...     print(alias["name"])
        """
        response: AliasesResponseSchema = await self.api_call.get(
            AsyncAliases.resource_path,
            as_json=True,
            entity_type=AliasesResponseSchema,
        )
        return response

    def _endpoint_path(self, alias_name: str) -> str:
        """
        Construct the API endpoint path for alias operations.

        Args:
            alias_name (str): The name of the alias.

        Returns:
            str: The constructed endpoint path.
        """
        return "/".join([AsyncAliases.resource_path, alias_name])
