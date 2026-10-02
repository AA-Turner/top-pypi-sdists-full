"""Run a recorded Python extraction over a fresh native viewport tree — the mobile textual_analyzer."""

import ast
import builtins
import json
import logging
import math
import multiprocessing
import re
import sys
import time
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from decimal import Decimal

import httpx

from testmu_appium import _config, perception
from testmu_appium._errors import (
    DegenerateViewportCaptureError,
    ViewportCaptureError,
    ViewportResultMissError,
    ViewportResultTypeError,
    ViewportScriptCompileError,
    ViewportScriptPolicyError,
    ViewportScriptRuntimeError,
    ViewportScriptTimeoutError,
    ViewportSelectionDriftError,
)
from testmu_appium._helpers import _screen
from testmu_appium._helpers._http import auth, headers
from testmu_appium._step import mark_autohealed

_CONTRACTS = {
    "testmu-appium.element-contract.v1": (
        "index", "parent_index", "depth",
        "role", "cls", "resource_id", "content_desc", "text", "name", "hint",
        "bounds", "center", "enabled", "checked", "selected", "clickable",
    ),
}
#: The one projection contract the binding speaks. Projection is additive-only
#: (fields are added, never renamed or removed), so a recording made against an
#: older field set stays compatible and heal wants the richest current
#: projection — there is no per-record contract to honour.
_CURRENT_CONTRACT = "testmu-appium.element-contract.v1"
_POPULATED_MIN_ROWS = 10
_DEGENERATE_FRACTION_NUMERATOR = 1
_DEGENERATE_FRACTION_DENOMINATOR = 10
_ALLOWED_BUILTIN_NAMES = frozenset({
    "len", "sum", "min", "max", "any", "all", "int", "float", "str",
    "bool", "list", "dict", "tuple", "set", "range", "enumerate", "zip",
    "sorted", "isinstance",
    # The prompts tell the model to raise rather than let an empty match become
    # a confident wrong answer, so the name it needs to do that has to be
    # reachable. Without it every guarded extraction is rejected and the model
    # falls back to recording a constant. Constructing an exception grants no
    # capability the sandbox otherwise withholds.
    "ValueError",
})
_INJECTED_GLOBAL_NAMES = frozenset({"re", "json", "math", "Decimal"})
_SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in _ALLOWED_BUILTIN_NAMES
}
#: How long the sandbox child gets to prove it is alive. Generous next to a
#: fork, which is immediate, and small next to the extraction budget.
_WORKER_START_TIMEOUT_S = 5.0
#: Sticky once a start method proves unusable in this process.
_FORCED_START_METHOD = None
_SELECTION_REQUIRED = (
    "this extraction records no selection, so replay cannot detect locator drift. "
    "Select with tree.where(...) so the predicates are recorded."
)
_CONFIDENCE_THRESHOLD = 0.7
_VIEWPORT_HEAL_SOURCE = "v16-textual-analyzer-viewport"
_DEFAULT_HEAL_TIMEOUT_S = 60.0
_log = logging.getLogger("testmu_appium")


@dataclass
class ViewportHealHit:
    """A regenerated viewport script selected fresh rows and returned a value."""

    value: object
    code: str
    reasoning: str = ""


@dataclass
class ViewportHealNoMatch:
    """The server authoritatively had no usable regeneration for this capture."""

    reason: str
    authoritative: bool = True


@dataclass
class ViewportHealUnresolved:
    """The server returned code, but it did not select a usable fresh value."""

    reason: str
    authoritative: bool = False


@dataclass
class ViewportHealUnavailable:
    """The one permitted recovery request could not be completed."""

    cause: str
    authoritative: bool = False


class _ViewportTree:
    __slots__ = ("_rows", "selection_records")

    def __init__(self, rows):
        self._rows = rows
        self.selection_records = []

    def __iter__(self):
        return iter(self._rows)

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, index):
        return self._rows[index]

    def where(self, **predicates):
        matches = _matching_rows(self._rows, predicates)
        self.selection_records.append({
            "where": dict(predicates),
            "matched": len(matches),
        })
        return matches


