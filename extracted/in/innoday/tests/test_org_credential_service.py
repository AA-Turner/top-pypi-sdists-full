"""Reader/stamper behaviour for the org_credentials Vault chokepoint (#572).

Two properties here are in tension, which is the whole reason this file exists:

* On **SQLite** ``get_org_credential_payload`` must keep returning ``None``. The
  wrapper is a Postgres function and SQLite will never have it; the entire test
  suite reads "no such function" as "nothing stored". Measured, by forcing
  ``_is_postgres`` to True and running the whole suite: **7 failures** — most
  callers patch ``get_github_credentials`` in their own module, so the shared
  reader is reached far less often than the blast radius first looks. Seven is
  still seven files' worth of unrelated red for one wrong branch, which is why
  the property is pinned explicitly below rather than left to them.
* On **Postgres** the same failure must **raise**. There the function is
  supposed to exist, so a failed call means a missing ``supabase_vault``
  extension, a dropped function or a revoked grant — and returning ``None``
  reports *every tenant in the deployment* as never having connected GitHub.
  That is Trap A from #525.

``test_reader_raises_on_real_postgres_missing_vault`` is the load-bearing one:
it runs against a real Postgres migrated from empty, where
``get_org_credential`` genuinely exists (the ``security_baseline`` migration
creates it) and genuinely fails at call time because there is no ``vault``
schema. Nothing is simulated. It **skips silently** without a reachable
Postgres, so the fake-dialect test below stands in for it locally — that one
proves the branch is keyed on the dialect, not that the branch fires against a
real broken database.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlmodel import Session, select

from src.domain.org_credential import OrgCredential
from src.domain.organization import Organization
from src.services.org_credential_service import (
    GITHUB_INTEGRATION,
    VaultUnavailableError,
    get_github_credentials,
    get_org_credential_payload,
    mark_org_credential_validated,
)
from tests.db_helpers import build_test_engine

ORG_ID = "org-under-test"


@pytest.fixture
def sqlite_session():
    engine = build_test_engine()
    with Session(engine) as session:
        yield session


def _fake_postgres_session(exc: Exception) -> MagicMock:
    """A session that looks bound to Postgres and fails the wrapper call.

    The dialect is what the production branch reads, so that is what has to be
    faked. Deliberately *not* an exception-message match: SQLite says "no such
    function" and Postgres "function ... does not exist", both as the same
    exception classes, and both strings are driver details.
    """
    session = MagicMock()
    session.get_bind.return_value.dialect.name = "postgresql"
    session.exec.side_effect = exc
    return session


def _programming_error(message: str) -> ProgrammingError:
    return ProgrammingError("SELECT get_org_credential(...)", {}, Exception(message))


class TestReaderIsLoudOnPostgresQuietOnSqlite:
    def test_reader_returns_none_on_sqlite(self, sqlite_session):
        """The property the rest of the suite depends on. Do not relax."""
        assert (
            get_org_credential_payload(sqlite_session, ORG_ID, GITHUB_INTEGRATION)
            is None
        )

    def test_github_reader_returns_none_on_sqlite(self, sqlite_session):
        """Same property one layer up, where most callers actually enter."""
        assert get_github_credentials(sqlite_session, ORG_ID) is None

    def test_reader_raises_on_postgres_dialect(self):
        session = _fake_postgres_session(
            _programming_error("function get_org_credential(text, text) does not exist")
        )

        with pytest.raises(VaultUnavailableError) as excinfo:
            get_org_credential_payload(session, ORG_ID, GITHUB_INTEGRATION)

        # The message has to name what an operator should go and look at.
        assert "supabase_vault" in str(excinfo.value)
        # An aborted Postgres transaction refuses every later statement and
        # turns COMMIT into a silent ROLLBACK, so the rollback must happen even
        # on the raising path.
        session.rollback.assert_called_once()

    def test_github_reader_propagates_the_raise_on_postgres(self):
        """The loudness must not be swallowed by the GitHub-shaped wrapper."""
        session = _fake_postgres_session(_programming_error("boom"))

        with pytest.raises(VaultUnavailableError):
            get_github_credentials(session, ORG_ID)

    def test_reader_raises_on_real_postgres_missing_vault(self, pg_engine):
        """No simulation: a real Postgres with the function but no vault schema.

        Skips silently without INNODAY_TEST_POSTGRES_URL / a reachable
        DATABASE_URL — see this module's docstring.
        """
        with Session(pg_engine) as session:
            assert (
                session.exec(
                    text(
                        "SELECT count(*) FROM pg_proc WHERE proname = 'get_org_credential'"
                    )
                ).first()[0]
                == 1
            ), "precondition: the wrapper function must exist here"
            assert (
                session.exec(
                    text("SELECT count(*) FROM pg_namespace WHERE nspname = 'vault'")
                ).first()[0]
                == 0
            ), "precondition: this test needs a database WITHOUT the vault schema"

            with pytest.raises(VaultUnavailableError):
                get_org_credential_payload(session, ORG_ID, GITHUB_INTEGRATION)


class TestMarkOrgCredentialValidated:
    def _row(self, session: Session) -> OrgCredential:
        org = Organization(id=str(uuid4()), name="Stamp Org")
        session.add(org)
        row = OrgCredential(
            id=str(uuid4()),
            organization_id=org.id,
            integration_type=GITHUB_INTEGRATION,
            vault_secret_id=str(uuid4()),
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    def test_stamps_naive_utc(self, sqlite_session):
        row = self._row(sqlite_session)
        assert row.last_validated_at is None

        stamped = mark_org_credential_validated(
            sqlite_session, row.organization_id, GITHUB_INTEGRATION
        )

        assert stamped is not None
        # Naive UTC is this schema's convention (99 naive columns to 7 aware);
        # an aware value in a naive column is how the TypeError class of bug
        # gets in.
        assert stamped.tzinfo is None
        assert abs(
            stamped - datetime.now(timezone.utc).replace(tzinfo=None)
        ) < timedelta(minutes=5)

        sqlite_session.expire_all()
        persisted = sqlite_session.exec(
            select(OrgCredential).where(OrgCredential.id == row.id)
        ).first()
        assert persisted.last_validated_at == stamped

    def test_returns_none_when_there_is_no_row(self, sqlite_session):
        """A validated credential must not fail over a bookkeeping column."""
        assert (
            mark_org_credential_validated(
                sqlite_session, "no-such-org", GITHUB_INTEGRATION
            )
            is None
        )

    def test_does_not_stamp_a_different_integration(self, sqlite_session):
        row = self._row(sqlite_session)

        assert (
            mark_org_credential_validated(sqlite_session, row.organization_id, "slack")
            is None
        )

        sqlite_session.expire_all()
        persisted = sqlite_session.exec(
            select(OrgCredential).where(OrgCredential.id == row.id)
        ).first()
        assert persisted.last_validated_at is None
