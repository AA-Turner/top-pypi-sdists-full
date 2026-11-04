"""Capture the public Python surface of the frozen Stainless client.

Run this script only in an isolated environment containing
``composio-client==1.43.0``::

    uv run --isolated --no-project --with composio-client==1.43.0 \
      python scripts/capture_stainless_surface.py

The committed fixture is an offline compatibility oracle. Normal tests read it;
they never install Stainless or use the network.
"""

from __future__ import annotations

import importlib
import inspect
import json
import pkgutil
import sys
import typing
from collections.abc import Callable, Mapping
from pathlib import Path
from types import ModuleType
from typing import Any, cast

from pydantic import BaseModel
from surface_docs import class_docs, doc_entry, field_docs_entry

ORACLE_VERSION = "1.43.0"
FIXTURE_PATH = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "stainless_surface.json"
CLIENT_METHODS = (
    "__init__",
    "__enter__",
    "__exit__",
    "__aenter__",
    "__aexit__",
    "close",
    "copy",
    "with_options",
    "request",
    "get",
    "post",
    "put",
    "patch",
    "delete",
)
COMPATIBILITY_IMPORTS = {
    "composio_client._base_client": ("DEFAULT_MAX_RETRIES",),
    "composio_client._types": ("SequenceNotStr",),
}


def _annotation(value: object) -> str | None:
    if value is inspect.Signature.empty:
        return None
    if isinstance(value, str):
        return value
    return inspect.formatannotation(value)


def _property_info_repr(value: Any) -> str:
    arguments = ", ".join(
        f"{name}={attribute!r}"
        for name in ("alias", "format", "format_template", "discriminator")
        if (attribute := getattr(value, name)) is not None
    )
    return f"{type(value).__name__}({arguments})"


def _default(value: object) -> dict[str, Any]:
    if value is inspect.Signature.empty:
        return {"kind": "required"}
    type_name = type(value).__name__
    if type_name == "Omit":
        return {"kind": "sentinel", "value": "OMIT"}
    if type_name == "NotGiven":
        return {"kind": "sentinel", "value": "NOT_GIVEN"}
    if value is None or isinstance(value, (bool, int, float, str, list, dict)):
        return {"kind": "value", "value": value}
    if isinstance(value, tuple):
        return {"kind": "value", "value": list(value)}
    raise TypeError(f"surface capture: unsupported default {value!r} ({type_name})")


def _signature(callable_: Callable[..., object]) -> dict[str, Any]:
    signature = inspect.signature(callable_, eval_str=False)
    return {
        "parameters": [
            {
                "name": parameter.name,
                "kind": parameter.kind.name,
                "annotation": _annotation(parameter.annotation),
                "default": _default(parameter.default),
            }
            for parameter in signature.parameters.values()
        ],
        "return": _annotation(signature.return_annotation),
    }


def _declared_methods(instance: object) -> dict[str, dict[str, Any]]:
    methods: dict[str, dict[str, Any]] = {}
    for name in instance.__class__.__dict__:
        if name.startswith("_"):
            continue
        value = getattr(instance, name)
        if callable(value):
            methods[name] = _signature(value)
    return dict(sorted(methods.items()))


def _resource_surface(client: Any, resource_base: type[Any]) -> dict[str, Any]:
    resources: dict[str, Any] = {}
    seen: set[int] = set()

    def walk(resource: Any, prefix: tuple[str, ...]) -> None:
        if id(resource) in seen:
            return
        seen.add(id(resource))
        path = ".".join(prefix)
        raw = resource.with_raw_response
        streaming = resource.with_streaming_response
        methods = _declared_methods(resource)
        resources[path] = {
            "class": f"{resource.__class__.__module__}.{resource.__class__.__name__}",
            "methods": methods,
            "raw_class": f"{raw.__class__.__module__}.{raw.__class__.__name__}",
            "raw_methods": {name: _signature(getattr(raw, name)) for name in methods},
            "streaming_class": f"{streaming.__class__.__module__}.{streaming.__class__.__name__}",
            "streaming_methods": {name: _signature(getattr(streaming, name)) for name in methods},
        }
        for name in sorted(dir(resource)):
            if name.startswith("_"):
                continue
            value = getattr(resource, name)
            if isinstance(value, resource_base):
                walk(value, (*prefix, name))

    for name in sorted(dir(client)):
        if name.startswith("_"):
            continue
        value = getattr(client, name)
        if isinstance(value, resource_base):
            walk(value, (name,))
    return dict(sorted(resources.items()))


def _client_surface(client_class: Any, resource_base: type[Any]) -> dict[str, Any]:
    client = client_class(api_key="surface-oracle", base_url="https://client.invalid")
    try:
        return {
            "class": f"{client_class.__module__}.{client_class.__name__}",
            "methods": {
                name: _signature(getattr(client_class, name))
                for name in CLIENT_METHODS
                if hasattr(client_class, name)
            },
            "resources": _resource_surface(client, resource_base),
        }
    finally:
        # Neither constructor dispatches. Closing the async client returns a
        # coroutine, which is deliberately closed rather than awaited: capture
        # needs no event loop and owns no opened response.
        close = client.close
        result = close()
        if inspect.iscoroutine(result):
            result.close()


