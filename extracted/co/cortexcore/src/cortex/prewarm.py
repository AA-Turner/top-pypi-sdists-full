from __future__ import annotations

from typing import Any


def _policy_uses_axon(policy_architecture: Any) -> tuple[bool, bool]:
    if policy_architecture.__class__.__name__ != "DefaultPolicyConfig":
        return False, False

    uses_axon = False
    uses_srht = False
    for cell in getattr(policy_architecture, "cortex_cells", None) or []:
        if cell.__class__.__name__ != "AxonCellConfig":
            continue
        uses_axon = True
        core = getattr(cell, "core", None)
        if core is not None and bool(getattr(core, "use_srht", False)):
            uses_srht = True
    return uses_axon, uses_srht


def prewarm_policy_kernels(policy_architecture: Any) -> None:
    from cortex.kernels.cuda.agalite.discounted_sum_cuda import prewarm_discounted_sum_cuda  # noqa: PLC0415

    prewarm_discounted_sum_cuda()

    uses_axon, uses_srht = _policy_uses_axon(policy_architecture)
    if uses_axon:
        from cortex.kernels.cuda.rtu.rtu_seq_allin import prewarm_rtu_seq_allin  # noqa: PLC0415

        prewarm_rtu_seq_allin()
    if uses_srht:
        from cortex.kernels.cuda.srht.srht_cuda import prewarm_srht_cuda  # noqa: PLC0415

        prewarm_srht_cuda()


__all__ = ["prewarm_policy_kernels"]
