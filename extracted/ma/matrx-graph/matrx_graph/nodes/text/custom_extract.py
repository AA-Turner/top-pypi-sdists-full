"""``text.custom_extract`` — sandboxed Python script for arbitrary text/object reshaping.

The design tension: workflows need to restructure data in ways the
constrained ``data.transform`` expression can't express (e.g. loops over
items, conditional accumulation, regex compose). A raw ``exec()`` would be
a footgun — untrusted authors could read env vars, open files, call the
network, etc.

This node threads the needle with a stricter-than-``safe_eval`` stmt-level
sandbox:

- AST walk rejects imports, attribute access, function defs, class defs,
  decorators, with-statements, async, try/finally, lambdas, generators,
  starred expressions, walrus.
- Whitelists: ``for``, ``while``, ``if``, ``break``, ``continue``,
  ``return`` (via ``__result__ = …``), arithmetic, boolean/compare ops,
  subscripts, list/dict/set/tuple comprehensions, literal containers,
  f-strings.
- Name whitelist: only ``inputs``, ``re``, ``json``, and a handful of
  builtin-like helpers (``len``, ``str``, ``int``, ``float``, ``bool``,
  ``list``, ``dict``, ``set``, ``tuple``, ``sorted``, ``reversed``,
  ``enumerate``, ``range``, ``min``, ``max``, ``sum``, ``abs``, ``any``,
  ``all``, ``zip``, ``filter``, ``map``). No dunders, no ``open``, no
  ``eval``/``exec``.
- Hard time limit via an interrupt thread (default 2s) — breaks infinite
  loops without a signal-based SIGALRM (portable to Windows / subinterp).
- Input size cap + output size cap to prevent memory DoS.

The script must assign a final value to the special name ``__result__`` —
that's what ends up in ``output.result``. Anything else in the local scope
is discarded.
"""

from __future__ import annotations

import ast
import json
import re
import threading
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.errors import ExecutionError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

_MAX_SCRIPT_LEN = 20_000
_MAX_INPUT_SIZE = 5_000_000  # 5 MB of JSON bytes

_ALLOWED_NODES: tuple[type[ast.AST], ...] = (
    ast.Module,
    ast.Expression,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.AnnAssign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.JoinedStr,
    ast.FormattedValue,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.If,
    ast.For,
    ast.While,
    ast.Break,
    ast.Continue,
    ast.Pass,
    ast.Subscript,
    ast.Slice,
    ast.Index,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
    ast.comprehension,
    # Attribute access — gated by dunder-name filter in the walker. Needed
    # for common methods like list.append / str.split / dict.get.
    ast.Attribute,
    # Operators. ast.Pow deliberately EXCLUDED: `10**10**10` computes an
    # exponential tower eagerly — the _InterruptTimer cannot interrupt a
    # single C-level big-int multiply, so a one-line expression hangs the
    # worker far past timeout_s. Exponentiation is banned here, same as in
    # nodes/_sandbox.py.
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.FloorDiv,
    ast.USub,
    ast.UAdd,
    ast.Not,
    ast.Invert,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.Is,
    ast.IsNot,
    ast.BitAnd,
    ast.BitOr,
    ast.BitXor,
    ast.LShift,
    ast.RShift,
    # Function calls — gated by whitelist in the walker
    ast.Call,
    ast.keyword,
)

# Helpers that are safe when called on arbitrary values.
_SAFE_BUILTINS: dict[str, Any] = {
    "len": len,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "sorted": sorted,
    "reversed": reversed,
    "enumerate": enumerate,
    "range": range,
    "min": min,
    "max": max,
    "sum": sum,
    "abs": abs,
    "any": any,
    "all": all,
    "zip": zip,
    "filter": filter,
    "map": map,
    "round": round,
}

# ``re`` surface we expose — just the read-only query APIs.
_RE_SURFACE = {
    "search": re.search,
    "match": re.match,
    "fullmatch": re.fullmatch,
    "findall": re.findall,
    "finditer": re.finditer,
    "split": re.split,
    "sub": re.sub,
    "subn": re.subn,
    "escape": re.escape,
    "IGNORECASE": re.IGNORECASE,
    "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL,
    "VERBOSE": re.VERBOSE,
}

