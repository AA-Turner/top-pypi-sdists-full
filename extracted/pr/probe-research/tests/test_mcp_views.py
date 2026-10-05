"""research_get's `view` seam: every view means something, and says so honestly.

The bugs these guard against were all live before this suite existed:
  * `reproduce`/`handoff`/`metrics`/`artifacts` all attached the SAME run bundle —
    four advertised views, one payload;
  * `contract`/`versions`/`usage` unconditionally reported missing:["versioned_assets"]
    and had never been implemented;
  * `token_budget` and (on research_get) `cursor` were echoed back and bounded nothing;
  * spans/groups/events/execution records were reachable from the SDK and invisible here,
    so an agent could see that 500 rollouts happened and not one of what they did.
"""

from __future__ import annotations

import json
import uuid

import pytest

from probe.mcp import service as service_module
from probe.mcp.service import _VIEWS, ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors


def _service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


#: The shared artifact `_populated` seeds, referenced by NAME because that is the
#: only way an artifact ref resolves.
_SHARED_ARTIFACT = "exec-accuracy.py"

#: The captured session `_populated` seeds — work, transcript AND digest, so the
#: honest-envelope guard can demand `complete` from every session view.
_SESSION_ID = "11111111-1111-1111-1111-111111111111"

#: The trial `_populated` seeds. It IS `span-0`, the run's first rollout, because
#: a Trial is keyed by its rollout span id -- a fixture using a fresh uuid would
#: let `_view_trial_trajectory` pass while never finding its own root.
_TRIAL_ID = "span-0"

#: The sandbox-state attempt `_populated` seeds a filesystem diff for. A run's
#: `diff` view needs one named (view_options.trial), so the loops below pass it.
_DIFF_TRIAL = "astropy-12907__attempt-1"

#: The titled sub-note `_populated` seeds (on the shared artifact, whose card
#: shows only an excerpt of notes, so no other view's payload changes).
_SUB_NOTE_ID = "22222222-2222-2222-2222-222222222222"

#: Views that need an option to answer at all, and the option that answers.
_REQUIRED_OPTIONS = {("run", "diff"): {"trial": _DIFF_TRIAL}}


def _populated(client, app, *, spans: int = 3):
    """A run with EVERYTHING a view could want: spans, series, metric points,
    artifacts, an execution record, a group, an experiment version, and events.

    Fully populated on purpose: it is what lets test_no_view_reports_missing_
    unconditionally tell "genuinely absent" apart from "always claims absence".
    """
    record = client.execution_record(
        code={"git_sha": "abc123"}, deps={"torch": "2.4"}, hardware={"gpu": "H100"}
    )
    # `run()` resolves its parents now instead of get-or-creating them, so they
    # have to exist first — the same two commands a real user runs.
    project = client.create_project("folding", kind="general")
    client.create_experiment(
        "dockq-path",
        "dockq-path",
        question="relative paths fix scoring",
        project_id=project["id"],
    )
    run = client.run(project="folding", experiment="dockq-path", name="eval-1")
    rid = run.id
    experiment_id = app.runs[rid]["experiment_id"]
    app.runs[rid]["env_ref"] = record["content_hash"]

    app.spans[rid] = [
        {
            "id": f"span-{i}",
            "run_id": rid,
            "span_type": "rollout" if i % 2 == 0 else "tool_call",
            "name": f"rollout-{i}",
            "step_index": i,
            "status": "ok",
            "parent_span_id": None,
            "attributes": {"reward": i * 0.1},
            "summary": {},
            "started_at": "2026-07-16T00:00:00Z",
            "ended_at": "2026-07-16T00:00:01Z",
            "customer_id": "lab-42",
            "created_at": "2026-07-16T00:00:00Z",
        }
        for i in range(spans)
    ]
    app.series[rid] = [
        {
            "run_id": rid,
            "key": "loss",
            "kind": "scalar",
            "x_axis": "step",
            "dimensions": {},
            "point_count": 2,
            "last_value": 0.3,
            "min_value": 0.3,
            "max_value": 0.9,
            "first_step_index": 0,
            "last_step_index": 1,
        },
    ]
    app.metric_points[rid] = [
        {
            "id": 1,
            "run_id": rid,
            "key": "loss",
            "kind": "scalar",
            "value": 0.9,
            "step_index": 0,
            "dimensions": {},
            "wall_clock": "2026-07-16T00:00:00Z",
        },
        {
            "id": 2,
            "run_id": rid,
            "key": "loss",
            "kind": "scalar",
            "value": 0.3,
            "step_index": 1,
            "dimensions": {},
            "wall_clock": "2026-07-16T00:00:01Z",
        },
    ]
    artifact_id = str(uuid.uuid4())
    app.artifacts[rid] = [
        {
            "id": artifact_id,
            "run_id": rid,
            "name": "loss.png",
            "kind": "figure",
            "status": "ready",
            "is_reference": False,
            "uri": "s3://b/loss.png",
            "customer_id": "lab-42",
            "created_at": "2026-07-16T00:00:00Z",
        },
        # A code_snapshot so a fully-populated run reads REPRODUCIBLE (env_ref +
        # snapshot => completeness.missing == []). The server's _completeness keys the
        # `code_snapshot_artifact` gap on this exact kind; the meta mirrors what a real
        # snapshot writes (nothing pending, a lockfile captured).
        {
            "id": str(uuid.uuid4()),
            "run_id": rid,
            "name": ".probe/snapshot",
            "kind": "code_snapshot",
            "status": "ready",
            "is_reference": False,
            "uri": "s3://b/snap.tar",
            "meta": {"n_pending_upload": 0, "n_lockfiles": 1},
            "customer_id": "lab-42",
            "created_at": "2026-07-16T00:00:00Z",
        },
    ]
    app.run_events[rid] = [
        {
            "id": "ev-1",
            "customer_id": "lab-42",
            "event_type": "run.created",
            "subject_type": "run",
            "subject_id": rid,
            "actor": "ingest:test",
            "payload": {},
            "created_at": "2026-07-16T00:00:00Z",
        },
    ]
    group = client.create_group(experiment_id, "lr-sweep", kind="sweep", spec={"lr": [1, 2]})
    client.experiment_version(experiment_id, label="v1")
    client.add_edge(
        source_type="run",
        source_id=rid,
        relation="produces",
        target_type="artifact",
        target_id=artifact_id,
    )
    # A SHARED artifact with a version chain: the reuse check's entity, and the
    # only kind reached by name rather than by id.
    shared_id = str(uuid.uuid4())
    app.artifacts["shared:team"] = [
        {
            "id": shared_id,
            "name": _SHARED_ARTIFACT,
            "kind": "dataset",
            "status": "ready",
            "is_reference": False,
            "uri": "s3://b/scorer.py",
            "customer_id": "lab-42",
            "created_at": "2026-07-16T00:00:00Z",
        },
    ]
    client.create_artifact_version(shared_id, uri="r2://bucket/v1")
    # Who made the run and the file -- the captured sessions each `sessions`
    # view reads (the run's off its bundle, the file's off its own route).
    session_row = {
        "session_id": _SESSION_ID,
        "agent": "claude_code",
        "owner_name": "Dev",
        "name": "eval smoke",
        "first_seen_at": "2026-07-16T00:00:00Z",
        "last_seen_at": "2026-07-16T00:05:00Z",
    }
    app.run_sessions[rid] = [session_row]
    app.artifact_sessions[shared_id] = [session_row]
    # One trial's filesystem diff, so the run's `diff` view has rows to serve.
    app.sandbox_diffs[(rid, _DIFF_TRIAL)] = {
        "entries": [{"path": "src/units.py", "status": "modified", "type": "f"}],
        "counts": {
            "added": 0,
            "modified": 1,
            "deleted": 0,
            "unchanged": 40,
            "begin_files": 41,
            "end_files": 41,
        },
    }
    app.project_readmes[project["id"]] = {
        "state": "snapshot",
        "repo": "acme/folding",
        "path": "README.md",
        "commit_sha": "c" * 40,
        "markdown": "# Folding\n\nDockQ evaluation harness.\n",
    }
    app.sub_notes[_SUB_NOTE_ID] = {
        "id": _SUB_NOTE_ID,
        "parent_kind": "artifact",
        "parent_id": shared_id,
        "title": "Scorer caveat",
        "body": "Relative paths only: absolute ones score zero.",
        "notes_version": 1,
        "created_at": "2026-07-16T00:00:00Z",
        "updated_at": "2026-07-16T00:00:00Z",
    }
    # The TEAM NOTE, non-empty deliberately: an empty document would let its
    # card pass by having nothing to report.
    app.team_note = {
        "body": "## Cluster\n\nGPUs are oversubscribed on weekdays.\n",
        "version": 3,
        "updated_at": "2026-08-18T04:00:00Z",
        "updated_by": "user:11111111-1111-1111-1111-111111111111",
        "remaining_chars": 99_950,
    }
    # A captured coding-agent session with all three reads present, keyed by
    # (id, source) on the transcript because `source` is part of the document's
    # identity server-side.
    app.session_work[_SESSION_ID] = {
        "session_id": _SESSION_ID,
        "agent": "claude_code",
        "name": "eval smoke",
        "device_label": None,
        "device_hostname": "dev-box",
        "projects": [],
        "experiments": [],
        "runs": [{"id": rid, "name": "eval-1"}],
        "artifacts": [],
    }
    app.session_transcripts[(_SESSION_ID, "claude_code")] = {
        "session_id": _SESSION_ID,
        "agent": "claude_code",
        "title": "eval smoke",
        "content": "user: run the eval\nassistant: running eval-1 now\n",
        "chunk_count": 1,
        "body_size_bytes": 48,
    }
    app.session_digests[_SESSION_ID] = {
        "session_id": _SESSION_ID,
        "agent": "claude_code",
        "status": "ready",
        "digest": {"title": "eval smoke"},
        "generated_at": "2026-07-16T00:00:00Z",
        "model": "test-model",
        "project_id": None,
        "skip_reason": None,
    }
    # The AUTHORED sidecar for `span-0` (research-os 0135). No notes key: 0145
    # took the carrier back out, and a fixture carrying one would let a card
    # regain its excerpt without any test noticing.
    app.trials[_TRIAL_ID] = {
        "id": _TRIAL_ID,
        "rollout_span_id": _TRIAL_ID,
        "customer_id": "lab-42",
        "run_id": rid,
        "name": "swebench/astropy-12907",
        "name_customized": False,
        "description": "patch the unit conversion path",
        "description_customized": True,
        "status": "completed",
        "step_index": 0,
        "started_at": "2026-07-16T00:00:00Z",
        "ended_at": "2026-07-16T00:00:01Z",
        "provider": "harbor",
        "attributes": {"reward": 0.0},
        "dimensions": {},
        "summary": {"reward": 0.0},
        "metadata": {},
        "created_at": "2026-07-16T00:00:00Z",
        "updated_at": "2026-07-16T00:00:00Z",
    }
    return rid, experiment_id, group["id"], record["content_hash"]


