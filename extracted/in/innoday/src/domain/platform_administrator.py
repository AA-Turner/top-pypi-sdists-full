"""
DEPRECATED: Platform Administrator domain model.

This module is deprecated and will be removed in a future version.
Platform administration functionality has been consolidated into the
Organization model with PLATFORM role.

See src/domain/organization.py and src/routers/platform.py for the new implementation.
"""

import warnings
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel

warnings.warn(
    "platform_administrator module is deprecated. Use Organization with PLATFORM role instead.",
    DeprecationWarning,
    stacklevel=2,
)


class PlatformAdministrator(SQLModel, table=True):
    """
    DEPRECATED: Platform Administrator information - singleton entity.

    This model is deprecated and replaced by Organization with PLATFORM role.
    It is kept for backward compatibility only and will be removed in v2.0.0.

    Migration path:
    1. Create a platform organization with PLATFORM role members
    2. Move platform administrator data to the platform organization
    3. Update all references to use the new platform API endpoints
    """

    __tablename__ = "platform_administrator"

    # Singleton pattern - only one record should exist
    id: int = Field(
        default=1, primary_key=True, description="Always 1 - singleton pattern"
    )

    # Company/Organization Information
    company_name: str = Field(
        max_length=200,
        description="Company or individual name providing InnoDay services",
    )
    display_name: Optional[str] = Field(
        default=None, max_length=100, description="Shorter display name for UI"
    )

    # Contact Information
    contact_person: Optional[str] = Field(
        default=None, max_length=100, description="Primary contact person name"
    )
    contact_email: str = Field(
        max_length=255, description="Primary contact email for platform support"
    )
    support_email: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Dedicated support email (if different)",
    )
    phone: Optional[str] = Field(
        default=None, max_length=50, description="Contact phone number"
    )

    # Online Presence
    website: Optional[str] = Field(
        default=None, max_length=500, description="Company website URL"
    )
    documentation_url: Optional[str] = Field(
        default=None, max_length=500, description="InnoDay documentation/help URL"
    )
    support_portal_url: Optional[str] = Field(
        default=None, max_length=500, description="Customer support portal URL"
    )

    # Business Information
    description: Optional[str] = Field(
        default=None, description="Description of services provided"
    )
    timezone: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Primary business timezone (e.g., 'America/New_York')",
    )
    business_hours: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Business hours description (e.g., '9 AM - 5 PM EST, Mon-Fri')",
    )

    # Development Services
    offers_development: bool = Field(
        default=True,
        description="Whether this administrator offers custom development work",
    )
    development_rate: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Development rate information (e.g., '$150/hour', 'Contact for quote')",
    )
    specializations: Optional[str] = Field(
        default=None, description="Areas of expertise and specialization"
    )

    # Platform Information
    platform_version: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Current InnoDay platform version being provided",
    )
    service_level: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Service level description (e.g., '24/7 support', 'Business hours only')",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When administrator info was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When administrator info was last updated",
    )

    def update_info(self, **kwargs) -> None:
        """Update administrator information and set updated timestamp"""
        warnings.warn(
            "PlatformAdministrator.update_info() is deprecated. Use Organization model instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":  # Don't allow ID updates
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)

    def get_display_name(self) -> str:
        """Get the best display name (display_name or company_name)"""
        return self.display_name or self.company_name

    def get_support_email(self) -> str:
        """Get the best support email (support_email or contact_email)"""
        return self.support_email or self.contact_email

    def has_development_services(self) -> bool:
        """Check if development services are offered"""
        return self.offers_development

    def __str__(self) -> str:
        """String representation of the platform administrator"""
        return f"Platform Administrator: {self.get_display_name()}"

    def __repr__(self) -> str:
        """Developer representation of the platform administrator"""
        return f"PlatformAdministrator(id={self.id}, company_name='{self.company_name}', contact_email='{self.contact_email}')"


# Singleton access functions
def get_platform_administrator_info() -> dict:
    """
    DEPRECATED: Get platform administrator information as a dictionary.

    This function is deprecated. Use the platform organization API instead:
    GET /api/v1/platform/info
    """
    warnings.warn(
        "get_platform_administrator_info() is deprecated. Use GET /api/v1/platform/info instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    return {
        "company_name": "InnoDay Platform Services",
        "contact_email": "admin@innoday.platform",
        "website": "https://innoday.platform",
        "offers_development": True,
        "service_level": "Business hours support",
        "_deprecated": True,
        "_migration_note": "Use GET /api/v1/platform/info for platform information",
    }
