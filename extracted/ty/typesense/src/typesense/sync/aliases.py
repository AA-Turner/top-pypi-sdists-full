"""
This module provides async functionality for managing aliases in Typesense.

It contains the Aliases class, which allows for creating, updating, retrieving, and
accessing individual aliases asynchronously.

Classes:
    Aliases: Manages aliases in the Typesense API (async).

Dependencies:
    - typesense.async_api_call: Provides the ApiCall class for making async API requests.
    - typesense.async_alias: Provides the Alias class for individual alias operations.
    - typesense.types.alias: Provides AliasCreateSchema, AliasSchema, and AliasesResponseSchema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

from .api_call import ApiCall
from .alias import Alias
from typesense.types.alias import AliasCreateSchema, AliasSchema, AliasesResponseSchema

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing


class Aliases:
    """
    Manages aliases in the Typesense API (async).

    This class provides async methods to create, update, retrieve, and access individual aliases.

    Attributes:
        resource_path (str): The API endpoint path for alias operations.
        api_call (ApiCall): The ApiCall instance for making async API requests.
        aliases (Dict[str, Alias]): A dictionary of Alias instances, keyed by alias name.
    """

    resource_path: typing.Final[str] = "/aliases"

    def __init__(self, api_call: ApiCall):
        """
        Initialize the Aliases instance.

        Args:
            api_call (ApiCall): The ApiCall instance for making async API requests.
        """
        self.api_call = api_call
        self.aliases: typing.Dict[str, Alias] = {}

    def __getitem__(self, name: str) -> Alias:
        """
        Get or create an Alias instance for a given alias name.

        This method allows accessing aliases using dictionary-like syntax.
        If the Alias instance doesn't exist, it creates a new one.

        Args:
            name (str): The name of the alias.

        Returns:
            Alias: The Alias instance for the specified alias name.

        Example:
            >>> aliases = Aliases(async_api_call)
            >>> company_alias = aliases["company_alias"]
        """
        if not self.aliases.get(name):
            self.aliases[name] = Alias(self.api_call, name)
        return self.aliases[name]

    def upsert(self, name: str, mapping: AliasCreateSchema) -> AliasSchema:
        """
        Create or update an alias.

        Args:
            name (str): The name of the alias.
            mapping (AliasCreateSchema): The schema for creating or updating the alias.

        Returns:
            AliasSchema: The created or updated alias.

        Example:
            >>> aliases = Aliases(async_api_call)
            >>> alias = await aliases.upsert(
            ...     "company_alias", {"collection_name": "companies"}
            ... )
        """
        response: AliasSchema = self.api_call.put(
            self._endpoint_path(name),
            body=mapping,
            entity_type=AliasSchema,
        )
        return response

    def retrieve(self) -> AliasesResponseSchema:
        """
        Retrieve all aliases.

        Returns:
            AliasesResponseSchema: The schema containing all aliases.

        Example:
            >>> aliases = Aliases(async_api_call)
            >>> all_aliases = await aliases.retrieve()
            >>> for alias in all_aliases["aliases"]:
            ...     print(alias["name"])
        """
        response: AliasesResponseSchema = self.api_call.get(
            Aliases.resource_path,
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
        return "/".join([Aliases.resource_path, alias_name])
