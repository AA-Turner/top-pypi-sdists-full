"""Propagate the caller's identity to Postgres so RLS policies can evaluate.

The policies live in ``alembic/versions/20260805_130000_rls_tenant_isolation.py``
and are scoped ``TO innoday_app``. They read the caller from a transaction-local
GUC::

    SELECT set_config('innoday.user_id', '<uuid>', true);   -- true = LOCAL
    SET LOCAL ROLE innoday_app;

Both statements are deliberately transaction-local. Dev connects through
Supabase's **transaction-mode** pooler (port 6543), which returns the connection
to the pool at transaction end; a session-level ``SET`` would hand the previous
request's tenant to the next caller, which is a cross-tenant read -- worse than
the gap it closes.

Being transaction-local creates the opposite problem, which is why this module
uses an event listener rather than a single call: authentication itself commits
(``token_auth._user_from_cli_token`` writes ``last_used_at``), and any later
``commit()`` ends the transaction the claim was attached to. A one-shot
``SET LOCAL`` would therefore stop applying part-way through a request and
enforcement would **fail open** -- silently, because queries keep working, just
unrestricted. Re-applying on ``after_begin`` binds the claim to the *session* and
lets Postgres scope it to whichever transaction is current.

Disabled unless ``INNODAY_RLS_ENFORCE`` is truthy. RLS is a backstop here, not
the control -- ``Depends(require_org_role())`` is the control, because RLS filters
rows and cannot authorise an action that touches no row (board sync calling Jira,
container execution, AI spend), and because a policy denial yields ``0 rows`` or
a database error rather than the ``403`` the CLI and tests expect.
"""

from __future__ import annotations

import logging
import os

from sqlalchemy import event
from sqlmodel import Session

logger = logging.getLogger(__name__)

APP_ROLE = "innoday_app"
CLAIM = "innoday.user_id"

# Key under which the claim is stashed on `Session.info`.
_SESSION_KEY = "_innoday_rls_user_id"

_TRUTHY = {"1", "true", "yes", "on"}


def rls_enforced() -> bool:
    """Whether to switch into the restricted role. Off unless explicitly enabled."""
    return os.getenv("INNODAY_RLS_ENFORCE", "").strip().lower() in _TRUTHY


def _apply(connection, user_id: str) -> None:
    """Set the claim and enter the restricted role for the current transaction."""
    connection.exec_driver_sql(f"SELECT set_config('{CLAIM}', %s, true)", (user_id,))
    # A literal, never caller-controlled -- no injection surface.
    connection.exec_driver_sql(f"SET LOCAL ROLE {APP_ROLE}")


def enforce_for_user(session: Session, user_id: str) -> None:
    """Bind `user_id` to `session` so every transaction on it is tenant-scoped.

    Call once, immediately after the caller has been authenticated. A no-op when
    ``INNODAY_RLS_ENFORCE`` is unset, on non-Postgres backends, or if the role is
    absent (a database that has not run the policy migration yet) -- in the last
    two cases the app keeps working with the app-layer check as its only control,
    which is the status quo rather than a regression.
    """
    if not user_id or not rls_enforced():
        return
    bind = session.get_bind()
    if bind is None or bind.dialect.name != "postgresql":
        return

    session.info[_SESSION_KEY] = user_id
    try:
        _apply(session.connection(), user_id)
    except Exception:  # pragma: no cover - defensive
        session.info.pop(_SESSION_KEY, None)
        session.rollback()
        logger.warning(
            "could not enter %s; continuing without RLS enforcement for this "
            "request (the app-layer membership check still applies)",
            APP_ROLE,
            exc_info=True,
        )


@event.listens_for(Session, "after_begin")
def _reapply_claim(session, transaction, connection) -> None:
    """Re-apply the claim whenever a new transaction starts on a bound session.

    Without this, the first ``commit()`` after ``enforce_for_user`` would drop
    both the claim and the role, and the rest of the request would run
    unrestricted.
    """
    user_id = session.info.get(_SESSION_KEY)
    if not user_id or connection.dialect.name != "postgresql":
        return
    try:
        _apply(connection, user_id)
    except Exception:  # pragma: no cover - defensive
        logger.warning("failed to re-apply RLS claim after begin", exc_info=True)
