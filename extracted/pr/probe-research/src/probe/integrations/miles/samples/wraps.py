"""Where Probe listens inside a Miles worker with no Miles commit: three module-level functions, each
wrapped in this process only, when (and if) its module loads. Each wrapper calls Miles' function first,
unchanged, then records; a Probe failure never reaches Miles.

| Miles function (upstream `bb18e6ab7811`; fork `bcd95a00128a`) | Called | Records |
|---|---|---|
| `backends/training_utils/metrics/train_dump.py:11` `save_debug_train_data`; fork `utils/train_dump_utils.py:9` | after each train step, every rank (`megatron_utils/actor.py:881`; fork :492) | trainer parts, seal, commit |
| `backends/training_utils/weight_update/updater.py:140` `WeightUpdater.update_weights` | each weight sync, every rank | weight versions |
| `dashboard/hooks.py:423` `push_sandbox_reports` | each `report_sandbox` | attempt starts, heartbeats |

The rollout process's live samples (rl-next W36, `../live/`) wrap four more as they load: `utils/http_utils.py` `post`
(a running try's request id), `rollout/inference_rollout/inference_rollout_common.py` (each generate function, and the
two calls that grade), `rollout/generate_utils/openai_endpoint_utils.py` `OpenAIEndpointTracer.create` (an agent
rollout's session), and `rollout/base_types.py` `RolloutFnTrainInput` (the step and weights a try starts under).
"""

from __future__ import annotations

import functools
import importlib.abc
import importlib.util
import logging
import sys
import threading
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

TRAIN_DUMP_MODULES = ("miles.backends.training_utils.metrics.train_dump", "miles.utils.train_dump_utils")
UPDATER_MODULE = "miles.backends.training_utils.weight_update.updater"
DASHBOARD_HOOKS_MODULE = "miles.dashboard.hooks"
HTTP_MODULE = "miles.utils.http_utils"
ROLLOUT_COMMON_MODULE = "miles.rollout.inference_rollout.inference_rollout_common"
ENDPOINT_MODULE = "miles.rollout.generate_utils.openai_endpoint_utils"
BASE_TYPES_MODULE = "miles.rollout.base_types"
_MARK = "__probe_wrapped__"


def wrap_train_dump(module: Any) -> None:
    original = getattr(module, "save_debug_train_data", None)
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    def save_debug_train_data(args, *, rollout_id, rollout_data, **kwargs):
        result = original(args, rollout_id=rollout_id, rollout_data=rollout_data, **kwargs)
        _record("train step", lambda: _get_trainer().on_train_data(args, rollout_id, rollout_data))
        return result

    setattr(save_debug_train_data, _MARK, True)
    module.save_debug_train_data = save_debug_train_data


def wrap_weight_updater(module: Any) -> None:
    updater = getattr(module, "WeightUpdater", None)
    original = getattr(updater, "update_weights", None)
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    def update_weights(self, weight_version: int, *args, **kwargs):
        is_done = original(self, weight_version, *args, **kwargs)
        if is_done:
            _record("weight push", lambda: _get_trainer().on_weights_pushed(getattr(self, "args", None), int(weight_version)))
        return is_done

    setattr(update_weights, _MARK, True)
    updater.update_weights = update_weights


def wrap_sandbox_reports(module: Any) -> None:
    original = getattr(module, "push_sandbox_reports", None)
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    def push_sandbox_reports(reports, *args, **kwargs):
        result = original(reports, *args, **kwargs)
        _record("sandbox report", lambda: _get_sandbox_reports().record(list(reports)))
        return result

    setattr(push_sandbox_reports, _MARK, True)
    module.push_sandbox_reports = push_sandbox_reports


def wrap_http(module: Any) -> None:
    from probe.integrations.miles.live import install_rid_stamp

    install_rid_stamp(module)


def wrap_rollout_common(module: Any) -> None:
    from probe.integrations.miles.live import wrap_rollout_common as wrap

    wrap(module)


def wrap_endpoint(module: Any) -> None:
    from probe.integrations.miles.live import wrap_session_tracer

    wrap_session_tracer(module)


def wrap_base_types(module: Any) -> None:
    from probe.integrations.miles.live import wrap_rollout_inputs

    wrap_rollout_inputs(module)


WRAPS: dict[str, Callable[[Any], None]] = {
    **dict.fromkeys(TRAIN_DUMP_MODULES, wrap_train_dump),
    UPDATER_MODULE: wrap_weight_updater,
    DASHBOARD_HOOKS_MODULE: wrap_sandbox_reports,
    HTTP_MODULE: wrap_http,
    ROLLOUT_COMMON_MODULE: wrap_rollout_common,
    ENDPOINT_MODULE: wrap_endpoint,
    BASE_TYPES_MODULE: wrap_base_types,
}


class _AfterImport(importlib.abc.MetaPathFinder):
    """Runs a module's wrap right after the module first loads in this process."""

    def __init__(self, wraps: dict[str, Callable[[Any], None]]) -> None:
        self._wraps = wraps
        self._busy = threading.local()

    def find_spec(self, fullname, path, target=None):
        wrap = self._wraps.get(fullname)
        if wrap is None or getattr(self._busy, "name", None) == fullname:
            return None
        self._busy.name = fullname
        try:
            spec = importlib.util.find_spec(fullname)
        finally:
            self._busy.name = None
        if spec is None or spec.loader is None or not hasattr(spec.loader, "exec_module"):
            return None
        spec.loader = _WrappingLoader(spec.loader, wrap)
        return spec


class _WrappingLoader(importlib.abc.Loader):
    def __init__(self, inner, wrap: Callable[[Any], None]) -> None:
        self._inner, self._wrap = inner, wrap

    def create_module(self, spec):
        return self._inner.create_module(spec)

    def exec_module(self, module) -> None:
        self._inner.exec_module(module)
        _record("wrap " + module.__name__, lambda: self._wrap(module))


_finder: _AfterImport | None = None


def install_worker_wraps() -> None:
    """Wrap the modules already loaded here, and the rest as they load. Idempotent."""
    global _finder
    for name, wrap in WRAPS.items():
        if (module := sys.modules.get(name)) is not None:
            _record("wrap " + name, lambda module=module, wrap=wrap: wrap(module))
    if _finder is None:
        _finder = _AfterImport(WRAPS)
        sys.meta_path.insert(0, _finder)


_warned: set[str] = set()


def _record(what: str, call: Callable[[], Any]) -> None:
    try:
        call()
    except Exception:  # noqa: BLE001 -- fail open: Miles never sees a Probe error
        if what not in _warned:
            _warned.add(what)
            logger.warning("Probe could not record a Miles %s; Miles continues", what, exc_info=True)


def _get_trainer():
    from probe.integrations.miles.samples.trainer import TRAINER

    return TRAINER


_reports = None


def _get_sandbox_reports():
    global _reports
    if _reports is None:
        from probe.integrations.miles.samples.events import SandboxReports
        from probe.integrations.miles.samples.producers import PROCESS, ROLLOUT

        _reports = SandboxReports(lambda: PROCESS.get_samples(ROLLOUT))
    return _reports
