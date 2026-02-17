"""
Module for interacting with the stemming dictionaries endpoint of the Typesense API (async).

This module provides a class for managing stemming dictionaries in Typesense, including creating
and updating them asynchronously.

Classes:
    - AsyncStemmingDictionaries: Handles async operations related to stemming dictionaries.

Methods:
    - __init__: Initializes the AsyncStemmingDictionaries object.
    - __getitem__: Retrieves or creates an AsyncStemmingDictionary object for a given dictionary_id.
    - upsert: Creates or updates a stemming dictionary.
    - _upsert_list: Creates or updates a list of stemming dictionaries.
    - _dump_to_jsonl: Dumps a list of StemmingDictionaryCreateSchema objects to a JSONL string.
    - _parse_response: Parses the response from the upsert operation.
    - _upsert_raw: Performs the raw upsert operation.
    - _endpoint_path: Constructs the API endpoint path for this specific stemming dictionary.

The AsyncStemmingDictionaries class interacts with the Typesense API to manage stemming dictionary
operations. It provides methods to create, update, and retrieve stemming dictionaries, as well as
access individual AsyncStemmingDictionary objects.

For more information on stemming dictionaries,
refer to the Stemming [documentation](https://typesense.org/docs/28.0/api/stemming.html)
"""

import json
import sys

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing

from .api_call import AsyncApiCall
from .stemming_dictionary import AsyncStemmingDictionary
from typesense.types.stemming import (
    StemmingDictionariesRetrieveSchema,
    StemmingDictionaryCreateSchema,
)


class AsyncStemmingDictionaries:
    """
    Class for managing stemming dictionaries in Typesense (async).

    This class provides methods to interact with stemming dictionaries, including
    creating, updating, and retrieving them.

    Attributes:
        api_call (AsyncApiCall): The API call object for making requests.
        stemming_dictionaries (Dict[str, AsyncStemmingDictionary]): A dictionary of
            AsyncStemmingDictionary objects.
    """

    resource_path: typing.Final[str] = "/stemming/dictionaries"

    def __init__(self, api_call: AsyncApiCall):
        """
        Initialize the AsyncStemmingDictionaries object.

        Args:
            api_call (AsyncApiCall): The API call object for making requests.
        """
        self.api_call = api_call
        self.stemming_dictionaries: typing.Dict[str, AsyncStemmingDictionary] = {}

    def __getitem__(self, dictionary_id: str) -> AsyncStemmingDictionary:
        """
        Get or create an AsyncStemmingDictionary object for a given dictionary_id.

        Args:
            dictionary_id (str): The ID of the stemming dictionary.

        Returns:
            AsyncStemmingDictionary: The AsyncStemmingDictionary object for the given ID.
        """
        if not self.stemming_dictionaries.get(dictionary_id):
            self.stemming_dictionaries[dictionary_id] = AsyncStemmingDictionary(
                self.api_call,
                dictionary_id,
            )
        return self.stemming_dictionaries[dictionary_id]

    async def retrieve(self) -> StemmingDictionariesRetrieveSchema:
        """
        Retrieve the list of stemming dictionaries.

        Returns:
            StemmingDictionariesRetrieveSchema: The list of stemming dictionaries.
        """
        response: StemmingDictionariesRetrieveSchema = await self.api_call.get(
            self._endpoint_path(),
            entity_type=StemmingDictionariesRetrieveSchema,
        )
        return response

    @typing.overload
    async def upsert(
        self,
        dictionary_id: str,
        word_root_combinations: typing.Union[str, bytes],
    ) -> str: ...

    @typing.overload
    async def upsert(
        self,
        dictionary_id: str,
        word_root_combinations: typing.List[StemmingDictionaryCreateSchema],
    ) -> typing.List[StemmingDictionaryCreateSchema]: ...

    async def upsert(
        self,
        dictionary_id: str,
        word_root_combinations: typing.Union[
            typing.List[StemmingDictionaryCreateSchema],
            str,
            bytes,
        ],
    ) -> typing.Union[str, typing.List[StemmingDictionaryCreateSchema]]:
        if isinstance(word_root_combinations, (str, bytes)):
            return await self._upsert_raw(dictionary_id, word_root_combinations)

        return await self._upsert_list(dictionary_id, word_root_combinations)

    async def _upsert_list(
        self,
        dictionary_id: str,
        word_root_combinations: typing.List[StemmingDictionaryCreateSchema],
    ) -> typing.List[StemmingDictionaryCreateSchema]:
        word_combos_in_jsonl = self._dump_to_jsonl(word_root_combinations)
        response = await self._upsert_raw(dictionary_id, word_combos_in_jsonl)
        return self._parse_response(response)

    def _dump_to_jsonl(
        self,
        word_root_combinations: typing.List[StemmingDictionaryCreateSchema],
    ) -> str:
        word_root_strs = [json.dumps(combo) for combo in word_root_combinations]

        return "\n".join(word_root_strs)

    def _parse_response(
        self,
        response: str,
    ) -> typing.List[StemmingDictionaryCreateSchema]:
        object_list: typing.List[StemmingDictionaryCreateSchema] = []

        for line in response.split("\n"):
            try:
                decoded = json.loads(line)
            except json.JSONDecodeError as err:
                raise ValueError(f"Failed to parse JSON from response: {line}") from err
            object_list.append(decoded)
        return object_list

    async def _upsert_raw(
        self,
        dictionary_id: str,
        word_root_combinations: typing.Union[bytes, str],
    ) -> str:
        response: str = await self.api_call.post(
            self._endpoint_path("import"),
            body=word_root_combinations,
            as_json=False,
            entity_type=str,
            params={"id": dictionary_id},
        )
        return response

    def _endpoint_path(self, action: typing.Union[str, None] = None) -> str:
        """
        Construct the API endpoint path for this specific stemming dictionary.

        Args:
            action (str, optional): The action to perform on the stemming dictionary.
                Defaults to None.

        Returns:
            str: The constructed endpoint path.
        """
        if action:
            return f"{AsyncStemmingDictionaries.resource_path}/{action}"
        return AsyncStemmingDictionaries.resource_path
