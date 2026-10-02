"""Budgeted traversal keeps every source row reachable without replay hashes."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from collections import Counter
from copy import deepcopy
from uuid import NAMESPACE_URL, uuid5

import pytest

from probe.mcp.browse_delivery import invoke
from probe.mcp.budget import Budget, serialize
from probe.mcp.continuation import ContinuationError, binding, decode
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource


def node(kind, label, **fields):
    ident = str(uuid5(NAMESPACE_URL, label))
    return {
        "entity_type": kind,
        "uuid": f"{kind}:{ident}",
        "name": label,
        "slug": f"{kind}:{label}",
        "url": f"https://research.prbe.ai/{kind}s/{ident}",
        **fields,
    }


class Tree:
    """Source fixture with the backend's exact handle wire size and list semantics.

    Independent backend integration tests prove SQL/RLS/signatures. This fixture
    verifies the MCP consumes those row positions correctly at every output cut.
    """

    def __init__(self, projects, experiments=None, runs=None, subprojects=None):
        self.projects = projects
        self.experiments = experiments or {}
        self.runs = runs or {}
        self.subprojects = subprojects or {}
        self.calls = []
        self.positions = {}

    def handle(self, args, level, position):
        context = hashlib.sha256(
            serialize(
                [
                    "tenant",
                    args.get("ref"),
                    args.get("workspace_id"),
                    args.get("status"),
                    sorted(set(args.get("tags") or [])),
                    level,
                ]
            ).encode()
        ).hexdigest()
        # Use random-looking UUIDs and real timestamps so the minimum-budget
        # test does not get a false pass from compressible toy cursor strings.
        raw = json.dumps(
            [
                context,
                "2026-09-05T08:12:34.123456+00:00" if position else None,
                str(uuid5(NAMESPACE_URL, f"{context}:{position}")) if position else None,
            ],
            separators=(",", ":"),
        ).encode()
        signature = hmac.digest(b"synthetic signing key", raw, "sha256")
        token = "browse1." + base64.urlsafe_b64encode(raw + signature).decode().rstrip("=")
        self.positions[token] = (context, position)
        return token

    def __call__(self, args):
        self.calls.append(dict(args))
        ref = args.get("ref")
        cap = args.get("limit", 10)
        data = {
            "scope": ref,
            "depth": args.get("depth", 1),
            "projects": None,
            "experiments": None,
            "runs": None,
            "subprojects": None,
            "available_views": {
                "project": ["card", "record", "notes", "summary"],
                "experiment": ["card", "record", "notes", "summary"],
                "run": ["card", "record", "notes", "summary"],
            },
        }
        handles = []

        def stream(level, all_rows, query_args, path, parameter, nested=False):
            cursor = query_args.get(parameter)
            start = self.handle(query_args, level, 0)
            position = 0
            if cursor:
                assert cursor in self.positions, "MCP invented a backend cursor"
                assert self.positions[cursor][0] == self.positions[start][0], (
                    "MCP crossed a bound scope"
                )
                position = self.positions[cursor][1]
                start = cursor
            limit = min(cap, 10) if nested else cap
            values = deepcopy(all_rows[position : position + limit])
            after = [
                self.handle(query_args, level, index + 1)
                for index in range(position, position + len(values))
            ]
            handles.append(
                {
                    "path": path,
                    "scope": query_args.get("ref"),
                    "workspace_id": query_args.get("workspace_id"),
                    "cursor_parameter": parameter,
                    "start": start,
                    "after": after,
                    "next_cursor": after[-1] if len(values) == limit else None,
                }
            )
            # Every fetch changes derived fields, including the same re-fetched
            # parent page. Delivery must not fingerprint this live collection.
            for value in values:
                value["active_run_count"] = len(self.calls)
                if (
                    not nested
                    and args.get("depth") == 2
                    and level in ("projects", "experiments", "subprojects")
                ):
                    child = "experiments" if level in ("projects", "subprojects") else "runs"
                    child_ref = value["uuid"]
                    ident = child_ref.split(":")[1]
                    query = {
                        **query_args,
                        "ref": child_ref,
                        "workspace_id": None,
                        "cursor": None,
                        "runs_cursor": None,
                        "subprojects_cursor": None,
                    }
                    child_values = (
                        self.experiments.get(child_ref, [])
                        if child == "experiments"
                        else self.runs.get(child_ref, [])
                    )
                    value[child] = stream(
                        child, child_values, query, [level, ident, child], "cursor", True
                    )
                elif level in ("projects", "subprojects"):
                    value["experiments"] = None
                elif level == "experiments":
                    value["runs"] = None
            return values

        if ref is None:
            data["projects"] = stream("projects", self.projects, args, ["projects"], "cursor")
        elif ref.startswith("experiment:"):
            data["runs"] = stream("runs", self.runs.get(ref, []), args, ["runs"], "cursor")
        else:
            has_cursor = any(
                args.get(key) for key in ("cursor", "runs_cursor", "subprojects_cursor")
            )
            for level, parameter, collection in (
                ("experiments", "cursor", self.experiments),
                ("runs", "runs_cursor", self.runs),
                ("subprojects", "subprojects_cursor", self.subprojects),
            ):
                if not has_cursor or args.get(parameter):
                    data[level] = stream(level, collection.get(ref, []), args, [level], parameter)
        return {
            "data": data,
            "_browse_handles": handles,
            "capabilities": {},
            "completeness": {"state": "partial", "missing": ["truncated_by_token_budget"]},
            "next_cursor": handles[0]["next_cursor"],
        }


def walk(tree, **args):
    cursor = args.get("cursor")
    results = []
    for _ in range(500):
        before = len(tree.calls)
        result = invoke({**args, "cursor": cursor}, tree, "tenant/user")
        assert len(tree.calls) == before + 1
        assert Budget(args.get("token_budget", 2000)).fits(result)
        assert "_browse_handles" not in serialize(result)
        assert "browse1." not in serialize(result)
        results.append(result)
        cursor = result.get("next_cursor")
        if not cursor:
            return results
        state = decode(cursor, binding("browse", {**args, "cursor": cursor}, "tenant/user"))
        assert len(serialize(state)) < 1500
    pytest.fail("browse did not make progress")


def seen(results):
    counts = Counter()

    def visit(data):
        for level in ("projects", "experiments", "runs", "subprojects"):
            for row in data.get(level) or []:
                counts[row["uuid"]] += 1
                visit(row)

    for result in results:
        visit(result["data"])
    return counts


def test_a_browse_walk_is_partial_until_its_last_page_which_says_nothing():
    projects = [
        node("project", f"project-{i}", description="Meaningful project description " * 8)
        for i in range(13)
    ]
    pages = walk(Tree(projects, {}), token_budget=512)
    assert len(pages) > 1
    for page in pages[:-1]:
        assert page["completeness"] == {"state": "partial", "missing": ["truncated_by_token_budget"]}
        assert page["next_cursor"]
    assert set(pages[-1]) == {"data"}


@pytest.mark.parametrize("token_budget", [512, 2000])
def test_all_projects_and_expanded_children_are_delivered_once(token_budget):
    projects = [
        node("project", f"project-{i}", description="Meaningful project description " * 8)
        for i in range(13)
    ]
    experiments = {
        p["uuid"]: [node("experiment", f"{p['name']}-experiment-{i}") for i in range(12)]
        for p in projects
    }
    tree = Tree(projects, experiments)
    results = walk(
        tree,
        depth=2,
        token_budget=token_budget,
        workspace_id="workspace",
        status="running",
        tags=["tag-2", "tag-1"],
    )
    expected = Counter(r["uuid"] for r in projects + [e for es in experiments.values() for e in es])
    assert seen(results) == expected
    assert all(
        call["status"] == "running" and call["tags"] == ["tag-2", "tag-1"] for call in tree.calls
    )
    assert all(call["workspace_id"] is None for call in tree.calls if call["ref"])


@pytest.mark.parametrize("token_budget", [512, 2000])
def test_project_all_three_streams_and_nested_runs_are_delivered_once(token_budget):
    root = node("project", "root")
    experiments = [node("experiment", f"experiment-{i}") for i in range(12)]
    runs = {
        e["uuid"]: [node("run", f"{e['name']}-run-{i}", status="running") for i in range(13)]
        for e in experiments
    }
    direct = [node("run", f"direct-{i}") for i in range(12)]
    children = [node("project", f"child-{i}") for i in range(12)]
    child_experiments = {
        p["uuid"]: [node("experiment", f"{p['name']}-experiment-{i}") for i in range(2)]
        for p in children
    }
    tree = Tree(
        [],
        {root["uuid"]: experiments, **child_experiments},
        {root["uuid"]: direct, **runs},
        {root["uuid"]: children},
    )
    results = walk(tree, ref=root["uuid"], depth=2, token_budget=token_budget)
    expected_rows = experiments + direct + children + [r for rs in runs.values() for r in rs]
    expected_rows += [e for es in child_experiments.values() for e in es]
    assert seen(results) == Counter(r["uuid"] for r in expected_rows)


def test_ordinary_browse_packs_multiple_rows_and_preserves_empty_vs_unexpanded():
    projects = [node("project", f"p-{i}") for i in range(5)]
    tree = Tree(projects)
    results = walk(tree, depth=2)
    assert len(results) == 1
    assert len(results[0]["data"]["projects"]) == 5
    assert all(row["experiments"] == [] for row in results[0]["data"]["projects"])
    shallow = walk(Tree(projects), depth=1)
    assert all(row["experiments"] is None for row in shallow[0]["data"]["projects"])


def test_small_project_keeps_all_side_lists_in_one_call():
    root = node("project", "root")["uuid"]
    tree = Tree(
        [],
        {root: [node("experiment", "exp")]},
        {root: [node("run", "run")]},
        {root: [node("project", "child")]},
    )
    results = walk(tree, ref=root, depth=1)
    assert len(results) == 1
    assert all(
        len(results[0]["data"][level]) == 1 for level in ("experiments", "runs", "subprojects")
    )
    assert results[0]["data"]["projects"] is None


def test_changed_request_and_legacy_cursor_restart_before_fetch():
    tree = Tree([node("project", f"project-{i}") for i in range(20)])
    first = invoke({"token_budget": 512, "status": "running"}, tree, "tenant/user")
    with pytest.raises(ContinuationError, match="changed request/scope"):
        invoke(
            {"token_budget": 512, "status": "completed", "cursor": first["next_cursor"]},
            tree,
            "tenant/user",
        )
    with pytest.raises(ContinuationError, match="Legacy"):
        invoke({"cursor": "old-opaque-cursor"}, tree, "tenant/user")
    assert len(tree.calls) == 1


def test_no_handles_reports_version_skew():
    with pytest.raises(ContinuationError, match="backend update"):
        invoke({}, lambda args: {"data": {"projects": []}}, "tenant/user")


def test_expensive_identity_retains_a_record_address_at_minimum_budget():
    project = node(
        "project",
        "long",
        name="漢🤖" * 500,
        description='"\\漢🤖' * 500,
        slug="project:" + "x" * 1000,
        url="https://example.com/" + "x" * 1000,
    )
    tree = Tree([project, node("project", "next")])
    results = walk(tree, depth=1, token_budget=512)
    assert seen(results) == Counter({project["uuid"]: 1, node("project", "next")["uuid"]: 1})
    row = results[0]["data"]["projects"][0]
    assert row["uuid"] == project["uuid"]
    assert "url" not in row
    assert "slug" not in row
    assert set(row["truncated_fields"]) >= {"name", "description", "slug", "url"}


def test_expensive_nested_identities_and_two_positions_fit_minimum_budget():
    projects = [
        node("project", f"project-{i}", name="漢🤖" * 500, description='"\\漢🤖' * 500)
        for i in range(10)
    ]
    experiments = {
        p["uuid"]: [
            node(
                "experiment",
                f"{p['uuid']}-experiment-{i}",
                name="漢🤖" * 500,
                description='"\\漢🤖' * 500,
            )
            for i in range(11)
        ]
        for p in projects
    }
    tree = Tree(projects, experiments)
    results = walk(tree, depth=2, token_budget=512)
    assert seen(results) == Counter(
        row["uuid"] for row in projects + [e for es in experiments.values() for e in es]
    )


def test_explicit_side_cursor_does_not_add_experiments_on_delivery_followup():
    root = node("project", "root")["uuid"]
    tree = Tree(
        [],
        {root: [node("experiment", "not-requested")]},
        {root: [node("run", f"run-{i}") for i in range(8)]},
    )
    native = tree.handle({"ref": root}, "runs", 2)
    results = walk(tree, ref=root, runs_cursor=native, token_budget=512)
    assert seen(results) == Counter(node("run", f"run-{i}")["uuid"] for i in range(2, 8))


def test_multiple_explicit_native_cursors_keep_their_original_streams():
    root = node("project", "root")["uuid"]
    tree = Tree(
        [],
        {root: [node("experiment", f"exp-{i}") for i in range(8)]},
        {root: [node("run", f"run-{i}") for i in range(8)]},
        {root: [node("project", "not-requested")]},
    )
    primary = tree.handle({"ref": root}, "experiments", 3)
    side = tree.handle({"ref": root}, "runs", 2)
    results = walk(tree, ref=root, cursor=primary, runs_cursor=side, token_budget=512)
    expected = [node("experiment", f"exp-{i}") for i in range(3, 8)]
    expected += [node("run", f"run-{i}") for i in range(2, 8)]
    assert seen(results) == Counter(row["uuid"] for row in expected)


def test_sdk_default_is_unchanged_and_opt_in_is_forwarded(client, app):
    app.browse_response = {"projects": [], "depth": 1, "limit": 50, "truncated": False}
    client.browse()
    assert "continuation_handles" not in dict(app.browse_requests[-1])
    client.browse(continuation_handles=True)
    assert dict(app.browse_requests[-1])["continuation_handles"] == "true"


def test_source_service_and_delivery_consume_the_opt_in_wire_contract(client, app):
    project = node("project", "root")
    children = [node("experiment", f"experiment-{i}") for i in range(13)]
    tree = Tree([project], {project["uuid"]: children})
    service = ResearchReadService(ResearchOSSource(client))

    def backend_node(row):
        raw = {
            key: value
            for key, value in row.items()
            if key not in ("uuid", "slug", "entity_type", "url")
        }
        raw["id"] = row["uuid"].partition(":")[2]
        raw["slug"] = row["slug"].partition(":")[2]
        for level in ("experiments", "runs"):
            if isinstance(raw.get(level), list):
                raw[level] = [backend_node(child) for child in raw[level]]
        return raw

    def read(args):
        fixture = tree(args)
        app.browse_response = {
            **{
                level: [backend_node(row) for row in fixture["data"][level]]
                if isinstance(fixture["data"][level], list)
                else None
                for level in ("projects", "experiments", "runs", "subprojects")
            },
            "continuation_handles": fixture["_browse_handles"],
            "cursor": fixture["next_cursor"],
            "depth": args["depth"],
            "limit": args["limit"],
            "truncated": any(h["next_cursor"] for h in fixture["_browse_handles"]),
        }
        return service.browse_research(
            scope=args.get("ref"),
            depth=args["depth"],
            limit=args["limit"],
            cursor=args.get("cursor"),
            runs_cursor=args.get("runs_cursor"),
            subprojects_cursor=args.get("subprojects_cursor"),
        )

    outputs = []
    cursor = None
    for _ in range(30):
        result = invoke({"depth": 2, "token_budget": 512, "cursor": cursor}, read, "tenant/user")
        assert Budget(512).fits(result)
        assert "_browse_handles" not in serialize(result)
        outputs.append(result)
        cursor = result.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("source/service traversal did not finish")
    assert seen(outputs) == Counter(row["uuid"] for row in [project, *children])
    assert all(dict(request)["continuation_handles"] == "true" for request in app.browse_requests)
    assert len(app.browse_requests) == len(outputs)
