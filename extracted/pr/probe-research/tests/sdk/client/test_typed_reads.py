"""Typed reads on every client domain (eng review O4): each resource verb answers with the route's
response model, parsed from what the flat method returns, and the flat method's dict is unchanged."""

from __future__ import annotations

import inspect
import json
import re
import warnings
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import httpx
import pydantic
import pytest

import probe.generated.models as generated
from probe.sdk.artifact.anchors import Anchor
from probe.sdk.client.client import Client
from probe.sdk.client.resource import Resource
from probe.sdk.client.resources.projects.experiments import _from_experiment_api
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.transport.transport import Page, Transport
from probe.sdk.settings.settings import Settings

OPENAPI = json.loads((Path(__file__).parents[3] / "schema" / "openapi.json").read_text())
SCHEMAS = OPENAPI["components"]["schemas"]
ID = "11111111-1111-4111-8111-111111111111"
OTHER_ID = "22222222-2222-4222-8222-222222222222"
WHEN = "2026-10-31T12:00:00Z"
NEWER_FIELD = "added_by_a_newer_server"

#: (domain.verb, flat method, "METHOD route", route's response model, shape, item model if not it)
#: shape: one | list | page (a Page) | iter (a generator over the body's points).
TABLE = [
    ("runs.get_span", "get_span", "GET /v1/spans/{}", "SpanOut", "one", None),
    ("runs.list_trials", "list_run_trials", "GET /v1/runs/{}/trials", "TrialListOut", "page", None),
    ("runs.get_trial", "get_trial", "GET /v1/trials/{}", "TrialOut", "one", None),
    ("runs.get_bundle", "run_bundle", "GET /v1/runs/{}/bundle", "RunBundle", "one", None),
    ("runs.get_reproduction", "run_reproduce", "GET /v1/runs/{}/reproduce", "RunReproduce", "one", None),
    ("runs.get_lineage", "run_lineage", "GET /v1/runs/{}/lineage", "RunLineage", "one", None),
    ("runs.list_writers", "list_writers", "GET /v1/runs/{}/writers", "WriterOut", "list", None),
    ("metrics.list", "run_metrics", "GET /v1/runs/{}/metrics", "MetricPointOut", "list", None),
    ("metrics.list_series", "run_series", "GET /v1/runs/{}/series", "MetricSeriesOut", "list", None),
    ("metrics.get_grouped", "get_metrics_grouped", "GET /v1/runs/{}/metrics/grouped",
     "GroupedSeriesResult", "one", None),
    ("metrics.get_wide", "get_metrics_wide", "GET /v1/runs/{}/metrics/wide", "WideSeriesResult", "one",
     None),
    ("metrics.export_points", "export_metric_points", "GET /v1/runs/{}/metrics/export",
     "MetricExportResult", "iter", "ExportPoint"),
    ("metrics.list_coordinates", "list_run_coordinates", "GET /v1/runs/{}/coordinates", "CoordinateOut",
     "list", None),
    ("metrics.list_views", "list_views", "GET /v1/runs/{}/views", "MetricViewOut", "list", None),
    ("metrics.get_view_data", "view_data", "GET /v1/runs/{}/views/{}/data", "MetricViewData", "one",
     None),
    ("metrics.query_series", "query_series", "POST /v1/series/query", "SeriesQueryResult", "one", None),
    ("metrics.get_latest", "latest_scalars", "POST /v1/series/latest", "LatestScalarsWithSettings", "one",
     None),
    ("projects.get_overview", "get_project_overview", "GET /v1/projects/{}/overview", "OverviewOut", "one",
     None),
    ("projects.list_sessions", "list_project_sessions", "GET /v1/projects/{}/sessions",
     "LinkedSessionsOut", "one", None),
    ("projects.get_metric", "get_project_metric", "GET /v1/projects/{}/metric", "HeadlineMetricOut", "one",
     None),
    ("projects.get_best", "get_project_best", "GET /v1/projects/{}/best", "BestPickOut", "one", None),
    ("projects.get_workspace", "get_project_workspace", "GET /v1/projects/{}/workspace",
     "ProjectWorkspaceOut", "one", None),
    ("projects.list_artifacts", "list_project_artifacts", "GET /v1/projects/{}/artifacts", "ArtifactOut",
     "list", None),
    ("experiments.get", "get_experiment", "GET /v1/projects/{}/experiments/{}",
     "ProjectExperimentDetailOut", "one", None),
    ("experiments.list", "list_experiments", "GET /v1/projects/{}/experiments", "ProjectExperimentListOut",
     "page", "ProjectExperimentOut"),
    ("experiments.get_overview", "get_experiment_overview", "GET /v1/projects/{}/experiments/{}/overview",
     "OverviewOut", "one", None),
    ("experiments.get_overview_status", "get_experiment_overview",
     "GET /v1/projects/{}/experiments/{}/overview/status", "OverviewStatusOut", "one", None),
    ("experiments.list_sessions", "list_experiment_sessions", "GET /v1/projects/{}/experiments/{}/sessions",
     "LinkedSessionsOut", "one", None),
    ("experiments.get_inherited_files", "experiment_inherited",
     "GET /v1/projects/{}/experiments/{}/inherited", "ExperimentInheritedOut", "one", None),
    ("experiments.get_inherited_runs", "experiment_inherited",
     "GET /v1/projects/{}/experiments/{}/inherited", "ExperimentInheritedOut", "one", None),
    ("experiments.list_groups", "list_groups", "GET /v1/projects/{}/experiments/{}/groups",
     "ExperimentGroupOut", "list", None),
    ("experiments.get_group", "get_group", "GET /v1/groups/{}", "RunGroupOut", "one", None),
    ("experiments.list_edges", "experiment_edges", "GET /v1/projects/{}/experiments/{}/edges",
     "LineageEdgeOut", "list", None),
    ("experiments.get_metric", "get_experiment_metric", "GET /v1/projects/{}/experiments/{}/metric",
     "HeadlineMetricOut", "one", None),
    ("experiments.get_reproduction", "experiment_reproduce", "GET /v1/projects/{}/experiments/{}/reproduce",
     "ExperimentReproduce", "one", None),
    ("experiments.list_artifacts", "list_experiment_artifacts",
     "GET /v1/projects/{}/experiments/{}/artifacts", "ArtifactOut", "list", None),
    ("papers.get", "get_paper", "GET /v1/papers/{}", "PaperOut", "one", None),
    ("papers.list", "list_papers", "GET /v1/projects/{}/papers", "PaperListOut", "page", None),
    ("papers.get_citation_graph", "citation_graph", "GET /v1/projects/{}/citation-graph",
     "CitationGraphOut", "one", None),
    ("papers.get_citations", "paper_citations", "GET /v1/papers/{}/citations", "PaperCitationsOut", "one",
     None),
    ("summaries.get", "get_summary", "GET /v1/projects/{}/summary", "SummaryOut", "one", None),
    ("summaries.list_versions", "list_summary_versions", "GET /v1/projects/{}/summary/versions",
     "SummaryVersionsOut", "one", None),
    ("summaries.get_version", "get_summary_version", "GET /v1/projects/{}/summary/versions/{}",
     "SummaryVersionOut", "one", None),
    ("summaries.get_visuals_options", "get_visuals_options", "GET /v1/projects/{}/visuals/options",
     "VisualsOptionsOut", "one", None),
    ("artifacts.get", "get_artifact", "GET /v1/artifacts/{}", "ArtifactDetailOut", "one", None),
    ("artifacts.list", "list_anchored", "GET /v1/projects/{}/artifacts", "ArtifactOut", "list", None),
    ("artifacts.get_tree", "list_run_artifact_tree", "GET /v1/runs/{}/artifacts/tree",
     "ArtifactTreeLevel", "one", None),
    ("catalog.get_source", "get_source", "GET /v1/sources/{}", "SourceOut", "one", None),
    ("catalog.list_sources", "list_sources", "GET /v1/catalog/sources", "SourceListOut", "one", None),
    ("catalog.list_artifact_versions", "list_artifact_versions", "GET /v1/artifacts/{}/versions",
     "ArtifactVersionOut", "list", None),
    ("catalog.get_pin_impact", "artifact_pin_impact", "GET /v1/artifacts/{}/pin-impact",
     "ArtifactPinImpact", "one", None),
    ("lineage.list_run_edges", "run_edges", "GET /v1/runs/{}/edges", "LineageEdgeOut", "list", None),
    ("lineage.get_run_inputs", "run_inputs", "GET /v1/runs/{}/inputs", "RunInputsOut", "one", None),
    ("lineage.get_run_outputs", "run_outputs", "GET /v1/runs/{}/outputs", "RunOutputsOut", "one", None),
    ("lineage.get_run_upstream", "run_upstream", "GET /v1/runs/{}/upstream", "RunUpstreamOut", "one",
     None),
    ("lineage.get_artifact_lineage", "artifact_lineage", "GET /v1/artifacts/{}/lineage",
     "ArtifactLineageOut", "one", None),
    ("lineage.get_project_lineage", "project_lineage", "GET /v1/projects/{}/lineage", "ProjectLineageOut",
     "one", None),
    ("lineage.get_experiment_lineage", "experiment_lineage", "GET /v1/projects/{}/experiments/{}/lineage",
     "ProjectLineageOut", "one", None),
    ("lineage.get_project_branches", "project_branches", "GET /v1/projects/{}/branches", "BranchesOut",
     "one", None),
    ("lineage.get_experiment_branch", "experiment_branch", "GET /v1/projects/{}/experiments/{}/branch",
     "BranchesOut", "one", None),
    ("lineage.get_workspace_branches", "workspace_branches", "GET /v1/workspaces/{}/branches",
     "BranchesOut", "one", None),
    ("lineage.find_artifacts_by_hash", "artifacts_by_hash", "GET /v1/artifacts/by-hash/{}",
     "HashLookupOut", "one", None),
    ("lineage.list_paper_edges", "paper_edges", "GET /v1/projects/{}/paper-edges", "LineageEdgeOut",
     "list", None),
    ("lineage.get_execution_record", "get_execution_record", "GET /v1/execution-records/{}",
     "ExecutionRecordOut", "one", None),
    ("lineage.list_experiment_versions", "list_experiment_versions",
     "GET /v1/projects/{}/experiments/{}/versions", "ExperimentManifestOut", "list", None),
    ("lineage.get_experiment_version", "get_experiment_version",
     "GET /v1/projects/{}/experiments/{}/versions/{}", "ExperimentManifestOut", "one", None),
    ("integrations.list_code_sources", "list_project_code_sources", "GET /v1/projects/{}/code-sources",
     "CodeSourceOut", "list", None),
    ("integrations.list_mirror_connections", "list_mirror_connections",
     "GET /v1/integrations/mirror/connections", "MirrorConnectionOut", "list", None),
    ("integrations.list_mirror_scope_options", "list_mirror_scope_options",
     "GET /v1/integrations/mirror/connections/{}/scope-options", "ScopeOptionOut", "list", None),
    ("integrations.list_pulls", "list_project_pulls", "GET /v1/projects/{}/pulls", "PullsPage", "one",
     None),
    ("integrations.list_releases", "list_project_releases", "GET /v1/projects/{}/releases", "ReleasesPage",
     "one", None),
    ("integrations.list_commits", "list_project_commits", "GET /v1/projects/{}/commits", "CommitsPage",
     "one", None),
    ("integrations.get_commit", "get_project_commit", "GET /v1/projects/{}/commits/{}", "CommitCard", "one",
     None),
    ("integrations.get_run_code", "get_run_code", "GET /v1/runs/{}/code", "RunCodeOut", "one", None),
    ("integrations.compare_run_code", "compare_run_code", "GET /v1/runs/{}/code/compare",
     "RunCodeCompareOut", "one", None),
    ("integrations.get_experiment_code", "get_experiment_code", "GET /v1/projects/{}/experiments/{}/code",
     "ExperimentCodeOut", "one", None),
    ("notes.list", "list_notes", "GET /v1/notes", "NoteCatalogOut", "one", None),
    ("notes.list_sub_notes", "list_sub_notes", "GET /v1/projects/{}/sub-notes", "SubNoteListOut", "one",
     None),
    ("notes.get_sub_note", "get_sub_note", "GET /v1/sub-notes/{}", "SubNoteOut", "one", None),
    ("notes.get_team_note", "get_team_note", "GET /v1/team-note", "TeamNoteOut", "one", None),
    ("notes.get_team_note_brief", "get_team_note_brief", "GET /v1/team-note/brief", "TeamNoteBriefOut",
     "one", None),
    ("notes.list_team_note_versions", "list_team_note_versions", "GET /v1/team-note/versions",
     "TeamNoteVersionsOut", "one", None),
    ("notes.get_team_note_version", "get_team_note_version", "GET /v1/team-note/versions/{}",
     "TeamNoteOut", "one", None),
    ("sessions.get_work", "session_work", "GET /v1/sessions/{}/work", "SessionWorkOut", "one", None),
    ("sessions.get_created", "session_created", "GET /v1/sessions/{}/created", "SessionCreatedOut", "one",
     None),
    ("sessions.get_transcript", "session_transcript", "GET /v1/sessions/{}/transcript",
     "SessionTranscriptOut", "one", None),
    ("sessions.get_trajectory", "session_trajectory", "GET /v1/sessions/{}/trajectory",
     "SessionTrajectoryOut", "one", None),
    ("workspaces.get", "get_workspace", "GET /v1/workspaces/{}", "WorkspaceOut", "one", None),
    ("workspaces.list", "list_workspaces", "GET /v1/workspaces", "WorkspaceOut", "list", None),
    ("workspaces.list_access_groups", "list_access_groups", "GET /v1/access-groups", "AccessGroupOut",
     "list", None),
    ("workspaces.get_writers", "get_workspace_writers", "GET /v1/workspaces/{}/writers",
     "WorkspaceWriters", "one", None),
    ("workspaces.get_best", "get_workspace_best", "GET /v1/workspaces/{}/best", "BestPickOut", "one", None),
    ("auth.list_tokens", "list_tokens", "GET /v1/tokens", "TokenOut", "list", None),
    ("auth.list_installations", "list_client_installations", "GET /v1/client-installations",
     "ClientInstallationsOut", "one", None),
    ("reads.search", "search", "POST /v1/search", "SearchResponse", "one", None),
    ("reads.search_web", "search_web", "POST /v1/web/search", "WebSearchResponse", "one", None),
    ("reads.find_papers", "find_papers", "POST /v1/web/papers", "PaperSearchResponse", "one", None),
    ("reads.read_page", "read_page", "POST /v1/web/read", "ReadPageResponse", "one", None),
    ("reads.get_tree", "browse", "GET /v1/browse", "BrowseResponse", "one", None),
    ("reads.search_docs", "docs", "GET /public/v1/docs", "DocsOut", "one", None),
]
#: Verbs that fix one of the flat method's arguments, which they drop from their own signature.
FIXED = {
    "experiments.get_overview_status": {"status_only": True},
    "experiments.get_overview": {"status_only": False},
    "experiments.get_inherited_files": {"runs": False},
    "experiments.get_inherited_runs": {"runs": True},
}
#: Flat parameters a verb leaves out because the flat method refuses every value of them.
DROPPED = {"experiments.list": {"tags", "params"}}
#: #3754's typed reads, tested in test_resources.py.
FIRST_TYPED = {"runs.get", "runs.list", "runs.list_spans", "projects.get", "projects.list"}
#: Flat reads that reshape the server's row (the typed read undoes it): row -> what the flat returns.
RESHAPED = {"experiments.get": _from_experiment_api, "experiments.list": _from_experiment_api}
ARGUMENTS = {
    "anchor": Anchor.PROJECT, "entity": "project", "version": 1, "sha": "abc123", "to": OTHER_ID,
    "content_hash": "sha256-abc", "ref": "src-1", "query": "loss curves", "mode": "search",
    "url": "https://example.com/a", "run_ids": [ID], "key": "loss",
}


