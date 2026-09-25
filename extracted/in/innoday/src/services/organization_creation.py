"""Create an organization with its owner -- the one implementation.

Shared by `POST /api/v1/organizations` and the operator script
`scripts/bootstrap_cli.py create-org`, so the two cannot drift on alias rules,
the owner membership or the default licence (PF-457). Moved here verbatim from
the router.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlmodel import Session, select

from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.user import User
from src.utils.license_utils import ensure_top_tier_license


class AliasTaken(Exception):
    """The requested alias belongs to another organization."""


def create_organization(
    session: Session,
    *,
    owner: User,
    name: str,
    alias: Optional[str] = None,
    **fields,
) -> Organization:
    """Create the org, make `owner` its ADMIN owner, give it a licence.

    `alias` must be free, else `AliasTaken`; omitted, one is derived from the
    name with a numeric suffix until it is. `fields` are the remaining
    `Organization` columns (description, website, ...).
    """
    if alias:
        if session.exec(
            select(Organization).where(Organization.alias == alias)
        ).first():
            raise AliasTaken(alias)
    else:
        base_alias = Organization.generate_alias(name)
        alias, counter = base_alias, 1
        while session.exec(
            select(Organization).where(Organization.alias == alias)
        ).first():
            alias = f"{base_alias}-{counter}"
            counter += 1

    now = datetime.now(timezone.utc)
    org = Organization(
        id=str(uuid4()),
        name=name,
        alias=alias,
        **fields,
        settings={},
        created_at=now,
        updated_at=now,
    )
    session.add(org)
    session.add(
        OrganizationMembership(
            id=str(uuid4()),
            organization_id=org.id,
            user_id=owner.id,
            role=OrganizationRole.ADMIN,
            is_owner=True,
            is_active=True,
            joined_at=now,
            updated_at=now,
        )
    )
    session.commit()
    session.refresh(org)

    # Every organization gets an active license by default (top tier for now --
    # see ensure_top_tier_license). Without this, ticket/board/user creation
    # 402s immediately for a brand-new org.
    ensure_top_tier_license(org.id, session)
    # ensure_top_tier_license commits, which expires session-loaded objects.
    session.refresh(org)
    return org
