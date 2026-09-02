"""P2 auth: CLI device flow (RFC 8628) endpoints (PF-350, #350).

Full round-trip: start → poll(pending) → approve → poll(token), plus the
error states (unknown code, denied, single-use consumption).
"""

from uuid import uuid4

from sqlmodel import Session

from src.domain.cli_token import CLIToken, generate_cli_token, hash_cli_token
from src.domain.device_authorization import (
    DeviceAuthorization,
    DeviceAuthStatus,
    generate_user_code,
)
from src.domain.user import User

# db_engine + client fixtures are provided by tests/conftest.py.

GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"


def _approver(db_engine):
    """A user + valid CLI token to authenticate the approval call."""
    with Session(db_engine) as s:
        user = User(id=str(uuid4()), email="approver@x.com", full_name="Approver")
        s.add(user)
        raw = generate_cli_token()
        s.add(CLIToken(user_id=user.id, token_hash=hash_cli_token(raw)))
        s.commit()
        return user.id, raw


class TestDeviceFlow:
    def test_full_roundtrip(self, client, db_engine):
        user_id, approver_token = _approver(db_engine)

        # 1. start
        start = client.post("/api/v1/device/code", json={})
        assert start.status_code == 200
        data = start.json()
        device_code = data["device_code"]
        user_code = data["user_code"]
        assert "-" in user_code
        assert data["verification_uri"].endswith("/device")
        assert data["interval"] >= 1

        # 2. poll before approval → authorization_pending
        poll = client.post(
            "/api/v1/device/token",
            json={"grant_type": GRANT_TYPE, "device_code": device_code},
        )
        assert poll.status_code == 400
        assert poll.json()["detail"]["error"] == "authorization_pending"

        # 3. approve (as the authenticated human)
        approve = client.post(
            "/api/v1/device/approve",
            json={"user_code": user_code, "approve": True},
            headers={"Authorization": f"Bearer {approver_token}"},
        )
        assert approve.status_code == 200
        assert approve.json()["status"] == "APPROVED"

        # 4. poll again → get the token
        poll2 = client.post(
            "/api/v1/device/token",
            json={"grant_type": GRANT_TYPE, "device_code": device_code},
        )
        assert poll2.status_code == 200
        body = poll2.json()
        # Device login mints an OAuth-kind token (ido_). This user has no
        # default org, so the org segment is the plat0 sentinel.
        assert body["access_token"].startswith("ido_plat0.")
        assert body["user"]["id"] == user_id

        # the minted token authenticates
        assert (
            client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {body['access_token']}"},
            ).status_code
            == 200
        )

        # 5. grant is single-use: a second poll no longer mints
        poll3 = client.post(
            "/api/v1/device/token",
            json={"grant_type": GRANT_TYPE, "device_code": device_code},
        )
        assert poll3.status_code == 400

    def test_unknown_device_code(self, client, db_engine):
        _approver(db_engine)
        r = client.post(
            "/api/v1/device/token",
            json={"grant_type": GRANT_TYPE, "device_code": "does-not-exist"},
        )
        assert r.status_code == 400
        assert r.json()["detail"]["error"] == "invalid_grant"

    def test_denied_flow(self, client, db_engine):
        _, approver_token = _approver(db_engine)
        start = client.post("/api/v1/device/code", json={}).json()
        client.post(
            "/api/v1/device/approve",
            json={"user_code": start["user_code"], "approve": False},
            headers={"Authorization": f"Bearer {approver_token}"},
        )
        poll = client.post(
            "/api/v1/device/token",
            json={"grant_type": GRANT_TYPE, "device_code": start["device_code"]},
        )
        assert poll.status_code == 400
        assert poll.json()["detail"]["error"] == "access_denied"

    def test_approve_requires_auth(self, client, db_engine):
        start = client.post("/api/v1/device/code", json={}).json()
        # no Authorization header
        r = client.post(
            "/api/v1/device/approve",
            json={"user_code": start["user_code"], "approve": True},
        )
        assert r.status_code == 401

    def test_approve_unknown_code(self, client, db_engine):
        _, approver_token = _approver(db_engine)
        r = client.post(
            "/api/v1/device/approve",
            json={"user_code": generate_user_code(), "approve": True},
            headers={"Authorization": f"Bearer {approver_token}"},
        )
        assert r.status_code == 404

    def test_verification_page_renders(self, client):
        r = client.get("/device?user_code=ABCD-EFGH")
        assert r.status_code == 200
        assert "ABCD-EFGH" in r.text
        assert "Authorize" in r.text


class TestDeviceModel:
    def test_user_code_format(self):
        code = generate_user_code()
        assert len(code) == 9 and code[4] == "-"

    def test_approve_sets_user_and_status(self):
        g = DeviceAuthorization(device_code_hash="h", user_code="AAAA-BBBB")
        g.approve("user-1")
        assert g.status == DeviceAuthStatus.APPROVED
        assert g.user_id == "user-1"
