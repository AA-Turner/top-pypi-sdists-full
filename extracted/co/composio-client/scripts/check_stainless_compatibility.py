"""Check an importable client or built wheel against Stainless 1.43's public contract.

Normal checks use the committed fixture and never install the Stainless wheel::

    uv run python scripts/check_stainless_compatibility.py
    uv run python scripts/check_stainless_compatibility.py --wheel dist/composio_client-2.0.0-py3-none-any.whl
"""

from __future__ import annotations

import argparse
import ast
import asyncio
import importlib
import inspect
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, cast, get_type_hints

from pydantic import BaseModel
from surface_docs import class_docs, doc_entry, field_docs_entry
from typing_extensions import get_overloads, is_typeddict
from wire_corpus import resolve_accessor

_PYTHON_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = _PYTHON_ROOT / "tests" / "fixtures" / "stainless_surface.json"


_LIST_SPELLING = re.compile(r"\bList\[")
_TYPING_PREFIX = re.compile(r"\btyping\.")
# Escape-aware: a member may contain the other quote, or an escaped one of
# its own, and a naive `[^']*` would end the literal early and fold the rest.
_STRING_LITERAL = re.compile(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"")


def _fold(fragment: str) -> str:
    return _TYPING_PREFIX.sub("", _LIST_SPELLING.sub("list[", fragment))


def canonical_annotation(value: str) -> str:
    """One spelling for both sides of an annotation comparison.

    Two differences are the renderer's spelling rather than a fidelity gap, and
    folding them is what lets the comparison report the rest:

    * The fixture captured ``List[...]`` because Stainless wrote ``typing.List``;
      the renderer emits the PEP 585 ``list[...]`` its aliases already use.
    * ``inspect.formatannotation`` strips ``typing.`` only when the *outermost*
      annotation belongs to ``typing``. Because ``list[...]`` is a builtin
      generic, a union nested inside one survives as ``typing.Union[...]`` on
      the emitted side and as ``Union[...]`` in the capture -- the same type,
      spelled two ways by one formatter.

    Neither is applied inside a string literal. A ``Literal['...']`` member is
    data, not a type: rewriting it would make ``Literal['List[str]']`` and
    ``Literal['list[str]']`` -- two different accepted values -- compare equal.
    That is the same mistake the ordering scan makes if it reads inside a
    literal, and it is excluded here for the same reason.

    Nothing else is folded: a difference that survives this is a real one.
    """
    folded: list[str] = []
    end = 0
    for literal in _STRING_LITERAL.finditer(value):
        folded.append(_fold(value[end : literal.start()]))
        folded.append(literal.group())
        end = literal.end()
    folded.append(_fold(value[end:]))
    return "".join(folded)


def declares_no_annotation(value: str | None) -> bool:
    """Whether an expectation says nothing at all.

    ``Any`` is exactly what the renderer emits when the capture holds no
    annotation, so an expectation of ``Any`` -- in any spelling ``typing``
    permits -- agrees with the flattened tree built from that same absence, and
    the regression is certified rather than caught.

    Only the *whole* annotation counts. ``Dict[str, Any]`` and ``Optional[Any]``
    are annotations the oracle may legitimately declare, and neither is what a
    lost capture produces; rejecting them would fail a faithful fixture.
    """
    return not value or canonical_annotation(value) == "Any"


_SESSION_TYPES = "composio_client.types.tool_router"
_APPROVAL_ONLY = "approval-only variant added upstream in the 2026-10 spec refresh"

#: Captured unions the spec gave a new object variant after 1.43.0, keyed by the
#: field that declares the union, with the captured member the addition follows
#: and the class the generator appends for it (``python-types.ts``'s
#: ``widenUnion``). A payload that is only the new variant's fields has to land
#: on a class of its own; declaring each one here keeps that widening reviewed
#: rather than silent. An entry the emitted annotation no longer shows is
#: reported, so the ledger cannot rot.
UPSTREAM_UNION_ADDITIONS: dict[tuple[str, str, str], tuple[str, str, str]] = {
    **{
        (f"{_SESSION_TYPES}.{module}", f"{prefix}Config", field): (
            f"{prefix}Config{after}",
            f"{prefix}Config{added}",
            _APPROVAL_ONLY,
        )
        for module, prefix in (
            ("session_attach_response", ""),
            ("session_create_response", ""),
            ("session_patch_response", ""),
            ("session_retrieve_response", ""),
            ("session_config_history_response", "Item"),
        )
        for field, after, added in (
            ("toolkits", "ToolkitsDisabled", "ToolkitsRequireApproval"),
            ("tools", "ToolsTags", "ToolsRequireApproval"),
        )
    },
    **{
        (f"{_SESSION_TYPES}.{module}", root, field): (after, added, _APPROVAL_ONLY)
        for module, root in (
            ("session_create_params", "SessionCreateParams"),
            ("session_patch_params", "SessionPatchParams"),
        )
        for field, after, added in (
            ("toolkits", "ToolkitsDisable", "ToolkitsRequireApproval"),
            ("tools", "ToolsTags", "ToolsRequireApproval"),
        )
    },
}


