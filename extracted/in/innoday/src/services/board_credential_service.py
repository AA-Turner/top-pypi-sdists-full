"""
Board Credential Service

Single Python-side entry point for the board_credentials Vault chokepoint
(get_board_credential / set_board_credential SQL functions -- see
alembic/versions/20260706_220000_add_board_credentials_vault.py and
20260707_041207_evolve_board_credentials_and_add_writer.py).

Also owns the conversion between the legacy colon-joined token string that
every existing call site (headers, env/orgs files, adapters) still speaks,
and the JSON payload Vault actually stores -- so callers can adopt Vault
without every adapter/service needing a simultaneous rewrite.
"""

import json
import logging
from typing import Any, Dict, Optional

from sqlalchemy import text
from sqlmodel import Session

from src.domain.board import BoardType

logger = logging.getLogger(__name__)

# BoardSyncService._get_adapter's discriminator for "this board's stored
# credential is OAuth (auth_type == 'oauth2'), don't try to reduce it to a
# legacy colon-joined string -- resolve a fresh (access_token, cloud_id) pair
# via ensure_fresh_jira_token instead." Keeps the OAuth/Basic-Auth branch
# entirely inside the Jira-specific code paths in board_sync_service.py and
# jira_oauth_service.py; Trello/Linear/Notion never see or check this.
OAUTH_TOKEN_SENTINEL = "__oauth2__"


def legacy_token_to_payload(board_type: BoardType, token: str) -> Dict[str, str]:
    """
    Convert an incoming X-Integration-Token string into the JSON payload
    shape Vault stores.

    Jira tokens arrive as "email:api_token" (Basic Auth); Trello as
    "api_key:token"; Linear/Notion/GitHub are a raw token with no split.
    Uses maxsplit=1 so a colon inside the second segment (the actual
    secret) is preserved, not mis-split -- verified this is lossless for
    round-tripping regardless of what characters appear in the token
    portion, since JSON string encoding handles arbitrary content.
    """
    if board_type == BoardType.JIRA:
        if ":" not in token:
            raise ValueError("Jira token must be 'email:api_token' format")
        email, api_token = token.split(":", 1)
        return {"email": email, "api_token": api_token}
    elif board_type == BoardType.TRELLO:
        if ":" not in token:
            raise ValueError("Trello token must be 'api_key:token' format")
        api_key, api_token = token.split(":", 1)
        return {"api_key": api_key, "token": api_token}
    else:
        # LINEAR, NOTION, and any future raw-token board type
        return {"token": token}


def payload_to_legacy_token(board_type: BoardType, payload: Dict[str, str]) -> str:
    """Inverse of legacy_token_to_payload -- reconstructs the colon-joined
    string every existing adapter/service call site still expects.

    A Jira payload with auth_type == "oauth2" has no email/api_token to
    reconstruct -- returns OAUTH_TOKEN_SENTINEL instead so callers can
    route to the OAuth refresh path (BoardSyncService._get_adapter) rather
    than crashing on a KeyError or silently building a bogus Basic Auth
    tuple from the wrong fields. Required OAuth fields are validated here
    (not left to whatever downstream reader hits them first, e.g.
    ensure_fresh_jira_token's own bare payload[...] lookups) so a malformed
    payload fails with a clear, specific KeyError message at the point of
    detection, matching this function's existing behavior for a malformed
    Basic Auth payload below.
    """
    if board_type == BoardType.JIRA and payload.get("auth_type") == "oauth2":
        required = ("access_token", "refresh_token", "cloud_id", "expires_at")
        missing = [field for field in required if field not in payload]
        if missing:
            raise KeyError(
                f"Jira OAuth payload is missing required field(s): {missing}"
            )
        return OAUTH_TOKEN_SENTINEL
    if board_type == BoardType.JIRA:
        return f"{payload['email']}:{payload['api_token']}"
    elif board_type == BoardType.TRELLO:
        return f"{payload['api_key']}:{payload['token']}"
    else:
        return payload["token"]


def get_board_credential_payload(
    session: Session, board_registration_id: str
) -> Optional[Dict[str, Any]]:
    """Fetch and decode the stored JSON payload for a board, or None if no
    credential has been stored for this board yet."""
    result = session.exec(
        text("SELECT get_board_credential(:board_registration_id)"),
        params={"board_registration_id": board_registration_id},
    ).first()

    raw = result[0] if result else None
    if raw is None:
        return None

    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        logger.error(
            f"Stored credential for board {board_registration_id} is not valid JSON"
        )
        return None


def set_board_credential(
    session: Session,
    board_registration_id: str,
    organization_id: str,
    board_type: BoardType,
    payload: Dict[str, str],
) -> None:
    """
    Store (or replace) the credential for a board. Create-or-update
    semantics are handled entirely inside the SQL function, keyed on the
    UniqueConstraint already enforcing one active credential row per board
    (uq_board_credential_per_board) -- calling this twice for the same
    board updates the existing Vault secret in place rather than
    duplicating it.
    """
    session.exec(
        text(
            "SELECT set_board_credential("
            ":board_registration_id, :organization_id, :board_type, :payload_json)"
        ),
        params={
            "board_registration_id": board_registration_id,
            "organization_id": organization_id,
            "board_type": (
                board_type.value if isinstance(board_type, BoardType) else board_type
            ),
            "payload_json": json.dumps(payload),
        },
    )
    session.commit()
    logger.info(
        "board_credential.written board_id=%s org_id=%s board_type=%s",
        board_registration_id,
        organization_id,
        board_type.value if isinstance(board_type, BoardType) else board_type,
    )
