"""SDK behavior against the fake v3 API."""

from __future__ import annotations

import json
import signal
import sys
import threading
import time
import warnings
from datetime import datetime, timedelta, timezone
from enum import Enum

import httpx
import pytest

from probe import errors
from probe._generated.models import ExperimentCreate, IngestRunRequest
from tests.conftest import open_run


def test_run_resolves_its_experiment_and_creates_only_the_run(client, app):
    """The central claim of explicit creation: run() writes exactly ONE thing.

    The old assertion checked that a POST /v1/experiments happened — which the
    `open_run` HELPER now issues, not run(). It would have passed even if run()
    never touched experiments at all, so it could not see the behaviour it was
    named for. Snapshot the request trail AFTER the explicit create and assert
    run() adds a run and nothing else.
    """
    project = client.create_project("dockq-project", kind="general")
    client.create_experiment("dockq-sweep", "DockQ", question="h", project_id=project["id"])
    before = len(app.requests)

    run = client.run(experiment="dockq-sweep", name="run-1")

    assert run.id in app.runs
    after = [(r.method, r.url.path) for r in app.requests[before:]]
    assert ("POST", "/v1/projects") not in after, "run() created an experiment"
    # 0231: the create moved to the project address, so the OLD spelling
    # passing this assertion would prove nothing -- keep both.
    assert ("POST", "/v1/experiments") not in after, "run() created an experiment"
    assert ("POST", "/v1/projects") not in after, "run() created a project"
    posts = [p for p in after if p[0] == "POST"]
    assert len(posts) == 1 and posts[0][1].endswith("/runs"), posts


def test_creating_a_taken_slug_raises_instead_of_returning_the_existing_one(client, app):
    """Inverted deliberately. Returning the existing row on conflict is what
    'get-or-create' MEANT, and it is the behaviour that made `probe run start`
    able to conjure a chain — so the conflict has to surface."""
    app.experiment_conflict_id = "existing-123"
    with pytest.raises(errors.ConflictError):
        client.create_experiment("dockq", "DockQ", question="h", project_id="p")


def test_log_metrics(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.42, "dockq": 0.71}, step=42)
    assert app.metrics_inserted == 2
    body = json.loads(app.requests[-1].content)
    assert body["points"][0]["step_index"] == 42


def test_log_hw_sends_real_dimensions(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log_hw({"gpu_temp": 88.0}, device=3, host="n1")
    body = json.loads(app.requests[-1].content)
    point = body["points"][0]
    assert point["key"] == "gpu_temp"  # key is clean; dims are first-class now
    assert point["kind"] == "hardware"
    assert point["dimensions"] == {"device": 3, "host": "n1"}


def test_log_dimensions_passthrough(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.1}, step=1, dimensions={"rank": 0})
    body = json.loads(app.requests[-1].content)
    assert body["points"][0]["dimensions"] == {"rank": 0}


# -- client wall clock (SDK reliability plan 1.4) ------------------------------
def _stamp(point: dict) -> datetime:
    return datetime.fromisoformat(point["wall_clock"].replace("Z", "+00:00"))


def test_a_logged_point_carries_the_time_it_was_logged(client, app):
    """The server stores COALESCE(wall_clock, now()): a point sent without one is
    dated when it ARRIVES. Every key in one call shares the one call-time stamp."""
    run = open_run(client, experiment="e", name="r")
    before = datetime.now(timezone.utc)
    run.log({"loss": 0.4, "dockq": 0.7}, step=3)
    after = datetime.now(timezone.utc)

    points = json.loads(app.requests[-1].content)["points"]
    stamps = {_stamp(p) for p in points}
    assert len(stamps) == 1, points
    (stamp,) = stamps
    assert before <= stamp <= after
    assert stamp.utcoffset() == timedelta(0)


def test_an_unstepped_point_is_stamped_too(client, app):
    """`probe log` and the importers pass step=None; their points live on the
    wall-clock axis, so the stamp matters there most."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5}, step=None)
    point = _points(app)[0]
    assert "step_index" not in point and "wall_clock" in point


def test_an_explicit_wall_clock_is_respected(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.4}, step=1, wall_clock="2026-01-02T03:04:05+00:00")
    point = json.loads(app.requests[-1].content)["points"][0]
    assert _stamp(point) == datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)


def test_a_queued_point_keeps_its_log_time_not_its_delivery_time(app, tmp_path):
    """The live bug: after a 90 s outage the journal replayed points that the
    server then dated at their ARRIVAL, up to 131 s late, so findings (which bin
    by point wall_clock) saw a gap and a burst. The stamp is taken when the loop
    logs, frozen into the journaled body, and survives the delayed drain."""
    from tests.conftest import make_client

    c = make_client(app, tmp_spool=tmp_path / "spool")
    run = open_run(c, experiment="e", name="r")
    app.fail_next_metrics = True
    before = datetime.now(timezone.utc)
    run.log({"loss": 1.0}, step=1)
    logged_by = datetime.now(timezone.utc)
    assert c.journal.pending(), "expected the failed write to be journaled"

    time.sleep(0.3)  # the outage
    drained_from = datetime.now(timezone.utc)
    assert c.flush() == 1
    delivered = app.metric_batches_posted[-1]["points"][0]

    stamp = _stamp(delivered)
    assert before <= stamp <= logged_by
    assert drained_from - stamp >= timedelta(seconds=0.3)


def test_a_frozen_clock_still_gives_distinct_unstepped_points(client, app, monkeypatch):
    """An unstepped point's server identity includes its wall_clock, and the
    server keeps the FIRST of two identical ones. A frozen clock (freezegun in
    a user's test) must not make the second log() vanish: stamps strictly
    increase within the process, by 1 us when the clock does not move."""
    import probe.sdk.run as run_module

    monkeypatch.setattr(run_module, "_now", lambda: "2026-09-27T00:00:00+00:00")
    run = open_run(client, experiment="e", name="r")
    run.log({"latency_ms": 12.0}, step=None)
    first = _stamp(_points(app)[0])
    run.log({"latency_ms": 97.0}, step=None)
    second = _stamp(_points(app)[0])
    assert second - first == timedelta(microseconds=1)


def test_a_clock_stepped_backwards_still_moves_the_stamp_forward(client, app, monkeypatch):
    import probe.sdk.run as run_module

    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, step=None)
    first = _stamp(_points(app)[0])
    monkeypatch.setattr(run_module, "_now", lambda: "2020-01-01T00:00:00+00:00")
    run.log({"loss": 2.0}, step=None)
    assert _stamp(_points(app)[0]) == first + timedelta(microseconds=1)


def _client_with_server_date(app, monkeypatch, date: str | None):
    """A client whose fake server answers with this HTTP `Date` header."""
    from probe.sdk import transport as transport_module
    from tests.conftest import make_client

    monkeypatch.setattr(transport_module, "_clock_checked", False)
    handler = app.handler

    def dated(request):
        response = handler(request)
        if date is not None:
            response.headers["Date"] = date
        return response

    app.handler = dated
    return make_client(app)


def test_a_client_clock_minutes_off_the_server_warns_once(app, monkeypatch):
    from email.utils import format_datetime

    skewed = format_datetime(datetime.now(timezone.utc) - timedelta(minutes=5), usegmt=True)
    client = _client_with_server_date(app, monkeypatch, skewed)
    with pytest.warns(UserWarning, match=r"clock is 30\d s ahead of the server"):
        run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as again:
        warnings.simplefilter("always")
        run.log({"loss": 1.0}, step=1)
    assert not [w for w in again if "clock is" in str(w.message)], "once per process"


def test_a_client_clock_within_a_minute_is_quiet(app, monkeypatch):
    from email.utils import format_datetime

    close = format_datetime(datetime.now(timezone.utc) - timedelta(seconds=20), usegmt=True)
    client = _client_with_server_date(app, monkeypatch, close)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        open_run(client, experiment="e", name="r").log({"loss": 1.0}, step=1)
    assert not [w for w in caught if "clock is" in str(w.message)]


def test_a_response_without_a_date_header_does_not_use_up_the_check(app, monkeypatch):
    from probe.sdk import transport as transport_module

    client = _client_with_server_date(app, monkeypatch, None)
    open_run(client, experiment="e", name="r")
    assert transport_module._clock_checked is False


def test_log_derived_is_not_stamped(client, app):
    """A derived write is computed after the fact; call time is not when the
    value was measured, so it keeps leaving wall_clock to the caller."""
    run = open_run(client, experiment="e", name="r")
    run.log_derived({"auroc": 0.9}, step=3, producer="rescore")
    assert "wall_clock" not in _points(app)[0]
    run.log_derived_series("auroc", {1: 0.8, 2: 0.85}, producer="rescore")
    assert all("wall_clock" not in p for p in _points(app))


# -- nested dicts flatten to "/" keys (SDK reliability plan (d)) ----------------
def _posts_since(app, mark):
    return [r.url.path for r in app.requests[mark:] if r.method == "POST"]


def _metric_values(app, run):
    body = next(
        json.loads(r.content)
        for r in reversed(app.requests)
        if r.method == "POST" and r.url.path == f"/v1/runs/{run.id}/metrics"
    )
    return {p["key"]: p["value"] for p in body["points"]}


def test_a_nested_dict_is_charted_under_slash_keys_at_one_step(client, app):
    """Before (d) `float(dict)` failed, so the whole dict went to the step record
    as ONE attribute and nothing was charted."""
    run = open_run(client, experiment="e", name="r")
    mark = len(app.requests)
    run.log({"nested": {"a": 1.0, "b": {"c": -1.0}}})

    assert _posts_since(app, mark) == [f"/v1/runs/{run.id}/metrics"], "no step-record POST"
    points = _points(app)
    assert {p["key"]: p["value"] for p in points} == {"nested/a": 1.0, "nested/b/c": -1.0}
    assert {p["step_index"] for p in points} == {0}
    run.log({"loss": 0.5})
    assert _points(app)[0]["step_index"] == 1, "a nested call consumes exactly one step"


def test_an_explicit_slash_key_beats_the_nested_spelling_warning_once(client, app):
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="'a/b'"):
        run.log({"a": {"b": 2.0}, "a/b": 1.0})
    assert _metric_values(app, run) == {"a/b": 1.0}

    # Either dict order, and warned once per key per RUN, not per call.
    with warnings.catch_warnings(record=True) as again:
        warnings.simplefilter("always")
        run.log({"a/b": 3.0, "a": {"b": 4.0}})
    assert _metric_values(app, run) == {"a/b": 3.0}
    assert not [w for w in again if "'a/b'" in str(w.message)]


def test_a_nested_string_leaf_lands_in_the_step_record_under_its_flat_key(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"eval": {"text": "looks right", "acc": 0.9}}, step=4)
    assert _metric_values(app, run) == {"eval/acc": 0.9}
    assert _attrs(app, run, 4) == {"eval/text": "looks right"}


def test_lists_are_not_flattened(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"eval": {"hist": [1, 2, {"x": 3}]}}, step=0)
    assert _attrs(app, run) == {"eval/hist": [1, 2, {"x": 3}]}


def test_an_empty_nested_dict_writes_nothing_and_burns_no_step(client, app):
    run = open_run(client, experiment="e", name="r")
    mark = len(app.requests)
    assert run.log({"a": {}, "b": {"c": {}}}) is None
    assert _posts_since(app, mark) == []
    run.log({"loss": 0.5})
    assert _points(app)[0]["step_index"] == 0


def test_dimensions_and_labels_are_never_flattened(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"eval": {"acc": 0.9}}, step=0, dimensions={"split": "val"}, labels={"ex": "x1"})
    (point,) = _points(app)
    assert point["key"] == "eval/acc"
    assert point["dimensions"] == {"split": "val"} and point["labels"] == {"ex": "x1"}
    # A nested dimension is still refused, never quietly turned into "split/name".
    with pytest.raises(ValueError, match="scalar"):
        run.log({"eval": {"acc": 0.9}}, step=1, dimensions={"split": {"name": "val"}})


def _chain(levels: int, leaf: dict) -> dict:
    for i in reversed(range(levels)):
        leaf = {f"l{i}": leaf}
    return leaf


def test_nesting_up_to_the_cap_flattens_fully(client, app):
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.log(_chain(15, {"leaf": 1.0}), step=0)  # a 16-segment key
    (point,) = _points(app)
    assert point["key"].count("/") == 15 and point["key"].endswith("/leaf")
    assert not [w for w in caught if "not flattened" in str(w.message)]


def test_a_mapping_past_the_depth_cap_stays_one_step_attribute(client, app):
    run = open_run(client, experiment="e", name="r")
    mark = len(app.requests)
    with pytest.warns(UserWarning, match="not flattened") as caught:
        run.log(_chain(20, {"leaf": 1.0}), step=0)
    assert len([w for w in caught if "not flattened" in str(w.message)]) == 1
    assert _posts_since(app, mark) == [f"/v1/runs/{run.id}/steps"]
    ((key, value),) = _attrs(app, run).items()
    assert key == "/".join(f"l{i}" for i in range(16))
    assert value == {"l16": {"l17": {"l18": {"l19": {"leaf": 1.0}}}}}


def test_a_dict_that_contains_itself_is_cut_not_followed(client, app):
    run = open_run(client, experiment="e", name="r")
    loop: dict = {"x": 1.0}
    loop["self"] = loop
    with pytest.warns(UserWarning, match="not flattened"):
        run.log({"loop": loop}, step=0)
    assert _metric_values(app, run) == {"loop/x": 1.0}
    assert isinstance(_attrs(app, run)["loop/self"], str)  # repr: JSON cannot hold a cycle


#: Regression contract (plan round 2, Tests): a flat log() is byte-identical to
#: what the SDK sent before nested flattening existed. Captured from the
#: pre-(d) code with this exact call; `json.dumps` in the transport is stdlib, so
#: the bytes are stable.
_FLAT_METRICS_BODY = (
    b'{"points": [{"dimensions": {"split": "val"}, "key": "loss", "kind": "model", '
    b'"labels": {"example": "x1"}, "step_index": 3, "value": 0.25, '
    b'"wall_clock": "2026-01-02T03:04:05Z"}, {"dimensions": {"split": "val"}, '
    b'"key": "train/acc", "kind": "model", "labels": {"example": "x1"}, "step_index": 3, '
    b'"value": 1.0, "wall_clock": "2026-01-02T03:04:05Z"}, {"dimensions": {"split": "val"}, '
    b'"key": "ok", "kind": "model", "labels": {"example": "x1"}, "step_index": 3, '
    b'"value": 1.0, "wall_clock": "2026-01-02T03:04:05Z"}], '
    b'"session_id": "00000000-0000-4000-8000-000000000000", "write_epoch": 1}'
)
_FLAT_STEP_BODY = (
    b'{"step_index": 3, "name": null, "attributes": {"phase": "eval", "cfg": [1, 2]}, '
    b'"session_id": "00000000-0000-4000-8000-000000000000", "write_epoch": 1}'
)


def test_a_flat_log_body_is_byte_identical(client, app, monkeypatch):
    import probe.sdk.run as run_module

    def _never(*_a, **_kw):
        raise AssertionError("a flat call must take the fast path")

    # raising=False: the same bytes hold on the pre-(d) code, which has no _flatten.
    monkeypatch.setattr(run_module, "_flatten", _never, raising=False)
    run = open_run(client, experiment="e", name="r")
    run.session_id = "00000000-0000-4000-8000-000000000000"
    mark = len(app.requests)
    run.log(
        {"loss": 0.25, "train/acc": 1, "ok": True, "phase": "eval", "cfg": [1, 2]},
        step=3,
        wall_clock="2026-01-02T03:04:05+00:00",
        dimensions={"split": "val"},
        labels={"example": "x1"},
    )
    metrics_req, step_req = app.requests[mark:]
    assert metrics_req.content == _FLAT_METRICS_BODY
    assert step_req.content == _FLAT_STEP_BODY


def test_a_dictconfig_flattens_like_a_dict(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create({"opt": {"lr": 3e-4, "name": "adam"}, "bs": 32})
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert _metric_values(app, run) == {"cfg/opt/lr": 3e-4, "cfg/bs": 32.0}
    assert _attrs(app, run) == {"cfg/opt/name": "adam"}

    run.log(cfg, step=1)  # a DictConfig as the whole metrics argument
    assert _metric_values(app, run) == {"opt/lr": 3e-4, "bs": 32.0}


def test_an_unreadable_dictconfig_never_raises_into_the_loop(client, app):
    """A `???` (or a broken reference) is kept as its own text, key by key:
    reading it would raise, and the rest of the config still lands."""
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create({"opt": {"lr": "???", "wd": 0.1, "ref": "${nowhere}"}})
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, "cfg": cfg}, step=0)
    assert _metric_values(app, run) == {"loss": 0.5, "cfg/opt/wd": 0.1}
    assert _attrs(app, run) == {"cfg/opt/lr": "???", "cfg/opt/ref": "${nowhere}"}


def test_a_top_level_dictconfig_with_a_missing_value_never_raises(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    run = open_run(client, experiment="e", name="r")
    run.log(omegaconf.OmegaConf.create({"lr": "???", "opt": {"b": 1.0}}), step=0)
    assert _metric_values(app, run) == {"opt/b": 1.0}
    assert _attrs(app, run) == {"lr": "???"}


# -- flattening must not undo redaction or explode series (#2009 review) --------
_NESTED_SECRETS = {
    "db": {"pwd": "hunter2hunter2", "passwd": "hunter2hunter2"},
    "headers": {"authorization": "Basic Zm9vOmJhcjpiYXo=", "cookie": "session=abcdef0123"},
    "ssh": {"private_key": "my-private-key-material-xyz"},
    "aws": {"aws_access_key_id": "notanakiavalue123"},
    "wandb": {"apikey": "0123456789abcdef0123456789abcdef01234567", "wandb_key": "abcabcabc"},
}


def _wire(app) -> str:
    return "".join(r.content.decode() for r in app.requests if r.content)


def test_flattening_keeps_redaction_by_the_leafs_own_key_name(client, app):
    """The scrubber redacts by a field's OWN key name. Flattened, `db/pwd`
    normalises to `db_pwd`, which matches no rule: all eight of these used to
    leave in cleartext, while the same dict unflattened was redacted."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, **_NESTED_SECRETS}, step=0)

    wire = _wire(app)
    for parent, fields in _NESTED_SECRETS.items():
        for name, secret in fields.items():
            assert secret not in wire, f"{parent}/{name} left in cleartext"
            assert _attrs(app, run)[f"{parent}/{name}"] == "<redacted>"
    assert _metric_values(app, run) == {"loss": 0.5}


def test_a_numeric_secret_is_redacted_not_charted(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, "db": {"pwd": 1234}}, step=0)
    assert _metric_values(app, run) == {"loss": 0.5}
    assert _attrs(app, run) == {"db/pwd": "<redacted>"}