# Apollo added createHint/updateHint to session tag arrays in October 2026.
# Keep every captured value and declare only these reviewed collection fields.
UPSTREAM_FIELD_LITERAL_ADDITIONS: set[tuple[str, str, str]] = {
    *(
        (f"{_SESSION_TYPES}.{module}", f"{prefix}{name}", field)
        for module, prefix in (
            ("session_attach_response", ""),
            ("session_create_response", ""),
            ("session_patch_response", ""),
            ("session_retrieve_response", ""),
            ("session_config_history_response", "Item"),
        )
        for name in ("ConfigTags", "ConfigToolsTagsTags")
        for field in ("enabled", "disabled")
    ),
    *(
        (f"{_SESSION_TYPES}.{module}", name, field)
        for module in ("session_create_params", "session_patch_params")
        for name in ("TagsUnionMember1", "ToolsTagsTagsUnionMember1")
        for field in ("enable", "disable")
    ),
    *(
        (f"{_SESSION_TYPES}.{module}", name, "tags")
        for module, root in (
            ("session_create_params", "SessionCreateParams"),
            ("session_patch_params", "SessionPatchParams"),
        )
        for name in (root, "ToolsTags")
    ),
}


def expected_annotation(module: str, name: str, field: str, annotation: str) -> str:
    """The frozen declaration with its declared union additions appended.

    The addition is written after the captured member it follows, so it lands
    in the same ``Union[...]`` at whatever depth that union sits.
    """
    if (module, name, field) in UPSTREAM_FIELD_LITERAL_ADDITIONS:
        annotation = annotation.replace("'openWorldHint'", "'openWorldHint', 'createHint', 'updateHint'", 1)
    addition = UPSTREAM_UNION_ADDITIONS.get((module, name, field))
    if addition is None:
        return annotation
    after, added, _reason = addition
    return re.sub(rf"\b{re.escape(f'{module}.{after}')}\b", f"{module}.{after}, {module}.{added}", annotation)


def absent_union_addition(module: str, name: str, field: str, captured: str, found: str | None) -> str | None:
    """The problem a declared union addition is when the emitted field lacks it.

    Covers both ways an entry goes stale: the emitted annotation is the captured
    one again, or the captured member the entry follows is not in the capture.
    """
    addition = UPSTREAM_UNION_ADDITIONS.get((module, name, field))
    if addition is None:
        return None
    declared = canonical_type(canonical_annotation(expected_annotation(module, name, field, captured)))
    frozen = canonical_type(canonical_annotation(captured))
    if declared != frozen and (found is None or canonical_type(found) != frozen):
        return None
    return f"{module}.{name}.{field}: declared union addition {addition[1]} ({addition[2]}) is absent"


def expected_request_annotation(module: str, name: str, field: str, annotation: str) -> str:
    """Apply reviewed upstream request changes to the frozen declaration."""
    if (module, name, field) == (
        "composio_client.types.trigger_instances.manage_update_params",
        "ManageUpdateParams",
        "status",
    ):
        return annotation.replace("Required[", "NotRequired[", 1)
    return expected_annotation(module, name, field, annotation)


def _qualified(value: type[Any]) -> str:
    return f"{value.__module__}.{value.__name__}"


def _default(value: object, empty: object, omit_type: type[Any], not_given_type: type[Any]) -> dict[str, Any]:
    if value is empty:
        return {"kind": "required"}
    if isinstance(value, omit_type):
        return {"kind": "sentinel", "value": "OMIT"}
    if isinstance(value, not_given_type):
        return {"kind": "sentinel", "value": "NOT_GIVEN"}
    if value is None or isinstance(value, (str, int, float, bool, list, dict)):
        return {"kind": "value", "value": value}
    return {"kind": "object", "type": _qualified(type(value))}


def _annotation_text(annotation: object) -> str | None:
    if annotation is inspect.Parameter.empty:
        return None
    return annotation if isinstance(annotation, str) else inspect.formatannotation(annotation)


