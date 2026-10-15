"""The data catalog on the hosted MCP (data-catalog T7): three browse modes and
three entity ref kinds, and no new tool.

  * `browse(mode="datasets"|"checkpoints"|"sources")` -- each reads ONE route,
    sends only that route's own filters, and refuses the rest naming the mode
    that reads them (refuse, never drop);
  * `entity(refs=["dataset:..."|"source:..."|"checkpoint:..."])` -- `card`,
    `versions` (a dataset's versions, a checkpoint's saves) and `lineage` (the
    provenance walk, or the methods view with `steps`);
  * `artifact:<name>` keeps its Shared reuse-check meaning.

Driven through the real tool layer against `McpCatalogApp`
(tests/mcp_catalog_fake.py): FakeApp plus the catalog's read routes.
"""

from __future__ import annotations

import ast
import asyncio
import inspect
import json
import uuid
from pathlib import Path

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from probe.mcp import accounting, contract
from probe.mcp.contract import EnvelopeState, MissingMarker, View
from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors
from tests.conftest import make_client
from tests.mcp_catalog_fake import (
    CHECKER_ID,
    RUN,
    RUN_ID,
    McpCatalogApp,
    dataset_version,
    seed_catalog,
)
from tests.test_mcp_description_budget import TARGET

_CATALOG_PATHS = ("/v1/catalog/", "/v1/sources/", "/v1/provenance")


@pytest.fixture
def catalog() -> McpCatalogApp:
    return McpCatalogApp()


@pytest.fixture
def refs(catalog) -> dict[str, str]:
    return seed_catalog(catalog)


@pytest.fixture
def service(catalog, tmp_path) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(make_client(catalog, tmp_spool=tmp_path / "spool")))


@pytest.fixture
def server(service):
    return create_server(service)


def _call(server, tool: str, args: dict) -> dict:
    result = asyncio.run(server.call_tool(tool, args))
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, list):
        return json.loads(payload[0].text)
    return payload


def _error(server, tool: str, args: dict) -> str:
    with pytest.raises(ToolError) as excinfo:
        _call(server, tool, args)
    return str(excinfo.value)


def _params(app, path: str) -> list[dict]:
    return [dict(r.url.params.multi_items()) for r in app.requests if r.url.path == path]


def _catalog_requests(app) -> list:
    return [r for r in app.requests if r.url.path.startswith(_CATALOG_PATHS)]


def _source(i: int) -> dict:
    sid = str(uuid.uuid4())
    return {
        "id": sid,
        "ref": f"source:{sid}",
        "canonical_key": f"hf:dataset/org/set-{i:02d}",
        "provider": "huggingface",
        "kind": "dataset",
        "revision": "",
        "uri": f"hf://datasets/org/set-{i:02d}",
        "title": f"set {i:02d}",
        "description": "d" * 300,
        "created_at": f"2026-10-01T00:00:{i:02d}Z",
        "updated_at": f"2026-10-01T00:00:{i:02d}Z",
        "counts": {"runs_using": i, "datasets_derived": 0},
    }


# -- browse: each mode reads its own route ------------------------------------


@pytest.mark.parametrize(
    ("args", "path", "sent"),
    [
        (
            {"mode": "datasets", "query": "c4", "project": "project:folding", "registered": "yes", "limit": 5},
            "/v1/catalog/datasets",
            {"q": "c4", "project": "project:folding", "registered": "yes", "limit": "5"},
        ),
        (
            {
                "mode": "checkpoints",
                "project": "project:folding",
                "experiment": "experiment:ablate",
                "run": "run:sft-7b-12",
                "best": True,
                "stored": "stored",
            },
            "/v1/catalog/checkpoints",
            {
                "project": "project:folding",
                "experiment": "experiment:ablate",
                "run": "run:sft-7b-12",
                "best": "true",
                "stored": "stored",
                "limit": "10",
            },
        ),
        (
            {"mode": "sources", "query": "c4", "provider": "huggingface", "kind": "dataset"},
            "/v1/catalog/sources",
            {"q": "c4", "provider": "huggingface", "kind": "dataset", "limit": "10"},
        ),
    ],
)
def test_each_catalog_mode_sends_its_routes_own_filters_and_nothing_else(
    server, catalog, refs, args, path, sent
):
    out = _call(server, "browse", args)
    assert _params(catalog, path) == [sent]
    # Exactly one read, of exactly that route.
    assert [r.url.path for r in _catalog_requests(catalog)] == [path]
    # What narrowed it is echoed in the caller's own names.
    for name, value in args.items():
        if name not in ("mode", "limit"):
            assert out["data"][name] == value


