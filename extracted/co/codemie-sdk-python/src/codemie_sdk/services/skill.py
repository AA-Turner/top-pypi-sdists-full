"""Skill service implementation."""

from __future__ import annotations

import json
from typing import Any

from ..models.skill import (
    SkillAttachRequest,
    SkillBulkAttachRequest,
    SkillCategory,
    SkillConfigResponse,
    SkillCreateRequest,
    SkillDetailResponse,
    SkillEventItem,
    SkillEventRequest,
    SkillImportRequest,
    SkillListPaginatedResponse,
    SkillListResponse,
    SkillStatsItem,
    SkillUpdateRequest,
    SingleSkillStatsResponse,
)
from ..utils.http import ApiRequestHandler, TokenSource


class SkillService:
    """Service for managing CodeMie skills."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the skill service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates. Default: True
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    # Core CRUD Operations

    def list(
        self,
        page: int = 0,
        per_page: int = 12,
        filters: dict[str, Any] | None = None,
    ) -> SkillListPaginatedResponse:
        """List skills with pagination.

        Args:
            page: Page number (0-based)
            per_page: Number of items per page
            filters: Optional filters for skills

        Returns:
            Paginated list of skills
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if filters:
            params["filters"] = json.dumps(filters)
        return self._api.get("/v1/skills", SkillListPaginatedResponse, params=params)

    def get(self, skill_id: str) -> SkillDetailResponse:
        """Get skill by ID.

        Args:
            skill_id: Skill identifier

        Returns:
            Full skill details
        """
        return self._api.get(f"/v1/skills/{skill_id}", SkillDetailResponse)

    def create(self, request: SkillCreateRequest) -> SkillDetailResponse:
        """Create a new skill.

        Args:
            request: Skill creation request

        Returns:
            Created skill details
        """
        return self._api.post(
            "/v1/skills",
            SkillDetailResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def update(self, skill_id: str, request: SkillUpdateRequest) -> SkillDetailResponse:
        """Update an existing skill.

        Args:
            skill_id: Skill identifier
            request: Skill update request

        Returns:
            Updated skill details
        """
        return self._api.put(
            f"/v1/skills/{skill_id}",
            SkillDetailResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def delete(self, skill_id: str) -> dict:
        """Delete a skill.

        Args:
            skill_id: Skill identifier

        Returns:
            Deletion confirmation
        """
        return self._api.delete(f"/v1/skills/{skill_id}", dict)

    # Import/Export Operations

    def import_skill(self, request: SkillImportRequest) -> SkillDetailResponse:
        """Import skill from .md file content.

        Args:
            request: Skill import request with file content

        Returns:
            Imported skill details
        """
        return self._api.post(
            "/v1/skills/import",
            SkillDetailResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def export(self, skill_id: str) -> str:
        """Export skill.

        Args:
            skill_id: Skill identifier

        Returns:
            Exported skill markdown content
        """
        # Export returns raw markdown content, not JSON
        response = self._api.get(
            f"/v1/skills/{skill_id}/export", None, wrap_response=False
        )
        return response.text

    # Assistant Integration

    def attach_to_assistant(self, assistant_id: str, skill_id: str) -> dict:
        """Attach skill to an assistant.

        Args:
            assistant_id: Assistant identifier
            skill_id: Skill identifier

        Returns:
            Attachment confirmation
        """
        request = SkillAttachRequest(skill_id=skill_id)
        return self._api.post(
            f"/v1/assistants/{assistant_id}/skills",
            dict,
            json_data=request.model_dump(),
        )

    def detach_from_assistant(self, assistant_id: str, skill_id: str) -> dict:
        """Detach skill from an assistant.

        Args:
            assistant_id: Assistant identifier
            skill_id: Skill identifier

        Returns:
            Detachment confirmation
        """
        return self._api.delete(
            f"/v1/assistants/{assistant_id}/skills/{skill_id}", dict
        )

    def get_assistant_skills(self, assistant_id: str) -> list[SkillListResponse]:
        """Get all skills attached to an assistant.

        Args:
            assistant_id: Assistant identifier

        Returns:
            List of skills attached to the assistant
        """
        return self._api.get(
            f"/v1/assistants/{assistant_id}/skills",
            list[SkillListResponse],
        )

    def bulk_attach_to_assistants(
        self, skill_id: str, assistant_ids: list[str]
    ) -> dict:
        """Bulk attach skill to multiple assistants.

        Args:
            skill_id: Skill identifier
            assistant_ids: List of assistant identifiers

        Returns:
            Bulk attachment confirmation
        """
        request = SkillBulkAttachRequest(assistant_ids=assistant_ids)
        return self._api.post(
            f"/v1/skills/{skill_id}/assistants/bulk-attach",
            dict,
            json_data=request.model_dump(),
        )

    def get_skill_assistants(self, skill_id: str) -> list[dict]:
        """Get all assistants using this skill.

        Args:
            skill_id: Skill identifier

        Returns:
            List of assistants using the skill
        """
        return self._api.get(f"/v1/skills/{skill_id}/assistants", list[dict])

    # Marketplace Operations

    def publish(
        self,
        skill_id: str,
        categories: list[str] | None = None,
    ) -> dict:
        """Publish skill to marketplace.

        Args:
            skill_id: Skill identifier
            categories: Optional list of category IDs

        Returns:
            Publication confirmation
        """
        body = {}
        if categories:
            body["categories"] = categories
        return self._api.post(
            f"/v1/skills/{skill_id}/marketplace/publish",
            dict,
            json_data=body if body else None,
        )

    def unpublish(self, skill_id: str) -> dict:
        """Unpublish skill from marketplace.

        Args:
            skill_id: Skill identifier

        Returns:
            Unpublication confirmation
        """
        return self._api.post(f"/v1/skills/{skill_id}/marketplace/unpublish", dict)

    # Utility Methods

    def list_categories(self) -> list[SkillCategory]:
        """Get list of available skill categories.

        Returns:
            List of skill categories
        """
        return self._api.get("/v1/skills/categories", list[SkillCategory])

    def get_users(self) -> list[dict]:
        """Get skill users.

        Returns:
            List of users with access to skills
        """
        return self._api.get("/v1/skills/users", list[dict])

    # Reactions

    def react(self, skill_id: str, reaction: str) -> dict:
        """React to a skill.

        Args:
            skill_id: Skill identifier
            reaction: Reaction type (e.g., "like", "dislike")

        Returns:
            Reaction confirmation
        """
        return self._api.post(
            f"/v1/skills/{skill_id}/reactions",
            dict,
            json_data={"reaction": reaction},
        )

    def remove_reactions(self, skill_id: str) -> dict:
        """Remove reactions from a skill.

        Args:
            skill_id: Skill identifier

        Returns:
            Removal confirmation
        """
        return self._api.delete(f"/v1/skills/{skill_id}/reactions", dict)

    # Statistics / Event Log

    def record_event(self, request: SkillEventRequest) -> dict:
        """Record a skill lifecycle event.

        Args:
            request: Skill event request

        Returns:
            Confirmation dict
        """
        return self._api.post(
            "/v1/skills/events",
            dict,
            json_data=request.model_dump(exclude_none=True),
        )

    def get_events(
        self,
        from_: str | None = None,
        to: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[SkillEventItem]:
        """Get raw skill event log.

        Args:
            from_: ISO datetime lower bound (inclusive)
            to: ISO datetime upper bound (inclusive)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of skill event items
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if from_ is not None:
            params["from"] = from_
        if to is not None:
            params["to"] = to
        return self._api.get("/v1/skills/events", list[SkillEventItem], params=params)

    def get_events_stats(
        self,
        from_: str | None = None,
        to: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[SkillStatsItem]:
        """Get per-skill aggregated install/removal counts.

        Args:
            from_: ISO datetime lower bound (inclusive)
            to: ISO datetime upper bound (inclusive)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of skill stats items
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if from_ is not None:
            params["from"] = from_
        if to is not None:
            params["to"] = to
        return self._api.get(
            "/v1/skills/events/stats", list[SkillStatsItem], params=params
        )

    def get_skill_stats(self, slug: str) -> SingleSkillStatsResponse:
        """Get aggregated stats for a single skill.

        Args:
            slug: Skill slug identifier

        Returns:
            Single skill stats
        """
        return self._api.get(
            f"/v1/skills/events/{slug}/stats", SingleSkillStatsResponse
        )

    def get_config(self) -> SkillConfigResponse:
        """Get effective skill content-length limits.

        Returns:
            Skill config with max_content_length and min_content_length
        """
        return self._api.get("/v1/skills/config", SkillConfigResponse)
