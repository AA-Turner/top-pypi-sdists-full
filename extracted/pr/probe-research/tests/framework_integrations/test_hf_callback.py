"""ProbeCallback through a REAL Hugging Face `Trainer.train` (plan (b), task T28).

A 2-layer BERT built from a config in the test (no download), 16 samples in
batches of 4: four optimizer steps, evaluated and saved every 2. The
single-process tests drive the real Trainer against the in-process fake API;
the exit-verdict tests and the two-rank test run a real child process
(`torchrun` over gloo for the ranks) against the same fake served on a
loopback socket.

Skipped when `transformers` is not installed (the default agent-ci job). The
integrations job sets PROBE_REQUIRE_INTEGRATIONS=1, which turns a missing
install into a failure instead of a green skip.

Checkpoint rows are read through `_stored_checkpoints`, which folds the POSTs
the way the server stores them: a hashless path reference is keyed on (run,
name, uri) and refreshed IN PLACE by a re-log (`app/artifacts/service.py`).
The fake only appends.
"""

from __future__ import annotations

import dataclasses
import json
import os
import pickle
import signal
import socket
import subprocess
import sys
import textwrap
import time
import warnings

import pytest

if os.environ.get("PROBE_REQUIRE_INTEGRATIONS") == "1":
    import transformers  # noqa: F401 -- an ImportError here fails the job
else:
    pytest.importorskip("transformers")
    pytest.importorskip("accelerate")  # the Trainer needs it

import torch  # noqa: E402
from transformers import (  # noqa: E402
    BertConfig,
    BertForSequenceClassification,
    Trainer,
    TrainerCallback,
    TrainingArguments,
)
from transformers.integrations import integration_utils  # noqa: E402

import probe  # noqa: E402
import probe.integrations.huggingface as hf  # noqa: E402
from probe.integrations.huggingface import ProbeCallback  # noqa: E402
from probe.sdk import fluent  # noqa: E402
from tests.conftest import make_client  # noqa: E402
from tests.served_fake_app import child_env, serve  # noqa: E402

HUB_TOKEN = "hf_NotARealTokenButLongEnough1234567"


class _Data(torch.utils.data.Dataset):
    def __init__(self, n: int) -> None:
        generator = torch.Generator().manual_seed(0)
        self.x = torch.randint(0, 32, (n, 6), generator=generator)
        self.y = torch.randint(0, 2, (n,), generator=generator)

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, i: int) -> dict:
        return {"input_ids": self.x[i], "labels": self.y[i]}


class _Other(_Data):
    """A second eval set: other rows, so another loss."""

    def __init__(self, n: int) -> None:
        generator = torch.Generator().manual_seed(7)
        self.x = torch.randint(0, 32, (n, 6), generator=generator)
        self.y = torch.randint(0, 2, (n,), generator=generator)


def _model() -> BertForSequenceClassification:
    torch.manual_seed(0)
    return BertForSequenceClassification(
        BertConfig(
            vocab_size=32,
            hidden_size=8,
            num_hidden_layers=2,
            num_attention_heads=2,
            intermediate_size=16,
            max_position_embeddings=16,
        )
    )


def _args(tmp_path, **kw) -> TrainingArguments:
    settings = dict(
        output_dir=str(tmp_path / "out"),
        max_steps=4,
        per_device_train_batch_size=4,
        logging_steps=1,
        eval_strategy="steps",
        eval_steps=2,
        save_steps=2,
        report_to="none",
        use_cpu=True,
        disable_tqdm=True,
        seed=0,
        learning_rate=0.01,
        hub_token=HUB_TOKEN,
    )
    settings.update(kw)
    return TrainingArguments(**settings)


def _trainer(tmp_path, *, callbacks=None, model=None, compute_metrics=None, **kw) -> Trainer:
    return Trainer(
        model=model or _model(),
        args=_args(tmp_path, **kw),
        train_dataset=_Data(16),
        eval_dataset=_Data(8),
        callbacks=callbacks,
        compute_metrics=compute_metrics,
    )


class _RaiseAt(TrainerCallback):
    """Raise inside the training loop, the way a bad batch would."""

    def __init__(self, step: int, exc: BaseException) -> None:
        self.step, self.exc = step, exc

    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step == self.step:
            raise self.exc


@pytest.fixture(autouse=True)
def _clean_binding():
    """fluent keeps process state on purpose; tests must not inherit it."""

    def reset():
        hf._CALLBACK_RUNS.clear()
        hf._LAUNCHER_RUNS.clear()
        hf._ADOPTED.clear()
        hf._UNFINISHED.clear()
        hf._SIGNALS_SEEN.clear()
        fluent._current.set(None)
        fluent._process_default = None
        fluent._exit_status = "completed"
        fluent._exit_recorded = False
        fluent._exit_exception = None
        fluent._exit_code = None
        fluent._exit_via = None

    reset()
    yield
    reset()


@pytest.fixture(autouse=True)
def _keep_signals():
    """A train() that raised leaves the chained notes in place (on_train_end
    never ran): give the suite its own handlers back."""
    before = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    yield
    for signum, handler in before.items():
        signal.signal(signum, handler)


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    """A bare `probe.init()` builds a client wired to the fake: the path the
    callback takes in real use."""
    monkeypatch.setattr(
        fluent, "Client", lambda *a, **kw: make_client(app, tmp_spool=tmp_path / "spool")
    )
    app.seed_experiment("e1")


def _points(app, run_id: str, key: str) -> list[int]:
    return sorted(
        p["step_index"] for p in app.metric_points_posted.get(run_id, []) if p["key"] == key
    )


def _only_run(app) -> dict:
    (row,) = app.runs.values()
    return row


def _checkpoint_posts(app, run_id: str) -> list[dict]:
    return [a for a in app.artifacts.get(run_id, []) if a.get("kind") == "checkpoint"]


def _stored_checkpoints(app, run_id: str) -> dict[str, dict]:
    """What the server holds per checkpoint folder (see the module docstring)."""
    stored: dict[tuple[str, str], dict] = {}
    for post in _checkpoint_posts(app, run_id):
        key = (post["name"], post["uri"])
        first = stored.get(key)
        stored[key] = {
            **post,
            "step_index": first["step_index"] if first else post.get("step_index"),
        }
    return {row["name"]: row for row in stored.values()}


def _folder_bytes(root: str) -> int:
    return sum(
        os.path.getsize(os.path.join(dirpath, f))
        for dirpath, _, files in os.walk(root)
        for f in files
    )


def _probe_warnings(caught) -> list[str]:
    return [str(w.message) for w in caught if str(w.message).startswith("probe:")]


# -- report_to="probe" ---------------------------------------------------------------

