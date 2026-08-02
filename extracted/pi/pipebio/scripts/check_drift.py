#!/usr/bin/env python3
"""Detect drift between the SDK and the server's OpenAPI contract + enums.

This performs two independent checks:

1. **Endpoint drift** (needs the OpenAPI spec): statically extracts every API
   path the SDK calls via ``self._session.<verb>(...)`` / ``self.session.<verb>``
   and compares them to the paths in the server's OpenAPI contract.
   * SDK endpoints that resolve to a concrete path but are absent from the spec
     are **failures** (a renamed/removed endpoint).
   * Spec endpoints the SDK does not wrap are **warnings** (new API surface).
   * SDK endpoints whose path cannot be resolved statically are **warnings**.

2. **Enum drift** (needs the everything checkout): verifies the committed,
   generated enum modules match what ``generate_models.py`` would produce from
   the canonical sources. A mismatch is a **failure**.

Inputs are optional so the script can run in different contexts:

* In the cross-repo sync workflow, both the spec and the everything checkout are
  available, so both checks run strictly.
* In the SDK's own push CI, neither may be present; by default the script then
  warns and exits 0. Pass ``--strict`` to require the inputs.

Usage:

    python scripts/check_drift.py [--spec PATH] [--everything-dir DIR] [--strict]
"""

import argparse
import ast
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = REPO_ROOT / "pipebio"
HTTP_VERBS = {"get", "post", "patch", "delete", "put"}

Endpoint = Tuple[str, str]  # (METHOD, normalized path)


def _normalize_path(path: str) -> str:
    """Normalise an API path for comparison.

    Strips query strings, a leading ``api/v2`` prefix and surrounding slashes,
    and collapses every ``{...}`` placeholder that occupies a whole path segment
    to ``{}`` so SDK templates and spec path parameters compare equal regardless
    of parameter names.

    An inline ``{...}`` glued to segment text (e.g. the SDK building
    ``f"sequences/import-signed-upload{query_string}"``) is not a path
    parameter - it is a dynamic suffix such as an appended query string. Real
    OpenAPI path parameters always occupy a complete segment, so such inline
    interpolations terminate the matchable path rather than becoming a spurious
    ``{}`` segment that can never match the contract.
    """
    path = path.split("?", 1)[0].strip()
    path = path.lstrip("/")
    for prefix in ("api/v2/", "api/v2"):
        if path.startswith(prefix):
            path = path[len(prefix):]
            break
    path = path.strip("/")
    out = []
    depth = 0
    segment_has_content = False
    for char in path:
        if char == "{":
            if depth == 0:
                if segment_has_content:
                    # Inline interpolation (e.g. an appended query string);
                    # treat it as the end of the matchable path.
                    break
                out.append("{}")
                segment_has_content = True
            depth += 1
        elif char == "}":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(char)
            segment_has_content = char != "/"
    return "".join(out).strip("/")