def _checked_parameters(value: Any) -> list[inspect.Parameter]:
    """The parameters a type checker resolves a Stainless-shaped call against.

    A method whose call forms cannot share one signature carries ``@overload``
    stubs, and the first is the Stainless shape. The implementation behind them
    accepts the pre-release forms too, so it declares every flat field optional
    -- reading it would hide exactly the required-ness this gate compares.
    """
    function = getattr(value, "__func__", value)
    overloads = get_overloads(function)
    if not overloads:
        return list(inspect.signature(value).parameters.values())
    parameters = list(inspect.signature(overloads[0]).parameters.values())
    return parameters[1:] if hasattr(value, "__self__") else parameters


def _signature(value: Any, omit_type: type[Any], not_given_type: type[Any]) -> dict[str, Any]:
    signature = inspect.signature(value)
    return {
        "parameters": {
            parameter.name: {
                "kind": parameter.kind.name,
                "default": _default(parameter.default, inspect.Parameter.empty, omit_type, not_given_type),
                "annotation": _annotation_text(parameter.annotation),
            }
            for parameter in _checked_parameters(value)
        },
        "return": None
        if signature.return_annotation is inspect.Signature.empty
        else str(signature.return_annotation).strip("'"),
        "coroutine": inspect.iscoroutinefunction(value),
    }


def _symbol(value: Any) -> dict[str, Any]:
    if is_typeddict(value):
        description, field_descriptions = class_docs(value)
        return {
            "kind": "typed_dict",
            "annotations": {
                name: canonical_annotation(inspect.formatannotation(annotation))
                for name, annotation in get_type_hints(value, include_extras=True).items()
            },
            "required": sorted(value.__required_keys__),
            "constructs_mapping": isinstance(value(), dict),
            **doc_entry(description),
            **field_docs_entry(field_descriptions),
        }
    if inspect.isclass(value) and issubclass(value, BaseModel):
        description, field_descriptions = class_docs(value)
        return {
            "kind": "model",
            "root_model": bool(getattr(value, "__pydantic_root_model__", False)),
            **doc_entry(description),
            "serialization_helpers": all(
                callable(getattr(value, name, None)) for name in ("to_dict", "to_json")
            ),
            # An incomplete model carries unresolved ``ForwardRef``s, which would
            # hand the comparison the renderer's own spelling instead of a type.
            "complete": bool(getattr(value, "__pydantic_complete__", False)),
            "fields": {
                name: {
                    "alias": None if field.alias is None else str(field.alias),
                    "required": field.is_required(),
                    "annotation": canonical_annotation(inspect.formatannotation(field.annotation)),
                    **doc_entry(field_descriptions.get(name)),
                }
                for name, field in value.model_fields.items()
            },
        }
    if inspect.isclass(value):
        return {"kind": "class", "bases": [base.__name__ for base in value.__bases__]}
    return {"kind": "alias", "value_type": type(value).__name__}


def capture_importable(fixture: dict[str, Any]) -> dict[str, Any]:
    """Capture only public observations named by the frozen fixture."""
    import composio_client
    from composio_client import AsyncComposio, Composio, NoAuth
    from composio_client._types import NotGiven, Omit

    snapshot: dict[str, Any] = {
        "module": str(Path(composio_client.__file__ or "?").resolve()),
        "root_exports": list(getattr(composio_client, "__all__", [])),
        "root_attributes": sorted(name for name in fixture["root_exports"] if hasattr(composio_client, name)),
        "errors": {},
        "clients": {},
        "compatibility_imports": {},
        "type_modules": {},
    }
    for name in fixture["errors"]:
        value = getattr(composio_client, name, None)
        snapshot["errors"][name] = (
            None if not inspect.isclass(value) else {"bases": [base.__name__ for base in value.__bases__]}
        )

    for lane, client_type in (("sync", Composio), ("async", AsyncComposio)):
        expected_client = fixture["clients"][lane]
        client = client_type(auth=NoAuth(), base_url="https://client.invalid")
        resources: dict[str, Any] = {}
        try:
            methods = {
                name: _signature(getattr(client_type, name), Omit, NotGiven)
                for name in expected_client["methods"]
                if hasattr(client_type, name)
            }
            leftovers: list[str] = []
            for path, expected_resource in expected_client["resources"].items():
                relocated = RESOURCE_RELOCATIONS.get(path)
                if relocated is not None:
                    original = resolve_accessor(client, tuple(path.split(".")))
                    leftovers.extend(
                        f"{path}.{name}" for name in expected_resource["methods"] if hasattr(original, name)
                    )
                resource = resolve_accessor(client, tuple((relocated or path).split(".")))
                if resource is None:
                    continue
                groups: dict[str, Any] = {}
                for group, target in (
                    ("methods", resource),
                    ("raw_methods", resource.with_raw_response),
                    ("streaming_methods", resource.with_streaming_response),
                ):
                    groups[group] = {
                        name: _signature(getattr(target, name), Omit, NotGiven)
                        for name in expected_resource[group]
                        if hasattr(target, name)
                    }
                resources[path] = groups
            snapshot["clients"][lane] = {
                "methods": methods,
                "resources": resources,
                "relocated_leftovers": leftovers,
            }
        finally:
            if lane == "sync":
                cast(Composio, client).close()
            else:
                asyncio.run(cast(AsyncComposio, client).close())

    for module_name, expected_names in fixture["compatibility_imports"].items():
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001 - import failures belong in the report
            snapshot["compatibility_imports"][module_name] = {"error": f"{type(exc).__name__}: {exc}"}
            continue
        snapshot["compatibility_imports"][module_name] = [
            name for name in expected_names if hasattr(module, name)
        ]

    for module_name, expected_module in fixture["type_modules"].items():
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001 - import failures belong in the report
            snapshot["type_modules"][module_name] = {"error": f"{type(exc).__name__}: {exc}"}
            continue
        snapshot["type_modules"][module_name] = {
            "exports": list(getattr(module, "__all__", [])),
            "symbols": {
                name: _symbol(getattr(module, name))
                for name in expected_module["exports"]
                if hasattr(module, name)
            },
        }
    return snapshot