def test_a_dataset_listing_names_each_row_by_the_address_entity_opens(server, catalog, refs):
    unregistered = str(uuid.uuid4())
    catalog.catalog_items["datasets"].append(
        {
            "ref": f"artifact:{unregistered}",
            "id": unregistered,
            "name": "shards/train.jsonl",
            "registered": False,
            "description": None,
            "created_at": "2026-09-01T00:00:00Z",
            "latest": None,
            "versions": 0,
            "used_by_runs": 1,
            "sources": [],
            "locked": False,
        }
    )
    out = _call(server, "browse", {"mode": "datasets"})
    named, loose = out["data"]["datasets"]
    entry = catalog.dataset_details["c4-clean"]
    assert named["entity_type"] == "dataset"
    assert named["slug"] == "dataset:c4-clean"
    assert named["uuid"] == f"dataset:{entry['id']}"
    assert named["latest"]["ref"] == "dataset:c4-clean@3"
    assert "ref" not in named and "id" not in named
    # A run-logged file nobody registered is a FILE, opened as one.
    assert loose["entity_type"] == "artifact"
    assert loose["uuid"] == f"artifact:{unregistered}"
    assert "slug" not in loose
    # Null keys are absent, as on every browse row.
    assert "description" not in loose and "latest" not in loose
    assert set(out["data"]["available_views"]) == {"dataset", "artifact"}
    assert out["data"]["available_views"]["dataset"] == ["card", "lineage", "record", "versions"]

    # Both addresses open the same entry.
    for address in (named["slug"], named["uuid"]):
        card = _call(server, "entity", {"refs": [address]})
        assert card["data"]["entity"]["id"] == entry["id"]


def test_a_checkpoint_listing_carries_the_totals_of_the_whole_filter(server, catalog, refs):
    catalog.checkpoint_totals = {"bytes": 7_000_000, "count": 1, "by_project": []}
    out = _call(server, "browse", {"mode": "checkpoints"})
    (row,) = out["data"]["checkpoints"]
    assert row["entity_type"] == "checkpoint"
    assert row["uuid"] == refs["checkpoint"]
    assert row["run"] == RUN and row["step"] == 4000
    assert "rewound" not in row and "experiment" not in row  # null, so absent
    assert out["data"]["totals"] == catalog.checkpoint_totals


def test_a_source_row_offers_its_readable_key_and_both_addresses_open_it(server, catalog, refs):
    out = _call(server, "browse", {"mode": "sources"})
    (row,) = out["data"]["sources"]
    assert row["uuid"] == refs["source"]
    assert row["slug"] == "source:hf:dataset/allenai/c4@main"
    assert row["counts"] == {"runs_using": 2, "datasets_derived": 1}
    for address in (row["uuid"], row["slug"]):
        card = _call(server, "entity", {"refs": [address]})
        assert card["data"]["entity"]["canonical_key"] == "hf:dataset/allenai/c4"


# -- browse: refuse, never drop ---------------------------------------------------


@pytest.mark.parametrize(
    ("args", "refused", "reader"),
    [
        ({"mode": "datasets", "run": "run:x"}, "run", "checkpoints"),
        ({"mode": "datasets", "provider": "s3"}, "provider", "sources"),
        ({"mode": "datasets", "best": True}, "best", "checkpoints"),
        ({"mode": "checkpoints", "query": "c4"}, "query", "datasets or notes or sources"),
        ({"mode": "checkpoints", "registered": "yes"}, "registered", "datasets"),
        ({"mode": "checkpoints", "kind": "model"}, "kind", "sources"),
        ({"mode": "sources", "project": "project:x"}, "project", "checkpoints or datasets"),
        ({"mode": "sources", "stored": "stored"}, "stored", "checkpoints"),
        ({"mode": "sources", "experiment": "experiment:x"}, "experiment", "checkpoints"),
        ({"mode": "notes", "provider": "s3"}, "provider", "sources"),
        ({"mode": "files", "registered": "no"}, "registered", "datasets"),
        ({"run": "run:x"}, "run", "checkpoints"),
        ({"mode": "datasets", "status": "running"}, "status", "runs or tree"),
        ({"mode": "sources", "prefix": "hf"}, "prefix", "files"),
    ],
)
def test_an_argument_a_catalog_mode_does_not_read_is_refused_naming_its_reader(
    server, catalog, args, refused, reader
):
    message = _error(server, "browse", args)
    mode = args.get("mode", "tree")
    assert f"mode={mode} does not read {refused}" in message
    assert f"read by mode={reader}" in message
    assert not _catalog_requests(catalog), "refused AFTER a listing was read"


def test_a_catalog_listing_refuses_ref_and_names_its_own_scoping_filters(server, catalog):
    message = _error(server, "browse", {"mode": "checkpoints", "ref": "run:sft-7b-12"})
    assert "mode=checkpoints does not read ref" in message
    assert "narrows by `project`" in message and "`run`" in message
    assert not _catalog_requests(catalog)


@pytest.mark.parametrize("mode", ["datasets", "checkpoints", "sources", "runs", "notes", "files"])
def test_best_false_asks_for_nothing_in_every_flat_mode(server, catalog, refs, mode):
    out = _call(server, "browse", {"mode": mode, "best": False})
    assert "data" in out
    if mode == "checkpoints":
        assert "best" not in _params(catalog, "/v1/catalog/checkpoints")[-1]


# -- browse: paging over the route's own cursor ------------------------------------


def _walk(server, args: dict, key: str, mutate=None) -> list[str]:
    seen: list[str] = []
    cursor = None
    for _ in range(40):
        page = _call(server, "browse", {**args, **({"cursor": cursor} if cursor else {})})
        seen += [row["uuid"] for row in page["data"][key]]
        cursor = page.get("next_cursor")
        if not cursor:
            return seen
        if mutate is not None:
            mutate(seen)
    raise AssertionError("walk did not end")


def _newest_first(rows: list[dict]) -> list[str]:
    return [row["ref"] for row in sorted(rows, key=lambda r: (r["created_at"], r["id"]), reverse=True)]


