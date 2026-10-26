"""`entity view=branches`, `browse mode=branches`, and the CLI and SDK reads
behind them (swarm visibility PR4b, D6, T20, T24).

On the swarm fixture's real reads: `fixtures/branches_swarm.json` holds what
`GET /v1/workspaces/{W}/branches`, `/v1/projects/{P1}/branches` and
`/v1/projects/{P1}/experiments/{I1b}/branch` answered for
`tests/fixtures/branches_swarm.py` (8 branches, 5 projects).
`tests/integration/test_branches_agent_view.py` holds it to the live shape and
rewrites it with `BRANCHES_SWARM_SNAPSHOT=<path>`.

Sizes are measured where an agent meets them: the real MCP boundary (`_wire`)
and the repo tokenizer, at the default budget.
"""

from __future__ import annotations

import copy
import importlib
import json
import re
from pathlib import Path

import anyio
import httpx
import pytest

from probe import cli
from probe.mcp import accounting
from probe.mcp.budget import count_tokens
from probe.mcp.contract import MissingMarker
from probe.mcp.service import ResearchReadService
from probe.sdk import errors
from test_mcp_delivery import _wire
from tests.conftest import make_client

cli_main = importlib.import_module("probe.cli.main")

SNAP = json.loads((Path(__file__).parent / "fixtures" / "branches_swarm.json").read_text())
NAME = SNAP["names"]
ID = {name: ident for ident, name in NAME.items()}
WORKSPACE = NAME["workspace"]
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")

#: D6's bounds (T24): the 8-branch compact read and one branch in full.
COMPACT_TOKENS = 2_000
DETAIL_TOKENS = 3_000


def _slug(name: str) -> str:
    for body in (SNAP["workspace"], SNAP["project"]):
        for branch in body["branches"]:
            for row in branch["experiments"]:
                if row["id"] == ID[name]:
                    return f"experiment:{row['slug']}"
    raise KeyError(name)


