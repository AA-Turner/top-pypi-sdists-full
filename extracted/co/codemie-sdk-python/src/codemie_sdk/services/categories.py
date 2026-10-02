"""Category service implementation."""

from ..models.categories import (
    Category,
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse,
    CategoryListResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class CategoryService:
    """Service for managing CodeMie assistant categories."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the category service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_categories(self) -> list[Category]:
        """Get all available assistant categories (legacy, non-paginated).

        This endpoint maintains backward compatibility with existing clients.
        For paginated access with assistant counts, use list_categories().

        Returns:
            List of all categories
        """
        return self._api.get("/v1/assistants/categories", list[Category])

    def list_categories(
        self, page: int = 0, per_page: int = 10
    ) -> CategoryListResponse:
        """Get paginated list of categories with assistant counts.

        Returns counts separated by marketplace vs project assistants.
        This is the preferred endpoint for admin UI with pagination support.

        Args:
            page: Page number (0-indexed, default: 0)
            per_page: Number of items per page (1-100, default: 10)

        Returns:
            Paginated response with categories and metadata
        """
        params = {"page": page, "per_page": per_page}
        return self._api.get(
            "/v1/assistants/categories/list", CategoryListResponse, params=params
        )

    def get_category(self, category_id: str) -> CategoryResponse:
        """Get a specific category by ID with assistant counts.

        Args:
            category_id: Category ID (humanized, e.g., "migration_modernization")

        Returns:
            Category details with assistant counts

        Raises:
            NotFoundError: Category not found
        """
        return self._api.get(
            f"/v1/assistants/categories/{category_id}", CategoryResponse
        )

    def create_category(self, request: CategoryCreateRequest) -> CategoryResponse:
        """Create a new category. Admin access required.

        The category ID will be auto-generated from the name using humanization logic:
        - Special characters are removed
        - Spaces are replaced with underscores
        - All text is lowercased

        Example: "Migration & Modernization" → "migration_modernization"

        Args:
            request: Category creation request with name and description

        Returns:
            Created category with assistant counts (will be 0 for new categories)

        Raises:
            ApiError: Invalid request data or duplicate category ID (400)
            ApiError: User is not an admin (403)
        """
        return self._api.post(
            "/v1/assistants/categories",
            CategoryResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def update_category(
        self, category_id: str, request: CategoryUpdateRequest
    ) -> CategoryResponse:
        """Update an existing category. Admin access required.

        If assistants are assigned to this category, the operation will succeed
        but the response will include the count of affected assistants.
        The frontend should display a warning to the admin when editing categories
        with assigned assistants.

        Args:
            category_id: Category ID to update
            request: Category update request with new name and description

        Returns:
            Updated category with current assistant counts

        Raises:
            ApiError: User is not an admin (403)
            NotFoundError: Category not found (404)
        """
        return self._api.put(
            f"/v1/assistants/categories/{category_id}",
            CategoryResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def delete_category(self, category_id: str) -> dict:
        """Delete a category. Admin access required.

        This operation will fail with a 409 Conflict error if any assistants
        (marketplace or project) are assigned to this category.
        The admin must first remove all assistants from the category before deletion.

        Args:
            category_id: Category ID to delete

        Returns:
            Empty dict on successful deletion (204 No Content)

        Raises:
            ApiError: User is not an admin (403)
            NotFoundError: Category not found (404)
            ApiError: Category has assigned assistants and cannot be deleted (409)
        """
        return self._api.delete(f"/v1/assistants/categories/{category_id}", dict)