def _schema(ref_or_schema: dict) -> dict:
    while "$ref" in ref_or_schema:
        ref_or_schema = SCHEMAS[ref_or_schema["$ref"].rsplit("/", 1)[-1]]
    return ref_or_schema


def _minimal(schema: dict) -> Any:
    """The smallest value the server's schema allows, with one item in every required list."""
    schema = _schema(schema)
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        return schema["enum"][0]
    for union in ("anyOf", "oneOf"):
        if union in schema:
            options = [o for o in schema[union] if o.get("type") != "null"]
            return _minimal(options[0]) if options else None
    if "allOf" in schema:
        return _minimal(schema["allOf"][0])
    kind = schema.get("type")
    if kind == "object" or "properties" in schema:
        properties = schema.get("properties", {})
        return {name: _minimal(properties[name]) for name in schema.get("required", [])}
    if kind == "array":
        if "prefixItems" in schema:  # a tuple
            return [_minimal(item) for item in schema["prefixItems"]]
        return [_minimal(schema["items"])] if schema.get("items") else []
    if kind == "string":
        return {"date-time": WHEN, "uuid": ID, "date": "2026-10-31"}.get(
            schema.get("format"), "x" * max(1, schema.get("minLength", 1))
        )
    if kind == "integer":
        return max(1, schema.get("minimum", 1))
    if kind == "number":
        return max(0.5, schema.get("minimum", 0.5))
    return False if kind == "boolean" else None


