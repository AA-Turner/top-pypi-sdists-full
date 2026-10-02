"""`probe.expect()` / `run.expect()` / `probe run expect`: declared metric ranges.

The promise under test: it is an ADD-ON. A script that never calls it is
unchanged, and a call can never break the script -- a malformed entry is dropped
with a warning and delivery is fail-open. What the server does with the ranges
(merge, stamp, alert) is proven against real tables in
`tests/integration/test_metric_ranges.py`; here, the wire body and the refusals.
"""

from __future__ import annotations

import json
import warnings

import httpx
import pytest

import probe
from probe.sdk import fluent
from probe.sdk.expectations import MAX_PER_CALL, normalize
from tests.conftest import make_client, open_run


def _patches(app) -> list[dict]:
    return [
        json.loads(r.content)
        for r in app.requests
        if r.method == "PATCH" and b"metric_expectations" in r.content
    ]


# -- normalize -----------------------------------------------------------------------


def test_normalize_accepts_tuples_dicts_and_removal() -> None:
    wire, problems = normalize(
        {"val/acc": (0.5, 1), "loss": [None, 20.0], "lr": {"max": 0.1}, "gone": None}
    )
    assert problems == []
    assert wire == {
        "val/acc": {"min": 0.5, "max": 1.0},
        "loss": {"min": None, "max": 20.0},
        "lr": {"min": None, "max": 0.1},
        "gone": None,
    }


@pytest.mark.parametrize(
    "spec",
    [
        (None, None),
        (2, 1),
        (float("nan"), 1),
        (0, float("inf")),
        (True, 1),
        ("0.5", 1),
        "0.5",
        (1, 2, 3),
        {"lo": 1},
    ],
)
def test_normalize_drops_a_bad_entry_and_says_why(spec) -> None:
    wire, problems = normalize({"bad": spec, "good": (0, 1)})
    assert wire == {"good": {"min": 0.0, "max": 1.0}}
    assert len(problems) == 1 and "'bad'" in problems[0]


def test_normalize_takes_numpy_style_scalars() -> None:
    class Scalar:  # quacks like np.float32: float() works, isinstance does not
        def __float__(self) -> float:
            return 0.25

    wire, problems = normalize({"k": (Scalar(), None)})
    assert problems == [] and wire == {"k": {"min": 0.25, "max": None}}


def test_normalize_never_raises_on_garbage() -> None:
    assert normalize("val/acc")[0] == {}
    assert normalize({"": (0, 1), 5: (0, 1)})[0] == {}
    wire, problems = normalize({f"k{i}": (0, 1) for i in range(MAX_PER_CALL + 5)})
    assert len(wire) == MAX_PER_CALL and problems


# -- Run.expect ---------------------------------------------------------------------------


def test_expect_sends_one_patch_with_the_ranges(client, app) -> None:
    run = open_run(client, experiment="e", name="r")
    run.expect({"val/acc": (0.5, 1.0), "loss": (None, 20)})
    (body,) = _patches(app)
    assert body == {
        "metric_expectations": {
            "val/acc": {"min": 0.5, "max": 1.0},
            "loss": {"min": None, "max": 20.0},
        }
    }


def test_expect_drops_a_bad_entry_with_a_warning_and_sends_the_rest(client, app) -> None:
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning, match="probe.expect: dropped 'oops'"):
        run.expect({"oops": (3, 1), "val/acc": (0.5, None)})
    (body,) = _patches(app)
    assert body == {"metric_expectations": {"val/acc": {"min": 0.5, "max": None}}}


def test_expect_with_nothing_valid_sends_nothing(client, app) -> None:
    run = open_run(client, experiment="e", name="r")
    with pytest.warns(UserWarning):
        assert run.expect({"oops": "x"}) is None
    assert _patches(app) == []


def test_expect_never_raises_into_the_script(app, tmp_path) -> None:
    """The server is down, or rejects the body: a training script must not die
    for an optional alert. Only strict=True (the CLI) raises."""
    client = make_client(app, tmp_spool=tmp_path / "spool")
    run = open_run(client, experiment="e", name="r")

    def boom(*_a, **_kw):
        raise httpx.ConnectError("down")

    run._client.write = boom
    with pytest.warns(UserWarning, match="not recorded"):
        assert run.expect({"val/acc": (0.5, 1)}) is None
    with pytest.raises(httpx.ConnectError):
        run.expect({"val/acc": (0.5, 1)}, strict=True)


# -- probe.expect (fluent) -------------------------------------------------------------------


