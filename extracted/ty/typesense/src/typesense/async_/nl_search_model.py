"""
This module provides async functionality for managing individual NL search models in Typesense.

It contains the AsyncNLSearchModel class, which allows for retrieving, updating, and deleting
NL search models asynchronously.

Classes:
    AsyncNLSearchModel: Manages async operations on a single NL search model in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.types.nl_search_model: Provides NLSearchModelDeleteSchema, NLSearchModelSchema, and NLSearchModelUpdateSchema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

from .api_call import AsyncApiCall
from typesense.types.nl_search_model import (
    NLSearchModelDeleteSchema,
    NLSearchModelSchema,
    NLSearchModelUpdateSchema,
)


class AsyncNLSearchModel:
    """
    Manages async operations on a single NL search model in the Typesense API.

    This class provides async methods to retrieve, update, and delete an NL search model.

    Attributes:
        model_id (str): The ID of the NL search model.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
    """

    def __init__(self, api_call: AsyncApiCall, model_id: str) -> None:
        """
        Initialize the AsyncNLSearchModel instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
            model_id (str): The ID of the NL search model.
        """
        self.model_id = model_id
        self.api_call = api_call

    async def retrieve(self) -> NLSearchModelSchema:
        """
        Retrieve this specific NL search model.

        Returns:
            NLSearchModelSchema: The schema containing the NL search model details.
        """
        response: NLSearchModelSchema = await self.api_call.get(
            self._endpoint_path,
            as_json=True,
            entity_type=NLSearchModelSchema,
        )
        return response

    async def update(self, model: NLSearchModelUpdateSchema) -> NLSearchModelSchema:
        """
        Update this specific NL search model.

        Args:
            model (NLSearchModelUpdateSchema):
              The schema containing the updated model details.

        Returns:
            NLSearchModelSchema: The schema containing the updated NL search model.
        """
        response: NLSearchModelSchema = await self.api_call.put(
            self._endpoint_path,
            body=model,
            entity_type=NLSearchModelSchema,
        )
        return response

    async def delete(self) -> NLSearchModelDeleteSchema:
        """
        Delete this specific NL search model.

        Returns:
            NLSearchModelDeleteSchema: The schema containing the deletion response.
        """
        response: NLSearchModelDeleteSchema = await self.api_call.delete(
            self._endpoint_path,
            entity_type=NLSearchModelDeleteSchema,
        )
        return response

    @property
    def _endpoint_path(self) -> str:
        """
        Construct the API endpoint path for this specific NL search model.

        Returns:
            str: The constructed endpoint path.
        """
        from .nl_search_models import AsyncNLSearchModels

        return "/".join([AsyncNLSearchModels.resource_path, self.model_id])