def test_a_dict_under_a_credential_name_is_dropped_whole_as_before(client, app):
    """`{"token": {...}}` is a credential bundle: the scrubber drops the whole
    subtree. Expanded, its leaves escaped as `token/a`."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, "token": {"a": "bundle-secret-1"}}, step=0)
    run.log({"cfg": {"credentials": {"user": "u", "k": "bundle-secret-2"}}}, step=1)
    wire = _wire(app)
    assert "bundle-secret-1" not in wire and "bundle-secret-2" not in wire
    assert "token/a" not in wire and "cfg/credentials/" not in wire
    assert _attrs(app, run, 0) == {"token": "<redacted>"}
    assert _attrs(app, run, 1) == {"cfg/credentials": "<redacted>"}


def test_a_hydra_dictconfig_keeps_its_secrets_redacted(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {
            "lr": 3e-4,
            "db": {"pwd": "hunter2hunter2"},
            "http": {"authorization": "Basic Zm9vOmJhcjpiYXo="},
            "wandb": {"apikey": "0123456789abcdef0123456789abcdef01234567"},
        }
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, "cfg": cfg}, step=0)
    wire = _wire(app)
    for secret in ("hunter2hunter2", "Zm9vOmJhcjpiYXo=", "0123456789abcdef0123456789abcdef01234567"):
        assert secret not in wire
    assert _metric_values(app, run) == {"loss": 0.5, "cfg/lr": 3e-4}
    assert _attrs(app, run) == {
        "cfg/db/pwd": "<redacted>",
        "cfg/http/authorization": "<redacted>",
        "cfg/wandb/apikey": "<redacted>",
    }


def _all_metric_keys(app, run) -> set[str]:
    return {
        p["key"]
        for r in app.requests
        if r.method == "POST" and r.url.path == f"/v1/runs/{run.id}/metrics"
        for p in json.loads(r.content)["points"]
    }


def test_a_dict_keyed_by_data_stops_minting_series_at_the_budget(client, app):
    """`{"per_example_loss": {example_id: v}}` minted a series per id: 12,801 by
    step 400, past the server's 10,000-series cap at step 312, after which the
    server refuses the WHOLE batch -- `loss` included. Past the per-run budget
    of nested keys the mapping stays one step attribute, with one warning."""
    import probe.sdk.run as run_module

    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for step in range(40):
            ids = {f"ex{step * 32 + i}": 0.1 for i in range(32)}
            run.log({"loss": 0.5, "per_example_loss": ids}, step=step)
    keys = _all_metric_keys(app, run)
    assert len(keys) <= 1 + run_module._NESTED_KEY_BUDGET
    assert _metric_values(app, run) == {"loss": 0.5}, "loss keeps landing, alone"
    assert len(_attrs(app, run, 39)["per_example_loss"]) == 32
    assert len([w for w in caught if "'per_example_loss' was not flattened" in str(w.message)]) == 1


def test_a_flattened_key_past_the_length_limit_keeps_its_mapping_whole(client, app):
    run = open_run(client, experiment="e", name="r")
    long_name = "x" * 300
    with pytest.warns(UserWarning, match="'a' was not flattened"):
        run.log({"loss": 0.5, "a": {long_name: 1.0}}, step=0)
    assert _metric_values(app, run) == {"loss": 0.5}
    assert _attrs(app, run) == {"a": {long_name: 1.0}}


class _Split(str, Enum):
    VAL = "val_acc"


def test_top_level_keys_pass_through_unchanged_beside_a_nested_sibling(client, app):
    """A nested sibling must not change how the OTHER keys are spelled: a
    `(str, Enum)` key used to become `_Split.VAL` only when one was present."""
    run = open_run(client, experiment="e", name="r")
    run.log({_Split.VAL: 0.5}, step=0)
    alone = [p["key"] for p in _points(app)]
    run.log({_Split.VAL: 0.5, "x": {"y": 1.0}}, step=1)
    beside = [p["key"] for p in _points(app)]
    assert alone == ["val_acc"] and beside == ["val_acc", "x/y"]


def test_an_int_key_is_refused_the_same_with_or_without_a_nested_sibling(client, app):
    import pydantic

    run = open_run(client, experiment="e", name="r")
    with pytest.raises(pydantic.ValidationError):
        run.log({0: 1.0}, step=None)
    with pytest.raises(pydantic.ValidationError):
        run.log({0: 1.0, "x": {"y": 1.0}}, step=None)


def test_an_unserialisable_value_never_raises_under_an_error_filter(client, app):
    """`-W error` turns a plain warning into an exception, inside the loop."""
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        run.log({"seen": {1, 2}}, step=0)
    assert isinstance(_attrs(app, run)["seen"], str)


# -- #2009 review, round 2 ------------------------------------------------------
#: Matches no content pattern, so only the key rules and the OmegaConf reader
#: can keep it off the wire. (An `sk-live-...` value is removed by the content
#: scrubber whatever the reader does, which made these tests pass on old code.)
_SECRET = "Plain7Zebra4Harbor9Quilt"


def test_the_content_scrubber_leaves_the_test_secret_alone(client, app):
    """Control: without it, `_SECRET not in _wire(app)` proves nothing."""
    run = open_run(client, experiment="e", name="r")
    run.log({"note": _SECRET}, step=0)
    assert _SECRET in _wire(app)


def test_an_interpolation_of_a_secret_is_sent_unresolved(client, app):
    """Reading a DictConfig resolves `${...}`. `client.auth` has a harmless
    name, so the resolved API key would have left in cleartext under it."""
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {"wandb": {"api_key": _SECRET}, "client": {"auth": "${wandb.api_key}", "retries": 3}}
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert _SECRET not in _wire(app)
    assert _attrs(app, run)["cfg/client/auth"] == "${wandb.api_key}"
    assert _metric_values(app, run) == {"cfg/client/retries": 3.0}


def test_an_environment_interpolation_is_sent_unresolved(client, app, monkeypatch):
    omegaconf = pytest.importorskip("omegaconf")
    monkeypatch.setenv("SERVICE_KEY", _SECRET)
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": omegaconf.OmegaConf.create({"service": {"key": "${oc.env:SERVICE_KEY}"}})}, step=0)
    run.log(omegaconf.OmegaConf.create({"endpoint": "${oc.env:SERVICE_KEY}"}), step=1)
    assert _SECRET not in _wire(app)
    assert _attrs(app, run, 0) == {"cfg/service/key": "${oc.env:SERVICE_KEY}"}
    assert _attrs(app, run, 1) == {"endpoint": "${oc.env:SERVICE_KEY}"}


def test_a_chain_of_references_to_a_secret_is_sent_unresolved(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {"wandb": {"api_key": _SECRET}, "b": "${wandb.api_key}", "client": {"header": "Bearer ${b}"}}
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert _SECRET not in _wire(app)
    assert _attrs(app, run)["cfg/client/header"] == "Bearer ${b}"


def test_a_harmless_interpolation_still_resolves(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {"opt": {"lr": 0.1, "warmup_lr": "${opt.lr}"}, "name": "run-${opt.lr}"}
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert _metric_values(app, run) == {"cfg/opt/lr": 0.1, "cfg/opt/warmup_lr": 0.1}
    assert _attrs(app, run) == {"cfg/name": "run-0.1"}


# -- #2009 review, round 3 ------------------------------------------------------
_GROUP_ALIASES = {
    "alias": {"credentials": {"x": _SECRET}, "alias": "${credentials}", "c": {"auth": "${alias}"}},
    "nested-key": {"which": "credentials", "credentials": {"x": _SECRET}, "c": {"auth": "${${which}}"}},
    "oc.select": {"which": "credentials", "credentials": {"x": _SECRET}, "c": {"auth": "${oc.select:${which}}"}},
    "oc.create": {"credentials": {"x": _SECRET}, "alias": "${credentials}", "c": {"auth": "${oc.create:${alias}}"}},
    "secret-group": {"secret": {"value": _SECRET}, "alias": "${secret}", "c": {"auth": "${alias}"}},
    "list": {"password": [_SECRET], "alias": "${password}", "c": {"auth": "${alias}"}},
}


@pytest.mark.parametrize("name", sorted(_GROUP_ALIASES))
def test_an_alias_to_a_whole_credential_group_is_sent_unresolved(client, app, name):
    """`auth: ${alias}` resolves to the whole credentials NODE, and only a
    string or number result was checked: flattening then sent `cfg/c/auth/x`
    (or the list's repr) with the secret, under a name no rule redacts."""
    omegaconf = pytest.importorskip("omegaconf")
    data = _GROUP_ALIASES[name]
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.log({"cfg": omegaconf.OmegaConf.create(data)}, step=0)
    assert _SECRET not in _wire(app)
    assert not any(_SECRET in str(w.message) for w in caught)
    assert _attrs(app, run)["cfg/c/auth"] == data["c"]["auth"]


def test_an_alias_to_a_harmless_group_still_flattens(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {"api_key": _SECRET, "opt": {"lr": 0.1, "name": "adam"}, "alias": "${opt}", "c": {"o": "${alias}"}}
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert _metric_values(app, run) == {"cfg/opt/lr": 0.1, "cfg/alias/lr": 0.1, "cfg/c/o/lr": 0.1}
    assert _attrs(app, run) == {
        "cfg/api_key": "<redacted>",
        "cfg/opt/name": "adam",
        "cfg/alias/name": "adam",
        "cfg/c/o/name": "adam",
    }


def test_a_switch_under_a_credential_name_hides_no_number(client, app):
    """`use_auth_token: true` was remembered as a secret, and True == 1 (False
    == 0), so every `${...}` resolving to 1 or 0.0 was sent as its text."""
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {
            "hf": {"use_auth_token": True, "token": False},
            "trainer": {"devices": 1, "gpus": "${trainer.devices}", "wd": 0.0, "wd2": "${trainer.wd}"},
        }
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    values = _metric_values(app, run)
    assert values["cfg/trainer/gpus"] == 1.0 and values["cfg/trainer/wd2"] == 0.0


def test_a_numeric_secret_read_back_as_a_number_is_sent_unresolved(client, app):
    """`${oc.decode:...}` turns `password: "839201"` into the int 839201, which
    was compared with number secrets only and charted as 839201.0."""
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {"password": "839201", "alias": "${password}", "c": {"x": "${oc.decode:${alias}}"}}
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert "839201" not in _wire(app)
    assert _attrs(app, run)["cfg/c/x"] == "${oc.decode:${alias}}"


def test_a_short_secret_inside_a_string_is_sent_unresolved(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {"db": {"password": "Qz9w1"}, "alias": "${db.password}", "c": {"dsn": "pw=${alias}"}}
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert "Qz9w1" not in _wire(app)
    assert _attrs(app, run)["cfg/c/dsn"] == "pw=${alias}"


def test_a_tiny_environment_value_leaves_harmless_values_resolved(client, app, monkeypatch):
    """Control for the length floor: an env read of `0` is a "secret" too, and
    searched for inside strings or compared with numbers it would turn
    `lr=0.1` and `${opt.n}` into text."""
    omegaconf = pytest.importorskip("omegaconf")
    monkeypatch.setenv("LOCAL_RANK", "0")
    cfg = omegaconf.OmegaConf.create(
        {"rank": "${oc.env:LOCAL_RANK}", "opt": {"lr": 0.1, "n": 0, "m": "${opt.n}"}, "name": "lr=${opt.lr}"}
    )
    run = open_run(client, experiment="e", name="r")
    run.log({"cfg": cfg}, step=0)
    assert _metric_values(app, run) == {"cfg/opt/lr": 0.1, "cfg/opt/n": 0.0, "cfg/opt/m": 0.0}
    assert _attrs(app, run) == {"cfg/rank": "${oc.env:LOCAL_RANK}", "cfg/name": "lr=0.1"}


def test_a_dict_of_dicts_keyed_by_data_costs_one_attribute_and_one_warning(client, app):
    """`{"per_ex": {example_id: {"loss": v}}}`: the budget was checked per
    inner mapping, so once spent every id was kept whole on its own -- 2,000
    warnings and 2,000 step attributes for 3,000 ids, and the warned set grew
    without bound. Now the TOP-LEVEL value is kept whole, warned once."""
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for step in range(100):
            per_ex = {f"ex{step * 30 + i}": {"loss": 0.1} for i in range(30)}
            run.log({"loss": 0.5, "per_ex": per_ex}, step=step)
    said = [w for w in caught if "not flattened" in str(w.message)]
    assert len(said) == 1 and "'per_ex'" in str(said[0].message)
    assert len(run._flatten_warned) == 1
    assert _metric_values(app, run) == {"loss": 0.5}
    assert set(_attrs(app, run, 99)) == {"per_ex"} and len(_attrs(app, run, 99)["per_ex"]) == 30
    assert len(_all_metric_keys(app, run)) <= 1 + 1_000


def test_the_warned_set_is_bounded(client, app):
    import probe.sdk.run as run_module

    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for i in range(run_module._FLATTEN_WARNINGS_REMEMBERED + 50):
            loop: dict = {"x": 1.0}
            loop["self"] = loop
            run.log({f"k{i}": loop}, step=i)
    assert len(run._flatten_warned) == run_module._FLATTEN_WARNINGS_REMEMBERED


def test_flattened_model_token_names_are_not_over_redacted(client, app):
    """The server-bound scrub judged `tok/pad_token` as one name ending in
    `_token` and redacted it; nested, `pad_token` is a model setting. Each
    segment is now judged by its own name, as it would be nested."""
    run = open_run(client, experiment="e", name="r")
    run.log({"tok": {"pad_token": "<pad>", "eos_token": "</s>"}, "gen": {"token": "the"}}, step=0)
    assert _attrs(app, run) == {"tok/pad_token": "<pad>", "tok/eos_token": "</s>", "gen/token": "the"}


def test_an_explicit_slash_key_is_now_judged_per_segment_too(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"headers/authorization": "Basic Zm9vOmJhcjpiYXo=", "api/key": "k3y-value-x"}, step=0)
    assert "Zm9vOmJhcjpiYXo=" not in _wire(app) and "k3y-value-x" not in _wire(app)


def test_a_bytes_top_level_key_is_checked_by_name(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, b"token": {"a": "bundle-secret-3"}}, step=0)
    assert "bundle-secret-3" not in _wire(app)
    assert _metric_values(app, run) == {"loss": 0.5}


# -- commit= (SDK reliability plan (f)) -----------------------------------------
def _metric_posts(app, run):
    return [
        json.loads(r.content)
        for r in app.requests
        if r.method == "POST" and r.url.path == f"/v1/runs/{run.id}/metrics"
    ]


def _triples(app, run):
    return sorted(
        (p["key"], p["value"], p.get("step_index"))
        for body in _metric_posts(app, run)
        for p in body["points"]
    )


@pytest.mark.parametrize("pattern", ["one_call", "commit_false", "same_step"])
def test_the_three_wandb_patterns_write_the_same_points(client, app, pattern):
    """W&B documents these as three ways to put two values on one step. They
    must land identically, and the next bare log() must move on to step 1."""
    run = open_run(client, experiment="e", name="r")
    if pattern == "one_call":
        run.log({"loss": 0.5, "acc": 0.8})
    elif pattern == "commit_false":
        run.log({"loss": 0.5}, commit=False)
        run.log({"acc": 0.8})
    else:
        run.log({"loss": 0.5}, step=0)
        run.log({"acc": 0.8}, step=0)
    run.log({"loss": 0.4})
    assert _triples(app, run) == sorted([("loss", 0.5, 0), ("acc", 0.8, 0), ("loss", 0.4, 1)])


def test_commit_false_buffers_then_the_next_call_writes_the_row_once(client, app):
    run = open_run(client, experiment="e", name="r")
    mark = len(app.requests)
    run.log({"loss": 0.5, "phase": "train"}, commit=False)
    assert _posts_since(app, mark) == [], "commit=False sends nothing"
    run.log({"acc": 0.8})
    assert _posts_since(app, mark) == [f"/v1/runs/{run.id}/metrics", f"/v1/runs/{run.id}/steps"]
    assert _triples(app, run) == [("acc", 0.8, 0), ("loss", 0.5, 0)]
    assert _attrs(app, run, 0) == {"phase": "train"}


def test_commit_false_twice_keeps_the_last_value(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, commit=False)
    run.log({"loss": 2.0}, commit=False)
    run.log({"acc": 0.5})
    assert _triples(app, run) == [("acc", 0.5, 0), ("loss", 2.0, 0)]
    assert len(_metric_posts(app, run)) == 1


def test_a_different_step_flushes_the_pending_row_first(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, step=3, commit=False)
    run.log({"loss": 0.9}, step=4)
    rows = [[(p["key"], p["step_index"]) for p in b["points"]] for b in _metric_posts(app, run)]
    assert rows == [[("loss", 3)], [("loss", 4)]]


def test_an_omitted_step_joins_the_pending_rows_step(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, step=7, commit=False)
    run.log({"acc": 0.5})
    assert _triples(app, run) == [("acc", 0.5, 7), ("loss", 1.0, 7)]
    run.log({"loss": 0.8})
    assert _points(app)[0]["step_index"] == 8


def test_an_empty_committing_call_writes_the_pending_row(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, commit=False)
    run.log({})
    assert _triples(app, run) == [("loss", 1.0, 0)]
    run.log({"loss": 0.5})
    assert _points(app)[0]["step_index"] == 1


def test_pending_rows_are_per_kind(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, commit=False)
    run.log_hw({"gpu_util": 50.0})  # the hardware rail writes now; the model row waits
    assert [p["key"] for p in _points(app)] == ["gpu_util"]
    run.log({"acc": 0.5})
    assert [(p["key"], p["step_index"]) for p in _points(app)] == [("loss", 0), ("acc", 0)]


def test_a_pending_row_is_delivered_at_finish(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0, "phase": "last"}, commit=False)
    run.finish()
    sent = [(r.method, r.url.path) for r in app.requests]
    metrics_at = sent.index(("POST", f"/v1/runs/{run.id}/metrics"))
    closed_at = max(i for i, s in enumerate(sent) if s == ("PATCH", f"/v1/runs/{run.id}"))
    assert metrics_at < closed_at, "the row must land before the run closes"
    assert _triples(app, run) == [("loss", 1.0, 0)]
    assert _attrs(app, run, 0) == {"phase": "last"}


