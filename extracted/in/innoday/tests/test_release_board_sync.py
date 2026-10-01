"""Two-way release sync, InnoDay ⇄ Linear (PF-469).

Rules pinned here:
- Linear pairs with exactly one pipeline: scheduled, production preferred.
  None, several or a plan without Releases = "managed in InnoDay only", not an error.
- A ticket in a *managed* release (one InnoDay holds) takes that version.
- *Extra* board releases never change a ticket's InnoDay release.
- InnoDay owns the release setup: created, renamed, staged and canceled on the
  board from InnoDay. Membership syncs both ways by three-way merge.
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.adapters.base_adapter import (
    BaseBoardAdapter,
    BoardAdapterError,
    BoardCapabilityError,
    BoardRelease,
)
from src.adapters.linear_adapter import LinearBoardAdapter
from src.api.linear_api import LinearAPI, LinearAPIError
from src.domain.board import BoardRegistration, BoardType
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket
from src.services import board_sync_service as bss
from src.services.board_sync_service import BoardSyncService
from src.services.release_board_sync import (
    reconcile_from_board,
    sync_project_releases,
)

# --------------------------------------------------------------------------- #
# Linear: pairing a team with its pipeline
# --------------------------------------------------------------------------- #


def _linear_adapter(pipelines=None, releases=None, pipelines_error=None):
    api = MagicMock(spec=LinearAPI)
    if pipelines_error:
        api.get_team_release_pipelines = AsyncMock(side_effect=pipelines_error)
    else:
        api.get_team_release_pipelines = AsyncMock(return_value=pipelines or [])
    api.get_pipeline_releases = AsyncMock(return_value=releases or [])
    reg = MagicMock(spec=BoardRegistration)
    reg.board_external_id = "team-1"
    return LinearBoardAdapter(api, reg), api


def _pipeline(pid, type_="scheduled", production=False, name=None):
    return {"id": pid, "name": name or pid, "type": type_, "isProduction": production}


class TestPipelinePairing:
    @pytest.mark.asyncio
    async def test_the_one_scheduled_pipeline_is_used(self):
        adapter, _ = _linear_adapter([_pipeline("web"), _pipeline("ci", "continuous")])
        assert (await adapter.resolve_release_pipeline())["id"] == "web"

    @pytest.mark.asyncio
    async def test_production_wins_among_several(self):
        adapter, _ = _linear_adapter(
            [_pipeline("nightly"), _pipeline("prod", production=True)]
        )
        assert (await adapter.resolve_release_pipeline())["id"] == "prod"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "pipelines",
        [
            [],
            [_pipeline("ci", "continuous")],
            [_pipeline("a"), _pipeline("b")],
            [_pipeline("a", production=True), _pipeline("b", production=True)],
        ],
        ids=["none", "continuous-only", "ambiguous", "two-production"],
    )
    async def test_no_single_pipeline_means_innoday_only(self, pipelines):
        adapter, _ = _linear_adapter(pipelines)
        with pytest.raises(BoardCapabilityError):
            await adapter.list_releases()

    @pytest.mark.asyncio
    async def test_a_plan_without_releases_means_innoday_only(self):
        adapter, _ = _linear_adapter(
            pipelines_error=LinearAPIError("GraphQL errors: feature not available")
        )
        with pytest.raises(BoardCapabilityError):
            await adapter.list_releases()


class TestLinearReleasesTranslate:
    @pytest.mark.asyncio
    async def test_releases_become_board_releases(self):
        adapter, api = _linear_adapter(
            [_pipeline("web")],
            [
                {
                    "id": "r1",
                    "name": "Spring",
                    "version": "v1.4.0",
                    "stage": {"type": "started"},
                    "issues": {
                        "nodes": [{"identifier": "PF-1"}, {"identifier": "PF-2"}]
                    },
                },
                # No version: the name is what the person typed.
                {
                    "id": "r2",
                    "name": "v1.5.0",
                    "version": None,
                    "stage": {"type": "planned"},
                },
                # Neither: nothing to pair on.
                {"id": "r3", "name": "", "version": None},
            ],
        )
        releases = await adapter.list_releases()

        api.get_pipeline_releases.assert_awaited_once_with("web")
        assert releases == [
            BoardRelease("r1", "v1.4.0", "started", ["PF-1", "PF-2"]),
            BoardRelease("r2", "v1.5.0", "planned", []),
        ]


class TestLinearApiPaginatesReleaseIssues:
    """A missing page would read as "not in this release"."""

    @pytest.mark.asyncio
    async def test_issues_beyond_the_first_page_are_fetched(self):
        api = LinearAPI("key")
        first = {
            "data": {
                "releasePipeline": {
                    "releases": {
                        "nodes": [
                            {
                                "id": "r1",
                                "version": "v1",
                                "issues": {
                                    "nodes": [{"identifier": "PF-1"}],
                                    "pageInfo": {
                                        "hasNextPage": True,
                                        "endCursor": "c1",
                                    },
                                },
                            }
                        ],
                        "pageInfo": {"hasNextPage": False},
                    }
                }
            }
        }
        second = {
            "data": {
                "release": {
                    "issues": {
                        "nodes": [{"identifier": "PF-2"}],
                        "pageInfo": {"hasNextPage": False},
                    }
                }
            }
        }
        api._execute = AsyncMock(side_effect=[first, second])

        releases = await api.get_pipeline_releases("p1")

        # Linear hides archived rows unless asked, and archives on its own; a
        # hidden one would read as "deleted" or "removed from the release".
        first_query, second_query = (c.args[0] for c in api._execute.await_args_list)
        assert first_query.count("includeArchived: true") == 2
        assert "includeArchived: true" in second_query

        assert [i["identifier"] for i in releases[0]["issues"]["nodes"]] == [
            "PF-1",
            "PF-2",
        ]


class TestOtherBoardsHaveNoReleaseLineYet:
    @pytest.mark.asyncio
    async def test_the_default_refuses_as_a_capability(self):
        class Bare(BaseBoardAdapter):
            async def initialize(self, token): ...
            async def get_tickets(self, board_id, since=None): ...
            async def get_ticket(self, ticket_id): ...
            async def create_ticket(self, board_id, data): ...
            async def update_ticket(self, ticket, updates): ...
            async def update_ticket_status(self, ticket, status): ...
            async def get_board_metadata(self): ...
            async def validate_connection(self): ...

        reg = MagicMock(spec=BoardRegistration)
        reg.board_external_id = "b"
        with pytest.raises(BoardCapabilityError):
            await Bare(reg).list_releases()


class TestLinearHttpErrors:
    @pytest.mark.asyncio
    async def test_an_http_failure_is_an_error_not_innoday_only(self):
        """A 401 or a query Linear rejects must not read as "no Releases"."""
        adapter, _ = _linear_adapter(
            pipelines_error=LinearAPIError("Linear returned HTTP 401", http_status=401)
        )
        with pytest.raises(BoardAdapterError) as exc:
            await adapter.list_releases()
        assert not isinstance(exc.value, BoardCapabilityError)


class TestLinearWrites:
    """The adapter translates neutral stages and ticket keys into Linear ids."""

    def _adapter(self):
        stages = {
            "nodes": [
                {"id": "st-planned", "type": "planned", "position": 0},
                {"id": "st-started", "type": "started", "position": 1},
                {"id": "st-done", "type": "completed", "position": 2},
                {"id": "st-cancel", "type": "canceled", "position": 3},
            ]
        }
        adapter, api = _linear_adapter([{**_pipeline("web"), "stages": stages}])
        api.create_release = AsyncMock(
            return_value={"id": "r9", "version": "v1.6.0", "stage": {"type": "planned"}}
        )
        api.update_release = AsyncMock()
        api.get_issue = AsyncMock(return_value={"id": "uuid-12"})
        api.add_issue_to_release = AsyncMock()
        api.remove_issue_from_release = AsyncMock()
        return adapter, api

    @pytest.mark.asyncio
    async def test_create_uses_the_stage_id(self):
        adapter, api = self._adapter()
        created = await adapter.create_release("v1.6.0", "planned")
        api.create_release.assert_awaited_once_with("web", "v1.6.0", "st-planned")
        assert created == BoardRelease("r9", "v1.6.0", "planned")

    @pytest.mark.asyncio
    async def test_update_renames_and_moves_stage(self):
        adapter, api = self._adapter()
        await adapter.update_release("r1", version="v1.4.1", stage="completed")
        api.update_release.assert_awaited_once_with(
            "r1", {"version": "v1.4.1", "name": "v1.4.1", "stageId": "st-done"}
        )

    @pytest.mark.asyncio
    async def test_attach_resolves_the_issue_id_once(self):
        adapter, api = self._adapter()
        await adapter.add_ticket_to_release("r1", "PF-12")
        await adapter.remove_ticket_from_release("r2", "PF-12")
        api.get_issue.assert_awaited_once_with("PF-12")
        api.add_issue_to_release.assert_awaited_once_with("uuid-12", "r1")
        api.remove_issue_from_release.assert_awaited_once_with("uuid-12", "r2")


# --------------------------------------------------------------------------- #
# The shared engine, against a board that keeps real state
# --------------------------------------------------------------------------- #


class FakeBoard:
    """A board release line with real state, standing in for Linear."""

    def __init__(self):
        self.releases = {}  # id -> dict(version, stage, keys:set)
        self.fail = set()  # operation names that raise
        self._n = 0

    def add(self, version, stage="planned", keys=(), archived=False):
        self._n += 1
        rid = f"b{self._n}"
        self.releases[rid] = {"version": version, "stage": stage, "keys": set(keys)}
        if archived:
            self.releases[rid]["archived"] = True
        return rid

    def by_version(self, version):
        return next(r for r in self.releases.values() if r["version"] == version)

    async def list_releases(self):
        return [
            BoardRelease(
                rid,
                r["version"],
                r["stage"],
                sorted(r["keys"]),
                archived=r.get("archived", False),
            )
            for rid, r in self.releases.items()
        ]

    async def create_release(self, version, stage):
        if "create" in self.fail:
            raise BoardAdapterError("create refused")
        rid = self.add(version, stage)
        return BoardRelease(rid, version, stage)

    async def update_release(self, external_id, *, version=None, stage=None):
        assert not self.releases[external_id].get("archived"), "wrote to archived"
        if version is not None:
            self.releases[external_id]["version"] = version
        if stage is not None:
            self.releases[external_id]["stage"] = stage

    async def add_ticket_to_release(self, rid, key):
        if "attach" in self.fail:
            raise BoardAdapterError("attach refused")
        self.releases[rid]["keys"].add(key)

    async def remove_ticket_from_release(self, rid, key):
        self.releases[rid]["keys"].discard(key)


class NoReleases(FakeBoard):
    async def list_releases(self):
        raise BoardCapabilityError("no pipeline")


@pytest.fixture
def board(db_session, org, project):
    b = BoardRegistration(
        id=str(uuid4()),
        organization_id=org.id,
        project_id=project.id,
        board_name="PF Linear",
        board_type=BoardType.LINEAR,
        board_url="https://linear.app/x/team/PF",
        board_external_id="team-1",
    )
    db_session.add(b)
    db_session.commit()
    return b


def _release(session, project, version, status=ReleaseStatus.PLANNED):
    r = Release(
        organization_id=project.organization_id,
        project_id=project.id,
        version=version,
        status=status,
    )
    session.add(r)
    session.commit()
    return r


def _ticket(session, board, key, release=None):
    t = Ticket(
        summary=key,
        organization_id=board.organization_id,
        project_id=board.project_id,
        board_registration_id=board.id,
        external_ticket_id=key,
        release=release,
    )
    session.add(t)
    session.commit()
    return t


async def _sync(session, board, fake, project):
    result = await reconcile_from_board(session, board, fake, project.id)
    session.commit()
    return result


class TestFlowAConnect:
    @pytest.mark.asyncio
    async def test_first_connect_pairs_creates_and_unions(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.3.0", ReleaseStatus.IN_PROGRESS)
        _release(db_session, project, "v1.4.0")
        fake = FakeBoard()
        fake.add("v1.4.0", "started", ["PF-12"])  # stage differs from InnoDay's
        fake.add("hotfix-ios", "planned", ["PF-99"])  # extra
        pf12 = _ticket(db_session, board, "PF-12")
        pf13 = _ticket(db_session, board, "PF-13", release="v1.3.0")
        pf99 = _ticket(db_session, board, "PF-99", release="v1.3.0")

        result = await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.3.0")["stage"] == "started"  # created
        assert fake.by_version("v1.4.0")["stage"] == "planned"  # InnoDay's stage
        assert pf12.release == "v1.4.0"  # board member adopted
        assert "PF-13" in fake.by_version("v1.3.0")["keys"]  # InnoDay's pushed
        assert pf13.release == "v1.3.0"
        assert pf99.release == "v1.3.0"  # an extra never changes InnoDay
        assert fake.by_version("hotfix-ios") == {
            "version": "hotfix-ios",
            "stage": "planned",
            "keys": {"PF-99"},
        }, "an extra is never touched"
        assert result["extra_releases"] == ["hotfix-ios"]
        assert result["releases_created"] == 1
        assert len(db_session.exec(select(Release)).all()) == 2, "none invented"

    @pytest.mark.asyncio
    async def test_the_board_wins_on_first_connect(self, db_session, board, project):
        _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        fake.add("v1.4.0", "started", ["PF-1"])
        fake.add("v1.5.0", "planned")
        t = _ticket(db_session, board, "PF-1", release="v1.5.0")  # e.g. a stale label

        await _sync(db_session, board, fake, project)

        assert t.release == "v1.4.0"
        assert fake.by_version("v1.4.0")["keys"] == {"PF-1"}
        assert fake.by_version("v1.5.0")["keys"] == set()


class TestFlowsBCStages:
    @pytest.mark.asyncio
    async def test_start_and_ship_move_the_board_stage(
        self, db_session, board, project
    ):
        v14 = _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        v15 = _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)

        # Ship v1.4.0: the pipeline rotates v1.5.0 in and opens v1.6.0.
        v14.status = ReleaseStatus.RELEASED
        v15.status = ReleaseStatus.IN_PROGRESS
        db_session.add_all([v14, v15])
        _release(db_session, project, "v1.6.0")
        await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.4.0")["stage"] == "completed"
        assert fake.by_version("v1.5.0")["stage"] == "started"
        assert fake.by_version("v1.6.0")["stage"] == "planned"

    @pytest.mark.asyncio
    async def test_a_board_side_stage_change_is_put_back(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        fake.by_version("v1.5.0")["stage"] = "completed"

        await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.5.0")["stage"] == "planned"

    @pytest.mark.asyncio
    async def test_a_rename_in_innoday_renames_the_same_board_release(
        self, db_session, board, project
    ):
        r = _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        r.version = "v1.5.1"
        db_session.add(r)

        await _sync(db_session, board, fake, project)

        assert [x["version"] for x in fake.releases.values()] == ["v1.5.1"]

    @pytest.mark.asyncio
    async def test_a_withdrawn_release_is_canceled_on_the_board(
        self, db_session, board, project
    ):
        r = _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        from datetime import datetime

        r.deleted_at = datetime(2026, 9, 29)  # withdrawn in InnoDay
        db_session.add(r)

        result = await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.5.0")["stage"] == "canceled"
        assert result["releases_canceled"] == 1

    @pytest.mark.asyncio
    async def test_housekeeping_archive_does_not_cancel(
        self, db_session, board, project
    ):
        r = _release(db_session, project, "v1.7.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        r.status = ReleaseStatus.ARCHIVED  # release planning's own tidy-up
        db_session.add(r)

        result = await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.7.0")["stage"] == "planned"
        assert result["releases_canceled"] == 0

    @pytest.mark.asyncio
    async def test_withdrawing_a_shipped_release_leaves_it_completed(
        self, db_session, board, project
    ):
        from datetime import datetime

        r = _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        r.status = ReleaseStatus.RELEASED
        db_session.add(r)
        await _sync(db_session, board, fake, project)
        r.deleted_at = datetime(2026, 9, 29)
        db_session.add(r)

        await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.4.0")["stage"] == "completed"


class TestFlowDBoardAttaches:
    @pytest.mark.asyncio
    async def test_added_moved_and_removed_on_the_board(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        _release(db_session, project, "v1.5.0")
        a = _ticket(db_session, board, "PF-1", release="v1.4.0")
        b = _ticket(db_session, board, "PF-2", release="v1.4.0")
        c = _ticket(db_session, board, "PF-3")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)  # baseline: PF-1, PF-2 pushed

        v14 = fake.by_version("v1.4.0")["keys"]
        v15 = fake.by_version("v1.5.0")["keys"]
        v14.discard("PF-1")
        v15.add("PF-1")  # moved on the board
        v14.discard("PF-2")  # removed on the board
        v15.add("PF-3")  # added on the board

        result = await _sync(db_session, board, fake, project)

        assert (a.release, b.release, c.release) == ("v1.5.0", None, "v1.5.0")
        assert result["tickets_attached"] == 2
        assert result["tickets_cleared"] == 1


class TestFlowEInnodayAttaches:
    @pytest.mark.asyncio
    async def test_innoday_move_is_pushed_not_reverted(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        _release(db_session, project, "v1.5.0")
        t = _ticket(db_session, board, "PF-1", release="v1.4.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)

        t.release = "v1.5.0"  # planned elsewhere in InnoDay
        db_session.add(t)
        await _sync(db_session, board, fake, project)

        assert t.release == "v1.5.0"
        assert fake.by_version("v1.4.0")["keys"] == set()
        assert fake.by_version("v1.5.0")["keys"] == {"PF-1"}

    @pytest.mark.asyncio
    async def test_innoday_clear_detaches_on_the_board(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        t = _ticket(db_session, board, "PF-1", release="v1.4.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)

        t.release = None  # back to the backlog
        db_session.add(t)
        await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.4.0")["keys"] == set()

    @pytest.mark.asyncio
    async def test_a_failed_push_is_retried_not_reverted(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        t = _ticket(db_session, board, "PF-1", release="v1.4.0")
        fake = FakeBoard()
        fake.fail.add("attach")

        first = await _sync(db_session, board, fake, project)
        assert first["status"] == "partial" and first["errors"]
        assert t.release == "v1.4.0", "the board refusing is not the board removing"

        fake.fail.clear()
        await _sync(db_session, board, fake, project)
        assert fake.by_version("v1.4.0")["keys"] == {"PF-1"}

    @pytest.mark.asyncio
    async def test_the_pick_does_not_depend_on_board_order(
        self, db_session, board, project
    ):
        for v, st in [
            ("v1.4.0", ReleaseStatus.RELEASED),
            ("v1.5.0", None),
            ("v1.6.0", None),
        ]:
            _release(db_session, project, v, st or ReleaseStatus.PLANNED)
        t = _ticket(db_session, board, "PF-1")
        fake = FakeBoard()
        fake.add("v1.6.0", "planned", ["PF-1"])
        fake.add("v1.4.0", "completed", ["PF-1"])
        fake.add("v1.5.0", "planned", ["PF-1"])

        await _sync(db_session, board, fake, project)

        assert t.release == "v1.5.0"


class TestFlowFBoardAddsAndDeletes:
    @pytest.mark.asyncio
    async def test_a_deleted_managed_release_is_recreated_with_its_tickets(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.5.0")
        t = _ticket(db_session, board, "PF-1", release="v1.5.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        rid = next(iter(fake.releases))
        del fake.releases[rid]  # deleted on the board

        result = await _sync(db_session, board, fake, project)

        assert result["releases_created"] == 1
        assert fake.by_version("v1.5.0")["keys"] == {"PF-1"}
        assert t.release == "v1.5.0"

    @pytest.mark.asyncio
    async def test_extras_added_or_deleted_are_ignored(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        extra = fake.add("v2.0.0", "planned", [])
        result = await _sync(db_session, board, fake, project)
        assert result["extra_releases"] == ["v2.0.0"]
        del fake.releases[extra]
        await _sync(db_session, board, fake, project)
        assert len(db_session.exec(select(Release)).all()) == 1


class TestFlowGNoReleaseFeature:
    @pytest.mark.asyncio
    async def test_no_release_line_is_innoday_only(self, db_session, board, project):
        _release(db_session, project, "v1.5.0")
        t = _ticket(db_session, board, "PF-1", release="v1.5.0")

        result = await _sync(db_session, board, NoReleases(), project)

        assert result["status"] == "innoday_only"
        assert result["message"] == "releases managed in InnoDay only"
        assert t.release == "v1.5.0"


# --------------------------------------------------------------------------- #
# Wired into board sync, and into InnoDay's own writes
# --------------------------------------------------------------------------- #


def _history(session, board):
    from src.domain.board import BoardSyncHistory, SyncStatus

    h = BoardSyncHistory(board_registration_id=board.id, sync_status=SyncStatus.PENDING)
    session.add(h)
    session.commit()
    session.refresh(h)
    return h


def _sync_adapter(fake, tickets):
    fake.initialize = AsyncMock(return_value=None)
    fake.get_tickets = AsyncMock(return_value=tickets)
    return fake


class TestBoardSync:
    @pytest.mark.asyncio
    async def test_sync_attaches_and_reports(
        self, db_engine, db_session, board, project, monkeypatch
    ):
        monkeypatch.setattr(bss, "engine", db_engine)
        _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        history = _history(db_session, board)
        fake = FakeBoard()
        fake.add("v1.4.0", "started", ["PF-7"])
        source = [
            Ticket(
                summary="s",
                organization_id=board.organization_id,
                external_ticket_id="PF-7",
            )
        ]
        service = BoardSyncService()
        monkeypatch.setattr(
            service, "_get_adapter", AsyncMock(return_value=_sync_adapter(fake, source))
        )

        result = await service.sync_board_tickets(board.id, history.id, token="tok")

        assert result["releases"]["tickets_attached"] == 1
        with Session(db_engine) as check:
            ticket = check.exec(
                select(Ticket).where(Ticket.external_ticket_id == "PF-7")
            ).one()
            release = check.exec(select(Release)).one()
        assert ticket.release == "v1.4.0"
        assert release.board_ticket_keys == ["PF-7"], "snapshot persisted"

    @pytest.mark.asyncio
    async def test_a_failure_after_a_partial_write_keeps_the_tickets(
        self, db_engine, db_session, board, project, monkeypatch
    ):
        """The release pass fails half-way: its write is undone, tickets are kept."""
        monkeypatch.setattr(bss, "engine", db_engine)
        history = _history(db_session, board)

        async def half_then_fail(session, registration, adapter, project_id):
            row = session.exec(
                select(Ticket).where(Ticket.external_ticket_id == "PF-9")
            ).one()
            row.release = "half-written"
            session.add(row)
            session.flush()
            raise RuntimeError("Linear hiccup")

        monkeypatch.setattr(bss, "reconcile_from_board", half_then_fail)
        source = [
            Ticket(
                summary="s",
                organization_id=board.organization_id,
                external_ticket_id="PF-9",
            )
        ]
        service = BoardSyncService()
        monkeypatch.setattr(
            service,
            "_get_adapter",
            AsyncMock(return_value=_sync_adapter(FakeBoard(), source)),
        )

        result = await service.sync_board_tickets(board.id, history.id, token="tok")

        assert result["tickets_created"] == 1
        assert result["releases"]["status"] == "error"
        with Session(db_engine) as check:
            ticket = check.exec(
                select(Ticket).where(Ticket.external_ticket_id == "PF-9")
            ).one()
        assert ticket.release is None, "the failed pass's write was rolled back"


class TestInnodayWritesPushNow:
    """`sync_project_releases` is what the release and ticket routes call."""

    @pytest.mark.asyncio
    async def test_it_builds_the_adapter_and_reconciles(
        self, db_session, board, project, monkeypatch
    ):
        from src.services import board_adapter_factory as factory

        paired = _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        paired.board_release_id = fake.add("v1.4.0", "started")
        db_session.add(paired)
        db_session.commit()
        fake.initialize = AsyncMock()
        monkeypatch.setattr(factory, "resolve_board_token", lambda *a, **k: "tok")
        monkeypatch.setattr(
            factory, "build_board_adapter", AsyncMock(return_value=fake)
        )

        result = await sync_project_releases(db_session, project.id)

        assert result["releases_created"] == 1
        fake.initialize.assert_awaited_once_with("tok")
        assert fake.by_version("v1.5.0")["stage"] == "planned"

    @pytest.mark.asyncio
    async def test_no_board_is_a_no_op(self, db_session, project):
        assert await sync_project_releases(db_session, project.id) is None

    @pytest.mark.asyncio
    async def test_a_credential_failure_never_raises(
        self, db_session, board, project, monkeypatch
    ):
        from src.services import board_adapter_factory as factory

        def boom(*a, **k):
            raise RuntimeError("vault unreachable")

        r = _release(db_session, project, "v1.5.0")
        r.board_release_id = "b1"
        db_session.add(r)
        db_session.commit()
        monkeypatch.setattr(factory, "resolve_board_token", boom)
        result = await sync_project_releases(db_session, project.id)
        assert result["status"] == "error"
        db_session.exec(select(Release)).all()  # session still usable

    def test_the_routes_call_it(self):
        """Every InnoDay write that changes a release or a ticket's release."""
        import inspect

        from src.routers import releases, tickets

        for fn in (
            releases.create_release,
            releases.update_release,
            releases.delete_release,
        ):
            assert "sync_project_releases" in inspect.getsource(fn), fn.__name__
        for fn in (
            tickets.update_ticket,
            tickets.update_ticket_by_id,
            tickets.create_ticket_by_id,
        ):
            assert "sync_project_releases" in inspect.getsource(fn), fn.__name__


