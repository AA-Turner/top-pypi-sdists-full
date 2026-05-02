from __future__ import annotations

import importlib
from types import SimpleNamespace

import cortex.utils as utils
import torch


def test_select_backend_honors_force_pytorch(monkeypatch) -> None:
    monkeypatch.setenv("CORTEX_FORCE_PYTORCH", "1")
    forced_utils = importlib.reload(utils)

    def _pytorch_backend():
        return "pytorch"

    def _cuda_backend():
        return "cuda"

    tensor = SimpleNamespace(is_cuda=True, device=torch.device("cuda", 0), dtype=torch.float32)
    backend = forced_utils.select_backend(
        triton_fn=None,
        pytorch_fn=_pytorch_backend,
        tensor=tensor,
        cuda_fn=_cuda_backend,
        allow_cuda=True,
    )

    assert backend is _pytorch_backend

    monkeypatch.delenv("CORTEX_FORCE_PYTORCH")
    importlib.reload(utils)
