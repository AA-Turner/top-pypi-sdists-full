"""Hardcoded auto-injection tool catalogue — discover + validate against tool_def.

Some tool names are wired into the platform in Python (structured-input
``_editable_tools``, capability bundles, context manifest context/context_patch
tools, web-search substitution, …) rather than coming from an agent definition or a DB surface
manifest. This module AST-scans the known source files, unions every hardcoded
name, and validates each resolves in the live ``tool_def`` catalogue.

Used by ``scripts/validate_tools.py`` (release), ``aidream/startup/tools_check.py``
(boot), and ``scripts/list_hardcoded_injection_tools.py`` (operator listing).
"""

from __future__ import annotations

import ast
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from matrx_utils import vcprint

Extractor = Callable[[Path], set[str]]

# Tool-like names: lowercase snake_case, at least one underscore OR known short names.
_SHORT_TOOL_NAMES = frozenset(
    {
        "context",
        "data",
        "dataset",
        "document",
        "note",
        "picklist",
        "skill",
        "sql",
        "task",
        "workbook",
    }
)


def find_repo_root(start: Path | None = None) -> Path:
    """Walk parents until the monorepo root (pyproject.toml + aidream/) is found."""
    here = (start or Path(__file__)).resolve()
    for parent in (here, *here.parents):
        if (parent / "pyproject.toml").is_file() and (parent / "aidream").is_dir():
            return parent
    # Standalone matrx-ai install — fall back to cwd.
    return Path.cwd()


def _is_tool_name(s: str) -> bool:
    if not s or not s[0].isalpha() or not s.replace("_", "").isalnum():
        return False
    if s in _SHORT_TOOL_NAMES:
        return True
    return "_" in s and s.islower()


def _strings_in_frozenset_call(node: ast.Call) -> set[str]:
    if not (
        isinstance(node.func, ast.Name)
        and node.func.id == "frozenset"
        and node.args
        and isinstance(node.args[0], ast.Set)
    ):
        return set()
    out: set[str] = set()
    for elt in node.args[0].elts:
        if (
            isinstance(elt, ast.Constant)
            and isinstance(elt.value, str)
            and _is_tool_name(elt.value)
        ):
            out.add(elt.value)
    return out


def _strings_in_tuple_or_list(node: ast.expr) -> set[str]:
    if not isinstance(node, (ast.Tuple, ast.List)):
        return set()
    out: set[str] = set()
    for elt in node.elts:
        if (
            isinstance(elt, ast.Constant)
            and isinstance(elt.value, str)
            and _is_tool_name(elt.value)
        ):
            out.add(elt.value)
    return out


