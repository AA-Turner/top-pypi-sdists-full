"""The project health report must not claim more than it checked.

Three properties, each of which a plausible implementation gets wrong:

* ``reachable`` is **three-valued**. Unprobed is ``None``, not ``False`` -- the
  difference between "we did not ask" and "the board said no" is the whole point
  of the endpoint, and collapsing it reports every working board as broken.
* Freshness ignores ``dry_run`` rows. A preview writes a history row that is
  otherwise indistinguishable from a real sync; reading one as freshness is a
  bug this codebase has already shipped once (see ``BoardSyncHistory.dry_run``).
* A dead database is ``unhealthy``, not a green report with a footnote.
"""

import asyncio
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from src.domain import BoardRegistration, BoardSyncHistory, BoardType
from src.domain.board import SyncStatus
from src.domain.repository import GitHubSyncHistory
from src.services.project_health_service import get_project_health


@pytest.fixture
def board(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Test Board",
        board_type=BoardType.LINEAR,
        board_url="https://linear.app/test",
        board_external_id="TEAM",
        is_active=True,
    )
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


def _sync(board_id, *, dry_run, minutes_ago, status=SyncStatus.COMPLETED):
    started = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(
        minutes=minutes_ago
    )
    return BoardSyncHistory(
        id=str(uuid4()),
        board_registration_id=board_id,
        sync_status=status,
        dry_run=dry_run,
        started_at=started,
        completed_at=started,
    )


@pytest.mark.asyncio
async def test_unprobed_board_is_null_not_false(db_session, org, project, board):
    """`probe=False` must leave a verdict unstated, not state a negative one."""
    health = await get_project_health(db_session, org, project.id, probe=False)

    (report,) = health["boards"]
    assert report["reachable"] is None, "unprobed must not be reported as unreachable"
    assert report["latency_ms"] is None
    # ...and an unstated verdict must not drag the overall status down.
    assert health["status"] == "healthy"


@pytest.mark.asyncio
async def test_dry_run_does_not_count_as_freshness(db_session, org, project, board):
    """A preview is not a sync.

    The real sync is 3 days old and a dry run ran a minute ago. Reading the dry
    run makes a stale board look fresh -- the exact failure the `dry_run` column
    was added to prevent.
    """
    db_session.add(_sync(board.id, dry_run=False, minutes_ago=3 * 24 * 60))
    db_session.add(_sync(board.id, dry_run=True, minutes_ago=1))
    db_session.commit()

    health = await get_project_health(db_session, org, project.id, probe=False)
    (report,) = health["boards"]

    age_hours = report["last_sync_age_seconds"] / 3600
    assert age_hours > 70, (
        f"reported {age_hours:.1f}h old — the 1-minute dry run was counted as a sync"
    )


@pytest.mark.asyncio
async def test_a_refused_board_is_reachable_false_and_degrades(
    db_session, org, project, board
):
    """A board that answers "no" is a verdict, and it must show in the status."""
    adapter = AsyncMock()
    adapter.validate_connection = AsyncMock(return_value=False)

    with (
        patch(
            "src.services.project_health_service.resolve_board_token",
            return_value="tok",
        ),
        patch(
            "src.services.project_health_service.build_board_adapter",
            AsyncMock(return_value=adapter),
        ),
    ):
        health = await get_project_health(db_session, org, project.id, probe=True)

    (report,) = health["boards"]
    assert report["reachable"] is False
    assert report["latency_ms"] is not None
    assert health["status"] == "degraded"


@pytest.mark.asyncio
async def test_a_reachable_board_is_healthy(db_session, org, project, board):
    """The companion direction, so the test above cannot pass by always failing."""
    adapter = AsyncMock()
    adapter.validate_connection = AsyncMock(return_value=True)

    with (
        patch(
            "src.services.project_health_service.resolve_board_token",
            return_value="tok",
        ),
        patch(
            "src.services.project_health_service.build_board_adapter",
            AsyncMock(return_value=adapter),
        ),
    ):
        health = await get_project_health(db_session, org, project.id, probe=True)

    (report,) = health["boards"]
    assert report["reachable"] is True
    assert health["status"] == "healthy"


@pytest.mark.asyncio
async def test_missing_credential_is_null_not_false(db_session, org, project, board):
    """ "No credential stored" proves nothing about the board."""
    from src.adapters import BoardCredentialError

    with patch(
        "src.services.project_health_service.resolve_board_token",
        side_effect=BoardCredentialError("no credential"),
    ):
        health = await get_project_health(db_session, org, project.id, probe=True)

    (report,) = health["boards"]
    assert report["reachable"] is None, (
        "an unaskable board must not be reported as unreachable"
    )


