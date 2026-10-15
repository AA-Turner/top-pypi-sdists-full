"""The data catalog's READ routes, faked for the hosted MCP's tests (data-catalog T7).

`McpCatalogApp` is the ordinary `FakeApp` plus the GETs the MCP's catalog
browse modes and entity refs read, shaped as the plan's Interfaces section
(and the server lane building them) spell them:

    GET /v1/catalog/datasets?q&project&registered&cursor&limit
    GET /v1/catalog/datasets/{ref}        `selected` + `versions_truncated`; 404 {message,
                                          state:"no_match", versions} for a missing version
    GET /v1/catalog/checkpoints?project&experiment&run&best&stored&cursor&limit
    GET /v1/catalog/checkpoints/{ref}
    GET /v1/catalog/sources?q&provider&kind&cursor&limit
    GET /v1/sources/{ref}
    GET /v1/provenance?ref&direction&depth | ?ref&format=steps

Every other request falls through to `FakeApp`, whose `GET /v1/server/features`
gains `catalog` while `supports_catalog` holds. False plays a server that
predates the catalog: no `catalog` feature, and every catalog route FastAPI's own
404. A dataset `{ref}` is ONE path segment, as on the server (no `:path`), so a
ref with a `/` in it misses the route and gets that same bare 404. `bare_404`
answers every resolver miss that way too (a catalog server whose 404 says
nothing). `sends_selected=False` plays a server that predates `selected`.

The lists page on a `(created_at, id)` keyset in a cursor format that is NOT
the shared one (`app/core/pagination.py`) on purpose: the MCP must resume a
mid-page cut without knowing it.
"""

from __future__ import annotations

import re
import uuid
from typing import Any

import httpx

from tests.conftest import FakeApp

_LIST = re.compile(r"^/v1/catalog/(datasets|checkpoints|sources)$")
_DETAIL = re.compile(r"^/v1/(catalog/datasets|catalog/checkpoints|sources)/(.+)$")
_DATASET_SEGMENT = re.compile(r"^/v1/catalog/datasets/[^/]+$")
_ROUTE_MISS = {"detail": "Not Found"}
_DETAIL_KIND = {"catalog/datasets": "dataset", "catalog/checkpoints": "checkpoint", "sources": "source"}
_SELECTOR = re.compile(r"^v?(\d+)$")


def _key(item: dict) -> tuple[str, str]:
    return (str(item["created_at"]), str(item["id"]))


