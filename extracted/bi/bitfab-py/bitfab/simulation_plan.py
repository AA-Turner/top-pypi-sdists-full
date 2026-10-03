from __future__ import annotations

import os
import threading
import time
import weakref
from collections import OrderedDict
from collections.abc import Callable
from typing import Any, Protocol

from bitfab.span_origin import recorded_by_framework
from bitfab.warn_once import warn_once

DISABLE_ENV = "BITFAB_DISABLE_SIM_PLAN"
REFRESH_SECONDS = 60.0
RETRY_SECONDS = 10.0
READ_TIMEOUT_SECONDS = 5.0
FIRST_READ_WAIT_SECONDS = READ_TIMEOUT_SECONDS
MAX_HELD_SPANS = 1000
MAX_UNCOUNTED_TRACES = 1024
NO_API_KEY_FOR_SIM_PLAN = "no API key is set"
CONTENT_OFF_KEY = "content_off_by_simulation_plan"
ROOT_TRACE_FUNCTION_KEY_FIELD = "rootTraceFunctionKey"
DECLARED_IN_CODE_FIELD = "declaredInCode"
CONTENT_KEYS = frozenset(
    {
        "input",
        "input_meta",
        "output",
        "output_meta",
        "input_serialized",
        "output_serialized",
        "replay_recording",
        "prompt",
    }
)

UNTIL_A_READ_SUCCEEDS = (
    "Until a read succeeds, spans other than a trace's root span are sent without "
    "their inputs and outputs, and the read is retried on the next span after "
    f"{RETRY_SECONDS:g}s."
)

ContentOffNames = dict[str, frozenset[str]]
Submit = Callable[[dict[str, Any]], None]
HeldEntry = tuple[dict[str, Any], str | None, Submit]
Discard = Callable[[dict[str, Any]], bool]


class SimulationPlanReader(Protocol):
    def get_simulation_plan(self) -> dict[str, Any]: ...


def plan_wait_slice(timeout: float) -> float:
    return min(READ_TIMEOUT_SECONDS, max(timeout, 0.0) / 2)


def parse_content_off(body: Any) -> ContentOffNames | None:
    if not isinstance(body, dict):
        return None
    nodes = body.get("nodes")
    if not isinstance(nodes, list):
        return None
    names: dict[str, set[str]] = {}
    for node in nodes:
        if not isinstance(node, dict):
            continue
        key = node.get("traceFunctionKey")
        name = node.get("name")
        capture = node.get("captureContent")
        if (
            not isinstance(key, str)
            or not isinstance(name, str)
            or not isinstance(capture, bool)
        ):
            continue
        if not capture:
            names.setdefault(key, set()).add(name)
    return {key: frozenset(value) for key, value in names.items()}


def _span_data_of(payload: dict[str, Any]) -> dict[str, Any] | None:
    raw_span = payload.get("rawSpan")
    if not isinstance(raw_span, dict):
        return None
    span_data = raw_span.get("span_data")
    return span_data if isinstance(span_data, dict) else None


def trace_id_of(payload: dict[str, Any]) -> str | None:
    trace_id = payload.get("traceId")
    if isinstance(trace_id, str):
        return trace_id
    identifier = payload.get("id")
    return identifier if isinstance(identifier, str) else None


def span_name_of(payload: dict[str, Any]) -> str | None:
    span_data = _span_data_of(payload)
    if span_data is None:
        return None
    name = span_data.get("name")
    return name if isinstance(name, str) else None


def has_parent(payload: dict[str, Any]) -> bool:
    raw_span = payload.get("rawSpan")
    return isinstance(raw_span, dict) and raw_span.get("parent_id") is not None


def declared_in_code(payload: dict[str, Any]) -> bool:
    return payload.get(DECLARED_IN_CODE_FIELD) is True


def has_error(payload: dict[str, Any]) -> bool:
    span_data = _span_data_of(payload)
    return span_data is not None and span_data.get("error") is not None


def strip_content(payload: dict[str, Any]) -> dict[str, Any]:
    raw_span = payload.get("rawSpan")
    span_data = _span_data_of(payload)
    if not isinstance(raw_span, dict) or span_data is None:
        return payload
    kept = {key: value for key, value in span_data.items() if key not in CONTENT_KEYS}
    kept[CONTENT_OFF_KEY] = True
    return {**payload, "rawSpan": {**raw_span, "span_data": kept}}


def _missing_plan_endpoint(error: BaseException) -> bool:
    return getattr(getattr(error, "response", None), "status_code", None) == 404


_live_plans: weakref.WeakSet[SimulationPlan] = weakref.WeakSet()
_live_plans_lock = threading.Lock()