def test_a_pending_row_is_delivered_when_the_with_block_exits(client, app):
    with open_run(client, experiment="e", name="r") as run:
        run.log({"loss": 1.0}, commit=False)
    assert _triples(app, run) == [("loss", 1.0, 0)]
    assert app.runs[run.id]["status"] == "completed"


def test_step_attributes_written_twice_at_one_step_are_unioned(client, app):
    """The server REPLACES a step record's attributes on upsert
    (`spans_router.py`: `attributes = EXCLUDED.attributes`), so a second log()
    at the same step used to wipe the first one's strings."""
    run = open_run(client, experiment="e", name="r")
    run.log({"phase": "eval"}, step=3)
    run.log({"note": "x"}, step=3)
    assert _attrs(app, run, 3) == {"phase": "eval", "note": "x"}
    run.log({"phase": "test"}, step=3)  # new wins per key
    assert _attrs(app, run, 3) == {"phase": "test", "note": "x"}


def test_a_failed_flush_never_raises_even_on_a_strict_client(app, tmp_path):
    from tests.conftest import make_client

    c = make_client(app, fail_open=False, tmp_spool=tmp_path / "spool")
    run = open_run(c, experiment="e", name="r")
    run.log({"loss": 1.0}, step=1, commit=False)
    app.fail_next_metrics = True
    run.log({"loss": 0.9}, step=2)  # the step-1 flush hits the 503: no raise
    assert c.journal.pending(), "the flushed row is kept durable, not dropped"
    run.finish()  # the hard barrier delivers it
    delivered = app.metric_points_posted[run.id]  # accepted writes only, not the 503
    assert sorted((p["key"], p["value"], p["step_index"]) for p in delivered) == [
        ("loss", 0.9, 2),
        ("loss", 1.0, 1),
    ]


