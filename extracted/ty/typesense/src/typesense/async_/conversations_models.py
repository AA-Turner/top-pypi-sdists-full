"""
This module provides async functionality for managing conversation models in Typesense.

It contains the AsyncConversationsModels class, which allows for creating, retrieving, and
accessing individual conversation models asynchronously.

Classes:
    AsyncConversationsModels: Manages conversation models in the Typesense API (async).

Dependencies:
    - typesense.async_api_call: Provides the AsyncApiCall class for making async API requests.
    - typesense.async_conversation_model: Provides the AsyncConversationModel class for individual conversation model operations.
    - typesense.types.conversations_model: Provides ConversationModelCreateSchema and ConversationModelSchema types.

Note: This module uses conditional imports to support both Python 3.11+ and earlier versions.
"""

import sys

from .api_call import AsyncApiCall
from .conversation_model import AsyncConversationModel
from typesense.types.conversations_model import (
    ConversationModelCreateSchema,
    ConversationModelSchema,
)

if sys.version_info >= (3, 11):
    import typing
else:
    import typing_extensions as typing


class AsyncConversationsModels:
    """
    Manages conversation models in the Typesense API (async).

    This class provides async methods to create, retrieve, and access individual conversation models.

    Attributes:
        resource_path (str): The API endpoint path for conversation models operations.
        api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        conversations_models (Dict[str, AsyncConversationModel]):
            A dictionary of AsyncConversationModel instances, keyed by model ID.
    """

    resource_path: typing.Final[str] = "/conversations/models"

    def __init__(self, api_call: AsyncApiCall) -> None:
        """
        Initialize the AsyncConversationsModels instance.

        Args:
            api_call (AsyncApiCall): The AsyncApiCall instance for making async API requests.
        """
        self.api_call = api_call
        self.conversations_models: typing.Dict[str, AsyncConversationModel] = {}

    def __getitem__(self, model_id: str) -> AsyncConversationModel:
        """
        Get or create an AsyncConversationModel instance for a given model ID.

        This method allows accessing conversation models using dictionary-like syntax.
        If the AsyncConversationModel instance doesn't exist, it creates a new one.

        Args:
            model_id (str): The ID of the conversation model.

        Returns:
            AsyncConversationModel: The AsyncConversationModel instance for the specified model ID.

        Example:
            >>> conversations_models = AsyncConversationsModels(async_api_call)
            >>> model = conversations_models["model_id"]
        """
        if model_id not in self.conversations_models:
            self.conversations_models[model_id] = AsyncConversationModel(
                self.api_call,
                model_id,
            )
        return self.conversations_models[model_id]

    async def create(
        self, model: ConversationModelCreateSchema
    ) -> ConversationModelSchema:
        """
        Create a new conversation model.

        Args:
            model (ConversationModelCreateSchema):
                The schema for creating the conversation model.

        Returns:
            ConversationModelSchema: The created conversation model.

        Example:
            >>> conversations_models = AsyncConversationsModels(async_api_call)
            >>> model = await conversations_models.create(
            ...     {
            ...         "api_key": "key",
            ...         "model_name": "openai/gpt-3.5-turbo",
            ...         "history_collection": "conversation_store",
            ...     }
            ... )
        """
        response: ConversationModelSchema = await self.api_call.post(
            endpoint=AsyncConversationsModels.resource_path,
            entity_type=ConversationModelSchema,
            as_json=True,
            body=model,
        )
        return response

    async def retrieve(self) -> typing.List[ConversationModelSchema]:
        """
        Retrieve all conversation models.

        Returns:
            List[ConversationModelSchema]: A list of all conversation models.

        Example:
            >>> conversations_models = AsyncConversationsModels(async_api_call)
            >>> all_models = await conversations_models.retrieve()
            >>> for model in all_models:
            ...     print(model["id"])
        """
        response: typing.List[ConversationModelSchema] = await self.api_call.get(
            endpoint=AsyncConversationsModels.resource_path,
            entity_type=typing.List[ConversationModelSchema],
            as_json=True,
        )
        return response
