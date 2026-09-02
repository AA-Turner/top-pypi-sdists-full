"""One place that turns a BoardRegistration + credential into a board adapter.

Before this, the same BoardType→client→adapter switch existed **three** times
(`BoardSyncService`, `BoardTicketCreationService`, and a dead third copy in
`BoardSyncService._get_api_client` that had no callers at all). They had drifted,
and the drift was user-visible:

| | sync | ticket creation (before) |
|---|---|---|
| OAuth Jira | supported | **raised "not supported yet"** |
| Notion | supported | **raised "Unsupported board type"** |
| Jira with no `board_url` | raises, clearly | built `JiraAPI(base_url=None)` |

So a board connected through Jira OAuth could be *synced* but tickets could not be
*created* on it — the error message even said to "extend this service's
`_get_adapter` to mirror BoardSyncService's". This module is that mirror, once.

The union of the correct behaviours wins: OAuth Jira and Notion are available to
every caller, and a missing `board_url` fails loudly rather than deferring to a
confusing failure inside JiraAPI.
"""

import logging
import re
from typing import Optional

from sqlmodel import Session

from src.adapters import (
    BaseBoardAdapter,
    BoardCredentialError,
    JiraBoardAdapter,
    LinearBoardAdapter,
    NotionBoardAdapter,
    TrelloBoardAdapter,
)
from src.api.jira_api import JiraAPI
from src.api.linear_api import LinearAPI
from src.api.notion_api import NotionAPI
from src.api.trello_api import TrelloAPI
from src.domain import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.services.board_credential_service import (
    OAUTH_TOKEN_SENTINEL,
    get_board_credential_payload,
    payload_to_legacy_token,
)
from src.services.jira_oauth_service import ensure_fresh_jira_token

logger = logging.getLogger(__name__)


def is_oauth_jira(registration: BoardRegistration, token: str) -> bool:
    """Whether this is a Jira board whose stored credential is OAuth.

    Callers need this to decide caching: an OAuth-mode adapter must **never** be
    cached. Every OAuth board would otherwise share one entry keyed on the same
    sentinel, and ``JiraBoardAdapter._refresh_api_auth_if_oauth`` mutates its
    JiraAPI's base_url/headers in place on each call — safe only while the adapter
    isn't shared concurrently.
    """
    return registration.board_type == BoardType.JIRA and token == OAUTH_TOKEN_SENTINEL


def _jira_base_url(registration: BoardRegistration) -> str:
    """Scheme+host from the board URL. Required — there is no sensible default."""
    if not registration.board_url:
        raise ValueError(
            "board_url is required for Jira integration — "
            "set it on the BoardRegistration"
        )
    match = re.match(r"(https?://[^/]+)", registration.board_url)
    if not match:
        raise ValueError(
            f"Cannot extract base URL from board_url: {registration.board_url}"
        )
    return match.group(1)