#: Parameters the frozen 1.43.0 surface declares that upstream removed from
#: the spec afterwards, so our generated methods no longer accept them. Each
#: entry names the upstream fact; a parameter that reappears while its entry
#: stands is reported as unexpected, so the ledger cannot silently rot.
UPSTREAM_PARAMETER_REMOVALS: dict[tuple[tuple[str, str], str], str] = {
    (("connected_accounts", "create"), "validate_credentials"): (
        "removed upstream with the auth-config scope rework in the 2026-08 spec refresh"
    ),
    (("connected_accounts", "refresh"), "validate_credentials"): (
        "removed upstream with the auth-config scope rework in the 2026-08 spec refresh"
    ),
}


#: Constructor and derivation keywords the frozen 1.43.0 surface declares that
#: this client removed on purpose, each with the release that removed it and the
#: migration. Client methods carry the label ``client``. A keyword that
#: reappears while its entry stands is reported, so the carve-out cannot
#: outlive the removal it declares.
CLIENT_PARAMETER_REMOVALS: dict[tuple[tuple[str, str], str], str] = {
    (("client", "__init__"), "api_key"): (
        "2.0.0-rc.18 removed `api_key` for `auth=ProjectAuth(key)` (python/README.md, "
        "'Removed in 2.0.0-rc.18'; the TypeScript twin is ledger entry client-options-api-key-removed)"
    ),
    (("client", "with_options"), "api_key"): (
        "2.0.0-rc.18 removed `with_options(api_key=)` for `with_options(auth=ProjectAuth(key))` "
        "(python/README.md, 'Removed in 2.0.0-rc.18')"
    ),
    (("client", "__init__"), "default_query"): (
        "2.0.0-rc.19 removed `default_query`: generated methods own their query and the raw methods "
        "take one (python/README.md, 'Removed in 2.0.0-rc.19')"
    ),
    (("client", "with_options"), "default_query"): "2.0.0-rc.19 removed `default_query` (python/README.md)",
    (
        ("client", "with_options"),
        "set_default_query",
    ): "2.0.0-rc.19 removed `set_default_query` (python/README.md)",
}


#: Root exports and client methods the frozen 1.43.0 surface declares that this
#: client removed on purpose in 2.0.0-rc.20, because they existed only to mirror
#: the Stainless build. One that reappears while its entry stands is reported.
_RC20_STAINLESS_ONLY = (
    "2.0.0-rc.20 removed it as Stainless-only structure (python/README.md, 'Removed in 2.0.0-rc.20')"
)
ROOT_EXPORT_REMOVALS: dict[str, str] = {
    name: _RC20_STAINLESS_ONLY
    for name in (
        "Stream",
        "AsyncStream",
        "DefaultAioHttpClient",
        "ProxiesTypes",
        "Transport",
        "DEFAULT_CONNECTION_LIMITS",
        "Client",
        "AsyncClient",
    )
}
CLIENT_METHOD_REMOVALS: dict[str, str] = {
    "copy": "2.0.0-rc.20 removed `copy`; `with_options` is the one spelling"
}

#: Resources whose 1.43.0 methods moved under ``client._internal`` in
#: 2.0.0-rc.22, because the spec tags their operations ``x-internal``. Each is
#: checked at its new path against the same frozen signatures: only where it is
#: reached changed. One still answering at its old path is reported.
RESOURCE_RELOCATIONS: dict[str, str] = {
    path: f"_internal.{path}" for path in ("cli", "cli.realtime", "logs.tools", "logs.triggers")
}