class McpCatalogApp(FakeApp):
    def __init__(self) -> None:
        super().__init__()
        #: Newest first, as each route orders them.
        self.catalog_items: dict[str, list[dict]] = {"datasets": [], "checkpoints": [], "sources": []}
        self.checkpoint_totals: dict | None = None
        #: Dataset details by entry name, versions newest first.
        self.dataset_details: dict[str, dict] = {}
        #: Checkpoint / source details by EVERY ref that resolves to them.
        self.checkpoint_details: dict[str, dict] = {}
        self.source_details: dict[str, dict] = {}
        #: Provenance answers by root ref.
        self.graphs: dict[str, dict] = {}
        self.steps: dict[str, dict] = {}
        self.supports_catalog = True
        self.bare_404 = False
        self.sends_selected = True

    def _dispatch(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "GET" and path == "/v1/server/features":
            answer = super()._dispatch(request)
            if answer.status_code != 200 or not self.supports_catalog:
                return answer
            features = answer.json()["features"]
            return httpx.Response(200, json={"features": [*features, "catalog"]})
        if request.method != "GET" or not (
            _LIST.match(path) or _DETAIL.match(path) or path == "/v1/provenance"
        ):
            return super()._dispatch(request)
        self.requests.append(request)
        if not self.supports_catalog:
            return httpx.Response(404, json=_ROUTE_MISS)
        if path.startswith("/v1/catalog/datasets/") and not _DATASET_SEGMENT.match(path):
            return httpx.Response(404, json=_ROUTE_MISS)
        params = dict(request.url.params)
        if path == "/v1/provenance":
            return self._provenance(params)
        listing = _LIST.match(path)
        if listing:
            return self._list(listing.group(1), params)
        detail = _DETAIL.match(path)
        assert detail is not None
        kind, ref = _DETAIL_KIND[detail.group(1)], detail.group(2)
        if kind == "dataset":
            return self._dataset(ref)
        found = (self.checkpoint_details if kind == "checkpoint" else self.source_details).get(ref)
        if found is None:
            return self._miss(f"{kind} not found")
        return httpx.Response(200, json=found)

    def _miss(self, detail: str) -> httpx.Response:
        return httpx.Response(404, json=_ROUTE_MISS if self.bare_404 else {"detail": detail})

    def _list(self, listing: str, params: dict[str, str]) -> httpx.Response:
        items = list(self.catalog_items[listing])
        q = params.get("q")
        if q:
            items = [
                i
                for i in items
                if any(q in str(i.get(k) or "") for k in ("name", "canonical_key", "uri", "title"))
            ]
        registered = params.get("registered")
        if registered in ("yes", "no"):
            items = [i for i in items if bool(i.get("registered")) is (registered == "yes")]
        for name in ("provider", "kind", "stored"):
            if params.get(name):
                items = [i for i in items if i.get(name) == params[name]]
        if params.get("best") == "true":
            items = [i for i in items if i.get("best")]
        # A real keyset, `(created_at, id)` newest first, in a format of the
        # fake's own: a deleted row moves no other row's position.
        items.sort(key=_key, reverse=True)
        if params.get("cursor"):
            after = tuple(params["cursor"].removeprefix("k:").split("|", 1))
            items = [i for i in items if _key(i) < after]
        limit = int(params.get("limit", 50))
        page = items[:limit]
        more = len(items) > limit
        body: dict[str, Any] = {
            "items": page,
            "next_cursor": "k:" + "|".join(_key(page[-1])) if more else None,
        }
        if listing == "checkpoints" and self.checkpoint_totals is not None:
            body["totals"] = self.checkpoint_totals
        return httpx.Response(200, json=body)

    def _dataset(self, ref: str) -> httpx.Response:
        # The server's parse (app/catalog/dataset_refs.py): parts stripped,
        # `latest` in any case, an id compared as a uuid.
        body = ref.strip().removeprefix("dataset:")
        key, _, selector = body.partition("@")
        key, selector = key.strip(), selector.strip()
        selector = "" if selector.lower() == "latest" else selector
        entry = self.dataset_details.get(key) or next(
            (d for d in self.dataset_details.values() if d["id"] == key.lower()), None
        )
        if entry is None:
            return self._miss("dataset not found")
        every = entry.get("_all_versions") or entry["versions"]
        match = _SELECTOR.fullmatch(selector) if selector else None
        chosen = every[0] if every else None
        if match is not None:
            n = int(match.group(1))
            chosen = next((v for v in every if v["n"] == n), None)
            if chosen is None:
                return httpx.Response(
                    404,
                    json={
                        "detail": {
                            "message": f"dataset {key} has no version {n}",
                            "state": "no_match",
                            "versions": sorted(v["n"] for v in every),
                        }
                    },
                )
        body = {k: v for k, v in entry.items() if k != "_all_versions"}
        if self.sends_selected and chosen is not None:
            body["selected"] = chosen
        if not self.sends_selected:
            body.pop("versions_truncated", None)
        return httpx.Response(200, json=body)

    def _provenance(self, params: dict[str, str]) -> httpx.Response:
        ref = params.get("ref", "")
        table = self.steps if params.get("format") == "steps" else self.graphs
        found = table.get(ref)
        if found is None:
            return self._miss("nothing with this ref")
        if table is self.graphs:
            found = {**found, "direction": params.get("direction"), "depth": int(params["depth"])}
        return httpx.Response(200, json=found)


# -- one fully populated catalog -------------------------------------------------

RUN_ID = "55555555-5555-5555-5555-555555555555"
PROJECT_ID = "66666666-6666-6666-6666-666666666666"
RUN = {"id": RUN_ID, "ref": "run:sft-7b-12", "name": "sft-7b", "slug": "sft-7b-12", "status": "completed"}
PROJECT = {"id": PROJECT_ID, "slug": "folding", "name": "Folding"}
#: A second run, that checked what the first produced.
CHECKER_ID = "77777777-7777-7777-7777-777777777777"


def _run_node(run_id: str, ref: str, label: str) -> dict:
    """A run node as `app/catalog/provenance.py` `_describe` writes it: the id
    is TYPED (`node_id = f"{type}:{id}"`), the ref is the run's readable one."""
    return {
        "id": f"run:{run_id}",
        "type": "run",
        "ref": ref,
        "label": label,
        "kind": None,
        "status": "completed",
        "project": PROJECT,
        "locked": False,
        "deleted": False,
    }


def provenance_graph(root: str, root_type: str, root_id: str, source: dict) -> dict:
    """`GET /v1/provenance` from `root`: the source, the run that read it and
    produced the root, and a run that checked the root. Node ids typed, edges
    naming them by `from` / `to`, exactly as the server builds them."""
    root_node = f"{root_type}:{root_id}"
    source_node = f"source:{source['id']}"
    nodes = [
        {"id": source_node, "type": "source", "ref": source["ref"], "label": "C4", "kind": None,
         "project": None, "locked": False, "deleted": False},
        _run_node(RUN_ID, RUN["ref"], RUN["name"]),
        _run_node(CHECKER_ID, "run:eval-3", "eval"),
    ]
    if root_node != source_node:
        nodes.append({"id": root_node, "type": root_type, "ref": root, "label": root, "kind": None,
                      "project": PROJECT, "locked": False, "deleted": False})

    def edge(src: str, relation: str, dst: str) -> dict:
        return {"from": src, "to": dst, "relation": relation, "roles": [], "share": None,
                "provenance": "observed_call", "derived": False, "basis": None}

    edges = [edge(f"run:{RUN_ID}", "consumes", source_node)]
    if root_node != source_node:
        edges.append(edge(f"run:{RUN_ID}", "produces", root_node))
    edges.append(edge(f"run:{CHECKER_ID}", "evaluates_on", root_node))
    return {
        "root": root_node,
        "nodes": nodes,
        "edges": edges,
        "truncated": False,
        "truncated_reason": None,
        "hidden": 0,
    }


def provenance_steps(root: str, root_type: str, source: dict) -> dict:
    """`GET /v1/provenance?format=steps` from `root`, in the server's shape."""

    def step(order: int, run_id: str, ref: str, label: str, inputs: list, outputs: list) -> dict:
        return {
            "order": order,
            "run": {"ref": ref, "label": label, "project": PROJECT, "status": "completed", "id": run_id},
            "check": order == 2,
            "recorded_after": False,
            "frozen": True,
            "read_live": [],
            "inputs": inputs,
            "outputs": outputs,
            "change": None,
            "session": None,
            "locked": False,
        }

    return {
        "target": {"ref": root, "label": root, "type": root_type},
        "sources": [{"ref": source["ref"], "canonical_key": source["canonical_key"], "title": "C4"}],
        "steps": [
            step(1, RUN_ID, RUN["ref"], RUN["name"], [source["ref"]], [root]),
            step(2, CHECKER_ID, "run:eval-3", "eval", [root], []),
        ],
        "truncated": False,
        "truncated_reason": None,
    }


def dataset_version(n: int, name: str = "c4-clean", **extra: Any) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "n": n,
        "ref": f"dataset:{name}@{n}",
        "created_at": f"2026-10-0{n}T00:00:00Z",
        "content_hash": f"sha256:{n:064d}",
        "identity": "bytes",
        "size_bytes": 1000 * n,
        "rows": 10 * n,
        "uri": f"s3://bucket/{name}/v{n}",
        "origin": "pinned",
        "meta": {"local_path": "/data/c4", "host": "gpu-1"},
        "producer": {"run": RUN, "project": PROJECT},
        "change": {"note": f"dedup pass {n}", "stats": {"removed": n}},
        "step": {"config": {"lr": 3e-4}, "code_ref": "abc123", "recorded_after": False},
        "sources": [{"ref": "source:hf-c4", "title": "C4", "canonical_key": "hf:dataset/allenai/c4", "revision": "main"}],
        "users": {
            "stored": [{"run": RUN, "roles": ["train"], "project": PROJECT}],
            # The server's exact count beside its capped list.
            "stored_count": 23,
            "derived": [],
            "truncated": True,
        },
        "checks": [{"run": RUN, "change": None}],
        "checks_count": 1,
        "composition": [],
        "locked": False,
        **extra,
    }


