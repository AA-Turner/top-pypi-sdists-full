"""
This module provides async functionality for managing individual conversation models in Typesense.

It contains the AsyncConversationModel class, which allows for retrieving, updating, and deleting
conversation models asynchronously.

Classes:
    AsyncConversationModel: Manages async operations on a single conversation model in the Typesense API.

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.types.conversations_model: Provides ConversationModelCreateSchema, ConversationModelDeleteSchema, and ConversationModelSchema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

from .api_call import AsyncApiCall
from typesense.types.conversations_model import (
    ConversationModelCreateSchema,
    ConversationModelDeleteSchema,
    ConversationModelSchema,
)


class AsyncConversationModel:
    """
    Manages async operations on a single conversation model in the Typesense API.

    This class provides async methods to retrieve, update, and delete a conversation model.

    Attributes:
        model_id (str): The ID of the conversation model.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
    """

    def __init__(self, api_call: AsyncApiCall, model_id: str) -> None:
        """
        Initialize the AsyncConversationModel instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
            model_id (str): The ID of the conversation model.
        """
        self.model_id = model_id
        self.api_call = api_call

    async def retrieve(self) -> ConversationModelSchema:
        """
        Retrieve this specific conversation model.

        Returns:
            ConversationModelSchema: The schema containing the conversation model details.
        """
        response: ConversationModelSchema = await self.api_call.get(
            self._endpoint_path,
            as_json=True,
            entity_type=ConversationModelSchema,
        )
        return response

    async def update(
        self, model: ConversationModelCreateSchema
    ) -> ConversationModelSchema:
        """
        Update this specific conversation model.

        Args:
            model (ConversationModelCreateSchema):
              The schema containing the updated model details.

        Returns:
            ConversationModelSchema: The schema containing the updated conversation model.
        """
        response: ConversationModelSchema = await self.api_call.put(
            self._endpoint_path,
            body=model,
            entity_type=ConversationModelSchema,
        )
        return response

    async def delete(self) -> ConversationModelDeleteSchema:
        """
        Delete this specific conversation model.

        Returns:
            ConversationModelDeleteSchema: The schema containing the deletion response.
        """
        response: ConversationModelDeleteSchema = await self.api_call.delete(
            self._endpoint_path,
            entity_type=ConversationModelDeleteSchema,
        )
        return response

    @property
    def _endpoint_path(self) -> str:
        """
        Construct the API endpoint path for this specific conversation model.

        Returns:
            str: The constructed endpoint path.
        """
        from .conversations_models import AsyncConversationsModels

        return "/".join([AsyncConversationsModels.resource_path, self.model_id])
