"""Complete saved Overview through SDK, shared entity reads and HTTP delivery."""

import json

import pytest

from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors
from test_mcp_delivery import _bounded, _wire


def _seed(app, client, kind, *, long=False):
    project = client.create_project("overview-parent", kind="general")
    entity = (
        project
        if kind == "project"
        else client.create_experiment(
            "overview-child", "Overview child", question="What changed?", project_id=project["id"]
        )
    )
    page = {
        "html": "<h1>Generated overview</h1><p>"
        + ("科学🧪 evidence " * (2400 if long else 500))
        + "</p><section data-probe-authored>Researcher's edits</section>",
        "series": {"manifest": [{"id": "loss"}], "data": {"loss": [{"x": 1, "y": 0.4}]}},
        "basis": {"runs": ["run-1"]},
        "saved_page_readable": True,
        "version": 7,
        "source": "lane",
        "model": "saved-model",
        "generated_at": "2026-10-05T12:00:00Z",
        "eta_seconds": 42,
    }
    app.__dict__.setdefault("overviews", {})[(kind, entity["id"])] = page
    return entity, page, ResearchReadService(ResearchOSSource(client))


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_complete_unified_saved_page_and_legacy_summary(app, client, kind):
    entity, page, service = _seed(app, client, kind)
    result = service.get_entity(f"{kind}:{entity['id']}", view="overview", token_budget=8000)
    saved = result["data"]["overview"]
    assert saved["html"] == page["html"] and len(saved["html"]) > 6000
    assert saved["series"] == page["series"] and saved["version"] == 7
    assert "eta_seconds" not in saved and "job" not in saved
    assert "overview" in service.get_entity(f"{kind}:{entity['id']}")["data"]["available_views"]
    legacy = service.get_entity(f"{kind}:{entity['id']}", view="summary")
    assert legacy["data"][f"{kind}_summary"]["document"] != page["html"]


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_absent_overview_is_an_honest_null_without_generation(app, client, kind):
    entity, _, service = _seed(app, client, kind)
    app.overviews.clear()
    result = service.get_entity(f"{kind}:{entity['id']}", view="overview")
    assert result["data"]["overview"]["html"] is None
    assert result["data"]["overview"]["version"] == 0
    assert app.overviews == {}


def test_http_continuation_reconstructs_saved_page_despite_worker_bookkeeping_changes(app, client):
    entity, page, service = _seed(app, client, "project", long=True)
    args = {"refs": [f"project:{entity['id']}"], "view": "overview", "token_budget": 512}
    fragments = []
    cursor = None
    for _ in range(100):
        result = _bounded(
            _wire(service, "entity", {**args, **({"cursor": cursor} if cursor else {})})
        )
        data = result["data"]
        assert data["format"] == "json_fragment"
        fragments.append(data["text"])
        cursor = result.get("next_cursor")
        page["eta_seconds"] -= 1
        page["basis"] = {
            "fingerprints": {"runs": str(len(fragments))},
            "low_signal_pending": {"at": str(len(fragments))},
            "gate_skipped": {"p_change": 0.01},
            "agent": {"rounds": len(fragments)},
            "panel_rebuilt": len(fragments) % 2 == 0,
        }
        if not cursor:
            break
    else:
        pytest.fail("Overview continuation did not finish")
    reconstructed = json.loads("".join(fragments))
    saved = reconstructed["data"]["overview"]
    assert saved["html"] == page["html"]
    assert saved["series"] == page["series"]
    assert "basis" not in saved
    assert saved["version"] == page["version"]
    for field in ("source", "model", "generated_at"):
        assert saved[field] == page[field]
    assert len(fragments) > 1


@pytest.mark.parametrize("mutation", ["edit", "ref", "view"])
def test_http_continuation_refuses_changed_source_or_request(app, client, mutation):
    entity, page, service = _seed(app, client, "project", long=True)
    args = {"refs": [f"project:{entity['id']}"], "view": "overview", "token_budget": 512}
    first = _bounded(_wire(service, "entity", args))
    if mutation == "edit":
        page["html"] += "new saved content"
        page["version"] += 1
    elif mutation == "ref":
        args["refs"] = ["project:unknown"]
    else:
        args["view"] = "summary"
    result = _wire(service, "entity", {**args, "cursor": first["next_cursor"]})
    assert result.get("isError") is True
    assert (
        "source_changed" in str(result) if mutation == "edit" else "cursor" in str(result).lower()
    )


@pytest.mark.parametrize("failure", [errors.AuthError, errors.NotFoundError, errors.TransportError])
def test_saved_page_errors_are_visible_tool_failures(app, client, monkeypatch, failure):
    entity, _, service = _seed(app, client, "project")
    read = client.transport.get

    def fail_overview(path, **kwargs):
        if path.endswith("/overview"):
            raise failure("Overview unavailable")
        return read(path, **kwargs)

    monkeypatch.setattr(client.transport, "get", fail_overview)
    result = _wire(service, "entity", {"refs": [f"project:{entity['id']}"], "view": "overview"})
    assert "Overview unavailable" in str(result)
    assert "missing" in str(result) or result.get("isError") is True


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_withheld_saved_page_never_reaches_the_tool(app, client, kind):
    entity, page, service = _seed(app, client, kind)
    # A rolling API upgrade may still return the old shape: content=absent
    # with saved fields populated. This is NOT permission to read those bytes.
    page["content"] = "absent"
    page.pop("saved_page_readable")
    result = service.get_entity(f"{kind}:{entity['id']}", view="overview", token_budget=8000)
    assert result["data"]["overview"]["html"] is None
    for field in ("plan", "blurb", "series", "model", "generated_at"):
        assert result["data"]["overview"][field] is None
    assert result["data"]["overview"]["version"] == 0


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_authored_only_saved_page_is_readable_before_generation(app, client, kind):
    entity, page, service = _seed(app, client, kind)
    page.update(content="absent", generated_at=None, source="human")
    saved = service.get_entity(f"{kind}:{entity['id']}", view="overview", token_budget=8000)["data"]["overview"]
    assert saved["html"] == page["html"]
    assert saved["series"] == page["series"] and saved["version"] == page["version"]
    assert saved["source"] == "human" and saved["generated_at"] is None
