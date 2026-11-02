"""What comes in and what goes out is visible on the canvas (Arman, 2026-10-28).

Every value a workflow uses arrives through a visible input step (``io.user_input``, whose labelled
fields ARE the run form), and every result leaves through a visible output step
(``output.to_frontend``). Words: common-docs ``systems/workflows/projects/generic-only/VISION.md``
§ "What comes in and what goes out must be visible"; rule: ``RULES.md`` Rule 18.

``visible_io_findings`` names every way a definition breaks that, one ``VisibleIoFinding`` each:

* ``no_input_step`` — no ``io.user_input`` step at all;
* ``unlabelled_input_field`` — an input field with no label (a person cannot name it);
* ``no_output_step`` — no ``output.to_frontend`` step at all;
* ``hidden_input`` — a run-level value a step reads that no input step shows: a ``{"$input": name}``
  / ``{"$var": name}`` reference whose name is not an input-step field, a declared variable
  (``definition.variables`` — set in a toolbar dialog, never drawn on the canvas) no input step
  shows, a ``{"$run": …}`` / ``{run.…}`` read, a ``{{trigger.…}}`` placeholder, or an entry step
  that reads the caller's values straight from ``inputs``;
* ``hidden_write`` — a step that saves a record, changes a setting or calls an outside service
  (its registered ``determinism`` is ``side_effect``) with no path to an output step.

Pure and registry-optional: the validator (a WARNING on every save/publish/validate door) and the
release guard (``scripts/check_workflow_visible_io.py``) call the same function. Without a registry,
or for a type the registry does not know, a write is recognised by its name.
"""

from __future__ import annotations

import re
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from matrx_graph.executor.registry import NodeRegistry
    from matrx_graph.types.definition import Definition, NodeDef

INPUT_STEP_TYPES = frozenset({"io.user_input"})
OUTPUT_STEP_TYPES = frozenset({"output.to_frontend"})
#: Side-effect steps that are not "secret writes": the output pack itself (it shows), and the run log.
_NOT_A_WRITE_PREFIXES = ("output.", "log.")
#: Name fallback for a type the registry does not know (unregistered / legacy specs).
_WRITE_NAME = re.compile(
    r"(^|[._])(save|save_many|upsert|sync|write|commit|land|apply|publish|deliver|notify|send|track|upload|"
    r"ingest|register|release|record|finalize|import|attach|archive|set_archived|launch|commission|"
    r"track_accounts|land_[a-z_]+|[a-z_]+_apply|gate_record|mapped_sync)($|[._])"
)
_TRIGGER_PLACEHOLDER = re.compile(r"\{\{\s*trigger[.\]\[]")
_RUN_PLACEHOLDER = re.compile(r"\{run[.}]")
_ENTRY_READS_INPUTS = re.compile(r"\binputs\s*(\[|\.get\()|get\(\s*inputs\s*,")

CODES = ("no_input_step", "unlabelled_input_field", "no_output_step", "hidden_input", "hidden_write")


@dataclass(frozen=True)
class VisibleIoFinding:
    code: str
    message: str
    node_id: str | None = None
    #: The hidden value's name (hidden_input) or the step's type (hidden_write).
    subject: str | None = None
    #: Where the read sits: ``$input`` / ``$var`` / ``variable`` / ``$run`` / ``trigger`` / ``entry``.
    via: str | None = None


def _refs(value: Any, key: str) -> list[str]:
    """Every ``{key: name}`` reference name anywhere inside ``value``."""
    out: list[str] = []
    if isinstance(value, dict):
        ref = value.get(key)
        if isinstance(ref, str):
            out.append(ref)
        for v in value.values():
            out.extend(_refs(v, key))
    elif isinstance(value, list):
        for v in value:
            out.extend(_refs(v, key))
    return out


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


def _reads_run(value: Any) -> bool:
    if isinstance(value, dict):
        return "$run" in value or any(_reads_run(v) for v in value.values())
    if isinstance(value, list):
        return any(_reads_run(v) for v in value)
    return isinstance(value, str) and bool(_RUN_PLACEHOLDER.search(value))


def input_fields(definition: Definition) -> dict[str, dict[str, Any]]:
    """Every field shown on an input step, by key."""
    fields: dict[str, dict[str, Any]] = {}
    for node in definition.nodes:
        if node.spec_type not in INPUT_STEP_TYPES:
            continue
        for fld in (node.config or {}).get("fields") or []:
            if isinstance(fld, dict) and fld.get("key"):
                fields.setdefault(str(fld["key"]), {**fld, "_node_id": node.id})
    return fields


