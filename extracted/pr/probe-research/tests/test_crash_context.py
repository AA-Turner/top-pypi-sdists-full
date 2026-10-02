"""Keep the failing unit during unwinding without retaining a prompt or tensor."""

import asyncio
import json
import threading

import pytest

from probe.sdk import diagnostics, failure_context
from probe.sdk.unit_context import FailureContext, UnitContext, current, failure_values
from tests.conftest import make_client, open_run


def test_nested_units_keep_the_inner_sample_after_unwinding(client):
    run = open_run(client, experiment="e", name="r")
    try:
        with run.unit(labels={"sample_id": "outer", "prompt": "PRIVATE"}):
            with run.unit(
                coords={"split": "validation"}, labels={"sample_id": 17, "prompt_id": "p17"}
            ):
                raise ValueError("bad input")
    except ValueError as exc:
        report = diagnostics.build_report(exc, run_id=run.id)
    assert current() == ({}, {})
    assert report["context"]["sample_id"] == "17"
    assert report["context"]["prompt_id"] == "p17"
    assert report["context"]["split"] == "validation"
    assert "PRIVATE" not in json.dumps(report)


def test_exception_context_is_scoped_to_its_run(client):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError) as caught:
        with run.unit(labels={"sample_id": "own-sample"}):
            raise ValueError("bad")
    report = diagnostics.build_report(caught.value, run_id="different-run")
    assert "context" not in report


def test_failed_span_captures_exact_step_and_identifier_before_reset(client):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError) as caught:
        with run.span(
            "step",
            step_index=42,
            name="parse prompt",
            attributes={"dataset": "eval-v2", "sample_id": "row42", "prompt": "PRIVATE"},
        ):
            raise ValueError("bad format")
    report = diagnostics.build_report(caught.value, run_id=run.id)
    assert report["context"]["step"] == 42
    assert report["context"]["sample_id"] == "row42"
    assert report["context"]["phase"] == "parse prompt"
    assert "PRIVATE" not in json.dumps(report)


def test_context_survives_raise_from_and_stays_bounded(client):
    run = open_run(client, experiment="e", name="r")
    try:
        try:
            with run.unit(labels={"sample_id": "x" * 5000}):
                raise ValueError("bad")
        except ValueError as cause:
            raise RuntimeError("parser failed") from cause
    except RuntimeError as exc:
        report = diagnostics.build_report(exc, run_id=run.id)
    assert len(report["context"]["sample_id"]) <= 160
    assert len(json.dumps(report).encode()) <= diagnostics.MAX_REPORT_BYTES


def test_capture_cannot_replace_original_exception(client):
    class SealedError(Exception):
        def __setattr__(self, name, value):
            raise RuntimeError("sealed")

    run = open_run(client, experiment="e", name="r")
    with pytest.raises(SealedError):
        with run.unit(labels={"sample_id": "sample"}):
            raise SealedError("original")


def test_plain_unit_without_run_does_not_attach_context():
    with pytest.raises(ValueError) as caught:
        with UnitContext(labels={"sample_id": "unowned"}):
            raise ValueError("bad")
    assert "context" not in diagnostics.build_report(caught.value, run_id="r")


def test_nested_runs_do_not_inherit_failure_identifiers(client):
    first = open_run(client, experiment="e", name="first")
    second = open_run(client, experiment="e", name="second")
    with pytest.raises(ValueError) as caught:
        with first.unit(labels={"sample_id": "first-private"}):
            with second.unit(coords={"split": "eval"}):
                raise ValueError("second failed")
    context = diagnostics.build_report(caught.value, run_id=second.id)["context"]
    assert context["split"] == "eval"
    assert "sample_id" not in context


def test_span_uses_own_coords_and_not_another_runs_unit(client):
    first = open_run(client, experiment="e", name="first")
    second = open_run(client, experiment="e", name="second")
    with pytest.raises(ValueError) as caught:
        with first.unit(coords={"dataset": "wrong"}, labels={"sample_id": "first-private"}):
            with second.span("step", coords={"dataset": "actual", "split": "test"}):
                raise ValueError("second failed")
    context = diagnostics.build_report(caught.value, run_id=second.id)["context"]
    assert context["dataset"] == "actual"
    assert context["split"] == "test"
    assert "sample_id" not in context