def _typed_dict(value: object) -> dict[str, Any] | None:
    is_typed_dict = typing.is_typeddict(value) or (
        inspect.isclass(value) and hasattr(value, "__required_keys__") and hasattr(value, "__optional_keys__")
    )
    if not is_typed_dict:
        return None
    annotations: Mapping[str, object] = typing.get_type_hints(value, include_extras=True)
    constructor = cast(Callable[[], object], value)
    description, field_descriptions = class_docs(cast(type[Any], value))
    return {
        "kind": "typed_dict",
        "annotations": {name: _annotation(annotation) for name, annotation in annotations.items()},
        "required_keys": sorted(getattr(value, "__required_keys__", ())),
        "optional_keys": sorted(getattr(value, "__optional_keys__", ())),
        "constructs_mapping": isinstance(constructor(), dict),
        **doc_entry(description),
        **field_docs_entry(field_descriptions),
    }


def _model(value: object) -> dict[str, Any] | None:
    if not inspect.isclass(value) or not issubclass(value, BaseModel):
        return None
    description, field_descriptions = class_docs(value)
    return {
        "kind": "model",
        "root_model": bool(getattr(value, "__pydantic_root_model__", False)),
        **doc_entry(description),
        "fields": {
            name: {
                "annotation": _annotation(field.annotation),
                "alias": field.alias,
                "required": field.is_required(),
                **doc_entry(field_descriptions.get(name)),
            }
            for name, field in value.model_fields.items()
        },
    }


def _symbol(value: object) -> dict[str, Any]:
    typed_dict = _typed_dict(value)
    if typed_dict is not None:
        return typed_dict
    model = _model(value)
    if model is not None:
        return model
    if inspect.isclass(value):
        return {"kind": "class", "bases": [base.__name__ for base in value.__bases__]}
    return {"kind": "alias", "value": _annotation(value)}


def _module_surface(module: ModuleType) -> dict[str, Any]:
    exported = list(getattr(module, "__all__", ()))
    return {
        "exports": exported,
        "symbols": {name: _symbol(getattr(module, name)) for name in exported},
    }


def _types_surface(types_module: ModuleType) -> dict[str, Any]:
    modules = sorted(
        entry.name for entry in pkgutil.walk_packages(types_module.__path__, f"{types_module.__name__}.")
    )
    return {name: _module_surface(importlib.import_module(name)) for name in modules}


def _errors(root: ModuleType) -> dict[str, Any]:
    errors: dict[str, Any] = {}
    for name in root.__all__:
        value = getattr(root, name)
        if name.endswith("Error") and inspect.isclass(value):
            errors[name] = {
                "module": value.__module__,
                "bases": [base.__name__ for base in value.__bases__],
            }
    return errors


def _compatibility_imports() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for module_name, names in COMPATIBILITY_IMPORTS.items():
        module = importlib.import_module(module_name)
        missing = [name for name in names if not hasattr(module, name)]
        if missing:
            raise RuntimeError(f"surface capture: {module_name} is missing {missing}")
        result[module_name] = list(names)
    return result


def capture() -> dict[str, Any]:
    from composio_client._resource import (  # type: ignore[import-not-found] # noqa: PLC0415
        AsyncAPIResource,
        SyncAPIResource,
    )

    import composio_client  # noqa: PLC0415
    import composio_client.types  # noqa: PLC0415
    from composio_client import AsyncComposio, Composio  # noqa: PLC0415

    if composio_client.__version__ != ORACLE_VERSION:
        raise RuntimeError(
            f"surface capture requires composio-client=={ORACLE_VERSION}, found {composio_client.__version__}"
        )
    # The pinned oracle's repr quotes absent values as the string "None".
    transform = cast(Any, importlib.import_module("composio_client._utils._transform"))
    transform.PropertyInfo.__repr__ = _property_info_repr
    return {
        "oracle": {
            "package": "composio-client",
            "version": ORACLE_VERSION,
            "regenerate": (
                "cd python && uv run --isolated --no-project --with composio-client==1.43.0 "
                "python scripts/capture_stainless_surface.py"
            ),
        },
        "root_exports": list(composio_client.__all__),
        "errors": _errors(composio_client),
        "clients": {
            "sync": _client_surface(Composio, SyncAPIResource),
            "async": _client_surface(AsyncComposio, AsyncAPIResource),
        },
        "compatibility_imports": _compatibility_imports(),
        "type_modules": _types_surface(composio_client.types),
    }


def main() -> int:
    fixture = capture()
    FIXTURE_PATH.write_text(f"{json.dumps(fixture, indent=2, sort_keys=True)}\n", encoding="utf-8")
    print(f"captured Stainless {ORACLE_VERSION} surface in {FIXTURE_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
