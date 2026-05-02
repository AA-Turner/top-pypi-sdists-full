from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import torch


def _load_synthetic_datasets_module():
    module_path = Path(__file__).resolve().parents[1] / "evaluations" / "synthetic_datasets.py"
    spec = importlib.util.spec_from_file_location("cortex_evaluation_synthetic_datasets", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_majority_dataset_uses_seed_for_generation() -> None:
    datasets_module = _load_synthetic_datasets_module()
    ds_a = datasets_module.MajorityDataset(num_samples=32, length=64, seed=7)
    ds_b = datasets_module.MajorityDataset(num_samples=32, length=64, seed=7)

    seqs_a = torch.stack(ds_a._seqs)
    seqs_b = torch.stack(ds_b._seqs)

    assert torch.equal(seqs_a, seqs_b)
    assert torch.equal(ds_a._labels, ds_b._labels)
