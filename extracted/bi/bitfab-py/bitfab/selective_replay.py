from __future__ import annotations

import copy
import json
import math
import threading
from collections import Counter, defaultdict
from typing import Any, TypedDict


class ReplayNodeIdentity(TypedDict):
    trace_function_key: str
    span_name: str


class SelectiveReplayOptions(TypedDict):
    """Required subtrees: changed code and unchanged code whose effects are needed."""

    must_run: list[ReplayNodeIdentity]


def wire_options(options: SelectiveReplayOptions) -> dict[str, Any]:
    if (
        type(options) is not dict
        or set(options) != {"must_run"}
        or type(options["must_run"]) is not list
        or not 1 <= len(options["must_run"]) <= 100
        or any(
            type(node) is not dict
            or set(node) != {"trace_function_key", "span_name"}
            or any(
                type(value) is not str or not 1 <= len(value) <= 500
                for value in node.values()
            )
            for node in options["must_run"]
        )
    ):
        raise ValueError(
            "experimental_selective_replay accepts only 1-100 must_run with trace_function_key and span_name; declare replay_reusable on eligible spans."
        )
    return {
        "mustRun": [
            {
                "traceFunctionKey": node["trace_function_key"],
                "spanName": node["span_name"],
            }
            for node in options["must_run"]
        ]
    }


def json_fingerprint(value: Any) -> str | None:
    """Reject lossy runtime values, aliases, cycles, and non-string dict keys."""
    seen: set[int] = set()

    def validate(item: Any) -> None:
        kind = type(item)
        if item is None or kind is bool:
            return
        if kind is str and not item.startswith("<unserializable"):
            return
        # The server's JSON number representation cannot preserve larger ints.
        if kind is int and abs(item) <= 2**53 - 1:
            return
        if kind is float and math.isfinite(item) and not item.is_integer():
            return
        if kind not in (dict, list) or id(item) in seen:
            raise ValueError("Not lossless JSON")
        seen.add(id(item))
        if kind is dict:
            for key, child in item.items():
                if type(key) is not str:
                    raise ValueError("Not a string key")
                if (
                    key.isascii()
                    and key.isdigit()
                    and str(int(key)) == key
                    and int(key) < 2**32 - 1
                ):
                    raise ValueError("JavaScript reorders integer-index object keys")
                validate(child)
        else:
            for child in item:
                validate(child)

    try:
        validate(value)
        return json.dumps(
            value, ensure_ascii=True, separators=(",", ":"), allow_nan=False
        )
    except (ValueError, TypeError, RecursionError):
        return None


def _key(node: dict[str, Any]) -> tuple[str, str]:
    return node["traceFunctionKey"], node["spanName"]


def _identity(node: dict[str, Any]) -> ReplayNodeIdentity:
    return {
        "trace_function_key": node["traceFunctionKey"],
        "span_name": node["spanName"],
    }


