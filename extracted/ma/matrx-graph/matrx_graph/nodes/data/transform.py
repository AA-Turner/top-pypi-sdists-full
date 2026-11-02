from __future__ import annotations

import ast
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_serializer, model_validator

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras


def _names_read(formula: str) -> set[str] | None:
    """The input names a formula reads: inputs['x'], get(inputs, 'x'), 'x' in inputs.

    None when it hands `inputs` itself on whole (it may then read anything).
    """
    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError:
        return set()
    read: set[str] = set()
    named: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "inputs":
            named.add(id(node.value))
            if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                read.add(node.slice.value)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "get" and len(node.args) >= 2:
            whole, key = node.args[0], node.args[1]
            if isinstance(whole, ast.Name) and whole.id == "inputs" and isinstance(key, ast.Constant):
                named.add(id(whole))
                read.add(str(key.value))
        elif isinstance(node, ast.Compare) and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
            for op, right in zip(node.ops, node.comparators):
                if isinstance(op, ast.In | ast.NotIn) and isinstance(right, ast.Name) and right.id == "inputs":
                    named.add(id(right))
                    read.add(node.left.value)
    whole_use = any(isinstance(n, ast.Name) and n.id == "inputs" and id(n) not in named for n in ast.walk(tree))
    return None if whole_use else read


class TransformInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class TransformOutput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": (
                "THE OUTPUT SHAPE IS THE EXPRESSION. A dict result is spread "
                "FLAT onto the output root — its own keys ARE the output keys "
                "and there is NO 'result' key to map from. Only a non-dict "
                "result arrives as {'result': <value>}. When the expression is "
                "a dict literal the compiler declares the real keys on the node "
                "(effective_output_schema) and the joint check enforces them."
            )
        },
    )

    result: JsonValue = Field(
        default=None,
        description=(
            "The value a NON-DICT expression evaluated to. Absent when the "
            "expression returned a dict: those keys are spread flat onto the "
            "output root instead, so downstream edges map from THEM "
            "('canon' <- 'canon'), never from 'result'."
        ),
    )

    @model_serializer(mode="wrap")
    def _omit_vestigial_result(self, handler):  # type: ignore[no-untyped-def]
        """Drop the vestigial ``result: null`` when a dict was spread flat.

        A dict expression result is spread onto the output root; the declared
        ``result`` field then serializes as ``null`` alongside the real keys.
        That junk key collides at any join fed by TWO transforms (the engine's
        multi-writer guard rejects the duplicate ``result``) and surfaces a
        useless "Result —" option in the studio's connection picker. A lone
        ``result`` (non-dict expression, even if None) is preserved.
        """
        data = handler(self)
        if isinstance(data, dict) and len(data) > 1 and data.get("result") is None:
            data = {k: v for k, v in data.items() if k != "result"}
        return data


class TransformConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    define: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Named parts, computed before the expression in the order they read each other (never the saved "
            "key order, which storage sorts): each is a formula over `inputs`, and "
            "its value is then readable as inputs['<name>'] by the parts after it and by the expression. "
            "One step can hold a chain (answers -> cells -> questions) with every part named and shown, "
            "instead of one step per link. A name may not repeat an input this step receives."
        ),
        json_schema_extra=field_extras(widget="json", placeholder='{"kept": "[p for p in inputs[\'pages\'] if p[\'good\']]"}'),
    )

    expression: str = Field(
        min_length=1,
        description=(
            "Python expression evaluated against `inputs`. THE OUTPUT SHAPE IS "
            "THIS EXPRESSION: if it returns a dict, that dict's keys are spread "
            "FLAT onto the output root (expression "
            "\"{'canon': inputs['canon']}\" emits `canon`, and there is NO "
            "`result` key to map from); any other value arrives as "
            "`output.result`. Uses the shared sandbox: only constants, "
            "arithmetic, comparisons, boolean ops, and subscripts."
        ),
        json_schema_extra=field_extras(
            widget="code",
            code_language="python",
            placeholder="inputs['value'] * 2",
            help=(
                "Safe Python expression. A dict result spreads FLAT onto the "
                "output (its keys become the output keys); anything else "
                "arrives as 'result'."
            ),
        ),
    )

    def part_order(self) -> list[str]:
        """The named parts in the order they read each other — never the stored key order.

        A Definition is stored as jsonb, which sorts object keys shortest-first, so the order an author
        wrote the parts in does not survive a save (v27 of a live workflow ran `scan` before the `texts`
        it reads). A part runs after every part it reads (inputs['x'], get(inputs, 'x'), 'x' in inputs);
        one that hands `inputs` on whole runs after the rest. The stored order only breaks ties. Two parts that quote each other are refused by name.
        """
        names = list(self.define)
        reads = {name: _names_read(formula) for name, formula in self.define.items()}
        needs = {name: (r & set(names)) - {name} for name, r in reads.items() if r is not None}
        for name, r in reads.items():
            if r is None:  # reads `inputs` whole: after every part that does not read it
                needs[name] = {n for n in names if n != name and name not in needs.get(n, set())}
        order: list[str] = []
        while len(order) < len(names):
            ready = [n for n in names if n not in order and needs[n] <= set(order)]
            if not ready:
                stuck = [n for n in names if n not in order]
                raise ValueError(
                    f"data.transform: the parts {stuck} each read another of them, so none can be computed "
                    "first; break the loop."
                )
            order.append(ready[0])
        return order

    @model_validator(mode="after")
    def _parts_can_be_ordered(self) -> TransformConfig:
        self.part_order()
        return self

    def effective_output_json_schema(self) -> dict[str, Any] | None:
        """The node's REAL output schema, resolved from the expression.

        ``data.transform`` is ``dynamic_output`` because its shape is the
        author's expression — but "dynamic" was being read as "unknowable",
        and the whole platform (the dry run, the joint check, the studio's
        connection picker, the deliverable schema) fell back to the
        registered ``TransformOutput``, which declares ``result``. That
        declaration is WRONG for every dict expression, and it is exactly
        what a Conductor mapped ``variables <- result`` against before the
        run died on ``KeyError: 'result'``.

        The compiler calls this for every dynamic-output node (compile.py
        § dynamic output schema). Returning a CLOSED schema here is what lets
        ``dry_run`` prove a mapping can never resolve; ``None`` (the honest
        answer for an expression whose shape is not statically knowable)
        leaves the joint unverified, and the joint check now SAYS so.
        """
        shape = expression_output_shape(self.expression)
        if shape is None:
            return None
        keys, reason = shape
        return {
            "type": "object",
            "title": "TransformOutput",
            "description": (
                f"Resolved from the step's expression: {reason}."
            ),
            "properties": {key: {"title": key} for key in keys},
            "additionalProperties": False,
        }


