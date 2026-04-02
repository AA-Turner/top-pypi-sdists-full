import uuid
from typing import TYPE_CHECKING

from .models import (
    AddContextRequest,
    AddContextResponse,
    ClosedGenerationRequest,
    ClosedGenerationResponse,
    MemoryStream,
    OpenGenerationRequest,
    OpenGenerationResponse,
    SurveySessionCloseResponse,
    SurveySessionCreateResponse,
    SurveySessionDetailResponse,
)

if TYPE_CHECKING:
    from .client import Simile


class Agent:
    """Represents an agent and provides methods for interacting with it directly."""

    def __init__(self, agent_id: uuid.UUID, client: "Simile"):
        self._agent_id = agent_id
        self._client = client

    @property
    def id(self) -> uuid.UUID:
        return self._agent_id

    async def generate_open_response(
        self,
        question: str,
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
        memory_stream: MemoryStream | None = None,
    ) -> OpenGenerationResponse:
        """Generates an open response from this agent based on a question."""
        return await self._client.generate_open_response(
            agent_id=self._agent_id,
            question=question,
            data_types=data_types,
            exclude_data_types=exclude_data_types,
            images=images,
            memory_stream=memory_stream,
        )

    async def generate_closed_response(
        self,
        question: str,
        options: list[str],
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
        memory_stream: MemoryStream | None = None,
    ) -> ClosedGenerationResponse:
        """Generates a closed response from this agent."""
        return await self._client.generate_closed_response(
            agent_id=self._agent_id,
            question=question,
            options=options,
            data_types=data_types,
            exclude_data_types=exclude_data_types,
            images=images,
            memory_stream=memory_stream,
        )