@pytest.mark.asyncio
async def test_dead_database_is_unhealthy(db_session, org, project, board):
    with patch(
        "src.services.project_health_service._database_connected",
        return_value=(False, None),
    ):
        health = await get_project_health(db_session, org, project.id, probe=False)

    assert health["database"] == "disconnected"
    assert health["status"] == "unhealthy"


@pytest.mark.asyncio
async def test_an_inactive_board_does_not_degrade_the_project(
    db_session, org, project, board
):
    """Deactivating a board is how you retire one, not a fault to alarm on.

    Found by running the endpoint against a real project: BPAI still carries the
    Jira board it used before moving to Linear, so it reported `degraded`
    forever. `board delete` is a soft delete, so no action could ever clear it —
    a status that can never go green is one people stop reading.
    """
    board.is_active = False
    db_session.add(board)
    db_session.commit()

    health = await get_project_health(db_session, org, project.id, probe=False)

    (report,) = health["boards"]
    assert report["is_active"] is False, "the state must still be reported"
    assert health["status"] == "healthy", (
        "an intentionally retired board is not a degraded project"
    )


@pytest.mark.asyncio
async def test_a_soft_deleted_board_is_not_reported_at_all(
    db_session, org, project, board
):
    """A deleted registration is gone, not merely inactive.

    Without the `deleted_at` filter this report resurrected boards that had
    already been deleted -- BPAI's Jira board was soft-deleted on 2026-08-08 and
    still showed up here, while `board list` correctly hid it. The two surfaces
    disagreeing is what made it look like outstanding cleanup rather than cleanup
    already done.
    """
    board.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
    board.is_active = False
    db_session.add(board)
    db_session.commit()

    health = await get_project_health(db_session, org, project.id, probe=False)

    assert health["boards"] == [], (
        "a soft-deleted board registration must not appear in the report"
    )
    assert health["status"] == "healthy"


@pytest.mark.asyncio
async def test_probing_is_the_default(db_session, org, project, board):
    """The whole point: the default answer must involve asking the board.

    It shipped defaulting off, which meant the default answer to "is this
    project working?" came entirely from InnoDay's own database — so a board
    whose credential expired months ago read as healthy. Calling with no `probe`
    argument must reach the adapter.
    """
    adapter = AsyncMock()
    adapter.validate_connection = AsyncMock(return_value=True)

    with (
        patch(
            "src.services.project_health_service.resolve_board_token",
            return_value="tok",
        ),
        patch(
            "src.services.project_health_service.build_board_adapter",
            AsyncMock(return_value=adapter),
        ),
        patch(
            "src.services.project_health_service._probe_github",
            AsyncMock(return_value={"scope": "organization", "reachable": True}),
        ),
    ):
        health = await get_project_health(db_session, org, project.id)

    adapter.validate_connection.assert_awaited()
    (report,) = health["boards"]
    assert report["reachable"] is True


@pytest.mark.asyncio
async def test_a_hanging_board_times_out_rather_than_hanging_the_report(
    db_session, org, project, board, monkeypatch
):
    """A board that never answers must not hold the report open.

    Probing is on by default, so this is the difference between a health check
    and the outage it is meant to describe.
    """
    monkeypatch.setattr(
        "src.services.project_health_service._PROBE_TIMEOUT_SECONDS", 0.05
    )

    async def _never_answers():
        await asyncio.sleep(30)
        return True

    adapter = AsyncMock()
    adapter.validate_connection = _never_answers

    with (
        patch(
            "src.services.project_health_service.resolve_board_token",
            return_value="tok",
        ),
        patch(
            "src.services.project_health_service.build_board_adapter",
            AsyncMock(return_value=adapter),
        ),
        patch(
            "src.services.project_health_service._probe_github",
            AsyncMock(return_value={"scope": "organization", "reachable": None}),
        ),
    ):
        health = await asyncio.wait_for(
            get_project_health(db_session, org, project.id), timeout=10
        )

    (report,) = health["boards"]
    assert report["reachable"] is False, "asked and got nothing is a verdict"
    assert "no answer" in report["detail"]
    assert health["status"] == "degraded"