def seed_catalog(app: McpCatalogApp) -> dict[str, str]:
    """One dataset (3 versions), one checkpoint, one source, each listed and
    readable, with a graph and a methods view behind each. Returns a ref per
    kind, for a guard that walks every (kind, view) pair."""
    entry_id = str(uuid.uuid4())
    versions = [dataset_version(n) for n in (3, 2, 1)]
    app.dataset_details["c4-clean"] = {
        "ref": "dataset:c4-clean",
        "id": entry_id,
        "name": "c4-clean",
        "registered": True,
        "description": "C4, deduplicated against the eval sets.",
        "created_at": "2026-10-01T00:00:00Z",
        "versions": versions,
        "versions_truncated": False,
    }
    checkpoint_id = str(uuid.uuid4())
    checkpoint = {
        "ref": f"checkpoint:{checkpoint_id}",
        "id": checkpoint_id,
        "name": "step-4000.pt",
        "step": 4000,
        "best": {"monitor": "val/loss", "score": 1.23},
        "rewound": None,
        "stored": "stored",
        "location": {"uri": "s3://ckpt/step-4000.pt", "local_path": None, "host": None},
        "size_bytes": 7_000_000,
        "created_at": "2026-10-05T00:00:00Z",
        "score": 1.23,
        "monitor_key": "val/loss",
        "run": RUN,
        "project": PROJECT,
        "telemetry": "live",
        "at_step": [{"key": "val/loss", "value": 1.23, "step": 4000, "previous": None, "delta": None}],
        "saves": [
            {"id": checkpoint_id, "ref": f"checkpoint:{checkpoint_id}", "step": 4000, "score": 1.23, "best": True, "rewound": False},
            {"id": str(uuid.uuid4()), "ref": "checkpoint:older", "step": 2000, "score": 1.5, "best": False, "rewound": False},
        ],
        "saves_next_cursor": None,
        "inputs_at_save": [{"ref": "dataset:c4-clean@3", "roles": ["train"], "share": None, "name": "c4-clean", "version": 3, "composition": []}],
        "inputs_source": "inputs_at_save",
        "started_from": None,
        "used_by": [],
        "locked": False,
    }
    for ref in (checkpoint["ref"], f"checkpoint:{RUN['ref']}@best"):
        app.checkpoint_details[ref] = checkpoint
    source_id = str(uuid.uuid4())
    source = {
        "id": source_id,
        "ref": f"source:{source_id}",
        "canonical_key": "hf:dataset/allenai/c4",
        "provider": "huggingface",
        "kind": "dataset",
        "revision": "main",
        "uri": "hf://datasets/allenai/c4",
        "title": "C4",
        "description": "Colossal Clean Crawled Corpus",
        "license": "odc-by",
        "homepage": None,
        "citation": None,
        "retrieved_at": None,
        "created_at": "2026-10-01T00:00:00Z",
        "updated_at": "2026-10-01T00:00:00Z",
        "counts": {"runs_using": 2, "datasets_derived": 1},
    }
    for ref in (source["ref"], "source:hf:dataset/allenai/c4@main"):
        app.source_details[ref] = source
    for root, root_type, root_id in (
        (versions[0]["ref"], "artifact_version", versions[0]["id"]),
        (checkpoint["ref"], "artifact", checkpoint_id),
        (source["ref"], "source", source_id),
    ):
        app.graphs[root] = provenance_graph(root, root_type, root_id, source)
        app.steps[root] = provenance_steps(root, root_type, source)
    app.catalog_items["datasets"] = [
        {
            "ref": "dataset:c4-clean",
            "id": entry_id,
            "name": "c4-clean",
            "registered": True,
            "description": "C4, deduplicated against the eval sets.",
            "created_at": "2026-10-01T00:00:00Z",
            "latest": {k: versions[0][k] for k in ("n", "ref", "id", "content_hash", "identity", "size_bytes", "rows", "created_at", "producer", "locked")},
            "versions": 3,
            "used_by_runs": 1,
            "sources": [{"ref": source["ref"], "title": "C4", "canonical_key": source["canonical_key"]}],
            "locked": False,
        }
    ]
    app.catalog_items["checkpoints"] = [
        {k: checkpoint[k] for k in ("ref", "id", "name", "step", "best", "rewound", "stored", "location", "size_bytes", "created_at", "run", "project", "started_from", "locked")}
        | {"experiment": None, "trained_on": [{"ref": "dataset:c4-clean@3", "roles": ["train"]}]}
    ]
    app.catalog_items["sources"] = [source]
    return {
        "dataset": "dataset:c4-clean",
        "checkpoint": checkpoint["ref"],
        "source": source["ref"],
    }
