"""#554 on the surviving endpoint: `POST /boards/{board_id}/sync`.

`POST /integrations/{trello|jira}/sync` resolved ONE token for a loop over every
board of that type in the org:

    token = x_integration_token or os.environ.get("GITHUB_TOKEN", "")
    for board in boards:
        background_tasks.add_task(sync_board_tickets_task, ..., token=token)

and `board_sync_service._get_adapter` never resolves a credential of its own — the
token is whatever the caller passed. So on any deployment with `GITHUB_TOKEN` set
and no `X-Integration-Token` header, every Trello board in the org synced with the
operator's **GitHub** token.

That is worse than a 401. `build_board_adapter`'s Jira branch raises on a token
with no colon, but its Trello branch does `api_key = api_token = token`, and
`TrelloAPI` puts both into `auth_params` — i.e. the operator's GitHub PAT is sent
to `api.trello.com` as query-string parameters, landing in a third party's request
logs. That endpoint duplicated this one and **has been deleted** (#595), along
with its regression tests (`tests/test_integrations_board_sync_credentials.py`),
which were the only place in the repo where credential fail-closed behaviour was
asserted for any sync path. This file is where that property is pinned now, on the
endpoint that survives, and `TestTheDuplicateFanOutRouteStaysDeleted` below keeps
the deletion itself from being quietly undone.

`get_board_credential_payload` is patched at its import location in
`src.routers.boards`: it calls a Postgres function that does not exist on the
SQLite test backend, and unlike its org-level sibling it does not swallow the
error — so patching is what makes the assertions about a real resolved value
rather than about an exception path.

**Scope of the "no GitHub-shaped token" claim.** What must be impossible is a
*server-side* credential reaching a board adapter: the env var, or any org-wide
value the caller did not name. `X-Integration-Token` on this endpoint is a
different thing and stays — it is one caller-supplied credential against one
named board, which is what made the org-wide header on the deleted endpoint
incoherent. These tests therefore pin: with `GITHUB_TOKEN` set and no header, the
board's own Vault credential is what is queued, and a board with no credential
fails closed rather than borrowing anything.
"""

import re
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import BackgroundTasks, HTTPException
from sqlmodel import select

from src.domain.board import BoardRegistration, BoardSyncHistory, BoardType

ROUTERS = Path(__file__).resolve().parents[1] / "src" / "routers"


def _route_decorator(method: str, path: str) -> re.Pattern:
    """A route-decorator matcher that a re-spelling cannot slip past.

    An exact-byte match on `@router.post("/{service}/sync")` guards precisely one
    spelling of the thing it guards: single quotes, an added
    `status_code=`/`response_model=` kwarg, or the multi-line decorator style
    already used elsewhere in `boards.py`/`repositories.py` would all reinstate
    the route while leaving the guard green -- a test that cannot fail. So match
    the decorator name, any quote style, and any whitespace/newline between `(`
    and the path, and stop at the closing quote so trailing kwargs are ignored.
    """
    return re.compile(
        r"@\w+\." + method + r"\(\s*(['\"])" + re.escape(path) + r"\1",
    )


SERVICE_SYNC_POST = _route_decorator("post", "/{service}/sync")
SERVICE_SYNC_STATUS_GET = _route_decorator("get", "/{service}/sync/status")

OPERATOR_TOKEN = "ghp_operator_must_never_be_used"
GITHUB_TOKEN_PREFIXES = ("ghp_", "gho_", "ghs_", "github_pat_")
TRELLO_PAYLOAD = {"api_key": "trello_key", "token": "trello_secret"}
TRELLO_LEGACY_TOKEN = "trello_key:trello_secret"


@pytest.fixture
def trello_board(db_session, org, project):
    board = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="Trello Board",
        board_type=BoardType.TRELLO,
        board_url="https://trello.com/b/abc123",
        board_external_id=uuid4().hex[:8],
        is_active=True,
    )
    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)
    return board


