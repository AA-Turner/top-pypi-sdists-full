"""Pins the requests HF ProbeCallback, Lightning ProbeLogger and the Miles backend send for a short faked loop."""

# HF and Lightning load over `framework_fakes` (no torch/transformers/lightning); Miles registers
# into a stub BACKEND_REGISTRY and exports its durable queue to a served fake. Writes are
# synchronous (an injected transport, or Miles' fail_open=False client): order is call order.

from __future__ import annotations

import os
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

import pytest

import probe
from tests.conftest import FakeApp, make_client
from tests.safety_net.sdk.framework_fakes import frameworks, miles_registry
from tests.safety_net.sdk.sdk_session import TOKEN, WORKSPACE, close_open_runs
from tests.safety_net.sdk.wire_recording import recording
from tests.served_fake_app import serve
from tests.test_miles_integration import _args as miles_args

#: Environment a run's identity or links read, unset (and restored) around every test.
_AMBIENT = (
    "PROBE_RUN_ID", "MILES_RUN_ID", "RESEARCH_OS_RUN_ID", "PROBE_PARENT_RUN", "PROBE_PARENT_RELATION",
    "SLURM_JOB_ID", "RAY_JOB_ID", "NEBIUS_CLUSTER_ID", "NEBIUS_NODE_GROUP_ID", "NEBIUS_GPU_CLUSTER_ID",
    "KUBERNETES_POD_NAME", "KUBERNETES_NAMESPACE", "PROBE_CHECKPOINTS",
)


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    for name in _AMBIENT:
        monkeypatch.setenv(name, "")  # set first, so the undo also removes what the test sets
        monkeypatch.delenv(name)
    monkeypatch.setenv("PROBE_EPHEMERAL", "0")  # the disk is lasting: no throwaway-checkpoint warning
    close_open_runs()
    yield
    close_open_runs()


@pytest.fixture
def literals(tmp_path) -> dict[str, str]:
    return {str(tmp_path): "<tmp_path>"}


class TrainerState(SimpleNamespace):
    """transformers' TrainerState, as far as the callback reads it (one object, mutated)."""


def _hf_args(out: Path) -> SimpleNamespace:
    settings = {"output_dir": str(out), "learning_rate": 0.01, "hub_token": "<HUB_TOKEN>", "max_steps": 3}
    return SimpleNamespace(
        output_dir=str(out), run_name="hf-run", metric_for_best_model="eval_loss",
        enable_jit_checkpoint=False, to_dict=lambda: dict(settings),
    )


def test_hugging_face_callback_sends_these_requests(monkeypatch, tmp_path, baseline, literals):
    app = FakeApp()
    with frameworks(monkeypatch) as integrations:
        callback = integrations["probe.integrations.huggingface"].ProbeCallback(
            project="hf-net", experiment="hf-exp", question="Does HF log?",
            client=make_client(app, tmp_spool=tmp_path / "outbox"),
        )
        args, control = _hf_args(tmp_path / "out"), SimpleNamespace(should_training_stop=False)
        state = TrainerState(is_world_process_zero=True, is_hyper_param_search=False, global_step=0,
                             max_steps=3, epoch=0.0, best_model_checkpoint=None, log_history=[])
        model = SimpleNamespace(config=SimpleNamespace(to_dict=lambda: {"model_type": "bert", "hidden_size": 8}))
        callback.on_init_end(args, state, control)
        callback.on_train_begin(args, state, control, model=model)
        for step in (1, 2, 3):
            state.global_step, state.epoch = step, step / 3
            callback.on_log(args, state, control, logs={"loss": 1.0 / step, "learning_rate": 0.01})
            callback.on_step_end(args, state, control)
            if step == 2:
                state.log_history.append({"step": 2, "eval_loss": 0.4})
                callback.on_log(args, state, control, logs={"eval_loss": 0.4, "epoch": 0.67})
                checkpoint = tmp_path / "out" / "checkpoint-2"
                checkpoint.mkdir(parents=True)
                (checkpoint / "model.safetensors").write_bytes(b"\0" * 128)
                state.best_model_checkpoint = str(checkpoint)
                callback.on_save(args, state, control)
        callback.on_train_end(args, state, control)
        probe.finish()  # the process's exit closes the run in real use
    baseline("integration_huggingface", recording(app.requests, literals))


class ModelCheckpoint:
    """Lightning's ModelCheckpoint, as far as ProbeLogger reads it after one save."""

    def __init__(self, folder: Path, step: int, score: float) -> None:
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"epoch=0-step={step}.ckpt"
        path.write_bytes(b"\0" * 64)
        self._last_checkpoint_saved, self._last_global_step_saved = str(path), step
        self.monitor, self.save_top_k, self.state_key = "val_loss", 1, "ModelCheckpoint{'monitor': 'val_loss'}"
        self.best_model_path, self.last_model_path = str(path), ""
        self.best_k_models = {str(path): score}


def test_lightning_logger_sends_these_requests(monkeypatch, tmp_path, baseline, literals):
    app = FakeApp()
    with frameworks(monkeypatch) as integrations:
        logger = integrations["probe.integrations.lightning"].ProbeLogger(
            project="pl-net", experiment="pl-exp", question="Does Lightning log?", name="pl-run",
            prefix="fit", client=make_client(app, tmp_spool=tmp_path / "outbox"),
        )
        logger.log_hyperparams(Namespace(lr=0.1, batch_size=4, schedule=sorted))
        for step in (0, 1, 2):
            logger.log_metrics({"train_loss": 1.0 / (step + 1)}, step=step)
        logger.log_metrics({"val_loss": 0.4}, step=2)
        logger.after_save_checkpoint(ModelCheckpoint(tmp_path / "ckpt", step=3, score=0.4))
        logger.finalize("success")
        assert logger.version and logger.experiment is probe.active_run()
        probe.finish()
    baseline("integration_lightning", recording(app.requests, literals))


def test_miles_backend_sends_these_requests(monkeypatch, tmp_path, baseline, literals):
    from probe.connectors.miles import make_per_sample_rollout_log, register

    app = FakeApp()
    registry = miles_registry(monkeypatch)
    monkeypatch.setenv("PROBE_TOKEN", TOKEN)
    monkeypatch.setenv("PROBE_WORKSPACE", WORKSPACE)
    with serve(app) as url:
        args = miles_args(tmp_path, probe_base_url=url, probe_snapshot=False, rollout_batch_size=2,
                          num_rollout=2, n_samples_per_prompt=1)
        register(args)
        backend_class, flag = registry["probe"]
        backend = backend_class()
        backend.init(args, primary=True)
        for step in (1, 2):
            backend.log({"train/step": step, "train/loss": 1.0 / step, "train/lr": 1e-5}, step=step,
                        step_key="train/step")
        hook = make_per_sample_rollout_log({"agent/turns": "metadata.turns"})
        samples = [SimpleNamespace(index=i, group_index=0, reward=float(i), response_length=10 + i,
                                   metadata={"turns": 3 + i}) for i in (0, 1)]
        assert hook(1, args, samples, {}, 0.5) is False
        backend.log({"rollout/step": 1, "rollout/reward_mean": 0.5}, step=1, step_key="rollout/step")
        backend.set_terminal_status("completed")
        backend.finish()
        assert args.probe_capture_status == "queue_drained", args.probe_capture_status
        requests = list(app.requests)
    assert flag == "use_probe" and os.environ.get("PROBE_RUN_ID")
    baseline("integration_miles", recording(requests, {url: "<server>", **literals}))
