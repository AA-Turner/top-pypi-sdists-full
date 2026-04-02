import uuid
from collections.abc import AsyncGenerator
from typing import Any

import httpx
from httpx import AsyncClient, Limits
from pydantic import BaseModel

from .exceptions import (
    SimileAPIError,
    SimileAuthenticationError,
    SimileBadRequestError,
    SimileNotFoundError,
)
from .models import (
    Agent as AgentModel,
)
from .models import (
    ClosedGenerationResponse,
    CreateAgentPayload,
    CreateDataItemPayload,
    CreatePopulationPayload,
    DataItem,
    DeletionResponse,
    MemoryStream,
    OpenGenerationRequest,
    OpenGenerationResponse,
    Population,
    PopulationInfo,
    SurveySessionCreateResponse,
    SurveySessionDetailResponse,
    UpdateAgentInfoPayload,
    UpdateDataItemPayload,
    UpdatePopulationInfoPayload,
    UpdatePopulationMetadataPayload,
)
from .resources import Agent, SurveySession

DEFAULT_BASE_URL = "https://api.simile.ai/api/v1"
TIMEOUT_CONFIG = httpx.Timeout(5.0, read=60.0, write=30.0, pool=30.0)


class Simile:
    APIError = SimileAPIError
    AuthenticationError = SimileAuthenticationError
    NotFoundError = SimileNotFoundError
    BadRequestError = SimileBadRequestError

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        max_connections: int = 5000,
        max_keepalive_connections: int = 2000,
        keepalive_expiry: float = 300.0,
    ):
        if not api_key:
            raise ValueError("API key is required.")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

        limits = Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=keepalive_expiry,
        )
        self._client = AsyncClient(
            headers={"X-API-Key": self.api_key},
            timeout=TIMEOUT_CONFIG,
            limits=limits,
        )

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response | BaseModel:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response_model_cls: type[BaseModel] | None = kwargs.pop("response_model", None)

        try:
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()

            if response_model_cls:
                return response_model_cls(**response.json())
            else:
                return response
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            try:
                error_data = e.response.json()
                detail = error_data.get("detail", e.response.text)
            except Exception:
                detail = e.response.text

            if status_code == 401:
                raise SimileAuthenticationError(detail=detail) from e
            elif status_code == 404:
                raise SimileNotFoundError(detail=detail) from e
            elif status_code == 400:
                raise SimileBadRequestError(detail=detail) from e
            else:
                raise SimileAPIError(
                    f"API request failed: {e}", status_code=status_code, detail=detail
                ) from e
        except httpx.ConnectTimeout as e:
            raise SimileAPIError("Connection timed out while trying to connect.") from e
        except httpx.ReadTimeout as e:
            raise SimileAPIError("Timed out waiting for data from the server.") from e
        except httpx.WriteTimeout as e:
            raise SimileAPIError("Timed out while sending data to the server.") from e
        except httpx.PoolTimeout as e:
            raise SimileAPIError("Timed out waiting for a connection from the pool.") from e
        except httpx.ConnectError as e:
            raise SimileAPIError("Failed to connect to the server.") from e
        except httpx.ProtocolError as e:
            raise SimileAPIError("A protocol error occurred.") from e
        except httpx.DecodingError as e:
            raise SimileAPIError("Failed to decode the response.") from e
        except httpx.RequestError as e:
            raise SimileAPIError(
                f"An unknown request error occurred: {type(e).__name__}: {e}"
            ) from e

    def agent(self, agent_id: uuid.UUID) -> Agent:
        """Returns an Agent object to interact with a specific agent."""
        return Agent(agent_id=agent_id, client=self)

    async def create_survey_session(self, agent_id: uuid.UUID) -> SurveySession:
        """Creates a new survey session for the given agent and returns a SurveySession object."""
        endpoint = "sessions/"
        response_data = await self._request(
            "POST",
            endpoint,
            json={"agent_id": str(agent_id)},
            response_model=SurveySessionCreateResponse,
        )

        # Create and return a SurveySession object
        return SurveySession(
            id=response_data.id,
            agent_id=response_data.agent_id,
            status=response_data.status,
            client=self,
        )

    async def get_survey_session_details(
        self, session_id: str | uuid.UUID
    ) -> SurveySessionDetailResponse:
        """Retrieves detailed information about a survey session including typed conversation history."""
        endpoint = f"sessions/{str(session_id)}"
        response_data = await self._request(
            "GET", endpoint, response_model=SurveySessionDetailResponse
        )
        return response_data

    async def get_survey_session(self, session_id: str | uuid.UUID) -> SurveySession:
        """Resume an existing survey session by ID and return a SurveySession object."""
        session_details = await self.get_survey_session_details(session_id)

        if session_details.status == "closed":
            raise ValueError(f"Session {session_id} is already closed")

        return SurveySession(
            id=session_details.id,
            agent_id=session_details.agent_id,
            status=session_details.status,
            client=self,
        )

    async def create_population(self, name: str, description: str | None = None) -> Population:
        """Creates a new population."""
        payload = CreatePopulationPayload(name=name, description=description)
        response_data = await self._request(
            "POST",
            "populations/create",
            json=payload.model_dump(mode="json", exclude_none=True),
            response_model=Population,
        )
        return response_data

    async def update_population_metadata(
        self,
        population_id: str | uuid.UUID,
        metadata: dict[str, Any],
        mode: str = "merge",
    ) -> Population:
        """
        Update a population's metadata (jsonb).

        Args:
            population_id: The ID of the population
            metadata: A dictionary of metadata to merge or replace
            mode: Either "merge" (default) or "replace"

        Returns:
            Updated Population object
        """
        payload = UpdatePopulationMetadataPayload(metadata=metadata, mode=mode)
        response_data = await self._request(
            "PATCH",
            f"populations/{str(population_id)}/metadata",
            json=payload.model_dump(mode="json", exclude_none=True),
            response_model=Population,
        )
        return response_data

    async def get_population(self, population_id: str | uuid.UUID) -> Population:
        response_data = await self._request(
            "GET", f"populations/get/{str(population_id)}", response_model=Population
        )
        return response_data

    async def update_population_info(
        self,
        population_id: str | uuid.UUID,
        name: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Population:
        """
        Updates population information (name, description, metadata).
        At least one of name, description, or metadata must be provided.
        Requires write access to the population.
        """
        payload = UpdatePopulationInfoPayload(name=name, description=description, metadata=metadata)
        response_data = await self._request(
            "PUT",
            f"populations/update/{str(population_id)}",
            json=payload.model_dump(mode="json", exclude_none=True),
            response_model=Population,
        )
        return response_data

    async def get_population_info(self, population_id: str | uuid.UUID) -> PopulationInfo:
        """Gets basic population info (name and agent count) without full population data."""
        response_data = await self._request(
            "GET",
            f"populations/info/{str(population_id)}",
            response_model=PopulationInfo,
        )
        return response_data

    async def delete_population(self, population_id: str | uuid.UUID) -> DeletionResponse:
        response_data = await self._request(
            "DELETE",
            f"populations/delete/{str(population_id)}",
            response_model=DeletionResponse,
        )
        return response_data

    async def get_agents_in_population(self, population_id: str | uuid.UUID) -> list[AgentModel]:
        """Retrieves all agents belonging to a specific population."""
        endpoint = f"populations/{str(population_id)}/agents"
        raw_response = await self._request("GET", endpoint)
        agents_data_list = raw_response.json()
        return [AgentModel(**data) for data in agents_data_list]

    async def get_agent_ids_in_population(self, population_id: str | uuid.UUID) -> list[str]:
        """Retrieves only agent IDs for a population without full agent data.

        This is a lightweight alternative to get_agents_in_population when
        only agent IDs are needed.

        Args:
            population_id: The ID of the population

        Returns:
            List of agent ID strings
        """
        endpoint = f"populations/{str(population_id)}/agents/ids"
        raw_response = await self._request("GET", endpoint)
        return raw_response.json()

    async def create_agent(
        self,
        name: str,
        source: str | None = None,
        source_id: str | None = None,
        population_id: str | uuid.UUID | None = None,
        agent_data: list[dict[str, Any]] | None = None,
    ) -> AgentModel:
        """Creates a new agent, optionally within a population and with initial data items."""
        pop_id_uuid: uuid.UUID | None = None
        if population_id:
            pop_id_uuid = (
                uuid.UUID(str(population_id))
                if not isinstance(population_id, uuid.UUID)
                else population_id
            )

        payload = CreateAgentPayload(
            name=name,
            population_id=pop_id_uuid,
            agent_data=agent_data,
            source=source,
            source_id=source_id,
        )
        response_data = await self._request(
            "POST",
            "agents/create",
            json=payload.model_dump(mode="json", exclude_none=True),
            response_model=AgentModel,
        )
        return response_data

    async def get_agent(self, agent_id: str | uuid.UUID) -> AgentModel:
        response_data = await self._request(
            "GET", f"agents/get/{str(agent_id)}", response_model=AgentModel
        )
        return response_data

    async def update_agent_info(
        self,
        agent_id: str | uuid.UUID,
        name: str,
    ) -> AgentModel:
        """
        Updates agent information (name).
        Name must be provided.
        Requires write access to the agent.
        """
        payload = UpdateAgentInfoPayload(
            name=name,
        )
        response_data = await self._request(
            "PUT",
            f"agents/update/{str(agent_id)}",
            json=payload.model_dump(mode="json", exclude_none=True),
            response_model=AgentModel,
        )
        return response_data

    async def delete_agent(self, agent_id: str | uuid.UUID) -> DeletionResponse:
        response_data = await self._request(
            "DELETE", f"agents/delete/{str(agent_id)}", response_model=DeletionResponse
        )
        return response_data

    async def add_agent_to_population(
        self, agent_id: str | uuid.UUID, population_id: str | uuid.UUID
    ) -> dict[str, str]:
        """Add an agent to an additional population."""
        raw_response = await self._request(
            "POST", f"agents/{str(agent_id)}/populations/{str(population_id)}"
        )
        return raw_response.json()

    async def remove_agent_from_population(
        self, agent_id: str | uuid.UUID, population_id: str | uuid.UUID
    ) -> dict[str, str]:
        """Remove an agent from a population."""
        raw_response = await self._request(
            "DELETE", f"agents/{str(agent_id)}/populations/{str(population_id)}"
        )
        return raw_response.json()

    async def batch_add_agents_to_population(
        self,
        agent_ids: list[str | uuid.UUID],
        population_id: str | uuid.UUID,
    ) -> dict[str, Any]:
        """Add multiple agents to a population in a single batch operation."""
        agent_id_strs = [str(aid) for aid in agent_ids]
        raw_response = await self._request(
            "POST", f"populations/{str(population_id)}/agents/batch", json=agent_id_strs
        )
        return raw_response.json()

    async def get_populations_for_agent(self, agent_id: str | uuid.UUID) -> dict[str, Any]:
        """Get all populations an agent belongs to."""
        raw_response = await self._request("GET", f"agents/{str(agent_id)}/populations")
        return raw_response.json()

    async def create_data_item(
        self,
        agent_id: str | uuid.UUID,
        data_type: str,
        content: Any,
        metadata: dict[str, Any] | None = None,
    ) -> DataItem:
        """Creates a new data item for a specific agent."""
        payload = CreateDataItemPayload(data_type=data_type, content=content, metadata=metadata)
        response_data = await self._request(
            "POST",
            f"data_item/create/{str(agent_id)}",
            json=payload.model_dump(mode="json"),
            response_model=DataItem,
        )
        return response_data

    async def get_data_item(self, data_item_id: str | uuid.UUID) -> DataItem:
        response_data = await self._request(
            "GET", f"data_item/get/{str(data_item_id)}", response_model=DataItem
        )
        return response_data

    async def list_data_items(
        self, agent_id: str | uuid.UUID, data_type: str | None = None
    ) -> list[DataItem]:
        params = {}
        if data_type:
            params["data_type"] = data_type
        agent_id_str = str(agent_id)
        raw_response = await self._request("GET", f"data_item/list/{agent_id_str}", params=params)
        return [DataItem(**item) for item in raw_response.json()]

    async def update_data_item(
        self,
        data_item_id: str | uuid.UUID,
        content: Any,
        metadata: dict[str, Any] | None = None,
    ) -> DataItem:
        """Updates an existing data item."""
        payload = UpdateDataItemPayload(content=content, metadata=metadata)
        response_data = await self._request(
            "POST",
            f"data_item/update/{str(data_item_id)}",
            json=payload.model_dump(),
            response_model=DataItem,
        )
        return response_data

    async def delete_data_item(self, data_item_id: str | uuid.UUID) -> DeletionResponse:
        response_data = await self._request(
            "DELETE",
            f"data_item/delete/{str(data_item_id)}",
            response_model=DeletionResponse,
        )
        return response_data

    async def stream_open_response(
        self,
        agent_id: uuid.UUID,
        question: str,
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
        reasoning: bool = False,
        evidence: bool = False,
        confidence: bool = False,
        memory_stream: MemoryStream | None = None,  # noqa: ARG002
    ) -> AsyncGenerator[str, None]:
        """Streams an open response from an agent."""
        endpoint = f"/generation/open-stream/{str(agent_id)}"
        request_payload = OpenGenerationRequest(
            question=question,
            data_types=data_types,
            exclude_data_types=exclude_data_types,
            images=images,
            reasoning=reasoning,
            evidence=evidence,
            confidence=confidence,
        )

        url = self.base_url + endpoint  # assuming self.base_url is defined

        async with (
            httpx.AsyncClient(timeout=None) as client,
            client.stream("POST", url, json=request_payload.model_dump()) as response,
        ):
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip():  # skip empty lines
                    if line.startswith("data: "):  # optional, if using SSE format
                        yield line.removeprefix("data: ").strip()
                    else:
                        yield line.strip()

    async def stream_closed_response(
        self,
        agent_id: uuid.UUID,
        question: str,
        options: list[str],
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
    ) -> AsyncGenerator[str, None]:
        """Streams a closed response from an agent."""
        endpoint = f"/generation/closed-stream/{str(agent_id)}"

        request_payload = {
            "question": question,
            "options": options,
            "data_types": data_types,
            "exclude_data_types": exclude_data_types,
            "images": images,
        }

        url = self.base_url + endpoint  # assuming self.base_url is defined

        async with (
            httpx.AsyncClient(timeout=None) as client,
            client.stream("POST", url, json=request_payload) as response,
        ):
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip():  # skip empty lines
                    if line.startswith("data: "):  # optional, if using SSE format
                        yield line.removeprefix("data: ").strip()
                    else:
                        yield line.strip()

    async def generate_open_response(
        self,
        agent_id: uuid.UUID,
        question: str,
        question_id: str | None = None,
        study_id: str | None = None,
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
        reasoning: bool = False,
        evidence: bool = False,
        confidence: bool = False,
        memory_stream: MemoryStream | None = None,
        use_memory: str | uuid.UUID | None = None,  # Session ID to load memory from
        exclude_memory_ids: list[str] | None = None,  # Study/question IDs to exclude
        save_memory: str | uuid.UUID | None = None,  # Session ID to save memory to
        include_data_room: bool | None = False,
        organization_id: str | None = None,
        data_room_context: str | None = None,
    ) -> OpenGenerationResponse:
        """Generates an open response from an agent based on a question.

        Args:
            agent_id: The agent to query
            question: The question to ask
            question_id: Optional question ID for tracking
            study_id: Optional study ID for tracking
            data_types: Optional data types to include
            exclude_data_types: Optional data types to exclude
            images: Optional images dict
            reasoning: Whether to include reasoning
            memory_stream: Explicit memory stream to use (overrides use_memory)
            use_memory: Session ID to automatically load memory from
            exclude_memory_ids: Study/question IDs to exclude from loaded memory
            save_memory: Session ID to automatically save response to memory
            include_data_room: Whether to include data room info
            organization_id: Optional organization ID
            data_room_context: Optional data room context
        """
        endpoint = f"/generation/open/{str(agent_id)}"
        # Build request payload directly as dict to avoid serialization issues
        request_payload = {
            "question": question,
            "question_id": question_id,
            "study_id": study_id,
            "data_types": data_types,
            "exclude_data_types": exclude_data_types,
            "images": images,
            "reasoning": reasoning,
            "evidence": evidence,
            "confidence": confidence,
        }

        # Conditionally add optional fields
        if include_data_room is not None:
            request_payload["include_data_room"] = include_data_room
        if organization_id is not None:
            request_payload["organization_id"] = organization_id
        if data_room_context is not None:
            request_payload["data_room_context"] = data_room_context

        # Pass memory parameters to API for server-side handling
        if use_memory:
            request_payload["use_memory"] = str(use_memory)
            if exclude_memory_ids:
                request_payload["exclude_memory_ids"] = exclude_memory_ids

        if save_memory:
            request_payload["save_memory"] = str(save_memory)

        # Only include explicit memory_stream if provided directly
        if memory_stream:
            request_payload["memory_stream"] = memory_stream.to_dict()

        response_data = await self._request(
            "POST",
            endpoint,
            json=request_payload,
            response_model=OpenGenerationResponse,
        )

        # Don't save memory here - API should handle it when save_memory is passed
        # Memory saving is now handled server-side for better performance

        return response_data

    async def generate_closed_response(
        self,
        agent_id: uuid.UUID,
        question: str,
        options: list[str],
        question_id: str | None = None,
        study_id: str | None = None,
        data_types: list[str] | None = None,
        exclude_data_types: list[str] | None = None,
        images: dict[str, str] | None = None,
        reasoning: bool = False,
        evidence: bool = False,
        confidence: bool = False,
        memory_stream: MemoryStream | None = None,
        use_memory: str | uuid.UUID | None = None,  # Session ID to load memory from
        exclude_memory_ids: list[str] | None = None,  # Study/question IDs to exclude
        save_memory: str | uuid.UUID | None = None,  # Session ID to save memory to
        summary_mode: bool = True,  # noqa: ARG002
        method: str | None = None,  # noqa: ARG002  # Sampling method; defaults to tool-call-random-sampling
        include_data_room: bool | None = False,
        organization_id: str | None = None,
        data_room_context: str | None = None,
    ) -> ClosedGenerationResponse:
        """Generates a closed response from an agent.

        Args:
            agent_id: The agent to query
            question: The question to ask
            options: The options to choose from
            question_id: Optional question ID for tracking
            study_id: Optional study ID for tracking
            data_types: Optional data types to include
            exclude_data_types: Optional data types to exclude
            images: Optional images dict
            reasoning: Whether to include reasoning
            memory_stream: Explicit memory stream to use (overrides use_memory)
            use_memory: Session ID to automatically load memory from
            exclude_memory_ids: Study/question IDs to exclude from loaded memory
            save_memory: Session ID to automatically save response to memory
            include_data_room: Whether to include data room info
            organization_id: Optional organization ID
            data_room_context: Optional data room context
        """
        endpoint = f"generation/closed/{str(agent_id)}"
        # Build request payload directly as dict to avoid serialization issues
        request_payload = {
            "question": question,
            "options": options,
            "question_id": question_id,
            "study_id": study_id,
            "data_types": data_types,
            "exclude_data_types": exclude_data_types,
            "images": images,
            "reasoning": reasoning,
            "evidence": evidence,
            "confidence": confidence,
        }

        # Conditionally add optional fields
        if include_data_room is not None:
            request_payload["include_data_room"] = include_data_room
        if organization_id is not None:
            request_payload["organization_id"] = organization_id
        if data_room_context is not None:
            request_payload["data_room_context"] = data_room_context

        # Pass memory parameters to API for server-side handling
        if use_memory:
            request_payload["use_memory"] = str(use_memory)
            if exclude_memory_ids:
                request_payload["exclude_memory_ids"] = exclude_memory_ids

        if save_memory:
            request_payload["save_memory"] = str(save_memory)

        # Only include explicit memory_stream if provided directly
        if memory_stream:
            request_payload["memory_stream"] = memory_stream.to_dict()

        response_data = await self._request(
            "POST",
            endpoint,
            json=request_payload,
            response_model=ClosedGenerationResponse,
        )

        # Don't save memory here - API should handle it when save_memory is passed
        # Memory saving is now handled server-side for better performance

        return response_data

    # Memory Management Methods

    async def save_memory(
        self,
        agent_id: str | uuid.UUID,
        response: str,
        session_id: str | uuid.UUID | None = None,
        question_id: str | uuid.UUID | None = None,
        study_id: str | uuid.UUID | None = None,
        memory_turn: dict[str, Any] | None = None,
        memory_stream_used: dict[str, Any] | None = None,
        reasoning: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """
        Save a response with associated memory information.

        Args:
            agent_id: The agent ID
            response: The agent's response text
            session_id: Session ID for memory continuity
            question_id: The question ID (optional)
            study_id: The study ID (optional)
            memory_turn: The memory turn to save
            memory_stream_used: The memory stream that was used
            reasoning: Optional reasoning
            metadata: Additional metadata

        Returns:
            Response ID if saved successfully
        """
        payload = {
            "agent_id": str(agent_id),
            "response": response,
        }

        if session_id:
            payload["session_id"] = str(session_id)
        if question_id:
            payload["question_id"] = str(question_id)
        if study_id:
            payload["study_id"] = str(study_id)
        if memory_turn:
            payload["memory_turn"] = memory_turn
        if memory_stream_used:
            payload["memory_stream_used"] = memory_stream_used
        if reasoning:
            payload["reasoning"] = reasoning
        if metadata:
            payload["metadata"] = metadata

        response = await self._request("POST", "memory/save", json=payload)
        data = response.json()
        if data.get("success"):
            return data.get("response_id")
        raise SimileAPIError("Failed to save memory")

    async def get_memory(
        self,
        session_id: str | uuid.UUID,
        agent_id: str | uuid.UUID,
        exclude_study_ids: list[str | uuid.UUID] | None = None,
        exclude_question_ids: list[str | uuid.UUID] | None = None,
        limit: int | None = None,
        use_memory: bool = True,
    ) -> MemoryStream | None:
        """
        Retrieve the memory stream for an agent in a session.

        Args:
            session_id: Session ID to filter by
            agent_id: The agent ID
            exclude_study_ids: List of study IDs to exclude
            exclude_question_ids: List of question IDs to exclude
            limit: Maximum number of turns to include
            use_memory: Whether to use memory at all

        Returns:
            MemoryStream object or None
        """
        payload = {
            "session_id": str(session_id),
            "agent_id": str(agent_id),
            "use_memory": use_memory,
        }

        if exclude_study_ids:
            payload["exclude_study_ids"] = [str(id) for id in exclude_study_ids]
        if exclude_question_ids:
            payload["exclude_question_ids"] = [str(id) for id in exclude_question_ids]
        if limit:
            payload["limit"] = limit

        response = await self._request("POST", "memory/get", json=payload)
        data = response.json()

        if data.get("success") and data.get("memory_stream"):
            return MemoryStream.from_dict(data["memory_stream"])
        return None

    async def get_memory_summary(
        self,
        session_id: str | uuid.UUID,
    ) -> dict[str, Any]:
        """
        Get a summary of memory usage for a session.

        Args:
            session_id: Session ID to analyze

        Returns:
            Dictionary with memory statistics
        """
        response = await self._request("GET", f"memory/summary/{session_id}")
        data = response.json()
        if data.get("success"):
            return data.get("summary", {})
        return {}

    async def clear_memory(
        self,
        session_id: str | uuid.UUID,
        agent_id: str | uuid.UUID | None = None,
        study_id: str | uuid.UUID | None = None,
    ) -> bool:
        """
        Clear memory for a session, optionally filtered by agent or study.

        Args:
            session_id: Session ID to clear memory for
            agent_id: Optional agent ID to filter by
            study_id: Optional study ID to filter by

        Returns:
            True if cleared successfully, False otherwise
        """
        payload = {
            "session_id": str(session_id),
        }

        if agent_id:
            payload["agent_id"] = str(agent_id)
        if study_id:
            payload["study_id"] = str(study_id)

        response = await self._request("POST", "memory/clear", json=payload)
        data = response.json()
        return data.get("success", False)

    async def copy_memory(
        self,
        from_session_id: str | uuid.UUID,
        to_session_id: str | uuid.UUID,
        agent_id: str | uuid.UUID | None = None,
    ) -> int:
        """
        Copy memory from one session to another.

        Args:
            from_session_id: Source session ID
            to_session_id: Destination session ID
            agent_id: Optional agent ID to filter by

        Returns:
            Number of memory turns copied
        """
        payload = {
            "from_session_id": str(from_session_id),
            "to_session_id": str(to_session_id),
        }

        if agent_id:
            payload["agent_id"] = str(agent_id)

        response = await self._request("POST", "memory/copy", json=payload)
        data = response.json()
        if data.get("success"):
            return data.get("copied_turns", 0)
        return 0

    async def aclose(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