def test_a_budget_cut_catalog_walk_delivers_every_row_exactly_once(server, catalog):
    rows = [_source(i) for i in range(9)]
    catalog.catalog_items["sources"] = list(rows)
    seen = _walk(server, {"mode": "sources", "limit": 4, "token_budget": 512}, "sources")
    assert seen == _newest_first(rows)
    sent = _params(catalog, "/v1/catalog/sources")
    # More reads than pages of 4: the budget cut inside a page, and each cut
    # resumed from the SAME route position (re-read at the route's ceiling),
    # never from a count of rows to skip.
    assert len(sent) > 3
    assert all(p["limit"] in ("4", "100") for p in sent)
    assert {p["limit"] for p in sent if "cursor" not in p} >= {"4"}


def test_rows_registered_mid_walk_do_not_push_the_resume_point_off_its_page(server, catalog):
    rows = [_source(i) for i in range(9)]
    catalog.catalog_items["sources"] = list(rows)
    added: list[dict] = []

    def register_newer(_seen: list[str]) -> None:
        # A whole page's worth: re-read at the page size, the row the cut
        # stopped after would be pushed off it and the walk refused.
        for _ in range(6):
            fresh = _source(50 + len(added))
            added.append(fresh)
            catalog.catalog_items["sources"].append(fresh)

    seen = _walk(server, {"mode": "sources", "limit": 6, "token_budget": 512}, "sources", register_newer)
    # Every row that existed when the walk began, each once, in order; rows
    # registered since sit ABOVE the walk and are the next walk's.
    assert seen == _newest_first(rows)


def test_a_row_deleted_inside_a_page_is_refused_never_skipped(server, catalog):
    rows = [_source(i) for i in range(9)]
    catalog.catalog_items["sources"] = list(rows)
    first = _call(server, "browse", {"mode": "sources", "limit": 9, "token_budget": 512})
    sent = first["data"]["sources"]
    assert 0 < len(sent) < 9 and first["next_cursor"]
    catalog.catalog_items["sources"] = [r for r in rows if r["ref"] != sent[-1]["uuid"]]
    message = _error(
        server,
        "browse",
        {"mode": "sources", "limit": 9, "token_budget": 512, "cursor": first["next_cursor"]},
    )
    assert "source_changed" in message and "restart" in message


def test_a_cursor_from_another_catalog_listing_is_refused(server, catalog, refs):
    rows = [_source(i) for i in range(9)]
    catalog.catalog_items["sources"] = rows
    first = _call(server, "browse", {"mode": "sources", "limit": 9, "token_budget": 512})
    assert first["next_cursor"]
    with pytest.raises(ToolError):
        _call(server, "browse", {"mode": "datasets", "cursor": first["next_cursor"]})


def _features_reads(app) -> int:
    return sum(1 for r in app.requests if r.url.path == "/v1/server/features")


def test_a_server_without_the_catalog_says_so_rather_than_answering_empty(server, catalog):
    """Decided by `GET /v1/server/features` (no `catalog`), asked once per
    source, never by the 404's wording."""
    catalog.supports_catalog = False
    message = _error(server, "browse", {"mode": "datasets"})
    assert "predates the data catalog" in message
    out = _call(server, "entity", {"refs": ["dataset:c4-clean"]})
    assert "predates the data catalog" in out["missing"][0]["reason"]
    assert _features_reads(catalog) == 1


def test_a_bare_404_from_a_catalog_server_is_not_found_not_an_old_server(
    server, catalog, refs
):
    """FastAPI's bare "Not Found" also answers a catalog server's route that a
    ref did not match. With `catalog` declared it is the answer -- no such
    checkpoint -- not "this server predates the catalog"."""
    catalog.bare_404 = True
    out = _call(server, "entity", {"refs": [f"checkpoint:{uuid.uuid4()}"]})
    reason = out["missing"][0]["reason"]
    assert reason.startswith("NotFoundError") and "Not Found" in reason
    assert "predates" not in reason
    _call(server, "entity", {"refs": [f"checkpoint:{uuid.uuid4()}"]})
    assert _features_reads(catalog) == 1  # cached on this source


@pytest.mark.parametrize(
    ("ref", "says"),
    [
        ("dataset:allenai/c4", "is a `source:` ref"),
        ("dataset:C4-Clean", "not a dataset name"),
        ("dataset:c4 clean", "not a dataset name"),
        ("dataset:-c4", "not a dataset name"),
        ("dataset:" + "a" * 129, "not a dataset name"),
        ("dataset:c4-clean@x", "unknown dataset version 'x'"),
        ("dataset:c4-clean@V2", "unknown dataset version 'V2'"),
    ],
)
def test_a_ref_outside_the_dataset_grammar_is_refused_before_any_request(
    server, catalog, refs, ref, says
):
    """`dataset:allenai/c4` used to reach the route as `%2F`, miss its one-
    segment `{ref}` and come back as FastAPI's bare 404 -- read as an old
    server, or as no such dataset."""
    out = _call(server, "entity", {"refs": [ref]})
    reason = out["missing"][0]["reason"]
    assert reason.startswith("ValidationError") and says in reason
    assert "lower-case letters" in reason or "unknown dataset version" in reason
    assert not _catalog_requests(catalog) and not _features_reads(catalog)