def test_a_dropped_non_numeric_value_never_raises_under_an_error_filter(client, app):
    """`log({"phase": ...}, step=None)` drops the string with a warning. Under
    `-W error` a plain warning raised into the loop; inside finish()'s flush it
    would also have read as a lost row, though the numbers had landed."""
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        run.log({"loss": 1.0, "phase": "eval"}, step=None)
        run.log({"loss": 2.0, "phase": "test"}, step=None, commit=False)
        run.finish()
    assert sorted(p["value"] for p in app.metric_points_posted[run.id]) == [1.0, 2.0]
    assert app.runs[run.id]["status"] == "completed"


def test_an_error_while_flushing_at_finish_never_raises(client, app, monkeypatch):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, commit=False)
    real_write = run._client.write

    def write(method, path, *args, **kwargs):
        if path.endswith("/metrics"):
            raise errors.TransportError("connection reset")
        return real_write(method, path, *args, **kwargs)

    monkeypatch.setattr(run._client, "write", write)
    with pytest.warns(UserWarning, match="commit=False"):
        run.finish()
    assert app.runs[run.id]["status"] == "completed"


# -- #2025 review ---------------------------------------------------------------
def _in_a_signal_handler_while_log_holds_the_lock(run, body) -> dict:
    """Run ``body`` in a SIGALRM handler while `_pending_lock` is held, as it
    is by the log(commit=False) call the signal interrupted. The safety timer
    stands in for "forever", so a regression fails in seconds, not a CI hour."""
    done: dict = {}

    def handler(signum, frame):
        started = time.monotonic()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            body()
        done["seconds"] = time.monotonic() - started
        done["said"] = [str(w.message) for w in caught]

    previous = signal.signal(signal.SIGALRM, handler)
    safety = threading.Timer(5.0, run._pending_lock.release)
    try:
        run._pending_lock.acquire()  # what an interrupted log(commit=False) holds
        safety.start()
        signal.setitimer(signal.ITIMER_REAL, 0.05)
        deadline = time.monotonic() + 10
        while "seconds" not in done and time.monotonic() < deadline:
            time.sleep(0.01)
    finally:
        safety.cancel()
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
        if run._pending_lock.locked():
            run._pending_lock.release()
    return done


@pytest.mark.skipif(not hasattr(signal, "setitimer"), reason="needs POSIX interval timers")
def test_finish_from_a_signal_handler_never_hangs_on_a_held_row(client, app):
    """SLURM `--signal=USR1` and submitit preemption call finish() from a
    signal handler, on the very thread the signal interrupted. If that was
    inside log(commit=False), the thread holds `_pending_lock` and never
    releases it: a plain wait hung the handler forever."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, commit=False)
    done = _in_a_signal_handler_while_log_holds_the_lock(run, run.finish)
    assert done["seconds"] < 3.0, f"finish() waited {done['seconds']:.1f}s on the held lock"
    assert any("could not flush" in message for message in done["said"])
    assert app.runs[run.id]["status"] == "completed"


@pytest.mark.skipif(not hasattr(signal, "setitimer"), reason="needs POSIX interval timers")
def test_log_from_a_signal_handler_never_hangs_on_a_held_row(client, app):
    """The usual handler records the preemption, THEN finishes. With a row
    pending, that log() took the buffered path and waited on the lock with no
    timeout, so it hung where finish() no longer did. Past a short wait it is
    now written at once, as an ordinary write."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 1.0}, commit=False)

    def preempted():
        run.log({"preempted": 1.0})
        run.finish()

    done = _in_a_signal_handler_while_log_holds_the_lock(run, preempted)
    assert done["seconds"] < 3.0, f"the handler waited {done['seconds']:.1f}s on the held lock"
    assert _triples(app, run) == [("preempted", 1.0, 0)]
    assert app.runs[run.id]["status"] == "completed"


def test_a_bad_point_is_refused_when_it_is_held_not_at_the_next_call(client, app):
    import pydantic

    run = open_run(client, experiment="e", name="r")
    with pytest.raises(pydantic.ValidationError):
        run.log({0: 1.0}, commit=False)
    run.log({"acc": 0.5})
    assert _triples(app, run) == [("acc", 0.5, 0)]


def test_commit_false_after_finish_warns_once(client, app):
    run = open_run(client, experiment="e", name="r")
    run.finish()
    with pytest.warns(UserWarning, match=r"commit=False\) after finish"):
        run.log({"loss": 1.0}, commit=False)
    with warnings.catch_warnings(record=True) as again:
        warnings.simplefilter("always")
        run.log({"loss": 2.0}, commit=False)
    assert not [w for w in again if "after finish" in str(w.message)]


def test_a_step_record_keeps_its_name_and_keys_through_a_later_log(client, app):
    """The server replaces the record whole, so a log() at the same step used
    to wipe the name and attributes a direct run.step() had written."""
    run = open_run(client, experiment="e", name="r")
    run.step(3, name="warmup", attributes={"phase": "a"})
    run.log({"note": "x"}, step=3)
    record = app.steps[run.id][3]
    assert record["name"] == "warmup"
    assert record["attributes"] == {"phase": "a", "note": "x"}


# -- non-numeric values --------------------------------------------------------
def _attrs(app, run, step=0):
    return app.steps[run.id][step]["attributes"]


def test_mixed_types_in_one_call_split_by_where_they_can_be_stored(client, app):
    """`metric_points.value` is DOUBLE PRECISION NOT NULL, so this is a schema
    boundary, not a preference. Numbers plot; everything else lands in that
    step's record, at the same step index."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.4, "phase": "eval", "cfg": {"lr": 3e-4, "opt": "adam"}}, step=7)

    points = json.loads(app.requests[-2].content)["points"]
    # A nested dict is flattened first (plan (d)), then split like any other key.
    assert [(p["key"], p["value"]) for p in points] == [("loss", 0.4), ("cfg/lr", 3e-4)]
    assert _attrs(app, run, 7) == {"phase": "eval", "cfg/opt": "adam"}


def test_a_string_no_longer_takes_its_numeric_neighbours_down(client, app):
    """The real bug this fixes. `float()` ran while building MetricBatch — before
    client.write()'s try/except — so one non-numeric key raised out of the
    training loop AND discarded every numeric metric in the same call."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.4, "dockq": 0.8, "note": "converged"}, step=1)

    points = json.loads(app.requests[-2].content)["points"]
    assert {p["key"] for p in points} == {"loss", "dockq"}
    assert _attrs(app, run, 1) == {"note": "converged"}


def test_types_survive_the_round_trip(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"s": "text", "d": {"a": "x"}, "l": [1, {"k": 2}], "n": None}, step=0)
    # A nested dict flattens to "d/a" (plan (d)); a list is kept as it is.
    assert _attrs(app, run) == {"s": "text", "d/a": "x", "l": [1, {"k": 2}], "n": None}


def test_a_numeric_string_stays_a_string(client, app):
    """`float("0.4")` parses, so coercing would silently make "0.4" and 0.4
    indistinguishable afterwards. A caller who logged a string meant one."""
    run = open_run(client, experiment="e", name="r")
    run.log({"version": "0.4"}, step=0)
    assert _attrs(app, run) == {"version": "0.4"}


def test_bools_stay_plottable(client, app):
    """W&B charts bools as 0/1, and a chart is what people log them for."""
    run = open_run(client, experiment="e", name="r")
    run.log({"converged": True, "diverged": False}, step=0)
    points = json.loads(app.requests[-1].content)["points"]
    assert {p["key"]: p["value"] for p in points} == {"converged": 1.0, "diverged": 0.0}
    assert run.id not in app.steps


def test_anything_with_a_float_dunder_is_a_metric(client, app):
    """numpy scalars and 0-d torch tensors arrive this way and must not be
    demoted to attributes just because they are not `float`."""

    class Scalar:
        def __float__(self):
            return 0.25

    run = open_run(client, experiment="e", name="r")
    run.log({"loss": Scalar()}, step=0)
    assert json.loads(app.requests[-1].content)["points"][0]["value"] == 0.25


def test_an_unserialisable_value_is_kept_as_repr_not_raised(client, app):
    """attributes is JSONB, so this would otherwise fail at encode time — inside
    the loop, past the fail-open boundary. repr loses fidelity, never the loop."""
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="not JSON-serialisable"):
        run.log({"seen": {1, 2}}, step=0)
    assert isinstance(_attrs(app, run)["seen"], str)


def test_non_numeric_needs_a_step_and_says_so_when_there_is_none(client, app):
    """A step record is keyed by step_index. `step=None` explicitly means "no step
    axis", so there is nowhere to put these — but the numeric ones still land."""
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="dropped non-numeric"):
        run.log({"loss": 0.4, "phase": "eval"}, step=None)
    points = json.loads(app.requests[-1].content)["points"]
    assert {p["key"] for p in points} == {"loss"}
    assert app.steps == {}


def test_the_return_value_still_reports_the_metric_write(client, app):
    """connectors/harbor.py keys "confirmed" vs "spooled" off this."""
    run = open_run(client, experiment="e", name="r")
    assert run.log({"loss": 0.4, "phase": "eval"}, step=0) is not None
    # with nothing numeric to write, the step record's result stands in
    assert run.log({"phase": "eval"}, step=1) is not None


# -- auto-increment step -------------------------------------------------------
def _points(app):
    return json.loads(app.requests[-1].content)["points"]


def test_a_bare_log_auto_increments_the_step(client, app):
    """The ported W&B loop. `for batch in loader: run.log({"loss": l})` has to
    produce a curve; without a counter every point arrives with no step at all and
    lands on the wall-clock axis as an unordered pile."""
    run = open_run(client, experiment="e", name="r")
    steps = []
    for loss in (0.5, 0.4, 0.3):
        run.log({"loss": loss})
        steps.append(_points(app)[0]["step_index"])
    assert steps == [0, 1, 2]


def test_every_key_in_one_call_shares_a_step(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, "dockq": 0.7})
    assert {p["step_index"] for p in _points(app)} == {0}
    run.log({"loss": 0.4, "dockq": 0.8})
    assert {p["step_index"] for p in _points(app)} == {1}


