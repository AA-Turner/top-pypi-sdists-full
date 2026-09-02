"""
Org Credential Service

Single Python-side entry point for the org_credentials Vault chokepoint
(get_org_credential / set_org_credential SQL functions -- see the FUNCTIONS
tuple in alembic/versions/20260807_140400_security_baseline.py, revision
``aaaa0001security``, which is where both function bodies now live. The
migration this docstring used to cite,
``20260803_190000_add_org_credential_vault_functions.py``, no longer exists:
PF-399 squashed 87 migrations into 4 and the functions were carried into the
security baseline).

This is the server-side source of truth for organization-scoped integration
credentials (GitHub today). It replaces CredentialProvider for server code:
that class reads ~/.innoday/config.json plus the local OS keyring, neither of
which exists on the deployed server, so every server-side GitHub call used to
fail with "No GitHub connection found for organization".

The payload is JSON so an integration can carry more than a bare token --
GitHub needs {"token": ..., "github_org": ...}. The plaintext exists only as
ciphertext in vault.secrets and transiently in vault.decrypted_secrets at read
time; it is never stored on org_credentials and never logged.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlmodel import Session, select

from src.domain.org_credential import OrgCredential
from src.utils.time_windows import parse_iso_naive

logger = logging.getLogger(__name__)

GITHUB_INTEGRATION = "github"

# `integration_type` is a plain VARCHAR(32) with no enum and no CHECK, and the
# table's uniqueness key is (organization_id, integration_type) -- so a second
# integration is a value, not a schema change. Adding "slack" needed no migration.


class VaultUnavailableError(RuntimeError):
    """The Vault wrapper function could not be called on a Postgres database.

    Distinct from "nothing stored", which is a plain ``None``. Raised so a
    missing ``supabase_vault`` extension or a dropped
    ``get_org_credential`` function surfaces as a 500 naming the cause,
    instead of every tenant in the deployment reading as unconfigured --
    Trap A from #525. Same spirit as the write/read-back guard in
    ``GitHubConnectService.connect_github_organization``.
    """


def _is_postgres(session: Session) -> bool:
    """Whether this session is bound to Postgres.

    Read from the bind's dialect rather than sniffed out of the exception
    text: SQLite's "no such function" and Postgres' "function does not
    exist" are both ``OperationalError``/``ProgrammingError``, the wording is
    a driver detail, and a message match would silently stop matching on a
    driver upgrade. A session with no resolvable bind (a test double) is
    treated as not-Postgres, which keeps the historical swallow.
    """
    try:
        bind = session.get_bind()
    except Exception:  # pragma: no cover - no bind is a test double, not a backend
        return False
    return bool(bind is not None and bind.dialect.name == "postgresql")


def _naive_utc_now() -> Optional[datetime]:
    """Now, as **naive UTC** -- the convention for this schema's columns.

    Via ``parse_iso_naive`` rather than a local ``.replace(tzinfo=None)``:
    CLAUDE.md's datetime section names that helper as the one conversion, and
    the hand-rolled form is the bug it exists to prevent (it strips an offset
    instead of converting it).
    """
    return parse_iso_naive(datetime.now(timezone.utc))


def get_org_credential_payload(
    session: Session, organization_id: str, integration_type: str
) -> Optional[Dict[str, Any]]:
    """Decrypted credential payload for an org's integration, or None.

    Returns None when no credential is stored (the caller decides whether that
    is fatal). A stored-but-unparseable payload is also None, logged without
    the value so a corrupt secret can't leak through the log.

    Raises:
        VaultUnavailableError: on **Postgres**, if the wrapper function cannot
            be called at all. On Postgres that is a broken deployment, not an
            unconfigured tenant, and swallowing it made every tenant read as
            unconfigured (#525 Trap A). On any other backend the call is
            still swallowed -- see the branch below.
    """
    try:
        row = session.exec(
            text(
                "SELECT get_org_credential(:org_id, :integration) AS payload"
            ).bindparams(org_id=organization_id, integration=integration_type)
        ).first()
    except (OperationalError, ProgrammingError) as exc:
        # Roll back either way: Postgres refuses every later statement on an
        # aborted transaction, so leaving it open would turn one failure into
        # a cascade (and a COMMIT into a silent ROLLBACK).
        session.rollback()
        if _is_postgres(session):
            # The function is supposed to exist here. Missing extension,
            # dropped function, revoked EXECUTE — all of them mean *no*
            # tenant's credential can be read, and returning None would
            # report that as "nobody has connected GitHub".
            raise VaultUnavailableError(
                "get_org_credential could not be called on this Postgres "
                "database — check the supabase_vault extension, the "
                "get_org_credential function, and its EXECUTE grant. "
                "Refusing to report the organization as unconfigured."
            ) from exc
        # A non-Postgres backend (SQLite, used by the test suite) has no such
        # function and never will. Treat that as "no credential stored" — the
        # same outcome a caller gets on Postgres with nothing stored yet.
        logger.debug(
            "get_org_credential unavailable on this backend; "
            "treating org=%s integration=%s as unconfigured",
            organization_id,
            integration_type,
        )
        return None

    raw = row[0] if row else None
    if not raw:
        return None

    try:
        payload = json.loads(raw)
    except (TypeError, ValueError):
        logger.warning(
            "org_credentials payload for org=%s integration=%s is not valid JSON",
            organization_id,
            integration_type,
        )
        return None

    if not isinstance(payload, dict):
        logger.warning(
            "org_credentials payload for org=%s integration=%s is not an object",
            organization_id,
            integration_type,
        )
        return None
    return payload


def set_org_credential(
    session: Session,
    organization_id: str,
    integration_type: str,
    payload: Dict[str, Any],
    rotated_by_user_id: Optional[str] = None,
) -> None:
    """Create or rotate an org's integration credential in Vault.

    Upsert on (organization_id, integration_type): an existing secret is
    updated in place so the vault_secret_id pointer stays stable.
    """
    session.exec(
        text(
            "SELECT set_org_credential(:org_id, :integration, :payload, :user_id)"
        ).bindparams(
            org_id=organization_id,
            integration=integration_type,
            payload=json.dumps(payload),
            user_id=rotated_by_user_id,
        )
    )
    session.commit()


def mark_org_credential_validated(
    session: Session,
    organization_id: str,
    integration_type: str,
) -> Optional[datetime]:
    """Stamp ``last_validated_at`` on an org's existing credential row.

    Deliberately **not** folded into ``set_org_credential``. Storing a
    credential and validating one are different claims: the registration-only
    branch of ``POST /integrations/github/connect`` stores nothing but could,
    and any future writer would inherit a validation timestamp it never
    earned. The column exists to answer "when did someone last prove this
    token works", so only a code path that actually proved it may write it.
    A separate updater is also required regardless, because revalidation
    (``POST /integrations/{service}/validate``) proves the token without
    writing a credential at all -- one mechanism, two call sites, rather than
    a flag threaded through the writer.

    Plain ORM UPDATE rather than a new SQL function: the column lives on
    ``org_credentials``, which is an ordinary table (the Vault chokepoint is
    the *secret*, not the audit columns), and ``set_org_credential``'s
    signature is deployed and correct — it must not change.

    Returns the timestamp written, or None when there was no row to stamp. A
    missing row is a warning rather than an exception: on a backend without the
    Vault functions (SQLite) no row was ever created, and a
    validated-and-stored credential must not be reported as a failure over a
    bookkeeping column.
    """
    row = session.exec(
        select(OrgCredential).where(
            OrgCredential.organization_id == organization_id,
            OrgCredential.integration_type == integration_type,
        )
    ).first()
    if row is None:
        logger.warning(
            "no org_credentials row to stamp last_validated_at on for "
            "org=%s integration=%s",
            organization_id,
            integration_type,
        )
        return None

    stamped_at = _naive_utc_now()
    row.last_validated_at = stamped_at
    session.add(row)
    session.commit()
    return stamped_at


def get_github_credentials(
    session: Session, organization_id: str
) -> Optional[Dict[str, str]]:
    """GitHub credentials for an org as {"token": ..., "github_org": ...}.

    Shaped to match what CredentialProvider.get_integration_credentials
    returned, so existing call sites need no rewrite. Returns None if no
    credential is stored or it carries no token.
    """
    payload = get_org_credential_payload(session, organization_id, GITHUB_INTEGRATION)
    if not payload:
        return None
    token = payload.get("token")
    if not token:
        logger.warning(
            "org_credentials GitHub payload for org=%s has no token", organization_id
        )
        return None
    creds = {"token": token}
    github_org = payload.get("github_org")
    if github_org:
        creds["github_org"] = github_org
    return creds


def set_github_credentials(
    session: Session,
    organization_id: str,
    token: str,
    github_org: Optional[str] = None,
    rotated_by_user_id: Optional[str] = None,
) -> None:
    """Store/rotate an org's GitHub token (+ optional github_org login)."""
    payload: Dict[str, Any] = {"token": token}
    if github_org:
        payload["github_org"] = github_org
    set_org_credential(
        session,
        organization_id,
        GITHUB_INTEGRATION,
        payload,
        rotated_by_user_id=rotated_by_user_id,
    )