@pytest.mark.parametrize(
    "suffix", ["", "@3", "@v3", "@latest", "@LATEST", " @ 3 "],
)
def test_every_form_of_the_dataset_grammar_reaches_the_route(server, catalog, refs, suffix):
    entry_id = catalog.dataset_details["c4-clean"]["id"]
    for key in ("c4-clean", entry_id, entry_id.upper()):
        out = _call(server, "entity", {"refs": [f"dataset:{key}{suffix}"]})
        assert out["data"]["entity"]["id"] == entry_id


# -- entity: datasets ---------------------------------------------------------------


def test_a_dataset_card_shows_the_entry_and_its_latest_version_with_lists_counted(
    server, catalog, refs
):
    out = _call(server, "entity", {"refs": ["dataset:c4-clean"]})
    data = out["data"]
    assert data["entity_type"] == "dataset"
    assert data["entity"]["ref"] == "dataset:c4-clean"
    assert data["entity"]["registered"] is True
    assert data["entity"]["description"].startswith("C4, deduplicated")
    assert data["available_views"] == ["card", "lineage", "record", "versions"]
    assert data["version_count"] == 3
    version = data["version"]
    assert version["n"] == 3 and version["ref"] == "dataset:c4-clean@3"
    assert version["producer"]["run"]["ref"] == RUN["ref"]
    assert version["change"]["note"] == "dedup pass 3"
    # The heavy parts are counted, not listed; the versions view has them.
    # The server's exact count, not the length of its capped list.
    assert version["users"] == {"stored": 23, "derived": 0, "truncated": True}
    assert version["checks"] == 1
    assert "step" not in version and "meta" not in version
    assert "completeness" not in out
    assert [r.url.raw_path.decode() for r in _catalog_requests(catalog)] == [
        "/v1/catalog/datasets/dataset:c4-clean"
    ]


@pytest.mark.parametrize("selector", ["@2", "@v2"])
def test_a_pinned_dataset_ref_shows_the_version_it_names(server, catalog, refs, selector):
    data = _call(server, "entity", {"refs": [f"dataset:c4-clean{selector}"]})["data"]
    assert data["version"]["n"] == 2
    assert _catalog_requests(catalog)[-1].url.raw_path.decode() == (
        f"/v1/catalog/datasets/dataset:c4-clean{selector}"
    )


def test_a_dataset_by_uuid_reads_the_same_entry(server, catalog, refs):
    entry = catalog.dataset_details["c4-clean"]
    data = _call(server, "entity", {"refs": [f"dataset:{entry['id']}@latest"]})["data"]
    assert data["entity"]["name"] == "c4-clean" and data["version"]["n"] == 3


def test_dataset_versions_are_every_version_newest_first_whole(server, catalog, refs):
    data = _call(
        server, "entity", {"refs": ["dataset:c4-clean"], "view": "versions", "token_budget": 8000}
    )["data"]
    assert [v["n"] for v in data["versions"]] == [3, 2, 1]
    assert data["versions"][0]["step"] == {"config": {"lr": 3e-4}, "code_ref": "abc123", "recorded_after": False}
    assert data["versions"][0]["users"]["stored"][0]["roles"] == ["train"]


@pytest.mark.parametrize("view", ["card", "versions", "lineage", "record"])
def test_a_missing_dataset_version_is_no_match_with_the_versions_that_exist(
    server, catalog, refs, view
):
    """The dataset EXISTS and version 7 does not: the reuse check's no_match,
    never absence -- absence licenses a new name, this says pin 1-3 or
    register the next version of the SAME one."""
    out = _call(server, "entity", {"refs": ["dataset:c4-clean@7"], "view": view})
    assert out["completeness"]["state"] == EnvelopeState.NO_MATCH
    data = out["data"]
    assert data["satisfied_by"] is None
    assert data["versions"] == [1, 2, 3]
    assert data["highest_version"] == 3 and data["version_count"] == 3
    assert data["requested"] == "dataset:c4-clean@7"
    assert "no version 7" in data["message"]
    assert not _params(catalog, "/v1/provenance")


def test_an_unknown_dataset_is_absent_not_no_match(server, catalog, refs):
    out = _call(server, "entity", {"refs": ["dataset:never-registered"]})
    assert out["rows"] == []
    assert "dataset not found" in out["missing"][0]["reason"]


# -- entity: checkpoints --------------------------------------------------------------


def test_a_checkpoint_card_is_its_overview_read(server, catalog, refs):
    selector = f"checkpoint:{RUN['ref']}@best"
    data = _call(server, "entity", {"refs": [selector]})["data"]
    entity = data["entity"]
    assert entity["ref"] == refs["checkpoint"]
    assert entity["step"] == 4000 and entity["best"] == {"monitor": "val/loss", "score": 1.23}
    assert entity["stored"] == "stored" and entity["telemetry"] == "live"
    assert entity["run"] == RUN
    assert data["at_step"][0]["key"] == "val/loss"
    assert data["inputs_at_save"][0]["ref"] == "dataset:c4-clean@3"
    assert data["inputs_source"] == "inputs_at_save"
    assert "saves" not in data and "saves" not in entity
    assert data["available_views"] == ["card", "lineage", "record", "versions"]
    # A run-selector ref rides the path whole and readable.
    assert _catalog_requests(catalog)[-1].url.raw_path.decode() == (
        "/v1/catalog/checkpoints/checkpoint:run:sft-7b-12@best"
    )