def _target_names(node):
    if isinstance(node, ast.Name):
        return {node.id}
    if isinstance(node, (ast.List, ast.Tuple)):
        return set().union(*(_target_names(element) for element in node.elts))
    if isinstance(node, ast.Starred):
        return _target_names(node.value)
    return set()


class _FunctionLocalBindings(ast.NodeVisitor):
    def __init__(self):
        self.names = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.names.add(node.id)

    def visit_ExceptHandler(self, node):
        if node.name is not None:
            self.names.add(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        return None

    def visit_AsyncFunctionDef(self, node):
        return None

    def visit_Lambda(self, node):
        return None

    def visit_ListComp(self, node):
        self._visit_comprehension(node, (node.elt,))

    def visit_SetComp(self, node):
        self._visit_comprehension(node, (node.elt,))

    def visit_GeneratorExp(self, node):
        self._visit_comprehension(node, (node.elt,))

    def visit_DictComp(self, node):
        self._visit_comprehension(node, (node.key, node.value))

    def _visit_comprehension(self, node, values):
        for generator in node.generators:
            self.visit(generator.iter)
            for condition in generator.ifs:
                self.visit(condition)
        for value in values:
            self.visit(value)


class _LoadNameValidator(ast.NodeVisitor):
    def __init__(self, function_locals):
        self._function_names = frozenset(function_locals)
        self._comprehension_scopes = []

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in self._allowed_names:
            raise ViewportScriptPolicyError(
                f"viewport extraction references disallowed name {node.id!r}"
            )

    @property
    def _allowed_names(self):
        names = (
            _ALLOWED_BUILTIN_NAMES
            | _INJECTED_GLOBAL_NAMES
            | {"tree"}
            | self._function_names
        )
        for scope in self._comprehension_scopes:
            names |= scope
        return names

    def visit_ListComp(self, node):
        self._visit_comprehension(node, (node.elt,))

    def visit_SetComp(self, node):
        self._visit_comprehension(node, (node.elt,))

    def visit_GeneratorExp(self, node):
        self._visit_comprehension(node, (node.elt,))

    def visit_DictComp(self, node):
        self._visit_comprehension(node, (node.key, node.value))

    def _visit_comprehension(self, node, values):
        for generator in node.generators:
            self.visit(generator.iter)
            self._comprehension_scopes.append(frozenset(_target_names(generator.target)))
            self.visit(generator.target)
            for condition in generator.ifs:
                self.visit(condition)
        for value in values:
            self.visit(value)
        for _generator in node.generators:
            self._comprehension_scopes.pop()


def _capture_rows(driver, total_rows):
    # Imported per call: tests patch testmu_appium._action_engine._settle, and
    # only a per-call attribute read sees the patch.
    from testmu_appium._action_engine import _Deadline, _settle

    try:
        page_source = _settle(driver, _Deadline())
        if page_source is None:
            page_source = driver.page_source
        width, height = _screen.window_size(driver)
        rows = perception.parse_tree(page_source, width, height)
    except Exception as exc:
        raise ViewportCaptureError(f"viewport capture failed: {exc}") from exc

    _assert_capture_health(rows, total_rows)
    return rows


def _coerce_total_rows(value):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ViewportCaptureError(
            "capture_baseline total_rows must be a non-negative integer or None"
        )
    return value


def _assert_capture_health(rows, total_rows):
    baseline = _coerce_total_rows(total_rows)
    if baseline in (None, 0):
        return
    if (
        baseline >= _POPULATED_MIN_ROWS
        and len(rows) * _DEGENERATE_FRACTION_DENOMINATOR
        <= baseline * _DEGENERATE_FRACTION_NUMERATOR
    ):
        raise DegenerateViewportCaptureError(
            "viewport hierarchy collapsed from recorded "
            f"{baseline} rows to {len(rows)} rows"
        )


def _project(rows):
    # Always the binding's current contract — no per-record contract to honour.
    fields = _CONTRACTS[_CURRENT_CONTRACT]
    return [{field: row.get(field) for field in fields} for row in rows]


def _matching_rows(rows: Iterable[Mapping], predicates: Mapping):
    _validate_predicates(predicates)
    return [row for row in rows if _matches(row, predicates)]


def _validate_predicates(predicates):
    if not isinstance(predicates, Mapping):
        raise ViewportScriptPolicyError("selection predicates must be a mapping")
    for key, value in predicates.items():
        if not isinstance(key, str) or not key:
            raise ViewportScriptPolicyError("selection predicate names must be strings")
        if "__" not in key:
            continue
        field, lookup = key.rsplit("__", 1)
        if not field or lookup != "startswith" or not isinstance(value, str):
            raise ViewportScriptPolicyError(
                f"unsupported selection predicate {key!r}"
            )


def _matches(row, predicates):
    for key, expected in predicates.items():
        if "__" not in key:
            if row.get(key) != expected:
                return False
            continue
        field, _lookup = key.rsplit("__", 1)
        value = row.get(field)
        if not isinstance(value, str) or not value.startswith(expected):
            return False
    return True


def _selection_drifts(rows, selection):
    if not isinstance(selection, list):
        raise ViewportScriptPolicyError("selection must be a list of recorded predicates")
    failed = []
    for record in selection:
        if not isinstance(record, Mapping):
            raise ViewportScriptPolicyError("selection records must be mappings")
        predicates = record.get("where")
        matched = record.get("matched")
        if isinstance(matched, bool) or not isinstance(matched, int) or matched < 0:
            raise ViewportScriptPolicyError(
                "selection records must carry a non-negative integer matched count"
            )
        fresh_matches = len(_matching_rows(rows, predicates))
        if matched > 0 and fresh_matches == 0:
            failed.append({"where": dict(predicates), "matched": matched})
    return failed


def _handle_selection_drift(predicates, matched):
    raise ViewportSelectionDriftError(
        f"viewport selection drift: {dict(predicates)!r} matched {matched} rows "
        "at authoring and none in the fresh capture"
    )


def _validate_script(code):
    if not isinstance(code, str):
        raise ViewportScriptCompileError("viewport extraction code must be a string")
    try:
        module = ast.parse(code, filename="<textual_analyzer>", mode="exec")
    except SyntaxError as exc:
        raise ViewportScriptCompileError(
            f"line {exc.lineno}: {exc.msg}"
        ) from exc
    if len(module.body) != 1 or not isinstance(module.body[0], ast.FunctionDef):
        raise ViewportScriptPolicyError(
            "viewport extraction must define exactly one extract(tree) function"
        )
    function = module.body[0]
    if function.name != "extract" or function.decorator_list:
        raise ViewportScriptPolicyError(
            "viewport extraction must define an undecorated extract(tree) function"
        )
    arguments = function.args
    positional = [*arguments.posonlyargs, *arguments.args]
    if (
        len(positional) != 1
        or positional[0].arg != "tree"
        or arguments.vararg is not None
        or arguments.kwonlyargs
        or arguments.kwarg is not None
        or arguments.defaults
        or arguments.kw_defaults
    ):
        raise ViewportScriptPolicyError(
            "viewport extraction must accept exactly one tree argument"
        )
    for node in ast.walk(module):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ViewportScriptPolicyError("imports are not allowed")
        if isinstance(node, ast.FunctionDef) and node is not function:
            raise ViewportScriptPolicyError("nested code definitions are not allowed")
        if isinstance(node, (ast.ClassDef, ast.Lambda, ast.AsyncFunctionDef)):
            raise ViewportScriptPolicyError("nested code definitions are not allowed")
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            raise ViewportScriptPolicyError("dunder names are not allowed")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            raise ViewportScriptPolicyError("dunder attributes are not allowed")
    bindings = _FunctionLocalBindings()
    for statement in function.body:
        bindings.visit(statement)
    _LoadNameValidator(bindings.names).visit(function)
    try:
        compile(module, "<textual_analyzer>", "exec")
    except (SyntaxError, ValueError, TypeError) as exc:
        raise ViewportScriptCompileError(str(exc)) from exc


def _worker(code, rows, connection):
    try:
        # Proof of life before any work. A silent worker is ambiguous — it could
        # be a slow script or a child that never ran — and the two have nothing
        # in common as fixes. This makes the parent able to tell them apart.
        connection.send(("started",))
        tree = _ViewportTree(rows)
        namespace = {
            "__builtins__": _SAFE_BUILTINS,
            "re": re,
            "json": json,
            "math": math,
            "Decimal": Decimal,
        }
        exec(compile(code, "<textual_analyzer>", "exec"), namespace, namespace)  # noqa: S102
        value = namespace["extract"](tree)
        connection.send(("value", value, tree.selection_records))
    except BaseException as exc:  # noqa: BLE001
        connection.send(("error", type(exc).__name__, str(exc)))
    finally:
        connection.close()


def _execution_timeout_seconds():
    return max(float(_config.get("default_action_timeout_ms")) / 1000, 0.001)


class _SandboxDidNotStart(Exception):
    """The child produced nothing before running any extraction code."""


def _is_frozen():
    return bool(getattr(sys, "frozen", False)) or "__compiled__" in globals()


def _start_methods():
    """Start methods to try, best first.

    fork stays first because it is immediate and is what a packaged runner can
    rely on. It is not always usable: inside the agent runner the forked child
    never reached a line of Python, on every attempt, while the same script
    finished in 0.01s standalone -- a fork inheriting the locks of a process
    that holds an asyncio loop and an HTTP pool. spawn is the fallback because
    it starts a clean interpreter, and it is skipped in a frozen build, where
    re-executing the binary without freeze_support would relaunch the app.
    """
    if _FORCED_START_METHOD:
        return [_FORCED_START_METHOD]
    available = multiprocessing.get_all_start_methods()
    order = [m for m in ("fork", "spawn") if m in available]
    if _is_frozen():
        order = [m for m in order if m != "spawn"]
    return order or available[:1]


def _run_script(code, rows):
    global _FORCED_START_METHOD
    candidates = _start_methods()
    for index, method in enumerate(candidates):
        try:
            result = _run_script_with(method, code, rows)
        except _SandboxDidNotStart:
            if index + 1 < len(candidates):
                # Remember it, so one dead fork costs one call and not every call.
                _FORCED_START_METHOD = candidates[index + 1]
                continue
            raise ViewportScriptTimeoutError(
                "viewport extraction sandbox never started: the worker process "
                f"produced nothing within {_WORKER_START_TIMEOUT_S:.1f}s using "
                f"{method}, before any of the extraction code ran. This is the "
                "sandbox, not the script."
            ) from None
        else:
            if index > 0:
                _FORCED_START_METHOD = method
            return result


def _run_script_with(method, code, rows):
    context = multiprocessing.get_context(method)
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=_worker, args=(code, rows, sender))
    process.start()
    sender.close()
    budget = _execution_timeout_seconds()
    try:
        started_at = time.monotonic()
        if not receiver.poll(min(_WORKER_START_TIMEOUT_S, budget)):
            process.terminate()
            process.join()
            raise _SandboxDidNotStart(method)
        try:
            first = receiver.recv()
        except EOFError as exc:
            raise ViewportScriptRuntimeError(
                "viewport extraction worker exited without a result"
            ) from exc
        # Older workers send the result directly; a started marker means the
        # child is alive and the remaining budget belongs to the script.
        if first == ("started",):
            remaining = max(budget - (time.monotonic() - started_at), 0.001)
            if not receiver.poll(remaining):
                process.terminate()
                process.join()
                raise ViewportScriptTimeoutError("viewport extraction timed out")
            try:
                result = receiver.recv()
            except EOFError as exc:
                raise ViewportScriptRuntimeError(
                    "viewport extraction worker exited without a result"
                ) from exc
        else:
            result = first
    finally:
        receiver.close()
        if process.is_alive():
            process.join(timeout=0.1)
        if process.is_alive():
            process.terminate()
            process.join()

    kind, *payload = result
    if kind == "error":
        error_type, message = payload
        raise ViewportScriptRuntimeError(f"{error_type}: {message}")
    return payload