_REGISTRY_SCRIPT = textwrap.dedent(
    """
    import json, sys
    from transformers import BertConfig, BertForSequenceClassification, Trainer, TrainingArguments
    model = BertForSequenceClassification(BertConfig(
        vocab_size=32, hidden_size=8, num_hidden_layers=1, num_attention_heads=2,
        intermediate_size=16, max_position_embeddings=16))
    args = TrainingArguments(output_dir=sys.argv[1], report_to="probe", use_cpu=True)
    out = {}
    try:
        Trainer(model=model, args=args)
        out["before"] = "built"
    except ValueError as exc:
        out["before"] = "ValueError: " + str(exc)[:80]
    import probe.integrations.huggingface as hf
    from transformers.integrations import integration_utils
    out["registered"] = integration_utils.INTEGRATION_TO_CALLBACK.get("probe") is hf.ProbeCallback
    trainer = Trainer(model=model, args=args)
    out["callbacks"] = [type(c).__name__ for c in trainer.callback_handler.callbacks]
    print(json.dumps(out))
    """
)


def test_report_to_probe_resolves_only_after_the_import(tmp_path):
    """A fresh interpreter: without the import, report_to="probe" is an
    unknown integration (the negative control); after it, the Trainer builds
    a ProbeCallback."""
    script = tmp_path / "registry.py"
    script.write_text(_REGISTRY_SCRIPT)
    done = subprocess.run(
        [sys.executable, str(script), str(tmp_path / "out")],
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert done.returncode == 0, done.stderr[-3000:]
    out = json.loads(done.stdout.strip().splitlines()[-1])
    assert out["before"].startswith("ValueError: probe is not supported")
    assert out["registered"] is True
    assert "ProbeCallback" in out["callbacks"]


def test_the_registry_entry_is_what_report_to_builds(app, wired, tmp_path, monkeypatch):
    assert integration_utils.INTEGRATION_TO_CALLBACK["probe"] is ProbeCallback
    monkeypatch.setenv("PROBE_PROJECT", "e1")
    trainer = _trainer(tmp_path, report_to="probe", run_name="from-args")
    (callback,) = [c for c in trainer.callback_handler.callbacks if isinstance(c, ProbeCallback)]
    trainer.train()
    row = _only_run(app)
    assert row["name"] == "from-args"
    assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]
    assert callback._run.id == row["id"]
    monkeypatch.delitem(integration_utils.INTEGRATION_TO_CALLBACK, "probe")
    with pytest.raises(ValueError, match="probe is not supported"):
        _trainer(tmp_path, report_to="probe")
    probe.finish()


# -- one Trainer ---------------------------------------------------------------------


def test_a_train_logs_steps_eval_config_and_checkpoints(app, wired, tmp_path):
    callback = ProbeCallback(experiment="e1", name="tiny", config={"batch": 4})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _trainer(tmp_path, callbacks=[callback]).train()
    fluent._finish_at_exit()

    row = _only_run(app)
    assert row["status"] == "completed" and row["name"] == "tiny"
    assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]
    # Once each: evaluate() reaches on_log, and on_evaluate logs nothing.
    assert _points(app, row["id"], "eval/loss") == [2, 4]
    assert _points(app, row["id"], "train/learning_rate") == [1, 2, 3, 4]
    assert _points(app, row["id"], "train/train_loss") == [4]  # the closing summary
    assert not [
        k for p in app.metric_points_posted[row["id"]] for k in [p["key"]] if k.startswith("eval_")
    ]

    config = row["config"]
    assert config["batch"] == 4  # init's config=
    assert config["learning_rate"] == 0.01  # TrainingArguments
    assert config["hidden_size"] == 8 and config["num_hidden_layers"] == 2  # the model's config
    # Masked twice over: TrainingArguments.to_dict() says "<HUB_TOKEN>", and the
    # SDK's scrubber then redacts the token-named key itself.
    assert config["hub_token"] in ("<HUB_TOKEN>", "<redacted>")
    assert not [r for r in app.requests if HUB_TOKEN.encode() in (r.content or b"")]
    assert _probe_warnings(caught) == []

    stored = _stored_checkpoints(app, row["id"])
    assert sorted(stored) == ["checkpoint-2", "checkpoint-4"]
    for name, artifact in stored.items():
        folder = os.path.join(tmp_path, "out", name)
        assert artifact["is_reference"] is True and artifact["uri"].startswith("file://")
        assert artifact["size_bytes"] == _folder_bytes(folder) > 0  # the folder, summed
        assert artifact["meta"]["n_files"] == sum(len(f) for _, _, f in os.walk(folder))
        assert artifact["step_index"] == int(name.split("-")[1])
        assert "best" not in artifact["meta"]  # no metric_for_best_model: no "best"


def test_evaluations_after_train_at_the_last_step_are_kept_with_a_repeat_label(
    app, wired, tmp_path
):
    """Review of #2070, MED-2: with load_best_model_at_end, evaluate() on the
    reloaded best model and on a second eval set log eval/* again at the last
    step. The server keeps the first point per (key, step, labels), so both
    were dropped in silence. They now land labelled repeat=1 and repeat=2; an
    unchanged value (train/epoch beside each eval) is not re-sent."""
    trainer = _trainer(
        tmp_path,
        callbacks=[ProbeCallback(experiment="e1")],
        max_steps=6,
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        greater_is_better=True,  # the best checkpoint is NOT the last one
    )
    trainer.train()
    best = trainer.evaluate()
    other = trainer.evaluate(eval_dataset=_Other(8))
    run_id = _only_run(app)["id"]
    at_last = [
        (p.get("labels"), p["value"])
        for p in app.metric_points_posted[run_id]
        if p["key"] == "eval/loss" and p["step_index"] == 6
    ]
    assert [labels for labels, _ in at_last] == [None, {"repeat": 1}, {"repeat": 2}]
    assert [value for _, value in at_last][1:] == [best["eval_loss"], other["eval_loss"]]
    epochs_at_last = [
        p
        for p in app.metric_points_posted[run_id]
        if p["key"] == "train/epoch" and p["step_index"] == 6
    ]
    assert len(epochs_at_last) == 1  # the same 1.5 each time: sent once
    probe.finish()


def test_evaluate_alone_opens_the_run_from_on_log(app, wired, tmp_path):
    _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")]).evaluate()
    row = _only_run(app)
    assert _points(app, row["id"], "eval/loss") == [0]
    assert row["config"]["learning_rate"] == 0.01
    probe.finish()


def test_predict_metrics_land_under_test(app, wired, tmp_path):
    trainer = _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")])
    trainer.train()
    trainer.predict(_Data(8))
    row = _only_run(app)
    assert _points(app, row["id"], "test/loss") == [4]
    probe.finish()


def test_an_active_run_is_adopted_and_left_open(app, wired, tmp_path):
    run = probe.init(experiment="e1", name="mine", config={"seed_note": "script"})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _trainer(tmp_path, callbacks=[ProbeCallback()]).train()
    assert _probe_warnings(caught) == []  # nothing was ignored

    assert list(app.runs) == [run.id], "the callback opened a second run"
    assert _points(app, run.id, "train/loss") == [1, 2, 3, 4]
    assert app.runs[run.id]["status"] == "running"  # the script closes it
    assert app.runs[run.id]["config"]["seed_note"] == "script"
    assert app.runs[run.id]["config"]["learning_rate"] == 0.01
    probe.finish()