def test_checkpoint_versions_are_the_runs_saves(server, catalog, refs):
    out = _call(server, "entity", {"refs": [refs["checkpoint"]], "view": "versions"})
    assert [s["step"] for s in out["data"]["saves"]] == [4000, 2000]
    assert "completeness" not in out


def test_saves_past_the_checkpoint_reads_page_are_reported_with_where_to_read_them(
    server, catalog, refs
):
    catalog.checkpoint_details[refs["checkpoint"]]["saves_next_cursor"] = "more"
    out = _call(server, "entity", {"refs": [refs["checkpoint"]], "view": "versions"})
    assert out["completeness"]["missing"] == [MissingMarker.SAVES_BEYOND_SERVER_PAGE]
    assert out["data"]["more_saves"] == f'browse(mode="checkpoints", run="{RUN["ref"]}")'


# -- entity: sources --------------------------------------------------------------------


def test_a_source_card_by_key_rides_one_path_segment(server, catalog, refs):
    data = _call(server, "entity", {"refs": ["source:hf:dataset/allenai/c4@main"]})["data"]
    entity = data["entity"]
    assert entity["provider"] == "huggingface" and entity["revision"] == "main"
    assert entity["license"] == "odc-by"
    assert entity["counts"] == {"runs_using": 2, "datasets_derived": 1}
    assert data["available_views"] == ["card", "lineage", "record"]
    assert _catalog_requests(catalog)[-1].url.raw_path.decode() == (
        "/v1/sources/source:hf:dataset%2Fallenai%2Fc4@main"
    )


def test_a_source_has_no_versions_and_the_refusal_names_its_views(service, server, refs):
    with pytest.raises(errors.ValidationError) as excinfo:
        service.get_entity(refs["source"], view=View.VERSIONS)
    message = str(excinfo.value)
    assert "source supports" in message
    for view in ("card", "lineage", "record"):
        assert f"  {view}" in message
    out = _call(server, "entity", {"refs": [refs["source"]], "view": "versions"})
    assert out["rows"] == [] and "source supports" in out["missing"][0]["reason"]


# -- entity: lineage is the provenance walk ------------------------------------------------


def test_lineage_walks_upstream_four_hops_from_the_version_the_card_shows(server, catalog, refs):
    out = _call(server, "entity", {"refs": ["dataset:c4-clean"], "view": "lineage"})
    assert _params(catalog, "/v1/provenance") == [
        {"ref": "dataset:c4-clean@3", "direction": "upstream", "depth": "4"}
    ]
    data = out["data"]
    version = catalog.dataset_details["c4-clean"]["versions"][0]
    assert data["root"] == f"artifact_version:{version['id']}"
    assert data["nodes"][0]["type"] == "source"
    assert data["truncated"] is False and data["hidden"] == 0


@pytest.mark.parametrize(
    ("ref_key", "root_key"),
    [("checkpoint", "checkpoint"), ("source", "source")],
)
def test_lineage_is_rooted_at_the_resolved_ref(server, catalog, refs, ref_key, root_key):
    asked = (
        f"checkpoint:{RUN['ref']}@best" if ref_key == "checkpoint" else "source:hf:dataset/allenai/c4@main"
    )
    _call(
        server,
        "entity",
        {
            "refs": [asked],
            "view": "lineage",
            "view_options": {"direction": "downstream", "depth": 8},
        },
    )
    assert _params(catalog, "/v1/provenance") == [
        {"ref": refs[root_key], "direction": "downstream", "depth": "8"}
    ]


def test_lineage_steps_is_the_methods_view(server, catalog, refs):
    out = _call(
        server,
        "entity",
        {"refs": ["dataset:c4-clean@3"], "view": "lineage", "view_options": {"steps": True}},
    )
    assert _params(catalog, "/v1/provenance") == [{"ref": "dataset:c4-clean@3", "format": "steps"}]
    assert out["data"]["steps"][0]["order"] == 1
    assert out["data"]["sources"][0]["ref"] == refs["source"]


@pytest.mark.parametrize(
    ("options", "says"),
    [
        ({"depth": 9}, "depth must be an integer from 1 to 8"),
        ({"depth": 0}, "depth must be an integer from 1 to 8"),
        ({"depth": "deep"}, "depth must be an integer from 1 to 8"),
        ({"depth": True}, "depth must be an integer from 1 to 8"),
        ({"direction": "sideways"}, "direction must be one of"),
        ({"steps": True, "direction": "downstream"}, "takes no direction"),
        ({"steps": True, "depth": 2}, "takes no depth"),
        ({"steps": "yes"}, "steps must be true or false"),
        ({"compare_to": "run:x"}, "unknown view option(s) ['compare_to']"),
    ],
)
def test_lineage_options_outside_the_route_are_refused_before_any_walk(
    service, catalog, refs, options, says
):
    with pytest.raises(errors.ValidationError) as excinfo:
        service.get_entity("dataset:c4-clean", view=View.LINEAGE, filters=options)
    assert says in str(excinfo.value)
    assert not _params(catalog, "/v1/provenance")


# -- what did NOT change ------------------------------------------------------------------