def _route_schema(route: str) -> dict:
    method, path = route.split(" ", 1)
    for template, operations in OPENAPI["paths"].items():
        if re.sub(r"\{[^}]+\}", "{}", template) == path and method.lower() in operations:
            responses = operations[method.lower()]["responses"]
            return responses["200"]["content"]["application/json"]["schema"]
    raise AssertionError(f"{route} is not in agent/schema/openapi.json")


def _served(route: str) -> Any:
    """The body the server sends on `route`: every object carries a field this SDK never heard of."""
    body = _minimal(_route_schema(route))
    for record in body if isinstance(body, list) else [body]:
        record[NEWER_FIELD] = True
    return body


BODIES = {row[2]: _served(row[2]) for row in TABLE}
ROUTES = [(row[2].split(" ")[0], re.compile(re.sub(r"\\\{\\\}", "[^/]+", re.escape(row[2].split(" ")[1])) + "$"),
           row[2]) for row in TABLE]


def _answer(request: httpx.Request) -> httpx.Response:
    for method, pattern, route in ROUTES:
        if request.method == method and pattern.match(request.url.path):
            return httpx.Response(200, json=BODIES[route], headers={"X-Next-Cursor": "c2"})
    return httpx.Response(404, json={"detail": "Not Found"})


@pytest.fixture
def client(tmp_path) -> Iterator[Client]:
    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token="ros_ing_cafef00d",
                        hmac_secret="s3cr3t", workspace="ws-mine")
    transport = Transport(settings, client=httpx.Client(base_url="http://test",
                                                        transport=httpx.MockTransport(_answer)))
    journal = Journal(str(tmp_path / "outbox"), context={"name": None, "base_url": settings.base_url})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        made = Client(settings=settings, transport=transport, journal=journal, async_writes=False,
                      auto_drain=False)
    yield made
    made.close()


