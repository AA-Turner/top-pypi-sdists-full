"""
Module for managing stemming dictionaries in Typesense (async).

This module provides a class for managing stemming dictionaries in Typesense,
including creating, updating, and retrieving them asynchronously.

Classes:
    - AsyncStemming: Handles async operations related to stemming dictionaries.

Attributes:
    - AsyncStemmingDictionaries: The AsyncStemmingDictionaries object for managing stemming dictionaries.

Methods:
    - __init__: Initializes the AsyncStemming object.

The AsyncStemming class interacts with the Typesense API to manage stemming dictionary operations.
It provides access to the AsyncStemmingDictionaries object for managing stemming dictionaries.

For more information on stemming dictionaries, refer to the Stemming
[documentation](https://typesense.org/docs/28.0/api/stemming.html)

This module uses type hinting and is compatible with Python 3.11+ as well as earlier
versions through the use of the typing_extensions library.
"""

from .api_call import AsyncApiCall
from .stemming_dictionaries import AsyncStemmingDictionaries


class AsyncStemming(object):
    """
    Class for managing stemming dictionaries in Typesense (async).

    This class provides methods to interact with stemming dictionaries, including
    creating, updating, and retrieving them.

    Attributes:
        dictionaries (AsyncStemmingDictionaries): The AsyncStemmingDictionaries object for managing
            stemming dictionaries.
    """

    def __init__(self, api_call: AsyncApiCall):
        """
        Initialize the AsyncStemming object.

        Args:
            api_call (AsyncApiCall): The API call object for making requests.
        """
        self.api_call = api_call
        self.dictionaries = AsyncStemmingDictionaries(api_call)
