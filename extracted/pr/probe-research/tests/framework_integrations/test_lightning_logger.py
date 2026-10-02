"""ProbeLogger through a REAL Lightning `Trainer.fit` (plan (a), task T27).

Tiny CPU model, 16 samples in batches of 4, two epochs: eight optimizer steps.
The single-process tests drive the real Trainer against the in-process fake
API; the two-rank test runs `torchrun` over gloo against the same fake served
on a loopback socket, which is the DDP shape Anthrogen launches.

Skipped when `lightning` is not installed (the default agent-ci job). The
integrations job sets PROBE_REQUIRE_INTEGRATIONS=1, which turns a missing
install into a failure instead of a green skip.

Checkpoint rows are read through `_stored_checkpoints`, which folds the POSTs
the way the server stores them: a hashless path reference is keyed on (run,
name, uri) and refreshed IN PLACE by a re-log (`app/artifacts/service.py`,
`apply_artifact`), keeping its first `step_index`. The fake only appends.
"""

from __future__ import annotations

import enum
import json
import multiprocessing.context
import os
import pickle
import shutil
import signal
import subprocess
import sys
import textwrap
import time
import warnings
from dataclasses import dataclass

import pytest

if os.environ.get("PROBE_REQUIRE_INTEGRATIONS") == "1":
    import lightning  # noqa: F401 -- an ImportError here fails the job
else:
    pytest.importorskip("lightning")

import torch  # noqa: E402
from lightning.pytorch import LightningModule, Trainer  # noqa: E402
from lightning.fabric.plugins import CheckpointIO  # noqa: E402
from lightning.pytorch.callbacks import ModelCheckpoint  # noqa: E402
from lightning.pytorch.loggers.logger import DummyExperiment  # noqa: E402
from lightning.pytorch.utilities.exceptions import SIGTERMException  # noqa: E402
from lightning.pytorch.utilities.rank_zero import rank_zero_only  # noqa: E402
from torch.utils.data import DataLoader, TensorDataset  # noqa: E402

import probe  # noqa: E402
import probe.integrations.lightning as lightning_logger  # noqa: E402
import probe.sdk.client as client_module  # noqa: E402
from probe.integrations.lightning import ProbeLogger  # noqa: E402
from probe.sdk import fluent  # noqa: E402
from tests.conftest import make_client  # noqa: E402
from tests.served_fake_app import child_env, serve  # noqa: E402


class Tiny(LightningModule):
    def __init__(self, lr: float = 0.1, fail_at: int | None = None, raise_at: str | None = None):
        super().__init__()
        self.save_hyperparameters()
        self.layer = torch.nn.Linear(4, 1)

    def training_step(self, batch, batch_idx):
        if self.hparams.fail_at is not None and self.global_step == self.hparams.fail_at:
            raise {
                "runtime": RuntimeError("boom"),
                "ctrl_c": KeyboardInterrupt(),
                "sigterm": SIGTERMException(),
            }[self.hparams.raise_at or "runtime"]
        x, y = batch
        loss = torch.nn.functional.mse_loss(self.layer(x), y)
        self.log("train_loss", loss, on_step=True, on_epoch=False)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        self.log("val_loss", torch.nn.functional.mse_loss(self.layer(x), y))

    def configure_optimizers(self):
        return torch.optim.SGD(self.parameters(), lr=self.hparams.lr)


def _loader() -> DataLoader:
    generator = torch.Generator().manual_seed(0)
    data = TensorDataset(torch.randn(16, 4, generator=generator), torch.randn(16, 1, generator=generator))
    return DataLoader(data, batch_size=4)


def _trainer(logger, tmp_path, *, callbacks=None, max_epochs=2, **kw) -> Trainer:
    return Trainer(
        max_epochs=max_epochs,
        accelerator="cpu",
        devices=1,
        logger=logger,
        log_every_n_steps=1,
        enable_progress_bar=False,
        enable_model_summary=False,
        default_root_dir=str(tmp_path),
        callbacks=callbacks or [ModelCheckpoint(monitor="val_loss", save_top_k=2, save_last=True)],
        **kw,
    )