def _verb(client: Client, name: str):
    domain, verb = name.split(".")
    return getattr(getattr(client, domain), verb)


def _call(function, name: str) -> tuple[list, dict]:
    """Arguments for one read: every required parameter, plus the project an experiment is filed in
    (so no `/v1/scopes` lookup runs) and the project a summary belongs to."""
    parameters = inspect.signature(function).parameters
    args, kwargs = [], {}
    for parameter in parameters.values():
        if parameter.default is not inspect.Parameter.empty or parameter.kind in (
            parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD
        ):
            continue
        value = ARGUMENTS.get(parameter.name, ID)
        if parameter.kind == parameter.KEYWORD_ONLY:
            kwargs[parameter.name] = value
        else:
            args.append(value)
    if "project_id" in parameters and ("experiment_id" in parameters or name == "experiments.list"):
        kwargs["project_id"] = ID
    if name == "artifacts.list":
        args.append(ID)
    if "project" in parameters:
        kwargs["project"] = ID
    return args, kwargs


def _flat_args(name: str, args: list, kwargs: dict) -> tuple[list, dict]:
    return args, {**kwargs, **FIXED.get(name, {})}


def _read_flat(client: Client, row: tuple, args: list, kwargs: dict) -> Any:
    """What the flat method answers to the call the verb makes."""
    flat_args, flat_kwargs = _flat_args(row[0], args, kwargs)
    return getattr(client, row[1])(*flat_args, **flat_kwargs)