class SelectiveReplayRuntime:
    def __init__(self, plan: dict[str, Any], options: SelectiveReplayOptions):
        expected = wire_options(options)
        if (
            not isinstance(plan, dict)
            or plan.get("version") != 4
            or not isinstance(plan.get("nodes"), list)
            or not 1 <= len(plan["nodes"]) <= 500
            or not isinstance(plan.get("assertions"), list)
            or not isinstance(plan.get("unresolvedMustRun"), list)
        ):
            raise ValueError(
                "Server did not return a compatible selective replay plan; update the server or disable experimental_selective_replay."
            )
        if plan.get("options") != expected:
            raise ValueError(
                "Selective replay plan does not match requested must_run nodes."
            )
        self.plan = copy.deepcopy(plan)
        self.required = {_key(node) for node in expected["mustRun"]}
        self.required_scopes: set[str] = set()
        self.nodes: dict[str, dict[str, Any]] = {}
        self.children: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.recordings: dict[str, tuple[str | None, str | None]] = {}
        self.parents: dict[str, str | None] = {}
        self.consumed: dict[str, set[str]] = defaultdict(set)
        self.reached: set[tuple[str, str]] = set()
        self.decisions: list[dict[str, Any]] = []
        self.assertion_names: set[str] = set()
        self.assertion_scopes: set[str] = set()
        self.observed: Counter[str] = Counter()
        self.unresolved_assertions: list[str] = []
        self.failure: RuntimeError | None = None
        self.lock = threading.RLock()
        for node in self.plan["nodes"]:
            if (
                not isinstance(node, dict)
                or not isinstance(node.get("id"), str)
                or node["id"] in self.nodes
                or not isinstance(node.get("traceFunctionKey"), str)
                or not isinstance(node.get("spanName"), str)
                or type(node.get("mustRun")) is not bool
                or type(node.get("reusable")) is not bool
                or "parentId" not in node
                or (
                    node["parentId"] is not None
                    and not isinstance(node["parentId"], str)
                )
            ):
                raise ValueError("Invalid selective replay node.")
            self.nodes[node["id"]] = node
            if node["parentId"] is not None:
                self.children[node["parentId"]].append(node)
            recording = node.get("recording")
            if isinstance(recording, dict) and "output" in recording:
                self.recordings[node["id"]] = (
                    json_fingerprint(
                        [recording.get("input"), recording.get("kwargs", {})]
                    ),
                    json_fingerprint(recording["output"]),
                )
        root = self.nodes.get(plan.get("rootId"))
        if not root or root["parentId"] is not None or not root["mustRun"]:
            raise ValueError("Selective replay requires a live recorded root.")
        ids: set[str] = set()
        whole_trace = False
        for assertion in self.plan["assertions"]:
            if (
                not isinstance(assertion, dict)
                or not isinstance(assertion.get("id"), str)
                or not assertion["id"]
                or assertion["id"] in ids
                or "target" not in assertion
            ):
                raise ValueError("Invalid selective replay assertion requirements.")
            ids.add(assertion["id"])
            target = assertion["target"]
            if target is None:
                whole_trace = True
                continue
            if not isinstance(target, dict) or target.get("kind") not in (
                "output",
                "span",
            ):
                raise ValueError("Invalid selective replay assertion target.")
            if target["kind"] == "span":
                occurrence = target.get("occurrence", "first")
                if (
                    not isinstance(target.get("name"), str)
                    or not target["name"]
                    or not (
                        occurrence in ("first", "last")
                        or (type(occurrence) is int and occurrence >= 0)
                    )
                ):
                    raise ValueError("Invalid selective replay assertion target.")
                self.assertion_names.add(target["name"])
                count = sum(
                    node["spanName"] == target["name"] for node in self.nodes.values()
                )
                if count <= (occurrence if type(occurrence) is int else 0):
                    self.unresolved_assertions.append(assertion["id"])
        self.full_trace = whole_trace or bool(self.unresolved_assertions)
        recorded_keys = {_key(node) for node in self.nodes.values()}
        if self.required - recorded_keys != {
            _key(node) for node in plan["unresolvedMustRun"]
        }:
            raise ValueError("Selective replay plan has incomplete mustRun coverage.")
        for node in self.nodes.values():
            ancestors = {node["id"]}
            required = _key(node) in self.required or bool(plan["unresolvedMustRun"])
            protected = self.full_trace or node["spanName"] in self.assertion_names
            parent_id = node["parentId"]
            while parent_id is not None:
                parent = self.nodes.get(parent_id)
                if (
                    not parent
                    or parent_id in ancestors
                    or (node["mustRun"] and not parent["mustRun"])
                ):
                    raise ValueError("Invalid selective replay ancestry.")
                ancestors.add(parent_id)
                required |= _key(parent) in self.required
                protected |= parent["spanName"] in self.assertion_names
                parent_id = parent["parentId"]
            if plan["rootId"] not in ancestors or (required and not node["mustRun"]):
                raise ValueError("Selective replay plan could hide required code.")
            if protected and not node["mustRun"]:
                raise ValueError("Selective replay plan could hide assertion evidence.")

    def enter(
        self,
        *,
        trace_function_key: str,
        span_name: str,
        span_id: str,
        parent_span_id: str | None,
        inputs: list[Any],
        kwargs: dict[str, Any],
        safety_mock: bool,
        can_reuse_output: bool,
        reuse_allowed: bool,
    ) -> tuple[bool, Any]:
        # Thread-pool children share one replay context; claiming a recording
        # and updating evidence must be atomic across those threads.
        with self.lock:
            return self._enter(
                trace_function_key,
                span_name,
                span_id,
                parent_span_id,
                inputs,
                kwargs,
                safety_mock,
                can_reuse_output,
                reuse_allowed,
            )

    def _enter(
        self,
        trace_function_key: str,
        span_name: str,
        span_id: str,
        parent_span_id: str | None,
        inputs: list[Any],
        kwargs: dict[str, Any],
        safety_mock: bool,
        can_reuse_output: bool,
        reuse_allowed: bool,
    ) -> tuple[bool, Any]:
        key = (trace_function_key, span_name)
        fingerprint = json_fingerprint([inputs, kwargs])
        node = None
        match_reason = "unmatched-call"
        if parent_span_id is None:
            node = self.nodes[self.plan["rootId"]]
        else:
            candidates = [
                candidate
                for candidate in self.children.get(self.parents.get(parent_span_id), [])
                if _key(candidate) == key
                and candidate["id"] not in self.consumed[parent_span_id]
            ]
            exact = [
                candidate
                for candidate in candidates
                if fingerprint is not None
                and self.recordings.get(candidate["id"], (None, None))[0] == fingerprint
            ]
            if len(exact) == 1:
                node = exact[0]
            elif not exact and len(candidates) == 1:
                node = candidates[0]
            if node:
                self.consumed[parent_span_id].add(node["id"])
            elif candidates:
                match_reason = "ambiguous-call"
                self.consumed[parent_span_id].update(
                    candidate["id"] for candidate in candidates
                )
        self.parents[span_id] = node["id"] if node else None
        required = key in self.required or parent_span_id in self.required_scopes
        if required:
            self.required_scopes.add(span_id)
        assertion_required = (
            self.full_trace
            or span_name in self.assertion_names
            or parent_span_id in self.assertion_scopes
        )
        if assertion_required:
            self.assertion_scopes.add(span_id)
        must_run = (
            parent_span_id is None
            or required
            or (node is not None and node["mustRun"])
            or assertion_required
            or bool(self.plan["unresolvedMustRun"])
        )
        recorded_input, recorded_output = (
            self.recordings.get(node["id"], (None, None)) if node else (None, None)
        )
        equal_inputs = fingerprint is not None and fingerprint == recorded_input
        reusable = recorded_output is not None and equal_inputs and can_reuse_output
        if must_run:
            reason = (
                "must-run"
                if required
                else "assertion"
                if assertion_required
                else node.get("reason", "unresolved-must-run")
                if node
                else "unresolved-must-run"
            )
        elif not node:
            reason = match_reason
        elif not equal_inputs:
            reason = "input-drift-or-missing-recording"
        elif not can_reuse_output:
            reason = "unsupported-output-boundary"
        elif not safety_mock and not reuse_allowed:
            reason = "reuse-not-declared"
        else:
            reason = node.get("reason", "not-reusable")
        decision = {
            "trace_function_key": trace_function_key,
            "span_name": span_name,
            "original_span_id": node["id"] if node else None,
        }
        if safety_mock and (must_run or not reusable):
            self.decisions.append(
                {**decision, "action": "blocked", "reason": f"safety-conflict:{reason}"}
            )
            self.failure = RuntimeError(
                f"Selective replay cannot execute or safely reuse safety-mocked node {span_name} ({reason})."
            )
            raise self.failure
        if (
            not must_run
            and reusable
            and (
                safety_mock or (node is not None and node["reusable"] and reuse_allowed)
            )
        ):
            self.decisions.append(
                {
                    **decision,
                    "action": "mock",
                    "reason": "safety-mock" if safety_mock else "unchanged-inputs",
                }
            )
            return True, json.loads(recorded_output)
        self.decisions.append({**decision, "action": "run", "reason": reason})
        self.observed[span_name] += 1
        if key in self.required:
            self.reached.add(key)
        return False, None

    def assert_no_safety_conflict(self) -> None:
        if self.failure is not None:
            raise self.failure

    def report(self) -> dict[str, Any]:
        with self.lock:
            return {
                "decisions": copy.deepcopy(self.decisions),
                "must_run_not_reached": [
                    _identity(node)
                    for node in self.plan["options"]["mustRun"]
                    if _key(node) not in self.reached
                ],
                "unresolved_must_run": [
                    _identity(node) for node in self.plan["unresolvedMustRun"]
                ],
                "assertion_ids": [
                    assertion["id"] for assertion in self.plan["assertions"]
                ],
                "unresolved_assertions": list(self.unresolved_assertions),
                "assertion_targets_not_reached": [
                    assertion["id"]
                    for assertion in self.plan["assertions"]
                    if assertion["target"] is not None
                    and assertion["target"]["kind"] == "span"
                    and self.observed[assertion["target"]["name"]]
                    <= (
                        assertion["target"]["occurrence"]
                        if type(assertion["target"].get("occurrence")) is int
                        else 0
                    )
                ],
            }
