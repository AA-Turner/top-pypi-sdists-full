"""The bench's side of recorder summaries (plan writer-owns-summary §8): the
fake Probe's summary and visuals routes with production's status codes, the
real CLI through them, and the scorer's S1-S4 (absolute bars, never counted in
the checks a comparison reads).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.test_companion_bench import (  # noqa: F401 -- `served` is a fixture
    CHOSEN,
    KEY,
    PCA_RUN,
    PROJECT,
    READS,
    SVM,
    T0,
    _call,
    _cli,
    _entity,
    _fake,
    _final,
    _reads,
    fp,
    score,
    served,
)

SUMMARY = (
    "Does an SVM beat logistic regression on digits?\n\n"
    "**Where it stands (Sep 23):** yes - SVM C=10 reaches 0.9889 (fortunate-quail-346) vs 0.9603.\n\n"
    "## Sep 23 · Richard\n- Swept C; C=10, gamma=0.001 wins.\n- PCA to 32 dropped: no gain.\n"
)


def test_the_fakes_summary_routes_answer_like_the_contract():
    fake = _fake(T0 + 3600)
    route = f"/v1/projects/{PROJECT}/experiments/{SVM}/summary"
    got = _call(fake, "GET", route)
    assert got.status == 200 and (got.body["markdown"], got.body["version"], got.body["mode"]) == (
        "",
        0,
        "recorder",
    )
    assert set(got.body) >= {
        "markdown",
        "version",
        "edited_at",
        "edited_by",
        "via",
        "session_title",
        "you",
        "today",
        "mode",
    }
    put = _call(
        fake,
        "PUT",
        route,
        {"markdown": SUMMARY, "expected_version": 0, "session_id": "s", "directed": False},
    )
    assert put.status == 200 and put.body == {"version": 1, "markdown": SUMMARY}
    stale = _call(fake, "PUT", route, {"markdown": "lost", "expected_version": 0})
    assert stale.status == 409 and stale.body["detail"] == {
        "code": "version_moved",
        "version": 1,
        "markdown": SUMMARY,
    }
    long = _call(fake, "PUT", route, {"markdown": "x" * 12_001, "expected_version": 1})
    assert (
        long.status == 422
        and long.body["detail"]["code"] == "too_long"
        and "12,000" in long.body["detail"]["message"]
    )
    key = "sk-proj-" + "Ab3dE5gH7jK9mN1pQ3sT5vX7zB9dF1hJ3lN5pR7tV9xZ"
    secret = _call(fake, "PUT", route, {"markdown": f"key {key}", "expected_version": 1})
    assert secret.status == 422 and secret.body["detail"]["code"] == "credential_shape"
    assert (
        _call(fake, "PUT", route, {"markdown": " ", "expected_version": 1}).body["detail"]["code"]
        == "empty"
    )
    versions = _call(fake, "GET", f"{route}/versions").body
    assert [v["version"] for v in versions["versions"]] == [1] and versions["next_before"] is None
    assert _call(fake, "GET", f"{route}/versions/1").body["markdown"] == SUMMARY
    # The project's own page is another page.
    assert _call(fake, "GET", f"/v1/projects/{PROJECT}/summary").body["version"] == 0
    lane = _fake(T0 + 3600, summaries_by="lane")
    off = _call(lane, "PUT", route, {"markdown": SUMMARY, "expected_version": 0})
    assert off.status == 503 and off.body["detail"]["code"] == "summary_writer_off"
    assert _call(lane, "GET", route).body["mode"] == "lane"


def test_the_fakes_visuals_routes_share_the_pages_version():
    fake = _fake(T0 + 3600)
    base = f"/v1/projects/{PROJECT}/experiments/{SVM}"
    options = _call(fake, "GET", f"{base}/visuals/options").body
    assert options["scope"] == "experiment" and options["eligible"] and options["version"] == 0
    assert {r["id"] for r in options["runs"]} == {CHOSEN, PCA_RUN}
    # PR V's FINAL shape (CONTRACT.md): kinds per scope, metrics as objects, caps per scope.
    assert options["kinds"] == [
        "table",
        "bar",
        "stacked_bar",
        "scatter",
        "heatmap",
        "box",
        "histogram",
        "parallel",
        "metric_grid",
    ]
    assert all(set(m) == {"key", "kind", "dimensions", "per_sample"} for m in options["metrics"])
    assert set(options) >= {
        "statuses",
        "metrics_open",
        "summary_paths",
        "config_paths",
        "paths_truncated",
        "runs_truncated",
        "current",
    }
    assert options["caps"]["max_visuals"] is None and options["caps"]["reduces"][-1] == "count"
    project_options = _call(fake, "GET", f"/v1/projects/{PROJECT}/visuals/options").body
    assert project_options["kinds"] == ["table", "metric_grid"]
    assert (project_options["caps"]["max_visuals"], project_options["caps"]["reduces"]) == (
        8,
        ["last", "min", "max"],
    )
    for bad, why in (
        ([{"id": "acc", "kind": "table", "title": "Accuracy"}], "`columns` needs at least 1"),
        ([{"id": "acc", "kind": "table", "columns": [{}]}], "`columns` needs its `source`"),
        ([{"id": "g", "kind": "metric_grid", "rows": [{"label": "a", "value": "a"}],
           "columns": [{"label": "b", "value": "b"}]}], "`key` is required"),
        ([{"id": "s", "kind": "table", "columns": [{"source": "run", "field": "name"}],
           "sort": {"measure": {}}}], "`sort.measure` needs its `source`"),
    ):
        refused = _call(fake, "PUT", f"{base}/visuals", {"visuals": bad, "expected_version": 0})
        assert refused.status == 422 and why in refused.body["detail"]["message"], (
            "a recipe production refuses earns no S3"
        )
    table = [{"id": "acc", "kind": "table", "title": "Accuracy",
              "columns": [{"source": "run", "field": "name"}]}]
    first = _call(fake, "PUT", f"{base}/visuals", {"visuals": table, "expected_version": 0})
    assert first.status == 200 and first.body == {
        "version": 1,
        "changed": True,
        "visuals": [{"id": "acc", "kind": "table"}],
    }
    same = _call(fake, "PUT", f"{base}/visuals", {"visuals": table, "expected_version": 1})
    assert same.status == 200 and same.body["changed"] is False and same.body["version"] == 1, (
        "the same list writes nothing"
    )
    stale = _call(fake, "PUT", f"{base}/summary", {"markdown": SUMMARY, "expected_version": 0})
    assert stale.status == 409, "a visuals set moved the page"
    moved = _call(fake, "PUT", f"{base}/visuals", {"visuals": [], "expected_version": 0})
    assert moved.status == 409 and moved.body["detail"]["current"] == table
    # The check comes before the version compare, as on the server.
    unchecked = _call(fake, "PUT", f"{base}/visuals", {"visuals": "nope", "expected_version": 0})
    assert unchecked.status == 422
    bad = _call(
        fake,
        "PUT",
        f"/v1/projects/{PROJECT}/visuals",
        {"visuals": [{"id": "b", "kind": "bar"}], "expected_version": 0},
    )
    assert (
        bad.status == 422
        and bad.body["detail"]["code"] == "visuals_refused"
        and "table" in bad.body["detail"]["message"]
    )
    state = fake.final_state()
    assert state["entities"][SVM]["visuals"] == table and state["visuals_sets"] == 1
    assert state["entities"][SVM]["summary"] is None, "no summary written"


@pytest.fixture
def served_markdown():
    """A fake without the full-page door: a server before ARTIFACT-PAGES P1."""
    fake = _fake(T0 + 3600, pages=False)
    server = fp.Served(fake, upstream=None, mcp=True)
    yield fake, server
    server.stop()


def test_the_real_cli_keeps_a_summary_and_sets_visuals_through_the_fake(tmp_path, served_markdown):
    """The Markdown path: a server before full pages ignores `format`, so the
    CLI drafts Markdown and pushes `markdown`, as it always did."""
    fake, server = served_markdown
    out = _cli(tmp_path, server, "summary", "checkout", "--experiment", "svm-vs-logreg")
    assert out.returncode == 0, out.stderr
    checkout = json.loads(out.stdout)
    assert checkout["version"] == 0 and checkout["mode"] == "recorder"
    assert checkout["path"].endswith(".md")
    Path(checkout["path"]).write_text(SUMMARY)
    pushed = _cli(tmp_path, server, "summary", "push", "--experiment", "svm-vs-logreg")
    assert pushed.returncode == 0, pushed.stderr
    assert json.loads(pushed.stdout)["pushed"] is True
    options = _cli(tmp_path, server, "visuals", "options", "--experiment", "svm-vs-logreg")
    assert options.returncode == 0, options.stderr
    table = [{"id": "acc", "kind": "table", "columns": [{"source": "run", "field": "name"}]}]
    Path(json.loads(options.stdout)["path"]).write_text(json.dumps(table))
    assert _cli(tmp_path, server, "visuals", "set", "--experiment", "svm-vs-logreg").returncode == 0
    state = fake.final_state()
    assert state["entities"][SVM]["summary"] == SUMMARY and state["entities"][SVM]["visuals"] == table
    assert state["summary_pushes"] == 1 and SVM in state["touched"] and fake.unmapped == []


# ---------------------------------------------------------------------------
# The full-page door (ARTIFACT-PAGES P1)
# ---------------------------------------------------------------------------

#: A run of the experiment with a logged metric, so `chartable` names one.
CHART_RUN_METRIC = "cv_accuracy"


def _paged_fake():
    reads = _reads()
    reads[f"/v1/runs/{CHOSEN}"]["summary_metrics"] = {CHART_RUN_METRIC: 0.9889}
    return fp.FakeProbe(reads, clock=fp.ManualClock(T0 + 3600), token="bench-fake-t")


def _page(series_id: str | None = None, metric: str = CHART_RUN_METRIC) -> str:
    block = ""
    chart = ""
    if series_id:
        declared = [{"id": series_id, "metric": metric, "run_ids": [CHOSEN]}]
        block = f'<script type="application/json" data-probe-series>{json.dumps(declared)}</script>\n'
        chart = (f'<div id="chart-{series_id}" class="ov-chart" style="height:280px"></div>'
                 f"<script>PROBE.lineChart('chart-{series_id}', '{series_id}', {{title: 'CV accuracy'}})</script>")
    return (block + "<p>An SVM beats logistic regression on digits: 0.9889 vs 0.9603 (fortunate-quail-346).</p>"
            '<h2>How it was run</h2><figure><svg viewBox="0 0 120 40"><rect x="4" y="4" width="50" height="30"/>'
            '<text x="10" y="24">sweep</text></svg><figcaption>The sweep.</figcaption></figure>' + chart)


def test_the_fakes_html_door_answers_like_the_contract():
    fake = _paged_fake()
    route = f"/v1/projects/{PROJECT}/experiments/{SVM}/summary"
    got = _call(fake, "GET", route, query="format=html").body
    assert (got["format"], got["markdown"], got["html"], got["series"], got["version"]) == ("html", "", "", [], 0)
    chartable = got["chartable"]
    assert chartable["columns"][:3] == ["kind", "key", "point_count"] and chartable["runs_covered"] == 1
    assert chartable["by_run"][0]["run_id"] == CHOSEN and chartable["by_run"][0]["series"][0][1:3] == [
        CHART_RUN_METRIC, 1], "a fixture's run holds one value per metric: one point"
    assert chartable["caps"]["charts_per_page"] == 6
    plain = _call(fake, "GET", route).body
    assert (plain["format"], plain["html"], plain["chartable"]) == ("markdown", None, None)

    put = _call(fake, "PUT", route, {"html": _page("acc"), "expected_version": 0, "session_id": "s"})
    assert put.status == 200, put.body
    assert (put.body["version"], put.body["changed"], put.body["markdown"]) == (1, True, "")
    assert put.body["html"].startswith('<article class="ov-page">'), "wrapped like the server wraps it"
    assert [s["id"] for s in put.body["series"]] == ["acc"] and "data-probe-series" not in put.body["html"]
    again = _call(fake, "PUT", route, {"html": _page("acc"), "expected_version": 1})
    assert (again.status, again.body["changed"], again.body["version"]) == (200, False, 1), "same page: no version"
    stale = _call(fake, "PUT", route, {"html": _page(), "expected_version": 0})
    assert stale.status == 409 and stale.body["detail"]["code"] == "version_moved"
    assert stale.body["detail"]["version"] == 1 and stale.body["detail"]["html"] == put.body["html"]
    assert [s["id"] for s in stale.body["detail"]["series"]] == ["acc"]
    both = _call(fake, "PUT", route, {"html": _page(), "markdown": "x", "expected_version": 1})
    assert both.status == 422 and both.body["detail"]["code"] == "body"
    md_series = _call(fake, "PUT", route, {"markdown": "x", "series": [], "expected_version": 1})
    assert md_series.status == 422 and md_series.body["detail"]["code"] == "body"
    # The Markdown read of an HTML page, and its history.
    assert "0.9889" in _call(fake, "GET", route).body["markdown"]
    assert "0.9889" in _call(fake, "GET", f"{route}/versions/1").body["markdown"]
    state = fake.final_state()
    page = state["entities"][SVM]
    assert page["summary_format"] == "html" and page["summary"] == put.body["html"]
    assert [s["id"] for s in page["summary_series"]] == ["acc"] and state["summary_pushes"] == 1
    assert [r["code"] for r in state["summary_refusals"]] == ["version_moved", "body", "body"]
    assert state["summary_pages"] is True and state["html_checks"] in ("server", "accept")


@pytest.mark.skipif(fp.server_pages() is None, reason="the server's page rules need asyncpg, structlog, "
                    "fastapi and orjson in this venv")
def test_an_html_push_meets_the_servers_own_refusals():
    fake = _paged_fake()
    route = f"/v1/projects/{PROJECT}/experiments/{SVM}/summary"
    assert fake.html_checks == "server"
    for html, code, words in (
        ("<p>ok</p><script>alert(1)</script>", "script_refused", "inside the <figure> it draws"),
        ("<h1>Title</h1><p>ok</p>", "page_refused", "<h1>"),
        (_page("acc", metric="val_loss"), "series_refused", "val_loss"),
        (_page().replace("<p>An SVM", '<p onclick="x()">An SVM'), "script_refused", "onclick"),
    ):
        refused = _call(fake, "PUT", route, {"html": html, "expected_version": 0})
        assert refused.status == 422 and refused.body["detail"]["code"] == code, refused.body
        assert words in refused.body["detail"]["message"]
    assert fake.final_state()["entities"][SVM]["summary"] is None, "nothing refused was written"


def test_the_real_cli_drafts_and_pushes_a_full_page_through_the_fake(tmp_path, served):  # noqa: F811
    fake, server = served
    out = _cli(tmp_path, server, "summary", "checkout", "--experiment", "svm-vs-logreg")
    assert out.returncode == 0, out.stderr
    checkout = json.loads(out.stdout)
    assert checkout["path"].endswith(".html") and Path(checkout["chartable_path"]).exists()
    draft = Path(checkout["path"])
    assert "data-probe-series" in draft.read_text(), "the declarations travel at the top of the draft"
    draft.write_text(_page())
    pushed = _cli(tmp_path, server, "summary", "push", "--experiment", "svm-vs-logreg")
    assert pushed.returncode == 0, pushed.stderr
    assert json.loads(pushed.stdout)["pushed"] is True
    state = fake.final_state()
    assert state["entities"][SVM]["summary_format"] == "html" and "<svg" in state["entities"][SVM]["summary"]
    assert fake.unmapped == []


def test_an_html_page_is_scored_on_its_visible_text_and_opens_with_prose():
    html = _page("acc")
    result = _state(html, visuals=[{"id": "acc", "kind": "table"}])
    result["final"]["entities"][SVM].update(summary_format="html", summary_series=[{"id": "acc"}])
    sm = score.score(result, KEY, READS, _evidence())["summaries"]
    assert (sm["S1"], sm["S2"], sm["S4"]) == (1.0, 1.0, 0), sm["detail"]
    assert sm["pages"]["svm-vs-logreg"] == {"format": "html", "words": 15, "svg": 1, "charts": 1, "series": 1}
    assert score.documents(result["final"])[0][1].startswith("An SVM beats"), "no markup in the text"
    assert score.html_shape("<h2>Results</h2><p>words</p>") == ["opens with <h2>, not prose"]
    assert score.html_shape('<div class="ov-chart"></div><p>words</p>') == ["opens with <chart>, not prose"]


# ---------------------------------------------------------------------------
# S1-S4
# ---------------------------------------------------------------------------


def _state(summary: str | None, *, visuals=(), touched=(SVM,), run_status="completed"):
    entities = {
        PROJECT: _entity(slug="digits"),
        SVM: _entity(
            "experiment",
            slug="svm-vs-logreg",
            summary=summary,
            summary_written=summary is not None,
            visuals=list(visuals),
            visuals_set=bool(visuals),
        ),
        CHOSEN: _entity("run", slug="fortunate-quail-346", status=run_status, parent=SVM),
    }
    result = _final(entities)
    result["final"].update(
        touched=list(touched), summary_pushes=1 if summary else 0, visuals_sets=len(visuals)
    )
    return result


def _evidence() -> "score.Evidence":
    return score.Evidence("0.9889 0.9603 0.001 10 23 32")


def test_a_top_down_summary_with_the_result_and_its_run_passes_every_bar():
    s = score.score(
        _state(SUMMARY, visuals=[{"id": "acc", "kind": "table"}]), KEY, READS, _evidence()
    )
    sm = s["summaries"]
    assert (sm["S1"], sm["S2"], sm["S3"], sm["S4"], sm["gate"]) == (1.0, 1.0, 1.0, 0, True), sm
    assert sm["pushes"] == 1 and sm["visuals_sets"] == 1
    # A summary is a document the daemon wrote: the checks read it too.
    assert score.documents(_state(SUMMARY)["final"]) == [(SVM, SUMMARY)]


def test_each_bar_fails_on_its_own_fault():
    no_run = SUMMARY.replace(" (fortunate-quail-346)", "")
    sm = score.score(_state(no_run), KEY, READS, _evidence())["summaries"]
    assert sm["S1"] == 1.0 and sm["S1_results"] is False and not sm["gate"], "a number without its run"
    unwritten = score.score(_state(None), KEY, READS, _evidence())["summaries"]
    assert unwritten["S1"] == 0.0 and not unwritten["gate"], "a touched entity with no summary"
    shapeless = "- 0.9889 on fortunate-quail-346\n"
    sm = score.score(_state(shapeless), KEY, READS, _evidence())["summaries"]
    assert (
        sm["S2"] == 0.0
        and not sm["gate"]
        and len(sm["detail"]["shape_faults"]["svm-vs-logreg"]) == 3
    )
    wordy = SUMMARY + "\n## Sep 22 · Richard\n" + "- word\n" * 500
    assert score.summary_shape(wordy)[0].endswith("words")
    no_tables = score.score(_state(SUMMARY), KEY, READS, _evidence())["summaries"]
    assert no_tables["S3"] == 0.0 and no_tables["detail"]["experiments_without_tables"] == [
        "svm-vs-logreg"
    ]
    running = score.score(_state(SUMMARY, run_status="running"), KEY, READS, _evidence())[
        "summaries"
    ]
    assert running["S3"] is None, "no finished run: no tables owed"
    made_up = SUMMARY.replace("0.9603", "0.9512")
    sm = score.score(
        _state(made_up, visuals=[{"id": "a", "kind": "table"}]), KEY, READS, _evidence()
    )["summaries"]
    assert sm["S4"] == 1 and not sm["gate"] and "0.9512" in sm["detail"]["unsupported"][0]
    nothing = score.score(_state(None), KEY, READS, _evidence())["summaries"]
    assert nothing["S1"] == 0.0 and nothing["S2"] is None and not nothing["gate"], (
        "touched, never written"
    )


def test_the_summary_bars_never_enter_the_checks_a_comparison_reads():
    s = score.score(_state(SUMMARY), KEY, READS, _evidence())
    assert s["checks"] and all(name.startswith("E") for name in s["checks"]), (
        "the key's own checks only"
    )
    assert s["applicable"] == len(s["checks"])


def test_a_result_from_a_bench_without_the_routes_reports_no_summaries():
    """No `touched` in the final state: nothing to say, never a vacuous pass."""
    old = _final({PROJECT: _entity(slug="digits"), SVM: _entity("experiment", slug="svm-vs-logreg")})
    assert score.score(old, KEY, READS, _evidence())["summaries"] is None
    row = score.summarize([score.score(old, KEY, READS, _evidence())])[("x", "fx")]
    assert row["summary_gate"] is None


def _scored(label: str, *, summary: str | None, cost: float, visuals=()) -> dict:
    result = _state(summary, visuals=visuals)
    result["label"] = label
    result["usage"] = {"cost_usd": cost}
    return score.score(result, KEY, READS, _evidence())


def test_compare_holds_the_cost_bar_and_the_summary_gate():
    """D25: NEW's $/run at most +25% of BASE's; D30: NEW's gate passes on every run."""
    table = [{"id": "acc", "kind": "table"}]
    base = [_scored("main", summary=None, cost=1.00), _scored("main", summary=None, cost=1.00)]
    good = [_scored("new", summary=SUMMARY, cost=1.20, visuals=table)] * 2
    better, lines = score.compare(score.summarize(base + good), "main", "new")
    assert better, lines
    assert any("summary gate 2/2 runs" in line and "(+20%)" in line for line in lines), lines
    dear = [_scored("new", summary=SUMMARY, cost=1.30, visuals=table)] * 2
    better, lines = score.compare(score.summarize(base + dear), "main", "new")
    assert not better and any("over the +25% bar" in line for line in lines), lines
    no_tables = [_scored("new", summary=SUMMARY, cost=1.00)] * 2
    better, lines = score.compare(score.summarize(base + no_tables), "main", "new")
    assert not better and any("summary gate 0/2 runs" in line for line in lines), lines
