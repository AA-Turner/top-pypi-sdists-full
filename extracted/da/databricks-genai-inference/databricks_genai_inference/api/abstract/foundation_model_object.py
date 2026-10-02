"""Foundation Model API Response Object.
"""
import json
from abc import ABC


class FoundationModelObject(ABC):
    """
    Abstract base class for all api response objects.
    """

    def __init__(self, response):
        """
        Initializes a new instance of the FoundationModelObject class.

        Args:
            response (dict): The response from the Foundation Model API.
        """
        self.response = response

    @property
    def json(self):
        """
        Gets the raw JSON representation of the response.

        Returns:
            dict: The raw JSON representation of the response.
        """
        return self.response

    @property
    def id(self):
        """
        Gets the ID of the model.

        Returns:
            str: The ID of the model.
        """
        return self.response['id']

    @property
    def model(self):
        """
        Gets the name of the model.

        Returns:
            str: The name of the model.
        """
        return self.response['model']

    @property
    def usage(self):
        """
        Gets the usage meta data.

        Returns:
            dict: The usage meta data.
        """
        return self.response['usage']

    def __str__(self):
        """
        Gets the string representation of the response.

        Returns:
            str: The string representation of the response.
        """
        return json.dumps(self.response, indent=2)