def _model(row: tuple):
    return getattr(generated, row[5] or row[3])


def _expected(row: tuple) -> Any:
    name, _flat, route, _route_model, shape, _item = row
    body, model = BODIES[route], _model(row)
    if shape == "one":
        return model.model_validate(body)
    if shape == "iter":
        return [model.model_validate(point) for point in body["points"]]
    rows = body["items"] if isinstance(body, dict) else body
    return [model.model_validate(item) for item in rows]


def _typed(result: Any, shape: str) -> Any:
    if shape == "page":
        assert isinstance(result, Page)
        return result.items
    return list(result) if shape == "iter" else result


IDS = [row[0] for row in TABLE]


@pytest.mark.parametrize("row", TABLE, ids=IDS)
def test_the_flat_method_still_returns_what_the_server_sent(client, row) -> None:
    name, flat, route, _model_name, shape, _item = row
    args, kwargs = _flat_args(name, *_call(_verb(client, name), name))
    result = getattr(client, flat)(*args, **kwargs)
    body, reshape = BODIES[route], RESHAPED.get(name, lambda served: served)
    if shape == "page":
        rows = body["items"] if isinstance(body, dict) else body
        assert isinstance(result, Page) and result.items == [reshape(item) for item in rows]
    elif shape == "iter":
        assert list(result) == body["points"]
    else:
        assert result == reshape(body)  # a dict or list of dicts, the newer server's field kept