# -- the headline gap: a trajectory is readable at all ------------------------


def test_trajectory_view_reads_the_actual_spans(client, app):
    """The gap that mattered most: the run bundle carries span_type COUNTS, so
    there was no way to read a trajectory through the MCP at all."""
    rid, _, _, _ = _populated(client, app, spans=3)
    result = _service(client).get_entity(f"run:{rid}", view="trajectory")

    spans = result["data"]["spans"]
    assert [s["name"] for s in spans] == ["rollout-0", "rollout-1", "rollout-2"]
    assert spans[0]["attributes"] == {"reward": 0.0}  # the payload, not a count
    assert "completeness" not in result


def test_trajectory_filters_push_to_the_backend(client, app):
    rid, _, _, _ = _populated(client, app, spans=6)
    result = _service(client).get_entity(
        f"run:{rid}", view="trajectory", filters={"span_type": "tool_call", "step_from": 3}
    )
    assert [s["step_index"] for s in result["data"]["spans"]] == [3, 5]
    assert any("span_type=tool_call" in str(r.url) for r in app.requests)


# -- trials: the entity, not the span (research-os 0135) ----------------------


def test_a_trial_is_readable_by_its_rollout_id(client, app):
    """The whole point of the kind. Before this, `trial:<id>` died in the ref
    parser with "unknown ref kind", so the authored title, description and note
    the dashboard had been editing since 0135 were unreadable from any agent."""
    _populated(client, app)
    result = _service(client).get_entity(f"trial:{_TRIAL_ID}")

    entity = result["data"]["entity"]
    assert entity["name"] == "swebench/astropy-12907"
    assert entity["description"] == "patch the unit conversion path"
    assert result["data"]["available_views"] == ["card", "record", "trajectory"]


def test_a_trial_card_carries_no_notes_and_a_shareable_link(client, app):
    """A trial is the ONE research entity with no notes document (0145), so its
    card carries no excerpt and `notes` is not among its views -- a rollout ran
    once and is immutable, which makes `description` the whole of its prose.
    Asserted rather than left to absence: every sibling card carries an excerpt,
    so a missing one reads as an oversight without a claim here.

    The URL is NESTED under the run, which is why `entity_url` had to learn a
    second route shape."""
    rid, *_ = _populated(client, app)
    result = _service(client).get_entity(f"trial:{_TRIAL_ID}")

    assert "notes" not in result["data"]
    assert "notes" not in result["data"]["available_views"]
    url = result["data"].get("url")
    # None when the fixture's base URL implies no dashboard origin -- but if one
    # IS built it must be the nested route, never `/trials/<id>`.
    if url:
        assert url.endswith(f"/runs/{rid}/trials/{_TRIAL_ID}")


def test_a_trial_trajectory_is_the_rollout_subtree_not_one_level(client, app):
    """`parent_span_id` on the spans route reaches ONE level, so a run-side read
    of "trial X's spans" returns X's children and stops. The tool_call under the
    turn is the row that proves this walks the whole tree."""
    rid, *_ = _populated(client, app)
    app.spans[rid].extend(
        [
            {
                "id": "turn-0",
                "run_id": rid,
                "span_type": "agent_turn",
                "name": "turn-0",
                "step_index": 0,
                "status": "ok",
                "parent_span_id": _TRIAL_ID,
                "attributes": {},
                "summary": {},
                "started_at": "2026-07-16T00:00:00Z",
                "ended_at": "2026-07-16T00:00:01Z",
                "customer_id": "lab-42",
                "created_at": "2026-07-16T00:00:00Z",
            },
            {
                "id": "call-0",
                "run_id": rid,
                "span_type": "tool_call",
                "name": "call-0",
                "step_index": 0,
                "status": "ok",
                "parent_span_id": "turn-0",
                "attributes": {},
                "summary": {},
                "started_at": "2026-07-16T00:00:00Z",
                "ended_at": "2026-07-16T00:00:01Z",
                "customer_id": "lab-42",
                "created_at": "2026-07-16T00:00:00Z",
            },
        ]
    )
    result = _service(client).get_entity(f"trial:{_TRIAL_ID}", view="trajectory")

    assert [s["id"] for s in result["data"]["spans"]] == [_TRIAL_ID, "turn-0", "call-0"]
    # And nothing belonging to a SIBLING rollout leaked in.
    assert "span-2" not in {s["id"] for s in result["data"]["spans"]}
    assert "completeness" not in result