@pytest.fixture
def _clean_binding():
    fluent._current.set(None)
    fluent._process_default = None
    yield
    fluent._current.set(None)
    fluent._process_default = None


def test_fluent_expect_without_a_run_warns_and_does_nothing(_clean_binding) -> None:
    with pytest.warns(UserWarning, match="no active run"):
        assert probe.expect({"val/acc": (0.5, 1)}) is None


def test_fluent_expect_on_the_active_run(app, tmp_path, monkeypatch, _clean_binding) -> None:
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "s"))
    app.seed_experiment("e1")
    run = probe.init(experiment="e1", name="r1")
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # a valid call warns about nothing
        probe.expect({"val/acc": (0.5, 1.0)})
    probe.finish()
    (body,) = _patches(app)
    assert body["metric_expectations"] == {"val/acc": {"min": 0.5, "max": 1.0}}
    assert probe.expect is not None and run is not None


# -- probe run expect (CLI) --------------------------------------------------------------------


def _cli_main(app, tmp_path, monkeypatch):
    """The CLI module with `_client` wired to the fake. The CLI owns and closes
    its client, so each command gets a fresh one."""
    import importlib

    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(cli_main, "_client", lambda: make_client(app, tmp_spool=tmp_path / "cli"))
    return cli_main


def test_cli_declares_a_range_on_a_running_run(client, app, tmp_path, monkeypatch, capsys) -> None:
    run = open_run(client, experiment="e", name="r")
    cli_main = _cli_main(app, tmp_path, monkeypatch)
    cli_main.run_expect(run.id, "val/acc", minimum=0.5, maximum=1.0, clear=False)
    assert json.loads(capsys.readouterr().out)["min"] == 0.5
    assert _patches(app)[-1] == {"metric_expectations": {"val/acc": {"min": 0.5, "max": 1.0}}}


def test_cli_clear_removes_the_range(client, app, tmp_path, monkeypatch, capsys) -> None:
    run = open_run(client, experiment="e", name="r")
    cli_main = _cli_main(app, tmp_path, monkeypatch)
    cli_main.run_expect(run.id, "val/acc", minimum=None, maximum=None, clear=True)
    assert json.loads(capsys.readouterr().out)["removed"] is True
    assert _patches(app)[-1] == {"metric_expectations": {"val/acc": None}}


@pytest.mark.parametrize(
    ("minimum", "maximum", "clear"),
    [(None, None, False), (1.0, None, True), (2.0, 1.0, False)],
)
def test_cli_refuses_an_incomplete_or_backwards_range(
    client, app, tmp_path, monkeypatch, minimum, maximum, clear
) -> None:
    import typer

    run = open_run(client, experiment="e", name="r")
    cli_main = _cli_main(app, tmp_path, monkeypatch)
    with pytest.raises(typer.BadParameter):
        cli_main.run_expect(run.id, "val/acc", minimum=minimum, maximum=maximum, clear=clear)
    assert _patches(app) == []


def test_expect_never_raises_even_under_warnings_as_errors(client, app) -> None:
    """Several ML harnesses run with `-W error`: a plain `warnings.warn` would
    RAISE inside the script. The add-on warns through the SDK's non-raising
    channel instead."""
    run = open_run(client, experiment="e", name="r")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert run.expect({"oops": (3, 1)}) is None
        run.expect({"oops": (3, 1), "val/acc": (0.5, 1.0)})
    assert _patches(app)[-1] == {"metric_expectations": {"val/acc": {"min": 0.5, "max": 1.0}}}


def test_fluent_expect_without_a_run_never_raises_under_warnings_as_errors(_clean_binding) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert probe.expect({"val/acc": (0.5, 1)}) is None


def test_strict_refuses_a_range_it_cannot_record(client, app) -> None:
    """The CLI asked: dropping the range and exiting 0 would print a range
    that was never set."""
    run = open_run(client, experiment="e", name="r")
    with pytest.raises(ValueError, match="'oops'"):
        run.expect({"oops": (float("nan"), 1)}, strict=True)
    assert _patches(app) == []


def test_cli_refuses_a_nan_bound(client, app, tmp_path, monkeypatch) -> None:
    import typer

    run = open_run(client, experiment="e", name="r")
    cli_main = _cli_main(app, tmp_path, monkeypatch)
    with pytest.raises(typer.BadParameter, match="finite"):
        cli_main.run_expect(run.id, "val/acc", minimum=float("nan"), maximum=None, clear=False)
