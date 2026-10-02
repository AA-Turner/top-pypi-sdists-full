"""Project budget groups service for the CodeMie SDK."""

from ..utils import ApiRequestHandler, TokenSource


class ProjectBudgetGroupsService:
    """Service for managing project budget group distributions."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the project budget groups service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def list_by_project(self, project_name: str) -> dict:
        """List project budget groups for a given project.

        Args:
            project_name: The project name to filter by.

        Returns:
            Response dict containing ``items`` list and ``total``.
        """
        if not project_name:
            raise ValueError("project_name must be a non-empty string")
        return self._api.get(
            "/v1/admin/project-budget-groups",
            dict,
            params={"project_name": project_name},
            wrap_response=False,
        )

    def get(self, group_id: str) -> dict:
        """Get a project budget group by ID.

        Args:
            group_id: The budget group identifier

        Returns:
            Budget group data as dict
        """
        if not group_id:
            raise ValueError("group_id must be a non-empty string")
        return self._api.get(
            f"/v1/admin/project-budget-groups/{group_id}",
            dict,
            wrap_response=False,
        )

    def update(self, group_id: str, categories: dict) -> dict:
        """Update spend bucket distribution for a project budget group.

        Only the ``categories`` field may be updated via this method.
        Non-maintainer callers (project admins) may ONLY change categories;
        passing any other field will raise HTTP 403.

        Args:
            group_id: The budget group identifier
            categories: Mapping of category name to percentage, e.g.
                        ``{"platform": 60.0, "cli": 40.0}``

        Returns:
            Updated budget group data as dict
        """
        if not group_id:
            raise ValueError("group_id must be a non-empty string")
        if not categories:
            raise ValueError("categories must be a non-empty dict")
        payload = {"categories": {cat: {"pct": pct} for cat, pct in categories.items()}}
        return self._api.put(
            f"/v1/admin/project-budget-groups/{group_id}",
            dict,
            json_data=payload,
            wrap_response=False,
        )

    def _update_raw(self, group_id: str, body: dict) -> dict:
        """Update a project budget group with an arbitrary request body.

        Internal helper used by test utilities to verify field-level
        restrictions — pass any fields to check that non-allowed fields are
        rejected with HTTP 403.  Not part of the intended public API contract.

        Args:
            group_id: The budget group identifier
            body: Arbitrary JSON body for the PUT request

        Returns:
            Updated budget group data as dict
        """
        if not group_id:
            raise ValueError("group_id must be a non-empty string")
        return self._api.put(
            f"/v1/admin/project-budget-groups/{group_id}",
            dict,
            json_data=body,
            wrap_response=False,
        )

    def create(
        self,
        project_name: str,
        name: str,
        total_amount: float,
        budget_duration: str,
        categories: dict,
    ) -> dict:
        """Create a new project budget group.

        Args:
            project_name: The project this group belongs to.
            name: Human-readable name for the budget group.
            total_amount: Total budget amount (hard limit).
            budget_duration: Budget period, e.g. ``"30d"``.
            categories: Flat mapping of category name to percentage,
                        e.g. ``{"platform": 100.0}``.  Auto-wrapped to the
                        ``{"platform": {"pct": 100.0}}`` format the API expects.

        Returns:
            Created budget group data as dict (includes ``group_id`` UUID).
        """
        if not project_name:
            raise ValueError("project_name must be a non-empty string")
        if not categories:
            raise ValueError("categories must be a non-empty dict")
        payload = {
            "project_name": project_name,
            "name": name,
            "total_amount": total_amount,
            "budget_duration": budget_duration,
            "categories": {cat: {"pct": pct} for cat, pct in categories.items()},
        }
        return self._api.post(
            "/v1/admin/project-budget-groups",
            dict,
            json_data=payload,
            wrap_response=False,
        )

    def delete(self, group_id: str) -> None:
        """Delete a project budget group by its UUID.

        The server returns 204 No Content on success.

        Args:
            group_id: The UUID of the budget group to delete.
        """
        if not group_id:
            raise ValueError("group_id must be a non-empty string")
        self._api.delete(
            f"/v1/admin/project-budget-groups/{group_id}",
            dict,
            wrap_response=False,
        )