class _BaseEndpointVisitor(ast.NodeVisitor):
    """Shared resolver for SDK ``self._session.<verb>(...)`` endpoint calls.

    Resolves f-string/concatenation path templates using the enclosing class's
    ``self._url`` constant and simple local ``name = <path-ish>`` assignments.
    ``_local_vars`` is scoped to each function (cleared on entry and restored on
    exit) so an assignment in one method can never leak into another. Subclasses
    customise how unresolved calls are recorded via :meth:`_record_unresolved`.
    """

    def __init__(self, class_url: Optional[str] = None) -> None:
        self.resolved: Set[Endpoint] = set()
        self.unresolved: List[str] = []
        self._class_url: Optional[str] = class_url
        self._local_vars: Dict[str, Optional[str]] = {}

    def _resolve(self, node: Optional[ast.AST]) -> Optional[str]:
        """Best-effort resolution of an AST node to a path template string."""
        if node is None:
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name):
            return self._local_vars.get(node.id)
        if isinstance(node, ast.Attribute):
            # self._url / self.url -> the class url constant (if known).
            if node.attr in ("_url", "url") and isinstance(node.value, ast.Name) and node.value.id == "self":
                return self._class_url
            return None
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self._resolve(node.left)
            right = self._resolve(node.right)
            if left is not None and right is not None:
                return left + right
            return None
        if isinstance(node, ast.JoinedStr):  # f-string
            parts: List[str] = []
            for value in node.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    parts.append(value.value)
                elif isinstance(value, ast.FormattedValue):
                    resolved = self._resolve(value.value)
                    # Substitute resolvable expressions; otherwise leave a placeholder.
                    parts.append(resolved if resolved is not None else "{}")
                else:
                    parts.append("{}")
            return "".join(parts)
        return None

    def _visit_scoped_function(self, node: ast.AST) -> None:
        # A function introduces a fresh local-variable scope.
        previous = self._local_vars
        self._local_vars = {}
        self.generic_visit(node)
        self._local_vars = previous

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_scoped_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_scoped_function(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        # Track simple `name = <path-ish>` assignments for later resolution.
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            self._local_vars[node.targets[0].id] = self._resolve(node.value)
        self.generic_visit(node)

    def _record_unresolved(self, method: str, resolved: Optional[str]) -> None:
        """Record a call whose path could not be matched. Overridable."""
        self.unresolved.append(method)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if (
            isinstance(func, ast.Attribute)
            and func.attr in HTTP_VERBS
            and isinstance(func.value, ast.Attribute)
            and func.value.attr in ("_session", "session")
        ):
            method = func.attr.upper()
            first_arg = node.args[0] if node.args else None
            resolved = self._resolve(first_arg) if first_arg is not None else None
            normalized = _normalize_path(resolved) if resolved is not None else ""
            if normalized and not resolved.strip().startswith("{"):
                self.resolved.add((method, normalized))
            else:
                self._record_unresolved(method, resolved)
        self.generic_visit(node)


class _EndpointVisitor(_BaseEndpointVisitor):
    """Collect resolved and unresolved SDK endpoint call sites from one module."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        previous = self._class_url
        for stmt in ast.walk(node):
            # Capture `self._url = '<const>'` so {self._url} can be resolved.
            if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                for target in stmt.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and target.attr == "_url"
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        self._class_url = stmt.value.value
        self.generic_visit(node)
        self._class_url = previous

    def _record_unresolved(self, method: str, resolved: Optional[str]) -> None:
        if resolved is None:
            self.unresolved.append(f"{method} <unresolved>")
        else:
            # Whole path is dynamic (e.g. a fully-qualified URL variable).
            self.unresolved.append(f"{method} {resolved}")


def extract_sdk_endpoints(package_dir: Path) -> Tuple[Set[Endpoint], List[str]]:
    """Extract SDK endpoint call sites from every module in the package."""
    resolved: Set[Endpoint] = set()
    unresolved: List[str] = []
    for path in sorted(package_dir.rglob("*.py")):
        visitor = _EndpointVisitor()
        try:
            visitor.visit(ast.parse(path.read_text(encoding="utf-8")))
        except SyntaxError:
            continue
        resolved |= visitor.resolved
        unresolved.extend(visitor.unresolved)
    return resolved, unresolved


def extract_spec_endpoints(spec: Dict) -> Set[Endpoint]:
    """Extract ``(METHOD, normalized path)`` pairs from an OpenAPI document."""
    endpoints: Set[Endpoint] = set()
    for raw_path, item in (spec.get("paths") or {}).items():
        normalized = _normalize_path(raw_path)
        for method in item:
            if method.lower() in HTTP_VERBS:
                endpoints.add((method.upper(), normalized))
    return endpoints


def _load_generate_models():
    """Import the sibling generate_models module."""
    spec = importlib.util.spec_from_file_location(
        "generate_models", Path(__file__).resolve().parent / "generate_models.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _resolve_spec_path(explicit: Optional[str], everything_dir: Optional[Path]) -> Optional[Path]:
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    env_spec = os.environ.get("DRIFT_OPENAPI_SPEC")
    if env_spec:
        candidates.append(Path(env_spec))
    candidates.append(REPO_ROOT / "scripts" / "contract" / "swagger-spec.json")
    if everything_dir:
        candidates.append(everything_dir / "shared" / "openapi" / "swagger-spec.json")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="Path to the OpenAPI swagger-spec.json.")
    parser.add_argument("--everything-dir", help="Path to the everything repo checkout.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if the spec or everything checkout is unavailable.",
    )
    args = parser.parse_args()

    failures: List[str] = []
    warnings: List[str] = []

    everything_dir: Optional[Path] = None
    if args.everything_dir and Path(args.everything_dir).is_dir():
        everything_dir = Path(args.everything_dir).resolve()
    elif os.environ.get("EVERYTHING_DIR") and Path(os.environ["EVERYTHING_DIR"]).is_dir():
        everything_dir = Path(os.environ["EVERYTHING_DIR"]).resolve()
    elif (REPO_ROOT.parent / "everything").is_dir():
        everything_dir = (REPO_ROOT.parent / "everything").resolve()

    # --- Endpoint drift ---
    spec_path = _resolve_spec_path(args.spec, everything_dir)
    if spec_path is not None:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        sdk_endpoints, unresolved = extract_sdk_endpoints(PACKAGE_DIR)
        spec_endpoints = extract_spec_endpoints(spec)

        for method, path in sorted(sdk_endpoints):
            if (method, path) not in spec_endpoints:
                # Fail for any (method, path) the SDK calls that the spec does not
                # declare. This catches renamed/removed endpoints as well as calls
                # to a path under an HTTP method the contract does not expose.
                failures.append(f"SDK calls {method} /{path} but it is not in the OpenAPI contract.")

        for method, path in sorted(spec_endpoints - sdk_endpoints):
            warnings.append(f"OpenAPI endpoint {method} /{path} is not wrapped by the SDK.")
        for item in sorted(set(unresolved)):
            warnings.append(f"Could not statically resolve SDK call: {item}")
        print(f"Endpoint drift: checked {len(sdk_endpoints)} SDK endpoints against {len(spec_endpoints)} spec endpoints.")
    else:
        message = "OpenAPI spec not found; skipping endpoint drift check."
        (failures if args.strict else warnings).append(message)

    # --- Enum drift ---
    if everything_dir is not None:
        generate_models = _load_generate_models()
        outputs = generate_models._generate(everything_dir)
        for path, expected in outputs.items():
            actual = path.read_text(encoding="utf-8") if path.exists() else None
            if actual != expected:
                rel = path.relative_to(REPO_ROOT).as_posix()
                failures.append(f"Enum {rel} is out of sync with canonical source (run generate_models.py).")
        print(f"Enum drift: checked {len(outputs)} generated enum modules.")
    else:
        message = "everything checkout not found; skipping enum drift check."
        (failures if args.strict else warnings).append(message)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)

    if failures:
        print(f"\nDrift check failed with {len(failures)} error(s).", file=sys.stderr)
        return 1
    print("\nDrift check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