async def build_board_adapter(
    registration: BoardRegistration,
    token: str,
    session: Session,
) -> BaseBoardAdapter:
    """Build the adapter for ``registration``, authenticating with ``token``.

    ``token`` is the whole credential: there is no second store to consult. A
    ``legacy_credentials`` keyword used to accept a ``~/.innoday``/OS-keyring
    lookup, passed only by the ticket-creation path for boards registered before
    Vault wiring existed. Removed in #525 phase 3 — board sync never passed one,
    so dropping it leaves sync's behaviour byte-for-byte identical and makes
    ticket creation resolve credentials the same single way.

    Args:
        registration: the board.
        token: resolved credential — colon-joined legacy string, a plain API key,
            or ``OAUTH_TOKEN_SENTINEL`` for an OAuth-credentialed Jira board.
        session: used only to mint the initial OAuth access_token/cloud_id pair
            for Jira. Not retained: the resulting adapter refreshes its own token
            via ``JiraBoardAdapter._jira_request_context``, opening its own
            session as needed.

    Raises:
        ValueError: unsupported board type, or an unusable Jira credential.
    """
    if registration.board_type == BoardType.TRELLO:
        if ":" in token:
            api_key, api_token = token.split(":", 1)
        else:
            api_key = api_token = token
        return TrelloBoardAdapter(TrelloAPI(api_key, api_token), registration)

    if registration.board_type == BoardType.JIRA:
        base_url = _jira_base_url(registration)

        if token == OAUTH_TOKEN_SENTINEL:
            # JiraAPI's access_token/cloud_id path sets self.auth = None, which
            # is what JiraBoardAdapter._is_oauth_mode() checks to keep refreshing
            # on every later call instead of trusting what's baked in here.
            access_token, cloud_id = await ensure_fresh_jira_token(
                session, registration.id
            )
            api = JiraAPI(
                base_url=base_url,
                access_token=access_token,
                cloud_id=cloud_id,
            )
            return JiraBoardAdapter(api, registration)

        if ":" not in token:
            raise ValueError("Invalid Jira token format. Expected email:api_token")
        email, api_token = token.split(":", 1)

        api = JiraAPI(
            base_url=base_url,
            email=email,
            api_token=api_token,
        )
        return JiraBoardAdapter(api, registration)

    if registration.board_type == BoardType.NOTION:
        # Notion uses a plain integration token (conventionally `secret_…`).
        return NotionBoardAdapter(NotionAPI(integration_token=token), registration)

    if registration.board_type == BoardType.LINEAR:
        return LinearBoardAdapter(LinearAPI(api_key=token), registration)

    raise ValueError(f"Unsupported board type: {registration.board_type}")


def resolve_board_token(
    session: Session,
    registration: BoardRegistration,
    org: Optional[Organization],
    token: Optional[str] = None,
) -> str:
    """A board's credential: caller-supplied → Vault. Nothing else.

    **Here rather than on a service, for the same reason `build_board_adapter`
    is.** This module is already the one place a `BoardRegistration` becomes
    something that can talk to a board; the credential is the other half of that
    and was living as a private method on `BoardTicketCreationService`, which
    until now was the only live caller of the outbound path. A second caller --
    `ticket_status_service` -- would otherwise have made a second private copy of
    the chain, and a drifted second copy of exactly this chain is the bug #525
    phase 3 was written to close: creating a ticket on a board resolved its
    credential differently from syncing it, and only one of the two could work on
    a deployed server.

    A caller-supplied token (the ``X-Integration-Token`` header) still wins, which
    is deliberate: it is the documented way to run a one-off operation with a
    different credential.

    There used to be a third step -- a per-board-type ``CredentialProvider``
    lookup in ``~/.innoday/config.json`` plus the OS keyring, for boards
    registered before Vault wiring existed. It is gone (#525 phase 3). A deployed
    server has neither store.

    ``org`` is taken, and may be None, because the error path names it: without a
    tenant an operator gets a board id and nowhere to look it up. A missing org is
    an orphaned board, which is a real state -- dereferencing it unguarded is how
    this raised ``AttributeError`` → 500 instead of a clear error.

    Raises:
        BoardCredentialError: no credential stored. A `ValueError` as it always
            was, so existing callers are unchanged, **and** a `BoardAdapterError`
            so the display path can recognise it by class. Written **to be read**
            -- it names the board and the one store that fixes it -- which is why
            callers pass its message through rather than replacing it with a
            generic one.
    """
    if token:
        return token

    payload = get_board_credential_payload(session, registration.id)
    if payload:
        try:
            return payload_to_legacy_token(registration.board_type, payload)
        except KeyError:
            logger.error(
                f"Stored credential for board {registration.id} is missing "
                f"expected fields for board_type {registration.board_type}"
            )

    # Name the store, not just the failure: this has exactly one remedy.
    where = getattr(org, "alias", None) or "unknown"
    raise BoardCredentialError(
        f"No credential stored for {registration.board_type.value} board "
        f"{registration.id} (organization {where}) — store one in "
        "board_credentials (innoday board set-credential), or pass a "
        "one-off token in the X-Integration-Token header"
    )