def test_report_interruption_preserves_body_error_and_still_closes(client, monkeypatch):
    run = open_run(client, experiment="e", name="r")
    closed = []

    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt()

    monkeypatch.setattr(diagnostics, "report_exception", interrupt)
    monkeypatch.setattr(run, "finish", closed.append)
    with pytest.raises(ValueError, match="original"):
        with run:
            raise ValueError("original")
    assert closed == ["failed"]


def test_forged_exception_context_is_allowlisted():
    exc = ValueError("bad")
    exc._probe_failure_context = {"run_id": "r", "sample_id": "x" * 1000, "prompt": "PRIVATE"}
    context = diagnostics.build_report(exc, run_id="r")["context"]
    assert "prompt" not in context
    assert len(context["sample_id"]) <= 160


def test_inner_scope_alias_overrides_outer_identifier(client):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError) as caught:
        with run.unit(labels={"sample_id": "outer"}):
            with run.unit(labels={"sample": "inner"}):
                raise ValueError("bad")
    assert diagnostics.build_report(caught.value, run_id=run.id)["context"]["sample_id"] == "inner"


# -- run.context(...): failure-only, never on the wire -------------------------
def _metric_bodies(app, run_id: str) -> list[dict]:
    """The raw JSON bodies the real Transport POSTed to this run's metrics route."""
    return [
        json.loads(r.content)
        for r in app.requests
        if r.method == "POST" and r.url.path == f"/v1/runs/{run_id}/metrics"
    ]


@pytest.mark.parametrize("async_writes", [False, True], ids=["sync", "outbox"])
def test_metrics_inside_a_context_are_sent_exactly_as_outside(app, tmp_path, async_writes):
    """THE regression this surface exists to avoid: `run.unit(labels=...)` would
    stamp the batch id onto every point (labeled points never plot) and a
    per-batch coord shreds the series. The block must change NOTHING on the wire
    -- asserted on the request bodies the SDK really sent, on both the direct
    path and the outbox path production defaults to."""
    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=async_writes)
    run = open_run(client, experiment="e", name="r")
    # Markers with non-hex letters: a random uuid in the body can never contain them.
    with run.context(batch_id="batch-seven", epoch=3, sample_id="sample-nine", step=1):
        run.log({"loss": 0.5}, step=1)
        run.span("rollout", name="rollout-0")
    run.log({"loss": 0.5}, step=2)
    run.span("rollout", name="rollout-1")
    client.flush()

    inside, outside = _metric_bodies(app, run.id)
    (point,) = inside["points"]
    assert point["dimensions"] == {}
    assert "labels" not in point  # absent, exactly as a unit-less point serializes
    outside["points"][0]["step_index"] = 1
    # Plan 1.4: each call is dated at call time, so the two stamps differ by
    # the clock alone -- the block itself must add or change nothing else.
    assert inside["points"][0]["wall_clock"] and outside["points"][0]["wall_clock"]
    outside["points"][0]["wall_clock"] = inside["points"][0]["wall_clock"]
    assert inside == outside
    wire = json.dumps(inside)
    assert "batch-seven" not in wire and "sample-nine" not in wire

    span_in, span_out = app.spans[run.id]
    assert span_in["coords"] == span_out["coords"] == {}
    assert span_in["attributes"] == span_out["attributes"] == {}
    client.close()


def test_context_leaves_the_unit_maps_alone_and_composes_with_a_unit(client, app):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError) as caught:
        with run.unit(coords={"split": "eval"}):
            with run.context(batch_id="b7", epoch=3):
                assert current() == ({"split": "eval"}, {})
                run.log({"loss": 1.0}, step=4)
                raise ValueError("bad batch")
    (point,) = app.metric_points_posted[run.id]
    assert point["dimensions"] == {"split": "eval"}  # the unit's, and only the unit's
    assert "labels" not in point
    context = diagnostics.build_report(caught.value, run_id=run.id)["context"]
    assert context == {"run_id": run.id, "split": "eval", "batch_id": "b7", "epoch": "3"}


def test_an_exception_inside_a_context_names_the_batch_and_epoch(client):
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(RuntimeError) as caught:
        with run.context(batch_id="b7", epoch=3):
            raise RuntimeError("CUDA error: an illegal memory access was encountered")
    report = diagnostics.build_report(caught.value, run_id=run.id)
    assert report["context"] == {"run_id": run.id, "batch_id": "b7", "epoch": "3"}
    assert failure_values(run.id) == {}  # restored on the way out