def test_adopting_the_scripts_run_warns_what_it_ignored_and_merges_config(app, wired, tmp_path):
    run = probe.init(experiment="e1", name="mine")
    with pytest.warns(
        UserWarning, match=r"adopted run .* its experiment, name, tags were not applied"
    ):
        _trainer(
            tmp_path,
            callbacks=[ProbeCallback(experiment="e1", name="x", tags=["a"], config={"k": 1})],
        ).train()
    assert app.runs[run.id]["config"]["k"] == 1
    probe.finish()


def test_a_failed_init_is_a_no_op_callback(app, wired, tmp_path, monkeypatch):
    def refuse(**kw):
        raise probe.errors.TransportError("API down")

    monkeypatch.setattr(probe, "init", refuse)
    with pytest.warns(UserWarning, match="could not open a run"):
        _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")]).train()  # training finishes
    assert app.runs == {}


class _NotWorldZero(Trainer):
    def is_world_process_zero(self) -> bool:
        return False


def test_a_process_that_is_not_world_zero_writes_nothing(app, wired, tmp_path):
    """Every hook, on a rank that is not world zero: no run, no request. The
    rank still saves checkpoints (should_save), and they are not recorded."""
    before = len(app.requests)
    callback = ProbeCallback(experiment="e1")
    trainer = _NotWorldZero(
        model=_model(),
        args=_args(tmp_path),
        train_dataset=_Data(16),
        eval_dataset=_Data(8),
        callbacks=[callback],
    )
    trainer.train()
    trainer.predict(_Data(8))
    assert os.path.isdir(tmp_path / "out" / "checkpoint-4")  # it did train and save
    assert len(app.requests) == before
    assert app.runs == {} and callback._run is None
    assert signal.getsignal(signal.SIGINT) is signal.default_int_handler  # nothing chained


def test_run_progress_is_called_at_each_step(app, wired, tmp_path, monkeypatch):
    """Plan 2.8's stall detector reads `run.progress()`: one per optimizer step."""
    from probe.sdk.run import Run

    calls = []
    monkeypatch.setattr(Run, "progress", lambda self: calls.append(self.id))
    _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")]).train()
    assert calls == [_only_run(app)["id"]] * 4
    probe.finish()


# -- checkpoints ---------------------------------------------------------------------


def test_a_folder_checkpoint_is_walked_once_per_save(app, wired, tmp_path, monkeypatch):
    from probe.sdk import hashing

    walks = []
    real = hashing.folder_size
    monkeypatch.setattr(hashing, "folder_size", lambda root: walks.append(root) or real(root))
    _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")]).train()
    assert [os.path.basename(w) for w in walks] == ["checkpoint-2", "checkpoint-4"]
    probe.finish()


def test_rows_follow_save_total_limit_and_the_best_checkpoint(app, wired, tmp_path):
    """With metric_for_best_model the rows carry monitor/score/best, and
    `best` follows the Trainer; a folder save_total_limit removed is marked
    deleted in place. Six steps, saves at 2/4/6, limit 1 (plus the best).
    The monitored metric is steered, 1.0 / 2.0 / 3.0 with lower better, so
    the best checkpoint is step 2 whatever the losses do."""
    evaluations = iter([1.0, 2.0, 3.0])
    trainer = _trainer(
        tmp_path,
        callbacks=[ProbeCallback(experiment="e1")],
        compute_metrics=lambda _prediction: {"steer": next(evaluations)},
        max_steps=6,
        save_total_limit=1,
        metric_for_best_model="steer",
        greater_is_better=False,
    )
    trainer.train()
    run_id = _only_run(app)["id"]
    stored = _stored_checkpoints(app, run_id)
    assert sorted(stored) == ["checkpoint-2", "checkpoint-4", "checkpoint-6"]
    assert {n: r["meta"].get("best") for n, r in stored.items()} == {
        "checkpoint-2": True,
        "checkpoint-4": False,
        "checkpoint-6": False,
    }
    assert trainer.state.best_model_checkpoint.endswith("checkpoint-2")
    # checkpoint-4 was rotated out at the next save; checkpoint-6 at the end of
    # train() (a limit of 1 keeps only the best). Every row says what the disk says.
    for name, row in stored.items():
        on_disk = os.path.isdir(os.path.join(tmp_path, "out", name))
        assert row["meta"].get("deleted", False) is (not on_disk), name
    assert stored["checkpoint-4"]["meta"]["deleted"] is True
    assert "deleted" not in stored["checkpoint-2"]["meta"]
    assert stored["checkpoint-4"]["meta"]["monitor"] == "eval_steer"
    assert stored["checkpoint-4"]["meta"]["score"] == 2.0
    assert stored["checkpoint-4"]["step_index"] == 4  # a refresh keeps the first step
    probe.finish()


def test_log_model_false_records_no_checkpoint(app, wired, tmp_path):
    _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1", log_model=False)]).train()
    run_id = _only_run(app)["id"]
    assert _checkpoint_posts(app, run_id) == []
    assert _points(app, run_id, "train/loss") == [1, 2, 3, 4]
    probe.finish()


# -- several Trainers, one process ---------------------------------------------------


def test_a_sweep_loop_gives_each_trainer_its_own_run(app, wired, tmp_path):
    for i in range(2):
        _trainer(
            tmp_path / str(i), callbacks=[ProbeCallback(experiment="e1", name=f"t{i}")]
        ).train()
    fluent._finish_at_exit()
    rows = sorted(app.runs.values(), key=lambda r: r["name"])
    assert [r["name"] for r in rows] == ["t0", "t1"]
    assert [r["status"] for r in rows] == ["completed", "completed"]
    for row in rows:
        assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]


def test_a_trial_whose_error_the_loop_caught_closes_failed(app, wired, tmp_path):
    before = signal.getsignal(signal.SIGINT)
    with pytest.raises(RuntimeError, match="boom"):
        _trainer(
            tmp_path / "a",
            callbacks=[ProbeCallback(experiment="e1", name="a"), _RaiseAt(2, RuntimeError("boom"))],
        ).train()
    assert isinstance(signal.getsignal(signal.SIGINT), hf._SignalNote)  # left by the raise
    _trainer(tmp_path / "b", callbacks=[ProbeCallback(experiment="e1", name="b")]).train()
    assert signal.getsignal(signal.SIGINT) is before  # taken off again
    fluent._finish_at_exit()
    assert {r["name"]: r["status"] for r in app.runs.values()} == {"a": "failed", "b": "completed"}


def test_a_ctrl_c_the_script_caught_closes_canceled_and_the_note_steps_aside(app, wired, tmp_path):
    """The note sees the Ctrl-C, puts the handler it found back, and hands
    the signal on (KeyboardInterrupt, as before). A later check for the
    default handler (asyncio.run makes one) finds it."""
    before = signal.getsignal(signal.SIGINT)

    class _CtrlC(TrainerCallback):
        def on_step_end(self, args, state, control, **kwargs):
            if state.global_step == 2:
                signal.raise_signal(signal.SIGINT)

    with pytest.raises(KeyboardInterrupt):
        _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1"), _CtrlC()]).train()
    assert signal.getsignal(signal.SIGINT) is before
    hf._note_unfinished_at_exit()
    fluent._finish_at_exit()
    assert _only_run(app)["status"] == "canceled"