#: Parameters whose captured ``Literal`` the spec widened after 1.43.0, with the
#: members it added. The generator appends them (``python-annotations.ts``'s
#: ``widenLiterals``), because a value the API accepts must not be a type error;
#: declaring each one here keeps that widening reviewed rather than silent. An
#: entry the annotation no longer shows is reported, so the ledger cannot rot.
UPSTREAM_LITERAL_ADDITIONS: dict[tuple[tuple[str, str], str], tuple[tuple[str, ...], str]] = {
    (("session", "execute_meta"), "slug"): (
        ("COMPOSIO_SUBMIT_FEEDBACK", "COMPOSIO_PROXY_EXECUTE"),
        "added upstream to the meta-tool enum after the 1.43.0 capture",
    ),
}

#: Methods whose *return annotation* departs from the frozen 1.43.0 surface,
#: with the name they return now. Only the plain ``methods`` group is compared:
#: the capture records the wrapped method's return for the raw and streaming
#: twins, where this client spells ``APIResponse[...]``, so those two groups
#: have no comparable expectation.
#:
#: The three session entries are the accepted 2.0 contract (issue #67).
#: The spec turned those responses into unions discriminated on ``result_type``.
#: The ``...Response`` name stays the captured class -- downstream code
#: subclasses and constructs it -- while ``blocked`` and ``input_required``
#: have their own classes. Methods return the complete ``...Result`` union.
#:
#: An entry whose method returns the captured annotation again is reported, and
#: so is one that returns anything but the name declared here, so the ledger
#: cannot rot.
UPSTREAM_RETURN_DEPARTURES: dict[tuple[str, str], tuple[str, str]] = {
    ("session", "execute"): (
        "SessionExecuteResult",
        "discriminated on result_type since the 2026-10 spec refresh (composio-client#67)",
    ),
    ("session", "execute_meta"): (
        "SessionExecuteMetaResult",
        "discriminated on result_type since the 2026-10 spec refresh (composio-client#67)",
    ),
    ("session", "proxy_execute"): (
        "SessionProxyExecuteResult",
        "discriminated on result_type since the 2026-10 spec refresh (composio-client#67)",
    ),
    ("auth_configs", "update"): (
        "AuthConfigUpdateResponse",
        "1.43.0 returned a bare object; the spec declares the response and the owned client types it",
    ),
    ("auth_configs", "update_status"): (
        "AuthConfigUpdateStatusResponse",
        "1.43.0 returned a bare object; the spec declares the response and the owned client types it",
    ),
}

_TYPE_SPELLINGS = {
    "Dict": "dict",
    "typing.Dict": "dict",
    "List": "list",
    "typing.List": "list",
    "typing.Iterable": "Iterable",
    "collections.abc.Iterable": "Iterable",
    "Optional": "Optional",
    "typing.Optional": "Optional",
    "Union": "Union",
    "typing.Union": "Union",
    "Literal": "Literal",
    "typing.Literal": "Literal",
    "typing_extensions.Literal": "Literal",
    "NoneType": "None",
}


def _canonical_union(members: list[Any]) -> Any:
    flat = frozenset(
        inner
        for member in members
        for inner in (member[1] if isinstance(member, tuple) and member[0] == "union" else (member,))
    )
    return next(iter(flat)) if len(flat) == 1 else ("union", flat)


def _canonical(node: ast.expr) -> Any:
    if isinstance(node, ast.Call):
        # Annotated metadata is compared as syntax, never evaluated.
        return ("metadata", ast.dump(node, include_attributes=False))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return _canonical_union([_canonical(node.left), _canonical(node.right)])
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return _canonical(ast.parse(node.value, mode="eval").body)
    if isinstance(node, ast.Constant) and node.value is None:
        return "None"
    if isinstance(node, (ast.Name, ast.Attribute)):
        spelled = ast.unparse(node)
        return _TYPE_SPELLINGS.get(spelled, spelled)
    if isinstance(node, ast.Subscript):
        head = _TYPE_SPELLINGS.get(ast.unparse(node.value), ast.unparse(node.value))
        args = list(node.slice.elts) if isinstance(node.slice, ast.Tuple) else [node.slice]
        if head == "Optional":
            return _canonical_union([_canonical(args[0]), "None"])
        if head == "Union":
            return _canonical_union([_canonical(arg) for arg in args])
        if head == "Literal":
            return _canonical_union([("literal", repr(ast.literal_eval(arg))) for arg in args])
        return (head, tuple(_canonical(arg) for arg in args))
    raise ValueError(f"cannot read the annotation {ast.unparse(node)!r}")


