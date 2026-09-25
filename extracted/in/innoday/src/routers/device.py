"""CLI device-flow endpoints (auth P2, PF-350, RFC 8628).

The machinery behind ``innoday login``:

  POST /api/v1/device/code     -- CLI starts the flow, gets device_code + user_code
  POST /api/v1/device/token    -- CLI polls; on approval receives an innoday_ token
  POST /api/v1/device/approve  -- the verification page approves a user_code  [authed]
  GET  /ui/device              -- the Pixelfuel-branded hosted approval page

Standard RFC 8628 polling responses (``authorization_pending`` / ``slow_down`` /
``expired_token`` / ``access_denied``) are returned to the CLI as 400s with an
``error`` field, matching the spec so a conventional device-flow client works.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select, update

from src.database import get_session
from src.domain.device_authorization import (
    DEFAULT_POLL_INTERVAL_SECONDS,
    DeviceAuthorization,
    DeviceAuthStatus,
    generate_device_code,
    generate_user_code,
    hash_device_code,
)
from src.domain.user import User
from src.middleware.rbac import get_current_user
from src.page_paths import DEVICE_PATH, app_url
from src.routers.auth import default_org_alias, mint_cli_token

router = APIRouter(tags=["device-auth"])

DEVICE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"


class DeviceCodeRequest(BaseModel):
    client_id: str = "innoday-cli"
    scope: str = "cli"


class DeviceCodeResponse(BaseModel):
    device_code: str  # raw; CLI keeps it in memory to poll
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


class DeviceTokenRequest(BaseModel):
    grant_type: str = DEVICE_GRANT_TYPE
    device_code: str


class DeviceApproveRequest(BaseModel):
    user_code: str
    approve: bool = True


@router.post("/api/v1/device/code", response_model=DeviceCodeResponse)
async def start_device_flow(
    request: DeviceCodeRequest,
    session: Session = Depends(get_session),
):
    """Begin the device flow. Returns the codes and polling parameters."""
    raw_device_code = generate_device_code()
    # Regenerate user_code on the rare collision with a live grant.
    for _ in range(5):
        user_code = generate_user_code()
        existing = session.exec(
            select(DeviceAuthorization).where(
                DeviceAuthorization.user_code == user_code,
                DeviceAuthorization.status == DeviceAuthStatus.PENDING,
            )
        ).first()
        if not existing:
            break

    grant = DeviceAuthorization(
        device_code_hash=hash_device_code(raw_device_code),
        user_code=user_code,
        interval_seconds=DEFAULT_POLL_INTERVAL_SECONDS,
    )
    session.add(grant)
    session.commit()
    session.refresh(grant)

    verification_uri = f"{app_url()}{DEVICE_PATH}"
    exp = grant.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    expires_in = max(0, int((exp - datetime.now(timezone.utc)).total_seconds()))

    return DeviceCodeResponse(
        device_code=raw_device_code,
        user_code=user_code,
        verification_uri=verification_uri,
        verification_uri_complete=f"{verification_uri}?user_code={user_code}",
        expires_in=expires_in,
        interval=grant.interval_seconds,
    )


@router.post("/api/v1/device/token")
async def poll_device_token(
    request: DeviceTokenRequest,
    session: Session = Depends(get_session),
):
    """CLI polls here. Returns the token once the grant is approved.

    Uses RFC 8628 error codes so a standard device-flow client understands the
    pending/denied/expired states.
    """
    if request.grant_type != DEVICE_GRANT_TYPE:
        raise HTTPException(status_code=400, detail={"error": "unsupported_grant_type"})

    grant = session.exec(
        select(DeviceAuthorization).where(
            DeviceAuthorization.device_code_hash
            == hash_device_code(request.device_code)
        )
    ).first()

    if not grant:
        raise HTTPException(status_code=400, detail={"error": "invalid_grant"})

    if grant.is_expired() and grant.status == DeviceAuthStatus.PENDING:
        grant.status = DeviceAuthStatus.EXPIRED
        session.add(grant)
        session.commit()
        raise HTTPException(status_code=400, detail={"error": "expired_token"})

    if grant.status == DeviceAuthStatus.PENDING:
        raise HTTPException(status_code=400, detail={"error": "authorization_pending"})
    if grant.status == DeviceAuthStatus.DENIED:
        raise HTTPException(status_code=400, detail={"error": "access_denied"})
    if grant.status == DeviceAuthStatus.EXPIRED:
        raise HTTPException(status_code=400, detail={"error": "expired_token"})

    # APPROVED — consume the grant ATOMICALLY before minting, so two concurrent
    # polls can't both mint a token. The conditional UPDATE flips APPROVED→EXPIRED
    # only if it's still APPROVED; exactly one racer's UPDATE matches a row.
    if not grant.user_id:
        raise HTTPException(status_code=400, detail={"error": "invalid_grant"})

    result = session.execute(
        update(DeviceAuthorization)
        .where(
            DeviceAuthorization.id == grant.id,
            DeviceAuthorization.status == DeviceAuthStatus.APPROVED,
        )
        .values(status=DeviceAuthStatus.EXPIRED)
    )
    session.commit()
    if result.rowcount != 1:
        # Another poll already consumed this grant — don't mint a second token.
        raise HTTPException(status_code=400, detail={"error": "expired_token"})

    user = session.get(User, grant.user_id)
    token_row, raw_token = mint_cli_token(
        session,
        user_id=grant.user_id,
        name="cli (device login)",
        kind="oauth",
        org_alias=default_org_alias(session, user) if user else None,
    )

    return {
        "access_token": raw_token,
        "token_type": "Bearer",
        "token_id": token_row.id,
        "user": (
            {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_platform_member": user.is_platform_member,
            }
            if user
            else None
        ),
    }


@router.post("/api/v1/device/approve")
async def approve_device(
    request: DeviceApproveRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Approve (or deny) a device grant by user_code. Called by the verification
    page, which carries the approving human's authenticated session."""
    grant = session.exec(
        select(DeviceAuthorization).where(
            DeviceAuthorization.user_code == request.user_code.upper(),
            DeviceAuthorization.status == DeviceAuthStatus.PENDING,
        )
    ).first()

    if not grant:
        raise HTTPException(
            status_code=404, detail="No pending device request for that code"
        )
    if grant.is_expired():
        grant.status = DeviceAuthStatus.EXPIRED
        session.add(grant)
        session.commit()
        raise HTTPException(status_code=400, detail="Device code expired")

    if request.approve:
        grant.approve(current_user.id)
        message = "Device approved. Return to your terminal."
    else:
        grant.deny()
        message = "Device request denied."

    session.add(grant)
    session.commit()
    return {"status": grant.status.value, "message": message}