def test_an_explicit_none_still_means_no_step(client, app):
    """What the CLI, the Miles exporter and the Harbor importer all pass. Each
    invocation of `probe log` is its own process, so a per-handle counter would
    restart at 0 every time — worse than no step. Only an OMITTED step opts in."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5}, step=None)
    assert "step_index" not in _points(app)[0]


def test_an_explicit_step_is_used_and_moves_the_counter_past_it(client, app):
    """Mixing the two forms must not stack a second series on steps the loop
    already used."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5}, step=41)
    assert _points(app)[0]["step_index"] == 41
    run.log({"loss": 0.4})
    assert _points(app)[0]["step_index"] == 42


def test_hardware_and_model_counters_are_independent(client, app):
    """A GPU sampler on its own thread must not shift the loss curve."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5})  # model 0
    run.log_hw({"gpu_temp": 88})  # hardware 0
    run.log_hw({"gpu_temp": 89})  # hardware 1
    assert _points(app)[0]["step_index"] == 1
    run.log({"loss": 0.4})  # model 1, unaffected by the two hw points
    assert _points(app)[0]["step_index"] == 1


def test_concurrent_logging_never_reuses_a_step(client, app):
    """Logging from several threads is ordinary — a sampler beside a training
    loop — and two threads reading the counter unguarded would put two different
    points on one step."""
    run = open_run(client, experiment="e", name="r")
    seen: list[int] = []
    lock = threading.Lock()
    threads_n, per_thread = 8, 2000

    def worker():
        for _ in range(per_thread):
            step = run._next_step("model")
            with lock:
                seen.append(step)

    # Without this the test is vacuous: the critical section is three bytecodes,
    # so at the default 5ms switch interval an UNLOCKED counter passes too —
    # verified by deleting the lock and watching the suite stay green.
    previous = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    try:
        threads = [threading.Thread(target=worker) for _ in range(threads_n)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    finally:
        sys.setswitchinterval(previous)

    assert sorted(seen) == list(range(threads_n * per_thread))


def test_span_generates_uuid_and_posts(client, app):
    run = open_run(client, experiment="e", name="r")
    span_id = run.span("rollout", name="rollout-0", step_index=1)
    assert app.spans_upserted == 1
    body = json.loads(app.requests[-1].content)
    assert body["spans"][0]["id"] == span_id
    assert body["spans"][0]["span_type"] == "rollout"


# -- span scopes --------------------------------------------------------------
def _last_state(app, run, span_id):
    """The most recent upsert of one span. The fake appends rather than merging,
    so an upserted span appears once per write."""
    return [s for s in app.spans[run.id] if s["id"] == span_id][-1]


def test_a_span_id_is_still_an_ordinary_string(client, app):
    """SpanHandle subclasses str so the two-call form keeps working untouched —
    callers store it, format it, and pass it back as `id=`."""
    run = open_run(client, experiment="e", name="r")
    span_id = run.span("rollout", name="rollout-0")
    assert isinstance(span_id, str)
    assert f"{span_id}" == str(span_id)
    assert {span_id: 1}[span_id] == 1
    run.span("rollout", id=span_id, status="completed", ended_at="2026-07-27T00:00:00Z")
    assert _last_state(app, run, span_id)["status"] == "completed"


def test_a_span_scope_closes_the_span_on_the_way_out(client, app):
    run = open_run(client, experiment="e", name="r")
    with run.span("rollout", name="rollout-0") as span:
        assert _last_state(app, run, span)["status"] == "running"
    final = _last_state(app, run, span)
    assert final["status"] == "completed"
    assert final["ended_at"] is not None
    assert final["started_at"] is not None


def test_a_raising_body_fails_the_span_rather_than_leaving_it_running(client, app):
    """The reason this exists. Spans have no heartbeat and no server-side reaper,
    so a span abandoned by a raise stays `running` forever with nothing to correct
    it. The exception still propagates — the span records the failure, it does not
    swallow it."""
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError, match="rollout diverged"):
        with run.span("rollout", name="rollout-0") as span:
            raise ValueError("rollout diverged")
    final = _last_state(app, run, span)
    assert final["status"] == "failed"
    assert final["ended_at"] is not None
    assert final["attributes"]["error.type"] == "ValueError"
    assert final["attributes"]["error.message"] == "rollout diverged"


def test_attributes_set_inside_the_block_are_sent_on_close(client, app):
    run = open_run(client, experiment="e", name="r")
    with run.span("rollout", name="rollout-0", attributes={"task": "fold"}) as span:
        span.attributes["reward"] = 0.8
    final = _last_state(app, run, span)
    assert final["attributes"] == {"task": "fold", "reward": 0.8}


def test_spans_nest_without_threading_the_parent_by_hand(client, app):
    run = open_run(client, experiment="e", name="r")
    with run.span("rollout", name="rollout-0") as rollout:
        with run.span("turn", name="turn-0") as turn:
            tool = run.span("tool_call", name="search")
        after_turn = run.span("turn", name="turn-1")
    detached = run.span("rollout", name="rollout-1")

    assert _last_state(app, run, rollout)["parent_span_id"] is None
    assert _last_state(app, run, turn)["parent_span_id"] == str(rollout)
    # a plain (non-scope) span still adopts the enclosing scope
    assert _last_state(app, run, tool)["parent_span_id"] == str(turn)
    # ...and the scope is popped on exit, so the next sibling re-parents correctly
    assert _last_state(app, run, after_turn)["parent_span_id"] == str(rollout)
    assert _last_state(app, run, detached)["parent_span_id"] is None


def test_an_explicit_none_is_honoured_so_replays_are_not_fabricated(client, app):
    """The ATIF expander and the Harbor importer replay STORED trajectories and
    pass `started_at=<maybe None>` on purpose — a stored step may have no usable
    timestamp. Defaulting those to now() would write a fabricated time into a
    historical record, so only an OMITTED argument gets a default."""
    run = open_run(client, experiment="e", name="r")
    replayed = run.span("rollout", name="old", started_at=None, parent_span_id=None)
    live = run.span("rollout", name="new")

    assert _last_state(app, run, replayed)["started_at"] is None
    assert _last_state(app, run, live)["started_at"] is not None


def test_a_replayed_span_is_not_reparented_by_an_enclosing_scope(client, app):
    run = open_run(client, experiment="e", name="r")
    with run.span("rollout", name="rollout-0"):
        replayed = run.span("turn", name="stored", parent_span_id=None)
    assert _last_state(app, run, replayed)["parent_span_id"] is None


def test_link_writes_real_foreign_keys_column(client, app):
    run = open_run(client, experiment="e", name="r")
    run.link(wandb_run_id="abc", s3_prefix="s3://x/y")
    # real runs.foreign_keys column (not metadata), server-merged
    assert app.runs[run.id]["foreign_keys"] == {"wandb_run_id": "abc", "s3_prefix": "s3://x/y"}
    # a later link merges per-key new-wins (overwrite one, keep the rest)
    run.link(wandb_run_id="def")
    assert app.runs[run.id]["foreign_keys"] == {"wandb_run_id": "def", "s3_prefix": "s3://x/y"}
    assert "foreign_keys" not in (app.runs[run.id].get("metadata") or {})


def test_artifact_with_uri(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log_artifact("final.sif", uri="r2://bucket/final.sif", kind="artifact")
    body = json.loads(app.requests[-1].content)
    assert body["uri"] == "r2://bucket/final.sif"
    assert body["name"] == "final.sif"


def test_artifact_path_reference_records_pointer_without_uploading(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    f = tmp_path / "ckpt.pt"
    f.write_bytes(b"x" * 2048)
    run.log_artifact("ckpt.pt", path=str(f), reference=True)
    req = app.requests[-1]
    # Direct create door, NOT the presign /uploads flow -- no bytes are uploaded.
    assert req.url.path == f"/v1/runs/{run.id}/artifacts"
    body = json.loads(req.content)
    assert body["is_reference"] is True
    assert body["uri"].startswith("file://") and body["uri"].endswith("/ckpt.pt")
    assert body["meta"]["local_path"] == str(f)
    assert body["meta"]["host"]
    assert body["size_bytes"] == 2048  # os.stat, not a read
    assert "content_hash" not in body  # no --hash -> no whole-file read


def test_artifact_path_reference_hash_opts_into_fingerprint(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    f = tmp_path / "big.bin"
    f.write_bytes(b"y" * 4096)
    run.log_artifact("big.bin", path=str(f), reference=True, hash_content=True)
    body = json.loads(app.requests[-1].content)
    assert body["is_reference"] is True
    assert len(body["content_hash"]) == 64  # sha256 hex
    assert body["size_bytes"] == 4096


def test_a_folder_reference_carries_the_folders_size(client, app, tmp_path):
    """Plan (a): a sharded checkpoint (DeepSpeed, FSDP) is a FOLDER. Its size
    is what is inside it, not the 4096-byte directory entry; symlinks are not
    followed out of it; hash_content does not apply to a folder."""
    ckpt = tmp_path / "epoch=1-step=8.ckpt"
    (ckpt / "checkpoint").mkdir(parents=True)
    (ckpt / "checkpoint" / "mp_rank_00_model_states.pt").write_bytes(b"m" * 3000)
    (ckpt / "latest").write_bytes(b"12")
    outside = tmp_path / "outside.bin"
    outside.write_bytes(b"o" * 10_000)
    (ckpt / "link").symlink_to(outside)
    run = open_run(client, experiment="e", name="r")

    with pytest.warns(UserWarning, match="hash_content=True does not apply to a folder"):
        run.log_artifact(ckpt.name, path=str(ckpt), reference=True, hash_content=True)

    body = json.loads(app.requests[-1].content)
    assert body["is_reference"] is True
    assert body["size_bytes"] == 3002
    assert body["meta"]["is_directory"] is True and body["meta"]["n_files"] == 2
    assert body["meta"]["content_hash_skipped"] == "directory"
    assert "content_hash" not in body and "size_partial" not in body["meta"]


@pytest.mark.parametrize("bound", ["entries", "seconds"])
def test_a_folder_reference_walk_is_bounded(client, app, tmp_path, monkeypatch, bound):
    """The folder walk runs beside a training loop, maybe on a network
    filesystem: past its bound the size is a lower bound, and the row says so."""
    from probe.sdk import hashing

    folder = tmp_path / "shards"
    folder.mkdir()
    for i in range(5):
        (folder / f"shard{i}").write_bytes(b"s" * 10)
    if bound == "entries":
        monkeypatch.setattr(hashing, "FOLDER_MAX_ENTRIES", 2)
    else:
        monkeypatch.setattr(hashing, "FOLDER_MAX_SECONDS", -1.0)
    run = open_run(client, experiment="e", name="r")

    run.log_artifact("shards", path=str(folder), reference=True)

    body = json.loads(app.requests[-1].content)
    assert body["meta"]["size_partial"] is True
    assert body["meta"]["n_files"] < 5 and body["size_bytes"] == 10 * body["meta"]["n_files"]


def test_a_folder_reference_whose_size_the_caller_measured_is_not_walked_again(
    client, app, tmp_path, monkeypatch
):
    """Plan (a) review: the Lightning logger sums a sharded checkpoint itself
    (it keeps the size for later refreshes of the row); `log_artifact` summed
    the same folder a second time beside the training loop."""
    from probe.sdk import hashing

    folder = tmp_path / "shards"
    folder.mkdir()
    (folder / "shard0").write_bytes(b"s" * 10)
    walks = []
    monkeypatch.setattr(hashing, "folder_size", lambda root: walks.append(root) or (0, 0, True))
    run = open_run(client, experiment="e", name="r")

    run.log_artifact("shards", path=str(folder), reference=True, size_bytes=1234)

    body = json.loads(app.requests[-1].content)
    assert walks == [] and body["size_bytes"] == 1234 and body["meta"]["is_directory"] is True
    run.log_artifact("shards", path=str(folder), reference=True)  # the control: no size given
    assert walks == [str(folder)]


def test_artifact_path_reference_missing_path_raises_unless_allowed(client, app):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(FileNotFoundError):
        run.log_artifact("gone.pt", path="/no/such/file.pt", reference=True)
    # allow_missing records it anyway (it may live on a mount/host this machine lacks).
    run.log_artifact("gone.pt", path="/mnt/shared/gone.pt", reference=True, allow_missing=True)
    body = json.loads(app.requests[-1].content)
    assert body["is_reference"] is True
    assert body["uri"] == "file:///mnt/shared/gone.pt"
    assert "size_bytes" not in body  # not stat-able here


def test_finish_sets_status_and_ended_at(client, app):
    run = open_run(client, experiment="e", name="r")
    run.finish("completed")
    row = app.runs[run.id]
    assert row["status"] == "completed"
    assert row["ended_at"] is not None


def test_context_manager_marks_failed_on_exception(client, app):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError):
        with run:
            raise ValueError("boom")
    assert app.runs[run.id]["status"] == "failed"


def test_fail_open_spools_on_error_then_flush(app, tmp_path):
    from tests.conftest import make_client

    c = make_client(app, tmp_spool=tmp_path / "spool")
    run = open_run(c, experiment="e", name="r")
    app.fail_next_metrics = True
    # fail-open: the failing metrics call is journaled, does not raise
    run.log({"loss": 1.0}, step=1)
    assert c.journal.pending(), "expected the failed write to be journaled"
    # replay succeeds now
    sent = c.flush()
    assert sent == 1
    assert not c.journal.pending()


def test_strict_write_raises(app, tmp_path):
    from tests.conftest import make_client

    c = make_client(app, fail_open=False, tmp_spool=tmp_path / "spool")
    run = open_run(c, experiment="e", name="r")
    app.fail_next_metrics = True
    with pytest.raises(errors.RosError):
        run.log({"loss": 1.0}, strict=True)


def test_ingest_push(client, app):
    out = client.ingest(
        project_slug="dockq-project",
        experiment_slug="dockq",
        run={"name": "r1", "source": "temporal", "external_id": "wf-1", "status": "running"},
        metrics=[{"kind": "model", "key": "loss", "value": 0.5, "step_index": 1}],
        strict=True,
    )
    assert out["name"] == "r1"
    # HMAC signature attached on the ingest path
    ingest_req = [r for r in app.requests if r.url.path == "/ingest/v1/runs"][0]
    assert json.loads(ingest_req.content)["project_slug"] == "dockq-project"
    assert ingest_req.headers.get("X-Signature", "").startswith("sha256=")
    assert ingest_req.headers["Authorization"] == "Bearer ros_ing_cafef00d"


def test_ingest_requires_project_and_removed_question_keyword(client):
    run = {"name": "r1", "source": "temporal", "external_id": "wf-1"}
    with pytest.raises(TypeError, match="project_slug"):
        client.ingest(experiment_slug="dockq", run=run)
    with pytest.raises(TypeError, match="experiment_question"):
        client.ingest(
            project_slug="dockq-project",
            experiment_slug="dockq",
            experiment_question="removed",
            run=run,
        )


def test_generated_contract_requires_projects_and_removes_ingest_question():
    experiment = ExperimentCreate.model_json_schema()
    ingest = IngestRunRequest.model_json_schema()
    assert "project_id" in experiment["required"]
    assert "project_slug" in ingest["required"]
    assert "experiment_question" not in ingest["properties"]


def test_ingest_validates_client_side(client, app):
    import pytest as _pytest

    # missing run.external_id -> the generated IngestRunRequest rejects it before
    # any HTTP call is made (no request recorded).
    before = len(app.requests)
    with _pytest.raises(Exception):
        client.ingest(
            project_slug="project",
            experiment_slug="e",
            run={"name": "r1", "source": "temporal"},  # no external_id
            strict=True,
        )
    assert len(app.requests) == before, "should fail before sending"


def test_error_mapping_409(app, tmp_path):
    """A taken slug RAISES now. It used to be swallowed: create posted, caught the
    409, and re-fetched the existing row — which is what made a typo silently
    attach to (or mint) the wrong identity instead of failing."""
    from tests.conftest import make_client

    c = make_client(app, tmp_spool=tmp_path / "spool")
    app.experiment_conflict_id = "e-9"
    with pytest.raises(errors.ConflictError) as caught:
        c.create_experiment("dup", "Dup", question="h", project_id="p")
    assert caught.value.existing_id == "e-9"


# -- v0.4 fold-in Phase 1 -----------------------------------------------------
def test_artifact_presign_upload(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    f = tmp_path / "ckpt.bin"
    f.write_bytes(b"weights")
    client.fail_open = False  # strict: real upload path
    result = run.log_artifact("ckpt.bin", path=str(f), strict=True)
    assert result["status"] == "complete"
    # presign -> PUT to r2 -> confirm
    paths = [r.url.path for r in app.requests]
    assert any(p.endswith("/artifacts/uploads") for p in paths)
    assert app.puts, "expected a PUT of the bytes to the presigned URL"
    assert any(p.endswith("/confirm") for p in paths)


def test_artifact_presign_upload_sends_server_signed_headers(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    f = tmp_path / "ckpt.bin"
    f.write_bytes(b"weights")
    app.upload_headers = {"x-amz-checksum-sha256": "checksum"}
    client.fail_open = False

    run.log_artifact("ckpt.bin", path=str(f), strict=True)

    assert app.put_headers[-1]["x-amz-checksum-sha256"] == "checksum"


def test_artifact_reference_still_metadata_only(client, app):
    run = open_run(client, experiment="e", name="r")
    run.log_artifact("final.sif", uri="r2://bucket/final.sif", kind="artifact")
    body = json.loads(app.requests[-1].content)
    assert body["uri"] == "r2://bucket/final.sif"
    assert body["is_reference"] is True


def test_add_edge(client, app):
    client.fail_open = False
    run = open_run(client, experiment="e", name="train")
    other = open_run(client, experiment="e", name="eval")
    client.add_edge(
        source_type="run",
        source_id=run.id,
        relation="evaluates_on",
        target_type="run",
        target_id=other.id,
    )
    edges = run.edges()
    assert edges and edges[0]["relation"] == "evaluates_on"


def test_experiment_version_create_and_list(client, app):
    client.fail_open = False
    project = client.create_project("dockq-project", kind="general")
    exp = client.create_experiment("dockq", "DockQ", question="h", project_id=project["id"])
    v = client.experiment_version(exp["id"], label="launch-1")
    assert v["version"] == 1
    assert client.list_experiment_versions(exp["id"])[0]["label"] == "launch-1"


def test_ingest_execution_record_and_foreign_keys_passthrough(client, app):
    out = client.ingest(
        project_slug="dockq-project",
        experiment_slug="dockq",
        run={
            "name": "r1",
            "source": "temporal",
            "external_id": "wf-1",
            "status": "running",
            "foreign_keys": {"wandb_run_id": "abc"},
        },
        execution_record={"code": {"git": {"commit": "x"}}, "deps": {"py": "3.12"}},
        metrics=[
            {"kind": "hardware", "key": "gpu_temp", "value": 88.0, "dimensions": {"device": 3}}
        ],
        strict=True,
    )
    assert out["name"] == "r1"
    body = json.loads([r for r in app.requests if r.url.path == "/ingest/v1/runs"][-1].content)
    assert body["run"]["foreign_keys"] == {"wandb_run_id": "abc"}
    assert body["execution_record"]["deps"] == {"py": "3.12"}
    assert body["metrics"][0]["dimensions"] == {"device": 3}


def test_run_exposes_slug_and_foreign_keys(client, app):
    run = open_run(client, experiment="e", name="r")
    assert run.slug and run.slug.startswith("run-")
    assert run.foreign_keys == {}


# -- v0.4 fold-in Phase 2 -----------------------------------------------------
def test_snapshot_pins_real_env_ref_column(client, app, tmp_path):
    # snapshot() posts an execution record and pins runs.env_ref via RunPatch
    # (not metadata). Uses a throwaway git repo for the shadow-ref capture.
    import subprocess

    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (["init", "-q"], ["config", "user.email", "t@e.com"], ["config", "user.name", "t"]):
        subprocess.run(["git", *args], cwd=repo, check=True)
    (repo / "a.txt").write_text("x\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=repo, check=True)

    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    snap = run.snapshot(cwd=str(repo), include_env=False, include_gpu=False)
    assert snap["content_hash"]
    assert app.runs[run.id]["env_ref"] == snap["content_hash"]
    assert "env_ref" not in (app.runs[run.id].get("metadata") or {})


def test_snapshot_splits_env_identity_from_provenance(client, app, tmp_path):
    """The hashed execution record gets what the environment IS; the artifact
    meta gets how it was found.

    Both other snapshot tests pass include_env=False, so without this the whole
    environment path through Run.snapshot is unexercised -- `env_provenance`
    could stop reaching the artifact meta entirely and every test would pass.
    """
    import subprocess

    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (["init", "-q"], ["config", "user.email", "t@e.com"], ["config", "user.name", "t"]):
        subprocess.run(["git", *args], cwd=repo, check=True)
    (repo / "a.txt").write_text("x\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=repo, check=True)

    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    snap = run.snapshot(cwd=str(repo), include_env=True, include_gpu=False)

    deps = snap["deps"]
    assert deps["packages"] and deps["package_count"] == len(deps["packages"])
    # identity only -- a path here would change content_hash per machine
    assert not ({"venv", "python_executable", "resolved_via"} & set(deps))

    prov = snap["env_provenance"]
    assert prov["resolved_via"] == "interpreter"
    assert prov["python_executable"] == sys.executable

    # ...and provenance actually reaches the artifact row a reader inspects.
    meta = next(
        a["meta"]
        for rows in app.artifacts.values()
        for a in rows
        if a.get("kind") == "code_snapshot"
    )
    assert meta["env"] == prov


def test_snapshot_rejects_backend_that_drops_env_ref(client, app, tmp_path):
    import subprocess

    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (["init", "-q"], ["config", "user.email", "t@e.com"], ["config", "user.name", "t"]):
        subprocess.run(["git", *args], cwd=repo, check=True)
    (repo / "a.txt").write_text("x\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=repo, check=True)

    original_handler = app.handler

    def drop_env_ref(request):
        response = original_handler(request)
        if request.method == "PATCH" and request.url.path.startswith("/v1/runs/"):
            body = response.json()
            body["env_ref"] = None
            return httpx.Response(response.status_code, json=body)
        return response

    import httpx

    client.transport._client = httpx.Client(
        base_url="http://test", transport=httpx.MockTransport(drop_env_ref)
    )
    client.fail_open = False
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(errors.CapabilityUnavailable, match="run.env_ref"):
        run.snapshot(cwd=str(repo), include_env=False, include_gpu=False, strict=True)


def test_artifact_upload_carries_kind_and_meta(client, app, tmp_path):
    """Harbor-ownership Phase 0: byte uploads are labeled like reference artifacts."""
    run = open_run(client, experiment="e", name="r")
    f = tmp_path / "trial.tar"
    f.write_bytes(b"sandbox-state")
    client.fail_open = False
    result = run.log_artifact(
        "trial-600",
        path=str(f),
        kind="harbor_trial",
        meta={"schema_version": "1.0", "trial": {"name": "swe__x"}},
        step_index=600,
        strict=True,
    )
    assert result["status"] == "complete"
    presign_body = json.loads(
        next(r for r in app.requests if r.url.path.endswith("/artifacts/uploads")).content
    )
    assert presign_body["kind"] == "harbor_trial"
    meta = presign_body["meta"]
    assert {k: meta[k] for k in ("schema_version", "trial")} == {
        "schema_version": "1.0",
        "trial": {"name": "swe__x"},
    }
    assert meta["written_during_run"] is True  # the SDK's write mark rides beside it
    assert presign_body["step_index"] == 600
    stored = client.list_run_artifacts(run.id, kind="harbor_trial")
    # `.tar` from the local path: the upload was named for what it IS, and the
    # extension is restored so the stored name still says what the bytes are.
    assert [a["name"] for a in stored] == ["trial-600.tar"]


def test_artifact_upload_default_kind_stays_file(client, app, tmp_path):
    """A plain upload omits kind (None on the wire) so restages preserve labels."""
    run = open_run(client, experiment="e", name="r")
    f = tmp_path / "ckpt.bin"
    f.write_bytes(b"weights")
    client.fail_open = False
    run.log_artifact("ckpt.bin", path=str(f), strict=True)
    presign_body = json.loads(
        next(r for r in app.requests if r.url.path.endswith("/artifacts/uploads")).content
    )
    assert "kind" not in presign_body  # exclude_none: absent, not "file"
    stored = client.list_run_artifacts(run.id)
    assert stored[0]["kind"] == "file"


def test_artifact_upload_fallback_keeps_kind_and_meta(client, app, tmp_path):
    """Fail-open fallback records the same label, not a bare 'file' reference."""
    run = open_run(client, experiment="e", name="r")
    f = tmp_path / "trial.tar"
    f.write_bytes(b"sandbox-state")
    app.fail_next_uploads = True
    with pytest.warns(UserWarning, match="recorded as a reference"):
        run.log_artifact(
            "trial-601", path=str(f), kind="harbor_trial", meta={"v": 1}, step_index=601
        )
    body = json.loads(app.requests[-1].content)
    assert body["kind"] == "harbor_trial"
    assert body["meta"]["v"] == 1
    assert body["meta"]["upload"] == "failed"
    assert body["is_reference"] is True


def test_list_run_artifacts_filters(client, app):
    """kind + inclusive step-window filters pass through as query params."""
    run = open_run(client, experiment="e", name="r")
    for step in (599, 600, 601):
        run.log_artifact(
            f"sandbox-{step}", uri=f"s3://lake/{step}", kind="sandbox_state", step_index=step
        )
    run.log_artifact("note", uri="s3://lake/note", kind="note")
    window = client.list_run_artifacts(run.id, kind="sandbox_state", step_from=599, step_to=601)
    assert sorted(a["name"] for a in window) == ["sandbox-599", "sandbox-600", "sandbox-601"]
    upper = client.list_run_artifacts(run.id, step_from=601)
    assert [a["name"] for a in upper] == ["sandbox-601"]
    request = app.requests[-1]
    assert request.url.params["step_from"] == "601"
    assert len(client.list_run_artifacts(run.id)) == 4


# -- regressions caught in pre-landing review ---------------------------------
def test_a_span_id_survives_copy_and_pickle(client, app):
    """Span ids were plain str before SpanHandle, and distributed training ships
    them across process boundaries (Ray, multiprocessing, checkpoint state).
    Reconstruction goes through __new__, which needs a live Run, so a handle has
    to degrade to its plain id rather than raise."""
    import copy
    import pickle

    run = open_run(client, experiment="e", name="r")
    span_id = run.span("rollout", name="x")
    assert copy.copy(span_id) == str(span_id)
    assert copy.deepcopy(span_id) == str(span_id)
    assert pickle.loads(pickle.dumps(span_id)) == str(span_id)
    assert type(pickle.loads(pickle.dumps(span_id))) is str


def test_the_two_call_close_does_not_rewrite_the_start_time(client, app):
    """`id=` means upsert, and stamping now() there would move the span's start to
    its close and collapse the duration to zero. Only a CREATE gets a start time;
    the close must send none, leaving the stored one alone."""
    run = open_run(client, experiment="e", name="r")
    span_id = run.span("rollout", name="x")
    assert _last_state(app, run, span_id)["started_at"] is not None, "create must stamp"

    run.span("rollout", id=span_id, status="completed", ended_at="2026-07-27T00:00:09Z")
    closed = _last_state(app, run, span_id)
    assert closed["status"] == "completed"
    assert closed["started_at"] is None, "the close fabricated a new start time"


def test_the_with_form_still_sends_its_real_start_time(client, app):
    """The counterpart: __exit__ re-sends the resolved start explicitly, so
    scoping a span must NOT lose the timestamp the fix stops re-stamping."""
    run = open_run(client, experiment="e", name="r")
    with run.span("rollout", name="x") as span:
        opened = _last_state(app, run, span)["started_at"]
    closed = _last_state(app, run, span)
    assert closed["started_at"] == opened
    assert closed["ended_at"] is not None


def test_a_spooled_metric_write_is_not_reported_as_confirmed(client, app):
    """connectors/harbor.py keys "confirmed" vs "spooled" off this return value,
    so a step record succeeding must not paper over numbers going to the spool."""
    run = open_run(client, experiment="e", name="r")
    app.fail_next_metrics = True
    assert run.log({"loss": 0.4, "phase": "eval"}, step=0) is None


def test_an_empty_log_does_not_burn_a_step(client, app):
    """`if metrics: run.log(metrics)` guards get written the other way round; an
    empty call must not shift the auto axis away from the loop index."""
    run = open_run(client, experiment="e", name="r")
    assert run.log({}) is None
    run.log({"loss": 0.5})
    assert _points(app)[0]["step_index"] == 0


def test_non_numeric_hardware_values_do_not_overwrite_the_model_step(client, app):
    """StepCreate has no `kind` — records are keyed on (run, step_index) alone —
    so a hardware value at hardware-step 0 would land on the model loop's step 0."""
    run = open_run(client, experiment="e", name="r")
    run.log({"loss": 0.5, "phase": "train"})  # model step 0, writes a record
    with pytest.warns(UserWarning, match="step records are keyed by step index"):
        run.log_hw({"driver": "535.x"})  # hardware step 0, must NOT merge
    assert app.steps[run.id][0]["attributes"] == {"phase": "train"}