#: AST node types whose value can NEVER be a dict, so the transform's output
#: is certainly the single key ``result``. ``BinOp`` is handled separately:
#: ``dict | dict`` IS a dict merge, so only that operator is excluded.
_NEVER_A_DICT = (
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.ListComp,
    ast.SetComp,
    ast.GeneratorExp,
    ast.JoinedStr,
    ast.Compare,
    ast.UnaryOp,
)


def expression_output_shape(expression: str) -> tuple[tuple[str, ...], str] | None:
    """The output keys this expression CERTAINLY emits, or ``None`` if unknowable.

    The runtime contract is simple and was never declared: a dict result is
    spread flat onto the output root, anything else lands under ``result``. So
    for the overwhelmingly common authored form — a dict LITERAL with constant
    string keys, which is what every projection step is — the output shape is
    fully knowable before the run, and the joint check must hold the author to
    it. (The live break: expression ``{'situation': ..., 'child_age': ...,
    'canon': ...}`` wired downstream as ``variables <- result``, run
    6511ffd1, 2026-09-12 — no node ever emits ``result`` there.)

    ``None`` is the honest answer for everything else (``inputs['inputs']``, a
    dict comprehension, a merge): the shape is decided at run time and the
    check must SAY so rather than stay quiet.

    Returns ``(keys, plain-language reason)``.
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError:
        return None
    node = tree.body
    if isinstance(node, ast.Dict):
        keys: list[str] = []
        for key in node.keys:
            # ``key is None`` is ``{**other}`` — unknown keys.
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                return None
            if key.value not in keys:
                keys.append(key.value)
        if not keys:
            # ``{}`` spreads nothing, so the declared ``result`` survives.
            return ("result",), (
                "the expression is an empty dict literal, which emits only 'result'"
            )
        return tuple(keys), (
            "the expression is a dict literal, and a dict result is spread flat "
            "onto the output root"
        )
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return None  # dict | dict — a merge of unknown keys
    if isinstance(node, (*_NEVER_A_DICT, ast.BinOp)):
        return ("result",), (
            "the expression cannot evaluate to a dict, so its value is delivered "
            "as 'result'"
        )
    return None


class TransformExecutor:
    """Evaluate a sandboxed expression over inputs and emit the result.

    Useful for shaping payloads between nodes (projection, arithmetic, literal
    enrichment). For anything that needs function calls or external state,
    use `tool.call` with a registered action instead.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.transform",
        category=NodeCategory.DATA,
        display_name="Transform",
        description="Reshape data with a small custom formula.",
        input_schema=TransformInput,
        output_schema=TransformOutput,
        config_schema=TransformConfig,
        # Round-1 F7: 'json' is a FORMAT word, not an identity — declaring
        # it masked the payload's real kind and settlement would stamp
        # __kind:'json' into business data. Undeclared, this pass-through
        # settles with the kind of what actually flowed (runtime
        # propagation), which is the honest answer.
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        # DYNAMIC BY DESIGN — the output shape IS the author's expression, so
        # no single kind can describe every instance. Declared dynamic (GAP 2,
        # §10g); the honest declaration lives on the node INSTANCE as
        # ``data.output_kind`` (see aidream/workflows/study_pack_v2.py::pack).
        dynamic_output=True,
        determinism=ActionTier.PURE,
        icon="function-square",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: TransformInput,
        config: TransformConfig,
    ) -> NodeResult[TransformOutput]:
        payload = inputs.model_dump(mode="json")
        for name in config.part_order():
            formula = config.define[name]
            if name in payload:
                raise ExecutionError(
                    f"data.transform: the part '{name}' has the same name as an input this step receives; "
                    "rename the part."
                )
            payload[name] = safe_eval(formula, payload)
        result = safe_eval(config.expression, payload)

        # Best Practice: If the transformation results in a dictionary,
        # we spread it into the root of the output so downstream Pydantic
        # models can validate against the flat keys natively. (Kept through
        # the NodeResult migration — authored edge mappings rely on the
        # flat keys; only tool.call's spread was retired.)
        if isinstance(result, dict):
            return success(TransformOutput(**result))

        return success(TransformOutput(result=result))