@pytest.mark.parametrize("row", TABLE, ids=IDS)
def test_the_typed_read_is_the_routes_response_model(client, row) -> None:
    name, _flat, _route, _model_name, shape, _item = row
    verb = _verb(client, name)
    args, kwargs = _call(verb, name)
    typed = _typed(verb(*args, **kwargs), shape)
    assert typed == _expected(row)
    first = typed if shape == "one" else typed[0]
    assert isinstance(first, _model(row)) and not hasattr(first, NEWER_FIELD)


@pytest.mark.parametrize("row", [r for r in TABLE if r[4] == "page"], ids=[r[0] for r in TABLE if r[4] == "page"])
def test_a_typed_page_keeps_the_flat_pages_cursor(client, row) -> None:
    name = row[0]
    args, kwargs = _call(_verb(client, name), name)
    flat = _read_flat(client, row, args, kwargs)
    assert _verb(client, name)(*args, **kwargs).next_cursor == flat.next_cursor is not None


@pytest.mark.parametrize("row", TABLE, ids=IDS)
def test_the_typed_read_goes_through_the_flat_name(client, monkeypatch, row) -> None:
    """A patch of the flat name (or an override in a subclass) is what the resource reads."""
    name, flat, _route, _model_name, shape, _item = row
    verb = _verb(client, name)
    args, kwargs = _call(verb, name)
    real = _read_flat(client, row, args, kwargs)
    real = list(real) if shape == "iter" else real
    calls: list[tuple] = []

    def patched(*called_args, **called_kwargs):
        calls.append((called_args, called_kwargs))
        return iter(real) if shape == "iter" else real

    defaults = {p.name: p.default for p in inspect.signature(getattr(Client, flat)).parameters.values()}
    monkeypatch.setattr(client, flat, patched)
    assert _typed(verb(*args, **kwargs), shape) == _expected(row)
    assert len(calls) == 1
    for fixed, value in FIXED.get(name, {}).items():  # passed, or left at the flat default
        assert calls[0][1].get(fixed, defaults[fixed]) == value


