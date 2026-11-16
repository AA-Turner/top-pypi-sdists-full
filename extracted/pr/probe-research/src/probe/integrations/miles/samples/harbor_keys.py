"""Each step's Harbor keys, handed from the rollout process to the train ranks. A Harbor-backed sample is keyed by its
trial (`metadata["external_key"]`), which Miles' train data never carries (`train_data_conversion.py:497-551`), so the
rollout hook saves `Sample.index -> key` in Ray's cluster store before the step trains and the train ranks read it."""

from __future__ import annotations

import json
import logging
import threading
from collections.abc import Mapping
from typing import Any

logger = logging.getLogger(__name__)

NAMESPACE = "probe-miles"


class RayStore:
    """Ray's cluster key-value store (GCS), one entry per step of this Ray job; does nothing outside a Ray worker."""

    def put(self, step: int, value: bytes) -> None:
        kv, name = _connect(step)
        if kv is not None:
            kv._internal_kv_put(name, value, namespace=NAMESPACE)

    def get(self, step: int) -> bytes | None:
        kv, name = _connect(step)
        return kv._internal_kv_get(name, namespace=NAMESPACE) if kv is not None else None

    def delete(self, step: int) -> None:
        kv, name = _connect(step)
        if kv is not None:
            kv._internal_kv_del(name, namespace=NAMESPACE)


def _connect(step: int) -> tuple[Any, str]:
    try:
        import ray
        from ray.experimental import internal_kv
    except ImportError:
        return None, ""
    if not ray.is_initialized() or not internal_kv._internal_kv_initialized():
        return None, ""
    return internal_kv, f"harbor-keys:{ray.get_runtime_context().get_job_id()}:{step}"


class HarborKeys:
    """The rollout side saves a step's keys; each train rank reads a step once. Fails open: a store error leaves the
    trainer's own `train:` keys (warned once)."""

    def __init__(self, store: Any = None) -> None:
        self.store = store or RayStore()
        self._steps: dict[int, dict[str, str]] = {}
        self._has_warned = False
        self._lock = threading.Lock()

    def save(self, step: int, keys: Mapping[Any, str]) -> None:
        """Merged with what the step already holds (a multi-policy run logs one step per policy)."""
        if keys:
            self._call(lambda: self.store.put(step, json.dumps({**self._read(step), **{
                str(index): key for index, key in keys.items()}}).encode()))

    def fetch_key(self, step: int, index: Any, fallback: str) -> str:
        """The Harbor key of the sample at ``index`` trained at ``step``, else ``fallback``."""
        with self._lock:
            if step not in self._steps:
                read = self._call(lambda: self._read(step))
                if read is None:
                    return fallback  # not cached: the next update reads again
                self._steps = {seen: keys for seen, keys in self._steps.items() if seen >= step - 1}
                self._steps[step] = read
            return self._steps[step].get(str(index), fallback)

    def clear(self, step: int) -> None:
        self._call(lambda: self.store.delete(step))

    def _read(self, step: int) -> dict[str, str]:
        raw = self.store.get(step)
        saved = json.loads(raw) if raw else {}
        return saved if isinstance(saved, dict) else {}

    def _call(self, call: Any) -> Any:
        try:
            return call()
        except Exception:  # noqa: BLE001 -- fail open: Miles never sees a Probe error
            if not self._has_warned:
                self._has_warned = True
                logger.warning("Probe could not hand Harbor keys to the train ranks; Miles continues", exc_info=True)
            return None


HARBOR_KEYS = HarborKeys()