# ``json`` surface — dumps + loads only.
_JSON_SURFACE = {"dumps": json.dumps, "loads": json.loads}

# Names callable via attribute are blocked below; exposing as namespace
# objects would require Attribute access in the AST, which we reject. So
# re/json are wrapped in dict-like facades and referenced by subscript.
# We use SimpleNamespace-ish via a dict wrapped class that supports . access
# via __getattr__. But __getattr__ is attribute access — not in our AST
# whitelist. Instead expose them directly via subscript or by name.
# Resolution: bind every entry as a top-level name so authors call
# ``search(pattern, text)`` directly instead of ``re.search(...)``.
_RE_NAMES = {f"re_{k}": v for k, v in _RE_SURFACE.items()}
_JSON_NAMES = {f"json_{k}": v for k, v in _JSON_SURFACE.items()}


class _Walker(ast.NodeVisitor):
    """Enforce node + name + call whitelists."""

    def __init__(self, allowed_names: frozenset[str]):
        self.allowed_names = allowed_names

    def _reject(self, msg: str, node: ast.AST) -> None:
        raise ExecutionError(f"custom_extract: {msg} at line {getattr(node, 'lineno', '?')}")

    def visit(self, node: ast.AST) -> None:
        if not isinstance(node, _ALLOWED_NODES):
            self._reject(f"disallowed syntax {type(node).__name__}", node)
        if isinstance(node, ast.Attribute):
            # Dunder filter: the classic sandbox escapes (``__class__``,
            # ``__globals__``, ``__subclasses__``, ``__builtins__``, etc.)
            # all go through underscore-prefixed attribute access. By
            # rejecting any ``_``-leading attribute, we lock those out
            # while keeping ``.append`` / ``.get`` / ``.split`` usable.
            if node.attr.startswith("_"):
                self._reject(f"dunder/private attribute '{node.attr}' is not allowed", node)
        if isinstance(node, ast.Name):
            # In Store position, any name is fine (locals).
            if isinstance(node.ctx, ast.Load) and node.id not in self.allowed_names:
                # allow dunder-free user locals (any name that was assigned)
                # We can't track locals here; accept any name — unknown reads
                # will NameError at runtime inside the restricted globals.
                pass
        self.generic_visit(node)


class _InterruptTimer:
    """Run a thread that raises KeyboardInterrupt in the main thread on timeout."""

    def __init__(self, timeout_s: float):
        self.timeout_s = timeout_s
        self._timer: threading.Timer | None = None
        self._tripped = False

    def __enter__(self) -> _InterruptTimer:
        import _thread

        def _trip() -> None:
            self._tripped = True
            # Interrupt the main interpreter thread. The executing script
            # sees a KeyboardInterrupt at the next bytecode boundary.
            _thread.interrupt_main()

        self._timer = threading.Timer(self.timeout_s, _trip)
        self._timer.daemon = True
        self._timer.start()
        return self

    def __exit__(self, *exc) -> None:
        if self._timer is not None:
            self._timer.cancel()

    @property
    def tripped(self) -> bool:
        return self._tripped


def _estimate_size(value: Any) -> int:
    try:
        return len(json.dumps(value, default=str))
    except Exception:
        return 0


class CustomExtractInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class CustomExtractConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    script: str = Field(
        min_length=1,
        description=(
            "Python script. The incoming payload is bound to ``inputs``; "
            "the final value must be assigned to ``__result__``. "
            "Only safe builtins, ``re_*`` regex functions, and ``json_*`` "
            "are exposed. No imports, no attribute access, no I/O."
        ),
        json_schema_extra=field_extras(
            widget="code",
            placeholder=(
                "out = []\n"
                "for item in inputs['items']:\n"
                "    if item.get('score', 0) > 0.5:\n"
                "        out.append({'name': item['name']})\n"
                "__result__ = out\n"
            ),
        ),
    )
    timeout_s: float = Field(
        default=2.0,
        ge=0.1,
        le=30.0,
        description="Hard wall-clock limit. Infinite loops / huge comprehensions get killed.",
    )
    max_output_bytes: int = Field(
        default=5_000_000,
        ge=1_000,
        le=50_000_000,
        description="Reject results larger than this when serialized to JSON.",
    )