def test_a_trial_whose_rollout_span_is_unread_says_so(client, app):
    """NOT an empty span list. 0135 lets the sidecar outlive the bounded span
    slice on purpose, so "this trial recorded nothing" and "this server could not
    reach its spans" are opposite claims -- and only the first stops an agent
    looking."""
    rid, *_ = _populated(client, app)
    app.spans[rid] = []
    result = _service(client).get_entity(f"trial:{_TRIAL_ID}", view="trajectory")

    assert result["data"]["spans"] == []
    assert result["completeness"]["missing"] == ["trial_rollout_span_unread"]


def test_a_run_lists_its_authored_trials(client, app):
    """The inventory. `trajectory` filtered to rollouts returns the producer's
    SPANS, which carry no title and no note -- so this is a different read, not a
    convenience over one."""
    rid, *_ = _populated(client, app)
    result = _service(client).get_entity(f"run:{rid}", view="trials")

    assert [t["id"] for t in result["data"]["trials"]] == [_TRIAL_ID]
    assert result["data"]["trials"][0]["name"] == "swebench/astropy-12907"
    assert "completeness" not in result


# -- the core regression: views must not collapse into one payload ------------


def test_every_run_view_returns_a_materially_different_payload(client, app):
    """`reproduce`/`handoff`/`metrics`/`artifacts` all used to attach the same
    self.source.bundle(...). Four advertised views, one identical response."""
    rid, _, _, _ = _populated(client, app)
    service = _service(client)
    views = [
        "card",
        "trajectory",
        "metrics",
        "artifacts",
        "reproduce",
        "handoff",
        "lineage",
        "events",
    ]

    payloads = {view: service.get_entity(f"run:{rid}", view=view)["data"] for view in views}
    for view, data in payloads.items():
        assert data["view"] == view

    serialized = {
        view: json.dumps(data, sort_keys=True, default=str) for view, data in payloads.items()
    }
    assert len(set(serialized.values())) == len(views), "two views returned the same payload"
    # The four that were literally identical before, spelled out.
    assert payloads["metrics"] != payloads["artifacts"]
    assert payloads["reproduce"] != payloads["handoff"]


def test_no_view_reports_missing_unconditionally(client, app):
    """THE honest-envelope guard, and the one tests/test_parity.py cannot give us:
    parity guards HTTP reachability, not whether a view is a lie.

    Against a fully-populated entity every view must be able to say `complete`. A
    view that cannot is either unimplemented (contract/versions/usage) or reporting
    absence that is not real — and `missing` stops meaning anything the moment it
    is always populated."""
    rid, experiment_id, group_id, _ = _populated(client, app)
    project_id = app.runs[rid].get("project_id") or client.list_projects().items[0]["id"]
    refs = {
        "run": f"run:{rid}",
        "experiment": f"experiment:{experiment_id}",
        "project": f"project:{project_id}",
        "group": f"group:{group_id}",
        "artifact": f"artifact:{_SHARED_ARTIFACT}",
        # The one ref with no value: one team note per tenant, named by the
        # credential. A KeyError here means a new kind was added to _VIEWS
        # without teaching this guard to reach it.
        "team-note": "team-note",
        "session": f"session:{_SESSION_ID}",
        "trial": f"trial:{_TRIAL_ID}",
        "sub_note": f"sub_note:{_SUB_NOTE_ID}",
    }
    service = _service(client)

    for kind, view in sorted(_VIEWS):
        result = service.get_entity(
            refs[kind],
            view=view,
            token_budget=100_000,
            filters=_REQUIRED_OPTIONS.get((kind, view)),
        )
        assert "completeness" not in result, (
            f"view={view!r} on a {kind} reports missing "
            f"{result['completeness']['missing']} against a fully-populated entity"
        )


def test_deleted_phantom_views_are_rejected_by_name(client, app):
    """contract/usage are gone, not degraded: AssetOut has no contract concept and
    there is no reverse-usage index anywhere in the schema, so they could never be
    implemented. A loud error naming the real views beats an envelope that says
    `missing` forever, which reads as "temporarily degraded"."""
    rid, _, _, _ = _populated(client, app)
    service = _service(client)
    for view in ("contract", "usage"):
        with pytest.raises(errors.ValidationError) as excinfo:
            service.get_entity(f"run:{rid}", view=view)
        assert "trajectory" in str(excinfo.value)  # names what a run really supports


def test_view_not_available_for_this_kind_names_the_kinds_real_views(client, app):
    _, experiment_id, _, _ = _populated(client, app)
    with pytest.raises(errors.ValidationError) as excinfo:
        _service(client).get_entity(f"experiment:{experiment_id}", view="trajectory")
    message = str(excinfo.value)
    assert "experiment supports" in message and "groups" in message


# -- reproduce: an actual reproduction ---------------------------------------


def test_reproduce_delegates_to_the_server_assembled_record(client, app):
    """This used to return a bundle and call that reproduction; then it assembled
    the manifest client-side. Now it delegates to research-os /reproduce, so the
    view is a faithful passthrough of the one place that reads every piece together."""
    rid, _, _, content_hash = _populated(client, app)
    data = _service(client).get_entity(f"run:{rid}", view="reproduce")["data"]

    assert data["question"] == "relative paths fix scoring"
    assert data["run"]["env_ref"] == content_hash  # env_ref lives on the run core now
    assert data["execution_record"]["code"] == {"git_sha": "abc123"}
    assert data["execution_record"]["hardware"] == {"gpu": "H100"}
    assert data["restore_command"].startswith("probe snapshot-restore")
    assert "completeness" in data
    assert "bundle" not in data


def test_reproduce_without_an_env_ref_reports_it_missing(client, app):
    """CONDITIONAL missing — the honest kind. This run captured no environment, so
    it genuinely cannot be reproduced from here."""
    _proj = client.create_project("folding", kind="general")
    client.create_experiment("e", "e", question="h", project_id=_proj["id"])
    run = client.run(project="folding", experiment="e", name="no-env")
    result = _service(client).get_entity(f"run:{run.id}", view="reproduce")
    # The server's completeness flags BOTH the absent execution record and the absent
    # code snapshot (mirrored from check_run) — verified against a live server.
    assert result["completeness"]["missing"] == ["execution_record", "code_snapshot_artifact"]
    assert result["completeness"]["state"] == "partial"


# -- groups reached by a parameter, never by a seventh tool -------------------


def test_groups_are_reachable_by_view_and_by_ref(client, app):
    """The thin-harness move: a sweep is an experiment-shaped noun, so it rides the
    existing `view=` / `ref=` seams instead of a research_list_groups tool."""
    _, experiment_id, group_id, _ = _populated(client, app)
    service = _service(client)

    listed = service.get_entity(f"experiment:{experiment_id}", view="groups")["data"]
    assert [g["name"] for g in listed["groups"]] == ["lr-sweep"]

    one = service.get_entity(f"group:{group_id}")["data"]
    assert one["entity_type"] == "group"
    assert one["entity"]["spec"] == {"lr": [1, 2]}


def test_versions_view_is_real_against_the_live_registry(client, app):
    """Was: unconditionally missing:["versioned_assets"], never implemented."""
    _, experiment_id, _, _ = _populated(client, app)
    result = _service(client).get_entity(f"experiment:{experiment_id}", view="versions")
    assert [v["label"] for v in result["data"]["versions"]] == ["v1"]
    assert "completeness" not in result