def _extract_frozenset_literals(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            out.update(_strings_in_frozenset_call(node))
    return out


def _extract_registered_tool_spec_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "RegisteredToolSpec":
            for kw in node.keywords:
                if (
                    kw.arg == "name"
                    and isinstance(kw.value, ast.Constant)
                    and isinstance(kw.value.value, str)
                    and _is_tool_name(kw.value.value)
                ):
                    out.add(kw.value.value)
        if isinstance(func, ast.Attribute) and func.attr == "RegisteredToolSpec":
            for kw in node.keywords:
                if (
                    kw.arg == "name"
                    and isinstance(kw.value, ast.Constant)
                    and isinstance(kw.value.value, str)
                    and _is_tool_name(kw.value.value)
                ):
                    out.add(kw.value.value)
    return out


def _names_from_named_value(node: ast.AST, var_name: str, value: ast.expr) -> set[str]:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == var_name:
                return _strings_in_tuple_or_list(value)
    if (
        isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == var_name
    ):
        return _strings_in_tuple_or_list(value)
    return set()


def _extract_named_tuple(path: Path, var_name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            val = node.value if isinstance(node, ast.AnnAssign) else node.value
            if val is not None:
                out.update(_names_from_named_value(node, var_name, val))
    return out


def _extract_named_frozenset(path: Path, var_name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var_name:
                    if isinstance(node.value, ast.Call):
                        out.update(_strings_in_frozenset_call(node.value))
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == var_name
        ):
            if isinstance(node.value, ast.Call):
                out.update(_strings_in_frozenset_call(node.value))
    return out


def _extract_string_constant_assigns(path: Path, var_names: frozenset[str]) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in var_names:
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        if _is_tool_name(node.value.value):
                            out.add(node.value.value)
    return out


def _dict_name_strings(d: ast.Dict) -> set[str]:
    out: set[str] = set()
    for key, val in zip(d.keys, d.values, strict=False):
        if (
            isinstance(key, ast.Constant)
            and key.value == "name"
            and isinstance(val, ast.Constant)
            and isinstance(val.value, str)
            and _is_tool_name(val.value)
        ):
            out.add(val.value)
    return out


def _extract_dict_literal_name(path: Path, dict_var: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id == dict_var
                    and isinstance(node.value, ast.Dict)
                ):
                    out.update(_dict_name_strings(node.value))
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == dict_var
            and isinstance(node.value, ast.Dict)
        ):
            out.update(_dict_name_strings(node.value))
    return out


def _extract_db_grant_tool_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "tool_name":
                    if isinstance(node.value, ast.IfExp):
                        for branch in (node.value.body, node.value.orelse):
                            if isinstance(branch, ast.Constant) and isinstance(branch.value, str):
                                if _is_tool_name(branch.value):
                                    out.add(branch.value)
    return out


def _extract_queue_tool_changes_remove(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        is_qtc = (isinstance(func, ast.Attribute) and func.attr == "queue_tool_changes") or (
            isinstance(func, ast.Name) and func.id == "queue_tool_changes"
        )
        if not is_qtc:
            continue
        for kw in node.keywords:
            if kw.arg == "remove":
                out.update(_strings_in_tuple_or_list(kw.value))
    return out


def _extract_editable_tools_frozensets(path: Path) -> set[str]:
    """Only ``_editable_tools`` field defaults (non-empty tool frozensets)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "field"):
            continue
        for kw in node.keywords:
            if kw.arg != "default":
                continue
            if isinstance(kw.value, ast.Call):
                out.update(_strings_in_frozenset_call(kw.value))
    return out


# Sources that INTRODUCE tool names in code (not pass-through / not DB-driven).
# Paths are repo-relative from the monorepo root.
INJECTION_SOURCES: dict[str, Extractor] = {
    "packages/matrx-ai/matrx_ai/config/structured_input_config.py": _extract_editable_tools_frozensets,
    # NOTE: these live under aidream/services/* after the 2026-07-06 service-layer
    # extraction (the old aidream/api/utils/* paths are import shims — file exists
    # but the tool-name constants moved out, so an AST scan of the shim yields
    # nothing). Point at the REAL file; the empty-source guard below screams if any
    # of these is ever gutted to a shim again.
    "aidream/services/conversation_context/context_utils.py": lambda p: _extract_string_constant_assigns(
        p, frozenset({"_CTX", "_CTX_PATCH"})
    ),
    "aidream/services/tooling/tool_merge.py": lambda p: _extract_named_tuple(
        p, "USER_DATA_DEFAULT_TOOLS"
    )
    | _extract_registered_tool_spec_names(p),
    "packages/matrx-ai/matrx_ai/capabilities/built_in.py": _extract_registered_tool_spec_names,
    "aidream/api/client_capabilities.py": _extract_registered_tool_spec_names,
    "aidream/services/db_grants/injection.py": _extract_db_grant_tool_names,
    "packages/matrx-ai/matrx_ai/capabilities/browser_dom.py": _extract_registered_tool_spec_names,
    "packages/matrx-ai/matrx_ai/tools/implementations/browser_discovery.py": lambda p: (
        _extract_frozenset_literals(p) | _extract_queue_tool_changes_remove(p)
    ),
    "packages/matrx-ai/matrx_ai/tools/vfs_routing.py": lambda p: _extract_dict_literal_name(
        p, "FS_EDIT_TOOL_DEFINITION"
    ),
    "aidream/services/ai_execution/realtime_tools.py": lambda p: _extract_named_frozenset(
        p, "BUILTIN_REALTIME_TOOLS"
    ),
}

# Per-source names that are hardcoded but intentionally NOT ``tool_def`` rows.
# Example: xAI native realtime session builtins — provider-side, not our registry.
SOURCE_REGISTRY_EXEMPT: dict[str, frozenset[str]] = {
    "aidream/services/ai_execution/realtime_tools.py": frozenset({"web_search", "x_search"}),
}

INJECTION_SOURCES_NOT_COVERED: tuple[str, ...] = (
    "aidream/services/tooling/surface_resolver.py — default tools from DB (tool_surface_defaults)",
    "packages/matrx-ai/matrx_ai/capabilities/browser_dom.py — enabled_tools_factory bulk from registry/DB bindings (only load_chrome_tools is in INJECTION_SOURCES)",
    "packages/matrx-ai/matrx_ai/tools/registry.py — _maybe_inject_fs_edit (reads FS_EDIT_TOOL_DEFINITION; vfs_routing is covered)",
    "packages/matrx-ai/matrx_ai/tools/dynamic_drain.py — rehydrates queue_tool_changes at runtime",
    "packages/matrx-ai/matrx_ai/tools/implementations/bundle_lister.py — names from registry at runtime",
    "aidream/services/tooling/skill_merge.py — skill allowed_tools are DB UUIDs",
    "Request/API fields (tools, excluded_tools, user.add/remove) — intentional caller strings",
    "Pass-through only: structured_input_resolver.py, context_utils grant_tool_name (sourced from db_grants/injection.py)",
)


@dataclass(frozen=True)
class InjectionValidationResult:
    missing: list[str]
    missing_by_source: dict[str, list[str]] = field(default_factory=dict)
    by_source: dict[str, frozenset[str]] = field(default_factory=dict)
    all_names: frozenset[str] = frozenset()
    checked_count: int = 0
    live_count: int = 0
    missing_source_files: tuple[str, ...] = ()
    # Source files that EXIST but yielded ZERO tool names. Every INJECTION_SOURCES
    # entry is listed precisely because it introduces at least one name, so an
    # empty extraction means the file was gutted (typically to an import shim in a
    # service-layer move) and the drift guard has gone BLIND to whatever names it
    # used to cover — a silent-degradation hole distinct from an outright-missing
    # file. This is the layer-2 backstop that turns that silence into a scream.
    empty_sources: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.missing and not self.missing_source_files and not self.empty_sources


def collect_hardcoded_injection_tool_names(
    *,
    repo_root: Path | None = None,
) -> dict[str, frozenset[str]]:
    """Return repo-relative source path -> tool names hardcoded for auto-injection."""
    root = repo_root or find_repo_root()
    by_file: dict[str, frozenset[str]] = {}
    for rel, extractor in INJECTION_SOURCES.items():
        path = root / rel
        if not path.is_file():
            by_file[rel] = frozenset()
            continue
        by_file[rel] = frozenset(extractor(path))
    return by_file


def hardcoded_injection_tool_names(*, repo_root: Path | None = None) -> frozenset[str]:
    """Union of every hardcoded auto-injection tool name across INJECTION_SOURCES."""
    names: set[str] = set()
    for file_names in collect_hardcoded_injection_tool_names(repo_root=repo_root).values():
        names.update(file_names)
    return frozenset(names)


def _sources_for_tool(tool_name: str, by_source: dict[str, frozenset[str]]) -> list[str]:
    return sorted(rel for rel, names in by_source.items() if tool_name in names)


def validate_injection_tool_catalog(
    live_tool_names: set[str],
    *,
    repo_root: Path | None = None,
    emit: bool = False,
) -> InjectionValidationResult:
    """Verify hardcoded auto-injection tool names resolve in the live tool_def catalogue."""
    root = repo_root or find_repo_root()
    by_source = collect_hardcoded_injection_tool_names(repo_root=root)
    missing_source_files = tuple(
        sorted(rel for rel in INJECTION_SOURCES if not (root / rel).is_file())
    )
    # A file that EXISTS but yields no names = the guard went blind on that source
    # (gutted to a shim, renamed constant, changed literal shape). Missing files
    # are the standalone-matrx-ai case (aidream paths absent) and are reported
    # separately — never conflated with a live-but-empty source.
    empty_sources = tuple(
        sorted(rel for rel, names in by_source.items() if (root / rel).is_file() and not names)
    )

    missing_by_source: dict[str, list[str]] = {}
    missing_set: set[str] = set()
    checked: set[str] = set()

    for rel, names in by_source.items():
        exempt = SOURCE_REGISTRY_EXEMPT.get(rel, frozenset())
        for name in names:
            if name in exempt:
                continue
            checked.add(name)
            if name not in live_tool_names:
                missing_set.add(name)
                missing_by_source.setdefault(rel, []).append(name)

    for rel in missing_by_source:
        missing_by_source[rel].sort()

    missing = sorted(missing_set)
    result = InjectionValidationResult(
        missing=missing,
        missing_by_source=missing_by_source,
        by_source=by_source,
        all_names=hardcoded_injection_tool_names(repo_root=root),
        checked_count=len(checked),
        live_count=len(live_tool_names),
        missing_source_files=missing_source_files,
        empty_sources=empty_sources,
    )
    if emit and not result.ok:
        emit_injection_validation_banner(result)
    elif emit and result.ok:
        vcprint(
            "  ✔ Hardcoded auto-injection tools all resolve in tool_def.",
            color="green",
        )
    return result


def format_injection_validation_banner(result: InjectionValidationResult) -> str:
    """Human-readable red banner for missing injection-catalog tools."""
    bar = "█" * 78
    lines: list[str] = [
        "",
        bar,
        "🚨  HARDCODED AUTO-INJECTION TOOLS — names not in tool_def  🚨",
        (
            f"   {len(result.missing)} tool name(s) hardcoded in Python for auto-injection "
            f"do not resolve in the live tool_def catalogue."
        ),
        f"   checked={result.checked_count}   live tool_def rows={result.live_count}",
        bar,
    ]
    for name in result.missing:
        sources = _sources_for_tool(name, result.by_source)
        src = ", ".join(sources) if sources else "?"
        lines.append(f"   ● {name}   (hardcoded in {src})")
    if result.missing_source_files:
        lines.append("")
        lines.append(f"   ⚠ {len(result.missing_source_files)} expected source file(s) missing:")
        for rel in result.missing_source_files:
            lines.append(f"      - {rel}")
    if result.empty_sources:
        lines.append("")
        lines.append(
            f"   🕳 {len(result.empty_sources)} source file(s) exist but yielded ZERO "
            "tool names — the guard has gone BLIND on them (gutted to a shim? "
            "renamed constant? changed literal shape?). Repoint INJECTION_SOURCES "
            "to the file that now holds the names, or fix the extractor:"
        )
        for rel in result.empty_sources:
            lines.append(f"      - {rel}")
    lines += [
        "",
        "   FIX: update the hardcoded name in the source file(s) above to the grouped",
        "   successor that exists in tool_def (dataset, picklist, note, task, web, …).",
        "   Reference: db/migrations/_repoint_agents_to_grouped_tools.py::successor()",
        "   List all:  uv run python scripts/list_hardcoded_injection_tools.py --by-file",
        bar,
        "",
    ]
    return "\n".join(lines)


def emit_injection_validation_banner(result: InjectionValidationResult) -> None:
    vcprint(format_injection_validation_banner(result), color="red")