async def _call_board_sync(session, org_id, board_id, user, *, token=None):
    """Invoke the endpoint, returning the tokens its queued tasks carry."""
    from src.routers.boards import SyncRequest, sync_board

    background_tasks = BackgroundTasks()
    result = await sync_board(
        organization_id=org_id,
        board_id=board_id,
        sync_request=SyncRequest(full_sync=True),
        background_tasks=background_tasks,
        token=token,
        session=session,
        current_user=user,
    )
    queued = [
        t.kwargs.get("token") for t in background_tasks.tasks if t.kwargs is not None
    ]
    return result, background_tasks, queued


class TestBoardSyncResolvesTheBoardsOwnCredential:
    @pytest.mark.asyncio
    async def test_the_vault_token_is_queued_not_the_process_env_one(
        self, db_session, org, trello_board, platform_user, monkeypatch
    ):
        monkeypatch.setenv("GITHUB_TOKEN", OPERATOR_TOKEN)

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value=dict(TRELLO_PAYLOAD),
        ) as resolver:
            _, _, queued = await _call_board_sync(
                db_session, org.id, trello_board.id, platform_user
            )

        # The stored credential won, and the resolver was actually consulted --
        # without that second assertion this passes against code that resolves
        # nothing at all.
        assert queued == [TRELLO_LEGACY_TOKEN]
        resolver.assert_called_once()
        assert OPERATOR_TOKEN not in queued

    @pytest.mark.asyncio
    async def test_no_queued_token_is_a_github_credential(
        self, db_session, org, trello_board, platform_user, monkeypatch
    ):
        """The disclosure assertion, stated independently of the happy path.

        A GitHub PAT is recognisable by prefix. None may ever be handed to a
        board adapter from the server's own environment, whatever else changes.
        """
        monkeypatch.setenv("GITHUB_TOKEN", OPERATOR_TOKEN)

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value=dict(TRELLO_PAYLOAD),
        ):
            _, _, queued = await _call_board_sync(
                db_session, org.id, trello_board.id, platform_user
            )

        assert queued
        for token in queued:
            assert not token.startswith(GITHUB_TOKEN_PREFIXES)

    @pytest.mark.asyncio
    async def test_the_header_overrides_the_stored_credential_for_this_one_board(
        self, db_session, org, trello_board, platform_user, monkeypatch
    ):
        """One caller-supplied credential against one named board is the
        legitimate override, and it short-circuits the Vault lookup."""
        monkeypatch.setenv("GITHUB_TOKEN", OPERATOR_TOKEN)

        with patch(
            "src.routers.boards.get_board_credential_payload",
            return_value=dict(TRELLO_PAYLOAD),
        ) as resolver:
            _, _, queued = await _call_board_sync(
                db_session,
                org.id,
                trello_board.id,
                platform_user,
                token="caller_key:caller_secret",
            )

        assert queued == ["caller_key:caller_secret"]
        resolver.assert_not_called()
        assert OPERATOR_TOKEN not in queued


