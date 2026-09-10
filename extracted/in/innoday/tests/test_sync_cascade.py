"""
Tests for `innoday sync`'s project-scoped cascade (board tickets, repos,
release status report). Mocks InnoDayAPIClient.get/post directly -- these
tests are about SyncCommands' own orchestration logic, not the routers
(which have their own test coverage).
"""

import argparse
from unittest.mock import AsyncMock, MagicMock

import pytest

import src.cli.commands.boards as boards
from src.cli.commands.sync import SyncCommands


def _config(project_id="proj-1"):
    """A config that raises if the cascade asks it for a board credential.

    The board leg of the cascade must reach no local credential store (#609);
    the server resolves the board's own credential from Vault. Making the
    attempt itself the failure is what keeps this honest -- returning None
    would pass whether or not the lookup happened.
    """
    config = MagicMock()
    config.get_current_organization.return_value = "acme"
    config.get_organization_id.return_value = "org-1"
    config.get_current_project_id.return_value = project_id
    config.get_organization_integration.side_effect = AssertionError(
        "the sync cascade read a board credential from local config"
    )
    config.get_credential.side_effect = AssertionError(
        "the sync cascade read a credential from the keyring"
    )
    return config


def _response(status_code, json_body=None, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body if json_body is not None else {}
    resp.text = text
    return resp


class TestCascadeGating:
    @pytest.mark.asyncio
    async def test_cascade_fails_without_org(self):
        config = _config()
        config.get_current_organization.return_value = None
        config.get_organization_id.return_value = None  # no org -> no id either

        result = await SyncCommands._handle_cascade(argparse.Namespace(), None, config)
        assert result == 1

    @pytest.mark.asyncio
    async def test_cascade_fails_without_project(self):
        config = _config(project_id=None)
        client = MagicMock()

        result = await SyncCommands._handle_cascade(
            argparse.Namespace(), client, config
        )
        assert result == 1


class TestSyncBoard:
    @pytest.mark.asyncio
    async def test_no_board_registered_skips_cleanly(self):
        client = MagicMock()
        client.get = AsyncMock(return_value=_response(200, []))
        config = _config()

        result = await SyncCommands._sync_board(client, "org-1", "proj-1", config)

        assert result == 0

    @pytest.mark.asyncio
    async def test_triggers_sync_with_no_locally_sourced_credential(self):
        """A board with no local credential syncs -- that used to be skipped.

        Before #609 this leg looked the board type up in
        ~/.innoday/config.json and returned early with "No jira credentials
        found" when it saw nothing, so the cascade quietly did not sync a
        board whose credential was sitting in Vault the whole time.
        """
        client = MagicMock()
        client.get = AsyncMock(
            return_value=_response(
                200, [{"id": "board-1", "board_type": "jira", "board_name": "Board"}]
            )
        )
        client.post = AsyncMock(
            return_value=_response(200, {"sync_id": "sync-1", "status": "PENDING"})
        )
        config = _config()

        # `wait=False`: this is about what the POST carries, and the fake
        # answers every GET with the board listing, so there is no
        # sync-history row to wait for. The waiting is covered below.
        result = await SyncCommands._sync_board(
            client, "org-1", "proj-1", config, wait=False
        )

        assert result == 0
        client.post.assert_called_once()
        endpoint = client.post.call_args[0][0]
        assert endpoint == "/organizations/org-1/boards/board-1/sync"
        headers = client.post.call_args.kwargs.get("headers") or {}
        assert "X-Integration-Token" not in headers

    @pytest.mark.asyncio
    async def test_board_lookup_failure_returns_error(self):
        client = MagicMock()
        client.get = AsyncMock(return_value=_response(500))
        config = _config()

        result = await SyncCommands._sync_board(client, "org-1", "proj-1", config)

        assert result == 1


class TestSyncRepos:
    @pytest.mark.asyncio
    async def test_reports_synced_repos(self):
        client = MagicMock()
        client.post = AsyncMock(
            return_value=_response(
                200,
                {
                    "repositories_synced": 2,
                    "github_label": "my-project",
                    "new_repositories": [{"name": "repo-a", "layer": "api", "url": ""}],
                    "deactivated_repositories": 0,
                },
            )
        )

        result = await SyncCommands._sync_repos(client, "org-1", "proj-1")

        assert result == 0
        endpoint = client.post.call_args[0][0]
        assert endpoint == "/organizations/org-1/projects/proj-1/repositories/discover"

    @pytest.mark.asyncio
    async def test_failure_returns_error(self):
        client = MagicMock()
        client.post = AsyncMock(return_value=_response(400, text="bad request"))

        result = await SyncCommands._sync_repos(client, "org-1", "proj-1")

        assert result == 1


class TestReportReleases:
    @pytest.mark.asyncio
    async def test_reports_no_releases(self):
        client = MagicMock()
        client.get = AsyncMock(return_value=_response(200, []))

        # Should not raise
        await SyncCommands._report_releases(client, "org-1", "proj-1")

        params = client.get.call_args.kwargs["params"]
        assert params == {"project_id": "proj-1"}

    @pytest.mark.asyncio
    async def test_reports_existing_releases(self):
        client = MagicMock()
        client.get = AsyncMock(
            return_value=_response(
                200, [{"version": "v1.0.0", "status": "released", "released_at": None}]
            )
        )

        await SyncCommands._report_releases(client, "org-1", "proj-1")


# ---------------------------------------------------- waiting for the sync (#741)
#
# Stage 1 POSTs to a route that queues the work and returns immediately, so
# "queued" was reported as success and stages 2 and 3 ran over tickets that
# were still being imported. `innoday sync` now waits for the run to reach a
# terminal state and reports what it actually did.


@pytest.fixture(autouse=True)
def _no_poll_delay(monkeypatch):
    """Poll with no delay -- the interval is not what these tests are about."""
    monkeypatch.setattr(boards, "SYNC_POLL_INTERVAL", 0)


def _history(status, **fields):
    """One sync-history row, shaped like `GET .../sync-history` returns them."""
    record = {
        "id": "sync-1",
        "sync_status": status,
        "tickets_found": 0,
        "tickets_created": 0,
        "tickets_updated": 0,
        "tickets_skipped": 0,
        "error_message": None,
        "started_at": "2026-09-08T09:00:00+00:00",
        "completed_at": None,
        "duration_seconds": None,
    }
    record.update(fields)
    return record


class _WaitingClient:
    """Routes by path: project sync status, board listing, sync history, repos.

    `history` is consumed one row per poll with the last row repeating, so a
    test can spell out a run that is still moving before it settles.
    """

    def __init__(self, history=None, sync_status_code=200, sync_payload=None):
        self.history = list(history or [_history("COMPLETED")])
        self._sync_status_code = sync_status_code
        self._sync_payload = sync_payload or {"sync_id": "sync-1", "status": "PENDING"}
        self.gets = []
        self.posts = []

    async def get(self, path, params=None):
        self.gets.append(path)
        if path.endswith("/sync/status"):
            return _response(200, {"running": [], "last_sync": None, "is_fresh": True})
        if path.endswith("/sync-history"):
            entry = self.history.pop(0) if len(self.history) > 1 else self.history[0]
            if isinstance(entry, int):
                # That poll was answered with an HTTP status, not a body.
                return _response(entry, {"detail": "Not authenticated"})
            rows = entry if isinstance(entry, list) else [entry]
            return _response(200, rows)
        if path.endswith("/boards"):
            return _response(
                200,
                [{"id": "board-1", "board_name": "Board One", "board_type": "linear"}],
            )
        return _response(200, [])

    async def post(self, path, json=None):
        self.posts.append(path)
        if path.endswith("/sync"):
            return _response(self._sync_status_code, self._sync_payload)
        return _response(
            200,
            {
                "repositories_synced": 0,
                "github_label": "bpai",
                "new_repositories": [],
                "deactivated_repositories": 0,
            },
        )

    @property
    def polls(self):
        return [path for path in self.gets if path.endswith("/sync-history")]


class TestSyncBoardWaitsForCompletion:
    @pytest.mark.asyncio
    async def test_a_completed_sync_reports_the_real_counts_and_exits_zero(
        self, capsys
    ):
        """ "Queued" is not an outcome -- the counts are."""
        client = _WaitingClient(
            [
                _history("IN_PROGRESS"),
                _history(
                    "COMPLETED",
                    tickets_found=257,
                    tickets_created=40,
                    tickets_updated=200,
                    tickets_skipped=17,
                    duration_seconds=153,
                    completed_at="2026-09-08T09:02:33+00:00",
                ),
            ]
        )

        result = await SyncCommands._sync_board(
            client, "org-1", "proj-1", _config(), wait_timeout=5.0
        )

        out = capsys.readouterr().out
        assert result == 0
        # It kept asking, rather than reading the first row and stopping.
        assert len(client.polls) >= 2, client.gets
        for count in ("257", "40", "200", "17", "153"):
            assert count in out, out
        assert "queued" not in out.lower(), out

    @pytest.mark.asyncio
    async def test_a_failed_sync_exits_non_zero(self, capsys):
        client = _WaitingClient(
            [_history("FAILED", error_message="Jira returned 401", tickets_found=0)]
        )

        result = await SyncCommands._sync_board(
            client, "org-1", "proj-1", _config(), wait_timeout=5.0
        )

        out = capsys.readouterr().out
        assert result == 1, "a failed sync reported success"
        assert "failed" in out.lower()
        assert "Jira returned 401" in out

    @pytest.mark.asyncio
    async def test_a_sync_that_never_finishes_times_out_and_exits_non_zero(
        self, capsys
    ):
        client = _WaitingClient([_history("IN_PROGRESS")])

        result = await SyncCommands._sync_board(
            client, "org-1", "proj-1", _config(), wait_timeout=0.0
        )

        out = capsys.readouterr().out
        assert result == 1, "a sync still running reported success"
        assert client.polls, "gave up without ever asking"
        assert "did not finish" in out.lower(), out
        # The operator is left with a run in flight, so point at how to watch it.
        assert "innoday board sync-status --board-id board-1" in out

    @pytest.mark.asyncio
    async def test_a_sync_the_server_gave_no_id_for_is_not_matched_by_recency(
        self, capsys
    ):
        """`sync_id` is how the wait finds *our* run's row.

        Without it the only thing left to match on is "the newest row", and a
        previous COMPLETED sync then ends this wait instantly with its own
        counts reported as ours. So a missing id stops the stage rather than
        falling back -- which also stops the cascade, since stage 3 would
        otherwise report over tickets nobody confirmed had arrived.
        """
        client = _WaitingClient(
            [_history("COMPLETED", tickets_found=999)],
            sync_payload={"sync_id": None, "status": "PENDING"},
        )

        result = await SyncCommands._sync_board(
            client, "org-1", "proj-1", _config(), wait_timeout=5.0
        )

        out = capsys.readouterr().out
        assert result == 1, "a sync with no id to match on reported success"
        assert not client.polls, "polled anyway, with nothing to match against"
        assert "999" not in out, out

    @pytest.mark.asyncio
    async def test_an_unreadable_history_route_is_not_reported_as_a_timeout(
        self, capsys
    ):
        """A 403 says nothing about the run, and will not clear by waiting."""
        client = _WaitingClient([403])

        result = await SyncCommands._sync_board(
            client, "org-1", "proj-1", _config(), wait_timeout=None
        )

        out = capsys.readouterr().out
        assert result == 1
        assert len(client.polls) == 1, client.polls
        assert "403" in out, out
        assert "did not finish within" not in out, out

    @pytest.mark.asyncio
    async def test_no_wait_returns_as_soon_as_it_is_queued(self, capsys):
        """The old behaviour, kept behind an explicit flag."""
        client = _WaitingClient()

        result = await SyncCommands._sync_board(
            client, "org-1", "proj-1", _config(), wait=False
        )

        out = capsys.readouterr().out
        assert result == 0
        assert "Board sync queued for Board One" in out
        assert "sync-1" in out
        assert "innoday board sync-status --board-id board-1" in out
        assert not client.polls, "--no-wait polled anyway"


class TestCascadeGatesOnTheBoardStage:
    @staticmethod
    def _args(**overrides):
        args = argparse.Namespace(
            scope="all",
            since=None,
            no_wait=False,
            wait_timeout=5.0,
            sync_command=None,
            sync_status_only=False,
        )
        for key, value in overrides.items():
            setattr(args, key, value)
        return args

    @pytest.mark.asyncio
    async def test_a_failed_board_stage_stops_before_repos_and_releases(self, capsys):
        """A release table assembled over half-imported tickets is worse than none."""
        client = _WaitingClient([_history("FAILED", error_message="boom")])

        result = await SyncCommands._handle_cascade(self._args(), client, _config())

        out = capsys.readouterr().out
        assert result == 1
        assert not [p for p in client.posts if "repositories/discover" in p], (
            "repositories were synced over a board sync that failed"
        )
        assert not [g for g in client.gets if g.endswith("/releases")], (
            "releases were reported over a board sync that failed"
        )
        assert "2. Repositories" not in out
        assert "3. Releases" not in out

    @pytest.mark.asyncio
    async def test_a_completed_board_stage_lets_the_rest_of_the_cascade_run(self):
        client = _WaitingClient([_history("COMPLETED", tickets_found=3)])

        result = await SyncCommands._handle_cascade(self._args(), client, _config())

        assert result == 0
        assert [p for p in client.posts if "repositories/discover" in p]
        assert [g for g in client.gets if g.endswith("/releases")]

    @pytest.mark.asyncio
    async def test_no_wait_leaves_the_cascade_ordering_as_it_was(self):
        """With --no-wait there is nothing to wait for, so nothing to gate on."""
        client = _WaitingClient(sync_status_code=429, sync_payload={"detail": "busy"})

        result = await SyncCommands._handle_cascade(
            self._args(no_wait=True), client, _config()
        )

        assert result == 1  # the refusal still exits 1 (#622)
        assert [p for p in client.posts if "repositories/discover" in p]
        assert not client.polls