def test_a_subclass_override_is_what_the_resource_reads(tmp_path) -> None:
    class Overriding(Client):
        def get_trial(self, trial_id: str) -> dict:
            return {**BODIES["GET /v1/trials/{}"], "name": "from the subclass"}

    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", workspace="ws-mine")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        made = Overriding(settings=settings, journal=Journal(str(tmp_path / "outbox")),
                          async_writes=False, auto_drain=False)
    try:
        assert made.runs.get_trial(ID).name == "from the subclass"
    finally:
        made.close()


@pytest.mark.parametrize("row", TABLE, ids=IDS)
def test_every_argument_reaches_the_flat_method_under_its_name(client, monkeypatch, row) -> None:
    """Each parameter, given a value of its own, arrives at the flat method as that parameter."""
    name, flat, _route, _model_name, shape, _item = row
    verb = _verb(client, name)
    args, kwargs = _call(verb, name)
    real = _read_flat(client, row, args, kwargs)
    real = list(real) if shape == "iter" else real
    sent: dict[str, object] = {}
    call_args: list[object] = []
    call_kwargs: dict[str, object] = {}
    for parameter in inspect.signature(verb).parameters.values():
        value = sent.setdefault(parameter.name, object())
        if parameter.kind == parameter.VAR_KEYWORD:
            del sent[parameter.name]
            extra = "a_filter_from_a_newer_server"
            call_kwargs[extra] = sent[extra] = value
        elif parameter.kind == parameter.KEYWORD_ONLY:
            call_kwargs[parameter.name] = value
        else:
            call_args.append(value)
    flat_signature = inspect.signature(getattr(Client, flat))
    received: dict[str, object] = {}

    def patched(*called_args, **called_kwargs):
        bound = flat_signature.bind(client, *called_args, **called_kwargs)
        bound.apply_defaults()
        for parameter_name, value in bound.arguments.items():
            if flat_signature.parameters[parameter_name].kind == inspect.Parameter.VAR_KEYWORD:
                received.update(value)
            elif parameter_name != "self":
                received[parameter_name] = value
        return iter(real) if shape == "iter" else real

    monkeypatch.setattr(client, flat, patched)
    _typed(verb(*call_args, **call_kwargs), shape)
    assert sent.keys() <= received.keys()
    for key, value in received.items():
        if key in sent:
            assert value is sent[key], key
        elif key in FIXED.get(name, {}):
            assert value == FIXED[name][key], key
        else:  # a parameter the verb does not take arrives at the flat default
            assert value == flat_signature.parameters[key].default, key


def test_an_experiment_reads_back_the_summary_the_flat_read_renames(client, monkeypatch) -> None:
    """The flat row says `overview_status` (unchanged); the typed read is the server's `summary`."""
    route = "GET /v1/projects/{}/experiments/{}"
    summary = _minimal(SCHEMAS["ProjectWorkspaceSummaryOut"])
    served = {**BODIES[route], "summary": summary}
    monkeypatch.setitem(BODIES, route, served)
    flat = client.get_experiment(ID, project_id=ID)
    assert "summary" not in flat and flat["overview_status"] == summary
    typed = client.experiments.get(ID, project_id=ID)
    assert typed.summary is not None
    assert typed == generated.ProjectExperimentDetailOut.model_validate(served)


@pytest.mark.parametrize("row", TABLE, ids=IDS)
def test_the_verb_takes_exactly_the_flat_methods_parameters(client, row) -> None:
    name, flat = row[0], row[1]
    left_out = FIXED.get(name, {}).keys() | DROPPED.get(name, set())

    def shape_of(parameter: inspect.Parameter) -> tuple:
        # `builtins.list` in a class that defines `list` is the flat method's `list`
        annotation = parameter.annotation
        if isinstance(annotation, str):
            annotation = annotation.replace("builtins.", "")
        return parameter.name, parameter.kind, parameter.default, annotation

    flat_parameters = [
        shape_of(p) for p in inspect.signature(getattr(Client, flat)).parameters.values()
        if p.name != "self" and p.name not in left_out
    ]
    typed = inspect.signature(_verb(client, name)).parameters.values()
    assert [shape_of(p) for p in typed] == flat_parameters