def _validate_result(value):
    # The comparison layer coerces per operator; the binding only guarantees a
    # scalar came back, not a declared type. bool is checked before int (it is
    # an int subclass) so a boolean read is not mistaken for a number.
    if value is None:
        raise ViewportResultMissError("viewport extraction returned None")
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, Decimal)):
        finite = (
            value.is_finite() if isinstance(value, Decimal)
            else not isinstance(value, float) or math.isfinite(value)
        )
        if not finite:
            raise ViewportResultTypeError("viewport extraction returned a non-finite number")
        return value
    if isinstance(value, str):
        return value
    raise ViewportResultTypeError(
        "viewport extraction must return a scalar (str, number or bool), "
        f"got {type(value).__name__}"
    )


def _execute_projected_extraction(
    projected,
    *,
    code,
):
    _validate_script(code)
    value, selection_records = _run_script(code, projected)
    if not selection_records:
        # A policy refusal, not a script fault: the code ran fine, it is the
        # recording that would be invalid. The distinction is load-bearing --
        # ViewportScriptRuntimeError is a heal trigger, and an extraction that
        # records no selection is precisely the one heal must never rescue.
        raise ViewportScriptPolicyError(_SELECTION_REQUIRED)
    return _validate_result(value), selection_records


def _execute_extraction(
    driver,
    *,
    code,
    total_rows=None,
):
    rows = _capture_rows(driver, total_rows)
    projected = _project(rows)
    value, selection_records = _execute_projected_extraction(
        projected,
        code=code,
    )
    return value, selection_records, len(rows)


