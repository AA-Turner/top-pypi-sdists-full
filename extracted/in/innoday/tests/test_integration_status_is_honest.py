"""`GET .../integrations` must answer GitHub's status from values that get written.

Sibling of `tests/test_unimplemented_routes_are_honest.py`: that file pins the
routes which admit they do nothing, this one pins the route that *did* answer and
was wrong. Both failures read identically to a caller — a confident answer with
nothing behind it.

Two columns were the whole problem, and neither was inaccurate. They were simply
never written on the path that matters (#652):

* **`connected` came from the existence of a `GitHubOrgRegistration` row.** That row
  is created only by `connect_github_organization`, and only when a `user_id` is
  attributable. Discovery and every project sync work fine without one, resolving
  the token from Vault. So the flag answered "did somebody once call the connect
  endpoint?" — and an org syncing daily through a working Vault credential reported
  `connected: false`.
* **`last_sync` came from `registration.last_sync_at`**, whose only writer was
  `RepositorySyncService` — the org-wide registration sync, whose sole remote caller
  spent months POSTing to a path no route served, and which #658 deleted outright
  (repositories arrive only by project topic now). So an org that had synced that
  morning reported "never synced", and nothing writes that column at all any more.

Combined, the endpoint's two most-read fields were both answerable only by a code
path nothing exercised, which is why "connected, never synced" was the standing
answer for every org.

The handler is called directly rather than through `TestClient`: the assertions are
about which *stored* value each field is derived from, and routing/auth are covered
elsewhere (`tests/test_auth_tiers.py`).
"""

from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from src.domain.repository import GitHubOrgRegistration, Repository

CREDENTIAL = {"token": "ghp_tenant", "github_org": "tenant-gh-org"}


async def _overview(session, org_id, *, credential):
    """Invoke the handler with the Vault lookup stubbed to `credential`."""
    from src.routers.integrations import get_integrations_overview

    with patch(
        "src.routers.integrations.get_github_credentials", return_value=credential
    ):
        return await get_integrations_overview(
            organization_id=org_id,
            session=session,
            current_user=MagicMock(id="test-user"),
            _org=MagicMock(id=org_id),
        )


def _registration(session, org, user, **kwargs):
    reg = GitHubOrgRegistration(
        id=str(uuid4()),
        user_id=user.id,
        organization_id=org.id,
        organization="tenant-gh-org",
        status="active",
        sync_enabled=True,
        **kwargs,
    )
    session.add(reg)
    session.commit()
    return reg


def _repository(session, org, *, name, last_synced_at):
    repo = Repository(
        id=str(uuid4()),
        organization_id=org.id,
        name=name,
        full_name=f"tenant-gh-org/{name}",
        url=f"https://github.com/tenant-gh-org/{name}",
        last_synced_at=last_synced_at,
    )
    session.add(repo)
    session.commit()
    return repo


class TestConnectedAnswersFromTheCredential:
    @pytest.mark.asyncio
    async def test_a_vault_credential_and_no_registration_row_is_connected(
        self, db_session, org
    ):
        """The configuration this endpoint used to deny outright.

        No registration row exists, and none is needed: the credential is what a
        sync authenticates with, so it is what decides whether GitHub is reachable.
        """
        result = await _overview(db_session, org.id, credential=CREDENTIAL)

        assert result.github.connected is True, (
            "an org whose GitHub credential is in Vault is connected — the "
            "registration row is not what a sync needs"
        )
        assert result.github.metadata["has_org_registration"] is False
        assert result.github.metadata["organization"] == "tenant-gh-org"
        assert result.summary["connected"] >= 1

    @pytest.mark.asyncio
    async def test_a_registration_row_without_a_credential_is_not_connected(
        self, db_session, org, platform_user
    ):
        """The mirror image, and the more dangerous direction.

        A registration row whose credential has been revoked or was never stored
        cannot sync at all. Reporting it connected is the failure that keeps an
        operator from looking at the one thing that is broken.
        """
        _registration(db_session, org, platform_user)

        result = await _overview(db_session, org.id, credential=None)

        assert result.github.connected is False, (
            "a registration row is not a credential; without one no sync can run"
        )
        # Still reported, just no longer standing in for "connected".
        assert result.github.metadata["has_org_registration"] is True