# -- experiment reproduce: a MAP of per-run summaries, not N assemblies -------


def test_experiment_reproduce_view_lists_run_summaries(client, app):
    """Delegates to /v1/experiments/{id}/reproduce — a map of compact summaries, each
    with a `reproduce_url` for drill-down, so it stays one cheap read at any scale."""
    rid, experiment_id, _, _ = _populated(client, app)
    data = _service(client).get_entity(f"experiment:{experiment_id}", view="reproduce")["data"]
    assert data["completeness"]["runs_total"] >= 1
    assert data["experiment"]["id"] == experiment_id  # the manifest carries the experiment
    assert any(r["reproduce_url"].endswith(f"/v1/runs/{rid}/reproduce") for r in data["runs"])


def test_experiment_reproduce_view_accepts_version_filter(client, app):
    """`filters={"version": N}` pins against a minted manifest — applied server-side."""
    _, experiment_id, _, _ = _populated(client, app)
    result = _service(client).get_entity(
        f"experiment:{experiment_id}", view="reproduce", filters={"version": 3}
    )
    assert result["data"]["resolved_version"] == 3


def test_experiment_reproduce_view_rejects_unknown_filter(client, app):
    _, experiment_id, _, _ = _populated(client, app)
    with pytest.raises(errors.ValidationError):
        _service(client).get_entity(
            f"experiment:{experiment_id}", view="reproduce", filters={"bogus": 1}
        )


# -- token_budget actually bounds ---------------------------------------------


def test_token_budget_bounds_a_large_trajectory(client, app):
    """The knob was accepted, echoed, and bounded nothing — so an agent asking for
    2000 tokens could take a 500-span trajectory to the face."""
    rid, _, _, _ = _populated(client, app, spans=500)
    service = _service(client)

    unbounded = service.get_entity(f"run:{rid}", view="trajectory", token_budget=1_000_000)
    bounded = service.get_entity(f"run:{rid}", view="trajectory", token_budget=600)

    assert 0 < len(bounded["data"]["spans"]) < len(unbounded["data"]["spans"])
    assert len(json.dumps(bounded["data"]["spans"])) // 4 <= 600
    assert bounded["completeness"]["state"] == "partial"
    assert "truncated_by_token_budget" in bounded["completeness"]["missing"]
    assert bounded["next_cursor"] is not None


def test_a_bounded_fetch_window_never_passes_itself_off_as_the_whole_trajectory(client, app):
    """Even with an effectively infinite budget, one call reads a WINDOW of a
    500-span run, not the run. Emitting those 200 rows with next_cursor=None would
    tell the agent it had read the entire trajectory — the exact confident-wrong
    answer this whole change is about."""
    rid, _, _, _ = _populated(client, app, spans=500)
    result = _service(client).get_entity(f"run:{rid}", view="trajectory", token_budget=1_000_000)
    assert len(result["data"]["spans"]) == 200  # _PAGE_FETCH, not 500
    assert result["next_cursor"] is not None  # ... and it SAYS so
    # Not a budget truncation, so this is ordinary pagination, as in research_search.
    assert "completeness" not in result


def test_a_budget_too_small_for_one_row_still_makes_progress(client, app):
    """Never return zero rows with a cursor: a walk would spin forever. Emit one
    and report the overflow instead."""
    rid, _, _, _ = _populated(client, app, spans=5)
    result = _service(client).get_entity(f"run:{rid}", view="trajectory", token_budget=1)
    assert len(result["data"]["spans"]) == 1
    assert result["completeness"]["state"] == "partial"


def test_reproduce_is_atomic_and_reports_overflow_instead_of_truncating(client, app):
    """A reproduction manifest with fields dropped to fit reproduces nothing, so
    overflow is REPORTED rather than silently corrupting the answer."""
    rid, _, _, _ = _populated(client, app)
    app.runs[rid]["config"] = {f"hyperparam_{i}": "x" * 100 for i in range(50)}

    result = _service(client).get_entity(f"run:{rid}", view="reproduce", token_budget=50)
    assert result["completeness"]["missing"] == ["token_budget_exceeded"]
    assert result["completeness"]["state"] == "partial"
    assert "next_cursor" not in result  # nothing to paginate
    assert len(result["data"]["run"]["config"]) == 50  # intact, not quietly trimmed


# -- cursor: real, and un-rebasable -------------------------------------------


def test_cursor_walks_a_trajectory_without_skipping_or_duplicating(client, app):
    rid, _, _, _ = _populated(client, app, spans=40)
    service = _service(client)

    seen: list[str] = []
    cursor, pages = None, 0
    while True:
        result = service.get_entity(
            f"run:{rid}", view="trajectory", token_budget=400, cursor=cursor
        )
        seen.extend(s["id"] for s in result["data"]["spans"])
        cursor = result.get("next_cursor")
        pages += 1
        if cursor is None or pages > 50:
            break

    assert pages > 1, "budget did not force pagination; the walk proves nothing"
    assert seen == [f"span-{i}" for i in range(40)]
    assert len(seen) == len(set(seen))


def test_backend_ceiling_marker_reflects_the_backend_not_the_offset(client, app):
    """`spans_beyond_backend_limit` must mean the BACKEND refused to go further.

    Deriving it as `offset + len(rows) >= 10000` fired on a short run read at a high
    offset — a false `missing` marker on a trajectory the agent had seen in full.
    A wrong entry in `missing` corrupts the one signal the envelope exists to
    carry, so it is worse than no marker at all."""
    rid, _, _, _ = _populated(client, app, spans=3)
    cursor = json.dumps({"offset": 9_900, "view": "trajectory"}, sort_keys=True)
    result = _service(client).get_entity(f"run:{rid}", view="trajectory", cursor=cursor)

    assert result["data"]["spans"] == []  # read past the end
    assert "completeness" not in result  # ... and says nothing is hidden


@pytest.mark.parametrize(
    "view, filters, rows_key, ceiling_const, marker",
    [
        ("trajectory", None, "spans", "_SPAN_BACKEND_MAX", "spans_beyond_backend_limit"),
        (
            "metrics",
            {"key": "loss"},
            "points",
            "_METRIC_BACKEND_MAX",
            "metric_points_beyond_backend_limit",
        ),
    ],
)
def test_at_the_backend_ceiling_a_view_never_claims_complete(
    client, app, monkeypatch, view, filters, rows_key, ceiling_const, marker
):
    """AT the ceiling, `want == backend_max`, so the lookahead row cannot be fetched
    and `more_beyond` is False BY CONSTRUCTION — `capped` is the only signal left
    that rows sit unread. A view that ignores it emits state="complete" with no
    cursor over data it never fetched, which is the precise invariant this whole
    change exists to protect. _view_metrics did exactly that.

    Both _bounded consumers are parametrized here so a third one cannot be added
    without this test demanding its marker."""
    monkeypatch.setattr(service_module, ceiling_const, 10)
    monkeypatch.setattr(service_module, "_PAGE_FETCH", 10)
    rid, _, _, _ = _populated(client, app, spans=12)
    app.metric_points[rid] = [
        {
            "id": i,
            "run_id": rid,
            "key": "loss",
            "kind": "scalar",
            "value": i / 10,
            "step_index": i,
            "dimensions": {},
            "wall_clock": "2026-07-16T00:00:00Z",
        }
        for i in range(12)
    ]

    result = _service(client).get_entity(
        f"run:{rid}", view=view, filters=filters, token_budget=1_000_000
    )
    assert len(result["data"][rows_key]) == 10  # the backend's ceiling, not the 12 that exist
    assert marker in result["completeness"]["missing"]
    assert result["completeness"]["state"] == "partial"