def _viewport_heal_endpoint():
    host = _config.resolved("ai_api_host", _config._resolve_ai_api_host)
    return f"{str(host).rstrip('/')}/api/v1/textual_analyzer/heal"


def _viewport_heal_timeout_s():
    milliseconds = int(_config.get("heal_timeout_ms", 60000) or 0)
    return milliseconds / 1000 if milliseconds > 0 else _DEFAULT_HEAL_TIMEOUT_S


def _selection_has_match(selection_records):
    return any(record.get("matched", 0) > 0 for record in selection_records)


def _heal_extraction(
    *,
    code,
    extraction_description,
    failed_predicates,
    projected_rows,
):
    """Make exactly one server request and prove its Python against this capture."""
    if not extraction_description:
        return ViewportHealNoMatch("recorded extraction_description is empty")

    request_headers = headers()
    request_headers["x-platform"] = _config.platform()
    body = {
        "query": extraction_description,
        "extraction_description": extraction_description,
        "previous_code": code,
        "failed_predicates": failed_predicates,
        # Rows go over as JSON text: the field is a string on the web leg too,
        # and the server only ever renders it into the prompt.
        "dom_snapshot": json.dumps(projected_rows, separators=(",", ":")),
    }
    try:
        with httpx.Client(
            timeout=_viewport_heal_timeout_s(), follow_redirects=True,
        ) as client:
            response = client.post(
                _viewport_heal_endpoint(),
                headers=request_headers,
                json=body,
                auth=auth(),
            )
    except httpx.HTTPError as exc:
        return ViewportHealUnavailable(f"viewport heal request failed: {exc}")

    if response.status_code == 404:
        return ViewportHealNoMatch("server returned no usable viewport extractor")
    if response.status_code != 200:
        return ViewportHealUnavailable(
            f"viewport heal returned {response.status_code}: {response.text[:500]}"
        )
    try:
        data = response.json()
    except ValueError:
        return ViewportHealNoMatch("server returned a non-JSON viewport extractor")
    if not isinstance(data, dict):
        return ViewportHealNoMatch("server viewport extractor response is not an object")

    healed_code = data.get("code")
    confidence = data.get("confidence", 0.0)
    if not isinstance(healed_code, str) or not healed_code:
        return ViewportHealNoMatch("server returned no viewport extractor code")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        return ViewportHealNoMatch("server returned invalid viewport confidence")
    if confidence < _CONFIDENCE_THRESHOLD:
        return ViewportHealNoMatch(
            f"server confidence {confidence} is below {_CONFIDENCE_THRESHOLD}"
        )

    try:
        value, selection_records = _execute_projected_extraction(
            projected_rows,
            code=healed_code,
        )
    except (
        ViewportResultMissError,
        ViewportResultTypeError,
        ViewportScriptCompileError,
        ViewportScriptPolicyError,
        ViewportScriptRuntimeError,
        ViewportScriptTimeoutError,
    ) as exc:
        return ViewportHealUnresolved(str(exc))
    if not _selection_has_match(selection_records):
        return ViewportHealUnresolved("regenerated extractor selected no fresh rows")
    return ViewportHealHit(value=value, code=healed_code, reasoning=str(data.get("reasoning", "")))


