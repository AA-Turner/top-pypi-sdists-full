#!/usr/bin/env python3
"""Inject API reference docs from the OpenAPI contract into SDK method docstrings.

The server's OpenAPI contract (``everything/shared/openapi/swagger-spec.json``,
vendored here as ``scripts/contract/swagger-spec.json``) carries human-authored
descriptions for every endpoint, path/query parameter and request-body field.
This script flows that text into the matching SDK method docstrings so the
generated API reference (``pdoc``) and IDE tooltips stay in sync with the
contract, without anyone hand-copying the descriptions.

How it works:

1. Load the OpenAPI spec (vendored snapshot, or a fallback inside an everything
   checkout) and index every operation by ``(VERB, normalized path)``.
2. Statically map each SDK ``Class.method`` to the endpoint(s) it calls via
   ``self._session.<verb>(...)`` (reusing the path resolution from
   ``check_drift.py``). Methods that resolve to exactly one endpoint are mapped
   automatically; methods that call several endpoints are disambiguated by the
   explicit ``METHOD_ENDPOINT_OVERRIDES`` map below.
3. Build an "API reference" text block from the operation (summary/description,
   parameters, request-body fields, resolving component ``$ref`` schemas).
4. Inject that block into the method's docstring between sentinel markers,
   preserving the hand-written Google-style content. Re-running replaces only
   the text between the markers, so the injection is idempotent.

Usage (from the repository root):

    python scripts/generate_docstrings.py                       # rewrite docstrings
    python scripts/generate_docstrings.py --check               # fail if stale
    python scripts/generate_docstrings.py --report              # print mapping only
    python scripts/generate_docstrings.py --everything-dir DIR  # locate the spec

The spec is located via (in order): ``--spec``, ``DRIFT_OPENAPI_SPEC``, the
vendored ``scripts/contract/swagger-spec.json``, then
``<everything>/shared/openapi/swagger-spec.json``.
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = REPO_ROOT / "pipebio"

# Sentinel markers delimiting the generated block inside a docstring. Everything
# between (and including) these lines is owned by this generator; the rest of
# the docstring is hand-written and never touched.
START_MARKER = ".. API reference (generated - do not edit) ::"
END_MARKER = ".. end API reference ::"

Endpoint = Tuple[str, str]  # (VERB, normalized path)

# Methods that call more than one endpoint and therefore cannot be mapped
# automatically. Each maps the SDK ``Class.method`` to the single endpoint whose
# docs should be surfaced. Keyed by ``(class_name, method_name)``.
METHOD_ENDPOINT_OVERRIDES: Dict[Tuple[str, str], Endpoint] = {
    # ``Jobs.list`` does a plain ``GET /jobs`` and, when filters are supplied, a
    # ``POST /jobs/_search``; document the primary list endpoint.
    ("Jobs", "list"): ("GET", "jobs"),
    # ``Jobs.upload_data_to_signed_url`` creates the signed upload
    # (``POST /sequences/signed-upload/{}``) and then uploads to it; document the
    # signed-upload creation that the SDK owns.
    ("Jobs", "upload_data_to_signed_url"): ("POST", "sequences/signed-upload/{}"),
}


def _load_check_drift():
    """Import the sibling check_drift module to reuse its path helpers."""
    spec = importlib.util.spec_from_file_location(
        "check_drift", Path(__file__).resolve().parent / "check_drift.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_check_drift = _load_check_drift()
_normalize_path = _check_drift._normalize_path
HTTP_VERBS = _check_drift.HTTP_VERBS


# --- Endpoint resolution (per enclosing function) --------------------------


class _FunctionEndpointVisitor(_check_drift._BaseEndpointVisitor):
    """Resolve the endpoint(s) a single method calls via ``self._session.<verb>``.

    Reuses the shared resolver in ``check_drift._BaseEndpointVisitor`` (seeded
    with the owning class's ``self._url`` constant so f-string templates such as
    ``f"{self._url}/{id}"`` resolve), keeping the two scripts in lock-step.
    """


def _class_url(class_node: ast.ClassDef) -> Optional[str]:
    """Find the ``self._url = '<const>'`` value declared anywhere in a class."""
    for stmt in ast.walk(class_node):
        if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
            for target in stmt.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and target.attr == "_url"
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    return stmt.value.value
    return None


# --- Spec indexing + block building ----------------------------------------


def _index_spec(spec: Dict) -> Dict[Endpoint, Tuple[str, Dict]]:
    """Map ``(VERB, normalized path)`` -> ``(raw path, operation)``."""
    index: Dict[Endpoint, Tuple[str, Dict]] = {}
    for raw_path, item in (spec.get("paths") or {}).items():
        normalized = _normalize_path(raw_path)
        for verb, operation in item.items():
            if verb.lower() in HTTP_VERBS and isinstance(operation, dict):
                index.setdefault((verb.upper(), normalized), (raw_path, operation))
    return index


def _deref(schema: Dict, spec: Dict) -> Dict:
    """Resolve a top-level ``$ref`` to its component schema (one level)."""
    if isinstance(schema, dict) and "$ref" in schema:
        name = schema["$ref"].split("/")[-1]
        return ((spec.get("components") or {}).get("schemas") or {}).get(name, {})
    return schema if isinstance(schema, dict) else {}


def _body_fields(operation: Dict, spec: Dict) -> List[Tuple[str, str, bool]]:
    """Return ``(name, description, required)`` for request-body properties."""
    request_body = operation.get("requestBody") or {}
    content = request_body.get("content") or {}
    schema: Optional[Dict] = None
    for media in content.values():
        if isinstance(media, dict) and "schema" in media:
            schema = media["schema"]
            break
    if not schema:
        return []
    schema = _deref(schema, spec)
    if schema.get("type") == "array":
        schema = _deref(schema.get("items") or {}, spec)
    properties = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    fields: List[Tuple[str, str, bool]] = []
    for name, definition in properties.items():
        description = ""
        if isinstance(definition, dict):
            description = (definition.get("description") or "").strip()
        fields.append((name, description, name in required))
    return fields


def build_api_block(verb: str, raw_path: str, operation: Dict, spec: Dict) -> List[str]:
    """Build the API reference block body (lines, unindented, no markers)."""
    lines: List[str] = [f"**{verb}** ``{raw_path}``"]

    summary = (operation.get("summary") or "").strip()
    description = (operation.get("description") or "").strip()
    if summary and description and summary != description:
        lines += ["", summary, "", description]
    elif description or summary:
        lines += ["", description or summary]

    parameters = operation.get("parameters") or []
    path_params = [p for p in parameters if isinstance(p, dict) and p.get("in") == "path"]
    query_params = [p for p in parameters if isinstance(p, dict) and p.get("in") == "query"]
    ordered = path_params + query_params
    if ordered:
        lines += ["", "API parameters:"]
        for parameter in ordered:
            name = parameter.get("name")
            location = parameter.get("in")
            param_description = (parameter.get("description") or "").strip()
            if param_description:
                lines.append(f"    * ``{name}`` ({location}) -- {param_description}")
            else:
                lines.append(f"    * ``{name}`` ({location})")

    fields = _body_fields(operation, spec)
    if fields:
        lines += ["", "API request body:"]
        for name, field_description, required in fields:
            suffix = "" if required else " (optional)"
            if field_description:
                lines.append(f"    * ``{name}``{suffix} -- {field_description}")
            else:
                lines.append(f"    * ``{name}``{suffix}")

    return lines


# --- Docstring injection ----------------------------------------------------


def _strip_existing_block(literal_lines: List[str]) -> List[str]:
    """Remove a previously generated marker block (and a leading blank)."""
    start = end = None
    for index, line in enumerate(literal_lines):
        stripped = line.strip()
        if stripped == START_MARKER and start is None:
            start = index
        elif stripped == END_MARKER:
            end = index
    if start is None or end is None or end < start:
        return literal_lines
    remove_from = start
    if remove_from > 0 and literal_lines[remove_from - 1].strip() == "":
        remove_from -= 1
    return literal_lines[:remove_from] + literal_lines[end + 1:]


def _rebuild_docstring(literal_lines: List[str], indent: str, content: List[str]) -> List[str]:
    """Return new docstring literal lines with the API block injected.

    ``literal_lines`` are the source lines (no trailing newline) spanning the
    docstring literal, from the opening quotes to the closing quotes.
    """
    literal_lines = _strip_existing_block(literal_lines)
    quote = '"""' if '"""' in literal_lines[-1] else "'''"

    block: List[str] = [indent + START_MARKER, ""]
    block += [(indent + line) if line else "" for line in content]
    block += ["", indent + END_MARKER]

    if len(literal_lines) == 1:
        # Single-line docstring: expand to multi-line, keeping the summary text.
        match = re.match(r'^(\s*)("""|\'\'\')(.*?)("""|\'\'\')\s*$', literal_lines[0])
        if match:
            inner = match.group(3)
            head = [f"{indent}{quote}{inner}".rstrip()]
            return head + [""] + block + [indent + quote]
        # Fall through for unusual quoting: append before the closing quote.
    head = literal_lines[:-1]
    closing = literal_lines[-1]
    if head and head[-1].strip() != "":
        head = head + [""]
    return head + block + [closing]