def test_a_run_whose_experiment_cannot_be_read_says_so(client, app, monkeypatch):
    """The fake answers 200 for ANY experiment id, so this branch was unreachable in
    tests. Absent `env_ref` was marked while an unreadable experiment was not: the
    view returned question=None under state="complete"."""
    rid, _, _, _ = _populated(client, app)

    def _gone(_experiment_id, **_kw):
        raise errors.NotFoundError("experiment not found")

    monkeypatch.setattr(service_module.ResearchOSSource, "experiment", staticmethod(_gone))
    result = _service(client).get_entity(f"run:{rid}", view="handoff", token_budget=100_000)

    assert result["data"]["question"] is None
    assert "experiment" in result["completeness"]["missing"]
    assert result["completeness"]["state"] == "partial"


def test_a_project_direct_run_reports_no_question_without_a_missing_marker(client, app):
    """experiment_id null WITH a project_id is the W&B shape (research-os 0054):
    a legitimately experiment-less run, not a run whose experiment vanished."""
    rid, _, _, _ = _populated(client, app)
    app.runs[rid]["experiment_id"] = None
    result = _service(client).get_entity(f"run:{rid}", view="reproduce")
    assert result["data"]["question"] is None
    assert "experiment" not in result.get("completeness", {}).get("missing", [])


def test_an_orphan_run_still_reproduces_with_its_lineage_gap_in_the_run_core(client, app):
    """A run carrying neither id has no question, but it still reproduces: since the
    view delegates to /reproduce, reproduction `missing` is about the ENVIRONMENT
    (env_ref, code), not lineage bookkeeping. The orphan state is not hidden — it is
    visible in the run core (both ids null) — it just does not masquerade as a
    reproducibility gap. The 'experiment' marker was client-side question logic the
    server now owns; handoff still surfaces it (see the handoff test above)."""
    rid, _, _, _ = _populated(client, app)
    app.runs[rid]["experiment_id"] = None
    app.runs[rid]["project_id"] = None
    result = _service(client).get_entity(f"run:{rid}", view="reproduce")
    assert result["data"]["question"] is None
    assert result["data"]["run"]["experiment_id"] is None
    assert result["data"]["run"]["project_id"] is None
    assert "experiment" not in result.get("completeness", {}).get("missing", [])


def test_an_empty_filter_value_is_dropped_not_echoed_as_applied(client, app):
    """`{"key": ""}` is falsy, so it fell through to the series path while echoing
    filters={"key": ""} back — a filter reported as applied that nothing honored."""
    rid, _, _, _ = _populated(client, app)
    result = _service(client).get_entity(f"run:{rid}", view="metrics", filters={"key": ""})
    assert result["data"]["granularity"] == "series_summary"
    assert result["data"]["filters"] is None


def test_cursor_from_another_view_is_rejected_not_rebased(client, app):
    """Offset 40 of a trajectory means nothing in an events list; silently
    reinterpreting it would skip 40 events with no signal."""
    rid, _, _, _ = _populated(client, app, spans=40)
    service = _service(client)
    cursor = service.get_entity(f"run:{rid}", view="trajectory", token_budget=400)["next_cursor"]

    with pytest.raises(errors.ValidationError) as excinfo:
        service.get_entity(f"run:{rid}", view="events", cursor=cursor)
    assert "issued for view='trajectory'" in str(excinfo.value)


def test_malformed_cursor_raises_validation_error(client, app):
    rid, _, _, _ = _populated(client, app)
    with pytest.raises(errors.ValidationError):
        _service(client).get_entity(f"run:{rid}", view="trajectory", cursor="not-json")


def test_atomic_view_cannot_be_paginated(client, app):
    rid, _, _, _ = _populated(client, app)
    cursor = json.dumps({"offset": 5, "view": "reproduce"}, sort_keys=True)
    with pytest.raises(errors.ValidationError) as excinfo:
        _service(client).get_entity(f"run:{rid}", view="reproduce", cursor=cursor)
    assert "cannot be paginated" in str(excinfo.value)


# -- filters are honest -------------------------------------------------------


def test_unknown_filter_is_rejected_with_the_supported_set(client, app):
    """A silently-ignored filter returns a full result set the agent believes was
    narrowed."""
    rid, _, _, _ = _populated(client, app)
    with pytest.raises(errors.ValidationError) as excinfo:
        _service(client).get_entity(f"run:{rid}", view="trajectory", filters={"nope": 1})
    assert "span_type" in str(excinfo.value)


def test_filters_are_rejected_on_a_view_that_cannot_honor_them(client, app):
    """GET /v1/experiments/{id}/artifacts takes no filters, so `kind` is honest on a
    run's artifacts and a lie on an experiment's."""
    _, experiment_id, _, _ = _populated(client, app)
    with pytest.raises(errors.ValidationError) as excinfo:
        _service(client).get_entity(
            f"experiment:{experiment_id}", view="artifacts", filters={"kind": "figure"}
        )
    assert "accepts no view options" in str(excinfo.value)


def test_metrics_view_drills_from_series_summary_to_raw_points(client, app):
    """Progressive disclosure INSIDE a view: summaries by default, points on
    request — rather than dumping every metric point a run ever logged."""
    rid, _, _, _ = _populated(client, app)
    service = _service(client)

    summary = service.get_entity(f"run:{rid}", view="metrics")["data"]
    assert summary["granularity"] == "series_summary"
    assert [s["key"] for s in summary["series"]] == ["loss"]

    points = service.get_entity(f"run:{rid}", view="metrics", filters={"key": "loss"})["data"]
    assert points["granularity"] == "points"
    assert [p["value"] for p in points["points"]] == [0.9, 0.3]


# -- the capability map is not a permanent lie --------------------------------


def test_research_context_can_finally_report_complete(client, app):
    """`missing` was derived from every False capability flag, and four were
    hardcoded False — so EVERY context envelope was partial no matter what it
    returned, which trains agents to ignore the signal. `portable_snapshots` is
    still honestly False and must NOT, by itself, make the answer partial."""
    _populated(client, app)
    service = _service(client)
    result = service.research_context("dockq")

    # The compact envelope carries no capability map (it is static per
    # release); `portable_snapshots` is honestly False at the source, and it
    # must NOT by itself make the answer partial.
    assert service.source.capabilities()["managed_artifact_upload"] is True
    assert service.source.capabilities()["portable_snapshots"] is False
    assert "capabilities" not in result
    assert "promotion_manifests" not in service.source.capabilities()  # rejected, not "coming"
    assert "completeness" not in result
    assert result["data"]["warnings"] == []


def test_research_context_token_budget_bounds_its_lists(client, app):
    """The other inert knob: research_context accepted token_budget and echoed it
    straight back into the payload, bounding nothing."""
    for i in range(30):
        client.create_project(slug=f"budget-{i}", name="x" * 200, kind="general")
    service = _service(client)

    big = service.research_context("dockq", token_budget=100_000)
    small = service.research_context("dockq", token_budget=400)

    assert len(small["data"]["projects"]) < len(big["data"]["projects"])
    assert len(json.dumps(small["data"], default=str)) // 4 <= 400 * 1.5
    assert "truncated_by_token_budget" in small["completeness"]["missing"]
    assert small["completeness"]["state"] == "partial"
    assert "token_budget" not in small["data"]  # the echo is gone, not decorated


