"""Creating an organization is one operation, shared by the API route and the
operator script (`scripts/bootstrap_cli.py create-org`) so they cannot drift
(PF-457)."""

from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.license import LicenseTier
from src.domain.organization import Organization, OrganizationMembership
from src.domain.user import User
from src.services.organization_creation import AliasTaken, create_organization
from src.utils.license_utils import TOP_LICENSE_TIER_NAME


def _user(session) -> User:
    """An owner, plus the licence tier every new org is given."""
    session.add(
        LicenseTier(id=str(uuid4()), name=TOP_LICENSE_TIER_NAME, display_name="Top")
    )
    user = User(email="owner@example.com", full_name="Owner")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_creates_the_org_with_its_owner_and_a_licence(db_engine):
    with Session(db_engine) as session:
        owner = _user(session)
        org = create_organization(session, owner=owner, name="Acme Corp", alias="acme")

        assert org.alias == "acme"
        membership = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == org.id
            )
        ).one()
        assert membership.user_id == owner.id and membership.is_owner

        from src.utils.license_utils import is_license_active

        assert is_license_active(org.id, session)


def test_derives_a_free_alias_when_none_is_given(db_engine):
    with Session(db_engine) as session:
        owner = _user(session)
        first = create_organization(session, owner=owner, name="Acme Corp")
        second = create_organization(session, owner=owner, name="Acme Corp")

        assert first.alias != second.alias
        assert len(session.exec(select(Organization)).all()) == 2


def test_refuses_a_taken_alias(db_engine):
    with Session(db_engine) as session:
        owner = _user(session)
        create_organization(session, owner=owner, name="Acme", alias="acme")
        with pytest.raises(AliasTaken):
            create_organization(session, owner=owner, name="Other", alias="acme")
