"""Models for category-related data structures."""

from pydantic import BaseModel, Field, ConfigDict


class Category(BaseModel):
    """Model for assistant category."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Category display name")
    description: str | None = Field(None, description="Category description")


class CategoryCreateRequest(BaseModel):
    """Model for creating a new category."""

    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., description="Category name")
    description: str | None = Field(None, description="Category description")


class CategoryUpdateRequest(BaseModel):
    """Model for updating an existing category."""

    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., description="Category name")
    description: str | None = Field(None, description="Category description")


class CategoryResponse(BaseModel):
    """Model for category response with assistant counts."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    description: str | None = Field(None, description="Category description")
    marketplace_count: int = Field(
        default=0, description="Number of marketplace assistants in this category"
    )
    project_count: int = Field(
        default=0, description="Number of project assistants in this category"
    )


class CategoryListMetadata(BaseModel):
    """Metadata for paginated category list response."""

    model_config = ConfigDict(extra="ignore")

    page: int = Field(..., description="Current page number (0-indexed)")
    per_page: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of categories")
    total_pages: int = Field(..., description="Total number of pages")


class CategoryListResponse(BaseModel):
    """Model for paginated category list response."""

    model_config = ConfigDict(extra="ignore")

    items: list[CategoryResponse] = Field(
        default_factory=list, description="List of categories with counts"
    )
    metadata: CategoryListMetadata = Field(..., description="Pagination metadata")
