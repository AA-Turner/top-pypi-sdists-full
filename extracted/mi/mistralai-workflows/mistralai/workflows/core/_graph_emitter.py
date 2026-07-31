"""Emit AtlasWireFormat from Python source or a live workflow class.

Source -> [_graph_builder] -> list[TreeNode] -> [_graph_flattener] -> flat dicts -> [_graph_emitter] -> AtlasWireFormat
                                                                                     ^ this module
"""

from __future__ import annotations

import ast
import dataclasses
import inspect
from pathlib import Path
from typing import Any, Callable, cast, get_type_hints

import structlog

from mistralai.workflows.core._graph_builder import (
    _apply_workflow_name_prefix,
    _ast_span,
    _build_import_symbol_table,
    _collect_connector_bindings,
    _collect_workflow_connectors_static,
    _collect_workflow_on_behalf_of_static,
    _connector_call_names,
    _DynamicResolver,
    _get_ast,
    _get_index,
    _is_workflow_cls_def,
    _module_bool_constants,
    _resolve_imported_connector_slot,
    _StaticResolver,
    _uses_connectors_decorator_names,
    _walk_body_tree,
    _workflow_define_name,
)
from mistralai.workflows.core._graph_flattener import (
    GraphValidationError,
    _flatten_tree,
    _validate_flat_graph,
)
from mistralai.workflows.core._graph_types import (
    _CONNECTORS_META_KEY,
    _MISTRALAI_PLUGIN_KEY,
    _PLUGIN_META_ATTR,
    _decorator_leaf_name,
    _FileIndex,
    _TreeCtx,
)
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.core.wire_format import AtlasWireFormat

logger = structlog.get_logger(__name__)

_HANDLER_ATTRS: frozenset[str] = frozenset({"signal", "update", "query"})


def _handler_name(node: ast.FunctionDef | ast.AsyncFunctionDef, dec: ast.expr) -> str:
    """Return the decorator's name= kwarg value if present, else the method name."""
    if isinstance(dec, ast.Call):
        for kw in dec.keywords:
            if kw.arg == "name":
                try:
                    return str(ast.literal_eval(kw.value))
                except (ValueError, SyntaxError):
                    return ast.unparse(kw.value)
    return node.name


def _non_self_params(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.arg]:
    return [a for a in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs) if a.arg != "self"]


def _handler_param_type(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    """Return the annotation of the first non-self parameter, or None."""
    params = _non_self_params(node)
    if params and params[0].annotation is not None:
        return ast.unparse(params[0].annotation)
    return None


def _entrypoint_param_fields(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, str]]:
    """Return structured param list [{name, type}] for all non-self params, or [] if none."""
    params = _non_self_params(node)
    if not params:
        return []
    return [{"name": p.arg, "type": ast.unparse(p.annotation) if p.annotation else "Any"} for p in params]


def _param_fields_to_summary(fields: list[dict[str, str]]) -> str:
    """Derive a human-readable summary string from structured param fields."""
    return ", ".join(
        f"{f['name']}: {f['type']}" + (f"  # {f['description']}" if "description" in f else "") for f in fields
    )


