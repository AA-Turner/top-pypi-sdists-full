"""The hosted MCP's experiment reads answer the same in BOTH storage shapes.

WHY (light experiments, task X9). Experiments are moving out of `projects` in
stages (`~/plans/research-os-backend-reconciled/PLAN.md` section 4). Until the
R2 job, an experiment E's runs, files and groups are STORED at `project_id = E`
(the old shape). After it they are stored at the real project P with a label,
`(project_id = P, experiment_id = E)` (the new shape). The leaf `projects` row
for E exists until R5, so `GET /v1/projects/{E}` keeps answering throughout.

The hosted MCP ships on its own workflow (`deploy-mcp.yml`), so whatever image
the API is on, the MCP has to read an experiment correctly from either shape.
The server's R1 image promises to answer every read the same way in both
shapes (plan 4.6 rule 2, the 4.9 adapters). This file holds the MCP to its half
of that: it must derive NOTHING from where a row happens to be stored.

HOW. `ShapedServer` is one tenant -- project P, experiments E1 and E2, four
runs, three files, one group, one edge -- stored in either shape, behind a fake
that answers every route the MCP's experiment reads call by the R1 server's
dual-shape READ RULES, written out once below (`_experiment_of`, `_home`,
`_in_scope`). Each MCP read runs against both stores and the two envelopes must
be byte-equal (the response clock aside): no field may differ.

THE WIRE IS THE LEAF SHAPE IN BOTH. Plan 4.9 keeps every response in the leaf
shape until R6, and the R1 seams (`app/artifacts/service.py`
`with_experiment_id` / `leaf_shaped`) present an experiment's file as
`project_id = experiment_id = E` whether it is stored at E or at (P, E); a
project's own file is `project_id = P, experiment_id = null`. A run's wire
`project_id` is its home project and `experiment_id` its experiment
(`run_detail_out`); a group's wire carries `experiment_id` only. So a server
that honours R1 sends the same bytes for both stores, and an equal MCP answer
is the proof that the MCP keys no decision on the stored address.

FROM R4 (X15) the MCP reads the experiment ITSELF through the experiment API:
`GET /v1/scopes/{E}` says which project it is filed under, then
`GET /v1/projects/{P}/experiments[/{E}]` answers it as an experiment (its run
count through the same R1 scope seam). The fake serves those too.

The fake answers these routes by rules the server's R1 image must honour. On
main today they read the leaf address only, and X3/X4/X6 make them dual-shape:
`GET /v1/runs?experiment_id|project_id|direct`, the run wire's
`experiment_id`, `GET /v1/projects/{E}` (`run_count`),
`GET /v1/projects/{E}/artifacts` and `/v1/projects/{P}/artifacts`,
`GET /v1/projects/{E}/groups` and `GET /v1/groups/{id}` (`experiment_id`),
`GET /v1/projects/{E}/edges`, `GET /v1/projects/{id}/lineage` (`nodes`) and
`GET /v1/browse?scope=experiment:E`.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import parse_qs

import httpx
import pytest

from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from tests.conftest import make_client

P = "aaaaaaaa-0000-4000-8000-000000000001"
E1 = "aaaaaaaa-0000-4000-8000-0000000000e1"
E2 = "aaaaaaaa-0000-4000-8000-0000000000e2"
R1 = "bbbbbbbb-0000-4000-8000-000000000001"  # in E1, finished
R2 = "bbbbbbbb-0000-4000-8000-000000000002"  # in E1, running
R3 = "bbbbbbbb-0000-4000-8000-000000000003"  # project-direct under P, running
R4 = "bbbbbbbb-0000-4000-8000-000000000004"  # in E2, finished
F_P = "cccccccc-0000-4000-8000-0000000000f0"  # P's own file
F_E1 = "cccccccc-0000-4000-8000-0000000000f1"  # E1's file
F_E1B = "cccccccc-0000-4000-8000-0000000000f2"  # E1's second file, in a folder
G1 = "dddddddd-0000-4000-8000-0000000000a1"  # a group (sweep) in E1
EDGE = "eeeeeeee-0000-4000-8000-000000000001"  # R1 produced F_E1

OLD = "old"
NEW = "new"
SHAPES = (OLD, NEW)

_T0 = "2026-10-01T00:00:0{}Z"


def _not_found(detail: str) -> httpx.Response:
    return httpx.Response(404, json={"detail": detail})


class ShapedServer:
    """One tenant stored in `shape`, answered by the R1 dual-shape read rules."""

    def __init__(self, shape: str) -> None:
        self.shape = shape
        self.requests: list[str] = []
        self.projects = {
            P: {
                "id": P,
                "customer_id": "lab-42",
                "workspace_id": "ffffffff-0000-4000-8000-000000000001",
                "slug": "rl-scaling",
                "name": "RL scaling",
                "kind": "research",
                "description": "Does RL scale with rollouts?",
                "parent_project_id": None,
                "notes": "P notes",
                "notes_version": 1,
                "created_at": _T0.format(0),
                "updated_at": _T0.format(0),
            },
            E1: self._leaf(E1, "lr-sweep", "LR sweep", "Is lr 3e-4 best?", 1),
            E2: self._leaf(E2, "kl-ablation", "KL ablation", "Does KL help?", 2),
        }
        # (id, experiment, name, status, created second). experiment None = direct.
        runs = [
            (R1, E1, "lr-1e-4", "finished", 1),
            (R2, E1, "lr-3e-4", "running", 2),
            (R3, None, "baseline", "running", 3),
            (R4, E2, "kl-0", "finished", 4),
        ]
        self.runs = [
            {
                "id": rid,
                **self._stored(exp),
                "slug": f"run-{name}",
                "name": name,
                "status": status,
                "group_id": G1 if rid == R1 else None,
                "created_at": _T0.format(sec),
                "updated_at": _T0.format(sec),
                "started_at": _T0.format(sec),
                "notes": None,
            }
            for rid, exp, name, status, sec in runs
        ]
        files = [
            (F_P, None, "readme.md", ""),
            (F_E1, E1, "results.json", ""),
            (F_E1B, E1, "plots/loss.png", "plots"),
        ]
        self.files = [
            {
                "id": fid,
                **self._stored(exp),
                "run_id": None,
                "name": name,
                "path": path,
                "kind": "file",
                "status": "complete",
                "content_hash": f"sha256:{fid[-4:]}",
                "size_bytes": 10,
                "created_at": _T0.format(5),
            }
            for fid, exp, name, path in files
        ]
        self.groups = [
            {
                "id": G1,
                **self._stored(E1),
                "kind": "sweep",
                "name": "lr-grid",
                "spec": {"lr": [1e-4, 3e-4]},
                "notes": "grid over lr",
                "created_at": _T0.format(6),
            }
        ]
        self.edges = [
            {
                "id": EDGE,
                "source_type": "run",
                "source_id": R1,
                "target_type": "artifact",
                "target_id": F_E1,
                "relation": "produced",
                "provenance": "observed_call",
            }
        ]

    def _leaf(self, eid: str, slug: str, name: str, question: str, sec: int) -> dict:
        return {
            "id": eid,
            "customer_id": "lab-42",
            "workspace_id": "ffffffff-0000-4000-8000-000000000001",
            "slug": slug,
            "name": name,
            "kind": "experiment",
            # An experiment's question IS its leaf's description (0231).
            "description": question,
            "parent_project_id": P,
            "notes": f"{name} notes",
            "notes_version": 3,
            "document": f"# {name}\n\nSetup.",
            "created_at": _T0.format(sec),
            "updated_at": _T0.format(sec),
        }

    def _stored(self, experiment: str | None) -> dict:
        """Where a child of `experiment` (None = the project itself) is STORED."""
        if experiment is None:
            return {"project_id": P, "experiment_id": None}
        if self.shape == OLD:
            return {"project_id": experiment, "experiment_id": None}
        return {"project_id": P, "experiment_id": experiment}

    # -- the R1 image's dual-shape read rules --------------------------------

    def _is_leaf(self, pid: str | None) -> bool:
        row = self.projects.get(pid or "")
        return bool(row) and row["kind"] == "experiment"

    def _experiment_of(self, row: dict) -> str | None:
        """The label when set, else the leaf the row is filed at (the R1
        `run_experiment_sql`, and what a group's and file's `experiment_id` must be)."""
        if row.get("experiment_id"):
            return row["experiment_id"]
        return row["project_id"] if self._is_leaf(row["project_id"]) else None

    def _home(self, row: dict) -> str | None:
        """The project a row is filed under (`run_home_project_sql`)."""
        pid = row["project_id"]
        return self.projects[pid]["parent_project_id"] if self._is_leaf(pid) else pid

    def _in_scope(self, row: dict, scope: str) -> bool:
        """`runs_filed_under_sql` with its R1 experiment arm."""
        if self._is_leaf(scope):
            return row["project_id"] == scope or row.get("experiment_id") == scope
        return self._home(row) == scope

    def _run_wire(self, row: dict) -> dict:
        return {
            **{k: v for k, v in row.items() if k not in ("project_id", "experiment_id")},
            # run_detail_out: `project_id` is the project the run is filed under.
            "project_id": self._home(row),
            "experiment_id": self._experiment_of(row),
        }

    def _file_wire(self, row: dict) -> dict:
        """The leaf shape the R1 seams serve (`with_experiment_id`): an
        experiment's file names the experiment in BOTH `project_id` and
        `experiment_id`, a project's own file names the project and no
        experiment -- whichever shape the row is stored in."""
        experiment = self._experiment_of(row)
        return {
            **row,
            "project_id": experiment if experiment is not None else row["project_id"],
            "experiment_id": experiment,
        }

    def _group_wire(self, row: dict) -> dict:
        out = {k: v for k, v in row.items() if k not in ("project_id", "experiment_id")}
        return {**out, "customer_id": "lab-42", "experiment_id": self._experiment_of(row)}

    def _project_wire(self, row: dict) -> dict:
        runs = [r for r in self.runs if self._in_scope(r, row["id"])]
        return {
            **row,
            "run_count": len(runs),
            "active_run_count": sum(r["status"] == "running" for r in runs),
        }

    # -- routes ----------------------------------------------------------------

    def handler(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        q = {k: v[-1] for k, v in parse_qs(request.url.query.decode()).items()}
        self.requests.append(f"{request.method} {path}")
        if request.method != "GET":
            raise AssertionError(f"an MCP read sent a write: {request.method} {path}")
        parts = path.strip("/").split("/")[1:]  # drop "v1"
        if parts == ["me"]:
            return httpx.Response(
                200,
                json={
                    "user_id": "00000000-0000-0000-0000-000000000001",
                    "email": "dev@example.com",
                    "name": "Dev",
                    "customer_id": "lab-42",
                    "role": "owner",
                    "scopes": ["read"],
                    "via": "oauth",
                },
            )
        if parts == ["projects"]:
            return httpx.Response(200, json=self._list_projects(q))
        if parts == ["runs"]:
            return httpx.Response(200, json=self._list_runs(q))
        if parts == ["browse"]:
            return self._browse(q)
        if len(parts) >= 2 and parts[0] == "runs":
            run = next((r for r in self.runs if r["id"] == parts[1]), None)
            if run is None:
                return _not_found("run not found")
            if len(parts) == 2:
                return httpx.Response(200, json=self._run_wire(run))
            if parts[2:] == ["bundle"]:
                return httpx.Response(
                    200,
                    json={
                        "run": self._run_wire(run),
                        "series": [],
                        "span_types": {},
                        "artifacts": [],
                        "artifact_total": 0,
                        "parent_run_id": None,
                        "child_run_ids": [],
                        "sessions": [],
                        "session_total": 0,
                    },
                )
        if len(parts) >= 2 and parts[0] == "groups":
            group = next((g for g in self.groups if g["id"] == parts[1]), None)
            if group is None:
                return _not_found("group not found")
            return httpx.Response(200, json=self._group_wire(group))
        if len(parts) == 2 and parts[0] == "scopes":
            return self._scope(parts[1])
        if len(parts) >= 2 and parts[0] == "projects":
            project = self.projects.get(parts[1])
            if project is None:
                return _not_found("project not found")
            if len(parts) >= 3 and parts[2] == "experiments":
                return self._experiment_api(project, parts[3:], q)
            return self._project_route(project, parts[2:], q)
        raise AssertionError(f"the fake does not serve {request.method} {request.url}")

    # -- the experiment API (R1 reads; what the MCP calls from R4) -------------

    def _scope(self, ident: str) -> httpx.Response:
        """`GET /v1/scopes/{id}` (`app/experiments/workspace.py::resolve_scope`)."""
        row = self.projects.get(ident)
        if row is not None and row["kind"] == "experiment":
            body = {"id": ident, "kind": "experiment", "project_id": row["parent_project_id"],
                    "experiment_id": ident, "run_id": None}
            return httpx.Response(200, json=body)
        if row is not None:
            body = {"id": ident, "kind": "project", "project_id": ident,
                    "experiment_id": None, "run_id": None}
            return httpx.Response(200, json=body)
        run = next((r for r in self.runs if r["id"] == ident), None)
        if run is not None:
            body = {"id": ident, "kind": "run", "project_id": self._home(run),
                    "experiment_id": self._experiment_of(run), "run_id": ident}
            return httpx.Response(200, json=body)
        return _not_found("nothing with this id")

    def _experiment_row(self, leaf: dict) -> dict:
        """`ProjectExperimentOut`: an experiment AS an experiment, filed under
        its project, its run count read through the R1 scope seam."""
        return {
            "id": leaf["id"],
            "project_id": leaf["parent_project_id"],
            "slug": leaf["slug"],
            "legacy_slug": None,
            "name": leaf["name"],
            "question": leaf["description"],
            "run_count": sum(1 for r in self.runs if self._in_scope(r, leaf["id"])),
            "created_at": leaf["created_at"],
            "updated_at": leaf["updated_at"],
            "created_by": None,
        }

    def _experiment_api(self, project: dict, rest: list[str], q: dict) -> httpx.Response:
        pid = project["id"]
        if self._is_leaf(pid):
            return _not_found("project not found: this id is an experiment")
        leaves = sorted(
            (p for p in self.projects.values() if p["parent_project_id"] == pid and self._is_leaf(p["id"])),
            key=lambda p: (p["created_at"], p["id"]),
            reverse=True,
        )
        if not rest:
            items = [self._experiment_row(p) for p in leaves]
            limit, offset = int(q.get("limit", 100)), int(q.get("offset", 0))
            window = items[offset : offset + limit]
            more = offset + limit < len(items)
            return httpx.Response(
                200,
                json={"items": window, "total": len(items), "limit": limit, "offset": offset,
                      "next_offset": offset + limit if more else None},
            )
        leaf = next((p for p in leaves if rest[0] in (p["id"], p["slug"])), None)
        if leaf is None:
            return _not_found("experiment not found")
        if rest[1:]:
            raise AssertionError(f"the fake does not serve experiments/{'/'.join(rest)}")
        return httpx.Response(
            200,
            json={
                **self._experiment_row(leaf),
                "notes": leaf["notes"],
                "notes_version": leaf["notes_version"],
                "notes_updated_at": None,
                "summary": {"content": "absent", "job": "idle", "blurb": None, "version": 0},
            },
        )

    def _list_projects(self, q: dict) -> list[dict]:
        rows = list(self.projects.values())
        if "parent_id" in q:
            rows = [r for r in rows if r["parent_project_id"] == q["parent_id"]]
        if "kind" in q:
            rows = [r for r in rows if r["kind"] == q["kind"]]
        names_a_row = any(k in q for k in ("parent_id", "slug", "name"))
        if not names_a_row and q.get("kind") != "experiment":
            rows = [r for r in rows if r["kind"] != "experiment"]
        # `project_id` is NOT a parameter of GET /v1/projects: the real route
        # ignores it, so the fake does too. (The SDK no longer sends it: its
        # experiment lists use GET /v1/projects/{P}/experiments since X15.)
        rows.sort(key=lambda r: (r["created_at"], r["id"]), reverse=True)
        return rows[: int(q.get("limit", 50))]

    def _list_runs(self, q: dict) -> list[dict]:
        rows = [r for r in self.runs if r["project_id"] is not None]
        if "experiment_id" in q:
            scope = q["experiment_id"]
            rows = [r for r in rows if self._is_leaf(scope) and self._in_scope(r, scope)]
        if "project_id" in q:
            rows = [r for r in rows if self._in_scope(r, q["project_id"])]
        if q.get("direct") == "true":
            rows = [r for r in rows if self._experiment_of(r) is None]
        if "status" in q:
            rows = [r for r in rows if r["status"] == q["status"]]
        rows.sort(key=lambda r: (r["created_at"], r["id"]), reverse=True)
        return [self._run_wire(r) for r in rows[: int(q.get("limit", 50))]]

    def _project_route(self, project: dict, rest: list[str], q: dict) -> httpx.Response:
        pid = project["id"]
        if not rest:
            return httpx.Response(200, json=self._project_wire(project))
        if rest == ["artifacts"]:
            if self._is_leaf(pid):
                rows = [f for f in self.files if self._in_scope(f, pid)]
            else:
                # The parent's own files: an experiment's files are not on its rail.
                rows = [
                    f
                    for f in self.files
                    if f["project_id"] == pid and self._experiment_of(f) is None
                ]
            return httpx.Response(200, json=[self._file_wire(f) for f in rows])
        if rest == ["groups"]:
            rows = [g for g in self.groups if self._experiment_of(g) == pid]
            return httpx.Response(200, json=[self._group_wire(g) for g in rows])
        if rest == ["sub-notes"]:
            return httpx.Response(200, json={"sub_notes": []})
        if rest == ["edges"]:
            ids = {r["id"] for r in self.runs if self._in_scope(r, pid)}
            ids |= {f["id"] for f in self.files if self._in_scope(f, pid)}
            rows = [e for e in self.edges if e["source_id"] in ids or e["target_id"] in ids]
            return httpx.Response(200, json=rows[: int(q.get("limit", 1000))])
        if rest == ["lineage"]:
            children = [self._run_wire(r) for r in self.runs if self._in_scope(r, pid)]
            if not self._is_leaf(pid):
                children = [c for c in children if c["experiment_id"] is None]
                children += [
                    self._project_wire(p)
                    for p in self.projects.values()
                    if p["parent_project_id"] == pid
                ]
            return httpx.Response(
                200,
                json={
                    "kind": project["kind"],
                    "origin": {"type": "project", "id": project["parent_project_id"]}
                    if project["parent_project_id"]
                    else None,
                    "edges": [],
                    "nodes": children,
                    "truncated": False,
                },
            )
        raise AssertionError(f"the fake does not serve /v1/projects/{pid}/{'/'.join(rest)}")

    def _browse(self, q: dict) -> httpx.Response:
        scope = q.get("scope", "")
        kind, _, ident = scope.partition(":")
        if kind == "experiment" and self._is_leaf(ident):
            runs = [r for r in self.runs if self._in_scope(r, ident)]
            runs.sort(key=lambda r: (r["created_at"], r["id"]), reverse=True)
            return httpx.Response(
                200,
                json={
                    "scope": scope,
                    "depth": 1,
                    "runs": [
                        {
                            k: v
                            for k, v in self._run_wire(r).items()
                            if k in ("id", "slug", "name", "status", "created_at", "experiment_id")
                        }
                        for r in runs
                    ],
                },
            )
        raise AssertionError(f"the fake does not browse {scope!r}")


def _service(shape: str) -> tuple[ResearchReadService, ShapedServer]:
    server = ShapedServer(shape)
    client = make_client(server)
    return ResearchReadService(ResearchOSSource(client)), server


def _clockless(value: Any) -> Any:
    """Drop the response clock (`as_of`), the one thing that differs between
    two calls whatever the store. Nothing else is removed."""
    if isinstance(value, list):
        return [_clockless(v) for v in value]
    if isinstance(value, dict):
        return {k: _clockless(v) for k, v in value.items() if k != "as_of"}
    return value


def _rows_naming(value: Any, key: str) -> list[dict]:
    """Every dict inside `value` that carries `key`."""
    found: list[dict] = []
    if isinstance(value, list):
        for v in value:
            found += _rows_naming(v, key)
    elif isinstance(value, dict):
        if key in value:
            found.append(value)
        for v in value.values():
            found += _rows_naming(v, key)
    return found


#: Every MCP read that touches an experiment, as (label, call). Each is run on
#: both stores; `test_every_read_answers_the_same_in_both_shapes` compares them.
_READS: list[tuple[str, Any]] = [
    ("experiment card", lambda s: s.get_entity(f"experiment:{E1}")),
    # A bare id: the sweep tries run first, then experiment (source.get).
    ("bare experiment id", lambda s: s.get_entity(E1)),
    ("experiment artifacts", lambda s: s.get_entity(f"experiment:{E1}", view="artifacts")),
    ("project artifacts", lambda s: s.get_entity(f"project:{P}", view="artifacts")),
    ("experiment groups", lambda s: s.get_entity(f"experiment:{E1}", view="groups")),
    ("group card", lambda s: s.get_entity(f"group:{G1}")),
    ("experiment lineage", lambda s: s.get_entity(f"experiment:{E1}", view="lineage")),
    ("project lineage", lambda s: s.get_entity(f"project:{P}", view="lineage")),
    ("experiment notes", lambda s: s.get_entity(f"experiment:{E1}", view="notes")),
    ("experiment summary", lambda s: s.get_entity(f"experiment:{E1}", view="summary")),
    ("run card", lambda s: s.get_entity(f"run:{R1}")),
    # The handoff reads the run's question off its experiment (_question_of).
    ("experiment run handoff", lambda s: s.get_entity(f"run:{R2}", view="handoff")),
    ("direct run handoff", lambda s: s.get_entity(f"run:{R3}", view="handoff")),
    ("runs in an experiment", lambda s: s.browse_list("runs", scope=f"experiment:{E1}")),
    ("runs in a project", lambda s: s.browse_list("runs", scope=f"project:{P}")),
    ("browse an experiment", lambda s: s.browse_research(scope=f"experiment:{E1}")),
    (
        "research context",
        lambda s: s.research_context(task="is lr 3e-4 best", project_ref="rl-scaling"),
    ),
]


@pytest.mark.parametrize("label,read", _READS, ids=[label for label, _ in _READS])
def test_every_read_answers_the_same_in_both_shapes(label, read) -> None:
    answers = {}
    for shape in SHAPES:
        service, _server = _service(shape)
        answers[shape] = read(service)
    old, new = (_clockless(answers[s]) for s in SHAPES)
    assert json.dumps(old, sort_keys=True) == json.dumps(new, sort_keys=True), (
        f"{label}: the MCP answered differently once E's rows moved to (P, E):\n"
        f"old: {json.dumps(old, indent=1, sort_keys=True)}\n"
        f"new: {json.dumps(new, indent=1, sort_keys=True)}"
    )


@pytest.mark.parametrize("shape", SHAPES)
def test_an_experiment_s_files_name_it_in_both_shapes(shape) -> None:
    """`experiment_id` names E1 on every one of its file rows, in the leaf
    shape (`project_id` = E1 too), and the parent's own file names the project
    and no experiment -- in either store."""
    service, _ = _service(shape)
    files = service.get_entity(f"experiment:{E1}", view="artifacts")["data"]["artifacts"]
    assert {f["name"] for f in files} == {"results.json", "plots/loss.png"}
    assert {f["experiment_id"] for f in files} == {E1}
    assert {f["project_id"] for f in files} == {E1}
    own = service.get_entity(f"project:{P}", view="artifacts")["data"]["artifacts"]
    assert [f["name"] for f in own] == ["readme.md"]
    assert all(f.get("experiment_id") is None for f in own)
    assert {f["project_id"] for f in own} == {P}


@pytest.mark.parametrize("shape", SHAPES)
def test_the_answers_are_about_the_right_rows(shape) -> None:
    """Equal answers could still be equally wrong. Pin the content once."""
    service, _ = _service(shape)
    card = service.get_entity(f"experiment:{E1}")["data"]
    assert card["entity_type"] == "experiment"
    assert card["entity"]["question"] == "Is lr 3e-4 best?"
    assert card["entity"]["run_count"] == 2

    handoff = service.get_entity(f"run:{R2}", view="handoff")
    assert handoff["data"]["question"] == "Is lr 3e-4 best?"
    assert "experiment" not in (handoff.get("completeness") or {}).get("missing", [])
    direct = service.get_entity(f"run:{R3}", view="handoff")
    assert direct["data"].get("question") is None
    assert "experiment" not in (direct.get("completeness") or {}).get("missing", [])

    runs = service.browse_list("runs", scope=f"experiment:{E1}")["data"]["runs"]
    assert [r["name"] for r in runs] == ["lr-3e-4", "lr-1e-4"]
    every = service.browse_list("runs", scope=f"project:{P}")["data"]["runs"]
    assert {r["name"] for r in every} == {"lr-1e-4", "lr-3e-4", "baseline", "kl-0"}

    groups = service.get_entity(f"experiment:{E1}", view="groups")["data"]["groups"]
    assert [(g["name"], g["experiment_id"]) for g in groups] == [("lr-grid", E1)]
    lineage = service.get_entity(f"experiment:{E1}", view="lineage")["data"]
    assert [(e["source_id"], e["target_id"]) for e in lineage["run_edges"]] == [(R1, F_E1)]

    context = service.research_context(task="is lr 3e-4 best", project_ref="rl-scaling")
    active = {r["name"] for r in context["data"]["active_runs"]}
    # The running experiment run AND the running project-direct run, once each.
    assert active == {"lr-3e-4", "baseline"}


@pytest.mark.parametrize("shape", SHAPES)
def test_every_wire_row_names_its_experiment_by_label(shape) -> None:
    """Over every read above, a row that names an experiment names E1 or E2 --
    never the project P, which is what a group row would say in the new shape
    if `experiment_id` were still read off the stored `project_id`."""
    service, _ = _service(shape)
    for label, read in _READS:
        for row in _rows_naming(read(service), "experiment_id"):
            assert row["experiment_id"] in {E1, E2, None}, (label, row)


def test_no_read_differs_between_the_shapes() -> None:
    """All reads at once, with nothing scrubbed but the clock: not one differs.
    (The per-read test above says WHICH read broke; this one makes the claim in
    one place, so a future exception has to be written here to pass.)"""
    differing = [
        label
        for label, read in _READS
        if _clockless(read(_service(OLD)[0])) != _clockless(read(_service(NEW)[0]))
    ]
    assert differing == []


def test_the_fake_really_stores_two_shapes() -> None:
    """Guard the guard: if both stores held the same rows, every comparison
    above would pass for nothing."""
    old, new = ShapedServer(OLD), ShapedServer(NEW)
    stored = {
        shape: {r["id"]: (r["project_id"], r["experiment_id"]) for r in s.runs + s.files + s.groups}
        for shape, s in ((OLD, old), (NEW, new))
    }
    assert stored[OLD][R1] == (E1, None) and stored[NEW][R1] == (P, E1)
    assert stored[OLD][F_E1] == (E1, None) and stored[NEW][F_E1] == (P, E1)
    assert stored[OLD][G1] == (E1, None) and stored[NEW][G1] == (P, E1)
    assert stored[OLD][R3] == stored[NEW][R3] == (P, None)