class SurveySession:
    """Represents an active survey session with an agent, allowing for contextual multi-turn generation."""

    def __init__(self, id: uuid.UUID, agent_id: uuid.UUID, status: str, client: "Simile"):
        self._id = id
        self._agent_id = agent_id
        self._status = status
        self._client = client

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def agent_id(self) -> uuid.UUID:
        return self._agent_id

    @property
    def status(self) -> str:
        return self._status

    async def get_details(self) -> SurveySessionDetailResponse:
        """Retrieves detailed information about this survey session including typed conversation history."""
        return await self._client.get_survey_session_details(self._id)

    async def view(self) -> SurveySessionDetailResponse:
        """Alias for get_details() - retrieves all turns in this session."""
        return await self.get_details()

    async def generate_open_response(
        self,
        question: str,
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
        reasoning: bool = False,
    ) -> OpenGenerationResponse:
        """Generates an open response within this survey session."""
        endpoint = f"sessions/{str(self._id)}/open"
        payload = OpenGenerationRequest(
            question=question,
            data_types=data_types,
            exclude_data_types=exclude_data_types,
            images=images,
            reasoning=reasoning,
        )
        return await self._client._request(
            "POST",
            endpoint,
            json=payload.model_dump(),
            response_model=OpenGenerationResponse,
        )

    async def generate_closed_response(
        self,
        question: str,
        options: list[str],
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
        reasoning: bool = False,
    ) -> ClosedGenerationResponse:
        """Generates a closed response within this survey session."""
        endpoint = f"sessions/{str(self._id)}/closed"
        payload = ClosedGenerationRequest(
            question=question,
            options=options,
            data_types=data_types,
            exclude_data_types=exclude_data_types,
            images=images,
            reasoning=reasoning,
        )
        return await self._client._request(
            "POST",
            endpoint,
            json=payload.model_dump(),
            response_model=ClosedGenerationResponse,
        )

    async def add_context(self, ctx: str) -> AddContextResponse:
        """Adds text to the SurveySession without requesting a response."""
        endpoint = f"sessions/{str(self._id)}/context"
        payload = AddContextRequest(context=ctx)
        return await self._client._request(
            "POST",
            endpoint,
            json=payload.model_dump(),
            response_model=AddContextResponse,
        )

    async def add_context_with_timestamp(
        self,
        context_text: str,
        timestamp: str,
    ) -> dict:
        """Adds context to this session with a specific timestamp.

        This is a lower-level method that allows specifying when the context was added.
        For normal use, prefer the add_context() method.

        Args:
            context_text: The context text to add
            timestamp: ISO timestamp of when this interaction occurred

        Returns:
            Dictionary with success status and the added turn details
        """
        endpoint = f"sessions/{str(self._id)}/add-turn"
        payload = {
            "turn_type": "context",
            "context_text": context_text,
            "timestamp": timestamp,
        }

        return await self._client._request(
            "POST",
            endpoint,
            json=payload,
            response_model=None,  # Return raw dict since we don't have a specific model
        )

    async def add_images(
        self,
        images: dict[str, str],
        timestamp: str | None = None,
    ) -> dict:
        """Adds images to the session's conversation history.

        Args:
            images: Dictionary mapping image descriptions to URLs
            timestamp: Optional ISO timestamp of when this interaction occurred

        Returns:
            Dictionary with success status and the added turn details
        """
        endpoint = f"sessions/{str(self._id)}/add-turn"
        payload = {
            "turn_type": "image",
            "images": images,
        }
        if timestamp:
            payload["timestamp"] = timestamp

        return await self._client._request(
            "POST",
            endpoint,
            json=payload,
            response_model=None,  # Return raw dict since we don't have a specific model
        )

    async def add_open_response(
        self,
        question: str,
        response: str,
        timestamp: str | None = None,
    ) -> dict:
        """Adds an open question-answer pair to the session's history.

        Args:
            question: The open question text
            response: The response that was given
            timestamp: Optional ISO timestamp of when this interaction occurred

        Returns:
            Dictionary with success status and the added turn details
        """
        endpoint = f"sessions/{str(self._id)}/add-turn"
        payload = {
            "turn_type": "open",
            "question": question,
            "response": response,
        }
        if timestamp:
            payload["timestamp"] = timestamp

        return await self._client._request(
            "POST",
            endpoint,
            json=payload,
            response_model=None,  # Return raw dict since we don't have a specific model
        )

    async def close(self) -> SurveySessionCloseResponse:
        """Closes this survey session on the server."""
        endpoint = f"sessions/{str(self._id)}/close"
        return await self._client._request(
            "POST", endpoint, response_model=SurveySessionCloseResponse
        )

    async def add_closed_response(
        self,
        question: str,
        options: list[str],
        response: str,
        timestamp: str | None = None,
    ) -> dict:
        """Adds a closed question-answer pair to the session's history.

        Args:
            question: The closed question text
            options: List of answer options
            response: The option that was selected
            timestamp: Optional ISO timestamp of when this interaction occurred

        Returns:
            Dictionary with success status and the added turn details
        """
        endpoint = f"sessions/{str(self._id)}/add-turn"
        payload = {
            "turn_type": "closed",
            "question": question,
            "options": options,
            "response": response,
        }
        if timestamp:
            payload["timestamp"] = timestamp

        return await self._client._request(
            "POST",
            endpoint,
            json=payload,
            response_model=None,  # Return raw dict since we don't have a specific model
        )

    async def fork(self, turn_index: int) -> "SurveySession":
        """Fork this session at a specific turn.

        Creates a new session with the same agent and copies turns from this session
        up to and including the specified turn index.

        Args:
            turn_index: The 0-based index of the last turn to include in the fork

        Returns:
            A new SurveySession object representing the forked session

        Raises:
            Simile.APIError: If the API request fails
        """
        endpoint = f"sessions/{str(self._id)}/fork"
        params = {"turn_index": turn_index}

        response = await self._client._request(
            "POST",
            endpoint,
            params=params,
            response_model=SurveySessionCreateResponse,
        )

        # Create a new SurveySession instance from the response
        return SurveySession(
            id=response.id,
            agent_id=response.agent_id,
            status=response.status,
            client=self._client,
        )