def test_a_span_does_not_adopt_a_parent_from_a_different_run(client, app):
    """Spans are per-run, so parenting runB's span to runA's would write a
    dangling FK — a worse record than no parent at all."""
    run_a = open_run(client, experiment="e", name="a")
    run_b = open_run(client, experiment="e", name="b")
    with run_a.span("rollout", name="a-rollout"):
        stray = run_b.span("turn", name="b-turn")
    assert _last_state(app, run_b, stray)["parent_span_id"] is None


def test_span_attributes_never_raise_into_the_loop(client, app):
    """`attributes` is JSONB, so an unserialisable value blows up in model_dump()
    BEFORE the strict/spool boundary. In the `with` form the raise happens during
    unwinding and displaces the body's own exception as the visible failure — and
    the README promotes `span.attributes[...] = ...` as the primary idiom."""

    class Opaque:
        pass

    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="not JSON-serialisable"):
        direct = run.span("rollout", attributes={"o": Opaque()})
    assert isinstance(_last_state(app, run, direct)["attributes"]["o"], str)

    with pytest.warns(UserWarning, match="not JSON-serialisable"):
        with run.span("rollout") as scoped:
            scoped.attributes["o"] = Opaque()
    assert isinstance(_last_state(app, run, scoped)["attributes"]["o"], str)