@pytest.mark.asyncio
async def test_a_raising_probe_phase_still_returns_the_report(
    db_session, org, project, board
):
    """The database verdict and sync ages are the half that cannot fail.

    A misbehaving third party must not turn this endpoint into a 500 — that
    would make it less reliable than the four calls it replaced.
    """
    with (
        patch(
            "src.services.project_health_service._build_probe",
            AsyncMock(side_effect=RuntimeError("boom")),
        ),
        patch(
            "src.services.project_health_service._probe_github",
            AsyncMock(return_value={"scope": "organization", "reachable": None}),
        ),
    ):
        health = await get_project_health(db_session, org, project.id)

    assert health["database"] == "connected"
    (report,) = health["boards"]
    assert report["reachable"] is None
    assert "setup error" in report["detail"]


@pytest.mark.asyncio
async def test_a_rejected_github_credential_degrades_the_project(
    db_session, org, project
):
    """An expired GitHub token stops repos, issues and releases resolving.

    It was invisible everywhere else — onboarding answered 500 and repository
    discovery answered `[]`, neither saying "the token expired".
    """
    with patch(
        "src.services.project_health_service._probe_github",
        AsyncMock(
            return_value={
                "scope": "organization",
                "reachable": False,
                "detail": "credential rejected",
            }
        ),
    ):
        health = await get_project_health(db_session, org, project.id)

    assert health["github"]["reachable"] is False
    assert health["status"] == "degraded"


@pytest.mark.asyncio
async def test_github_verdict_never_carries_the_account_identity(
    db_session, org, project
):
    """`github_login` names the account the org's token belongs to.

    That disclosure is why `/integrations/{service}/validate` is ADMIN-only.
    This route is DEVELOPER, so the identity must not ride along in it.
    """
    with patch(
        "src.services.github_connect_service.GitHubConnectService.validate_stored_github_credential",
        AsyncMock(
            return_value={
                "service": "github",
                "valid": True,
                "github_org": "havilandsoftware",
                "github_login": "some-account",
                "org_access": True,
                "last_validated_at": None,
                "error": None,
            }
        ),
    ):
        health = await get_project_health(db_session, org, project.id)

    gh = health["github"]
    assert gh["reachable"] is True
    assert gh["github_org"] == "havilandsoftware"
    assert "github_login" not in gh, "the account identity must not be exposed here"


class TestWhenGitHubLastFoundThisProjectsRepositories:
    """`GitHubSyncHistory` is the only honest source for that date.

    `Repository.last_synced_at` and the registration's `last_sync_at` sit right
    beside it and are never written -- the model's own comment records a reader
    that trusted them and reported "connected, never synced" for every
    organisation.
    """

    def _run(self, session, org, project, *, status, when):
        session.add(
            GitHubSyncHistory(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project.id,
                status=status,
                started_at=when,
            )
        )
        session.commit()

    @pytest.mark.asyncio
    async def test_a_completed_run_sets_the_age(self, db_session, org, project):
        self._run(
            db_session,
            org,
            project,
            status="completed",
            when=datetime.now(timezone.utc) - timedelta(days=6),
        )

        health = await get_project_health(db_session, org, project.id, probe=False)

        age = health["github"]["last_sync_age_seconds"]
        assert age is not None and 5 * 86400 < age < 7 * 86400

    @pytest.mark.asyncio
    async def test_a_failed_run_is_not_freshness(self, db_session, org, project):
        """A failed attempt wrote nothing. Counting it is the same mistake as
        counting a board's `--dry-run`, which this codebase has already made
        once -- and it reads as a project whose repositories are current when
        discovery has been broken for a week."""
        self._run(
            db_session,
            org,
            project,
            status="failed",
            when=datetime.now(timezone.utc) - timedelta(hours=1),
        )

        health = await get_project_health(db_session, org, project.id, probe=False)

        assert health["github"]["last_sync_age_seconds"] is None

    @pytest.mark.asyncio
    async def test_the_newest_completed_run_wins(self, db_session, org, project):
        now = datetime.now(timezone.utc)
        self._run(
            db_session, org, project, status="completed", when=now - timedelta(days=30)
        )
        self._run(
            db_session, org, project, status="completed", when=now - timedelta(hours=2)
        )

        health = await get_project_health(db_session, org, project.id, probe=False)

        assert health["github"]["last_sync_age_seconds"] < 3 * 3600

    @pytest.mark.asyncio
    async def test_another_projects_sync_does_not_count(self, db_session, org, project):
        """The table also holds org-wide rows with a NULL `project_id`, and rows
        for sibling projects. Either would report this project's repositories as
        current on the strength of somebody else's run."""
        self._run(
            db_session,
            org,
            project,
            status="completed",
            when=datetime.now(timezone.utc),
        )
        health = await get_project_health(
            db_session, org, "some-other-project", probe=False
        )

        assert health["github"]["last_sync_age_seconds"] is None