@pytest.fixture(autouse=True)
def _clean_binding():
    """fluent keeps process state on purpose; tests must not inherit it."""

    def reset():
        lightning_logger._LOGGER_RUNS.clear()
        lightning_logger._LAUNCHER_RUNS.clear()
        lightning_logger._SCRIPT_RUNS.clear()
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
def _keep_sigint():
    """Lightning's Ctrl-C path sets SIGINT to SIG_IGN; give the suite its Ctrl-C back."""
    before = signal.getsignal(signal.SIGINT)
    yield
    signal.signal(signal.SIGINT, before)


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    """A bare `probe.init()` builds a client wired to the fake: the path the
    logger takes in real use."""
    monkeypatch.setattr(fluent, "Client", lambda *a, **kw: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e1")


def _points(app, run_id: str, key: str) -> list[int]:
    return sorted(p["step_index"] for p in app.metric_points_posted.get(run_id, []) if p["key"] == key)


def _only_run(app) -> dict:
    (row,) = app.runs.values()
    return row


def _checkpoint_posts(app, run_id: str) -> list[dict]:
    return [a for a in app.artifacts.get(run_id, []) if a.get("kind") == "checkpoint"]


def _stored_checkpoints(app, run_id: str) -> dict[str, dict]:
    """What the server holds per checkpoint path (see the module docstring)."""
    stored: dict[tuple[str, str], dict] = {}
    for post in _checkpoint_posts(app, run_id):
        key = (post["name"], post["uri"])
        first = stored.get(key)
        stored[key] = {**post, "step_index": first["step_index"] if first else post.get("step_index")}
    return {row["meta"]["local_path"]: row for row in stored.values()}


def test_a_fit_logs_one_run_with_its_steps_and_checkpoints(app, wired, tmp_path):
    logger = ProbeLogger(experiment="e1", name="tiny", config={"batch_size": 4})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _trainer(logger, tmp_path).fit(Tiny(), _loader(), _loader())
    fluent._finish_at_exit()

    row = _only_run(app)
    assert row["status"] == "completed"
    assert _points(app, row["id"], "train_loss") == list(range(8))
    assert _points(app, row["id"], "val_loss")  # once per epoch
    assert logger.version == row["id"]
    # The creation-time config, and the module's hyperparameters merged in
    # after the run opened (run.update_config, plan (c)).
    assert row["config"]["batch_size"] == 4
    assert row["config"]["lr"] == 0.1
    assert not [w for w in caught if str(w.message).startswith("probe:")]

    checkpoints = [a for a in app.artifacts.get(row["id"], []) if a.get("kind") == "checkpoint"]
    assert checkpoints, "no checkpoint was recorded"
    for artifact in checkpoints:
        assert artifact["is_reference"] is True and artifact["uri"].startswith("file://")
        assert artifact["size_bytes"] > 0
    scored = [a for a in checkpoints if "score" in a["meta"]]
    assert scored and all(a["meta"]["monitor"] == "val_loss" for a in scored)
    assert any(a["meta"].get("last") for a in checkpoints)


def test_an_exception_in_training_closes_the_run_failed(app, wired, tmp_path):
    with pytest.raises(RuntimeError, match="boom"):
        _trainer(ProbeLogger(experiment="e1"), tmp_path).fit(Tiny(fail_at=2), _loader())
    fluent._finish_at_exit()
    assert _only_run(app)["status"] == "failed"


def test_ctrl_c_closes_the_run_canceled(app, wired, tmp_path):
    """Lightning catches KeyboardInterrupt, calls finalize("failed") and exits 1:
    no process hook sees the Ctrl-C, the logger does."""
    with pytest.raises(SystemExit):
        _trainer(ProbeLogger(experiment="e1"), tmp_path).fit(
            Tiny(fail_at=2, raise_at="ctrl_c"), _loader()
        )
    fluent._finish_at_exit()
    assert _only_run(app)["status"] == "canceled"


def test_sigterm_closes_the_run_failed_not_completed(app, wired, tmp_path):
    """SIGTERMException is a code-less SystemExit: the process exits 0."""
    with pytest.raises(SystemExit):
        _trainer(ProbeLogger(experiment="e1"), tmp_path).fit(
            Tiny(fail_at=2, raise_at="sigterm"), _loader()
        )
    fluent._finish_at_exit()
    assert _only_run(app)["status"] == "failed"


def test_an_active_run_is_adopted_and_left_open(app, wired, tmp_path):
    run = probe.init(experiment="e1", name="mine")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _trainer(ProbeLogger(), tmp_path).fit(Tiny(), _loader())
    assert not [w for w in caught if "adopted" in str(w.message)]  # nothing was ignored

    assert list(app.runs) == [run.id], "the logger opened a second run"
    assert _points(app, run.id, "train_loss") == list(range(8))
    assert app.runs[run.id]["status"] == "running"  # the script closes it
    probe.finish()


def test_a_prefix_sections_every_key(app, wired, tmp_path):
    _trainer(ProbeLogger(experiment="e1", prefix="stage1"), tmp_path).fit(Tiny(), _loader())
    row = _only_run(app)
    assert _points(app, row["id"], "stage1/train_loss") == list(range(8))
    probe.finish()


def test_a_failed_init_is_a_no_op_logger(app, wired, tmp_path, monkeypatch):
    def refuse(**kw):
        raise probe.errors.TransportError("API down")

    monkeypatch.setattr(probe, "init", refuse)
    logger = ProbeLogger(experiment="e1")
    with pytest.warns(UserWarning, match="could not open a run"):
        _trainer(logger, tmp_path).fit(Tiny(), _loader())  # training finishes
    assert app.runs == {}
    assert isinstance(logger.experiment, DummyExperiment)


def test_a_non_zero_rank_writes_nothing(app, wired, monkeypatch, tmp_path):
    """The hooks Lightning calls on every rank, on rank 1: no run, no request."""
    monkeypatch.setattr(rank_zero_only, "rank", 1)
    logger = ProbeLogger(experiment="e1")
    before = len(app.requests)

    assert isinstance(logger.experiment, DummyExperiment)
    logger.log_hyperparams({"lr": 0.1})
    logger.log_metrics({"loss": 1.0}, step=0)
    logger.finalize("failed")
    _ = logger.version

    assert len(app.requests) == before
    assert app.runs == {}


def test_pickling_reattaches_by_run_id(app, wired, tmp_path, monkeypatch):
    """ddp_spawn pickles the logger into each worker. The copy carries the run
    id, never the live handle, and writes to the same run without claiming it."""
    logger = ProbeLogger(experiment="e1")
    run_id = logger.experiment.id

    monkeypatch.setattr(client_module, "Client", lambda *a, **kw: make_client(app, tmp_spool=tmp_path / "spool2"))
    copy = pickle.loads(pickle.dumps(logger))
    copy.log_metrics({"loss": 0.5}, step=3)

    assert copy.version == run_id and list(app.runs) == [run_id]
    assert _points(app, run_id, "loss") == [3]
    probe.finish()


def _recording_client(app, tmp_path, monkeypatch) -> list[dict]:
    built: list[dict] = []

    def build(*args, **kwargs):
        built.append(kwargs)
        return make_client(app, tmp_spool=tmp_path / f"copy{len(built)}")

    monkeypatch.setattr(client_module, "Client", build)
    return built


def test_a_custom_client_reaches_a_spawned_worker(app, wired, tmp_path, monkeypatch):
    """A Client cannot be pickled, so the copy used a default Client() from the
    environment: another server, or another identity. Pickled to LAUNCH a
    worker, the copy gets the custom client's settings."""
    client = make_client(app, tmp_spool=tmp_path / "own")
    logger = ProbeLogger(experiment="e1", client=client)
    run_id = logger.experiment.id
    multiprocessing.context.set_spawning_popen(object())
    try:
        blob = pickle.dumps(logger)
    finally:
        multiprocessing.context.set_spawning_popen(None)
    built = _recording_client(app, tmp_path, monkeypatch)

    copy = pickle.loads(blob)
    copy.log_metrics({"loss": 0.5}, step=3)

    assert built == [{"settings": client.settings}]
    assert _points(app, run_id, "loss") == [3]
    probe.finish()
    client.close()


def test_a_custom_client_pickled_elsewhere_warns_it_stays_behind(app, wired, tmp_path, monkeypatch):
    """Anywhere but a process launch the token is never pickled (it could land
    in a file), so the copy builds its own client -- and says so."""
    client = make_client(app, tmp_spool=tmp_path / "own")
    logger = ProbeLogger(experiment="e1", client=client)
    _ = logger.experiment
    with pytest.warns(UserWarning, match="client= was pickled"):
        blob = pickle.dumps(logger)
    assert b"ros_pat_deadbeef" not in blob
    built = _recording_client(app, tmp_path, monkeypatch)
    pickle.loads(blob).log_metrics({"loss": 0.5}, step=3)
    assert built == [{}]
    probe.finish()
    client.close()


# -- one run per Trainer (sweep loops) ---------------------------------------------
def test_a_sweep_loop_gives_each_trainer_its_own_run(app, wired, tmp_path):
    """Review HIGH2: the second logger adopted the run the first one left open,
    so two trials became ONE run named after the first, with the first's
    config, and train_loss 0..7 twice (the server keeps one point per step)."""
    for lr in (0.1, 0.01):
        logger = ProbeLogger(experiment="e1", name=f"lr-{lr}", config={"lr": lr})
        _trainer(logger, tmp_path / str(lr)).fit(Tiny(lr=lr), _loader(), _loader())
        if lr == 0.1:
            first = logger.version
    # The first trial was closed when the second Trainer started, not at exit.
    assert app.runs[first]["status"] == "completed"
    fluent._finish_at_exit()

    rows = sorted(app.runs.values(), key=lambda row: row["name"])
    assert [row["name"] for row in rows] == ["lr-0.01", "lr-0.1"]
    for row, lr in zip(rows, (0.01, 0.1)):
        assert row["status"] == "completed"
        assert row["config"]["lr"] == lr
        assert _points(app, row["id"], "train_loss") == list(range(8))


def test_a_trial_whose_error_the_loop_caught_closes_failed(app, wired, tmp_path):
    with pytest.raises(RuntimeError, match="boom"):
        _trainer(ProbeLogger(experiment="e1", name="bad"), tmp_path / "a").fit(Tiny(fail_at=2), _loader())
    _trainer(ProbeLogger(experiment="e1", name="good"), tmp_path / "b").fit(Tiny(), _loader())
    fluent._finish_at_exit()
    assert {row["name"]: row["status"] for row in app.runs.values()} == {
        "bad": "failed",
        "good": "completed",
    }


def test_adopting_the_scripts_run_warns_what_it_ignored_and_merges_config(app, wired, tmp_path):
    run = probe.init(experiment="e1", name="mine")
    with pytest.warns(UserWarning, match=r"adopted run .* so its name, tags were not applied"):
        _trainer(ProbeLogger(name="other", tags=["x"], config={"bs": 4}), tmp_path).fit(Tiny(), _loader())
    assert list(app.runs) == [run.id]
    assert app.runs[run.id]["name"] == "mine"
    assert app.runs[run.id]["config"]["bs"] == 4
    assert app.runs[run.id]["status"] == "running"  # still the script's to close
    probe.finish()


def test_under_a_launcher_every_logger_writes_the_launchers_run(app, wired, tmp_path, monkeypatch):
    """PROBE_RUN_ID (`probe exec`): probe.init() refuses identity kwargs next to
    it, which disabled the logger for the whole job. And the logger must never
    close the launcher's run to open another: a process has one run there."""
    for var in ("RANK", "WORLD_SIZE", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK"):
        monkeypatch.delenv(var, raising=False)
    launcher = make_client(app, tmp_spool=tmp_path / "launcher")
    run = launcher.run(experiment="e1", name="launched", heartbeat=False, capture_outputs=False)
    monkeypatch.setenv("PROBE_RUN_ID", run.id)
    monkeypatch.setenv("PROBE_RUN_EPOCH", str(run.write_epoch))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for name in ("a", "b"):
            _trainer(ProbeLogger(experiment="e1", name=name), tmp_path / name).fit(Tiny(), _loader())

    assert list(app.runs) == [run.id]
    assert app.runs[run.id]["status"] == "running"  # the launcher closes it
    assert _points(app, run.id, "train_loss") == sorted(list(range(8)) * 2)
    messages = [str(w.message) for w in caught]
    assert any("experiment, name were not applied" in m for m in messages)
    assert any("same run an earlier ProbeLogger" in m for m in messages)
    probe.finish()
    launcher.close()


def test_a_run_a_parent_process_opened_is_neither_adopted_nor_closed(app, wired, tmp_path):
    """A forked worker inherits its parent's binding and this module's map: the
    parent's trial is the parent's to close, and this Trainer is its own trial."""
    parent = probe.init(experiment="e1", name="parent-trial")
    lightning_logger._LOGGER_RUNS[parent.id] = os.getpid() + 1  # opened before a fork
    # What a fork copies: the binding too, naming the pid that opened it. So
    # the worker's own probe.init() opens a run beside it (#2016's reinit
    # closes only a run this process opened).
    binding = fluent._current.get()
    binding.owner = (os.getpid() + 1, *binding.owner[1:])
    logger = ProbeLogger(experiment="e1", name="worker-trial")
    _trainer(logger, tmp_path).fit(Tiny(), _loader())
    assert logger.version != parent.id
    assert app.runs[parent.id]["status"] == "running"
    assert app.runs[logger.version]["name"] == "worker-trial"
    probe.finish()


# -- hyperparameters (plan (c)) ---------------------------------------------------
@dataclass
class _Optimizer:
    name: str = "sgd"
    momentum: float = 0.9


class _Mode(enum.Enum):
    FAST = "fast"


class _Configured(Tiny):
    def __init__(self, optimizer=_Optimizer(), mode=_Mode.FAST, clip=float("inf"), lr=0.1):
        super().__init__(lr=lr)
        self.save_hyperparameters()


def test_hyperparameters_land_in_the_run_config_coerced(app, wired, tmp_path):
    """Through the SDK's coercion (plan (c)), not a local str() fallback: a
    dataclass is a mapping, an Enum its value, infinity JSON's spelling."""
    _trainer(ProbeLogger(experiment="e1"), tmp_path).fit(_Configured(), _loader())
    config = _only_run(app)["config"]
    assert config["optimizer"] == {"name": "sgd", "momentum": 0.9}
    assert config["mode"] == "fast"
    assert config["clip"] == "Infinity"
    assert config["lr"] == 0.1
    probe.finish()


# -- checkpoints ------------------------------------------------------------------
class _FolderIO(CheckpointIO):
    """A sharded checkpoint, as DeepSpeed and FSDP write one: a FOLDER whose
    files are rewritten in place, so the folder's own mtime never moves."""

    def save_checkpoint(self, checkpoint, path, storage_options=None):
        os.makedirs(path, exist_ok=True)
        for shard in ("model_states.pt", "optim_states.pt"):
            with open(os.path.join(path, shard), "wb") as f:
                f.write(b"x" * 100 * (checkpoint["global_step"] + 1))

    def load_checkpoint(self, path, map_location=None):
        raise NotImplementedError

    def remove_checkpoint(self, path):
        shutil.rmtree(path, ignore_errors=True)


def test_a_folder_rewritten_in_place_is_recorded_at_every_save(app, wired, tmp_path):
    """Review MED4: the dedupe key was (path, folder mtime), so `last.ckpt`
    saved at step 4 and again at step 8 was recorded once, with step 4's size."""
    callback = ModelCheckpoint(save_last=True)
    _trainer(ProbeLogger(experiment="e1"), tmp_path, callbacks=[callback], plugins=[_FolderIO()]).fit(
        Tiny(), _loader()
    )
    run_id = _only_run(app)["id"]
    last = os.path.abspath(callback.last_model_path)
    posts = [p for p in _checkpoint_posts(app, run_id) if p["meta"]["local_path"] == last]
    assert [p["meta"]["step"] for p in posts] == [4, 8]
    assert [p["size_bytes"] for p in posts] == [1000, 1800]
    assert all(p["meta"]["is_directory"] and p["meta"]["n_files"] == 2 for p in posts)
    assert _stored_checkpoints(app, run_id)[last]["meta"]["step"] == 8
    probe.finish()


def test_checkpoint_rows_follow_top_k_pruning(app, wired, tmp_path):
    """Review LOW: every row kept the flags it was saved with -- five epochs at
    save_top_k=2 left several `best: True` and rows for files top-k had
    deleted. Now the stored rows say what is true at the end."""
    callback = ModelCheckpoint(monitor="val_loss", save_top_k=2, save_last=True)
    _trainer(ProbeLogger(experiment="e1"), tmp_path, callbacks=[callback], max_epochs=5).fit(
        Tiny(), _loader(), _loader()
    )
    stored = _stored_checkpoints(app, _only_run(app)["id"])
    best = os.path.abspath(callback.best_model_path)
    kept = {os.path.abspath(p) for p in callback.best_k_models} | {os.path.abspath(callback.last_model_path)}
    assert kept <= set(stored)
    assert [path for path, row in stored.items() if row["meta"]["best"]] == [best]
    for path, row in stored.items():
        meta = row["meta"]
        if path in kept:
            assert os.path.exists(path) and "superseded" not in meta and "deleted" not in meta
        else:
            assert meta["superseded"] is True and meta["deleted"] is True
            assert not os.path.exists(path)
            assert row["size_bytes"] > 0  # the refresh keeps what the first write said
            assert meta["written_at"] and meta["step"] == row["step_index"]
    assert len(stored) > len(kept), "nothing was pruned; the test proves nothing"
    probe.finish()


# -- a failed init ------------------------------------------------------------------
def test_each_failed_init_gets_its_own_checkpoint_folder(app, wired, tmp_path, monkeypatch):
    """A fixed "offline" version put every such job in <root>/e1/offline/."""

    def refuse(**kw):
        raise probe.errors.TransportError("API down")

    monkeypatch.setattr(probe, "init", refuse)
    folders = []
    for _ in range(2):
        callback = ModelCheckpoint(save_top_k=0, save_last=True)
        with pytest.warns(UserWarning, match="could not open a run"):
            _trainer(ProbeLogger(experiment="e1"), tmp_path, callbacks=[callback]).fit(Tiny(), _loader())
        folders.append(callback.dirpath)
    assert folders[0] != folders[1]
    assert all(os.path.basename(os.path.dirname(f)).startswith("offline-") for f in folders)


# -- the run-id broadcast -----------------------------------------------------------
@pytest.fixture
def two_ranks(monkeypatch):
    """torch.distributed as two initialized ranks; records every broadcast."""
    import torch.distributed as dist

    state = {"rank": 0, "calls": [], "payload": None}

    def broadcast(objects, src=0):
        state["calls"].append(list(objects))
        if state["rank"] != src:
            objects[0] = state["payload"]

    monkeypatch.setattr(dist, "is_available", lambda: True)
    monkeypatch.setattr(dist, "is_initialized", lambda: True)
    monkeypatch.setattr(dist, "get_world_size", lambda *a, **k: 2)
    monkeypatch.setattr(dist, "get_rank", lambda *a, **k: state["rank"])
    monkeypatch.setattr(dist, "broadcast_object_list", broadcast)
    return state


def test_only_lightnings_setup_hook_starts_the_broadcast(app, wired, two_ranks):
    """A rank-0-only read of `experiment` (a callback, `prepare_data`) must not
    start a collective: the other ranks never join it, or pair it with
    another collective. Lightning's `_call_setup_hook` reads it on every rank."""
    logger = ProbeLogger(experiment="e1")
    run = logger.experiment
    _ = logger.experiment.id, logger.version
    assert two_ranks["calls"] == []

    def _call_setup_hook():  # the name Lightning's reader has
        return logger.experiment

    _call_setup_hook()
    _call_setup_hook()
    assert two_ranks["calls"] == [[(run.id, run.write_epoch)]]
    probe.finish()


def test_a_rank_told_there_is_no_run_holds_no_lease(app, wired, two_ranks, monkeypatch):
    """Rank 0's init failed, so it broadcast (None, None): that is not a run id."""
    monkeypatch.setattr(rank_zero_only, "rank", 1)
    two_ranks.update(rank=1, payload=(None, None))
    leases = []
    monkeypatch.setattr(ProbeLogger, "_start_rank_lease", lambda self, *a: leases.append(a))
    logger = ProbeLogger(experiment="e1")

    def _call_setup_hook():
        return logger.experiment

    assert isinstance(_call_setup_hook(), DummyExperiment)
    assert len(two_ranks["calls"]) == 1
    assert leases == [] and logger._run_id is None


_DDP_SCRIPT = textwrap.dedent(
    """
    import json, os, sys
    import torch
    from torch.utils.data import DataLoader, TensorDataset
    from lightning.pytorch import LightningModule, Trainer
    from probe.integrations.lightning import ProbeLogger

    class Tiny(LightningModule):
        def __init__(self):
            super().__init__()
            self.layer = torch.nn.Linear(4, 1)
        def training_step(self, batch, batch_idx):
            x, y = batch
            loss = torch.nn.functional.mse_loss(self.layer(x), y)
            self.log("train_loss", loss, on_step=True, on_epoch=False)
            return loss
        def configure_optimizers(self):
            return torch.optim.SGD(self.parameters(), lr=0.1)

    g = torch.Generator().manual_seed(0)
    data = TensorDataset(torch.randn(16, 4, generator=g), torch.randn(16, 1, generator=g))
    logger = ProbeLogger(experiment="e1", name="ddp")
    trainer = Trainer(
        max_epochs=2, accelerator="cpu", devices=2, strategy="ddp", num_nodes=1,
        logger=logger, log_every_n_steps=1, enable_progress_bar=False,
        enable_model_summary=False, enable_checkpointing=False,
        default_root_dir=sys.argv[1],
    )
    trainer.fit(Tiny(), DataLoader(data, batch_size=4))
    with open(os.path.join(sys.argv[1], f"rank{trainer.global_rank}.json"), "w") as f:
        json.dump({"run_id": logger._run_id, "epoch": logger._write_epoch,
                   "has_run": logger._run is not None}, f)
    """
)


def test_two_ranks_over_gloo_share_the_run_and_only_rank_zero_writes(app, tmp_path):
    """torchrun, 2 processes, gloo: rank 0 opens the run and broadcasts its id
    and epoch; rank 1 learns both and writes nothing. A server without writer
    leases (this fake's default) gets nothing at all from rank 1: never a
    run-level heartbeat, which would keep the run alive with rank 0 gone."""
    app.seed_experiment("e1")
    script = tmp_path / "ddp_fit.py"
    script.write_text(_DDP_SCRIPT)
    with serve(app) as url:
        # Its own session, so a hang kills every rank, not just the launcher.
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "torch.distributed.run", "--standalone",
                "--nproc_per_node=2", str(script), str(tmp_path),
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
    row = _only_run(app)
    assert ranks[0] == {"run_id": row["id"], "epoch": row.get("write_epoch", 1), "has_run": True}
    assert ranks[1] == {"run_id": row["id"], "epoch": ranks[0]["epoch"], "has_run": False}
    assert row["status"] == "completed"
    # Each rank trains on half the batches: 2 per epoch, 4 optimizer steps.
    assert _points(app, row["id"], "train_loss") == list(range(4))
    assert not [r for r in app.requests if r.url.path.endswith("/heartbeat") or "/writers/" in r.url.path]


# -- every rank holds a writer lease (plan 2.8 + (a)) --------------------------------
_LEASE_SCRIPT = textwrap.dedent(
    """
    import os, sys, time
    import torch
    from torch.utils.data import DataLoader, TensorDataset
    from lightning.pytorch import LightningModule, Trainer
    from probe.integrations.lightning import ProbeLogger

    root, mode = sys.argv[1], sys.argv[2]
    rank = int(os.environ["RANK"])

    class Tiny(LightningModule):
        def __init__(self):
            super().__init__()
            self.layer = torch.nn.Linear(4, 1)
        def training_step(self, batch, batch_idx):
            if mode == "slow":
                if self.global_step == 0:
                    with open(os.path.join(root, f"rank{rank}.pid"), "w") as f:
                        f.write(str(os.getpid()))
                time.sleep(0.2)
            x, y = batch
            loss = torch.nn.functional.mse_loss(self.layer(x), y)
            self.log("train_loss", loss, on_step=True, on_epoch=False)
            return loss
        def configure_optimizers(self):
            return torch.optim.SGD(self.parameters(), lr=0.1)

    g = torch.Generator().manual_seed(0)
    data = TensorDataset(torch.randn(16, 4, generator=g), torch.randn(16, 1, generator=g))
    trainer = Trainer(
        max_epochs=(200 if mode == "slow" else 2), accelerator="cpu", devices=2, strategy="ddp",
        logger=ProbeLogger(experiment="e1", name="ddp"), log_every_n_steps=1,
        enable_progress_bar=False, enable_model_summary=False, enable_checkpointing=False,
        default_root_dir=root,
    )
    trainer.fit(Tiny(), DataLoader(data, batch_size=4))
    """
)


def _torchrun_leases(app, tmp_path, mode: str, *, kill=None) -> tuple[int, str]:
    """The two-rank torchrun job against a fake that takes writer leases.
    ``kill(tmp_path, proc)`` runs once both ranks hold their lease and rank 0
    has logged a few steps (``mode="slow"``)."""
    app.supports_leases = True
    app.seed_experiment("e1")
    script = tmp_path / "ddp_leases.py"
    script.write_text(_LEASE_SCRIPT)
    with serve(app) as url:
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "torch.distributed.run", "--standalone",
                "--nproc_per_node=2", str(script), str(tmp_path), mode,
            ],
            env=child_env(url, PROBE_HW="0", PROBE_HEARTBEAT_SECONDS="0", OMP_NUM_THREADS="1"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            if kill is not None:
                deadline = time.monotonic() + 60
                while True:
                    leases = [lease for held in app.leases.values() for lease in held.values()]
                    points = sum(len(v) for v in app.metric_points_posted.values())
                    pids = all((tmp_path / f"rank{r}.pid").exists() for r in (0, 1))
                    if len(leases) == 2 and points >= 3 and pids:
                        break
                    if time.monotonic() > deadline or proc.poll() is not None:
                        os.killpg(proc.pid, signal.SIGKILL)
                        _, stderr = proc.communicate()
                        pytest.fail(
                            f"the job never had both ranks' leases and 3 steps before the kill: "
                            f"{len(leases)} lease(s), {points} point(s); stderr:\n{stderr[-2000:]}"
                        )
                    time.sleep(0.1)
                kill(tmp_path, proc)
            _, stderr = proc.communicate(timeout=180)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            _, stderr = proc.communicate()
            pytest.fail(f"torchrun hung; last stderr:\n{stderr[-4000:]}")
    return proc.returncode, stderr


def _leases_by_rank(app, run_id: str) -> dict[int, dict]:
    leases = list(app.leases.get(run_id, {}).values())
    by_rank = {lease.get("rank"): lease for lease in leases}
    assert len(by_rank) == len(leases), leases
    return by_rank


def _telemetry_sessions(app) -> set:
    return {batch.get("session_id") for batch in app.metric_batches_posted}


def test_two_ranks_each_hold_a_lease_on_the_one_run_and_rank_one_writes_nothing(app, tmp_path):
    """Plan 2.8 + (a): the server can tell a lost node from a finished job only
    if every rank holds a writer lease. Rank 0 opens the run under its owner
    lease; rank 1 joins as a lease-only writer (beats, never logs, never sends
    a status) and releases at its clean exit. Before this, 0.195.0's rank 1
    held no lease at all (the soak worked around it with PROBE_RUN_ID)."""
    returncode, stderr = _torchrun_leases(app, tmp_path, "ok")
    assert returncode == 0, stderr[-4000:]
    row = _only_run(app)
    by_rank = _leases_by_rank(app, row["id"])
    assert sorted(by_rank) == [0, 1], by_rank
    assert (by_rank[0]["role"], by_rank[1]["role"]) == ("owner", "rank")
    assert by_rank[1]["world_size"] == 2 and by_rank[1]["write_epoch"] == row.get("write_epoch", 1)
    assert [by_rank[r]["exit_status"] for r in (0, 1)] == ["completed", "completed"]
    assert all(by_rank[r]["released_at"] for r in (0, 1))
    assert row["status"] == "completed"
    assert row["liveness_protocol"] == "leases"  # nothing flipped it to legacy
    # Rank 1 wrote no metric: every batch is rank 0's, and the curve is one writer's.
    assert _telemetry_sessions(app) == {by_rank[0]["session_id"]}
    assert _points(app, row["id"], "train_loss") == list(range(4))
    releases = [r["session_id"] for r in app.lease_releases]
    assert sorted(releases) == sorted([by_rank[0]["session_id"], by_rank[1]["session_id"]])
    assert not [r for r in app.requests if r.url.path.endswith("/heartbeat")]
    assert not [
        r for r in app.requests if r.method == "PATCH" and b'"status"' in (r.content or b"")
    ], "a status PATCH: the leases close this run, and rank 1 never sends one"


def test_a_node_lost_mid_fit_leaves_its_lease_and_the_survivor_releases_its_own(app, tmp_path):
    """The partial-node failure 2.8 exists for: rank 0 is SIGKILLed mid-fit.
    Its owner lease is never released (nothing runs in a killed process; the
    server reads it expired), while rank 1 -- whose gloo peer vanished and
    which torch then SIGTERMs -- releases its own lease `failed` before it
    goes."""

    def kill_rank_zero(root, proc):
        os.kill(int((root / "rank0.pid").read_text()), signal.SIGKILL)

    returncode, stderr = _torchrun_leases(app, tmp_path, "slow", kill=kill_rank_zero)
    assert returncode != 0
    row = _only_run(app)
    by_rank = _leases_by_rank(app, row["id"])
    assert sorted(by_rank) == [0, 1], (by_rank, stderr[-4000:])
    assert by_rank[0]["released_at"] is None  # the lost node: its lease just stops
    assert by_rank[1]["released_at"] and by_rank[1]["exit_status"] == "failed", stderr[-4000:]
    assert by_rank[1]["session_id"] not in _telemetry_sessions(app)
    assert row["status"] == "running"  # the owner's expiry decides it, server-side


def test_a_preempted_job_releases_every_ranks_lease_failed(app, tmp_path):
    """SIGTERM to torchrun (a scheduler preempting the job, a deleted pod):
    it forwards SIGTERM to both ranks, Lightning turns it into
    SIGTERMException (a code-less exit 0, which no exit hook reads as a
    failure), and each rank releases its lease `failed` from its logger's
    `finalize`. The run closes `failed` from its leases."""

    def preempt(root, proc):
        os.kill(proc.pid, signal.SIGTERM)

    _, stderr = _torchrun_leases(app, tmp_path, "slow", kill=preempt)
    row = _only_run(app)
    by_rank = _leases_by_rank(app, row["id"])
    assert sorted(by_rank) == [0, 1], (by_rank, stderr[-4000:])
    assert [by_rank[r]["exit_status"] for r in (0, 1)] == ["failed", "failed"], stderr[-4000:]
    assert row["status"] == "failed"
    assert by_rank[1]["session_id"] not in _telemetry_sessions(app)


def _gone(pid: int) -> bool:
    """Exited: no such process, or a zombie its launcher has not reaped yet."""
    try:
        with open(f"/proc/{pid}/stat") as f:
            return f.read().rsplit(")", 1)[1].split()[0] == "Z"
    except OSError:
        return True


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="reads /proc")
def test_sigterm_to_rank_zero_alone_still_closes_the_run_preempted(app, tmp_path):
    """One node of a multi-node job is preempted, or its pod deleted: only
    rank 0's process gets SIGTERM (each node runs its own torchrun). Lightning
    2.6's SIGTERM handler BROADCASTS from rank 0 inside the handler, a
    collective no other rank joins, so rank 0's main thread blocks in gloo for
    good. Ours, which Lightning composes after that notifier, never ran: the
    run stayed `running`, and torchrun SIGKILLed rank 0 30 s later (soak
    finding F2). Ours now runs first, and when the handler it chains does not
    return, the close goes ahead on our worker thread: the run closes
    failed/preempted, and rank 0 ends, within the budget."""
    budget = 6.0
    script = tmp_path / "ddp_leases.py"
    script.write_text(_LEASE_SCRIPT)
    app.supports_leases = True
    app.seed_experiment("e1")
    with serve(app) as url:
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "torch.distributed.run", "--standalone",
                "--nproc_per_node=2", str(script), str(tmp_path), "slow",
            ],
            env=child_env(
                url, PROBE_HW="0", PROBE_HEARTBEAT_SECONDS="0", OMP_NUM_THREADS="1",
                PROBE_SIGTERM_FLUSH_SECONDS=str(budget),
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            deadline = time.monotonic() + 90
            while True:
                leases = [lease for held in app.leases.values() for lease in held.values()]
                points = sum(len(v) for v in app.metric_points_posted.values())
                if len(leases) == 2 and points >= 3 and (tmp_path / "rank0.pid").exists():
                    break
                assert time.monotonic() < deadline and proc.poll() is None, (
                    f"the job never had both leases and 3 steps: {len(leases)} lease(s), "
                    f"{points} point(s)"
                )
                time.sleep(0.1)
            rank0 = int((tmp_path / "rank0.pid").read_text())
            sent = time.monotonic()
            os.kill(rank0, signal.SIGTERM)
            while not _gone(rank0) and time.monotonic() - sent < budget + 10:
                time.sleep(0.1)
            took = time.monotonic() - sent
            row = dict(_only_run(app))
        finally:
            # torch starts each rank in a session of its own: the group kill
            # alone would leave a rank stuck in gloo holding the pipes open.
            for r in (0, 1):
                try:
                    os.kill(int((tmp_path / f"rank{r}.pid").read_text()), signal.SIGKILL)
                except (OSError, ValueError):
                    pass
            os.killpg(proc.pid, signal.SIGKILL)
            _, stderr = proc.communicate()
    assert "Received SIGTERM" in stderr, stderr[-4000:]  # Lightning's notifier ran
    assert row["status"] == "failed", (row["status"], took, stderr[-4000:])
    finish = (row.get("summary_metrics") or row.get("summary") or {}).get("probe_finish") or {}
    assert finish.get("reason") == "preempted" and finish.get("signal") == "SIGTERM", finish
    assert took < budget + 2, (took, stderr[-4000:])
    assert "closed the run from another thread" in stderr, stderr[-4000:]


def test_lightnings_composed_sigterm_handler_has_the_shape_run_first_reorders(app, wired, tmp_path):
    """`preempt.run_first` recognises Lightning's `_HandlersCompose` by its
    `signal_handlers` list, which it calls in order, ours last: checked here on
    the real one, during a real fit, after the first logged step."""
    from probe.sdk import preempt

    seen = {}

    class Look(Tiny):
        def on_train_batch_end(self, outputs, batch, batch_idx):
            if batch_idx == 1:
                handler = signal.getsignal(signal.SIGTERM)
                seen["type"] = type(handler).__name__
                seen["handlers"] = list(getattr(handler, "signal_handlers", []))

    _trainer(ProbeLogger(experiment="e1", name="shape"), tmp_path, max_epochs=1).fit(Look(), _loader())
    assert seen["type"] == "_HandlersCompose", seen
    assert seen["handlers"][0] is preempt._on_sigterm, seen  # moved to the front
    assert len(seen["handlers"]) >= 2, seen  # Lightning's notifier is still there


_FORK_SCRIPT = textwrap.dedent(
    """
    import sys
    import torch
    from torch.utils.data import DataLoader, TensorDataset
    from lightning.pytorch import LightningModule, Trainer
    from probe.integrations.lightning import ProbeLogger

    class Tiny(LightningModule):
        def __init__(self, fail):
            super().__init__()
            self.fail = fail
            self.layer = torch.nn.Linear(4, 1)
        def training_step(self, batch, batch_idx):
            if self.fail and self.global_step == 2:
                raise RuntimeError("boom")
            x, y = batch
            loss = torch.nn.functional.mse_loss(self.layer(x), y)
            self.log("train_loss", loss, on_step=True, on_epoch=False)
            return loss
        def configure_optimizers(self):
            return torch.optim.SGD(self.parameters(), lr=0.1)

    g = torch.Generator().manual_seed(0)
    data = TensorDataset(torch.randn(16, 4, generator=g), torch.randn(16, 1, generator=g))
    trainer = Trainer(
        max_epochs=2, accelerator="cpu", devices=2, strategy="ddp_fork",
        logger=ProbeLogger(experiment="e1", name="fork"), log_every_n_steps=1,
        enable_progress_bar=False, enable_model_summary=False,
        enable_checkpointing=False, default_root_dir=sys.argv[1],
    )
    trainer.fit(Tiny(sys.argv[2] == "fail"), DataLoader(data, batch_size=4))
    """
)


def _run_forked(app, tmp_path, mode: str) -> subprocess.CompletedProcess:
    app.seed_experiment("e1")
    if mode == "fail":
        # Hold rank 0's closing PATCH, so the SIGTERM torch sends it the moment
        # rank 1 is gone lands INSIDE the close, every time, not one run in six.
        answer = app.handler

        def slow_close(request):
            if request.method == "PATCH" and b'"status"' in request.content:
                time.sleep(2)
            return answer(request)

        app.handler = slow_close
    script = tmp_path / "fork_fit.py"
    script.write_text(_FORK_SCRIPT)
    with serve(app) as url:
        proc = subprocess.Popen(
            [sys.executable, str(script), str(tmp_path), mode],
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
            pytest.fail(f"ddp_fork hung; last stderr:\n{stderr[-4000:]}")
    if os.environ.get("LANEI_DEBUG"):
        with open(os.environ["LANEI_DEBUG"], "w") as f:
            f.write(stderr)
    return subprocess.CompletedProcess(proc.args, proc.returncode, "", stderr)


def test_ddp_fork_closes_the_run_its_worker_opened(app, tmp_path):
    """Review MED3: ddp_fork (and ddp_notebook, Jupyter's default with >1
    device) run rank 0 in a FORKED worker, which exits through os._exit: no
    exit hook ran, the run stayed `running`, and the reaper called it
    `crashed` 15 minutes later, with a crash email."""
    result = _run_forked(app, tmp_path, "ok")
    assert result.returncode == 0, result.stderr[-4000:]
    row = _only_run(app)
    assert row["status"] == "completed"
    assert _points(app, row["id"], "train_loss") == list(range(4))


def test_ddp_fork_closes_a_failed_workers_run_failed(app, tmp_path):
    """Both ranks raise at step 2; torch's worker wrapper turns it into
    sys.exit(1) inside the forked worker, and Lightning's own `finalize`
    ("failed") runs in the PARENT, whose logger holds no run. Rank 1 exits
    first, so torch SIGTERMs rank 0 mid-close, and Lightning's SIGTERM handler
    broadcasts to the dead rank: gloo's error used to abort the close."""
    result = _run_forked(app, tmp_path, "fail")
    assert result.returncode != 0
    assert "Received SIGTERM" in result.stderr  # the race this test exists for
    assert _only_run(app)["status"] == "failed", result.stderr[-4000:]


# -- forked / spawned workers: how the run ends (review 2 of #2029) -----------------
_SIGNAL_SCRIPT = textwrap.dedent(
    """
    import sys, time
    import torch
    from torch.utils.data import DataLoader, TensorDataset
    from lightning.pytorch import LightningModule, Trainer
    from probe.integrations.lightning import ProbeLogger

    class Tiny(LightningModule):
        def __init__(self, slow):
            super().__init__()
            self.slow = slow
            self.layer = torch.nn.Linear(4, 1)
        def training_step(self, batch, batch_idx):
            if self.slow:
                time.sleep(0.3)
            x, y = batch
            loss = torch.nn.functional.mse_loss(self.layer(x), y)
            self.log("train_loss", loss, on_step=True, on_epoch=False)
            return loss
        def configure_optimizers(self):
            return torch.optim.SGD(self.parameters(), lr=0.1)

    def main():
        root, strategy, mode = sys.argv[1:4]
        g = torch.Generator().manual_seed(0)
        data = TensorDataset(torch.randn(16, 4, generator=g), torch.randn(16, 1, generator=g))
        trainer = Trainer(
            max_epochs=(20 if mode == "slow" else 2), accelerator="cpu", devices=2,
            strategy=strategy, logger=ProbeLogger(experiment="e1", name=strategy),
            log_every_n_steps=1, enable_progress_bar=False, enable_model_summary=False,
            enable_checkpointing=False, default_root_dir=root,
        )
        trainer.fit(Tiny(mode == "slow"), DataLoader(data, batch_size=4))

    if __name__ == "__main__":  # ddp_spawn imports this file again in each worker
        main()
    """
)


def _run_signalled(app, tmp_path, strategy: str, sig) -> tuple[int, str]:
    """The two-worker job in its own session. Once rank 0 has logged three
    steps, `sig` goes to the whole group, as a terminal's Ctrl-C (or a
    scheduler's SIGTERM) does; None lets it finish."""
    app.seed_experiment("e1")
    script = tmp_path / "signal_fit.py"
    script.write_text(_SIGNAL_SCRIPT)
    with serve(app) as url:
        proc = subprocess.Popen(
            [sys.executable, str(script), str(tmp_path), strategy, "ok" if sig is None else "slow"],
            env=child_env(url, PROBE_HW="0", PROBE_HEARTBEAT_SECONDS="0", OMP_NUM_THREADS="1"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            if sig is not None:
                deadline = time.monotonic() + 120
                while sum(len(v) for v in app.metric_points_posted.values()) < 3:
                    if time.monotonic() > deadline or proc.poll() is not None:
                        break
                    time.sleep(0.1)
                os.killpg(proc.pid, sig)
            _, stderr = proc.communicate(timeout=180)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            _, stderr = proc.communicate()
            pytest.fail(f"{strategy} hung; last stderr:\n{stderr[-4000:]}")
    return proc.returncode, stderr


@pytest.mark.parametrize(
    "strategy, sig, status",
    [
        ("ddp_fork", signal.SIGINT, "canceled"),
        ("ddp_fork", signal.SIGTERM, "failed"),
        ("ddp_spawn", signal.SIGINT, "canceled"),
        ("ddp_spawn", signal.SIGTERM, "failed"),
        ("ddp_spawn", None, "completed"),  # the control: nothing sent
    ],
    ids=["fork-ctrl-c", "fork-sigterm", "spawn-ctrl-c", "spawn-sigterm", "spawn-no-signal"],
)
def test_a_workers_run_closes_with_how_the_job_was_stopped(app, tmp_path, strategy, sig, status):
    """Review 2 MED-A of #2029: all four closed `completed`. torch's worker
    wrapper swallows KeyboardInterrupt, SIGTERMException carries no exit code,
    and Lightning's finalize("failed") runs in the parent, whose logger holds
    no run. torchrun already closed them `canceled` / `failed`; these match it.
    Under SIGTERM the parent dies too, and its workers get torch's death signal,
    SIGINT: that must read `failed`, never `canceled`."""
    _, stderr = _run_signalled(app, tmp_path, strategy, sig)
    row = _only_run(app)
    assert row["status"] == status, stderr[-4000:]
    assert _points(app, row["id"], "train_loss"), "the worker logged nothing"


_HOLD_SCRIPT = textwrap.dedent(
    """
    import json, os, signal, sys, time
    import probe.integrations.lightning as L
    from probe.sdk import fluent

    name, out, hold, close_seconds = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    L.WORKER_HOLD_SECONDS = hold
    marks = {}

    def write():
        with open(out, "w") as f:
            json.dump(marks, f)

    def close():  # the worker's close, with the signal landing in the middle of it
        os.kill(os.getpid(), getattr(signal, name))
        time.sleep(close_seconds)
        marks["close_finished"] = True
        write()

    fluent._finish_at_exit = close
    L._close_at_worker_exit(None)
    marks["signal_swallowed"] = True
    write()
    """
)


def _hold(tmp_path, name: str, *, hold: float, close_seconds: float) -> tuple[int | None, dict, float]:
    script = tmp_path / "hold.py"
    script.write_text(_HOLD_SCRIPT)
    out = tmp_path / "marks.json"
    started = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, str(script), name, str(out), str(hold), str(close_seconds)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        returncode = proc.returncode
    except subprocess.TimeoutExpired:
        returncode = None
    marks = json.loads(out.read_text()) if out.exists() else {}
    return returncode, marks, time.monotonic() - started


@pytest.mark.parametrize("name, killed_by", [("SIGINT", -signal.SIGINT), ("SIGTERM", -signal.SIGTERM)])
def test_a_signal_during_the_workers_close_waits_for_it_then_arrives(tmp_path, name, killed_by):
    """Review 2 MED-A: under ddp_spawn + SIGTERM the parent dies, and torch's
    death signal (SIGINT) reached the worker MID-CLOSE: its KeyboardInterrupt
    cut the close short and dropped a queued write. Both signals are now held
    until the close is done, then delivered to the handler they were meant for
    (Python's SIGINT raises KeyboardInterrupt, and an uncaught one exits by SIGINT)."""
    returncode, marks, _ = _hold(tmp_path, name, hold=25.0, close_seconds=0.5)
    assert marks == {"close_finished": True}
    assert returncode == killed_by


def test_a_close_that_hangs_holds_a_sigterm_only_so_long(tmp_path):
    """Review 2 LOW 7: the hold had no timer, so a hung close made the worker
    deaf to SIGTERM until torch's SIGKILL. Past WORKER_HOLD_SECONDS the signal
    is delivered, close finished or not."""
    returncode, marks, elapsed = _hold(tmp_path, "SIGTERM", hold=1.0, close_seconds=45.0)
    assert returncode == -signal.SIGTERM
    assert marks == {} and elapsed < 30


def test_every_held_signal_reaches_its_handler_even_when_one_raises():
    calls = []

    def on_term(signum, frame):
        calls.append("term")

    def on_int(signum, frame):
        calls.append("int")
        raise KeyboardInterrupt

    old_term, old_int = signal.signal(signal.SIGTERM, on_term), signal.signal(signal.SIGINT, on_int)
    try:
        with pytest.raises(KeyboardInterrupt):
            with lightning_logger._signals_held((signal.SIGTERM, signal.SIGINT), 30.0):
                signal.raise_signal(signal.SIGINT)
                signal.raise_signal(signal.SIGTERM)
                assert calls == []
        assert calls == ["int", "term"]
        assert signal.getsignal(signal.SIGTERM) is on_term
        assert signal.getsignal(signal.SIGINT) is on_int
    finally:
        signal.signal(signal.SIGTERM, old_term)
        signal.signal(signal.SIGINT, old_int)


def test_a_handler_set_outside_python_is_never_taken_over(monkeypatch):
    """Review 2 LOW 7: `signal.signal` returns None for a handler not set from
    Python; the hold read that as "nothing to restore" and left its own lambda
    installed for good, swallowing every later SIGTERM."""
    real = signal.getsignal
    before = real(signal.SIGTERM)
    monkeypatch.setattr(signal, "getsignal", lambda signum: None if signum == signal.SIGTERM else real(signum))
    with lightning_logger._signals_held((signal.SIGTERM,), 30.0):
        assert real(signal.SIGTERM) is before
    assert real(signal.SIGTERM) is before


@pytest.mark.parametrize(
    "requested, applied", [(None, "20.0"), ("600", "20.0"), ("nonsense", "20.0"), ("5", "5")]
)
def test_a_workers_close_fits_inside_torchs_grace(monkeypatch, requested, applied):
    """Review 2 LOW 7: set with setdefault, a PROBE_FINISH_TIMEOUT_SEC above
    30 s won, and torch's SIGKILL cut the close off. A smaller one stands."""
    # setenv first, always: it records the variable's state before the test,
    # so the cap's own os.environ write is undone afterwards. A delenv of an
    # absent variable records nothing, and "20.0" leaked into every later test
    # in the worker (tests/test_outbox_cli.py's paused `run end` then closed
    # its run after 20 s instead of refusing).
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", requested or "")
    if requested is None:
        monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC")
    seen = []
    monkeypatch.setattr(fluent, "_finish_at_exit", lambda: seen.append(os.environ["PROBE_FINISH_TIMEOUT_SEC"]))
    lightning_logger._close_at_worker_exit(None)
    assert seen == [applied]


@pytest.fixture
def worker_sigint(monkeypatch):
    """The handler `_chain_worker_sigint` chains, over Python's default one."""
    monkeypatch.setattr(lightning_logger, "_SIGINT_CHAINED_PID", None)
    signal.signal(signal.SIGINT, signal.default_int_handler)
    noted = []
    monkeypatch.setattr(fluent, "note_exit", lambda status, exc=None: noted.append(status))
    return noted


def test_ctrl_c_in_a_worker_is_noted_canceled_then_raised_as_before(worker_sigint):
    lightning_logger._chain_worker_sigint()
    with pytest.raises(KeyboardInterrupt):
        signal.raise_signal(signal.SIGINT)
    assert worker_sigint == ["canceled"]


def test_the_death_signal_of_a_killed_parent_is_noted_failed(worker_sigint, monkeypatch):
    """torch arms PR_SET_PDEATHSIG = SIGINT: after the parent is gone a SIGINT
    is its death (SIGTERM, SIGKILL, the OOM killer), not a person's Ctrl-C."""
    lightning_logger._chain_worker_sigint()
    monkeypatch.setattr(os, "getppid", lambda: 1)
    with pytest.raises(KeyboardInterrupt):
        signal.raise_signal(signal.SIGINT)
    assert worker_sigint == ["failed"]


def test_a_process_forked_from_the_worker_notes_nothing(worker_sigint, monkeypatch):
    lightning_logger._chain_worker_sigint()
    pid = os.getpid()
    monkeypatch.setattr(os, "getpid", lambda: pid + 1)
    with pytest.raises(KeyboardInterrupt):
        signal.raise_signal(signal.SIGINT)
    assert worker_sigint == []


def test_an_ignored_sigint_is_left_alone(worker_sigint):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    lightning_logger._chain_worker_sigint()
    assert signal.getsignal(signal.SIGINT) is signal.SIG_IGN


# -- runs two Trainers share (review 2 of #2029) -----------------------------------
def test_a_second_trainer_on_the_scripts_run_is_told_it_shares_it(app, wired, tmp_path):
    """Review 2 MED-B: the server keeps the first point per step (ON CONFLICT
    DO NOTHING), so Trainer 2's curve was lost with no word. Only the second
    adoption warns, and it points at the line that started it (LOW 8)."""
    run = probe.init(experiment="e1", name="mine")
    for i in range(2):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            _trainer(ProbeLogger(), tmp_path / str(i)).fit(Tiny(), _loader())
        shared = [w for w in caught if "same run an earlier ProbeLogger" in str(w.message)]
        assert len(shared) == i
    assert "server keeps the first point" in str(shared[0].message)
    assert "probe.finish()" in str(shared[0].message)
    assert os.path.abspath(shared[0].filename) == os.path.abspath(__file__)
    assert list(app.runs) == [run.id]
    probe.finish()


@pytest.mark.parametrize("another_trainer, status", [(True, "completed"), (False, "failed")])
def test_a_failure_the_loop_caught_is_forgotten_when_the_next_trainer_starts(
    app, wired, tmp_path, another_trainer, status
):
    """Review 2 LOW 2: note_exit is process-wide, and adopting the run never
    cleared it, so one caught failure closed a shared run `failed` though the
    next Trainer ran on. With no next Trainer the failure still stands."""
    run = probe.init(experiment="e1", name="mine")
    with pytest.raises(RuntimeError, match="boom"):
        _trainer(ProbeLogger(), tmp_path / "a").fit(Tiny(fail_at=2), _loader())
    if another_trainer:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _trainer(ProbeLogger(), tmp_path / "b").fit(Tiny(), _loader())
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == status


@pytest.mark.parametrize("failing", [1, 2], ids=["middle-trial", "last-trial"])
def test_under_a_launcher_a_failure_the_loop_caught_leaves_the_verdict_to_it(
    app, wired, tmp_path, monkeypatch, failing
):
    """Review 2 LOW 2: under `probe exec` a trial whose error the sweep caught
    closed the launcher's run `failed`, and `probe exec` exited 0. The
    launcher reads the real exit code; an uncaught error still exits 1."""
    from probe.sdk.run import EXEC_FINALIZES_ENV

    for var in ("RANK", "WORLD_SIZE", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK"):
        monkeypatch.delenv(var, raising=False)
    launcher = make_client(app, tmp_spool=tmp_path / "launcher")
    run = launcher.run(experiment="e1", name="launched", heartbeat=False, capture_outputs=False)
    monkeypatch.setenv("PROBE_RUN_ID", run.id)
    monkeypatch.setenv("PROBE_RUN_EPOCH", str(run.write_epoch))
    monkeypatch.setenv(EXEC_FINALIZES_ENV, run.id)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for i in range(3):
            try:
                _trainer(ProbeLogger(), tmp_path / str(i)).fit(Tiny(fail_at=2 if i == failing else None), _loader())
            except RuntimeError:
                pass
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "running"  # the launcher closes it, from exit 0
    launcher.close()


def test_an_older_logger_still_writing_to_its_closed_run_warns_once(app, wired, tmp_path):
    """Review 2 LOW 6: a newer ProbeLogger closes the older one's trial; the
    older logger, reused, kept writing into that closed run in silence."""
    first = ProbeLogger(experiment="e1", name="a")
    _trainer(first, tmp_path / "a").fit(Tiny(), _loader())
    _trainer(ProbeLogger(experiment="e1", name="b"), tmp_path / "b").fit(Tiny(), _loader())
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert first.version  # reading the id afterwards is no write: the control
        assert not [w for w in caught if "already closed" in str(w.message)]
        first.log_metrics({"late": 1.0}, step=100)
        first.log_metrics({"late": 2.0}, step=101)
    closed = [w for w in caught if "already closed (completed)" in str(w.message)]
    assert len(closed) == 1
    fluent._finish_at_exit()


def test_a_workers_copy_pickled_again_carries_no_token(app, wired, tmp_path):
    """Review 2 LOW 1: the settings a spawned worker's copy holds (a token)
    were written out again whenever that copy was pickled, to a file or not."""
    client = make_client(app, tmp_spool=tmp_path / "own")
    logger = ProbeLogger(experiment="e1", client=client)
    _ = logger.experiment
    multiprocessing.context.set_spawning_popen(object())
    try:
        worker_copy = pickle.loads(pickle.dumps(logger))
    finally:
        multiprocessing.context.set_spawning_popen(None)
    assert worker_copy._client_settings is not None  # what the worker needs
    with pytest.warns(UserWarning, match="client= was pickled"):
        blob = pickle.dumps(worker_copy)
    assert b"ros_pat_deadbeef" not in blob
    assert pickle.loads(blob)._client_settings is None
    probe.finish()
    client.close()


def test_only_a_monitored_callback_marks_a_checkpoint_best(app, wired, tmp_path):
    """Review 2 LOW 4: without a monitor `best_model_path` is just the latest
    save, and every such row said `best`. Each row names its callback."""
    monitored = ModelCheckpoint(monitor="val_loss", save_top_k=1)
    periodic = ModelCheckpoint(every_n_train_steps=3, save_top_k=-1, filename="periodic-{step}")
    _trainer(ProbeLogger(experiment="e1"), tmp_path, callbacks=[monitored, periodic], max_epochs=3).fit(
        Tiny(), _loader(), _loader()
    )
    run_id = _only_run(app)["id"]
    posts = _checkpoint_posts(app, run_id)
    by_callback: dict[str, list[dict]] = {}
    for post in posts:
        by_callback.setdefault(post["meta"]["callback"], []).append(post)
    assert set(by_callback) == {monitored.state_key, periodic.state_key}
    assert by_callback[periodic.state_key] and all("best" not in p["meta"] for p in by_callback[periodic.state_key])
    best = [path for path, row in _stored_checkpoints(app, run_id).items() if row["meta"].get("best")]
    assert best == [os.path.abspath(monitored.best_model_path)]
    probe.finish()


def test_a_folder_checkpoint_is_walked_once_per_save(app, wired, tmp_path, monkeypatch):
    """Review 2 LOW 5: the logger summed the folder, then `log_artifact` summed
    it again (and again on every refresh of its row)."""
    from probe.sdk import hashing

    walks = []
    real = hashing.folder_size
    monkeypatch.setattr(hashing, "folder_size", lambda root: walks.append(root) or real(root))
    _trainer(ProbeLogger(experiment="e1"), tmp_path, callbacks=[ModelCheckpoint(save_last=True)], plugins=[_FolderIO()]).fit(
        Tiny(), _loader()
    )
    saves = {(p["meta"]["local_path"], p["meta"]["step"]) for p in _checkpoint_posts(app, _only_run(app)["id"])}
    assert len(walks) == len(saves) >= 2
    probe.finish()