def test_the_body_exception_survives_an_unserialisable_attribute(client, app):
    """The failure the caller needs to see is theirs, not a serialization error
    raised while closing the span on the way out."""
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError, match="rollout diverged"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with run.span("rollout") as scoped:
                scoped.attributes["o"] = object()
                raise ValueError("rollout diverged")
    assert _last_state(app, run, scoped)["status"] == "failed"


# -- external_key is an identity, so it decides the id ------------------------
#
# The server upserts ON CONFLICT (id) but ALSO holds a partial unique index on
# (run_id, span_type, external_key). A client minting a fresh uuid per call made
# the two disagree: `probe span add --external-key k` twice sent a NEW id
# carrying a key the first call had taken, and the write that reads as an upsert
# failed the uniqueness constraint instead -- dead-lettering on the async path.


def test_the_same_external_key_upserts_one_span(client, app):
    run = open_run(client, experiment="e", name="r")

    first = run.span("rollout", external_key="episode-7", name="open")
    second = run.span("rollout", external_key="episode-7", status="completed")

    assert first == second, "a repeat of the same identity minted a second id"
    assert len({s["id"] for s in app.spans[run.id]}) == 1
    assert _last_state(app, run, first)["status"] == "completed"


def test_the_derived_id_is_scoped_to_its_run_and_type(client, app):
    """Same key, different run or different type, is a different span -- exactly
    the shape of the index it is derived to match."""
    one = open_run(client, experiment="e", name="r1")
    two = open_run(client, experiment="e", name="r2")

    assert one.span("rollout", external_key="k") != two.span("rollout", external_key="k")
    assert one.span("rollout", external_key="k") != one.span("eval", external_key="k")


def test_the_derivation_matches_the_servers_normalisation(client, app):
    """The server stores span_type.strip().lower(), so deriving from the raw
    casing would give `LLM` and `llm` two ids for what it stores as one row."""
    run = open_run(client, experiment="e", name="r")
    assert run.span("LLM", external_key="k") == run.span(" llm ", external_key="k")


def test_a_span_without_an_external_key_still_gets_a_fresh_id(client, app):
    """There is no natural key to derive from, so two calls are two spans."""
    run = open_run(client, experiment="e", name="r")
    assert run.span("rollout", name="a") != run.span("rollout", name="b")


def test_an_explicit_id_still_wins(client, app):
    """The documented two-call close passes the id back; derivation must not
    displace it."""
    run = open_run(client, experiment="e", name="r")
    chosen = "11111111-2222-3333-4444-555555555555"
    assert run.span("rollout", id=chosen, external_key="k") == chosen


def test_update_project_parent_wire_shapes(client, app):
    """The one omitted-vs-explicit-null field (0148), pinned ON THE WIRE.

    A future 'cleanup' replacing the _UNSET sentinel with a None default
    would either stop detaches working or start detaching on every unrelated
    PATCH — with every other test still green. The wire body is the contract.
    """
    project = client.create_project("wire-shapes", kind="general")

    client.update_project(project["id"], name="renamed")
    body = json.loads(app.requests[-1].content)
    assert "parent_project_id" not in body  # omitted = untouched

    client.update_project(project["id"], parent_project_id=None)
    body = json.loads(app.requests[-1].content)
    assert body == {"parent_project_id": None}  # explicit null = detach

    client.update_project(project["id"], parent_project_id="p-123")
    body = json.loads(app.requests[-1].content)
    assert body == {"parent_project_id": "p-123"}


def test_delete_project_recursive_rides_the_query_string(client, app):
    project = client.create_project("recursive-delete", kind="general")
    client.delete_project(project["id"])
    assert app.requests[-1].url.params.get("recursive") is None

    project2 = client.create_project("recursive-delete-2", kind="general")
    client.delete_project(project2["id"], recursive=True)
    assert app.requests[-1].url.params.get("recursive") == "true"


def test_browse_forwards_the_level_cursors(client, app):
    """0148: the side-list cursors must reach the wire, or MCP agents can see
    `cursors.runs` in a response and have no way to spend it."""
    app.browse_response = {"experiments": [], "runs": [], "subprojects": []}
    client.browse(scope="project:p-1", runs_cursor="rc", subprojects_cursor="sc")
    params = app.requests[-1].url.params
    assert params.get("runs_cursor") == "rc"
    assert params.get("subprojects_cursor") == "sc"


def test_complete_artifact_reads_cross_the_server_default_cap(client, app):
    """Snapshot/CLI readers must not lose file 1001 when list defaults are capped."""
    from probe.sdk.restore import capture_rows

    run = open_run(client, experiment="e", name="paged-capture")
    app.artifacts[run.id] = [
        {"id": str(i), "name": f"src/{i}.py", "kind": "code", "status": "complete",
         "meta": {"capture": "code-snapshot"}}
        for i in range(2001)
    ]
    rows = capture_rows(client, run.id)
    assert len(rows) == 2001
    assert len({row["id"] for row in rows}) == 2001
    requests = [r for r in app.requests if r.url.path == f"/v1/runs/{run.id}/artifacts"]
    assert [r.url.params.get("offset") for r in requests] == [None, "1000", "2000"]
    assert all(r.url.params["kind"] == "code" for r in requests)


@pytest.mark.parametrize("count", [1000, 2001])
def test_artifact_reads_preserve_legacy_unbounded_inventory(client, count):
    """Older servers accept limit but ignore offset; never send either to them."""
    rows = [{"id": str(i), "kind": "code"} for i in range(count)]
    requests = []

    def legacy(request):
        requests.append(request)
        assert len(requests) == 1, "a legacy inventory is already complete"
        limit = request.url.params.get("limit")
        return httpx.Response(200, json=rows[:int(limit)] if limit else rows)

    with httpx.Client(base_url="http://test", transport=httpx.MockTransport(legacy)) as http:
        client.transport._client = http
        assert client.list_run_artifacts("run", kind="code") == rows
    assert dict(requests[0].url.params) == {"kind": "code"}


@pytest.mark.parametrize("failure", ["repeated_page", "overlapping_page", "missing_header"])
def test_artifact_reads_refuse_unreliable_pagination(client, failure):
    first = [{"id": str(i)} for i in range(1000)]
    requests = []

    def backend(request):
        requests.append(request)
        assert len(requests) <= 2, "an unreliable inventory must not loop"
        headers = {"X-Artifact-Pagination": "offset-v1"}
        if len(requests) == 1:
            return httpx.Response(200, json=first, headers=headers)
        if failure == "missing_header":
            return httpx.Response(200, json=[{"id": "1000"}])
        second = first if failure == "repeated_page" else [{"id": "999"}, {"id": "1000"}]
        return httpx.Response(200, json=second, headers=headers)

    with httpx.Client(base_url="http://test", transport=httpx.MockTransport(backend)) as http:
        client.transport._client = http
        message = "pagination support changed" if failure == "missing_header" else "repeated artifact IDs"
        with pytest.raises(errors.RosError, match=message):
            client.list_run_artifacts("run")
    assert [r.url.params.get("offset") for r in requests] == [None, "1000"]