def test_nested_contexts_merge_inner_wins_and_exit_restores(client):
    run = open_run(client, experiment="e", name="r")
    with run.context(batch_id="outer", epoch=1):
        with run.context(batch_id="inner", sample_id=17):
            assert failure_values(run.id) == {"batch_id": "inner", "epoch": "1", "sample_id": "17"}
        assert failure_values(run.id) == {"batch_id": "outer", "epoch": "1"}
        with pytest.raises(ValueError) as caught:
            with run.context(sample_id="s-2"):
                raise ValueError("bad")
    assert failure_values(run.id) == {}
    context = diagnostics.build_report(caught.value, run_id=run.id)["context"]
    assert context == {"run_id": run.id, "batch_id": "outer", "epoch": "1", "sample_id": "s-2"}


def test_a_handled_exception_leaves_nothing_for_the_next_one(client):
    run = open_run(client, experiment="e", name="r")
    try:
        with run.context(batch_id="b1"):
            raise ValueError("retried")
    except ValueError:
        pass
    with pytest.raises(ValueError) as caught:
        raise ValueError("later, outside any context")
    assert "context" not in diagnostics.build_report(caught.value, run_id=run.id)


def test_bad_values_are_dropped_and_nothing_raises(client):
    class Hostile(str):
        def __str__(self):
            raise RuntimeError("hostile __str__")

        def split(self, *a, **kw):
            raise RuntimeError("hostile split")

    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError, match="the body's own error") as caught:
        with run.context(
            batch_id=object(),
            epoch=1.5,  # floats are not identifiers; pass the loop's int
            sample_id=["x"],
            task_id=True,
            prompt_id="p\x00",
            step=-1,
            unknown_key="ignored",
            model="qwen-7b",
        ):
            raise ValueError("the body's own error")
    assert diagnostics.build_report(caught.value, run_id=run.id)["context"] == {
        "run_id": run.id,
        "model": "qwen-7b",
    }
    with run.context(batch_id=Hostile("b")):  # identifiers() swallows, the loop goes on
        pass
    with run.context():
        pass
    assert failure_values(run.id) == {}


def test_a_context_without_a_run_is_a_no_op():
    with pytest.raises(ValueError) as caught:
        with FailureContext(None, {"batch_id": "b7"}):
            assert failure_values(None) == {}
            raise ValueError("bad")
    assert not hasattr(caught.value, "_probe_failure_context")


def test_a_context_never_suppresses_the_exception(client):
    run = open_run(client, experiment="e", name="r")
    ctx = run.context(batch_id="b")
    ctx.__enter__()
    assert ctx.__exit__(ValueError, ValueError("x"), None) is None


def test_a_context_is_scoped_to_its_run(client):
    first = open_run(client, experiment="e", name="first")
    second = open_run(client, experiment="e", name="second")
    with pytest.raises(ValueError) as caught:
        with first.context(batch_id="first-batch"):
            with second.context(epoch=2):
                raise ValueError("second failed")
    assert diagnostics.build_report(caught.value, run_id=second.id)["context"] == {
        "run_id": second.id,
        "epoch": "2",
    }


def test_contexts_are_isolated_across_threads_and_asyncio_tasks(client):
    run = open_run(client, experiment="e", name="r")
    seen: dict = {}
    with run.context(batch_id="main"):
        thread = threading.Thread(target=lambda: seen.update(thread=failure_values(run.id)))
        thread.start()
        thread.join()
    assert seen["thread"] == {}  # a fresh thread starts with no context

    async def worker(batch: int, out: dict) -> None:
        with run.context(batch_id=batch):
            await asyncio.sleep(0)  # yield so the tasks interleave
            out[batch] = failure_values(run.id)["batch_id"]

    async def main() -> dict:
        out: dict = {}
        await asyncio.gather(worker(0, out), worker(1, out))
        return out

    assert asyncio.run(main()) == {0: "0", 1: "1"}


def test_epoch_is_an_identifier_and_never_the_step():
    assert failure_context.identifiers({"epoch": 3, "step": 5}) == {"epoch": "3", "step": 5}
    assert failure_context.identifiers({"epoch": "warmup"}) == {"epoch": "warmup"}
    assert failure_context.identifiers({"epoch": True}) == {}
    assert "step" not in failure_context.identifiers({"epoch": 7})


def test_a_whole_float_epoch_is_kept_and_a_fraction_is_not():
    """Hugging Face's `state.epoch` is a float: 2.0 at a boundary is epoch 2;
    2.37 is a position inside one, not an epoch name."""
    assert failure_context.identifiers({"epoch": 2.0}) == {"epoch": "2"}
    assert failure_context.identifiers({"epoch": 2.37}) == {}