class _Source:
    """The three branches reads, answered from the snapshot; P1 and I1b as
    the entities `entity` opens."""

    def __init__(self, **bodies: dict) -> None:
        self.calls: list[tuple] = []
        self.created: dict | None = {"project_ids": [], "run_ids": []}
        self.bodies = {key: bodies.get(key) or SNAP[key] for key in ("project", "experiment", "workspace")}

    def identity(self) -> dict:
        return {"customer_id": "lab-42"}

    def capabilities(self) -> dict:
        return {}

    def get(self, ref: str) -> tuple[str, dict]:
        kind = ref.partition(":")[0]
        if kind == "project":
            return "project", {"id": ID["P1"], "slug": "p1", "name": "P1"}
        if kind == "experiment":
            return "experiment", {"id": ID["I1b"], "slug": "i1b", "name": "I1b", "project_id": ID["P1"]}
        raise errors.NotFoundError(f"{ref} not found")

    def project_branches(self, project_id: str) -> dict:
        self.calls.append(("project", project_id))
        return copy.deepcopy(self.bodies["project"])

    def experiment_branch(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        self.calls.append(("experiment", experiment_id, project_id))
        return copy.deepcopy(self.bodies["experiment"])

    def workspace_branches(self, workspace_id: str) -> dict:
        self.calls.append(("workspace", workspace_id))
        return copy.deepcopy(self.bodies["workspace"])

    def session_created(self, session_id: str) -> dict | None:
        return self.created


def _delivered(result: dict, limit: int) -> tuple[dict, int]:
    assert not result.get("isError"), result
    [block] = result["content"]
    text = block["text"]
    tokens = count_tokens(text)
    assert tokens <= limit and len(text.encode()) <= 8 * limit
    return json.loads(text), tokens


def _rows(data: dict) -> dict[str, dict]:
    return {row["name"]: row for row in data["branches"]}


# -- the compact tier ----------------------------------------------------------


def test_one_workspace_call_answers_the_swarm_within_the_default_budget():
    """T24: the 8-branch compact read, through the real boundary and the repo
    tokenizer, fits the default 2,000 tokens whole: no cursor, nothing cut."""
    source = _Source()
    out, tokens = _delivered(
        _wire(ResearchReadService(source), "browse", {"mode": "branches", "workspace_id": WORKSPACE}),
        COMPACT_TOKENS,
    )
    print(f"compact workspace read (8 branches): {tokens} tokens")
    assert "next_cursor" not in out and "completeness" not in out
    data = out["data"]
    assert source.calls == [("workspace", WORKSPACE)]
    rows = _rows(data)
    assert sorted(rows) == ["B0", "I1", "I2", "J1", "K1", "L1", "M1", "M3"]
    # Q1: leader, runner-up and gap on the one metric; the person's pick apart.
    assert data["metric"] == {"key": "test/acc", "goal": "max", "reduce": "final"}
    assert data["leader"] == {
        "branch": _slug("I1"), "name": "I1", "experiment": _slug("I1b"), "value": 0.91,
    }
    assert data["runner_up"]["branch"] == _slug("J1") and data["gap"] == {"abs": 0.01, "pct": 1.11}
    assert data["pick"] == {
        "experiment": _slug("J1"), "name": "J1", "source": "human",
        "reason": "J1 is cheaper and within 0.01 of the leader.",
    }
    assert data["workspace"] == {"id": WORKSPACE, "name": SNAP["workspace"]["scope"]["name"]}
    ranked = sorted((r for r in rows.values() if "rank" in r), key=lambda r: r["rank"])
    assert [r["name"] for r in ranked] == ["I1", "J1", "K1", "I2", "M1", "B0", "L1"]
    # Q2: effort; an unknown cost is null, never 0.
    assert rows["I1"]["effort"] == {
        "span": [rows["I1"]["effort"]["span"][0], rows["I1"]["last_active_at"]],
        "busy_h": 2.0, "run_h": 2.0, "agent_h": 2.0, "cost_usd": 4.2, "cost_estimated": True,
    }
    assert rows["J1"]["effort"]["cost_usd"] is None
    assert data["elsewhere_agent_h"] == 1.0
    # Q3-Q7 at a glance: overlap, links, state, gain, who.
    assert rows["I1"]["overlaps_top"] == {"ref": _slug("L1"), "hours": 2.0}
    assert rows["B0"]["used_by_total"] == 3
    assert {n: r["state"] for n, r in rows.items()} == {
        "I2": "live", "L1": "stopped", "M1": "concluded", "M3": "idle",
        "I1": "active", "J1": "active", "B0": "active", "K1": "active",
    }
    assert rows["I1"]["gain"] == {"agent_h_since_best": 0.0, "last_delta": 0.06}
    assert all("gain" in rows[r["name"]] for r in ranked)
    assert rows["I1"]["harnesses"] == "claude_code 1" and rows["I2"]["harnesses"] == "codex 1"
    assert "sessions_total" not in rows["M3"] and "best" not in rows["M3"]
    # Slug refs: no row names a uuid.
    assert not _UUID.search(json.dumps(data["branches"]))


def test_the_compact_row_golden():
    """One row, whole: D6's compact field list and nothing else."""
    out = ResearchReadService(_Source()).browse_list("branches", workspace_id=WORKSPACE)
    i1 = _rows(out["data"])["I1"]
    assert i1 == {
        "ref": _slug("I1"),
        "name": "I1",
        "experiments_total": 2,
        "best": {"value": 0.91, "experiment": _slug("I1b")},
        "rank": 1,
        "effort": {
            "span": ["2026-10-25T18:45Z", "2026-10-25T21:45Z"],
            "busy_h": 2.0, "run_h": 2.0, "agent_h": 2.0, "cost_usd": 4.2, "cost_estimated": True,
        },
        "state": "active",
        "last_active_at": "2026-10-25T21:45Z",
        "gain": {"agent_h_since_best": 0.0, "last_delta": 0.06},
        "overlaps_top": {"ref": _slug("L1"), "hours": 2.0},
        "used_by_total": 1,
        "sessions_total": 1,
        "harnesses": "claude_code 1",
    }
    assert _rows(out["data"])["J1"]["behind_leader"] == {"abs": 0.01, "pct": 1.1}


def test_a_project_read_is_its_tree_and_an_experiment_read_is_its_line():
    source = _Source()
    service = ResearchReadService(source)
    project = service.get_entity(f"project:{ID['P1']}", view="branches")["data"]
    assert source.calls == [("project", ID["P1"])]
    assert [r["name"] for r in project["branches"]] == ["B0", "I1", "I2"]
    assert project["leader"]["branch"] == _slug("I1") and project["runner_up"]["branch"] == _slug("I2")
    assert "focus" not in project
    line = service.get_entity(f"experiment:{ID['I1b']}", view="branches")["data"]
    assert source.calls[-1] == ("experiment", ID["I1b"], ID["P1"])
    assert line["focus"] == _slug("I1")
    assert [r["name"] for r in line["branches"]] == ["B0", "I1"]


def test_a_small_budget_pages_whole_branches_and_sends_each_once():
    """Past the budget the read pages by cursor and says so; every branch
    arrives once, whole, on both surfaces."""
    service = ResearchReadService(_Source())
    for tool, args in (
        ("browse", {"mode": "branches", "workspace_id": WORKSPACE}),
        ("entity", {"refs": [f"project:{ID['P1']}"], "view": "branches"}),
    ):
        seen, cursor, pages = [], None, 0
        while True:
            call = {**args, "token_budget": 600, **({"cursor": cursor} if cursor else {})}
            out, _ = _delivered(_wire(service, tool, call), 600)
            assert out["data"].get("format") is None, "a page is whole rows, never a fragment"
            seen += [row["ref"] for row in out["data"]["branches"]]
            pages += 1
            cursor = out.get("next_cursor")
            if not cursor:
                break
            assert "truncated_by_token_budget" in out["completeness"]["missing"]
        assert pages > 1 and len(seen) == len(set(seen))
        assert len(seen) == (8 if tool == "browse" else 3)


# -- the detail tier -------------------------------------------------------------


def test_one_branch_in_full_fits_its_bound_with_each_experiments_effort():
    source = _Source()
    out, tokens = _delivered(
        _wire(
            ResearchReadService(source),
            "entity",
            {"refs": [f"project:{ID['P1']}"], "view": "branches", "view_options": {"branch": _slug("I1")}},
        ),
        DETAIL_TOKENS,
    )
    print(f"one branch in full (I1): {tokens} tokens")
    data = out["data"]
    assert "branches" not in data and data["leader"]["branch"] == _slug("I1")
    branch = data["branch"]
    assert branch["ref"] == _slug("I1") and branch["split_from"] == _slug("B0")
    assert branch["best"]["run"].startswith("run:") and branch["best"]["value"] == 0.91
    assert branch["climb"] == [
        {"at": "2026-10-25T20:45Z", "agent_h": 1.0, "best": 0.85},
        {"at": "2026-10-25T21:45Z", "agent_h": 2.0, "best": 0.91},
    ]
    [session] = branch["sessions"]
    assert session["session"] == "session:claude_code/5f0c1d2e-0001-4a10-9f3e-000000000001"
    assert branch["built_on"] == [{"ref": _slug("B0"), "name": "B0", "relation": "forked_from"}]
    # L1 is outside P1's tree: the read names no slug for it, so its id.
    assert branch["used_by"] == [{"ref": f"experiment:{ID['L1']}", "name": "L1", "relation": "informed_by"}]
    assert [(e["name"], e["effort"]) for e in data["experiments"]] == [
        ("I1", {"busy_h": 1.0, "run_h": 1.0, "agent_h": 1.0}),
        ("I1b", {"busy_h": 1.0, "run_h": 1.0, "agent_h": 1.0}),
    ]
    i1b = data["experiments"][1]
    assert i1b == {
        "ref": _slug("I1b"), "name": "I1b", "parent": _slug("I1"), "relation": "derived_from",
        "created_at": "2026-10-25T20:39Z", "value": 0.91, "run": i1b["run"],
        "effort": {"busy_h": 1.0, "run_h": 1.0, "agent_h": 1.0},
    }
    assert data["metric_source"] == "human"
    # The same branch opened from the workspace page fits the same bound.
    out, tokens = _delivered(
        _wire(
            ResearchReadService(_Source()),
            "browse",
            {"mode": "branches", "workspace_id": WORKSPACE, "branch": _slug("I1")},
        ),
        DETAIL_TOKENS,
    )
    print(f"one branch in full from the workspace read (I1): {tokens} tokens")
    assert out["data"]["branch"]["ref"] == _slug("I1") and len(out["data"]["experiments"]) == 2


@pytest.mark.parametrize("form", ["ref", "slug", "uuid"])
def test_the_branch_option_takes_the_ref_its_slug_or_its_id(form):
    ref = _slug("I1")
    wanted = {"ref": ref, "slug": ref.partition(":")[2], "uuid": ID["I1"]}[form]
    data = ResearchReadService(_Source()).get_entity(
        f"project:{ID['P1']}", view="branches", filters={"branch": wanted}
    )["data"]
    assert data["branch"]["ref"] == ref


def test_a_branch_option_that_names_no_branch_here_is_refused_with_those_that_do():
    service = ResearchReadService(_Source())
    with pytest.raises(errors.ValidationError) as caught:
        # I1b is IN a branch, not the start of one.
        service.get_entity(f"project:{ID['P1']}", view="branches", filters={"branch": _slug("I1b")})
    message = str(caught.value)
    assert all(_slug(name) in message for name in ("B0", "I1", "I2"))
    with pytest.raises(errors.ValidationError, match="supported view options.*branch"):
        service.get_entity(f"project:{ID['P1']}", view="branches", filters={"grep": "x"})
    with pytest.raises(errors.ValidationError, match="ref"):
        service.get_entity(f"project:{ID['P1']}", view="branches", filters={"branch": 3})


# -- browse ------------------------------------------------------------------------


def test_browse_branches_needs_a_workspace_and_reads_nothing_else():
    service = ResearchReadService(_Source())
    with pytest.raises(errors.ValidationError, match="workspace_id"):
        service.browse_list("branches")
    with pytest.raises(errors.ValidationError, match="UUID"):
        service.browse_list("branches", workspace_id="team")
    for extra in ({"limit": 5}, {"ref": f"project:{ID['P1']}"}, {"query": "x"}):
        result = _wire(service, "browse", {"mode": "branches", "workspace_id": WORKSPACE, **extra})
        assert result.get("isError") and "mode=branches does not read" in result["content"][0]["text"]


def test_hidden_session_work_is_said_never_silently_left_in():
    """The daemon reader hides its own session's work; a branch is an
    aggregate that cannot take it out, so the read says so, once."""
    source = _Source()
    service = ResearchReadService(source)
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(accounting, "session_work_to_hide", lambda: "11111111-2222-3333-4444-555555555555")
        for created in ({"project_ids": [], "run_ids": []}, None):
            source.created = created
            entity = service.get_entity(f"project:{ID['P1']}", view="branches")
            assert entity["completeness"]["missing"] == [MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED]
        listed = service.browse_list("branches", workspace_id=WORKSPACE)
        assert listed["completeness"]["missing"] == [MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED]


# -- review fixes: scope, metric groups, bounded pages, exact and short refs ------

_T0 = "2026-10-25T10:00:00Z"


def _uuid(n: int) -> str:
    return f"00000000-0000-4000-8000-{n:012d}"


def _member(n: int, slug: str, *, project: str = "p1", metric: tuple | None = None) -> dict:
    """One experiment of a branch, as the server lists it."""
    return {
        "id": _uuid(n), "slug": slug, "name": slug.strip() or "x", "project_id": _uuid(900 + int(project[1:])),
        "parent": None, "relation": None, "created_at": _T0,
        "metric": None if metric is None else dict(zip(("key", "goal", "reduce"), metric)),
        "value": None, "superseded": False, "conclusion": None,
        "effort": {"busy_h": 1.0, "run_h": 1.0, "agent_h": 1.0},
    }


def _line(n: int, members: list[dict], *, metric: tuple = ("test/acc", "max", "final"),
          rank: int | None = 1, of: int | None = 1, span_end: str = "2026-10-25T11:00:00Z") -> dict:
    """One branch, as the server answers it, rooted at `members[0]`."""
    root = members[0]
    return {
        "root": root["id"], "name": root["name"], "project_id": root["project_id"],
        "parent_branch": None, "split_from": None, "split_at": None, "cycle": False,
        "experiments": members, "experiments_total": len(members),
        "metric": dict(zip(("key", "goal", "reduce"), metric)),
        "best": {"experiment": root["id"], "run": _uuid(5000 + n), "value": 0.5, "live": False},
        "rank": rank, "of": of, "behind_leader": None,
        "effort": {"span": [_T0, span_end], "busy_h": 1.0, "run_h": 1.0, "agent_h": float(len(members)),
                   "cost_usd": None, "cost_estimated": False},
        "busy": [[_T0, span_end]], "busy_total": 1, "overlaps": [], "climb": [], "gain": None,
        "state": "idle", "last_active_at": span_end, "sessions": [], "sessions_total": 0,
        "sessions_by": [], "built_on": [], "built_on_total": 0, "used_by": [], "used_by_total": 0,
    }


def _read(branches: list[dict], *, workspace: bool = False, groups: list[dict] | None = None) -> dict:
    """A branches read around `branches`, its groups one per metric unless given."""
    if groups is None:
        groups = []
        for b in branches:
            if all(g["metric"] != b["metric"] for g in groups):
                standing = {"branch": b["root"], "name": b["name"], "best": b["best"]}
                groups.append({"metric": b["metric"], "leader": {**standing, "incomplete": False},
                               "runner_up": None, "gap": None, "standings": [standing], "leader_changes": []})
    metric = None if workspace else {**branches[0]["metric"], "declared_on": {"type": "project", "id": _uuid(901)},
                                     "inherited": False, "source": "human", "set_by": "user:x", "set_at": _T0}
    return {
        "scope": {"type": "workspace" if workspace else "project", "id": _uuid(999), "name": "scope"},
        "generated_at": _T0, "metric": metric, "pick": None, "leader": None, "runner_up": None, "gap": None,
        "groups": groups, "focus": None, "branches": branches, "elsewhere_agent_h": 0.0, "locked_runs": 0,
        "values_withheld": False, "truncated": False, "effort_truncated": None,
    }


def test_a_workspace_branch_opens_in_full_from_the_workspace_read():
    """A in P1, continued by B in P2: one branch in the workspace read, A
    alone in P1's. Opened from the workspace page, the branch keeps both
    members and the numbers it was listed with; a project read would cut it."""
    a, b = _member(1, "a"), _member(2, "b", project="p2")
    workspace = _read([_line(1, [a, b], span_end="2026-10-25T14:00:00Z")], workspace=True)
    project = _read([_line(1, [a], span_end="2026-10-25T11:00:00Z")])
    source = _Source(workspace=workspace, project=project)
    service = ResearchReadService(source)
    [row] = service.browse_list("branches", workspace_id=WORKSPACE)["data"]["branches"]
    assert row["experiments_total"] == 2
    full = service.browse_list("branches", workspace_id=WORKSPACE, branch=row["ref"])["data"]
    assert full["branch"]["ref"] == row["ref"] and full["branch"]["experiments_total"] == 2
    assert full["branch"]["effort"] == row["effort"]
    assert [e["name"] for e in full["experiments"]] == ["a", "b"]
    assert all(call[0] == "workspace" for call in source.calls)
    out, _ = _delivered(
        _wire(service, "browse", {"mode": "branches", "workspace_id": WORKSPACE, "branch": row["ref"]}),
        COMPACT_TOKENS,
    )
    assert [e["name"] for e in out["data"]["experiments"]] == ["a", "b"]


def test_a_row_ranked_on_another_metric_names_its_whole_group():
    """The server ranks per (key, goal, reduce): three `score` groups stay
    three on the rows and on an experiment in full."""
    tuples = [("score", "max", "final"), ("score", "min", "final"), ("score", "max", "best")]
    branches = [_line(i, [_member(i, f"s{i}", metric=t)], metric=t) for i, t in enumerate(tuples)]
    rows = ResearchReadService(_Source(workspace=_read(branches, workspace=True))).browse_list(
        "branches", workspace_id=WORKSPACE
    )["data"]["branches"]
    assert [(r["metric"]["key"], r["metric"]["goal"], r["metric"]["reduce"]) for r in rows] == tuples
    assert all(r["rank"] == 1 and r["of"] == 1 for r in rows)
    mixed = _line(9, [_member(9, "m", metric=tuples[0]), _member(10, "m2", metric=tuples[2])], metric=tuples[0])
    data = ResearchReadService(_Source(project=_read([mixed]))).get_entity(
        f"project:{ID['P1']}", view="branches", filters={"branch": "experiment:m"}
    )["data"]
    assert "metric" not in data["experiments"][0]
    assert data["experiments"][1]["metric"] == {"key": "score", "goal": "max", "reduce": "best"}


def test_two_hundred_metric_groups_still_page_whole_branches():
    """A group rides only on its own row, so the fixed part stays small and
    every page can be served at the default budget, on both surfaces."""
    branches = [_line(i, [_member(i, f"g{i}")], metric=(f"metric/{i}", "max", "final")) for i in range(200)]
    service = ResearchReadService(
        _Source(workspace=_read(branches, workspace=True), project=_read(branches))
    )
    for tool, args in (
        ("browse", {"mode": "branches", "workspace_id": WORKSPACE}),
        ("entity", {"refs": [f"project:{ID['P1']}"], "view": "branches"}),
    ):
        seen, cursor = [], None
        while True:
            out, _ = _delivered(_wire(service, tool, {**args, **({"cursor": cursor} if cursor else {})}), 2000)
            assert out["data"].get("format") is None, "whole rows, never a fragment"
            seen += [row["ref"] for row in out["data"]["branches"]]
            cursor = out.get("next_cursor")
            if not cursor:
                break
        assert len(seen) == len(set(seen)) == 200, tool


def test_a_ref_selects_exactly_the_branch_it_names():
    """Slugs are free-form: `baseline` and `baseline ` are two branches."""
    one, two = _line(1, [_member(1, "baseline")]), _line(2, [_member(2, "baseline ")])
    two["name"] = "second"
    service = ResearchReadService(_Source(workspace=_read([one, two], workspace=True), project=_read([one, two])))
    rows = service.browse_list("branches", workspace_id=WORKSPACE)["data"]["branches"]
    assert [r["ref"] for r in rows] == ["experiment:baseline", "experiment:baseline "]
    for ref, name in (("experiment:baseline ", "second"), ("experiment:baseline", "baseline"), (_uuid(2), "second")):
        on_project = service.get_entity(f"project:{ID['P1']}", view="branches", filters={"branch": ref})
        assert on_project["data"]["branch"]["name"] == name, ref
        full = service.browse_list("branches", workspace_id=WORKSPACE, branch=ref)["data"]["branch"]
        assert full["name"] == name, ref


def test_a_slug_too_long_for_entity_is_emitted_as_its_id():
    """`entity` takes refs of at most 256 characters: a longer slug ref is
    sent as the uuid ref, everywhere a ref is emitted, and still opens."""
    from probe.mcp.server import create_server

    entity = next(t for t in anyio.run(create_server(object()).list_tools) if t.name == "entity")
    limit = entity.inputSchema["properties"]["refs"]["items"]["maxLength"]
    long_slug = "s" * 246
    line = _line(1, [_member(1, long_slug), _member(2, "child")])
    line["overlaps"] = [{"branch": _uuid(1), "hours": 1.0}]
    service = ResearchReadService(_Source(workspace=_read([line], workspace=True)))
    out = service.browse_list("branches", workspace_id=WORKSPACE)
    refs = re.findall(r'"(experiment:[^"]*)"', json.dumps(out["data"]))
    assert refs and all(len(ref) <= limit for ref in refs)
    [row] = out["data"]["branches"]
    assert row["ref"] == f"experiment:{_uuid(1)}"
    full = service.browse_list("branches", workspace_id=WORKSPACE, branch=row["ref"])["data"]
    assert full["branch"]["ref"] == row["ref"] and full["experiments"][0]["ref"] == row["ref"]
    from probe.mcp.branches import MAX_REF_CHARS

    assert MAX_REF_CHARS == limit


# -- the CLI and the SDK ---------------------------------------------------------

_BRANCHES = re.compile(r"^/v1/(?:projects/[^/]+(?:/experiments/[^/]+/branch|/branches)|workspaces/[^/]+/branches)$")


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"]) == 0
    seen: list[str] = []
    real = app.handler

    def handler(request: httpx.Request) -> httpx.Response:
        if _BRANCHES.match(request.url.path) and request.method == "GET":
            seen.append(request.url.path)
            return httpx.Response(200, json=SNAP["project"])
        return real(request)

    monkeypatch.setattr(app, "handler", handler)
    return app, seen


def test_the_cli_prints_the_branches_reads(wired, capsys):
    app, seen = wired
    project = next(p for p in app.projects.values() if p.get("slug") == "p")
    capsys.readouterr()
    assert cli.main(["project", "branches", "p"]) == 0
    assert json.loads(capsys.readouterr().out) == SNAP["project"]
    assert seen[-1] == f"/v1/projects/{project['id']}/branches"
    assert cli.main(["experiment", "branch", "e"]) == 0
    assert json.loads(capsys.readouterr().out) == SNAP["project"]
    experiment = next(e for e in app.experiments.values() if e.get("slug") == "e")
    assert seen[-1] == f"/v1/projects/{project['id']}/experiments/{experiment['id']}/branch"


def test_the_sdk_reads_the_three_routes(wired, tmp_path):
    app, seen = wired
    client = make_client(app, tmp_spool=tmp_path / "spool2")
    project = next(p for p in app.projects.values() if p.get("slug") == "p")
    experiment = next(e for e in app.experiments.values() if e.get("slug") == "e")
    assert client.project_branches(project["id"]) == SNAP["project"]
    assert client.experiment_branch(experiment["id"], project_id=project["id"]) == SNAP["project"]
    assert client.workspace_branches(WORKSPACE) == SNAP["project"]
    assert seen == [
        f"/v1/projects/{project['id']}/branches",
        f"/v1/projects/{project['id']}/experiments/{experiment['id']}/branch",
        f"/v1/workspaces/{WORKSPACE}/branches",
    ]