# --------------------------------------------------------------------------- #
# Review round 2
# --------------------------------------------------------------------------- #


class TestShippedReleasesAreHistory:
    @pytest.mark.asyncio
    async def test_an_archived_issue_in_a_shipped_release_is_not_cleared(
        self, db_session, board, project
    ):
        v14 = _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        t = _ticket(db_session, board, "PF-12", release="v1.4.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        v14.status = ReleaseStatus.RELEASED
        db_session.add(v14)
        await _sync(db_session, board, fake, project)
        fake.by_version("v1.4.0")["keys"].discard("PF-12")  # Linear archived it

        await _sync(db_session, board, fake, project)

        assert t.release == "v1.4.0"

    @pytest.mark.asyncio
    async def test_rollover_after_ship_does_not_unship_tickets(
        self, db_session, board, project
    ):
        v14 = _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        v15 = _release(db_session, project, "v1.5.0")
        t = _ticket(db_session, board, "PF-1", release="v1.4.0")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        v14.status, v15.status = ReleaseStatus.RELEASED, ReleaseStatus.IN_PROGRESS
        db_session.add_all([v14, v15])
        await _sync(db_session, board, fake, project)
        # Linear's "move open issues to next release" on completion:
        fake.by_version("v1.4.0")["keys"].discard("PF-1")
        fake.by_version("v1.5.0")["keys"].add("PF-1")

        await _sync(db_session, board, fake, project)

        assert t.release == "v1.4.0"

    @pytest.mark.asyncio
    async def test_old_shipped_releases_are_not_created_on_connect(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.0.0", ReleaseStatus.RELEASED)
        _release(db_session, project, "v1.1.0")
        fake = FakeBoard()

        await _sync(db_session, board, fake, project)

        assert [r["version"] for r in fake.releases.values()] == ["v1.1.0"]

    @pytest.mark.asyncio
    async def test_an_archived_board_release_is_neither_recreated_nor_written(
        self, db_session, board, project
    ):
        v14 = _release(db_session, project, "v1.4.0", ReleaseStatus.RELEASED)
        fake = FakeBoard()
        v14.board_release_id = fake.add("v1.4.0", "planned", archived=True)
        db_session.add(v14)

        result = await _sync(db_session, board, fake, project)

        assert len(fake.releases) == 1
        assert result["releases_updated"] == 0


class TestTheNewerIntentWins:
    @pytest.mark.asyncio
    async def test_a_persons_write_beats_an_unsynced_board_change(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.4.0", ReleaseStatus.IN_PROGRESS)
        _release(db_session, project, "v1.5.0")
        t = _ticket(db_session, board, "PF-12")
        fake = FakeBoard()
        await _sync(db_session, board, fake, project)
        fake.by_version("v1.4.0")["keys"].add("PF-12")  # in Linear, not yet synced
        t.release = "v1.5.0"  # a PATCH in InnoDay
        db_session.add(t)

        await reconcile_from_board(
            db_session, board, fake, project.id, innoday_wins={"PF-12"}
        )

        assert t.release == "v1.5.0"
        assert fake.by_version("v1.4.0")["keys"] == set()
        assert fake.by_version("v1.5.0")["keys"] == {"PF-12"}


class TestPairingDetails:
    @pytest.mark.asyncio
    async def test_1_5_0_on_the_board_pairs_with_v1_5_0(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        fake.add("1.5.0", "planned")

        result = await _sync(db_session, board, fake, project)

        assert result["releases_created"] == 0
        assert [r["version"] for r in fake.releases.values()] == ["1.5.0"]

    @pytest.mark.asyncio
    async def test_a_ticket_in_another_project_is_untouched(
        self, db_session, board, project, org
    ):
        from src.domain.project import Project

        other = Project(
            id=str(uuid4()),
            organization_id=org.id,
            name="Other",
            alias="OT",
            description="other",
        )
        db_session.add(other)
        db_session.commit()
        _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        fake.add("v1.5.0", "planned", ["PF-1"])
        t = _ticket(db_session, board, "PF-1")
        t.project_id = other.id
        db_session.add(t)
        db_session.commit()

        await _sync(db_session, board, fake, project)

        assert t.release is None


class TestCheapOnOtherBoards:
    @pytest.mark.asyncio
    async def test_a_jira_board_is_skipped_before_any_credential_work(
        self, db_session, board, project, monkeypatch
    ):
        from src.services import board_adapter_factory as factory

        board.board_type = BoardType.JIRA
        db_session.add(board)
        r = _release(db_session, project, "v1.5.0")
        r.board_release_id = "x"
        db_session.add(r)
        db_session.commit()
        called = MagicMock(side_effect=AssertionError("resolved a credential"))
        monkeypatch.setattr(factory, "resolve_board_token", called)

        assert await sync_project_releases(db_session, project.id) is None

    @pytest.mark.asyncio
    async def test_the_first_reconcile_waits_for_board_sync(
        self, db_session, board, project, monkeypatch
    ):
        from src.services import board_adapter_factory as factory

        _release(db_session, project, "v1.5.0")  # never paired
        called = MagicMock(side_effect=AssertionError("ran inside a request"))
        monkeypatch.setattr(factory, "resolve_board_token", called)

        assert await sync_project_releases(db_session, project.id) is None


class TestLinearLabelsYieldToThePipeline:
    def _issue(self):
        return {
            "id": "i1",
            "identifier": "PF-1",
            "title": "t",
            "state": {"name": "Todo"},
            "labels": {"nodes": [{"name": "v1.4.0"}]},
        }

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "pipelines,expected",
        [([_pipeline("web")], None), ([], "v1.4.0")],
        ids=["pipeline", "no-pipeline"],
    )
    async def test_labels_count_only_without_a_pipeline(self, pipelines, expected):
        adapter, api = _linear_adapter(pipelines)
        reg = adapter.board_registration
        reg.organization_id, reg.project_id, reg.id = "o", "p", "r"
        api.get_team_issues = AsyncMock(return_value=[self._issue()])
        assert (await adapter.get_tickets("team-1"))[0].release == expected

    @pytest.mark.asyncio
    async def test_a_missing_stage_is_skipped_not_failed(self):
        adapter, api = _linear_adapter([{**_pipeline("web"), "stages": {"nodes": []}}])
        api.update_release = AsyncMock()
        await adapter.update_release("r1", stage="started")
        api.update_release.assert_not_awaited()


# --------------------------------------------------------------------------- #
# Review round 3
# --------------------------------------------------------------------------- #


class TestRoundThree:
    @pytest.mark.asyncio
    async def test_a_shared_pipeline_means_innoday_only(self):
        shared = {
            **_pipeline("web"),
            "teams": {"nodes": [{"id": "team-1"}, {"id": "t2"}]},
        }
        adapter, _ = _linear_adapter([shared])
        with pytest.raises(BoardCapabilityError):
            await adapter.list_releases()

    @pytest.mark.asyncio
    async def test_a_pipeline_of_this_team_only_is_used(self):
        own = {**_pipeline("web"), "teams": {"nodes": [{"id": "team-1"}]}}
        adapter, _ = _linear_adapter([own])
        assert (await adapter.resolve_release_pipeline())["id"] == "web"

    @pytest.mark.asyncio
    async def test_a_pipeline_hiccup_drops_labels_and_never_fails_the_sync(self):
        import httpx

        adapter, api = _linear_adapter(pipelines_error=httpx.ReadTimeout("slow"))
        reg = adapter.board_registration
        reg.organization_id, reg.project_id, reg.id = "o", "p", "r"
        api.get_team_issues = AsyncMock(
            return_value=[
                {
                    "id": "i1",
                    "identifier": "PF-1",
                    "title": "t",
                    "state": {"name": "Todo"},
                    "labels": {"nodes": [{"name": "v1.4.0"}]},
                }
            ]
        )
        tickets = await adapter.get_tickets("team-1")
        assert tickets[0].release is None

    @pytest.mark.asyncio
    async def test_old_shipped_releases_keep_their_board_stage(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.0.0", ReleaseStatus.RELEASED)
        fake = FakeBoard()
        fake.add("v1.0.0", "started")  # Linear never completed it

        result = await _sync(db_session, board, fake, project)

        assert fake.by_version("v1.0.0")["stage"] == "started"
        assert result["releases_updated"] == 0

    @pytest.mark.asyncio
    async def test_an_empty_board_stage_is_not_updated_every_sync(
        self, db_session, board, project
    ):
        _release(db_session, project, "v1.5.0")
        fake = FakeBoard()
        fake.add("v1.5.0", "")

        result = await _sync(db_session, board, fake, project)

        assert result["releases_updated"] == 0

    @pytest.mark.asyncio
    async def test_id_pairing_is_never_stolen_by_a_version_match(
        self, db_session, board, project
    ):
        a = _release(db_session, project, "v1.5.0")
        b = _release(db_session, project, "v1.6.0")
        fake = FakeBoard()
        rid = fake.add("v1.5.0", "planned")  # renamed in Linear; owned by b
        b.board_release_id = rid
        db_session.add(b)

        await _sync(db_session, board, fake, project)

        assert fake.releases[rid]["version"] == "v1.6.0"
        assert a.board_release_id and a.board_release_id != rid

    def test_only_a_v_before_a_digit_is_dropped(self):
        from src.services.release_board_sync import _same_version

        assert _same_version("v1.5.0", "1.5.0")
        assert not _same_version("vNext", "Next")
        assert not _same_version("Venus", "enus")