def test_a_failure_the_script_caught_at_the_end_closes_failed(app, wired, tmp_path):
    """No later Trainer closes it: the exit check does (the order against
    probe's own close is proven in a real process below)."""
    with pytest.raises(RuntimeError):
        _trainer(
            tmp_path, callbacks=[ProbeCallback(experiment="e1"), _RaiseAt(2, RuntimeError("boom"))]
        ).train()
    hf._note_unfinished_at_exit()
    fluent._finish_at_exit()
    assert _only_run(app)["status"] == "failed"


def test_a_train_that_ended_leaves_the_exit_verdict_alone(app, wired, tmp_path):
    """The control for the test above: the same exit check after a train()
    that reached on_train_end changes nothing."""
    _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")]).train()
    hf._note_unfinished_at_exit()
    fluent._finish_at_exit()
    assert _only_run(app)["status"] == "completed"


def test_after_probe_finish_the_next_train_writes_the_scripts_next_run(app, wired, tmp_path):
    """Review of this PR, HIGH: one Trainer reused per seed, the script
    opening and finishing a run around each train(). The callback held on to
    the first, closed run: every later curve went there, the new run empty."""
    trainer = _trainer(tmp_path, callbacks=[ProbeCallback()])
    runs = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for seed in ("a", "b"):
            runs.append(probe.init(experiment="e1", name=seed))
            trainer.train()
            probe.finish()
    assert _probe_warnings(caught) == []
    for run in runs:
        assert _points(app, run.id, "train/loss") == [1, 2, 3, 4], run.id
        assert app.runs[run.id]["status"] == "completed"


def test_after_probe_finish_a_callbacks_own_run_is_followed_by_a_new_one(app, wired, tmp_path):
    trainer = _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")])
    trainer.train()
    probe.finish()
    trainer.train()
    fluent._finish_at_exit()
    assert len(app.runs) == 2
    for row in app.runs.values():
        assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]
        assert row["status"] == "completed"


def test_of_two_probe_callbacks_the_one_given_arguments_logs(app, wired, tmp_path):
    """Review of #2070, LOW: report_to=["probe"] builds a bare ProbeCallback
    first, and it won over the user's configured one: the run floated,
    unnamed, and the experiment= and name= were silently dropped."""
    with pytest.warns(UserWarning, match="the one given arguments logs"):
        _trainer(
            tmp_path,
            report_to=["probe"],
            callbacks=[ProbeCallback(experiment="e1", name="explicit")],
        ).train()
    row = _only_run(app)
    (e1,) = [e["id"] for e in app.experiments.values() if e["slug"] == "e1"]
    assert row["name"] == "explicit"
    assert e1 in (row.get("experiment_id"), row.get("project_id"))
    assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]
    probe.finish()


def test_two_probe_callbacks_on_one_trainer_log_once(app, wired, tmp_path, monkeypatch):
    """report_to="probe" plus callbacks=[ProbeCallback()]: the second one
    closed the first's run as a failed trial and opened a stray run."""
    monkeypatch.setenv("PROBE_PROJECT", "e1")
    with pytest.warns(UserWarning, match="two ProbeCallbacks"):
        _trainer(tmp_path, report_to="probe", callbacks=[ProbeCallback()]).train()
    fluent._finish_at_exit()
    row = _only_run(app)
    assert row["status"] == "completed"
    assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]  # once each


def test_a_second_trainer_on_the_scripts_run_is_told_it_shares_it(app, wired, tmp_path):
    """The server keeps the first point per step (ON CONFLICT DO NOTHING), so
    Trainer 2's curve would be lost with no word. Only the second adoption
    warns, and it points at the line that started it."""
    run = probe.init(experiment="e1", name="mine")
    shared: list = []
    for i in range(2):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            _trainer(tmp_path / str(i), callbacks=[ProbeCallback()]).train()
        shared = [w for w in caught if "an earlier Trainer in this process" in str(w.message)]
        assert len(shared) == i
    assert "server keeps the first point" in str(shared[0].message)
    assert "probe.finish()" in str(shared[0].message)
    assert os.path.abspath(shared[0].filename) == os.path.abspath(__file__)
    assert list(app.runs) == [run.id]
    probe.finish()


def test_training_again_below_the_logged_steps_warns_once(app, wired, tmp_path):
    trainer = _trainer(tmp_path, callbacks=[ProbeCallback(experiment="e1")])
    trainer.train()
    with pytest.warns(UserWarning, match=r"train\(\) started again at step 0, below step 4"):
        trainer.train()
    assert len(app.runs) == 1
    probe.finish()


