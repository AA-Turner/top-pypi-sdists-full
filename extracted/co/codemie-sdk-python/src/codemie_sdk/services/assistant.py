"""Assistant service implementation."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Union, Any, Literal, Optional, Dict
from pydantic import BaseModel
from copy import deepcopy

import requests
import mimetypes

from ..models.assistant import (
    Assistant,
    AssistantCreateRequest,
    AssistantUpdateRequest,
    AssistantCreateResponse,
    AssistantUpdateResponse,
    BuiltinSubagent,
    ToolKitDetails,
    AssistantChatRequest,
    VirtualAssistantChatRequest,
    BaseModelResponse,
    AssistantBase,
    Context,
    ExportAssistantPayload,
    AssistantEvaluationRequest,
    ReactionRequest,
    ToolCallResumeRequest,
)
from ..models.common import PaginationParams
from ..utils import ApiRequestHandler, TokenSource


class AssistantService:
    """Service for managing CodeMie assistants."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the assistant service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def list(
        self,
        minimal_response: bool = True,
        scope: Literal["visible_to_user", "marketplace"] = "visible_to_user",
        page: int = 0,
        per_page: int = 12,
        filters: dict[str, Any] | None = None,
        sort_by: str | None = None,
        sort_order: str = "desc",
    ) -> list[Assistant | AssistantBase]:
        """Get list of available assistants.

        Args:
            minimal_response: Whether to return minimal assistant info
            scope: Visibility scope of assistants to retrieve
            page: Page number for pagination
            per_page: Number of items per page
            filters: Optional filters to apply
            sort_by: Sort field; one of "usage", "likes", "dislikes", "name". None = default ordering.
            sort_order: Sort direction; "asc" or "desc" (default "desc"). Only used when sort_by is set.

        Returns:
            List of assistants matching the criteria
        """
        params = PaginationParams(page=page, per_page=per_page).to_dict()
        params["scope"] = scope
        params["minimal_response"] = minimal_response
        if filters:
            params["filters"] = json.dumps(filters)
        if sort_by is not None:
            params["sort_by"] = sort_by
            params["sort_order"] = sort_order

        model = AssistantBase if minimal_response else Assistant
        return self._api.get("/v1/assistants", list[model], params=params)

    def get(self, assistant_id: str) -> Assistant:
        """Get assistant by ID.

        Args:
            assistant_id: ID of the assistant to retrieve

        Returns:
            Assistant details
        """
        return self._api.get(f"/v1/assistants/id/{assistant_id}", Assistant)

    def get_by_slug(self, slug: str) -> Assistant:
        """Get assistant by slug.

        Args:
            slug: Slug of the assistant to retrieve

        Returns:
            Assistant details
        """
        return self._api.get(f"/v1/assistants/slug/{slug}", Assistant)

    def create(self, request: AssistantCreateRequest) -> AssistantCreateResponse:
        """Create a new assistant.

        Args:
            request: Assistant creation request

        Returns:
            AssistantCreateResponse with assistant_id and optional validation results
        """
        return self._api.post(
            "/v1/assistants",
            AssistantCreateResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def update(
        self, assistant_id: str, request: AssistantUpdateRequest
    ) -> AssistantUpdateResponse:
        """Update an existing assistant.

        Args:
            assistant_id: ID of the assistant to update
            request: Assistant update request

        Returns:
            AssistantUpdateResponse with optional validation results
        """
        return self._api.put(
            f"/v1/assistants/{assistant_id}",
            AssistantUpdateResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def get_tools(self) -> list[ToolKitDetails]:
        """Get list of available tools.

        Returns:
            List of available tool kits
        """
        return self._api.get(
            "/v1/assistants/tools", list[ToolKitDetails], wrap_response=False
        )

    def get_context(self, project_name: str) -> list[Context]:
        """Get list of available contexts.

        Args: project_name: Name of the project to retrieve context for

        Returns:
            All available assistants context
        """
        params = {"project_name": project_name}
        return self._api.get("/v1/assistants/context", list[Context], params=params)

    def get_builtin_subagents(self) -> list[BuiltinSubagent]:
        """Get list of available built-in subagents.

        Returns:
            List of built-in subagent catalog entries
        """
        return self._api.get(
            "/v1/assistants/builtin_subagents",
            list[BuiltinSubagent],
            wrap_response=False,
        )

    def delete(self, assistant_id: str) -> dict:
        """Delete an assistant by ID.

        Args:
            assistant_id: ID of the assistant to delete

        Returns:
            Deletion confirmation
        """
        return self._api.delete(f"/v1/assistants/{assistant_id}", dict)

    def get_prebuilt(self) -> list[Assistant]:
        """Get list of prebuilt assistants.

        Returns:
            List of prebuilt assistants
        """
        return self._api.get("/v1/assistants/prebuilt", list[Assistant])

    def get_prebuilt_by_slug(self, slug: str) -> Assistant:
        """Get prebuilt assistant by slug.

        Args:
            slug: Slug of the prebuilt assistant to retrieve

        Returns:
            Prebuilt assistant details
        """
        return self._api.get(f"/v1/assistants/prebuilt/{slug}", Assistant)

    def list_versions(
        self, assistant_id: str, page: int = 0, per_page: int | None = None
    ):
        """List assistant versions.

        Args:
            assistant_id: Assistant identifier
            page: Page number for pagination
            per_page: Items per page (optional). If not provided, backend defaults are used.

        Returns:
            List of AssistantVersion objects
        """

        params: dict[str, Any] = {"page": page}
        if per_page is not None:
            params["per_page"] = per_page
        from ..models.assistant import AssistantVersion

        raw = self._api.get(
            f"/v1/assistants/{assistant_id}/versions",
            dict,
            params=params,
            wrap_response=False,
        )
        items = []
        if isinstance(raw, list):
            items = raw
        elif isinstance(raw, dict):
            items = raw.get("data") or raw.get("versions") or []
        else:
            items = []
        return [AssistantVersion.model_validate(it) for it in items]

    def get_version(self, assistant_id: str, version_number: int):
        """Get a specific assistant version by number.

        Args:
            assistant_id: Assistant identifier
            version_number: Version number to retrieve

        Returns:
            AssistantVersion object
        """
        from ..models.assistant import AssistantVersion

        raw = self._api.get(
            f"/v1/assistants/{assistant_id}/versions/{version_number}", AssistantVersion
        )
        if isinstance(raw, dict):
            return AssistantVersion.model_validate(raw)
        return raw

    def compare_versions(self, assistant_id: str, v1: int, v2: int) -> dict[str, Any]:
        """Compare two assistant versions and return diff summary.

        Args:
            assistant_id: Assistant identifier
            v1: First version number
            v2: Second version number

        Returns:
            Generic dictionary with comparison result (diff, summary, etc.)
        """
        return self._api.get(
            f"/v1/assistants/{assistant_id}/versions/{v1}/compare/{v2}",
            dict,
        )

    def rollback_to_version(
        self, assistant_id: str, version_number: int, change_notes: str | None = None
    ) -> dict:
        """Rollback assistant to a specific version. Creates a new version mirroring target.

        Args:
            assistant_id: Assistant identifier
            version_number: Target version to rollback to
            change_notes: Optional description of why rollback is performed

        Returns:
            Backend response (dict)
        """
        payload: dict[str, Any] = {}
        if change_notes:
            payload["change_notes"] = change_notes
        try:
            return self._api.post(
                f"/v1/assistants/{assistant_id}/versions/{version_number}/rollback",
                dict,
                json_data=payload,
            )
        except requests.HTTPError as err:
            try:
                assistant = self.get(assistant_id)
                version = self.get_version(assistant_id, version_number)

                update_req = AssistantUpdateRequest(
                    name=assistant.name,
                    description=assistant.description or "",
                    system_prompt=version.system_prompt,
                    project=assistant.project,
                    llm_model_type=version.llm_model_type or assistant.llm_model_type,
                    temperature=version.temperature
                    if hasattr(version, "temperature")
                    else assistant.temperature,
                    top_p=version.top_p
                    if hasattr(version, "top_p")
                    else assistant.top_p,
                    context=version.context
                    if hasattr(version, "context")
                    else assistant.context,
                    toolkits=version.toolkits
                    if hasattr(version, "toolkits")
                    else assistant.toolkits,
                    user_prompts=assistant.user_prompts,
                    shared=assistant.shared,
                    is_react=assistant.is_react,
                    is_global=assistant.is_global,
                    slug=assistant.slug,
                    mcp_servers=version.mcp_servers
                    if hasattr(version, "mcp_servers")
                    else assistant.mcp_servers,
                    assistant_ids=version.assistant_ids
                    if hasattr(version, "assistant_ids")
                    else assistant.assistant_ids,
                )
                update_resp = self.update(assistant_id, update_req)
                resp = update_resp.model_dump()
                resp["_rollback_fallback"] = True
                resp["_target_version"] = version_number
                if change_notes:
                    resp["change_notes"] = change_notes
                return resp
            except Exception:
                raise err

    def chat(
        self,
        assistant_id: str,
        request: AssistantChatRequest,
        headers: dict[str, str] | None = None,
    ) -> Union[requests.Response, BaseModelResponse]:
        """Send a chat request to an assistant.

        Args:
            assistant_id: ID of the assistant to chat with
            request: Chat request details
            headers: Optional additional HTTP headers (e.g., X-* for MCP propagation)

        Returns:
            Chat response or streaming response
        """
        pydantic_schema = None
        if (
            request.output_schema is not None
            and inspect.isclass(request.output_schema)
            and issubclass(request.output_schema, BaseModel)
        ):
            pydantic_schema = deepcopy(request.output_schema)
            request.output_schema = request.output_schema.model_json_schema()

        response = self._api.post(
            f"/v1/assistants/{assistant_id}/model",
            BaseModelResponse,
            json_data=request.model_dump(exclude_none=True, by_alias=True),
            stream=request.stream,
            extra_headers=headers,
        )
        if not request.stream and pydantic_schema:
            # we do conversion to the BaseModel here because self._parse_response don't see actual request model,
            # where reflected desired output format for structured output
            response.generated = pydantic_schema.model_validate(response.generated)

        return response

    def chat_with_version(
        self,
        assistant_id: str,
        version_number: int,
        request: AssistantChatRequest,
    ) -> Union[requests.Response, BaseModelResponse]:
        """Send a chat request to a specific assistant version.

        Uses the stable chat endpoint with an explicit `version` parameter to
        ensure compatibility with environments that don't expose
        /versions/{version}/model.

        Args:
            assistant_id: ID of the assistant to chat with
            version_number: version to pin chat to
            request: Chat request details

        Returns:
            Chat response or streaming response
        """
        pydantic_schema = None
        if (
            request.output_schema is not None
            and inspect.isclass(request.output_schema)
            and issubclass(request.output_schema, BaseModel)
        ):
            pydantic_schema = deepcopy(request.output_schema)
            request.output_schema = request.output_schema.model_json_schema()

        payload = request.model_dump(exclude_none=True, by_alias=True)
        payload["version"] = version_number

        response = self._api.post(
            f"/v1/assistants/{assistant_id}/model",
            BaseModelResponse,
            json_data=payload,
            stream=request.stream,
        )
        if not request.stream and pydantic_schema:
            response.generated = pydantic_schema.model_validate(response.generated)

        return response

    def chat_by_slug(
        self,
        assistant_slug: str,
        request: AssistantChatRequest,
        headers: dict[str, str] | None = None,
    ) -> Union[requests.Response, BaseModelResponse]:
        """Send a chat request to an assistant by slug.

        Args:
            assistant_slug: Slug of the assistant to chat with
            request: Chat request details
            headers: Optional additional HTTP headers (e.g., X-* for MCP propagation)

        Returns:
            Chat response or streaming response
        """
        pydantic_schema = None
        if (
            request.output_schema is not None
            and inspect.isclass(request.output_schema)
            and issubclass(request.output_schema, BaseModel)
        ):
            pydantic_schema = deepcopy(request.output_schema)
            request.output_schema = request.output_schema.model_json_schema()

        response = self._api.post(
            f"/v1/assistants/slug/{assistant_slug}/model",
            BaseModelResponse,
            json_data=request.model_dump(exclude_none=True, by_alias=True),
            stream=request.stream,
            extra_headers=headers,
        )
        if not request.stream and pydantic_schema:
            response.generated = pydantic_schema.model_validate(response.generated)

        return response

    def ask_virtual(
        self,
        request: VirtualAssistantChatRequest,
        headers: Optional[Dict[str, str]] = None,
    ) -> Union[requests.Response, BaseModelResponse]:
        """Run inference using an inline (virtual) assistant definition.

        No database assistant record is required. History is never persisted.

        Args:
            request: Virtual assistant chat request with inline assistant definition
            headers: Optional additional HTTP headers (e.g., X-* for MCP propagation)

        Returns:
            Chat response or streaming response
        """
        pydantic_schema = None
        if (
            request.output_schema is not None
            and inspect.isclass(request.output_schema)
            and issubclass(request.output_schema, BaseModel)
        ):
            pydantic_schema = deepcopy(request.output_schema)
            request.output_schema = request.output_schema.model_json_schema()

        response = self._api.post(
            "/v1/assistants/virtual/model",
            BaseModelResponse,
            json_data=request.model_dump(exclude_none=True, by_alias=True),
            stream=request.stream,
            extra_headers=headers,
        )
        if not request.stream and pydantic_schema:
            response.generated = pydantic_schema.model_validate(response.generated)

        return response

    def upload_file_to_chat(self, file_path: Path):
        """Upload a file to assistant chat and return the response containing file_url."""

        with open(file_path, "rb") as file:
            files = [
                (
                    "file",
                    (
                        file_path.name,
                        file,
                        mimetypes.guess_type(file_path.name)[0]
                        or "application/octet-stream",
                    ),
                ),
            ]
            response = self._api.post_multipart("/v1/files/", dict, files=files)

        return response

    def export(self, assistant_id: str, request: ExportAssistantPayload):
        """Export an assistant.

        Args:
            assistant_id: ID of the assistant to export
            request: Export request details

        Returns:
             input stream of the exported assistant file"""

        return self._api.post(
            f"/v1/assistants/id/{assistant_id}/export",
            response_model=Any,
            stream=True,
            json_data=request.model_dump(exclude_none=True),
        )

    def evaluate(self, assistant_id: str, request: AssistantEvaluationRequest) -> dict:
        """Evaluate an assistant with a dataset.

        Args:
            assistant_id: ID of the assistant to evaluate
            request: Evaluation request details

        Returns:
            Evaluation results
        """
        return self._api.post(
            f"/v1/assistants/{assistant_id}/evaluate",
            dict,
            json_data=request.model_dump(exclude_none=True),
        )

    def publish(
        self,
        assistant_id: str,
        categories: list[str] | None = None,
        ignore_recommendations: bool = False,
    ) -> dict:
        """Publish an assistant to the marketplace.
        Args:
            assistant_id: ID of the assistant to publish
            categories: List of categories for marketplace classification (e.g., ['quality-assurance'])
            ignore_recommendations: If True, bypass validation and publish anyway
        """
        body = {}
        if categories:
            body["categories"] = categories
        if ignore_recommendations:
            body["ignore_recommendations"] = ignore_recommendations

        return self._api.post(
            f"/v1/assistants/{assistant_id}/marketplace/publish",
            dict,
            json_data=body if body else None,
        )

    def unpublish(self, assistant_id: str) -> dict:
        """Unpublish an assistant from the marketplace.
        Args:
            assistant_id: ID of the assistant to publish
        """
        return self._api.post(
            f"/v1/assistants/{assistant_id}/marketplace/unpublish", dict
        )

    def marketplace_validate(self, assistant_id: str) -> dict:
        """Validate an assistant before publishing to the marketplace.
        Args:
            assistant_id: ID of the assistant to validate
        """
        return self._api.post(
            f"/v1/assistants/{assistant_id}/marketplace/publish/validate", dict
        )

    def resume_tool_call(
        self,
        assistant_id: str,
        request: ToolCallResumeRequest,
    ):
        """Resume a paused tool-call after user approval or denial.

        Calls POST /v1/assistants/{id}/model/tool-call/resume.
        When stream=True, returns the raw streaming requests.Response so the
        caller can iterate the NDJSON chunks.  When stream=False, returns a
        parsed dict containing the final generated text.

        Args:
            assistant_id: ID of the assistant that has a pending tool call
            request: Resume request with conversation_id, action, and stream flag

        Returns:
            requests.Response (streaming) or dict (non-streaming)
        """
        import requests as _requests

        response = self._api.post(
            f"/v1/assistants/{assistant_id}/model/tool-call/resume",
            _requests.Response,
            json_data=request.model_dump(),
            stream=request.stream,
        )
        return response

    def react(self, assistant_id: str, request: ReactionRequest) -> dict:
        """React to an assistant with like or dislike.

        If the user already has the opposite reaction, it will be removed.

        Args:
            assistant_id: ID of the assistant to react to
            request: Reaction request containing reaction type ('like' or 'dislike')

        Returns:
            Response from the API
        """
        return self._api.post(
            f"/v1/assistants/{assistant_id}/reactions",
            dict,
            json_data=request.model_dump(exclude_none=True),
        )

    def remove_reactions(self, assistant_id: str) -> dict:
        """Remove all reactions (likes/dislikes) from an assistant for the current user.

        Args:
            assistant_id: ID of the assistant to remove reactions from

        Returns:
            Response from the API
        """
        return self._api.delete(f"/v1/assistants/{assistant_id}/reactions", dict)