def is_write(node: NodeDef, registry: NodeRegistry | None = None) -> bool:
    spec = node.spec_type
    if spec in INPUT_STEP_TYPES or spec.startswith(_NOT_A_WRITE_PREFIXES):
        return False
    if registry is not None and registry.has(spec):
        tier = registry.get(spec).spec.determinism
        return str(getattr(tier, "value", tier)) == "side_effect"
    return bool(_WRITE_NAME.search(spec))


def _reaches_output(definition: Definition) -> set[str]:
    """Node ids with a path (any edge kind) to an output step — themselves included."""
    upstream: dict[str, list[str]] = defaultdict(list)
    for edge in definition.edges:
        upstream[edge.target].append(edge.source)
    seen = {n.id for n in definition.nodes if n.spec_type in OUTPUT_STEP_TYPES}
    queue = deque(seen)
    while queue:
        for src in upstream.get(queue.popleft(), ()):
            if src not in seen:
                seen.add(src)
                queue.append(src)
    return seen


def visible_io_findings(definition: Definition, registry: NodeRegistry | None = None) -> list[VisibleIoFinding]:
    findings: list[VisibleIoFinding] = []
    fields = input_fields(definition)
    shown = set(fields)
    has_input = any(n.spec_type in INPUT_STEP_TYPES for n in definition.nodes)
    has_output = any(n.spec_type in OUTPUT_STEP_TYPES for n in definition.nodes)

    if not has_input:
        findings.append(VisibleIoFinding(
            "no_input_step",
            "This workflow has no input step, so nobody opening it can see what it takes in. Add a "
            "'Collect Inputs' step (io.user_input) with a labelled field for every value it uses.",
        ))
    for key, fld in fields.items():
        if not str(fld.get("label") or "").strip():
            findings.append(VisibleIoFinding(
                "unlabelled_input_field",
                f"Input field '{key}' has no label. Give it one so a person can say what it asks for.",
                node_id=fld["_node_id"], subject=key,
            ))
    if not has_output:
        findings.append(VisibleIoFinding(
            "no_output_step",
            "This workflow has no output step, so nobody opening it can see what it produces. End it "
            "with a 'Show on Screen' step (output.to_frontend) that presents the result.",
        ))

    hidden: dict[str, VisibleIoFinding] = {}

    def _hide(name: str, via: str, node_id: str | None, why: str) -> None:
        hidden.setdefault(name, VisibleIoFinding(
            "hidden_input",
            f"{why} '{name}' is read from the run but no input step shows it. Add it as a labelled field "
            "on the input step.",
            node_id=node_id, subject=name, via=via,
        ))

    targets = {e.target for e in definition.edges}
    for node in definition.nodes:
        if node.spec_type in INPUT_STEP_TYPES:
            continue
        data = node.data or {}
        for name in _refs(data, "$input"):
            if name not in shown:
                _hide(name, "$input", node.id, "Run input")
        for name in _refs(data, "$var"):
            if name not in shown:
                _hide(name, "$var", node.id, "Run variable")
        if _reads_run(data):
            _hide("run", "$run", node.id, "The run's own settings")
        for text in _strings(data):
            if _TRIGGER_PLACEHOLDER.search(text):
                _hide("trigger", "trigger", node.id, "The trigger's record")
                break
        if node.id not in targets and node.spec_type not in OUTPUT_STEP_TYPES:
            if any(_ENTRY_READS_INPUTS.search(t) for t in _strings(data)):
                _hide(f"{node.id} (caller values)", "entry", node.id,
                      "A first step reads the caller's values directly:")
    for var in definition.variables or []:
        name = getattr(var, "name", None) or (var.get("name") if isinstance(var, dict) else None)
        if name and name not in shown:
            _hide(str(name), "variable", None, "Declared run variable")
    findings.extend(hidden.values())

    reach = _reaches_output(definition)
    for node in definition.nodes:
        if is_write(node, registry) and node.id not in reach:
            findings.append(VisibleIoFinding(
                "hidden_write",
                f"Step '{node.label or node.id}' saves or changes something, but what it did never reaches "
                "an output step. Connect its result to an output step so the change is visible.",
                node_id=node.id, subject=node.spec_type,
            ))
    return findings
