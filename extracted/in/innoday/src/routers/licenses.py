"""
License management API endpoints.

This module provides RESTful endpoints for managing organization licenses,
license tiers, and usage tracking.

ARCHITECTURE NOTES:
==================
- All license operations follow RESTful conventions
- License validation happens at the API layer
- Usage tracking is real-time and atomic
- All license changes are audited automatically
- Organizations can only manage their own licenses
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from src.database import get_session
from src.domain.license import LicenseTier

router = APIRouter(tags=["licenses"])


# Public License Information Models
class LicenseInfoResponse(BaseModel):
    """Public license information response"""

    open_source_license: str = "AGPL-3.0-or-later"
    open_source_license_url: str = "https://www.gnu.org/licenses/agpl-3.0.html"
    source_code_url: str = "https://github.com/havilandsoftware/innoday"
    commercial_license_available: bool = True
    commercial_contact: str = "sales@havilandsoftware.com"
    commercial_license_url: str = (
        "https://github.com/havilandsoftware/innoday/blob/main/LICENSE.commercial"
    )
    cla_required: bool = True
    cla_url: str = "https://github.com/havilandsoftware/innoday/blob/main/CLA.md"
    legal_notice: str = (
        "Use of this software implies acceptance of the AGPL-3.0 license "
        "unless a commercial license has been purchased. Network use constitutes distribution."
    )


class LicenseTierResponse(BaseModel):
    """License tier information"""

    id: str
    name: str
    display_name: str
    max_users: Optional[int] = Field(
        None, description="Max users allowed (null = unlimited)"
    )
    max_boards: Optional[int] = Field(
        None, description="Max boards allowed (null = unlimited)"
    )
    daily_ticket_limit: Optional[int] = Field(
        None, description="Daily ticket limit per user (null = unlimited)"
    )
    api_rate_limit: Optional[int] = Field(
        None, description="API rate limit per hour (null = unlimited)"
    )
    sync_interval_minutes: int = Field(
        0, description="Sync interval in minutes (0 = real-time)"
    )
    features: Dict[str, Any] = Field(
        default_factory=dict, description="Additional features"
    )


# Public License Information
@router.get("/license-info", response_model=LicenseInfoResponse)
async def get_license_info():
    """
    Get open source license information and commercial licensing options.

    This endpoint provides information about the AGPL-3.0 open source license
    and available commercial licensing options for organizations that cannot
    comply with AGPL-3.0 requirements.
    """
    return LicenseInfoResponse()


# License Tier Management
@router.get("/tiers", response_model=List[LicenseTierResponse])
async def get_license_tiers(session: Session = Depends(get_session)):
    """
    Get all available license tiers.

    Returns a list of all license tiers available in the system,
    including their limits and features.
    """
    statement = select(LicenseTier)
    tiers = session.exec(statement).all()
    return [
        LicenseTierResponse(
            id=tier.id,
            name=tier.name,
            display_name=tier.display_name,
            max_users=tier.max_users,
            max_boards=tier.max_boards,
            daily_ticket_limit=tier.daily_ticket_limit,
            api_rate_limit=tier.api_rate_limit,
            sync_interval_minutes=tier.sync_interval_minutes,
            features=tier.features,
        )
        for tier in tiers
    ]


@router.get("/tiers/{tier_name}", response_model=LicenseTierResponse)
async def get_license_tier(tier_name: str, session: Session = Depends(get_session)):
    """
    Get a specific license tier by name.

    Args:
        tier_name: Name of the license tier (e.g., 'guidance', 'spark', 'sprint', 'velocity')

    Returns:
        Detailed information about the specified license tier.

    Raises:
        404: If the specified tier does not exist
    """
    # Backwards-compatibility aliases for old tier names.
    TIER_ALIASES = {"pro": "spark", "max": "sprint", "unlimited": "velocity"}
    tier_name = TIER_ALIASES.get(tier_name, tier_name)

    statement = select(LicenseTier).where(LicenseTier.name == tier_name)
    tier = session.exec(statement).first()

    if not tier:
        raise HTTPException(
            status_code=404, detail=f"License tier '{tier_name}' not found"
        )

    return LicenseTierResponse(
        id=tier.id,
        name=tier.name,
        display_name=tier.display_name,
        max_users=tier.max_users,
        max_boards=tier.max_boards,
        daily_ticket_limit=tier.daily_ticket_limit,
        api_rate_limit=tier.api_rate_limit,
        sync_interval_minutes=tier.sync_interval_minutes,
        features=tier.features,
    )


# Note: All client-based license endpoints have been removed.
# Use organization-based endpoints for license management:
# - GET /api/v1/organizations/{organization_id}/license
# - PUT /api/v1/organizations/{organization_id}/license
# - GET /api/v1/organizations/{organization_id}/usage