def _handler_return_type(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    """Return the function's return annotation, or None."""
    return ast.unparse(node.returns) if node.returns is not None else None


def _field_description_ast(value: ast.expr | None) -> str | None:
    """Extract description= from a Field(...) call, if present."""
    if not isinstance(value, ast.Call):
        return None
    for kw in value.keywords:
        if kw.arg == "description" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return None


def _type_fields_structured_ast(type_name: str, module_ast: ast.Module) -> list[dict[str, str]] | None:
    """Resolve a type name to its annotated fields via AST (no imports needed).

    Only searches top-level class definitions; nested classes and dotted type
    names (e.g. ``Config.Input``) are not resolved.
    """
    for node in module_ast.body:
        if isinstance(node, ast.ClassDef) and node.name == type_name:
            fields: list[dict[str, str]] = []
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    entry: dict[str, str] = {"name": stmt.target.id, "type": ast.unparse(stmt.annotation)}
                    desc = _field_description_ast(stmt.value)
                    if desc:
                        entry["description"] = desc
                    fields.append(entry)
            return fields if fields else None
    return None


def _type_fields_structured_runtime(cls: type) -> list[dict[str, str]] | None:
    """Extract structured fields from a Pydantic model or dataclass at runtime."""
    if dataclasses.is_dataclass(cls):
        try:
            hints = get_type_hints(cls)
        except NameError:
            hints = {}
        return [
            {"name": f.name, "type": _format_runtime_type(hints.get(f.name)) or "Any"} for f in dataclasses.fields(cls)
        ] or None

    model_fields = getattr(cls, "model_fields", None)
    if isinstance(model_fields, dict) and model_fields:
        fields: list[dict[str, str]] = []
        for name, f in model_fields.items():
            entry: dict[str, str] = {"name": name, "type": _format_runtime_type(f.annotation) or "Any"}
            desc = getattr(f, "description", None)
            if desc:
                entry["description"] = desc
            fields.append(entry)
        return fields

    return None


def _expand_single_param_fields(
    fields: list[dict[str, str]],
    module_ast: ast.Module,
    module_ns: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    """If fields is a single-param list whose type resolves to a structured class, expand it."""
    if len(fields) != 1:
        return fields
    type_name = fields[0]["type"]

    if module_ns is not None:
        try:
            param_cls = module_ns.get(type_name)
            if isinstance(param_cls, type):
                structured = _type_fields_structured_runtime(param_cls)
                if structured is not None:
                    return structured
        except (TypeError, AttributeError, KeyError):
            logger.debug("runtime type expansion failed", type_name=type_name, exc_info=True)

    structured = _type_fields_structured_ast(type_name, module_ast)
    if structured is not None:
        return structured

    return fields


def _scan_class_handlers(
    cls_def: ast.ClassDef, index: _FileIndex, file_offset: int = 0
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Scan a class AST for @workflow.signal(), @workflow.update(), @workflow.query() methods."""
    signals: list[dict[str, Any]] = []
    updates: list[dict[str, Any]] = []
    queries: list[dict[str, Any]] = []
    by_kind = {"signal": signals, "update": updates, "query": queries}
    for node in cls_def.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            dec_inner = dec.func if isinstance(dec, ast.Call) else dec
            if not isinstance(dec_inner, ast.Attribute) or dec_inner.attr not in _HANDLER_ATTRS:
                continue
            kind = dec_inner.attr
            begin, end = _ast_span(node, index)
            by_kind[kind].append(
                {
                    "kind": kind,
                    "name": _handler_name(node, dec),
                    "param_type": _handler_param_type(node),
                    "return_type": _handler_return_type(node),
                    "source_range": {"begin": file_offset + begin, "end": file_offset + end},
                }
            )
            break
    return signals, updates, queries


# Marker attribute (set by the @workflow.signal/update/query decorators) -> handler kind.
_HANDLER_DEF_ATTRS: dict[str, str] = {
    "__wf_signal_def": "signal",
    "__wf_update_def": "update",
    "__wf_query_def": "query",
}


def _format_runtime_type(annotation: object) -> str | None:
    """Render a resolved type hint as the same display string the AST scanner emits."""
    if annotation is None or annotation is type(None):
        return "None"
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def _collect_class_handlers_runtime(
    workflow_cls: type, cls_def: ast.ClassDef, index: _FileIndex
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Collect signal/update/query handlers from the live class via decorator metadata.

    Unlike _scan_class_handlers (static AST), this reads the authoritative runtime markers
    the decorators stamp on each handler wrapper, so it resolves dynamic handler names and
    sees handlers inherited from base classes. Source ranges are attached only for handlers
    defined directly in this class' file; inherited handlers carry no range.
    """
    signals: list[dict[str, Any]] = []
    updates: list[dict[str, Any]] = []
    queries: list[dict[str, Any]] = []
    by_kind = {"signal": signals, "update": updates, "query": queries}

    ast_methods: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {
        node.name: node for node in cls_def.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    seen: set[int] = set()
    for attr_name in dir(workflow_cls):
        try:
            member = getattr(workflow_cls, attr_name)
        except Exception:
            continue
        if id(member) in seen:
            continue

        for def_attr, kind in _HANDLER_DEF_ATTRS.items():
            handler_def = getattr(member, def_attr, None)
            if handler_def is None:
                continue
            seen.add(id(member))

            meta = getattr(member, "__wf_handler_meta", None)
            if meta is not None and meta.is_internal:
                break

            original = meta.original_func if meta is not None else member

            param_type: str | None = None
            if meta is not None and meta.user_params_dict:
                param_type = _format_runtime_type(next(iter(meta.user_params_dict.values())))

            try:
                return_type = _format_runtime_type(get_type_hints(original).get("return"))
            except Exception:
                return_type = None

            entry: dict[str, Any] = {
                "kind": kind,
                "name": handler_def.name,
                "param_type": param_type,
                "return_type": return_type,
            }
            ast_node = ast_methods.get(getattr(original, "__name__", ""))
            if ast_node is not None:
                begin, end = _ast_span(ast_node, index)
                entry["source_range"] = {"begin": begin, "end": end}

            by_kind[kind].append(entry)
            break

    def _sort_key(entry: dict[str, Any]) -> tuple[int, object]:
        sr = entry.get("source_range")
        return (0, sr["begin"]) if sr is not None else (1, entry["name"])

    for handlers in (signals, updates, queries):
        handlers.sort(key=_sort_key)

    return signals, updates, queries


def _find_entrypoint_method_ast(
    cls_def: ast.ClassDef,
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    """Find the workflow entrypoint method by @*.entrypoint decorator or name 'run'."""
    for node in cls_def.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            inner = dec.func if isinstance(dec, ast.Call) else dec
            if _decorator_leaf_name(inner) == "entrypoint":
                return node
    for node in cls_def.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "run":
            return node
    return None


def _collect_workflow_connectors_runtime(workflow_cls: type) -> list[str]:
    """Connector names declared on a workflow class via ``@uses_connectors(...)``."""
    metadata = getattr(workflow_cls, _PLUGIN_META_ATTR, None)
    if not isinstance(metadata, dict):
        return []
    mistralai_meta = metadata.get(_MISTRALAI_PLUGIN_KEY, {})
    entries = mistralai_meta.get(_CONNECTORS_META_KEY, []) if isinstance(mistralai_meta, dict) else []
    names: list[str] = []
    for entry in entries:
        name = entry.get("connector_name") if isinstance(entry, dict) else None
        if isinstance(name, str) and name not in names:
            names.append(name)
    return names


def build_graph_dynamically(workflow_cls: type) -> AtlasWireFormat:
    from mistralai.workflows.core.definition.workflow_definition import (
        _get_workflow_entrypoint_method,
    )

    file_path = inspect.getfile(workflow_cls)
    source_text = Path(file_path).read_text()
    sources: dict[str, str] = {file_path: source_text}
    asts: dict[str, ast.Module] = {}
    indices: dict[str, _FileIndex] = {}
    ast_tree = _get_ast(file_path, sources, asts)

    cls_def = next(
        (n for n in ast_tree.body if isinstance(n, ast.ClassDef) and n.name == workflow_cls.__name__),
        None,
    )
    if cls_def is None:
        raise ValueError(f"Class {workflow_cls.__name__} not found in {file_path}")

    entrypoint_fn = cast("Callable[..., Any] | None", _get_workflow_entrypoint_method(workflow_cls))
    if entrypoint_fn is None:
        raise ValueError(f"No entrypoint method for {workflow_cls.__name__}")

    ep_name = entrypoint_fn.__name__
    ep_def = next(
        (n for n in cls_def.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == ep_name),
        None,
    )
    if ep_def is None:
        raise ValueError(f"Entrypoint method {ep_name} not found in {workflow_cls.__name__}")

    workflow_name = get_workflow_definition(workflow_cls).name
    byte_len = len(source_text.encode("utf-8"))
    file_ranges: dict[str, dict[str, int]] = {file_path: {"begin": 0, "end": byte_len}}

    module_ns: dict[str, Any] = vars(inspect.getmodule(entrypoint_fn))
    resolver = _DynamicResolver(module_ns=module_ns, workflow_cls=workflow_cls)

    tree_nodes = _walk_body_tree(
        ep_def.body,
        resolver,
        sources,
        asts,
        indices,
        file_path,
        workflow_name,
        _TreeCtx(cls_def=cls_def, workflow_cls=workflow_cls),
        file_ranges,
    )

    index = _get_index(file_path, sources, asts, indices)
    ep_begin, ep_end = _ast_span(ep_def, index)
    cls_begin, cls_end = _ast_span(cls_def, index)
    output_type: str | None = ast.unparse(ep_def.returns) if ep_def.returns is not None else None
    ep_param_fields = _entrypoint_param_fields(ep_def)
    if ep_param_fields:
        ep_param_fields = _expand_single_param_fields(ep_param_fields, ast_tree, module_ns)
    ep_param_type = _param_fields_to_summary(ep_param_fields) if ep_param_fields else None

    signals, updates, queries = _collect_class_handlers_runtime(workflow_cls, cls_def, index)
    connectors = _collect_workflow_connectors_runtime(workflow_cls)
    on_behalf_of = bool(getattr(getattr(workflow_cls, "__workflows_workflow_def", None), "on_behalf_of", False))

    flat_nodes, flat_edges = _flatten_tree(
        tree_nodes,
        workflow_name,
        output_type,
        ep_name=ep_name,
        ep_begin=ep_begin,
        ep_end=ep_end,
        ep_line=ep_def.lineno,
        ep_end_line=ep_def.end_lineno,
        ep_param_type=ep_param_type,
        ep_param_fields=ep_param_fields,
        wf_begin=cls_begin,
        wf_end=cls_end,
        wf_line=cls_def.lineno,
    )
    _validate_flat_graph(workflow_name, flat_nodes, flat_edges)

    return AtlasWireFormat.model_validate(
        {
            "version": 3,
            "workflow_name": workflow_name,
            "sources": dict(sources),
            "files": file_ranges,
            "primary_file": next(iter(file_ranges), ""),
            "nodes": flat_nodes,
            "edges": flat_edges,
            "incomplete": False,
            "entrypoint": {"name": ep_name, "begin": ep_begin, "end": ep_end},
            "output_type": output_type,
            "signals": signals,
            "updates": updates,
            "queries": queries,
            "connectors": connectors,
            "on_behalf_of": on_behalf_of,
            "schedule": None,
        }
    )


def build_graph_statically(
    source: str,
    path: str,
    file_resolver: Callable[[str], str | None],
) -> list[AtlasWireFormat]:
    """Parse *source* and return one :class:`AtlasWireFormat` per workflow class found.

    ``path`` is the absolute path used for source-range anchoring and import resolution.
    ``file_resolver`` is called lazily with an absolute path and returns the source text
    of that file, or ``None`` when the file is unavailable.
    """
    try:
        module_ast = ast.parse(source)
    except SyntaxError:
        return []

    sources: dict[str, str] = {path: source}
    asts: dict[str, ast.Module] = {path: module_ast}
    indices: dict[str, _FileIndex] = {}
    symbols, symbol_names = _build_import_symbol_table(module_ast, path)
    connector_call_names = _connector_call_names(module_ast)
    connector_bindings = _collect_connector_bindings(module_ast, connector_call_names)
    uses_connectors_names = _uses_connectors_decorator_names(module_ast)
    bool_constants = _module_bool_constants(module_ast)

    def connector_slot_resolver(local_name: str) -> str | None:
        return _resolve_imported_connector_slot(local_name, symbols, symbol_names, file_resolver, sources, asts)

    results: list[AtlasWireFormat] = []

    for node in module_ast.body:
        if not isinstance(node, ast.ClassDef):
            continue
        if not _is_workflow_cls_def(node):
            continue

        cls_def = node
        workflow_name = _apply_workflow_name_prefix(_workflow_define_name(cls_def) or cls_def.name)
        ep_def = _find_entrypoint_method_ast(cls_def)
        if ep_def is None:
            continue

        byte_len = len(source.encode("utf-8"))
        file_ranges: dict[str, dict[str, int]] = {path: {"begin": 0, "end": byte_len}}

        index = _get_index(path, sources, asts, indices)
        ep_begin, ep_end = _ast_span(ep_def, index)
        cls_begin, cls_end = _ast_span(cls_def, index)
        output_type: str | None = ast.unparse(ep_def.returns) if ep_def.returns is not None else None
        ep_param_fields = _entrypoint_param_fields(ep_def)
        if ep_param_fields:
            ep_param_fields = _expand_single_param_fields(ep_param_fields, module_ast)
        ep_param_type = _param_fields_to_summary(ep_param_fields) if ep_param_fields else None

        resolver = _StaticResolver(
            symbols=symbols,
            symbol_names=symbol_names,
            file_resolver=file_resolver,
            cls_def=cls_def,
            file_path=path,
        )
        tree_nodes = _walk_body_tree(
            ep_def.body,
            resolver,
            sources,
            asts,
            indices,
            path,
            workflow_name,
            _TreeCtx(cls_def=cls_def),
            file_ranges,
        )

        file_offset = file_ranges[path]["begin"]
        signals, updates, queries = _scan_class_handlers(cls_def, index, file_offset)
        connectors = _collect_workflow_connectors_static(
            cls_def, connector_bindings, connector_call_names, uses_connectors_names, connector_slot_resolver
        )
        on_behalf_of = _collect_workflow_on_behalf_of_static(cls_def, bool_constants)

        flat_nodes, flat_edges = _flatten_tree(
            tree_nodes,
            workflow_name,
            output_type,
            ep_name=ep_def.name,
            ep_begin=ep_begin,
            ep_end=ep_end,
            ep_line=ep_def.lineno,
            ep_end_line=ep_def.end_lineno,
            ep_param_type=ep_param_type,
            ep_param_fields=ep_param_fields,
            wf_begin=cls_begin,
            wf_end=cls_end,
            wf_line=cls_def.lineno,
        )

        try:
            _validate_flat_graph(workflow_name, flat_nodes, flat_edges)
            incomplete = False
        except GraphValidationError:
            logger.exception("Graph validation failed", workflow_name=workflow_name)
            incomplete = True

        results.append(
            AtlasWireFormat.model_validate(
                {
                    "version": 3,
                    "workflow_name": workflow_name,
                    "sources": dict(sources),
                    "files": file_ranges,
                    "primary_file": next(iter(file_ranges), ""),
                    "nodes": flat_nodes,
                    "edges": flat_edges,
                    "incomplete": incomplete,
                    "entrypoint": {"name": ep_def.name, "begin": ep_begin, "end": ep_end},
                    "output_type": output_type,
                    "signals": signals,
                    "updates": updates,
                    "queries": queries,
                    "connectors": connectors,
                    "on_behalf_of": on_behalf_of,
                    "schedule": None,
                }
            )
        )

    return results
