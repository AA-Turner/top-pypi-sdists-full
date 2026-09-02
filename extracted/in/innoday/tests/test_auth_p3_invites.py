"""P3 auth: organization invites + self-registration (PF-350, #350).

Covers send/list/revoke authz, accept → membership creation (with invited_by),
email mismatch rejection, self-register opt-in gating, and the platform-user
short-circuits.
"""

from uuid import uuid4

from sqlmodel import Session

from src.domain.cli_token import CLIToken, generate_cli_token, hash_cli_token
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.organization_invite import (
    InviteStatus,
    OrganizationInvite,
    hash_invite_token,
)
from src.domain.user import User

# db_engine + client fixtures are provided by tests/conftest.py.


def _user_with_token(session, **kw) -> tuple[User, str]:
    user = User(
        id=str(uuid4()),
        email=kw.pop("email", f"{uuid4().hex[:8]}@example.com"),
        full_name=kw.pop("full_name", "U"),
        **kw,
    )
    session.add(user)
    raw = generate_cli_token()
    session.add(CLIToken(user_id=user.id, token_hash=hash_cli_token(raw)))
    session.commit()
    session.refresh(user)
    return user, raw


def _org(session, alias="acme", **kw) -> Organization:
    org = Organization(id=str(uuid4()), name=alias.title(), alias=alias, **kw)
    session.add(org)
    session.commit()
    session.refresh(org)
    return org


def _admin_membership(session, user_id, org_id, owner=False):
    session.add(
        OrganizationMembership(
            user_id=user_id,
            organization_id=org_id,
            role=OrganizationRole.ADMIN,
            is_owner=owner,
            is_active=True,
        )
    )
    session.commit()


