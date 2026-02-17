"""
This module provides async functionality for managing NL search models in Typesense.

It contains the NLSearchModels class, which allows for creating, retrieving, and
accessing individual NL search models asynchronously.

Classes:
    NLSearchModels: Manages NL search models in the Typesense API (async).

Dependencies:
    - typesense.async_api_call: Provides the ApiCall class for making async API requests.
    - typesense.async_nl_search_model: Provides the NLSearchModel class for individual NL search model operations.
    - typesense.types.nl_search_model: Provides NLSearchModelCreateSchema, NLSearchModelSchema, and NLSearchModelsRetrieveSchema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

from .api_call import ApiCall
from .nl_search_model import NLSearchModel
from typesense.types.nl_search_model import (
    NLSearchModelCreateSchema,
    NLSearchModelSchema,
    NLSearchModelsRetrieveSchema,
)

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing


class NLSearchModels:
    """
    Manages NL search models in the Typesense API (async).

    This class provides async methods to create, retrieve, and access individual NL search models.

    Attributes:
        resource_path (str): The API endpoint path for NL search models operations.
        api_call (ApiCall): The ApiCall instance for making async API requests.
        nl_search_models (Dict[str, NLSearchModel]):
            A dictionary of NLSearchModel instances, keyed by model ID.
    """

    resource_path: typing.Final[str] = "/nl_search_models"

    def __init__(self, api_call: ApiCall) -> None:
        """
        Initialize the NLSearchModels instance.

        Args:
            api_call (ApiCall): The ApiCall instance for making async API requests.
        """
        self.api_call = api_call
        self.nl_search_models: typing.Dict[str, NLSearchModel] = {}

    def __getitem__(self, model_id: str) -> NLSearchModel:
        """
        Get or create an NLSearchModel instance for a given model ID.

        This method allows accessing NL search models using dictionary-like syntax.
        If the NLSearchModel instance doesn't exist, it creates a new one.

        Args:
            model_id (str): The ID of the NL search model.

        Returns:
            NLSearchModel: The NLSearchModel instance for the specified model ID.

        Example:
            >>> nl_search_models = NLSearchModels(async_api_call)
            >>> model = nl_search_models["model_id"]
        """
        if model_id not in self.nl_search_models:
            self.nl_search_models[model_id] = NLSearchModel(
                self.api_call,
                model_id,
            )
        return self.nl_search_models[model_id]

    def create(self, model: NLSearchModelCreateSchema) -> NLSearchModelSchema:
        """
        Create a new NL search model.

        Args:
            model (NLSearchModelCreateSchema):
                The schema for creating the NL search model.

        Returns:
            NLSearchModelSchema: The created NL search model.

        Example:
            >>> nl_search_models = NLSearchModels(async_api_call)
            >>> model = await nl_search_models.create(
            ...     {
            ...         "api_key": "key",
            ...         "model_name": "openai/gpt-3.5-turbo",
            ...         "system_prompt": "System prompt",
            ...     }
            ... )
        """
        response: NLSearchModelSchema = self.api_call.post(
            endpoint=NLSearchModels.resource_path,
            entity_type=NLSearchModelSchema,
            as_json=True,
            body=model,
        )
        return response

    def retrieve(self) -> NLSearchModelsRetrieveSchema:
        """
        Retrieve all NL search models.

        Returns:
            NLSearchModelsRetrieveSchema: A list of all NL search models.

        Example:
            >>> nl_search_models = NLSearchModels(async_api_call)
            >>> all_models = await nl_search_models.retrieve()
            >>> for model in all_models:
            ...     print(model["id"])
        """
        response: NLSearchModelsRetrieveSchema = self.api_call.get(
            endpoint=NLSearchModels.resource_path,
            entity_type=NLSearchModelsRetrieveSchema,
            as_json=True,
        )
        return response