class TestBoardSyncFailsClosed:
    @pytest.mark.asyncio
    async def test_board_without_a_stored_credential_gets_400_and_queues_nothing(
        self, db_session, org, trello_board, platform_user, monkeypatch
    ):
        monkeypatch.setenv("GITHUB_TOKEN", OPERATOR_TOKEN)

        with (
            patch("src.routers.boards.get_board_credential_payload", return_value=None),
            pytest.raises(HTTPException) as ei,
        ):
            await _call_board_sync(db_session, org.id, trello_board.id, platform_user)

        assert ei.value.status_code == 400
        detail = str(ei.value.detail)
        assert "credential" in detail.lower()
        assert "X-Integration-Token" in detail

    @pytest.mark.asyncio
    async def test_no_background_task_is_queued_without_a_credential(
        self, db_session, org, trello_board, platform_user, monkeypatch
    ):
        """The fail-closed twin, asserted at the boundary rather than on the
        response: a 400 that still queued the task would hand the operator's
        GitHub token to `api.trello.com` exactly as before while looking fixed.

        The rejection itself is the sibling test's job, so this one deliberately
        swallows the ``HTTPException`` and reports what was queued. That is what
        makes the failure message name the leaked credential instead of only
        saying "DID NOT RAISE".
        """
        from src.routers.boards import SyncRequest, sync_board

        monkeypatch.setenv("GITHUB_TOKEN", OPERATOR_TOKEN)
        background_tasks = BackgroundTasks()

        with patch(
            "src.routers.boards.get_board_credential_payload", return_value=None
        ):
            try:
                await sync_board(
                    organization_id=org.id,
                    board_id=trello_board.id,
                    sync_request=SyncRequest(full_sync=True),
                    background_tasks=background_tasks,
                    token=None,
                    session=db_session,
                    current_user=platform_user,
                )
            except HTTPException:
                pass

        queued = [
            t.kwargs.get("token")
            for t in background_tasks.tasks
            if t.kwargs is not None
        ]
        assert queued == []

    @pytest.mark.asyncio
    async def test_no_sync_history_row_is_written_without_a_credential(
        self, db_session, org, trello_board, platform_user, monkeypatch
    ):
        """A PENDING history row for a sync that never runs blocks this board's
        next `force=false` sync, so the credential check has to come first."""
        monkeypatch.setenv("GITHUB_TOKEN", OPERATOR_TOKEN)

        with (
            patch("src.routers.boards.get_board_credential_payload", return_value=None),
            pytest.raises(HTTPException),
        ):
            await _call_board_sync(db_session, org.id, trello_board.id, platform_user)

        rows = db_session.exec(
            select(BoardSyncHistory).where(
                BoardSyncHistory.board_registration_id == trello_board.id
            )
        ).all()
        assert rows == []


class TestTheDuplicateFanOutRouteStaysDeleted:
    """The deletion is enforced here rather than in a file of its own.

    A guard living beside the tests for the endpoint that *survived* is a guard
    someone reads while working on this behaviour; a standalone
    `test_route_is_gone.py` is a file nobody opens until it goes red. Precedent:
    #590 made its own deletion self-enforcing inside the existing gate file.

    Reinstating the fan-out route would not merely duplicate `sync_board`: the
    only coherent reading of one `X-Integration-Token` against every board of a
    type is "use this for all of them", which is precisely how an operator's
    GitHub PAT reached `api.trello.com`'s query string. The assertions are static
    (a decorator string, not a live app) because that is what actually fails if
    someone pastes the handler back -- an app-level 404 probe would also pass if
    the route were re-added under a different path.
    """

    def test_integrations_router_declares_no_service_sync_post(self):
        text = (ROUTERS / "integrations.py").read_text()
        match = SERVICE_SYNC_POST.search(text)
        found = match.group(0) if match else ""
        assert match is None, (
            "POST /integrations/{service}/sync was deleted in #595 -- it fanned "
            "one org-wide credential out over every board of a type. Sync one "
            "board with POST /boards/{board_id}/sync, or one GitHub org with "
            "POST /github-registrations/{registration_id}/sync. Found: "
            f"{found!r}"
        )
        # The 501 GET stub is deliberately NOT deleted: it is tracked in
        # tests/test_unimplemented_routes_are_honest.py and the deleted POST was
        # never its data source.
        assert SERVICE_SYNC_STATUS_GET.search(text) is not None

    def test_boards_router_still_declares_the_per_board_sync(self):
        text = (ROUTERS / "boards.py").read_text()
        assert '"/organizations/{organization_id}/boards/{board_id}/sync"' in text, (
            "POST /boards/{board_id}/sync is the endpoint the deleted fan-out "
            "route's callers were sent to; every test in this file asserts "
            "against it."
        )
