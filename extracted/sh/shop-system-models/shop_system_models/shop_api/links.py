import re
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

from shop_system_models.shop_api import MetaBaseModel

# Schemes valid in href (http, https, mailto, tel, and other URI schemes)
ALLOWED_LINK_SCHEMES = frozenset({"http", "https", "mailto", "tel"})
SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*$")


def _is_valid_href(value: str) -> bool:
    s = value.strip()
    if not s or ":" not in s:
        return False
    scheme, _ = s.split(":", 1)
    return scheme.lower() in ALLOWED_LINK_SCHEMES or bool(SCHEME_PATTERN.match(scheme))


class ServiceLink(MetaBaseModel):
    """Model representing a link to another service."""

    service_name: str
    url: HttpUrl
    resource_id: str
    link_metadata: Optional[Dict[str, Any]] = Field(default_factory=lambda: {})


class ServiceLinkResponse(MetaBaseModel):
    """Response model for service link operations."""

    link_id: str
    service_name: str
    resource_id: str
    success: bool = True
    error: Optional[str] = None


class LinkBlocksModel(BaseModel):
    contacts: str | None = "https://teletype.in/@tg-shops/09hOkoJjizN"  # Teletype link
    info: str | None = "https://teletype.in/@tg-shops/2vZa_0ykcCF"  # Teletype link

    @field_validator("contacts", "info", mode="before")
    def link_validation(cls, value):
        if not value:
            return value
        s = value.strip() if isinstance(value, str) else value
        if not s:
            return value
        return s if _is_valid_href(str(s)) else ""
