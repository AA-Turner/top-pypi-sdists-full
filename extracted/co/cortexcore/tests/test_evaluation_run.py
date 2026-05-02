from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import Dataset


def _load_run_module():
    module_path = Path(__file__).resolve().parents[1] / "evaluations" / "run.py"
    sys.path.insert(0, str(module_path.parent))
    spec = importlib.util.spec_from_file_location("cortex_evaluation_run", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class _ToySequenceDataset(Dataset):
    def __init__(self, seqs: torch.Tensor, labels: torch.Tensor, ids: list[int]) -> None:
        self._seqs = seqs
        self._labels = labels
        self.ids = ids

    def __len__(self) -> int:  # type: ignore[override]
        return int(self._labels.shape[0])

    def __getitem__(self, idx: int):  # type: ignore[override]
        return self._seqs[idx], self._labels[idx]


class _TinyStack(nn.Module):
    def __init__(self, d_hidden: int) -> None:
        super().__init__()
        self.proj = nn.Linear(d_hidden, d_hidden)

    def forward(self, x: torch.Tensor, state=None):
        return torch.tanh(self.proj(x)), state


def _make_toy_task(run_module, *, name: str, offset: float):
    def _splits():
        base = torch.tensor(
            [
                [[0.0], [0.0], [0.0]],
                [[0.1], [0.1], [0.1]],
                [[1.0], [1.0], [1.0]],
                [[1.1], [1.1], [1.1]],
            ],
            dtype=torch.float32,
        )
        train = _ToySequenceDataset(base + offset, torch.tensor([0, 0, 1, 1], dtype=torch.long), ids=[0, 1, 2, 3])
        val = _ToySequenceDataset(base[:2] + offset, torch.tensor([0, 0], dtype=torch.long), ids=[4, 5])
        test = _ToySequenceDataset(base[2:] + offset, torch.tensor([1, 1], dtype=torch.long), ids=[6, 7])
        return train, val, test

    return run_module.TaskSpec(name=name, make_splits=_splits, vocab_size=None, n_classes=2, input_dim=1)


def test_train_continual_reports_forgetting_metrics():
    run_module = _load_run_module()
    task_sequence = run_module.ContinualTaskSpec(
        name="toy_continual",
        tasks=[
            _make_toy_task(run_module, name="toy_a", offset=0.0),
            _make_toy_task(run_module, name="toy_b", offset=0.25),
        ],
        vocab_size=None,
        n_classes=2,
        input_dim=1,
    )

    metrics = run_module.train_continual(
        stack=_TinyStack(d_hidden=8),
        d_hidden=8,
        task=task_sequence,
        device=torch.device("cpu"),
        epochs=1,
        batch_size=2,
        lr=1e-2,
    )

    assert set(metrics) == {"val_acc", "test_acc", "test_loss", "avg_forgetting", "backward_transfer"}
    assert 0.0 <= metrics["val_acc"] <= 1.0
    assert 0.0 <= metrics["test_acc"] <= 1.0
    assert math.isfinite(metrics["test_loss"])
    assert math.isfinite(metrics["avg_forgetting"])
    assert math.isfinite(metrics["backward_transfer"])


def test_train_continual_reports_task_incremental_metrics_when_label_subsets_exist():
    run_module = _load_run_module()
    task_a = _make_toy_task(run_module, name="toy_a", offset=0.0)
    task_b = _make_toy_task(run_module, name="toy_b", offset=0.25)
    task_a.label_subset = (0, 1)
    task_b.label_subset = (0, 1)
    task_sequence = run_module.ContinualTaskSpec(
        name="toy_continual_masked",
        tasks=[task_a, task_b],
        vocab_size=None,
        n_classes=2,
        input_dim=1,
    )

    metrics = run_module.train_continual(
        stack=_TinyStack(d_hidden=8),
        d_hidden=8,
        task=task_sequence,
        device=torch.device("cpu"),
        epochs=1,
        batch_size=2,
        lr=1e-2,
    )

    assert "task_test_acc" in metrics
    assert "task_avg_forgetting" in metrics
    assert "task_backward_transfer" in metrics
    assert 0.0 <= metrics["task_test_acc"] <= 1.0
    assert math.isfinite(metrics["task_avg_forgetting"])
    assert math.isfinite(metrics["task_backward_transfer"])


def test_train_continual_with_replay_runs():
    run_module = _load_run_module()
    task_sequence = run_module.ContinualTaskSpec(
        name="toy_continual_replay",
        tasks=[
            _make_toy_task(run_module, name="toy_a", offset=0.0),
            _make_toy_task(run_module, name="toy_b", offset=0.25),
        ],
        vocab_size=None,
        n_classes=2,
        input_dim=1,
    )

    metrics = run_module.train_continual(
        stack=_TinyStack(d_hidden=8),
        d_hidden=8,
        task=task_sequence,
        device=torch.device("cpu"),
        epochs=1,
        batch_size=2,
        lr=1e-2,
        replay_examples_per_task=2,
    )

    assert "test_acc" in metrics
    assert 0.0 <= metrics["test_acc"] <= 1.0
