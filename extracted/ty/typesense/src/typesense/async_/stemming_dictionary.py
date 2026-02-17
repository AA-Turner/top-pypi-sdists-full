"""
Module for managing individual stemming dictionaries in Typesense (async).

This module provides a class for managing individual stemming dictionaries in Typesense,
including retrieving them asynchronously.

Classes:
    - AsyncStemmingDictionary: Handles async operations related to individual stemming dictionaries.

Methods:
    - __init__: Initializes the AsyncStemmingDictionary object.
    - retrieve: Retrieves this specific stemming dictionary.

The AsyncStemmingDictionary class interacts with the Typesense API to manage operations on a
specific stemming dictionary. It provides methods to retrieve the dictionary details.

For more information on stemming dictionaries, refer to the Stemming
[documentation](https://typesense.org/docs/28.0/api/stemming.html)

This module uses type hinting and is compatible with Python 3.11+ as well as earlier
versions through the use of the typing_extensions library.
"""

from .api_call import AsyncApiCall
from typesense.types.stemming import StemmingDictionarySchema


class AsyncStemmingDictionary:
    """
    Class for managing individual stemming dictionaries in Typesense (async).

    This class provides methods to interact with a specific stemming dictionary,
    including retrieving it.

    Attributes:
        api_call (AsyncApiCall): The API call object for making requests.
        dict_id (str): The ID of the stemming dictionary.
    """

    def __init__(self, api_call: AsyncApiCall, dict_id: str):
        """
        Initialize the AsyncStemmingDictionary object.

        Args:
            api_call (AsyncApiCall): The API call object for making requests.
            dict_id (str): The ID of the stemming dictionary.
        """
        self.api_call = api_call
        self.dict_id = dict_id

    async def retrieve(self) -> StemmingDictionarySchema:
        """
        Retrieve this specific stemming dictionary.

        Returns:
            StemmingDictionarySchema: The schema containing the stemming dictionary details.
        """
        response: StemmingDictionarySchema = await self.api_call.get(
            self._endpoint_path,
            entity_type=StemmingDictionarySchema,
            as_json=True,
        )
        return response

    @property
    def _endpoint_path(self) -> str:
        """
        Construct the API endpoint path for this specific stemming dictionary.

        Returns:
            str: The constructed endpoint path.
        """
        from .stemming_dictionaries import AsyncStemmingDictionaries

        return "/".join([AsyncStemmingDictionaries.resource_path, self.dict_id])
