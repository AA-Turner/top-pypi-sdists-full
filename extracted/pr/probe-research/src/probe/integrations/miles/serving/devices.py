"""An SGLang engine's GPUs on this node, from its own `ServerArgs`, as device lists `GpuRequests` reads: one per DP
group SGLang routes requests to, else one for the whole engine. Mirrors SGLang's own placement
(`data_parallel_controller.py:420-449,700-752`, `engine.py:924-940` at sglang-miles@18a44326)."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

#: `disaggregation_mode` of an engine that serves only part of each request (prefill or decode).
PD_MODES = frozenset({"prefill", "decode"})


@dataclass(frozen=True)
class EngineDevices:
    #: Device lists (`CUDA_VISIBLE_DEVICES` entries, comma-joined), one per DP group when `is_routed`, else one.
    groups: tuple[str, ...]
    #: Each request runs on one DP group, named by its `routed_dp_rank` (DP without DP attention).
    is_routed: bool
    #: Some of a request's GPUs are not read here: other nodes (`nnodes > 1`) or the other half of a PD pair.
    is_partial: bool

    def get_group(self, rank: Any) -> str | None:
        """The device list a request runs on; None for a routed engine's request that names no valid rank."""
        if not self.is_routed:
            return self.groups[0]
        if isinstance(rank, int) and not isinstance(rank, bool) and 0 <= rank < len(self.groups):
            return self.groups[rank]
        return None


def read_engine_devices(server_args: Any, environ: Mapping[str, str] = os.environ) -> EngineDevices:
    tp, pp, dp = (max(int(getattr(server_args, name, 1) or 1), 1) for name in ("tp_size", "pp_size", "dp_size"))
    nnodes = max(int(getattr(server_args, "nnodes", 1) or 1), 1)
    base = int(getattr(server_args, "base_gpu_id", 0) or 0)
    step = max(int(getattr(server_args, "gpu_id_step", 1) or 1), 1)
    is_dp_attention = bool(getattr(server_args, "enable_dp_attention", False)) or int(
        getattr(server_args, "attn_dp_size", 1) or 1) > 1
    is_routed = dp > 1 and not is_dp_attention
    # SGLang's per-node shares (`engine.py:_calculate_rank_ranges`): this process is node 0's HTTP server.
    pp_per_node = max(pp // nnodes, 1)
    tp_per_node = max(tp // max(nnodes // pp, 1), 1)
    ordinals_per_group = [[base + group * tp * pp * step + pp_rank * tp_per_node + tp_rank * step
                           for pp_rank in range(pp_per_node) for tp_rank in range(tp_per_node)]
                          for group in range(dp if is_routed else 1)]  # fmt: skip
    visible = [entry.strip() for entry in environ.get("CUDA_VISIBLE_DEVICES", "").split(",") if entry.strip()]
    groups = tuple(",".join(_to_visible(ordinal, visible) for ordinal in ordinals) for ordinals in ordinals_per_group)
    mode = str(getattr(server_args, "disaggregation_mode", "") or "").lower()
    return EngineDevices(groups=groups, is_routed=is_routed, is_partial=nnodes > 1 or mode in PD_MODES)


def _to_visible(ordinal: int, visible: list[str]) -> str:
    """A CUDA ordinal as the device it names: its `CUDA_VISIBLE_DEVICES` entry, else the physical index."""
    if not visible:
        return str(ordinal)
    if ordinal >= len(visible):
        raise ValueError(f"GPU ordinal {ordinal} is past CUDA_VISIBLE_DEVICES ({len(visible)} devices)")
    return visible[ordinal]