@pytest.mark.parametrize("row", TABLE, ids=IDS)
def test_the_routes_response_model_is_the_one_the_verb_returns(client, row) -> None:
    name, _flat, route, route_model, shape, item = row
    schema = json.dumps(_route_schema(route))
    assert f'"#/components/schemas/{route_model}"' in schema
    if item:  # experiments.list's items, export's points: the wrapper's own field
        wrapper = SCHEMAS[route_model]["properties"]
        assert any(f'"#/components/schemas/{item}"' in json.dumps(field) for field in wrapper.values())
    returned = inspect.signature(_verb(client, name)).return_annotation
    if shape == "page":
        assert returned == "Page" and f"`{item or route_model}`" in _verb(client, name).__doc__
    else:
        assert re.search(rf"\b{item or route_model}\b", returned), returned


def _enum_field(row: tuple) -> str | None:
    """A required field of the route's record whose values the server's schema closes, if any."""
    route_schema = _schema(_route_schema(row[2]))
    record = _schema(route_schema["items"]) if route_schema.get("type") == "array" else route_schema
    for field in record.get("required", []):
        if "enum" in _schema(record["properties"][field]):
            return field
    return None


ENUM_ROWS = [row for row in TABLE if row[4] in ("one", "list") and _enum_field(row)]


@pytest.mark.parametrize("row", ENUM_ROWS, ids=[row[0] for row in ENUM_ROWS])
def test_a_new_enum_value_passes_the_flat_dict_and_fails_the_typed_read(client, monkeypatch, row) -> None:
    """As `client.runs.get` set it (#3754): the flat dict carries a newer server's value through,
    the typed read refuses a value outside the vocabulary it was built with."""
    name, route = row[0], row[2]
    field = _enum_field(row)
    newer = json.loads(json.dumps(BODIES[route]))
    for record in newer if isinstance(newer, list) else [newer]:
        record[field] = "a-value-from-a-newer-server"
    monkeypatch.setitem(BODIES, route, newer)
    args, kwargs = _call(_verb(client, name), name)
    flat_result = _read_flat(client, row, args, kwargs)
    records = flat_result if isinstance(flat_result, list) else [flat_result]
    assert records[0][field] == "a-value-from-a-newer-server"
    with pytest.raises(pydantic.ValidationError):
        _verb(client, name)(*args, **kwargs)


def test_the_flat_path_never_parses_into_a_model(client, monkeypatch) -> None:
    """Typed parsing runs only on the resource API: the flat reads stay as cheap as before."""
    def refuse(*_args, **_kwargs):
        raise AssertionError("a flat read parsed its answer into a model")

    for helper in ("_to_model", "_to_models", "_to_typed_page"):
        monkeypatch.setattr(Resource, helper, staticmethod(refuse))
    for model in {_model(row) for row in TABLE} | {getattr(generated, row[3]) for row in TABLE}:
        monkeypatch.setattr(model, "model_validate", classmethod(refuse))
    for row in TABLE:
        args, kwargs = _flat_args(row[0], *_call(_verb(client, row[0]), row[0]))
        result = getattr(client, row[1])(*args, **kwargs)
        list(result) if row[4] == "iter" else result


def test_every_typed_verb_is_in_the_table(client) -> None:
    domains = {name.split(".")[0] for name in IDS} | {"runs", "projects"}
    verbs = {
        f"{domain}.{verb}"
        for domain in domains
        for verb, member in vars(type(getattr(client, domain))).items()
        if not verb.startswith("_") and callable(member)
    }
    assert verbs == set(IDS) | FIRST_TYPED
    assert all(isinstance(getattr(client, domain), Resource) for domain in domains)