def canonical_type(text: str) -> Any:
    """A parameter annotation by meaning rather than by spelling.

    The capture is spelled the way Stainless wrote it (``Optional[List[...]]``);
    a resource module must be spelled the PEP 604 / 585 way ``ruff`` requires
    (``list[...] | None``). This reads both into one structure -- unions as
    sets, ``Literal`` members as values, ``Dict``/``List`` as their builtins --
    so the comparison sees a difference in *type* and nothing else. It parses
    the text itself rather than sharing the generator's spelling rules, so a
    rule the generator got wrong cannot agree with itself here.
    """
    return _canonical(ast.parse(text, mode="eval").body)


def render_type(value: Any) -> str:
    """One readable spelling of a :func:`canonical_type`, members sorted."""
    if isinstance(value, str):
        return value
    if value[0] == "union":
        return " | ".join(sorted(render_type(member) for member in value[1]))
    if value[0] == "literal":
        return f"Literal[{value[1]}]"
    return f"{value[0]}[{', '.join(render_type(arg) for arg in value[1])}]"


def _ledger_key(label: str) -> tuple[str, str] | None:
    """``(resource, method)`` for a ``lane.path.method[.streaming]`` label."""
    trimmed = label[: -len(".streaming")] if label.endswith(".streaming") else label
    parts = trimmed.split(".")
    return (parts[-2], parts[-1]) if len(parts) >= 3 else None


def _compare_typing(label: str, name: str, expected: dict[str, Any], found: dict[str, Any]) -> list[str]:
    """A resource parameter keeps the oracle's type and required-ness."""
    problems: list[str] = []
    # September 2026: trigger updates also accept egress-only changes.
    optional_status = _ledger_key(label) == ("manage", "update") and name == "status"
    if optional_status and found["default"] != {"kind": "sentinel", "value": "OMIT"}:
        problems.append(f"{label}.{name}: upstream optional status must default to OMIT")
    if (
        not optional_status
        and expected["default"]["kind"] == "required"
        and found["default"]["kind"] != "required"
    ):
        problems.append(f"{label}.{name}: expected a required parameter, found default {found['default']}")
    declared = canonical_type(expected["annotation"])
    actual = None if found.get("annotation") is None else canonical_type(found["annotation"])
    if optional_status:
        declared = _canonical_union([declared, "Omit"])
    key = _ledger_key(label)
    addition = None if key is None else UPSTREAM_LITERAL_ADDITIONS.get((key, name))
    if addition is not None:
        if actual == declared:
            problems.append(
                f"{label}.{name}: declared Literal addition {list(addition[0])} ({addition[1]}) is absent"
            )
        declared = _canonical_union([declared, *(("literal", repr(value)) for value in addition[0])])
    if actual != declared:
        found_text = "no annotation" if actual is None else render_type(actual)
        problems.append(f"{label}.{name}: expected type {render_type(declared)}, found {found_text}")
    return problems


def _removal_for(label: str, parameter: str) -> str | None:
    """The ledger entry for a `(lane.)path.method[.streaming]` label + parameter."""
    key = _ledger_key(label)
    if key is None:
        return None
    return UPSTREAM_PARAMETER_REMOVALS.get((key, parameter)) or CLIENT_PARAMETER_REMOVALS.get(
        (key, parameter)
    )