def test_card_advertises_exactly_the_views_that_kind_supports(client, app):
    """`card` is the default, so one call tells you what else you can ask for.

    Derived from `_VIEWS`, so it cannot advertise a view the very same matrix
    would reject -- and both the get_entity description and the track-work
    skill promise this, so it has to be true.
    """
    from probe.mcp.service import _supported_views

    rid, experiment_id, group_id, _ = _populated(client, app)
    service = _service(client)

    for ref, kind in ((f"run:{rid}", "run"), (f"experiment:{experiment_id}", "experiment")):
        card = service.get_entity(ref, view="card")
        advertised = card["data"]["available_views"]
        assert advertised == _supported_views(kind)
        # Everything advertised actually answers -- given the option a view
        # cannot answer without (a run's `diff` needs its trial named).
        for view in advertised:
            service.get_entity(
                ref,
                view=view,
                token_budget=100_000,
                filters=_REQUIRED_OPTIONS.get((kind, view)),
            )


def test_artifacts_view_surfaces_undelivered_async_uploads(client, app):
    """A row with status='pending' is a registered upload intent whose bytes
    have not arrived (async outbox, eng review 2026-07-29); 'failed' means the
    grace window expired. The view must make both unmissable -- an agent that
    sees a metadata row and assumes the blob exists is the exact failure the
    metadata-match-is-not-the-blob rule exists to stop."""
    rid, _, _, _ = _populated(client, app)
    app.artifacts[rid].extend(
        [
            {
                "id": str(uuid.uuid4()),
                "run_id": rid,
                "name": "ckpt.bin",
                "kind": "file",
                "status": "pending",
                "is_reference": False,
                "uri": None,
                "customer_id": "lab-42",
                "created_at": "2026-07-16T00:01:00Z",
            },
            {
                "id": str(uuid.uuid4()),
                "run_id": rid,
                "name": "old.bin",
                "kind": "file",
                "status": "failed",
                "is_reference": False,
                "uri": None,
                "customer_id": "lab-42",
                "created_at": "2026-07-10T00:00:00Z",
            },
        ]
    )
    service = _service(client)
    data = service.get_entity(f"run:{rid}", view="artifacts")["data"]
    assert data["undelivered"]["pending"] == 1
    assert data["undelivered"]["failed"] == 1
    assert "bytes not yet arrived" in data["undelivered"]["note"]

    # A fully-delivered listing carries no undelivered key at all.
    app.artifacts[rid] = [r for r in app.artifacts[rid] if r["status"] not in ("pending", "failed")]
    clean = service.get_entity(f"run:{rid}", view="artifacts")["data"]
    assert "undelivered" not in clean


# -- lineage: two relations, both surfaced ------------------------------------


def test_run_lineage_view_carries_edges_not_just_run_parentage(client, app):
    """The reported defect: `lineage` on a run that consumed a dataset version
    and produced three artifacts answered `ancestors: [] / descendants: []`.

    It walked `parent_run_id` — fork/retry parentage — and never read the edge
    table at all, so artifact provenance had no field it could arrive in. An
    agent reads an empty lineage as "this run has no lineage", which is a
    confident wrong answer rather than a missing one."""
    rid, _, _, _ = _populated(client, app)  # seeds one run -> artifact `produces`

    data = _service(client).get_entity(f"run:{rid}", view="lineage")["data"]
    produced = [e for e in data["edges"] if e["relation"] == "produces"]
    assert produced, "the run's artifact provenance must reach the lineage view"
    assert all(e["source_id"] == rid for e in produced)
    # The parent-chain walk is still here, under its own key — it answers a
    # different question and merging the two would recreate the ambiguity.
    assert "run_ancestry" in data
    assert set(data["run_ancestry"]) >= {"ancestors", "descendants"}


def test_run_lineage_keeps_the_two_relations_separate(client, app):
    """Artifact edges must not be reported as run parentage, or vice versa.

    Different relations over different endpoint kinds: this run has an artifact
    edge and no parent run, and the two keys have to say so independently."""
    rid, _, _, _ = _populated(client, app)
    data = _service(client).get_entity(f"run:{rid}", view="lineage")["data"]
    assert data["edges"], "edges are present"
    assert data["run_ancestry"]["ancestors"] == []
    assert data["run_ancestry"]["descendants"] == []


# -- a finished walk is complete, even when it overspent ----------------------
#
# The report that prompted this: a low-budget metrics walk paginated through
# every series and its LAST page still said partial, with no next_cursor. A
# caller following the documented contract ("a partial response has more --
# pass next_cursor back") is handed a dead end on the one page that is actually
# the whole answer.


def _metrics_walk(service, rid, *, token_budget):
    """Every page of a metrics walk, in order."""
    pages, cursor = [], None
    while True:
        page = service.get_entity(
            f"run:{rid}", view="metrics", token_budget=token_budget, cursor=cursor
        )
        pages.append(page)
        cursor = page.get("next_cursor")
        if cursor is None or len(pages) > 50:
            return pages


def test_the_last_page_of_a_metrics_walk_terminates_cleanly(client, app):
    rid, _, _, _ = _populated(client, app)
    app.series[rid] = [dict(app.series[rid][0], key=f"loss_{i}") for i in range(7)]

    pages = _metrics_walk(_service(client), rid, token_budget=120)

    assert len(pages) > 1, "budget too generous to exercise the walk"
    last = pages[-1]
    assert "next_cursor" not in last
    assert last["completeness"]["state"] == "complete", (
        "partial with no cursor says data is missing and gives no way to fetch it"
    )
    # Still reported: a caller sizing a context window wants to know it overspent.
    assert "token_budget_exceeded" in last["completeness"]["missing"]


def test_the_pages_before_the_last_still_report_partial(client, app):
    """The signal has to survive where it is TRUE -- rows really were withheld,
    and the cursor really does fetch them."""
    rid, _, _, _ = _populated(client, app)
    app.series[rid] = [dict(app.series[rid][0], key=f"loss_{i}") for i in range(7)]

    pages = _metrics_walk(_service(client), rid, token_budget=120)

    for page in pages[:-1]:
        assert page["next_cursor"] is not None
        assert page["completeness"]["state"] == "partial"
        assert "truncated_by_token_budget" in page["completeness"]["missing"]


def test_the_walk_returns_every_series_exactly_once(client, app):
    """The state fix must not come at the cost of the rows."""
    rid, _, _, _ = _populated(client, app)
    app.series[rid] = [dict(app.series[rid][0], key=f"loss_{i}") for i in range(7)]

    seen = [
        row["key"]
        for page in _metrics_walk(_service(client), rid, token_budget=120)
        for row in page["data"]["series"]
    ]
    assert sorted(seen) == sorted(f"loss_{i}" for i in range(7))


# --- papers (0152) -----------------------------------------------------------


def _review_project(client, app):
    """A `research` project with three papers, newest last as written."""
    project = client.create_project("attention-review", kind="research")
    client.add_paper(
        project["id"],
        title="Attention Is All You Need",
        authors="Vaswani et al.",
        source_url="https://arxiv.org/abs/1706.03762",
        repo_url="https://github.com/tensorflow/tensor2tensor",
        summary_md="Self-attention replaces recurrence.",
        discrepancies_md="Label smoothing is absent from the release.",
    )
    client.add_paper(
        project["id"],
        title="Deep Residual Learning",
        source_url="./papers/resnet.pdf",
    )
    return project


def test_project_papers_view_returns_the_recorded_literature(client, app):
    """The read that makes a lit review visible at all.

    Before papers existed the substance of a review — what it read — was
    nowhere, so an agent opening the project saw an empty page and could not
    tell a captured review from an uncaptured one.
    """
    project = _review_project(client, app)
    data = _service(client).get_entity(f"project:{project['id']}", view="papers")["data"]
    titles = [row["title"] for row in data["papers"]]
    assert "Attention Is All You Need" in titles
    assert "Deep Residual Learning" in titles
    first = next(r for r in data["papers"] if r["title"] == "Attention Is All You Need")
    # The discrepancies are the point: the delta between paper and repo is what
    # no abstract carries, so the view must not drop it.
    assert first["discrepancies_md"] == "Label smoothing is absent from the release."
    assert first["repo_url"].endswith("tensor2tensor")