def _raise_unrecovered_viewport_heal(trigger, outcome):
    if isinstance(outcome, ViewportHealNoMatch):
        detail = f"authoritative no-match: {outcome.reason}"
    elif isinstance(outcome, ViewportHealUnresolved):
        detail = f"regenerated script unresolved: {outcome.reason}"
    else:
        detail = f"unavailable: {outcome.cause}"
    raise type(trigger)(f"{trigger}; viewport heal {detail}") from trigger


def _as_recorded(value):
    """The extraction result as authoring stored it: a bool is recorded as
    ``'true'``/``'false'`` (the analyzer's comparison convention, which the
    recorded assertion's expected value follows); every other scalar is unchanged."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return value


def textual_analyzer(
    driver,
    *,
    code,
    capture_baseline=None,
    extraction_description="",
):
    """Evaluate a recorded extraction against a fresh projected viewport tree.

    ``capture_baseline`` is the authoring capture's shape,
    ``{"total_rows": int | None, "selection": [{"where": {...}, "matched": N}]}``:
    ``total_rows`` gates whole-capture collapse and ``selection`` gates
    per-predicate drift. Drift, runtime failure, and a None result get one
    non-persistent recovery attempt only during replay. Authoring uses its
    separate entry point below.
    """
    baseline = capture_baseline or {}
    total_rows = baseline.get("total_rows")
    selection = baseline.get("selection") or []
    rows = _capture_rows(driver, total_rows)
    failed_predicates = _selection_drifts(rows, selection)
    projected = _project(rows)
    try:
        if failed_predicates:
            _handle_selection_drift(
                failed_predicates[0]["where"], failed_predicates[0]["matched"]
            )
        value, _selection_records = _execute_projected_extraction(
            projected,
            code=code,
        )
        return _as_recorded(value)
    except (
        ViewportSelectionDriftError,
        ViewportResultMissError,
        ViewportScriptRuntimeError,
        ViewportScriptTimeoutError,
    ) as trigger:
        if not _config.heal_enabled():
            raise
        outcome = _heal_extraction(
            code=code,
            extraction_description=extraction_description,
            failed_predicates=failed_predicates,
            projected_rows=projected,
        )
        if isinstance(outcome, ViewportHealHit):
            mark_autohealed(_VIEWPORT_HEAL_SOURCE)
            _log.info(
                "[textual_analyzer] healed for this run only; re-author if this repeats | %s",
                outcome.reasoning,
            )
            return _as_recorded(outcome.value)
        _raise_unrecovered_viewport_heal(trigger, outcome)


def textual_analyzer_authoring(driver, *, code):
    """Execute a viewport extraction and return its recording metadata.

    ``row_count`` and ``selection`` become the recorded ``capture_baseline``
    (``total_rows`` + ``selection``) that replay reads back.
    """
    started = time.perf_counter()
    value, selection, row_count = _execute_extraction(
        driver,
        code=code,
    )
    return {
        "value": value,
        "selection": selection,
        "row_count": row_count,
        "duration_ms": (time.perf_counter() - started) * 1000,
    }
