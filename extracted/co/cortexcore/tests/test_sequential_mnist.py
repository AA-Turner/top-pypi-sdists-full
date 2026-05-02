from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import torch


def _load_sequential_mnist_module():
    module_path = Path(__file__).resolve().parents[1] / "evaluations" / "sequential_mnist.py"
    spec = importlib.util.spec_from_file_location("cortex_evaluation_sequential_mnist", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fake_mnist():
    train_images = torch.arange(24 * 8, dtype=torch.uint8).view(24, 8)
    train_labels = torch.tensor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3])
    test_images = torch.arange(10 * 8, dtype=torch.uint8).view(10, 8)
    test_labels = torch.tensor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    return train_images, train_labels, test_images, test_labels


def test_sequential_mnist_splits_use_cached_loader(monkeypatch):
    module = _load_sequential_mnist_module()
    monkeypatch.setattr(module, "_load_mnist", lambda cache_dir=None: _fake_mnist())

    train, val, test = module.SequentialMNISTDataset.splits(num_samples=6, seed=3, val_size=3)

    assert len(train) == 6
    assert len(val) == 3
    assert len(test) == 10
    seq, label = train[0]
    assert seq.dtype == torch.long
    assert seq.shape == (8,)
    assert label.dtype == torch.long


def test_permuted_sequential_mnist_applies_fixed_permutation(monkeypatch):
    module = _load_sequential_mnist_module()
    monkeypatch.setattr(module, "_load_mnist", lambda cache_dir=None: _fake_mnist())

    base_train, _, _ = module.SequentialMNISTDataset.splits(num_samples=4, seed=0, val_size=2)
    perm_train, _, _ = module.SequentialMNISTDataset.splits(
        num_samples=4,
        seed=0,
        val_size=2,
        permutation_seed=11,
    )

    assert not torch.equal(base_train[0][0], perm_train[0][0])
    assert sorted(base_train[0][0].tolist()) == sorted(perm_train[0][0].tolist())


def test_delayed_sequential_mnist_appends_delay_tokens(monkeypatch):
    module = _load_sequential_mnist_module()
    monkeypatch.setattr(module, "_load_mnist", lambda cache_dir=None: _fake_mnist())

    train, _, _ = module.SequentialMNISTDataset.splits(num_samples=4, seed=0, val_size=2, delay_steps=3)
    seq, _ = train[0]

    assert seq.shape == (11,)
    assert seq[-3:].tolist() == [256, 256, 256]


def test_split_mnist_task_sequence_filters_class_pairs(monkeypatch):
    module = _load_sequential_mnist_module()
    monkeypatch.setattr(module, "_load_mnist", lambda cache_dir=None: _fake_mnist())

    tasks = module.split_mnist_task_sequence(num_samples=2, seed=1, val_size=1)

    assert len(tasks) == 5
    train, _, test = tasks[0]
    train_labels = {int(train[idx][1]) for idx in range(len(train))}
    test_labels = {int(test[idx][1]) for idx in range(len(test))}
    assert train_labels <= {0, 1}
    assert test_labels <= {0, 1}


def test_permuted_mnist_task_sequence_uses_distinct_task_permutations(monkeypatch):
    module = _load_sequential_mnist_module()
    monkeypatch.setattr(module, "_load_mnist", lambda cache_dir=None: _fake_mnist())

    tasks = module.permuted_mnist_task_sequence(num_samples=3, seed=5, num_tasks=2, val_size=2)

    first_train, _, _ = tasks[0]
    second_train, _, _ = tasks[1]
    assert not torch.equal(first_train[0][0], second_train[0][0])