def test_project_papers_view_carries_the_reader_tags(client, app):
    """0176. The view is how an agent groups a reading list without opening
    every paper, so the tags have to ride the ROWS — a `tags` field that only
    appeared on the detail read would make the concept invisible exactly where
    the grouping happens."""
    project = client.create_project("tagged-review", kind="research")
    client.add_paper(
        project["id"],
        title="Attention Is All You Need",
        source_url="https://arxiv.org/abs/1706.03762",
        tags=["Self Attention", "seq2seq"],
    )
    client.add_paper(
        project["id"], title="Untagged", source_url="./papers/u.pdf"
    )

    data = _service(client).get_entity(f"project:{project['id']}", view="papers")["data"]
    by_title = {row["title"]: row for row in data["papers"]}
    # Canonicalized by the server, exactly as a project or run tag would be.
    assert by_title["Attention Is All You Need"]["tags"] == [
        "self-attention",
        "seq2seq",
    ]
    # An untagged paper reads as an empty list, never as a missing key.
    assert by_title["Untagged"]["tags"] == []


def test_listing_papers_by_tag_narrows_to_the_concept(client, app):
    """The whole point of tagging a reading list: ask it a question. Driven
    through the real transport rather than a stubbed method, so the query
    parameter, the server-side filter and the SDK's skew guard all participate.
    """
    project = client.create_project("filterable-review", kind="research")
    client.add_paper(
        project["id"],
        title="Retrieval one",
        source_url="./a.pdf",
        tags=["retrieval", "rl"],
    )
    client.add_paper(
        project["id"], title="Retrieval two", source_url="./b.pdf", tags=["retrieval"]
    )
    client.add_paper(project["id"], title="Neither", source_url="./c.pdf")

    # Canonicalized on the way in: the caller types it how they say it.
    got = client.list_papers(project["id"], tags=["Retrieval"])
    assert {row["title"] for row in got.items} == {"Retrieval one", "Retrieval two"}

    # AND, not OR.
    both = client.list_papers(project["id"], tags=["retrieval", "rl"])
    assert [row["title"] for row in both.items] == ["Retrieval one"]

    # No filter means no filter — never "the untagged ones".
    assert len(client.list_papers(project["id"]).items) == 3


def test_project_papers_view_is_empty_not_missing_when_none_recorded(client, app):
    """EMPTY means zero rows read successfully — never "this read did not look".

    On a review-flavored project that emptiness IS the finding (a capture
    failure surfacing itself), so it must arrive as a clean empty list rather
    than as a missing marker an agent would read as "unknown".
    """
    project = client.create_project("unstarted-review", kind="research")
    envelope = _service(client).get_entity(f"project:{project['id']}", view="papers")
    assert envelope["data"]["papers"] == []
    assert not envelope.get("missing")


def test_papers_is_advertised_on_the_project_card(client, app):
    """A view an agent has to guess at is a view it does not use."""
    project = _review_project(client, app)
    card = _service(client).get_entity(f"project:{project['id']}")
    assert "papers" in card["data"]["available_views"]


def test_papers_view_is_project_only(client, app):
    """Papers are project-level inputs. An experiment-anchored read would be a
    half-built surface promising something no route serves (the chart_settings
    trap), so the pair is simply not in the matrix."""
    _, experiment_id, _, _ = _populated(client, app)
    with pytest.raises((errors.ValidationError, KeyError)):
        _service(client).get_entity(f"experiment:{experiment_id}", view="papers")


# --- project references (0153) -----------------------------------------------


def test_project_card_names_peers_in_both_directions(client, app):
    """A relation an agent has to know to ask about is one it never sees, so
    the card carries it. FLAT keys, matching what the tool description says —
    nesting them made `referenced_by` unfindable and read as "no incoming
    links", a confident wrong answer about the one relation this surfaces."""
    project = client.create_project("prosecco", kind="training")
    app.project_references[project["id"]] = [
        {
            "id": "r1",
            "direction": "outgoing",
            "project_id": "p-am",
            "project_slug": "assignment-modeling",
            "project_name": "Assignment modeling",
            "created_at": "2026-08-20T00:00:00Z",
        },
        {
            "id": "r2",
            "direction": "incoming",
            "project_id": "p-rev",
            "project_slug": "sampler-review",
            "project_name": "Sampler review",
            "created_at": "2026-08-20T00:00:00Z",
        },
    ]
    data = _service(client).get_entity(f"project:{project['id']}")["data"]
    assert data["references"]["projects"] == ["assignment-modeling"]
    assert data["referenced_by"]["projects"] == ["sampler-review"]


def test_project_card_caps_the_peer_list_and_states_the_count(client, app):
    """The card is the CHEAP glance and `token_budget` bounds rows, not
    payload — so an uncapped list here would blow the default budget on a
    heavily-referenced project. The count stays exact so the excerpt never
    reads as the whole set."""
    project = client.create_project("hub", kind="general")
    app.project_references[project["id"]] = [
        {
            "id": f"r{i}",
            "direction": "outgoing",
            "project_id": f"p{i}",
            "project_slug": f"peer-{i}",
            "project_name": f"Peer {i}",
            "created_at": "2026-08-20T00:00:00Z",
        }
        for i in range(25)
    ]
    data = _service(client).get_entity(f"project:{project['id']}")["data"]
    assert len(data["references"]["projects"]) == 10
    assert data["references"]["count"] == 25
    assert "referenced_by" not in data


def test_project_card_omits_references_when_there_are_none(client, app):
    """Absent, not an empty block: a key that is always present stops meaning
    anything, and the card is where an agent decides what to open."""
    project = client.create_project("lonely", kind="general")
    data = _service(client).get_entity(f"project:{project['id']}")["data"]
    assert "references" not in data
    assert "referenced_by" not in data


# -- lineage: what a run read, and who wrote it (0255) ---------------------------


def test_run_lineage_walks_upstream_only_when_asked(client, app):
    """`view_options.depth` adds the upstream walk (parents, runs built on, the
    writers of files read). Without it the view makes no extra call."""
    rid, _, _, _ = _populated(client, app)
    service = _service(client)
    plain = service.get_entity(f"run:{rid}", view="lineage")["data"]
    assert "upstream" not in plain
    deep = service.get_entity(
        f"run:{rid}", view="lineage", filters={"depth": 3}
    )["data"]
    assert deep["upstream"]["run_id"] == rid
    assert deep["upstream"]["depth"] == 3


def test_run_lineage_depth_is_bounded_and_checked(client, app):
    rid, _, _, _ = _populated(client, app)
    service = _service(client)
    capped = service.get_entity(f"run:{rid}", view="lineage", filters={"depth": 99})
    assert capped["data"]["upstream"]["depth"] == 5
    from probe import errors

    with pytest.raises(errors.ValidationError, match="depth"):
        service.get_entity(f"run:{rid}", view="lineage", filters={"depth": "far"})


def test_a_file_has_a_lineage_view(client, app):
    """Which run wrote the file and which runs read it -- the file-side half of
    "what produced this number"."""
    _populated(client, app)
    data = _service(client).get_entity(f"artifact:{_SHARED_ARTIFACT}", view="lineage")["data"]
    assert set(data) >= {"artifact_id", "written_by_run", "readers"}