def test_the_reuse_check_still_reads_shared_by_name_and_sees_catalog_entries(
    service, catalog, refs
):
    """`artifact:<name>` is the Shared reuse check, unchanged. A catalog dataset
    entry IS a Shared row (kind `dataset`), so the check still sees it."""
    entry_id = catalog.dataset_details["c4-clean"]["id"]
    catalog.artifacts["shared:team"] = [
        {
            "id": entry_id,
            "customer_id": "lab-42",
            "name": "c4-clean",
            "kind": "dataset",
            "status": "complete",
            "is_reference": True,
            "size_bytes": 3000,
            "created_at": "2026-10-01T00:00:00Z",
        }
    ]
    out = service.get_entity("artifact:c4-clean")
    assert out["data"]["entity_type"] == "artifact"
    assert out["data"]["entity"]["id"] == entry_id
    assert not _catalog_requests(catalog)
    assert any(r.url.path == "/v1/shared/files" for r in catalog.requests)
    with pytest.raises(errors.NotFoundError, match="SHARED level"):
        service.get_entity("artifact:never-shared")


def test_an_unknown_ref_kind_lists_the_catalog_kinds(service):
    with pytest.raises(errors.ValidationError) as excinfo:
        service.get_entity("datset:c4-clean")
    message = str(excinfo.value)
    for kind in ("dataset", "source", "checkpoint", "artifact"):
        assert f"'{kind}'" in message


def test_the_descriptions_teach_the_catalog_within_the_client_cap(server):
    tools = {t.name: t for t in asyncio.run(server.list_tools())}
    browse = inspect.cleandoc(tools["browse"].description)[:2048]
    for mode in ("`datasets`", "`checkpoints`", "`sources`"):
        assert mode in browse
    entity = inspect.cleandoc(tools["entity"].description)
    # The forms ride `refs`'s schema (uncapped); the description points there,
    # and keeps the headroom the budget test asks for.
    assert len(entity) <= TARGET
    assert len(inspect.cleandoc(tools["browse"].description)) <= TARGET
    assert "`dataset:`, `source:`, `checkpoint:` - forms in `refs`" in entity
    assert "`artifact:<name>` for the shared-registry reuse check" in entity
    schema = tools["entity"].inputSchema["properties"]
    refs_doc = schema["refs"]["description"]
    for form in (
        "`dataset:<name>[@<N>|@v<N>|@latest]`",
        "`dataset:<uuid>`",
        "`source:<canonical_key>[@<revision>]`",
        "`checkpoint:<run ref>@best[:<callback>]|latest|step<N>`",
    ):
        assert form in refs_doc
    assert "`artifact:<name>` stays the Shared reuse check" in refs_doc
    for kind in ("dataset", "source", "checkpoint"):
        assert any(
            line.strip().startswith(kind + " ") for line in schema["view"]["description"].splitlines()
        )


# -- the dataset read's `selected` and `versions_truncated` ------------------------------


def _capped(catalog, shown: int) -> list[dict]:
    """The c4-clean entry with 5 versions, its list capped at the newest
    `shown` as the server caps it at 200."""
    every = [dataset_version(n) for n in (5, 4, 3, 2, 1)]
    entry = catalog.dataset_details["c4-clean"]
    entry["_all_versions"] = every
    entry["versions"] = every[:shown]
    entry["versions_truncated"] = True
    return every


def test_the_card_shows_the_servers_selected_version_even_past_the_cap(server, catalog, refs):
    every = _capped(catalog, 2)
    data = _call(server, "entity", {"refs": ["dataset:c4-clean@1"]})["data"]
    assert data["version"]["n"] == 1 and data["version"]["ref"] == every[-1]["ref"]
    assert data["versions_truncated"] is True and data["version_count"] == 2
    _call(server, "entity", {"refs": ["dataset:c4-clean@1"], "view": "lineage"})
    assert _params(catalog, "/v1/provenance")[-1]["ref"] == "dataset:c4-clean@1"


def test_the_versions_view_says_the_list_stopped_at_the_cap(server, catalog, refs):
    _capped(catalog, 2)
    data = _call(server, "entity", {"refs": ["dataset:c4-clean"], "view": "versions"})["data"]
    assert [v["n"] for v in data["versions"]] == [5, 4]
    assert data["versions_truncated"] is True


def test_a_full_list_says_so_too(server, catalog, refs):
    card = _call(server, "entity", {"refs": ["dataset:c4-clean"]})["data"]
    assert card["versions_truncated"] is False
    versions = _call(server, "entity", {"refs": ["dataset:c4-clean"], "view": "versions"})["data"]
    assert versions["versions_truncated"] is False


def test_an_older_server_without_selected_still_shows_the_version_named(server, catalog, refs):
    catalog.sends_selected = False
    data = _call(server, "entity", {"refs": ["dataset:c4-clean@2"]})["data"]
    assert data["version"]["n"] == 2
    assert "versions_truncated" not in data


# -- X-Probe-Hide-Session-Work over the provenance walk ------------------------------------


class _CreatedSource(ResearchOSSource):
    def __init__(self, client, created):
        super().__init__(client)
        self.created = created

    def session_created(self, session_id):
        return self.created


def _hiding_service(catalog, tmp_path, run_ids: list[str]) -> ResearchReadService:
    client = make_client(catalog, tmp_spool=tmp_path / "hide-spool")
    return ResearchReadService(_CreatedSource(client, {"project_ids": [], "run_ids": run_ids}))