def _docstring_expr(function: ast.FunctionDef) -> Optional[ast.Expr]:
    if not function.body:
        return None
    first = function.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return first
    return None


def _iter_methods(tree: ast.Module):
    """Yield ``(class_name, class_url, function_node)`` for class methods."""
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            url = _class_url(node)
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    yield node.name, url, item


def _choose_endpoint(
    class_name: str,
    method_name: str,
    resolved: Set[Endpoint],
    warnings: List[str],
    location: str,
) -> Optional[Endpoint]:
    override = METHOD_ENDPOINT_OVERRIDES.get((class_name, method_name))
    if override is not None:
        return override
    if not resolved:
        return None
    if len(resolved) == 1:
        return next(iter(resolved))
    endpoints = ", ".join(f"{verb} /{path}" for verb, path in sorted(resolved))
    warnings.append(
        f"{location}: {class_name}.{method_name} calls multiple endpoints ({endpoints}); "
        f"add a METHOD_ENDPOINT_OVERRIDES entry to document one."
    )
    return None


def process_file(
    path: Path,
    spec_index: Dict[Endpoint, Tuple[str, Dict]],
    spec: Dict,
    warnings: List[str],
    report: List[str],
) -> str:
    """Return the rewritten source for one SDK module."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    relative = path.relative_to(REPO_ROOT).as_posix()

    edits: List[Tuple[int, int, List[str]]] = []
    for class_name, class_url, function in _iter_methods(tree):
        visitor = _FunctionEndpointVisitor(class_url)
        visitor.visit(function)
        endpoint = _choose_endpoint(class_name, function.name, visitor.resolved, warnings, relative)
        if endpoint is None:
            continue
        if endpoint not in spec_index:
            warnings.append(
                f"{relative}: {class_name}.{function.name} maps to {endpoint[0]} /{endpoint[1]} "
                f"which is not in the OpenAPI contract."
            )
            continue
        docstring_expr = _docstring_expr(function)
        if docstring_expr is None:
            warnings.append(
                f"{relative}: {class_name}.{function.name} has no docstring; skipping injection."
            )
            continue

        raw_path, operation = spec_index[endpoint]
        report.append(f"{relative}: {class_name}.{function.name} -> {endpoint[0]} {raw_path}")
        content = build_api_block(endpoint[0], raw_path, operation, spec)

        start_index = docstring_expr.lineno - 1
        end_index = docstring_expr.end_lineno - 1
        indent = " " * docstring_expr.col_offset
        rebuilt = _rebuild_docstring(lines[start_index:end_index + 1], indent, content)
        edits.append((start_index, end_index, rebuilt))

    for start_index, end_index, rebuilt in sorted(edits, key=lambda edit: edit[0], reverse=True):
        lines[start_index:end_index + 1] = rebuilt

    trailing_newline = "\n" if source.endswith("\n") else ""
    return "\n".join(lines) + trailing_newline


def _generate(spec_path: Path) -> Tuple[Dict[Path, str], List[str], List[str]]:
    """Return ``(path -> new text, warnings, report)`` for every SDK module."""
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec_index = _index_spec(spec)
    warnings: List[str] = []
    report: List[str] = []
    outputs: Dict[Path, str] = {}
    for path in sorted(PACKAGE_DIR.rglob("*.py")):
        try:
            new_text = process_file(path, spec_index, spec, warnings, report)
        except SyntaxError:
            continue
        if new_text != path.read_text(encoding="utf-8"):
            outputs[path] = new_text
    return outputs, warnings, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="Path to the OpenAPI swagger-spec.json.")
    parser.add_argument("--everything-dir", help="Path to the everything repo checkout.")
    parser.add_argument("--check", action="store_true", help="Fail if docstrings are stale.")
    parser.add_argument("--report", action="store_true", help="Print the method->endpoint mapping and exit.")
    args = parser.parse_args()

    everything_dir: Optional[Path] = None
    if args.everything_dir and Path(args.everything_dir).is_dir():
        everything_dir = Path(args.everything_dir).resolve()

    spec_path = _check_drift._resolve_spec_path(args.spec, everything_dir)
    if spec_path is None:
        print(
            "OpenAPI spec not found. Pass --spec, set DRIFT_OPENAPI_SPEC, vendor "
            "scripts/contract/swagger-spec.json, or pass --everything-dir.",
            file=sys.stderr,
        )
        return 1

    outputs, warnings, report = _generate(spec_path)

    if args.report:
        for line in sorted(report):
            print(line)
        for warning in warnings:
            print(f"WARNING: {warning}")
        print(f"\nMapped {len(report)} methods; {len(warnings)} warning(s).")
        return 0

    for warning in warnings:
        print(f"WARNING: {warning}")

    if args.check:
        stale = sorted(path.relative_to(REPO_ROOT).as_posix() for path in outputs)
        if stale:
            print(
                f"SDK docstrings are stale: {', '.join(stale)}. "
                f"Run `python scripts/generate_docstrings.py` and commit the result.",
                file=sys.stderr,
            )
            return 1
        print("SDK docstrings are up to date.")
        return 0

    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path.relative_to(REPO_ROOT).as_posix()}.")
    if not outputs:
        print("SDK docstrings already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