class SimulationPlan:
    def __init__(
        self,
        http_client: SimulationPlanReader,
        enabled: bool = True,
        on_discard: Discard | None = None,
    ) -> None:
        self._http_client = http_client
        self._enabled = enabled
        self._on_discard = on_discard
        self._uncounted: OrderedDict[str, int] = OrderedDict()
        self._lock = threading.Lock()
        self._content_off: ContentOffNames | None = None
        self._refresh_after = 0.0
        self._thread: threading.Thread | None = None
        self._held: list[HeldEntry] = []
        self._draining = False
        self._draining_trace_ids: set[str] = set()
        self._stop = threading.Event()
        self._first_read_finished = threading.Event()
        self._first_read_deadline: float | None = None
        with _live_plans_lock:
            _live_plans.add(self)

    def disabled(self) -> bool:
        return not self._enabled or os.environ.get(DISABLE_ENV, "").strip() != ""

    @property
    def loaded(self) -> bool:
        return self._content_off is not None

    def unreadable(self) -> bool:
        return (
            self._content_off is None
            and self._first_read_finished.is_set()
            and not self.disabled()
        )

    def refresh(self) -> None:
        if self._stop.is_set() or self.disabled():
            return
        with self._lock:
            if self._thread is not None or time.monotonic() < self._refresh_after:
                return
            self._start_reader(0.0)

    def _start_reader(self, delay: float) -> None:
        thread = threading.Thread(
            target=self._read_until_loaded,
            args=(delay,),
            name="bitfab-sim-plan",
            daemon=True,
        )
        try:
            thread.start()
        except RuntimeError:
            self._refresh_after = time.monotonic() + RETRY_SECONDS
            self._first_read_finished.set()
            return
        self._thread = thread

    def wait(self, timeout: float) -> None:
        with self._lock:
            thread = self._thread
        if thread is not None:
            thread.join(max(timeout, 0.0))

    def awaiting_first_read(self) -> bool:
        deadline = self._first_read_deadline
        return (
            self._thread is not None
            and not self._first_read_finished.is_set()
            and not self._stop.is_set()
            and not self.disabled()
            and (deadline is None or time.monotonic() < deadline)
        )

    def wait_for_first_read(self) -> None:
        if not self.awaiting_first_read():
            return
        with self._lock:
            if self._first_read_deadline is None:
                self._first_read_deadline = time.monotonic() + FIRST_READ_WAIT_SECONDS
            remaining = self._first_read_deadline - time.monotonic()
        if remaining > 0:
            self._first_read_finished.wait(remaining)

    def _read_once(self) -> ContentOffNames | None:
        suffix = "" if self.loaded else f" {UNTIL_A_READ_SUCCEEDS}"
        try:
            body = self._http_client.get_simulation_plan()
        except Exception as error:
            if _missing_plan_endpoint(error):
                return {}
            warn_once(
                "sim-plan-unavailable",
                f"could not read the sim plan: {error}.{suffix}",
            )
            return None
        parsed = parse_content_off(body)
        if parsed is None:
            warn_once(
                "sim-plan-unreadable",
                f"the sim plan response was not understood.{suffix}",
            )
        return parsed

    def _read_until_loaded(self, delay: float = 0.0) -> None:
        if delay > 0 and self._stop.wait(delay):
            with self._lock:
                self._thread = None
                self._first_read_finished.set()
            return
        skip = self._stop.is_set() or self.disabled()
        parsed = None if skip else self._read_once()
        with self._lock:
            if parsed is not None:
                self._content_off = parsed
                self._refresh_after = time.monotonic() + REFRESH_SECONDS
            else:
                self._refresh_after = time.monotonic() + RETRY_SECONDS
            held, self._held = self._held, []
            self._draining = bool(held)
            self._draining_trace_ids = {
                trace_id
                for payload, key, _ in held
                if key is not None and (trace_id := trace_id_of(payload)) is not None
            }
            self._first_read_finished.set()
        try:
            while held:
                for payload, key, submit in held:
                    self._submit(payload, key, submit)
                with self._lock:
                    held, self._held = self._held, []
        finally:
            with self._lock:
                self._draining = False
                self._draining_trace_ids.clear()
                self._thread = None

    def send(
        self, payload: dict[str, Any], trace_function_key: str | None, submit: Submit
    ) -> None:
        self.refresh()
        if (
            self.disabled()
            or trace_function_key is None
            or span_name_of(payload) is None
            or recorded_by_framework(payload)
        ):
            submit(payload)
            return
        with self._lock:
            holding = self._holds_new_spans()
            overflow = (
                self._hold((payload, trace_function_key, submit)) if holding else []
            )
        for entry in overflow:
            self._submit(*entry)
        if not holding:
            self._submit(payload, trace_function_key, submit)

    def send_trace(self, payload: dict[str, Any], submit: Submit) -> None:
        self.refresh()
        if self._stop.is_set() or self.disabled():
            submit(payload)
            return
        with self._lock:
            holding = self._holds_span_of_trace(trace_id_of(payload))
            overflow = self._hold((payload, None, submit)) if holding else []
        for entry in overflow:
            self._submit(*entry)
        if not holding:
            submit(payload)

    def _holds_new_spans(self) -> bool:
        return (
            self._content_off is None
            and not self._first_read_finished.is_set()
            and not self._stop.is_set()
        )

    def _holds_span_of_trace(self, trace_id: str | None) -> bool:
        if trace_id is None:
            return False
        return trace_id in self._draining_trace_ids or any(
            key is not None and trace_id_of(payload) == trace_id
            for payload, key, _ in self._held
        )

    def _hold(self, entry: HeldEntry) -> list[HeldEntry]:
        self._held.append(entry)
        overflow: list[HeldEntry] = []
        while len(self._held) > MAX_HELD_SPANS:
            overflow.append(self._held.pop(0))
        if (
            self._thread is None
            and self._content_off is None
            and not self._stop.is_set()
            and not self.disabled()
        ):
            self._start_reader(max(0.0, self._refresh_after - time.monotonic()))
        return overflow

    def _submit(
        self, payload: dict[str, Any], trace_function_key: str | None, submit: Submit
    ) -> None:
        try:
            if trace_function_key is None:
                submit(self._counted(payload))
            elif self._discards(payload, trace_function_key):
                self._discard(payload)
            else:
                submit(self._prepared(payload, trace_function_key))
        except Exception as error:
            warn_once(
                "sim-plan-held-span-dropped",
                f"a span held for the sim plan was dropped when released: {error}",
            )

    def _discards(self, payload: dict[str, Any], trace_function_key: str) -> bool:
        name = span_name_of(payload)
        return (
            name is not None
            and self._content_off is not None
            and not self.disabled()
            and has_parent(payload)
            and not has_error(payload)
            and not recorded_by_framework(payload)
            and not declared_in_code(payload)
            and self.content_off(trace_function_key, name)
        )

    def _discard(self, payload: dict[str, Any]) -> None:
        if self._on_discard is not None and self._on_discard(payload):
            return
        trace_id = trace_id_of(payload)
        if trace_id is None:
            return
        with self._lock:
            self._uncounted[trace_id] = self._uncounted.get(trace_id, 0) + 1
            self._uncounted.move_to_end(trace_id)
            while len(self._uncounted) > MAX_UNCOUNTED_TRACES:
                self._uncounted.popitem(last=False)

    def _counted(self, payload: dict[str, Any]) -> dict[str, Any]:
        trace_id = trace_id_of(payload)
        expected = payload.get("expectedSpanCount")
        if trace_id is None or not isinstance(expected, int):
            return payload
        with self._lock:
            uncounted = self._uncounted.pop(trace_id, 0)
        if uncounted == 0:
            return payload
        return {**payload, "expectedSpanCount": max(expected - uncounted, 0)}

    def _prepared(
        self, payload: dict[str, Any], trace_function_key: str
    ) -> dict[str, Any]:
        if (
            self.disabled()
            or recorded_by_framework(payload)
            or declared_in_code(payload)
        ):
            return payload
        if self._content_off is not None:
            return self.apply(payload, trace_function_key)
        if not has_parent(payload):
            return payload
        warn_once(
            "sim-plan-unreadable-content-removed",
            "spans are being sent without their inputs and outputs because the sim "
            "plan could not be read; a later successful read restores them.",
        )
        return strip_content(payload)

    def release(self, timeout: float) -> bool:
        self.refresh()
        with self._lock:
            holds_records = bool(self._held) or self._draining
        if holds_records:
            self.wait(timeout)
        with self._lock:
            return not self._held and not self._draining

    def stop(self) -> None:
        self._stop.set()
        with self._lock:
            held, self._held = self._held, []
            self._first_read_finished.set()
        for payload, key, submit in held:
            self._submit(payload, key, submit)

    def content_off(self, trace_function_key: str, span_name: str) -> bool:
        names = (self._content_off or {}).get(trace_function_key)
        return names is not None and span_name in names

    def skips_content(self, trace_function_key: str | None, span_name: str) -> bool:
        return (
            trace_function_key is not None
            and not self._stop.is_set()
            and not self.disabled()
            and self.content_off(trace_function_key, span_name)
        )

    def apply(self, payload: dict[str, Any], trace_function_key: str) -> dict[str, Any]:
        if recorded_by_framework(payload) or declared_in_code(payload):
            return payload
        name = span_name_of(payload)
        if name is None or not self.content_off(trace_function_key, name):
            return payload
        return strip_content(payload)


def _reset_after_fork() -> None:
    global _live_plans_lock
    _live_plans_lock = threading.Lock()
    for plan in list(_live_plans):
        plan._lock = threading.Lock()
        plan._thread = None
        plan._held = []
        plan._uncounted = OrderedDict()
        plan._draining = False
        plan._draining_trace_ids = set()
        plan._first_read_finished = threading.Event()
        plan._first_read_deadline = None


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_after_fork)