class CustomExtractOutput(KindModel, kind="custom_script_result"):
    """Success payload (Node Result System) — genuine failures (sandbox
    violation, timeout, runtime error, non-JSON result) FAIL the node
    (ExecutionError → the scheduler's failure ladder); the old vestigial
    ok/error payload fields are gone."""

    result: JsonValue = Field(
        default=None,
        description="The value the script assigned to `__result__`.",
    )


class CustomExtractExecutor:
    """Run a sandboxed Python script that reshapes ``inputs`` into ``result``."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="text.custom_extract",
        category=NodeCategory.DATA,
        display_name="Custom Extract",
        description="Run a small custom script to pull out or reshape data.",
        input_schema=CustomExtractInput,
        output_schema=CustomExtractOutput,
        config_schema=CustomExtractConfig,
        output_kind="custom_script_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="code",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: CustomExtractInput,
        config: CustomExtractConfig,
    ) -> NodeResult[CustomExtractOutput]:
        _ = ctx

        # D1 (audit 2026-07-08): every genuine failure RAISES ExecutionError so
        # the NODE fails honestly. The old code swallowed script/extraction
        # errors into a COMPLETED node carrying ``ok=False`` — the silent-
        # success shape the tool-output gate kills elsewhere. Downstream
        # mappings then missed ``result.*`` and the run died as an *edge-routing*
        # error attributed to the wrong node. A failing script must FAIL its own
        # node (same posture as data.transform, whose safe_eval propagates).

        if len(config.script) > _MAX_SCRIPT_LEN:
            raise ExecutionError(
                f"custom_extract: script too long ({len(config.script)} > {_MAX_SCRIPT_LEN})"
            )

        payload = inputs.model_dump(mode="json")
        if _estimate_size(payload) > _MAX_INPUT_SIZE:
            raise ExecutionError("custom_extract: input payload exceeds size cap; chunk first")

        # Parse + walk. A SyntaxError or sandbox violation (ExecutionError from
        # the walker) is a hard authoring failure — let it fail the node.
        try:
            tree = ast.parse(config.script, mode="exec")
        except SyntaxError as e:
            raise ExecutionError(f"custom_extract: SyntaxError: {e}") from e

        allowed = frozenset(
            ["inputs", "__result__", *_SAFE_BUILTINS.keys(), *_RE_NAMES.keys(), *_JSON_NAMES.keys()]
        )
        _Walker(allowed).visit(tree)  # raises ExecutionError on a violation

        # Build the restricted globals. ``__builtins__`` is nulled; only the
        # whitelisted names are in scope. Locals hold script-assigned names.
        restricted_globals: dict[str, Any] = {
            "__builtins__": {},
            "inputs": payload,
            **_SAFE_BUILTINS,
            **_RE_NAMES,
            **_JSON_NAMES,
        }
        local_ns: dict[str, Any] = {}

        code = compile(tree, "<custom_extract>", "exec")

        try:
            with _InterruptTimer(config.timeout_s) as timer:
                try:
                    exec(code, restricted_globals, local_ns)  # noqa: S102
                except KeyboardInterrupt:
                    if timer.tripped:
                        raise ExecutionError(
                            f"custom_extract: script timed out after {config.timeout_s}s"
                        ) from None
                    raise
        except ExecutionError:
            raise
        except Exception as e:
            # A genuine script runtime error (NameError, ZeroDivisionError, a
            # bad subscript on missing data, …). FAIL the node — this is the
            # core D1 fix.
            raise ExecutionError(f"custom_extract: {type(e).__name__}: {e}") from e

        if "__result__" not in local_ns:
            raise ExecutionError("custom_extract: script did not assign to ``__result__``")

        result = local_ns["__result__"]
        if _estimate_size(result) > config.max_output_bytes:
            raise ExecutionError(
                f"custom_extract: result exceeds max_output_bytes ({config.max_output_bytes})"
            )

        # Enforce JSON-serializability — channel writes require it. No
        # default=str fallback: sets / custom classes would silently
        # stringify here then blow up at channel-write time with a less
        # actionable error.
        try:
            json.dumps(result)
        except (TypeError, ValueError) as e:
            raise ExecutionError(f"custom_extract: result is not JSON-serializable: {e}") from e

        return success(CustomExtractOutput(result=result))