def test_read_lineage_on_an_older_server_says_so(client, app):
    """A server without the read routes (0255) answers them 404; passed on, that
    reads as "no such file" for a file that exists."""
    rid, _, _, _ = _populated(client, app)
    app.supports_run_inputs = False
    client._server_features_cache = None
    service = _service(client)
    art = service.get_entity(f"artifact:{_SHARED_ARTIFACT}", view="lineage")["data"]
    assert "run_inputs" in art["unsupported"]
    run = service.get_entity(f"run:{rid}", view="lineage", filters={"depth": 2})["data"]
    assert "run_inputs" in run["upstream"]["unsupported"]


# -- lineage plan 2: every node has an origin; projects and experiments link --


def test_a_run_lineage_view_says_where_the_run_came_from(client, app):
    """L18: `origin` is the run's first parent, else its container -- one key,
    lifted out of the ancestry read rather than said twice."""
    rid, experiment_id, _, _ = _populated(client, app)
    service = _service(client)
    data = service.get_entity(f"run:{rid}", view="lineage")["data"]
    assert data["origin"] == {"type": "experiment", "id": experiment_id, "via": "container", "relation": None}
    assert "origin" not in data["run_ancestry"]
    retry = client.run(project="folding", experiment="dockq-path", parent_run_id=rid, parent_relation="retry")
    data = service.get_entity(f"run:{retry.id}", view="lineage")["data"]
    assert data["origin"] == {"type": "run", "id": rid, "via": "lineage", "relation": "retried_from"}


def test_a_file_lineage_view_carries_its_origin(client, app):
    """The server's `origin` (the run that wrote it) passes through."""
    rid, _, _, _ = _populated(client, app)
    loss_png = next(a["id"] for a in app.artifacts[rid] if a["name"] == "loss.png")
    data = _service(client).get_entity(f"artifact:{loss_png}", view="lineage")["data"]
    assert data["origin"] == {"type": "run", "id": rid, "via": "lineage", "relation": "produces"}


def test_a_project_and_an_experiment_show_their_own_links_and_children(client, app):
    """L12: an experiment that builds on another is linked experiment -> experiment,
    and the lineage view of either end shows the link; each child carries an
    origin, so the graph is connected up to the root project."""
    rid, first, group_id, _ = _populated(client, app)
    project_id = app.experiments[first]["project_id"]
    followup = client.create_experiment(
        "dockq-followup", question="does the fix hold on new complexes", project_id=project_id
    )["id"]
    link = client.add_edge(
        source_type="project", source_id=followup, relation="derived_from",
        target_type="project", target_id=first, reason="the follow-up question on its result",
    )
    service = _service(client)

    later = service.get_entity(f"experiment:{followup}", view="lineage")
    assert "completeness" not in later
    assert later["data"]["origin"] == {
        "type": "experiment", "id": first, "via": "lineage", "relation": "derived_from"
    }
    assert [e["id"] for e in later["data"]["edges"]] == [link["id"]]
    assert later["data"]["nodes"] == []

    earlier = service.get_entity(f"experiment:{first}", view="lineage")["data"]
    assert earlier["origin"] == {"type": "project", "id": project_id, "via": "container", "relation": None}
    assert [e["id"] for e in earlier["edges"]] == [link["id"]]  # the link IN, too
    by_id = {n["id"]: n for n in earlier["nodes"]}
    assert by_id[rid]["type"] == "run" and by_id[rid]["origin"]["via"] == "container"
    assert by_id[group_id]["origin"] == {"type": "experiment", "id": first, "via": "container", "relation": None}
    # The graph AMONG its runs and files, which this view always returned: the
    # seeded run -> loss.png `produces`, beside (never mixed into) its own links.
    assert [(e["source_id"], e["relation"]) for e in earlier["run_edges"]] == [(rid, "produces")]
    flags = {"edges_truncated", "derived_truncated", "nodes_truncated", "run_edges_truncated"}
    assert not flags & set(earlier)

    root = service.get_entity(f"project:{project_id}", view="lineage")
    assert "completeness" not in root
    assert root["data"]["origin"] is None  # a top-level project is a root
    assert "run_edges" not in root["data"]  # a container has no graph of its own runs
    assert {n["id"]: n["type"] for n in root["data"]["nodes"]} == {first: "experiment", followup: "experiment"}


def test_a_cut_lineage_window_is_partial_and_its_links_ride_the_first_page_only(client, app, monkeypatch):
    """Every window the read stopped at is flagged and the view is `partial`,
    never `complete`: children past the route's limit, links past the view's
    cap, "built on" derived over only the newest runs, links among its runs
    past their cap. The links are the fixed part, so they come once, on the
    first page; the budget pages the children, and the walk ends."""
    _, experiment_id, _, _ = _populated(client, app)

    def edge(i: int, **kw) -> dict:
        return {"id": f"edge-{i}", "source_type": "project", "source_id": experiment_id,
                "relation": "derived_from", "target_type": "project", "target_id": f"p-{i}", **kw}

    own = [edge(i) for i in range(25)] + [edge(99, id=None, derived=True, meta={"basis": "runs_read"})]
    among = [{"id": f"among-{i}", "source_type": "run", "source_id": f"run-{i}", "relation": "produces",
              "target_type": "artifact", "target_id": f"file-{i}"} for i in range(30)]
    nodes = [{"type": "run", "id": f"run-{i}", "name": f"sweep point {i}",
              "origin": {"type": "experiment", "id": experiment_id, "via": "container", "relation": None}}
             for i in range(40)]
    body = {"project_id": experiment_id, "kind": "experiment", "origin": None, "edges": own,
            "edges_truncated": False, "derived_truncated": True, "nodes": nodes, "truncated": True}
    among_calls: list[int] = []

    def experiment_edges(self, eid, limit):
        among_calls.append(limit)
        return among[:limit]

    monkeypatch.setattr(service_module.ResearchOSSource, "project_lineage", lambda self, pid: body)
    monkeypatch.setattr(service_module.ResearchOSSource, "experiment_edges", experiment_edges)
    service = _service(client)

    first = service.get_entity(f"experiment:{experiment_id}", view="lineage", token_budget=100_000)
    data = first["data"]
    assert first["completeness"]["state"] == "partial"
    assert "lineage_beyond_window" in first["completeness"]["missing"]
    assert [e["id"] for e in data["edges"]] == [f"edge-{i}" for i in range(20)]
    assert [e["id"] for e in data["run_edges"]] == [f"among-{i}" for i in range(20)]
    assert data["edges_truncated"] and data["derived_truncated"] and data["nodes_truncated"]
    assert data["run_edges_truncated"]
    assert "next_cursor" not in first  # the whole window fitted: nothing past it to page
    assert among_calls == [21]  # one past the cap, so a full window says so

    seen: list[str] = []
    cursor, pages = None, 0
    while True:
        result = service.get_entity(f"experiment:{experiment_id}", view="lineage", token_budget=512, cursor=cursor)
        data = result["data"]
        assert result["completeness"]["state"] == "partial" and data["nodes_truncated"]
        if pages == 0:
            assert len(data["edges"]) == 20 and len(data["run_edges"]) == 20
        else:
            assert "edges" not in data and "run_edges" not in data and data["links_on_first_page"]
        seen.extend(n["id"] for n in data["nodes"])
        cursor, pages = result.get("next_cursor"), pages + 1
        if cursor is None or pages > 60:
            break
    assert pages > 1, "the budget did not page the children; the walk proves nothing"
    assert cursor is None, "the walk never ended: a cursor past the route's window"
    assert seen == [f"run-{i}" for i in range(40)]
    assert among_calls == [21, 21], "later pages must not re-read the links"