@pytest.mark.parametrize("params", [{}, {"limit": 2}, {"offset": 1000}, {"limit": 2, "offset": 1000}])
def test_anchored_run_reads_are_complete_unless_explicitly_paged(client, app, params):
    from probe.sdk.client import Anchor

    rows = [{"id": str(i), "kind": "code"} for i in range(2001)]
    app.artifacts["run"] = rows
    actual = client.list_anchored(Anchor.RUN, "run", kind="code", **params)
    requests = [r for r in app.requests if r.url.path == "/v1/runs/run/artifacts"]
    if params:
        offset = params.get("offset", 0)
        assert actual == rows[offset:offset + params.get("limit", 1000)]
        assert len(requests) == 1
        assert dict(requests[0].url.params) == {"kind": "code", **{k: str(v) for k, v in params.items()}}
    else:
        assert actual == rows
        assert [r.url.params.get("offset") for r in requests] == [None, "1000", "2000"]
    assert all(r.url.params["kind"] == "code" for r in requests)


# -- config coercion and updates after init (plan (c)) --------------------------
def _config_patches(app, run):
    return [
        json.loads(r.content)
        for r in app.requests
        if r.method == "PATCH" and r.url.path == f"/v1/runs/{run.id}" and b"config_merge" in r.content
    ]


def test_a_namespace_config_is_stored_as_a_dict_not_its_repr(client, app):
    import argparse

    run = open_run(client, experiment="e", name="r", config=argparse.Namespace(lr=0.1, bs=32))
    assert app.runs[run.id]["config"] == {"lr": 0.1, "bs": 32}


def test_a_dictconfig_config_is_stored_resolved(client, app):
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create({"opt": {"lr": 3e-4, "warmup_lr": "${opt.lr}"}})
    run = open_run(client, experiment="e", name="r", config=cfg)
    assert app.runs[run.id]["config"] == {"opt": {"lr": 3e-4, "warmup_lr": 3e-4}}


def test_update_config_merges_shallow_and_new_wins(client, app):
    run = open_run(client, experiment="e", name="r", config={"lr": 0.1, "opt": {"b": 1}})
    run.update_config({"bs": 64, "opt": {"c": 2}}, allow_val_change=True)
    assert _config_patches(app, run) == [
        {"config_merge": {"bs": 64, "opt": {"c": 2}}}
    ]
    assert app.runs[run.id]["config"] == {"lr": 0.1, "opt": {"c": 2}, "bs": 64}
    assert run.config == app.runs[run.id]["config"]


def test_update_config_coerces_what_it_is_given(client, app):
    import argparse

    np = pytest.importorskip("numpy")
    run = open_run(client, experiment="e", name="r")
    run.update_config(argparse.Namespace(seed=np.int64(7), drop=float("nan")))
    assert app.runs[run.id]["config"] == {"seed": 7, "drop": "NaN"}


def test_a_changed_key_warns_once_per_key_and_the_new_value_wins(client, app):
    run = open_run(client, experiment="e", name="r", config={"lr": 0.1, "bs": 32})
    with pytest.warns(UserWarning, match=r"config 'lr' changed from 0\.1 to 0\.2"):
        run.update_config({"lr": 0.2, "bs": 32})
    with warnings.catch_warnings(record=True) as again:
        warnings.simplefilter("always")
        run.update_config({"lr": 0.3})
    assert not [w for w in again if "changed" in str(w.message)]
    assert app.runs[run.id]["config"]["lr"] == 0.3


def test_allow_val_change_true_is_quiet_and_false_refuses_before_sending(client, app):
    run = open_run(client, experiment="e", name="r", config={"lr": 0.1})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.update_config({"lr": 0.2}, allow_val_change=True)
    assert not [w for w in caught if "changed" in str(w.message)]
    sent = len(app.requests)
    with pytest.raises(errors.ValidationError, match="allow_val_change"):
        run.update_config({"lr": 0.5, "bs": 8}, allow_val_change=False)
    assert len(app.requests) == sent, "nothing sent"
    assert app.runs[run.id]["config"] == {"lr": 0.2}


def test_an_older_server_is_not_sent_a_field_it_would_drop(client, app):
    """RunPatch forbids no extra fields: a server without `run_config_merge`
    answers 200 and drops it. So the SDK does not send it, and says so once."""
    app.supports_config_merge = False
    run = open_run(client, experiment="e", name="r", config={"lr": 0.1})
    with pytest.warns(UserWarning, match="cannot merge a run's config"):
        assert run.update_config({"bs": 64}) is None
    with warnings.catch_warnings(record=True) as again:
        warnings.simplefilter("always")
        run.update_config({"seed": 1})
    assert not [w for w in again if "cannot merge" in str(w.message)], "once per run"
    assert _config_patches(app, run) == []
    with pytest.raises(errors.CapabilityUnavailable):
        run.update_config({"seed": 2}, strict=True)


def test_update_config_is_sent_when_the_server_cannot_be_asked(client, app, monkeypatch):
    run = open_run(client, experiment="e", name="r")

    def unreachable(name):
        raise errors.TransportError("GET /v1/server/features: connection refused")

    monkeypatch.setattr(run._client, "supports_feature", unreachable)
    run.update_config({"bs": 64})
    assert _config_patches(app, run) == [{"config_merge": {"bs": 64}}]


def test_run_config_writes_route_through_update_config(client, app):
    run = open_run(client, experiment="e", name="r", config={"lr": 0.1})
    cfg = run.config
    assert cfg["lr"] == 0.1 and cfg.lr == 0.1
    cfg["bs"] = 64
    cfg.update({"seed": 1}, warmup=10)
    cfg.dropout = 0.2
    assert cfg.setdefault("lr", 9.9) == 0.1
    assert app.runs[run.id]["config"] == {
        "lr": 0.1, "bs": 64, "seed": 1, "warmup": 10, "dropout": 0.2
    }
    assert dict(cfg) == app.runs[run.id]["config"]
    for remove in (lambda: cfg.pop("lr"), lambda: cfg.__delitem__("lr"), cfg.clear):
        with pytest.raises(TypeError, match="cannot be removed"):
            remove()


def test_numpy_values_log_as_numbers_and_arrays_do_not_raise(client, app):
    np = pytest.importorskip("numpy")
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # float(np.array([x])) warns on numpy >= 1.25
        run.log({"a": np.float32(0.5), "b": np.array([1.5]), "c": np.int64(3)}, step=0)
    assert {p["key"]: p["value"] for p in _points(app)} == {"a": 0.5, "b": 1.5, "c": 3.0}
    run.log({"hist": np.zeros(3)}, step=1)  # not a metric: the step record
    assert "hist" in _attrs(app, run, 1)


def test_a_numpy_scalar_in_a_request_body_is_a_number_not_its_repr(client, app):
    np = pytest.importorskip("numpy")
    run = open_run(client, experiment="e", name="r")
    run.step(3, attributes={"score": np.float32(0.5), "n": np.int64(2)})
    assert _attrs(app, run, 3) == {"score": 0.5, "n": 2}


# -- #2032 review ---------------------------------------------------------------
_RAW = "raw-" + "c0ffee1234567890deadbeef"


def test_update_config_never_prints_or_misjudges_a_credential(client, app, capsys):
    """The stored config is scrubbed, so the RAW new value under a credential
    key always looked "changed", and the warning printed it -- into stderr,
    which the run log uploads. Compare and print only what goes on the wire."""
    run = open_run(client, experiment="e", name="r", config={"api_key": _RAW, "lr": 0.1})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.update_config({"api_key": _RAW})
        run.update_config({"api_key": _RAW}, allow_val_change=False)  # a repeat, not a change
        run.update_config({"lr": 0.2, "api_key": "another-" + _RAW})
    said = " ".join(str(w.message) for w in caught)
    assert _RAW not in said and _RAW not in capsys.readouterr().err
    assert "'lr' changed" in said and "'api_key' changed" not in said
    assert _RAW not in _wire(app)
    assert app.runs[run.id]["config"] == {"api_key": "<redacted>", "lr": 0.2}
    assert _RAW not in json.dumps(dict(run.config))


def test_run_config_update_takes_a_namespace(client, app):
    import argparse

    run = open_run(client, experiment="e", name="r")
    run.config.update(argparse.Namespace(lr=0.1, bs=32))
    run.config.update([("seed", 1)], warmup=5)
    assert app.runs[run.id]["config"] == {"lr": 0.1, "bs": 32, "seed": 1, "warmup": 5}


def test_a_namespace_subclass_or_simplenamespace_is_a_config(client, app):
    import argparse
    import types

    class JsonargparseNamespace(argparse.Namespace):  # what LightningCLI hands out
        pass

    run = open_run(client, experiment="e", name="r", config=JsonargparseNamespace(lr=0.1))
    assert app.runs[run.id]["config"] == {"lr": 0.1}
    run.update_config(types.SimpleNamespace(bs=64))
    assert app.runs[run.id]["config"] == {"lr": 0.1, "bs": 64}


def test_copies_of_run_config_are_plain_snapshots_and_send_nothing(client, app):
    import copy
    import pickle

    run = open_run(client, experiment="e", name="r", config={"lr": 0.1})
    sent = len(app.requests)
    for clone in (copy.copy(run.config), copy.deepcopy(run.config), pickle.loads(pickle.dumps(run.config))):
        assert type(clone) is dict and clone == {"lr": 0.1}
        clone["lr"] = 9.9
    assert len(app.requests) == sent and app.runs[run.id]["config"] == {"lr": 0.1}


def test_in_place_or_on_run_config_sends(client, app):
    run = open_run(client, experiment="e", name="r", config={"lr": 0.1})
    cfg = run.config
    cfg |= {"bs": 64}
    assert app.runs[run.id]["config"] == {"lr": 0.1, "bs": 64}
    assert cfg["bs"] == 64


def test_a_config_interpolation_that_would_reveal_a_secret_is_stored_unresolved(client, app, monkeypatch):
    """DECIDED (#2032 review): security over W&B parity. `${oc.env:...}` and
    references to credential-shaped paths stay their `${...}` text; the rest
    resolve."""
    omegaconf = pytest.importorskip("omegaconf")
    monkeypatch.setenv("SERVICE_KEY", _RAW)
    cfg = omegaconf.OmegaConf.create(
        {
            "wandb": {"api_key": _RAW},
            "client": {"auth": "${wandb.api_key}", "key": "${oc.env:SERVICE_KEY}"},
            "opt": {"lr": 0.1, "warmup_lr": "${opt.lr}"},
        }
    )
    run = open_run(client, experiment="e", name="r", config=cfg)
    stored = app.runs[run.id]["config"]
    assert _RAW not in json.dumps(stored) and _RAW not in _wire(app)
    assert stored["client"] == {"auth": "${wandb.api_key}", "key": "${oc.env:SERVICE_KEY}"}
    assert stored["opt"] == {"lr": 0.1, "warmup_lr": 0.1}


def test_a_config_alias_to_a_whole_credential_group_is_stored_unresolved(client, app, capfd):
    """`auth: ${alias}` with `alias: ${credentials}` resolves to the whole
    credentials NODE. Stored, that put the secret in the run's config under
    `auth.x`; through update_config, the "config 'client' changed from ... to
    ..." warning printed it too (#2032 review 2)."""
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create({"credentials": {"x": _SECRET}, "alias": "${credentials}", "auth": "${alias}"})
    first = open_run(client, experiment="e", name="r1", config=cfg)
    run = open_run(client, experiment="e", name="r2", config={"client": {"auth": "old"}})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.update_config({"client": cfg})
    said = " ".join(str(w.message) for w in caught)
    assert "'client' changed" in said and _SECRET not in said
    assert _SECRET not in capfd.readouterr().err
    assert _SECRET not in _wire(app)
    assert app.runs[first.id]["config"]["auth"] == "${alias}"
    assert app.runs[run.id]["config"]["client"]["auth"] == "${alias}"
