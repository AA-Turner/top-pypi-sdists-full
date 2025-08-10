from typing import Dict, List
from orionis.services.inspirational.contracts.inspire import IInspire
from orionis.services.inspirational.quotes import INSPIRATIONAL_QUOTES
import random

class Inspire(IInspire):

    def __init__(self, quotes: List[Dict] = None) -> None:
        """
        Initializes the Inspire service with a list of inspirational quotes.

        This constructor sets up the internal list of quotes to be used by the service.
        If no list is provided or the provided list is empty, it defaults to using the
        predefined `INSPIRATIONAL_QUOTES`. The method also validates the structure of
        the provided quotes to ensure each entry is a dictionary containing both 'quote'
        and 'author' keys.

        Parameters
        ----------
        quotes : List[dict], optional
            A list of dictionaries, where each dictionary must contain the keys 'quote'
            (str) and 'author' (str). If not provided or empty, the default list
            `INSPIRATIONAL_QUOTES` will be used.

        Returns
        -------
        None
            This method does not return any value. It initializes the internal state
            of the Inspire service.

        Raises
        ------
        ValueError
            If any item in the provided list is not a dictionary, or if a dictionary
            does not contain both 'quote' and 'author' keys.
        """

        # Use the default quotes if none are provided or the list is empty
        if quotes is None or not quotes:

            # Assign the default list of inspirational quotes
            self.__quotes = INSPIRATIONAL_QUOTES

        # Validate the provided list of quotes
        else:

            # Validate each quote in the provided list
            for row in quotes:
                if not isinstance(row, dict):
                    raise ValueError("Quotes must be provided as a list of dictionaries.")
                if 'quote' not in row or 'author' not in row:
                    raise ValueError("Each quote dictionary must contain 'quote' and 'author' keys.")

            # Assign the validated list of quotes
            self.__quotes = quotes

    def random(self) -> dict:
        """
        Returns a random inspirational quote from the available list.

        This method selects and returns a random quote from the list of inspirational quotes.
        If the list is empty, it returns a fallback quote to ensure a valid response is always provided.

        Returns
        -------
        dict
            A dictionary containing two keys: 'quote' (str) and 'author' (str), representing
            the selected inspirational quote and its author. If no quotes are available, a fallback
            quote is returned.
        """

        # Count the number of quotes available
        count = len(self.__quotes)

        # If there are no quotes available, return the fallback quote
        if count == 0:
            return self.__fallback()

        # Select a random index within the range of available quotes
        num_random = random.randint(0, count - 1)

        # Return the randomly selected quote
        return self.__quotes[num_random] or self.__fallback()

    def __fallback(self) -> dict:
        """
        Returns a default inspirational quote when no quotes are available.

        This method provides a fallback quote in case the list of inspirational quotes
        is empty or unavailable. It ensures that the service always returns a valid
        response, even in edge cases.

        Returns
        -------
        dict
            A dictionary containing two keys: 'quote' (str) and 'author' (str), representing
            the fallback inspirational quote and its author.
        """

        # Return a hardcoded fallback quote and author
        return {
            'quote': 'Greatness is not measured by what you build, but by what you inspire others to create.',
            'author': 'Raul M. Uñate'
        }