def _compare_return(label: str, expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    """A resource method returns what the oracle's did, or a declared departure."""
    key = _ledger_key(label)
    departure = None if key is None else UPSTREAM_RETURN_DEPARTURES.get(key)
    declared = expected["return"]
    found = actual["return"]
    if departure is not None:
        if found == declared:
            return [f"{label}: declared return departure {departure[0]} ({departure[1]}) is absent"]
        declared = departure[0]
    return [] if found == declared else [f"{label}: expected return {declared}, found {found}"]


def _compare_signature(
    label: str,
    expected: dict[str, Any],
    actual: dict[str, Any] | None,
    *,
    resource: bool,
) -> list[str]:
    if actual is None:
        return [f"missing method {label}"]
    problems: list[str] = []
    for parameter in expected["parameters"]:
        name = parameter["name"]
        found = actual["parameters"].get(name)
        if found is None:
            if _removal_for(label, name) is not None:
                continue
            problems.append(f"{label}: missing parameter {name}")
            continue
        if found["kind"] != parameter["kind"]:
            problems.append(f"{label}.{name}: expected {parameter['kind']}, found {found['kind']}")
        expected_default = parameter["default"]
        if expected_default["kind"] != "required" and found["default"] != expected_default:
            problems.append(f"{label}.{name}: expected default {expected_default}, found {found['default']}")
        if resource:
            problems.extend(_compare_typing(label, name, parameter, found))
    for ((path, method), parameter), reason in (
        *UPSTREAM_PARAMETER_REMOVALS.items(),
        *CLIENT_PARAMETER_REMOVALS.items(),
    ):
        if _ledger_key(label) == (path, method) and parameter in actual["parameters"]:
            problems.append(f"{label}: parameter {parameter} is declared removed ({reason}) but is present")
    if label.endswith(".streaming") and actual["coroutine"]:
        problems.append(f"{label}: streaming context factory must not be a coroutine function")
    return problems


def compare_snapshot(fixture: dict[str, Any], snapshot: dict[str, Any]) -> list[str]:
    """Return every subtraction from the frozen public contract."""
    problems: list[str] = []
    root_exports = set(snapshot["root_exports"])
    root_attributes = set(snapshot["root_attributes"])
    for name in fixture["root_exports"]:
        removal = ROOT_EXPORT_REMOVALS.get(name)
        if removal is None:
            if name not in root_exports or name not in root_attributes:
                problems.append(f"missing root export {name}")
        elif name in root_exports or name in root_attributes:
            problems.append(f"root export {name} is declared removed ({removal}) but is present")

    for name, expected in fixture["errors"].items():
        actual = snapshot["errors"].get(name)
        if actual is None:
            problems.append(f"missing public error {name}")
        elif not set(expected["bases"]).issubset(actual["bases"]):
            problems.append(f"{name}: expected base(s) {expected['bases']}, found {actual['bases']}")

    for lane in ("sync", "async"):
        expected_client = fixture["clients"][lane]
        actual_client = snapshot["clients"].get(lane, {"methods": {}, "resources": {}})
        for name, expected_method in expected_client["methods"].items():
            removal = CLIENT_METHOD_REMOVALS.get(name)
            if removal is not None:
                if name in actual_client["methods"]:
                    problems.append(f"{lane}.client.{name} is declared removed ({removal}) but is present")
                continue
            problems.extend(
                _compare_signature(
                    f"{lane}.client.{name}",
                    expected_method,
                    actual_client["methods"].get(name),
                    resource=False,
                )
            )
        for leftover in actual_client.get("relocated_leftovers", []):
            problems.append(f"{lane}.{leftover} is declared moved under `_internal` but is still present")
        for path, expected_resource in expected_client["resources"].items():
            actual_resource = actual_client["resources"].get(path)
            if actual_resource is None:
                problems.append(f"{lane}: missing resource {path}")
                continue
            for group in ("methods", "raw_methods", "streaming_methods"):
                actual_group = actual_resource.get(group)
                if actual_group is None:
                    problems.append(f"{lane}.{path}: missing {group}")
                    continue
                for name, expected_method in expected_resource[group].items():
                    suffix = ".streaming" if group == "streaming_methods" else ""
                    actual_method = actual_group.get(name)
                    problems.extend(
                        _compare_signature(
                            f"{lane}.{path}.{name}{suffix}",
                            expected_method,
                            actual_method,
                            resource=True,
                        )
                    )
                    if group == "methods" and actual_method is not None:
                        problems.extend(
                            _compare_return(f"{lane}.{path}.{name}", expected_method, actual_method)
                        )

    for module_name, expected_names in fixture["compatibility_imports"].items():
        actual_names = snapshot["compatibility_imports"].get(module_name)
        if not isinstance(actual_names, list):
            problems.append(f"missing compatibility module {module_name}")
            continue
        for name in expected_names:
            if name not in actual_names:
                problems.append(f"{module_name}: missing compatibility import {name}")

    for module_name, expected_module in fixture["type_modules"].items():
        actual_module = snapshot["type_modules"].get(module_name)
        if actual_module is None or "error" in actual_module:
            problems.append(f"missing type module {module_name}")
            continue
        for name in expected_module["exports"]:
            if name not in actual_module["exports"] or name not in actual_module["symbols"]:
                problems.append(f"{module_name}: missing export {name}")
                continue
            expected_symbol = expected_module["symbols"][name]
            actual_symbol = actual_module["symbols"][name]
            if actual_symbol["kind"] != expected_symbol["kind"]:
                problems.append(
                    f"{module_name}.{name}: expected {expected_symbol['kind']}, found {actual_symbol['kind']}"
                )
                continue
            expected_description = expected_symbol.get("description")
            if expected_description is not None and actual_symbol.get("description") != expected_description:
                problems.append(f"{module_name}.{name}: class docstring changed")
            if expected_symbol["kind"] == "typed_dict":
                if not actual_symbol["constructs_mapping"]:
                    problems.append(f"{module_name}.{name}: parameter alias is not constructible")
                missing = set(expected_symbol["annotations"]) - set(actual_symbol["annotations"])
                if missing:
                    problems.append(f"{module_name}.{name}: missing field(s) {sorted(missing)}")
                for field_name, annotation in expected_symbol["annotations"].items():
                    if declares_no_annotation(annotation):
                        problems.append(f"{module_name}.{name}.{field_name}: fixture declares no annotation")
                        continue
                    declared = canonical_annotation(
                        expected_request_annotation(module_name, name, field_name, annotation)
                    )
                    found = actual_symbol["annotations"].get(field_name)
                    absent = absent_union_addition(module_name, name, field_name, annotation, found)
                    if absent is not None:
                        problems.append(absent)
                    if found is None or canonical_type(found) != canonical_type(declared):
                        problems.append(
                            f"{module_name}.{name}.{field_name}: expected annotation {declared}, "
                            f"found {found}"
                        )
                for field_name, description in expected_symbol.get("descriptions", {}).items():
                    if actual_symbol.get("descriptions", {}).get(field_name) != description:
                        problems.append(f"{module_name}.{name}.{field_name}: field docstring changed")
            elif expected_symbol["kind"] == "model":
                if actual_symbol["root_model"]:
                    problems.append(f"{module_name}.{name}: response unexpectedly requires .root")
                if not actual_symbol.get("serialization_helpers"):
                    problems.append(f"{module_name}.{name}: missing response serialization helpers")
                if not actual_symbol.get("complete"):
                    problems.append(f"{module_name}.{name}: model annotations did not resolve")
                for field_name, expected_field in expected_symbol["fields"].items():
                    actual_field = actual_symbol["fields"].get(field_name)
                    if actual_field is None:
                        problems.append(f"{module_name}.{name}: missing response field {field_name}")
                        continue
                    if (actual_field["alias"], actual_field["required"]) != (
                        expected_field["alias"],
                        expected_field["required"],
                    ):
                        problems.append(f"{module_name}.{name}.{field_name}: field metadata changed")
                    # An expectation of nothing is a problem, never a match.
                    # The renderer emits `Any` for an uncaptured annotation, so
                    # an expectation that is absent -- or is itself `Any` --
                    # would agree with the flattened tree it produced, and the
                    # regression would be certified rather than caught. That is
                    # how the original one survived its gates.
                    if declares_no_annotation(expected_field.get("annotation")):
                        problems.append(f"{module_name}.{name}.{field_name}: fixture declares no annotation")
                        continue
                    declared = canonical_annotation(
                        expected_annotation(module_name, name, field_name, expected_field["annotation"])
                    )
                    absent = absent_union_addition(
                        module_name,
                        name,
                        field_name,
                        expected_field["annotation"],
                        actual_field["annotation"],
                    )
                    if absent is not None:
                        problems.append(absent)
                    if canonical_type(actual_field["annotation"]) != canonical_type(declared):
                        problems.append(
                            f"{module_name}.{name}.{field_name}: expected annotation {declared}, "
                            f"found {actual_field['annotation']}"
                        )
                    expected_field_description = expected_field.get("description")
                    if (
                        expected_field_description is not None
                        and actual_field.get("description") != expected_field_description
                    ):
                        problems.append(f"{module_name}.{name}.{field_name}: field docstring changed")
    return problems


def snapshot_from_wheel(wheel: Path) -> dict[str, Any]:
    completed = subprocess.run(  # noqa: S603
        [
            "uv",
            "run",
            "--isolated",
            "--no-project",
            "--refresh-package",
            "composio-client",
            "--with",
            str(wheel.resolve()),
            "python",
            str(Path(__file__).resolve()),
            "--dump",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(f"stainless compatibility: could not inspect {wheel}\n{completed.stderr.strip()}")
    return cast(dict[str, Any], json.loads(completed.stdout))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump", action="store_true", help="dump the importable package as JSON")
    parser.add_argument("--wheel", type=Path, help="inspect this wheel in an isolated environment")
    args = parser.parse_args(argv)
    fixture = cast(dict[str, Any], json.loads(FIXTURE_PATH.read_text(encoding="utf-8")))

    if args.dump:
        json.dump(capture_importable(fixture), sys.stdout, sort_keys=True)
        return 0

    snapshot = snapshot_from_wheel(args.wheel) if args.wheel else capture_importable(fixture)
    problems = compare_snapshot(fixture, snapshot)
    if problems:
        print(f"stainless compatibility: {len(problems)} problem(s) in {snapshot['module']}")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(f"stainless compatibility: Stainless 1.43 contract preserved in {snapshot['module']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