class TestLastSyncAnswersFromSomethingThatIsWritten:
    @pytest.mark.asyncio
    async def test_it_reads_the_repositories_not_the_registration(
        self, db_session, org, platform_user
    ):
        """`Repository.last_synced_at` is stamped by discovery on every real sync.

        The registration's own `last_sync_at` is deliberately seeded to a value far
        in the past here: if the endpoint were still reading it, this test would
        report that stale date and fail on a value that is present rather than on
        `None`. A `None`-only assertion would also pass against a handler that read
        a column nobody writes.
        """
        _registration(
            db_session,
            org,
            platform_user,
            last_sync_at=datetime(2020, 1, 1, 0, 0, 0),
        )
        _repository(
            db_session, org, name="older", last_synced_at=datetime(2026, 8, 17, 9, 0, 0)
        )
        _repository(
            db_session,
            org,
            name="newest",
            last_synced_at=datetime(2026, 8, 18, 11, 30, 0),
        )
        # A repo discovery has never reached must not drag the answer to NULL.
        _repository(db_session, org, name="never", last_synced_at=None)

        result = await _overview(db_session, org.id, credential=CREDENTIAL)

        assert result.github.last_sync == datetime(2026, 8, 18, 11, 30, 0), (
            "the newest repository sync stamp is the most recent evidence that a "
            "sync ran; `registration.last_sync_at` is written only by a path whose "
            "sole caller was pointed at a route that does not exist"
        )
        assert result.github.metadata["total_repos"] == 3

    @pytest.mark.asyncio
    async def test_an_org_that_has_never_synced_still_reports_never(
        self, db_session, org
    ):
        """The half that keeps the field meaningful.

        Without this, "read something that is written" could be satisfied by any
        non-NULL timestamp — including the moment of the call, which is exactly the
        fabrication `GET /{service}/sync/status` was turned into a 501 for.
        """
        result = await _overview(db_session, org.id, credential=CREDENTIAL)

        assert result.github.connected is True
        assert result.github.last_sync is None
        assert result.github.metadata["total_repos"] == 0


class TestErrorAnswersFromSomethingThatIsWritten:
    @pytest.mark.asyncio
    async def test_a_failing_project_sync_is_reported(self, db_session, org):
        """The third field with the same defect, and the one that matters most.

        `registration.last_error` is written only by the same never-called
        registration sync, so an org whose every project sync was failing reported
        `error: null` -- next to a `last_sync` that, once fixed, correctly shows how
        old the failure is. `Project.github_error_message` is what #641 added, what
        the dashboard icon already reads, and it arrives already narrowed through
        `_reportable_sync_error`, so it is a string this response may carry.
        """
        from src.domain.project import Project

        stale = Project(
            name="Stale",
            alias="STALE",
            description="d",
            organization_id=org.id,
            github_errored_at=datetime(2026, 8, 10, 0, 0, 0),
            github_error_message="an older failure",
        )
        newest = Project(
            name="Newest",
            alias="NEWEST",
            description="d",
            organization_id=org.id,
            github_errored_at=datetime(2026, 8, 18, 12, 0, 0),
            github_error_message="No GitHub connection found for organization",
        )
        healthy = Project(
            name="Healthy", alias="HEALTHY", description="d", organization_id=org.id
        )
        db_session.add_all([stale, newest, healthy])
        db_session.commit()

        result = await _overview(db_session, org.id, credential=CREDENTIAL)

        assert result.github.error == "No GitHub connection found for organization", (
            "the most recent recorded failure is the one an operator needs; a "
            "healthy sibling project must not clear it, and a staler failure must "
            "not win"
        )

    @pytest.mark.asyncio
    async def test_no_recorded_failure_reports_none(self, db_session, org):
        """The clearing half. A flag that is only ever set becomes permanent red."""
        from src.domain.project import Project

        db_session.add(
            Project(name="Fine", alias="FINE", description="d", organization_id=org.id)
        )
        db_session.commit()

        result = await _overview(db_session, org.id, credential=CREDENTIAL)
        assert result.github.error is None
