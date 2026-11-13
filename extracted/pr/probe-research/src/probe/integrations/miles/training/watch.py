"""What one Miles `loss_function` call reduces, observed while it runs and never changed: every reducer Miles builds
(the objective's `get_sum_of_sample_mean` and `response_layout`'s own binding, which TIS / RS and the mismatch metrics
use through `layout.reducer`; `PaddedRows`' own `sum_of_sample_mean` / `reducer` on padded logit rows), Miles' own context-parallel ESS sums after its collective ran, and OPSM's keep mask.
Line refs are `radixark/miles@bb18e6ab7811`. Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import contextlib
import functools
import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

RESPONSE_LAYOUT_MODULE = "miles.backends.training_utils.loss.hub.response_layout"
MATH_MODULE = "miles.backends.training_utils.loss.hub.math_utils"
LOSSES_MODULE = "miles.backends.training_utils.loss.hub.losses"


@dataclass
class ReducerCall:
    #: What Miles reduced and its output, detached (no copy: they are only read).
    values: Any
    output: Any
    reducer: Any
    #: `PaddedRows` only: each padded row's sample (padding rows: the sample count), from `map_padded_rows`.
    row_ids: Any = None


@dataclass
class LossCalls:
    """What one `loss_function` call reduced, in order, and what Miles computed beside its reducer."""

    reductions: list[ReducerCall] = field(default_factory=list)
    #: Miles' own context-parallel all-reduced per-sample ESS sums `[samples, 2]` (`math_utils.py:72-73`), copied
    #: after Miles' collective ran: the hook adds none (D15).
    ess_sums: Any = None
    #: Miles' own `compute_opsm_mask` output (`math_utils.py:184-222`): the per-token keep mask.
    opsm_mask: Any = None


class CollectiveCopy:
    """`torch.distributed` as `math_utils` sees it during one ESS call: every call goes to the real module; an
    `all_reduce` keeps a copy of the tensor Miles' own collective produced."""

    def __init__(self, real: Any, calls: LossCalls) -> None:
        self._real, self._calls = real, calls

    def all_reduce(self, tensor: Any, *args: Any, **kwargs: Any) -> Any:
        result = self._real.all_reduce(tensor, *args, **kwargs)
        try:
            self._calls.ess_sums = tensor.detach().clone()
        except Exception:  # noqa: BLE001 -- the ESS goes unrecorded
            pass
        return result

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)


@contextlib.contextmanager
def watch_reductions(objective: Any) -> Iterator[LossCalls]:
    """While the block runs, every reducer Miles builds is observed, Miles' ESS collective copied and OPSM's mask
    kept; each patched name is restored after."""
    calls = LossCalls()
    layout = sys.modules.get(RESPONSE_LAYOUT_MODULE)
    math_module = sys.modules.get(MATH_MODULE)
    losses = sys.modules.get(LOSSES_MODULE)
    padded = getattr(layout, "PaddedRows", None)
    patches: list[tuple[Any, str, Callable[[Any], Any]]] = [
        (objective, "get_sum_of_sample_mean", lambda real: _make_reducer_getter(real, calls)),
        (layout, "get_sum_of_sample_mean", lambda real: _make_reducer_getter(real, calls)),
        (losses, "compute_opsm_mask", lambda real: _make_opsm_watch(real, calls)),
        (padded, "sum_of_sample_mean", lambda real: _make_padded_reduction(real, calls)),
        (padded, "reducer", lambda real: _make_padded_reducer(real, calls)),
    ]
    if math_module is not None:
        patches.append((layout, "compute_ess_ratio_contribution", lambda real: _make_ess_watch(real, math_module, calls)))
    saved: list[tuple[Any, str, Any]] = []
    try:
        for module, name, make in patches:
            real = getattr(module, name, None) if module is not None else None
            if callable(real):
                saved.append((module, name, real))
                setattr(module, name, make(real))
        yield calls
    finally:
        for module, name, real in reversed(saved):
            setattr(module, name, real)


def _make_reducer_getter(real_get: Any, calls: LossCalls) -> Any:
    def get_sum_of_sample_mean(*args: Any, **kwargs: Any) -> Any:
        return _watch_reducer(real_get(*args, **kwargs), calls)

    return get_sum_of_sample_mean


def _watch_reducer(reducer: Any, calls: LossCalls, row_ids: Any = None) -> Any:
    def watch(*values: Any, **options: Any) -> Any:
        output = reducer(*values, **options)
        try:
            if len(values) == 1 and not options:
                calls.reductions.append(ReducerCall(values[0].detach(), output.detach(), reducer, row_ids))
        except Exception:  # noqa: BLE001 -- a shape this hook does not know: that reduction goes unrecorded
            pass
        return output

    return watch


def _make_ess_watch(real_ess: Any, math_module: Any, calls: LossCalls) -> Any:
    def compute_ess_ratio_contribution(*args: Any, **kwargs: Any) -> Any:
        real_dist = math_module.dist
        math_module.dist = CollectiveCopy(real_dist, calls)
        try:
            return real_ess(*args, **kwargs)
        finally:
            math_module.dist = real_dist

    return compute_ess_ratio_contribution


def _make_opsm_watch(real_opsm: Any, calls: LossCalls) -> Any:
    def compute_opsm_mask(*args: Any, **kwargs: Any) -> Any:
        result = real_opsm(*args, **kwargs)
        try:
            calls.opsm_mask = result[0].detach()
        except Exception:  # noqa: BLE001 -- the OPSM clip fraction goes unrecorded
            pass
        return result

    return compute_opsm_mask


def map_padded_rows(layout: Any) -> Any:
    """Each of a `PaddedRows` layout's `[T]` logit rows mapped to its sample (Miles' own `row_index`: the row of every
    response token, in sample order, `response_layout.py:352-385`); a row no response token sits on (prompt, padding)
    maps to the sample count, a bucket the summary drops."""
    import torch

    lengths = torch.as_tensor(list(layout.response_lengths), dtype=torch.long)
    ids = torch.full((int(layout.num_rows),), len(lengths), dtype=torch.long)
    ids[layout.row_index.to("cpu", torch.long)] = torch.repeat_interleave(torch.arange(len(lengths)), lengths)
    return ids.to(layout.device)


def _make_padded_reduction(real: Any, calls: LossCalls) -> Any:
    def reduce_padded_rows(layout: Any, values: Any) -> Any:
        output = real(layout, values)
        try:
            calls.reductions.append(ReducerCall(values.detach(), output.detach(), functools.partial(real, layout),
                                                map_padded_rows(layout)))  # fmt: skip
        except Exception:  # noqa: BLE001 -- that reduction goes unrecorded
            pass
        return output

    return reduce_padded_rows


def _make_padded_reducer(real: Any, calls: LossCalls) -> Any:
    def build_padded_reducer(layout: Any, loss_masks: Any) -> Any:
        built = real(layout, loss_masks)
        try:
            return _watch_reducer(built, calls, map_padded_rows(layout))
        except Exception:  # noqa: BLE001 -- Miles' own reducer, unwatched
            return built

    return build_padded_reducer