class TestSendInvite:
    def test_admin_can_invite(self, client, db_engine):
        with Session(db_engine) as s:
            admin, token = _user_with_token(s, email="admin@acme.com")
            org = _org(s)
            _admin_membership(s, admin.id, org.id)
            org_id = org.id

        r = client.post(
            f"/api/v1/organizations/{org_id}/invites",
            json={"email": "new@acme.com", "role": "DEVELOPER"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["email"] == "new@acme.com"
        assert data["status"] == "PENDING"
        # dev convenience: accept_url present when Supabase email not configured
        assert data["accept_url"] and "token=" in data["accept_url"]

    def test_platform_user_can_invite_any_org_without_membership(
        self, client, db_engine
    ):
        with Session(db_engine) as s:
            plat, token = _user_with_token(
                s, email="staff@hs.com", is_platform_member=True
            )
            org = _org(s, alias="other")
            org_id = org.id  # platform user has NO membership row here

        r = client.post(
            f"/api/v1/organizations/{org_id}/invites",
            json={"email": "x@other.com"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200, r.text

    def test_plain_member_cannot_invite(self, client, db_engine):
        with Session(db_engine) as s:
            member, token = _user_with_token(s, email="m@acme.com")
            org = _org(s)
            s.add(
                OrganizationMembership(
                    user_id=member.id,
                    organization_id=org.id,
                    role=OrganizationRole.MEMBER,
                    is_active=True,
                )
            )
            s.commit()
            org_id = org.id

        r = client.post(
            f"/api/v1/organizations/{org_id}/invites",
            json={"email": "x@acme.com"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 403

    def test_reinvite_revokes_prior(self, client, db_engine):
        with Session(db_engine) as s:
            admin, token = _user_with_token(s, email="admin@acme.com")
            org = _org(s)
            _admin_membership(s, admin.id, org.id)
            org_id = org.id
        auth = {"Authorization": f"Bearer {token}"}
        client.post(
            f"/api/v1/organizations/{org_id}/invites",
            json={"email": "dup@acme.com"},
            headers=auth,
        )
        client.post(
            f"/api/v1/organizations/{org_id}/invites",
            json={"email": "dup@acme.com"},
            headers=auth,
        )
        listing = client.get(
            f"/api/v1/organizations/{org_id}/invites", headers=auth
        ).json()
        pending = [i for i in listing if i["status"] == "PENDING"]
        assert len(pending) == 1  # only the newest is live


class TestAcceptInvite:
    def _seed_invite(self, db_engine, invitee_email):
        with Session(db_engine) as s:
            admin, _ = _user_with_token(s, email="admin@acme.com")
            org = _org(s)
            _admin_membership(s, admin.id, org.id)
            raw_token = "rawtok-" + uuid4().hex
            inv = OrganizationInvite(
                organization_id=org.id,
                email=invitee_email,
                role=OrganizationRole.DEVELOPER,
                invited_by=admin.id,
                token_hash=hash_invite_token(raw_token),
            )
            s.add(inv)
            s.commit()
            return org.id, admin.id, raw_token

    def test_accept_creates_membership_with_invited_by(self, client, db_engine):
        org_id, admin_id, raw_token = self._seed_invite(db_engine, "invitee@acme.com")
        with Session(db_engine) as s:
            invitee, itoken = _user_with_token(s, email="invitee@acme.com")
            invitee_id = invitee.id

        r = client.post(
            f"/api/v1/invites/{raw_token}/accept",
            headers={"Authorization": f"Bearer {itoken}"},
        )
        assert r.status_code == 200, r.text
        assert r.json()["role"] == "DEVELOPER"

        with Session(db_engine) as s:
            m = s.exec(_select_membership(invitee_id, org_id)).first()
            assert m is not None
            assert m.invited_by == admin_id
            assert m.is_active is True
            # invitee is NOT a platform user
            u = s.get(User, invitee_id)
            assert u.is_platform_member is False
            assert u.default_organization_id == org_id
            # invite is ACCEPTED
            inv = s.exec(_select_invite_by_hash(hash_invite_token(raw_token))).first()
            assert inv.status == InviteStatus.ACCEPTED

    def test_email_mismatch_rejected(self, client, db_engine):
        _, _, raw_token = self._seed_invite(db_engine, "intended@acme.com")
        with Session(db_engine) as s:
            _, wrong_token = _user_with_token(s, email="someone-else@acme.com")

        r = client.post(
            f"/api/v1/invites/{raw_token}/accept",
            headers={"Authorization": f"Bearer {wrong_token}"},
        )
        assert r.status_code == 403

    def test_unknown_token(self, client, db_engine):
        with Session(db_engine) as s:
            _, token = _user_with_token(s)
        r = client.post(
            "/api/v1/invites/nope/accept",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 404

    def test_accept_marks_the_email_verified(self, client, db_engine):
        """#414: acceptance proves control of the invited address.

        The invite token reached them only by email, and the email match is
        already enforced. Without this, a CLI-token invitee would stay
        unverified forever and be locked out the moment
        REQUIRE_VERIFIED_EMAIL is switched on — the magic-link flow gets
        verified via the Supabase JWT path, but the CLI path never did.
        """
        _, _, raw_token = self._seed_invite(db_engine, "fresh@acme.com")
        with Session(db_engine) as s:
            invitee, itoken = _user_with_token(s, email="fresh@acme.com")
            invitee_id = invitee.id
            assert invitee.email_verified_at is None, "precondition: unverified"

        r = client.post(
            f"/api/v1/invites/{raw_token}/accept",
            headers={"Authorization": f"Bearer {itoken}"},
        )
        assert r.status_code == 200

        with Session(db_engine) as s:
            u = s.get(User, invitee_id)
            assert u.email_verified_at is not None
            assert u.email_verified is True

    def test_accept_does_not_reset_an_existing_verification_time(
        self, client, db_engine
    ):
        """Re-accepting must not move the original verification timestamp."""
        from datetime import datetime

        original = datetime(2026, 1, 1, 12, 0, 0)
        _, _, raw_token = self._seed_invite(db_engine, "already@acme.com")
        with Session(db_engine) as s:
            invitee, itoken = _user_with_token(s, email="already@acme.com")
            invitee.email_verified_at = original
            s.add(invitee)
            s.commit()
            invitee_id = invitee.id

        r = client.post(
            f"/api/v1/invites/{raw_token}/accept",
            headers={"Authorization": f"Bearer {itoken}"},
        )
        assert r.status_code == 200

        with Session(db_engine) as s:
            assert s.get(User, invitee_id).email_verified_at == original


class TestSelfRegister:
    def test_join_requires_opt_in(self, client, db_engine):
        with Session(db_engine) as s:
            user, token = _user_with_token(s)
            org = _org(s, allow_self_registration=False)
            org_id = org.id
        r = client.post(
            f"/api/v1/organizations/{org_id}/join",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 403

    def test_join_when_opted_in(self, client, db_engine):
        with Session(db_engine) as s:
            user, token = _user_with_token(s)
            org = _org(s, allow_self_registration=True)
            org_id, user_id = org.id, user.id
        r = client.post(
            f"/api/v1/organizations/{org_id}/join",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        with Session(db_engine) as s:
            m = s.exec(_select_membership(user_id, org_id)).first()
            assert m is not None and m.role == OrganizationRole.MEMBER

    def test_platform_user_join_is_noop_success(self, client, db_engine):
        with Session(db_engine) as s:
            user, token = _user_with_token(s, is_platform_member=True)
            org = _org(s, allow_self_registration=False)
            org_id, user_id = org.id, user.id
        r = client.post(
            f"/api/v1/organizations/{org_id}/join",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        with Session(db_engine) as s:
            # NO membership row created for a platform user
            m = s.exec(_select_membership(user_id, org_id)).first()
            assert m is None


class TestAcceptPage:
    def test_accept_page_renders(self, client):
        r = client.get("/invite/accept?token=abc123")
        assert r.status_code == 200
        assert "Accept" in r.text
        assert "abc123" in r.text


def _select_membership(user_id, org_id):
    from sqlmodel import select

    return select(OrganizationMembership).where(
        OrganizationMembership.user_id == user_id,
        OrganizationMembership.organization_id == org_id,
    )


def _select_invite_by_hash(token_hash):
    from sqlmodel import select

    return select(OrganizationInvite).where(OrganizationInvite.token_hash == token_hash)