def _as_reader(service, *args, **kwargs) -> dict:
    state = accounting.begin_request(
        "claude_code", str(uuid.uuid4()), {}, hide_session_work=True
    )
    try:
        return service.get_entity(*args, **kwargs)
    finally:
        accounting.end_request(state)


@pytest.mark.parametrize("kind", ["dataset", "checkpoint", "source"])
def test_the_hidden_sessions_run_leaves_the_lineage_graph_with_its_edges(
    catalog, refs, tmp_path, kind
):
    """Provenance nodes are TYPED (`run:<uuid>`) and edges name them by
    `from` / `to`; the session-work scrub matched bare ids only, so the
    reader's own run stayed in every lineage graph."""
    service = _hiding_service(catalog, tmp_path, [RUN_ID.upper()])
    data = _as_reader(service, refs[kind], view=View.LINEAGE)["data"]
    ids = {node["id"] for node in data["nodes"]}
    assert f"run:{RUN_ID}" not in ids
    assert f"run:{CHECKER_ID}" in ids and any(i.startswith("source:") for i in ids)
    assert data["edges"], "the other run's edge stays"
    for edge in data["edges"]:
        assert RUN_ID not in (edge["from"].partition(":")[2], edge["to"].partition(":")[2])
    # Every edge left names nodes still in the graph.
    assert {e["from"] for e in data["edges"]} | {e["to"] for e in data["edges"]} <= ids


def test_the_hidden_sessions_run_leaves_the_methods_view(catalog, refs, tmp_path):
    service = _hiding_service(catalog, tmp_path, [RUN_ID])
    data = _as_reader(
        service, "dataset:c4-clean", view=View.LINEAGE, filters={"steps": True}
    )["data"]
    assert [step["run"]["id"] for step in data["steps"]] == [CHECKER_ID]


def test_without_the_header_the_graph_is_whole(catalog, refs, tmp_path):
    service = _hiding_service(catalog, tmp_path, [RUN_ID])
    data = service.get_entity("dataset:c4-clean", view=View.LINEAGE)["data"]
    assert f"run:{RUN_ID}" in {node["id"] for node in data["nodes"]}
    assert len(data["edges"]) == 3


# -- X-Probe-Hide-Session-Work over the catalog listings ------------------------------------

_CHECKER = {"id": CHECKER_ID, "ref": "run:eval-3", "name": "eval", "slug": "eval-3", "status": "completed"}


def _list_as_reader(service, mode: str, **kwargs) -> dict:
    state = accounting.begin_request("claude_code", str(uuid.uuid4()), {}, hide_session_work=True)
    try:
        return service.browse_list(mode, **kwargs)
    finally:
        accounting.end_request(state)


def _save(i: int, run: dict | None, *, project: dict | None = None) -> dict:
    cid = str(uuid.uuid4())
    return {
        "ref": f"checkpoint:{cid}",
        "id": cid,
        "name": f"step-{i}.pt",
        "step": i,
        "stored": "reference",
        "size_bytes": 10,
        "created_at": f"2026-10-05T00:00:{i:02d}Z",
        "run": run,
        "project": project,
        "locked": False,
    }


def _loose_file(i: int, run: dict) -> dict:
    aid = str(uuid.uuid4())
    return {
        "ref": f"artifact:{aid}",
        "id": aid,
        "name": f"shards/{i}.jsonl",
        "registered": False,
        "created_at": f"2026-09-01T00:00:{i:02d}Z",
        "latest": {"ref": f"artifact:{aid}", "producer": {"run": run, "project": None}, "locked": False},
        "versions": 1,
        "used_by_runs": 0,
        "sources": [],
        "locked": False,
    }


def test_the_hidden_sessions_checkpoints_leave_the_checkpoint_listing(catalog, refs, tmp_path):
    """`runs`, `notes` and lineage left out the reader's own session's work;
    `checkpoints` listed every save its runs made. A save is the session's when
    its run is (saved with no run: when the project it is filed at is)."""
    session_project = {"id": str(uuid.uuid4()), "slug": "mine", "name": "Mine"}
    theirs = _save(30, _CHECKER)
    catalog.catalog_items["checkpoints"] += [theirs, _save(31, None, project=session_project)]
    catalog.checkpoint_totals = {"bytes": 7_000_020, "count": 3, "by_project": []}
    service = _hiding_service(catalog, tmp_path, [RUN_ID.upper(), session_project["id"]])
    data = _list_as_reader(service, "checkpoints")["data"]
    assert [row["uuid"] for row in data["checkpoints"]] == [theirs["ref"]]
    # Counted over the hidden saves too, and named by project: not sent.
    assert "totals" not in data
    whole = service.browse_list("checkpoints")["data"]
    assert len(whole["checkpoints"]) == 3 and whole["totals"] == catalog.checkpoint_totals


def test_the_hidden_sessions_datasets_leave_the_dataset_listing(catalog, refs, tmp_path):
    """A file the session's run logged, and a dataset whose newest version that
    run wrote (the session already knows it), are its own work; a dataset
    another run made stays."""
    mine, theirs = _loose_file(1, RUN), _loose_file(2, _CHECKER)
    catalog.catalog_items["datasets"] += [mine, theirs]
    service = _hiding_service(catalog, tmp_path, [RUN_ID])
    data = _list_as_reader(service, "datasets")["data"]
    assert [row["uuid"] for row in data["datasets"]] == [theirs["ref"]]
    assert len(service.browse_list("datasets")["data"]["datasets"]) == 3