def test_under_a_launcher_every_callback_writes_the_launchers_run(
    app, wired, tmp_path, monkeypatch
):
    from probe.sdk.run import EXEC_FINALIZES_ENV

    for var in ("RANK", "WORLD_SIZE", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK"):
        monkeypatch.delenv(var, raising=False)
    launcher = make_client(app, tmp_spool=tmp_path / "launcher")
    run = launcher.run(experiment="e1", name="launched", heartbeat=False, capture_outputs=False)
    monkeypatch.setenv("PROBE_RUN_ID", run.id)
    monkeypatch.setenv("PROBE_RUN_EPOCH", str(run.write_epoch))
    monkeypatch.setenv(EXEC_FINALIZES_ENV, run.id)
    with pytest.warns(UserWarning, match="ProbeCallback's experiment were not applied"):
        _trainer(tmp_path / "a", callbacks=[ProbeCallback(experiment="e1")]).train()
    with pytest.warns(UserWarning, match="chose one run for the whole process"):
        _trainer(tmp_path / "b", callbacks=[ProbeCallback()]).train()
    assert list(app.runs) == [run.id]
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "running"  # the launcher closes it
    launcher.close()


def test_under_a_launcher_a_failure_the_script_caught_leaves_the_verdict_to_it(
    app, wired, tmp_path, monkeypatch
):
    """Review of this PR, MED: the script joined the launcher's run with its
    own probe.init(); the exit check saw a script run, noted `failed`, and
    the close skipped the launcher's hand-off. `probe exec` reads exit 0."""
    from probe.sdk.run import EXEC_FINALIZES_ENV

    for var in ("RANK", "WORLD_SIZE", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK"):
        monkeypatch.delenv(var, raising=False)
    launcher = make_client(app, tmp_spool=tmp_path / "launcher")
    run = launcher.run(experiment="e1", name="launched", heartbeat=False, capture_outputs=False)
    monkeypatch.setenv("PROBE_RUN_ID", run.id)
    monkeypatch.setenv("PROBE_RUN_EPOCH", str(run.write_epoch))
    monkeypatch.setenv(EXEC_FINALIZES_ENV, run.id)
    assert probe.init().id == run.id  # the script joins it
    with pytest.raises(RuntimeError):
        _trainer(tmp_path, callbacks=[ProbeCallback(), _RaiseAt(2, RuntimeError("boom"))]).train()
    hf._note_unfinished_at_exit()
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "running"  # the launcher closes it
    launcher.close()


def test_an_older_callback_still_writing_to_its_closed_run_warns_once(app, wired, tmp_path):
    first = _trainer(tmp_path / "a", callbacks=[ProbeCallback(experiment="e1", name="a")])
    first.train()
    _trainer(tmp_path / "b", callbacks=[ProbeCallback(experiment="e1", name="b")]).train()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        first.evaluate()
        first.evaluate()
    assert len([w for w in caught if "already closed (completed)" in str(w.message)]) == 1
    fluent._finish_at_exit()


def test_each_hyperparameter_trial_gets_its_own_run(app, wired, tmp_path):
    """hyperparameter_search calls train() once per trial on ONE callback
    (state.is_hyper_param_search, state.trial_name); the hooks are driven
    directly here, the search backends being optional packages."""
    from transformers import TrainerControl, TrainerState

    callback = ProbeCallback(experiment="e1")
    args = _args(tmp_path, run_name="final")
    # Two trials, then the final train() with the best values (HF's own
    # recipe: set them on trainer.args, train() again on the same Trainer).
    for trial in ("trial-0", "trial-1", None):
        state = TrainerState(is_hyper_param_search=trial is not None, trial_name=trial, max_steps=1)
        callback.on_train_begin(args, state, TrainerControl(), model=_model())
        state.global_step = 1
        callback.on_log(args, state, TrainerControl(), logs={"loss": 0.5})
        callback.on_train_end(args, state, TrainerControl())
    fluent._finish_at_exit()
    rows = {r["name"]: r for r in app.runs.values()}
    assert sorted(rows) == ["final", "trial-0", "trial-1"]
    assert {r["status"] for r in rows.values()} == {"completed"}
    assert all(_points(app, r["id"], "train/loss") == [1] for r in rows.values())


def test_an_optuna_search_names_each_trial_and_a_pruned_one_is_canceled(app, wired, tmp_path):
    """Review of #2070, LOWs: every trial was named after run_name alone, and
    the trial transformers pruned (on_train_end, then optuna.TrialPruned)
    closed `completed`. A real optuna search: trial 1 is pruned at its first
    evaluation; the final train() with the best values gets its own run."""
    if os.environ.get("PROBE_REQUIRE_INTEGRATIONS") == "1":
        import optuna
    else:
        optuna = pytest.importorskip("optuna")

    class _PruneTrialOne(optuna.pruners.BasePruner):
        def prune(self, study, trial):
            return trial.number == 1

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    trainer = Trainer(
        model_init=lambda trial=None: _model(),
        args=_args(tmp_path, run_name="search"),
        train_dataset=_Data(16),
        eval_dataset=_Data(8),
        callbacks=[ProbeCallback(experiment="e1")],
    )
    best = trainer.hyperparameter_search(
        direction="minimize",
        backend="optuna",
        n_trials=3,
        hp_space=lambda trial: {"learning_rate": trial.suggest_float("learning_rate", 1e-3, 1e-1)},
        pruner=_PruneTrialOne(),
    )
    for key, value in best.hyperparameters.items():
        setattr(trainer.args, key, value)
    trainer.train()
    fluent._finish_at_exit()
    statuses = {row["name"]: row["status"] for row in app.runs.values()}
    assert statuses == {
        "search-trial-0": "completed",
        "search-trial-1": "canceled",
        "search-trial-2": "completed",
        "search": "completed",
    }


# -- pickling ------------------------------------------------------------------------


def test_a_pickled_copy_carries_no_token_and_opens_its_own_run(app, wired, tmp_path, monkeypatch):
    """ray's hyperparameter_search pickles the Trainer, callbacks included:
    the copy drops the live handle and the client (it holds the token)."""
    client = make_client(app, tmp_spool=tmp_path / "own")
    callback = ProbeCallback(experiment="e1", client=client)
    _trainer(tmp_path / "a", callbacks=[callback]).train()
    with pytest.warns(UserWarning, match="client= was pickled"):
        blob = pickle.dumps(callback)
    assert b"ros_pat_deadbeef" not in blob
    copy = pickle.loads(blob)
    assert copy._run is None and "client" not in copy._init_kwargs
    probe.finish()
    client.close()


# -- how the job ended: real processes ------------------------------------------------

_VERDICT_SCRIPT = textwrap.dedent(
    """
    import os, signal, sys, time
    import torch
    from transformers import (BertConfig, BertForSequenceClassification, Trainer,
                              TrainerCallback, TrainingArguments)
    from probe.integrations.huggingface import ProbeCallback

    out, mode = sys.argv[1], sys.argv[2]

    class Data(torch.utils.data.Dataset):
        def __init__(self, n):
            g = torch.Generator().manual_seed(0)
            self.x = torch.randint(0, 32, (n, 6), generator=g)
            self.y = torch.randint(0, 2, (n,), generator=g)
        def __len__(self): return len(self.x)
        def __getitem__(self, i): return {"input_ids": self.x[i], "labels": self.y[i]}

    class Stop(TrainerCallback):
        def __init__(self): self.trainer = None
        def on_step_end(self, args, state, control, **kw):
            if state.global_step != 2:
                if mode == "jit_sigterm":
                    time.sleep(0.3)  # give the JIT timer thread its moment
                return
            if mode.endswith("error"):
                raise RuntimeError("boom")
            if mode.endswith("ctrl_c"):
                signal.raise_signal(signal.SIGINT)  # a real Ctrl-C, through the handlers
            if mode == "jit_sigterm":
                jit = [c for c in self.trainer.callback_handler.callbacks if type(c).__name__ == "JITCheckpointCallback"]
                jit[0].jit_manager.kill_wait = 0
                os.kill(os.getpid(), signal.SIGTERM)
                time.sleep(0.3)

    model = BertForSequenceClassification(BertConfig(
        vocab_size=32, hidden_size=8, num_hidden_layers=2, num_attention_heads=2,
        intermediate_size=16, max_position_embeddings=16))
    args = TrainingArguments(
        output_dir=out, max_steps=8, per_device_train_batch_size=2, logging_steps=1,
        save_strategy="no", report_to="none", use_cpu=True, disable_tqdm=True,
        # Only named when used: transformers 4.x has no such argument.
        **({"enable_jit_checkpoint": True} if mode == "jit_sigterm" else {}))
    stop = Stop()
    trainer = Trainer(model=model, args=args, train_dataset=Data(16),
                      callbacks=[ProbeCallback(experiment="e1", name=mode), stop])
    stop.trainer = trainer
    if mode.startswith("caught"):
        try:
            trainer.train()
        except (RuntimeError, KeyboardInterrupt):
            print("caught", file=sys.stderr)
    else:
        trainer.train()
    """
)


@pytest.mark.parametrize(
    "mode, status, exit_zero",
    [
        ("complete", "completed", True),
        ("error", "failed", False),
        ("ctrl_c", "canceled", False),
        ("caught_error", "failed", True),
        ("caught_ctrl_c", "canceled", True),
        ("jit_sigterm", "failed", True),
    ],
)
def test_a_real_process_closes_its_run_with_how_the_job_ended(
    app, tmp_path, mode, status, exit_zero
):
    """Through probe's real exit hooks. `caught_*`: the script caught what
    stopped train() and ran to its end (exit 0). `jit_sigterm`:
    enable_jit_checkpoint turned a SIGTERM into a normal return at step 3 of
    8 (exit 0), and its checkpoint, which no on_save reported, is recorded."""
    if mode == "jit_sigterm" and "enable_jit_checkpoint" not in {
        f.name for f in dataclasses.fields(TrainingArguments)
    }:
        pytest.skip("this transformers has no enable_jit_checkpoint (added in 5.x)")
    app.seed_experiment("e1")
    script = tmp_path / "verdict.py"
    script.write_text(_VERDICT_SCRIPT)
    with serve(app) as url:
        done = subprocess.run(
            [sys.executable, str(script), str(tmp_path / "out"), mode],
            env=child_env(url, PROBE_HW="0", PROBE_HEARTBEAT_SECONDS="0", OMP_NUM_THREADS="1"),
            capture_output=True,
            text=True,
            timeout=240,
        )
    assert (done.returncode == 0) is exit_zero, done.stderr[-3000:]
    row = _only_run(app)
    assert row["status"] == status, done.stderr[-3000:]
    steps = _points(app, row["id"], "train/loss")
    if mode == "complete":
        assert steps == list(range(1, 9))
    elif mode == "jit_sigterm":
        assert steps[:2] == [1, 2] and steps[-1] < 8  # stopped early
    else:
        assert steps == [1]  # stopped inside step 2, before its log
    if mode == "jit_sigterm":
        (checkpoint,) = _checkpoint_posts(app, row["id"])
        (on_disk,) = os.listdir(tmp_path / "out")
        assert checkpoint["name"] == on_disk and on_disk.startswith("checkpoint-")
        assert checkpoint["size_bytes"] == _folder_bytes(
            os.path.join(tmp_path, "out", checkpoint["name"])
        )


_WORKER_SCRIPT = textwrap.dedent(
    """
    import os, sys, time
    import torch
    from transformers import (BertConfig, BertForSequenceClassification, Trainer,
                              TrainerCallback, TrainingArguments)
    from probe.integrations.huggingface import ProbeCallback

    class Data(torch.utils.data.Dataset):
        def __init__(self, n):
            g = torch.Generator().manual_seed(0)
            self.x = torch.randint(0, 32, (n, 6), generator=g)
            self.y = torch.randint(0, 2, (n,), generator=g)
        def __len__(self): return len(self.x)
        def __getitem__(self, i): return {"input_ids": self.x[i], "labels": self.y[i]}

    class Ctl(TrainerCallback):
        def __init__(self, mode): self.mode = mode
        def on_step_end(self, args, state, control, **kw):
            if self.mode == "slow":
                time.sleep(0.3)
            if self.mode == "fail" and state.global_step == 2:
                raise RuntimeError("boom")

    def train(out, mode, name, ddp=False):
        torch.manual_seed(0)
        model = BertForSequenceClassification(BertConfig(
            vocab_size=32, hidden_size=8, num_hidden_layers=2, num_attention_heads=2,
            intermediate_size=16, max_position_embeddings=16))
        args = TrainingArguments(
            output_dir=out, max_steps=(400 if mode == "slow" else 8), per_device_train_batch_size=2,
            logging_steps=1, save_strategy="no", report_to="none", use_cpu=True, disable_tqdm=True,
            **({"ddp_backend": "gloo"} if ddp else {}))
        Trainer(model=model, args=args, train_dataset=Data(32),
                callbacks=[ProbeCallback(experiment="e1", name=name), Ctl(mode)]).train()

    def job(out, mode):
        train(out, mode, "nb", ddp=True)

    if __name__ == "__main__":
        out, how, modes = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
        if how == "notebook_launcher":
            from accelerate import notebook_launcher
            notebook_launcher(job, (out, modes[0]), num_processes=2, use_port=sys.argv[4])
        else:  # one forked Process per trial
            import multiprocessing as mp
            ctx = mp.get_context("fork")
            for i, mode in enumerate(modes):
                p = ctx.Process(target=train, args=(os.path.join(out, str(i)), mode, f"t{i}-{mode}"))
                p.start()
                p.join()
    """
)


def _free_port() -> str:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return str(sock.getsockname()[1])


def _run_workers(app, tmp_path, how: str, modes: str, *, sig=None, target=None, timeout=240):
    """Run the worker script against the served fake. With ``sig``, send it
    once three train/loss points are in: to the whole process group, or to
    the launching process alone (``target="parent"``, SIGKILL)."""
    app.seed_experiment("e1")
    script = tmp_path / "workers.py"
    script.write_text(_WORKER_SCRIPT)
    with serve(app) as url:
        proc = subprocess.Popen(
            [sys.executable, str(script), str(tmp_path / "out"), how, modes, _free_port()],
            env=child_env(url, PROBE_HW="0", PROBE_HEARTBEAT_SECONDS="0", OMP_NUM_THREADS="1"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            if sig is not None:
                deadline = time.monotonic() + 120
                while (
                    time.monotonic() < deadline
                    and sum(
                        1
                        for pts in app.metric_points_posted.values()
                        for p in pts
                        if p["key"] == "train/loss"
                    )
                    < 3
                ):
                    time.sleep(0.2)
                if target == "parent":
                    os.kill(proc.pid, sig)
                else:
                    os.killpg(proc.pid, sig)
            _, stderr = proc.communicate(timeout=timeout)
            if target == "parent":
                # The orphaned workers close after the parent is gone: wait for it.
                deadline = time.monotonic() + 60
                while time.monotonic() < deadline and any(
                    r["status"] == "running" for r in app.runs.values()
                ):
                    time.sleep(0.2)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            _, stderr = proc.communicate()
            pytest.fail(f"workers hung; last stderr:\n{stderr[-4000:]}")
    return proc.returncode, stderr


def test_a_forked_process_per_trial_closes_each_run_with_how_it_ended(app, tmp_path):
    """Review of #2070, MED-1: a forked worker leaves through os._exit, which
    runs no exit hook, so every run stayed `running`, successes included."""
    returncode, stderr = _run_workers(app, tmp_path, "process", "ok,fail,ok")
    assert returncode == 0, stderr[-3000:]
    statuses = {row["name"]: row["status"] for row in app.runs.values()}
    assert statuses == {"t0-ok": "completed", "t1-fail": "failed", "t2-ok": "completed"}, stderr[
        -3000:
    ]


@pytest.mark.parametrize("mode, status", [("ok", "completed"), ("fail", "failed")])
def test_accelerate_notebook_launcher_closes_the_run(app, tmp_path, mode, status):
    """notebook_launcher forks the ranks (torch's start_processes); rank 0's
    worker opened the run and closes it on its way out."""
    returncode, stderr = _run_workers(app, tmp_path, "notebook_launcher", mode)
    assert (returncode == 0) is (mode == "ok"), stderr[-3000:]
    row = _only_run(app)
    assert row["status"] == status, stderr[-3000:]


def test_ctrl_c_in_a_forked_worker_closes_its_run_canceled(app, tmp_path):
    """torch's worker wrapper swallows KeyboardInterrupt, so the worker exits
    0 and no exception is in flight at its close; the signal note saw the
    Ctrl-C (the parent still there), and the train() never ended."""
    _, stderr = _run_workers(app, tmp_path, "notebook_launcher", "slow", sig=signal.SIGINT)
    assert _only_run(app)["status"] == "canceled", stderr[-6000:]


def test_a_killed_launcher_leaves_its_forked_worker_to_close_failed(app, tmp_path):
    """SIGKILL the notebook_launcher process: torch's death signal (SIGINT)
    reaches the workers with their parent gone. Nobody decided that: `failed`,
    never `canceled`."""
    _run_workers(app, tmp_path, "notebook_launcher", "slow", sig=signal.SIGKILL, target="parent")
    assert _only_run(app)["status"] == "failed"


_DDP_SCRIPT = textwrap.dedent(
    """
    import json, os, sys
    import torch
    from transformers import BertConfig, BertForSequenceClassification, Trainer, TrainingArguments
    from probe.integrations.huggingface import ProbeCallback

    class Data(torch.utils.data.Dataset):
        def __init__(self, n):
            g = torch.Generator().manual_seed(0)
            self.x = torch.randint(0, 32, (n, 6), generator=g)
            self.y = torch.randint(0, 2, (n,), generator=g)
        def __len__(self): return len(self.x)
        def __getitem__(self, i): return {"input_ids": self.x[i], "labels": self.y[i]}

    torch.manual_seed(0)
    model = BertForSequenceClassification(BertConfig(
        vocab_size=32, hidden_size=8, num_hidden_layers=2, num_attention_heads=2,
        intermediate_size=16, max_position_embeddings=16))
    out = sys.argv[1]
    args = TrainingArguments(
        output_dir=os.path.join(out, "ckpt"), max_steps=4, per_device_train_batch_size=2,
        logging_steps=1, save_steps=2, report_to="none", use_cpu=True, ddp_backend="gloo",
        disable_tqdm=True)
    callback = ProbeCallback(experiment="e1", name="ddp")
    trainer = Trainer(model=model, args=args, train_dataset=Data(16), callbacks=[callback])
    trainer.train()
    rank = int(os.environ["RANK"])
    with open(os.path.join(out, f"rank{rank}.json"), "w") as f:
        json.dump({"world_zero": trainer.is_world_process_zero(), "has_run": callback._run is not None,
                   "world_size": args.world_size}, f)
    """
)


def test_two_ranks_over_gloo_only_world_zero_writes(app, tmp_path):
    """torchrun, 2 processes, gloo: rank 0 opens the one run and writes the
    curve and checkpoints; rank 1 opens nothing and, against a server that
    takes no writer leases, sends nothing."""
    app.seed_experiment("e1")
    script = tmp_path / "ddp_train.py"
    script.write_text(_DDP_SCRIPT)
    with serve(app) as url:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "torch.distributed.run",
                "--standalone",
                "--nproc_per_node=2",
                str(script),
                str(tmp_path),
            ],
            env=child_env(url, PROBE_HW="0", PROBE_HEARTBEAT_SECONDS="0", OMP_NUM_THREADS="1"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            _, stderr = proc.communicate(timeout=240)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            _, stderr = proc.communicate()
            pytest.fail(f"torchrun hung; last stderr:\n{stderr[-4000:]}")
    assert proc.returncode == 0, stderr[-4000:]
    ranks = [json.loads((tmp_path / f"rank{r}.json").read_text()) for r in (0, 1)]
    assert ranks == [
        {"world_zero": True, "has_run": True, "world_size": 2},
        {"world_zero": False, "has_run": False, "world_size": 2},
    ]
    row = _only_run(app)
    assert row["status"] == "completed"
    assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]  # once each: one writer
    assert sorted(_stored_checkpoints(app, row["id"])) == ["checkpoint-2", "checkpoint-4"]
    creates = [
        r for r in app.requests if r.method == "POST" and r.url.path.rstrip("/").endswith("/runs")
    ]
    assert len(creates) == 1
    # A server without writer leases (this fake's default) gets nothing from
    # rank 1: never a run-level heartbeat, which would keep the run alive with
    # rank 0 gone.
    assert not [r for r in app.requests if r.url.path.endswith("/heartbeat") or "/writers/" in r.url.path]


# -- every rank holds a writer lease (plan 2.8 + (b)) --------------------------------
_LEASE_SCRIPT = textwrap.dedent(
    """
    import os, sys
    import torch
    from transformers import (BertConfig, BertForSequenceClassification, Trainer,
                              TrainerCallback, TrainingArguments)
    from probe.integrations.huggingface import ProbeCallback

    class Data(torch.utils.data.Dataset):
        def __init__(self, n):
            g = torch.Generator().manual_seed(0)
            self.x = torch.randint(0, 32, (n, 6), generator=g)
            self.y = torch.randint(0, 2, (n,), generator=g)
        def __len__(self): return len(self.x)
        def __getitem__(self, i): return {"input_ids": self.x[i], "labels": self.y[i]}

    class RankOneFails(TrainerCallback):
        def on_step_end(self, args, state, control, **kwargs):
            if int(os.environ["RANK"]) == 1 and state.global_step == 2:
                raise RuntimeError("rank 1 boom")

    out, mode = sys.argv[1], sys.argv[2]
    torch.manual_seed(0)
    model = BertForSequenceClassification(BertConfig(
        vocab_size=32, hidden_size=8, num_hidden_layers=2, num_attention_heads=2,
        intermediate_size=16, max_position_embeddings=16))
    args = TrainingArguments(
        output_dir=os.path.join(out, "ckpt"), max_steps=4, per_device_train_batch_size=2,
        logging_steps=1, save_strategy="no", report_to="none", use_cpu=True, ddp_backend="gloo",
        disable_tqdm=True)
    rank = int(os.environ["RANK"])
    with open(os.path.join(out, f"rank{rank}.pid"), "w") as f:
        f.write(str(os.getpid()))
    # A common HF shape: loggers attached on the main process only (or, by
    # mistake, only elsewhere).
    only = {"rank0-only": 0, "rank1-only": 1}.get(mode)
    callbacks = [ProbeCallback(experiment="e1", name="ddp")] if only in (None, rank) else []
    if mode == "rank1-fails":
        callbacks.append(RankOneFails())
    Trainer(model=model, args=args, train_dataset=Data(16), callbacks=callbacks).train()
    with open(os.path.join(out, f"rank{rank}.done"), "w") as f:
        f.write("trained")
    """
)


def _torchrun_leases(app, tmp_path, mode: str, *, timeout: float = 240, **env: str) -> tuple[int, str]:
    """The two-rank job; a hang past ``timeout`` fails the test."""
    app.supports_leases = True
    app.seed_experiment("e1")
    script = tmp_path / "ddp_leases.py"
    script.write_text(_LEASE_SCRIPT)
    with serve(app) as url:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "torch.distributed.run",
                "--standalone",
                "--nproc_per_node=2",
                str(script),
                str(tmp_path),
                mode,
            ],
            env=child_env(url, PROBE_HW="0", PROBE_HEARTBEAT_SECONDS="0", OMP_NUM_THREADS="1", **env),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            _, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # torchrun starts each worker in a session of its own: killing
            # torchrun's group orphans them, still holding the pipes.
            for pid_file in tmp_path.glob("rank*.pid"):
                try:
                    os.kill(int(pid_file.read_text()), signal.SIGKILL)
                except (OSError, ValueError):
                    pass
            os.killpg(proc.pid, signal.SIGKILL)
            _, stderr = proc.communicate(timeout=30)
            pytest.fail(f"torchrun hung past {timeout:g} s; last stderr:\n{stderr[-4000:]}")
    return proc.returncode, stderr


def _leases_by_rank(app, run_id: str) -> dict[int, dict]:
    leases = list(app.leases.get(run_id, {}).values())
    by_rank = {lease.get("rank"): lease for lease in leases}
    assert len(by_rank) == len(leases), leases
    return by_rank


def test_two_ranks_each_hold_a_lease_on_the_one_run_and_rank_one_writes_nothing(app, tmp_path):
    """Plan 2.8 + (b): every rank holds a writer lease, metrics stay world
    zero's. Rank 0 opens the run under its owner lease and broadcasts it in
    on_train_begin; rank 1 joins as a lease-only writer (beats, never logs,
    never sends a status) and releases at its clean exit. Before this, rank 1
    held no lease: a lost node was invisible to 2.8."""
    returncode, stderr = _torchrun_leases(app, tmp_path, "ok")
    assert returncode == 0, stderr[-4000:]
    row = _only_run(app)
    by_rank = _leases_by_rank(app, row["id"])
    assert sorted(by_rank) == [0, 1], by_rank
    assert (by_rank[0]["role"], by_rank[1]["role"]) == ("owner", "rank")
    assert by_rank[1]["world_size"] == 2 and by_rank[1]["write_epoch"] == row.get("write_epoch", 1)
    assert [by_rank[r]["exit_status"] for r in (0, 1)] == ["completed", "completed"]
    assert row["status"] == "completed"
    assert row["liveness_protocol"] == "leases"  # nothing flipped it to legacy
    # Rank 1 wrote no metric: every batch is world zero's, each step once.
    assert {b.get("session_id") for b in app.metric_batches_posted} == {by_rank[0]["session_id"]}
    assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]
    assert not [r for r in app.requests if r.url.path.endswith("/heartbeat")]
    assert not [
        r for r in app.requests if r.method == "PATCH" and b'"status"' in (r.content or b"")
    ], "a status PATCH: the leases close this run, and rank 1 never sends one"


def test_a_rank_that_crashes_releases_its_lease_failed(app, tmp_path):
    """An exception out of train() on rank 1 alone: the process's exit hooks
    record it and the lease is released `failed` before the process goes
    (torchrun then stops rank 0). Rank 1 still wrote no metric."""
    returncode, stderr = _torchrun_leases(app, tmp_path, "rank1-fails")
    assert returncode != 0
    assert "rank 1 boom" in stderr
    row = _only_run(app)
    by_rank = _leases_by_rank(app, row["id"])
    assert sorted(by_rank) == [0, 1], (by_rank, stderr[-4000:])
    assert by_rank[1]["released_at"] and by_rank[1]["exit_status"] == "failed", stderr[-4000:]
    assert by_rank[1]["session_id"] not in {b.get("session_id") for b in app.metric_batches_posted}


# -- a callback on some ranks only: nothing may wait on the others -------------------
#: Well past a normal run of this job (~15 s here) and the 10 s a rank waits
#: for rank 0's run id, well short of gloo's 30-minute collective timeout.
_NO_HANG_SECONDS = 120


def test_a_callback_on_rank_zero_only_never_waits_for_the_other_ranks(app, tmp_path):
    """Review of #2091 (BLOCKER): `callbacks=[ProbeCallback()] if
    trainer.is_world_process_zero() else []` is a common HF shape. The run id
    went out in a collective broadcast that rank 1 never joins, so rank 0
    blocked in it (until the process group's 30-minute timeout). Rank 0 only
    publishes now; it never waits."""
    returncode, stderr = _torchrun_leases(app, tmp_path, "rank0-only", timeout=_NO_HANG_SECONDS)
    assert returncode == 0, stderr[-4000:]
    assert all((tmp_path / f"rank{r}.done").exists() for r in (0, 1))
    row = _only_run(app)
    assert row["status"] == "completed"
    by_rank = _leases_by_rank(app, row["id"])
    assert sorted(by_rank) == [0] and by_rank[0]["role"] == "owner"
    assert _points(app, row["id"], "train/loss") == [1, 2, 3, 4]


def test_a_callback_on_rank_one_only_gives_up_on_the_run_id_and_trains_on(app, tmp_path):
    """The other way round: rank 1 waits at most `RUN_ID_WAIT_SECONDS` for a
    run id rank 0 never publishes (it has no callback, so there is no run),
    says so once, and training completes."""
    started = time.monotonic()
    returncode, stderr = _torchrun_leases(app, tmp_path, "rank1-only", timeout=_NO_HANG_SECONDS)
    assert returncode == 0, stderr[-4000:]
    assert all((tmp_path / f"rank{r}.done").exists() for r in (0, 1))
    assert time.monotonic() - started < hf.RUN_ID_WAIT_SECONDS + 60
    assert stderr.count("got no run id from rank 0") == 1, stderr[-4000:]
    assert app.runs == {} and not [r for r in app.requests if "/writers/" in r.url.path]


def test_under_a_launcher_a_rank_takes_its_lease_on_probe_run_id_without_waiting(app, tmp_path):
    """PROBE_RUN_ID (`probe exec`) names the run on every rank: rank 1 leases
    it at once, with no hand-off from rank 0 -- here rank 0 has no callback at
    all, so nothing is published -- and no warning."""
    launcher = make_client(app, tmp_spool=tmp_path / "launcher")
    app.seed_experiment("e1")
    run = launcher.run(experiment="e1", name="launched", heartbeat=False, capture_outputs=False)
    returncode, stderr = _torchrun_leases(
        app,
        tmp_path,
        "rank1-only",
        timeout=_NO_HANG_SECONDS,
        PROBE_RUN_ID=run.id,
        PROBE_RUN_EPOCH=str(run.write_epoch or 1),
    )
    assert returncode == 0, stderr[-4000:]
    assert "got no run id" not in stderr
    by_rank = _leases_by_rank(app, run.id)
    assert sorted(by_rank) == [1] and by_rank[1]["role"] == "rank"
    assert by_rank[1]["exit_status"] == "completed"
    launcher.close()