def test_a_source_listing_names_no_session_work(catalog, refs, tmp_path):
    service = _hiding_service(catalog, tmp_path, [RUN_ID])
    out = _list_as_reader(service, "sources")
    assert [row["uuid"] for row in out["data"]["sources"]] == [refs["source"]]
    assert "completeness" not in out  # compact: complete, nothing missing


def test_a_page_of_only_the_sessions_saves_reads_on_and_the_walk_skips_none(catalog, tmp_path):
    """A page the session's own saves fill reads the next one, and every save
    of another run is delivered once, in order, whatever page it sat on."""
    saves = [_save(i, RUN if i % 3 else _CHECKER) for i in range(1, 10)]
    catalog.catalog_items["checkpoints"] = list(saves)
    service = _hiding_service(catalog, tmp_path, [RUN_ID])
    seen, cursor = [], None
    for _ in range(20):
        out = _list_as_reader(service, "checkpoints", limit=2, cursor=cursor)
        seen += [row["uuid"] for row in out["data"]["checkpoints"]]
        cursor = out.get("next_cursor")
        # Only the last page may come back empty: the hidden tail of the listing.
        assert out["data"]["checkpoints"] or not cursor, "a page of hidden saves read on"
        if not cursor:
            break
    expected = [s["ref"] for s in sorted(saves, key=lambda s: s["created_at"], reverse=True) if s["run"] is _CHECKER]
    assert seen == expected


def test_a_listing_past_the_fill_bound_says_its_page_was_hidden(catalog, tmp_path):
    catalog.catalog_items["checkpoints"] = [_save(i, RUN) for i in range(1, 30)]
    service = _hiding_service(catalog, tmp_path, [RUN_ID])
    out = _list_as_reader(service, "checkpoints", limit=2)
    assert out["data"]["checkpoints"] == [] and out["next_cursor"]
    assert MissingMarker.PAGE_HIDDEN_AS_OWN_SESSION_WORK in out["completeness"]["missing"]


def test_a_server_that_cannot_say_what_the_session_made_marks_the_listing(catalog, refs, tmp_path):
    class _Blind(ResearchOSSource):
        def session_created(self, session_id):
            raise errors.NotFoundError("Not Found", status=404)

    service = ResearchReadService(_Blind(make_client(catalog, tmp_spool=tmp_path / "blind")))
    out = _list_as_reader(service, "checkpoints")
    assert len(out["data"]["checkpoints"]) == 1
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED in out["completeness"]["missing"]


# -- the catalog vocabulary this client sends, held to the server's ------------------------

_REPO = Path(__file__).resolve().parents[2]


def _server_enum(relpath: str, name: str) -> dict[str, str]:
    """`{member: value}` of StrEnum `name` in the server source, read by AST
    (this package never imports `app/`). A value is a string literal or a
    module constant (`dataset_reads.REGISTERED_ALL`), resolved through that
    file's `from app.x import module`."""
    path = _REPO / relpath
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules = {
        alias.asname or alias.name: _REPO / Path(*node.module.split("."), f"{alias.name}.py")
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module
        for alias in node.names
    }

    def constant(module: Path, attr: str) -> str:
        for node in ast.parse(module.read_text(encoding="utf-8")).body:
            if (
                isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == attr for t in node.targets)
                and isinstance(node.value, ast.Constant)
            ):
                return node.value.value
        raise AssertionError(f"{attr} is not a constant in {module}")

    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name)
    values: dict[str, str] = {}
    for node in cls.body:
        if not (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)):
            continue
        value = node.value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            values[node.targets[0].id] = value.value
        elif isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name):
            values[node.targets[0].id] = constant(modules[value.value.id], value.attr)
        else:
            raise AssertionError(f"{name}.{node.targets[0].id}: a value this test cannot read")
    return values


@pytest.mark.parametrize(
    ("client", "relpath", "server"),
    [
        (contract.ProvenanceDirection, "app/catalog/provenance.py", "Direction"),
        (contract.DatasetRegistered, "app/catalog/router.py", "Registered"),
        (contract.CheckpointStored, "app/catalog/router.py", "StoredState"),
        (contract.SourceKind, "app/core/catalog_vocab.py", "SourceKind"),
        (contract.SourceProvider, "app/core/catalog_vocab.py", "SourceProvider"),
    ],
)
def test_the_catalog_vocabulary_matches_the_servers_value_for_value(client, relpath, server):
    if not (_REPO / relpath).is_file():
        pytest.skip("no server source beside the agent")
    assert {m.name: m.value for m in client} == _server_enum(relpath, server)


def test_browse_offers_the_vocabulary_as_schema_enums(server):
    """Typed, so a typo is refused before a request is built, naming every
    valid value."""
    tools = {t.name: t for t in asyncio.run(server.list_tools())}
    defs = tools["browse"].inputSchema["$defs"]
    for enum in (
        contract.DatasetRegistered,
        contract.CheckpointStored,
        contract.SourceKind,
        contract.SourceProvider,
    ):
        assert defs[enum.__name__]["enum"] == [m.value for m in enum]
    message = _error(server, "browse", {"mode": "sources", "provider": "huggingfac"})
    assert "huggingface" in message
