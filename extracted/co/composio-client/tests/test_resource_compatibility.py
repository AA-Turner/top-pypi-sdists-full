"""Generated resources preserve the frozen Stainless 1.43 call surface."""

from __future__ import annotations

import asyncio
import importlib.util
import inspect
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from composio_client import AsyncComposio, Composio, ProjectAuth
from composio_client._types import NOT_GIVEN, Omit

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "stainless_surface.json").read_text())


def _load_checker() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "scripts" / "check_stainless_compatibility.py"
    spec = importlib.util.spec_from_file_location("_stainless_compatibility_resources", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_checker = _load_checker()
#: Parameters the frozen 1.43.0 fixture declares that upstream removed; this
#: test skips exactly those, while the checker reports a re-added one loudly.
REMOVED_PARAMETERS = {
    (path, method, parameter) for ((path, method), parameter) in _checker.UPSTREAM_PARAMETER_REMOVALS
}
#: Released resources reached under ``client._internal`` since 2.0.0-rc.22.
RESOURCE_RELOCATIONS: dict[str, str] = _checker.RESOURCE_RELOCATIONS


def resolve(root: object, dotted: str) -> Any:
    value = root
    for part in dotted.split("."):
        value = getattr(value, part)
    return value


@pytest.mark.parametrize(
    ("lane", "client_type"),
    [("sync", Composio), ("async", AsyncComposio)],
)
def test_every_released_method_and_wrapper_accepts_the_stainless_signature(
    lane: str,
    client_type: type[Composio] | type[AsyncComposio],
) -> None:
    client = client_type(auth=ProjectAuth("test"), base_url="https://api.invalid")
    try:
        for resource_path, expected_resource in FIXTURE["clients"][lane]["resources"].items():
            resource = resolve(client, RESOURCE_RELOCATIONS.get(resource_path, resource_path))
            variants = (
                (resource, "methods"),
                (resource.with_raw_response, "raw_methods"),
                (resource.with_streaming_response, "streaming_methods"),
            )
            for target, method_group in variants:
                for method_name, expected_method in expected_resource[method_group].items():
                    method = getattr(target, method_name)
                    signature = inspect.signature(method)
                    positional: list[object] = []
                    keywords: dict[str, object] = {}
                    for expected in expected_method["parameters"]:
                        if (resource_path, method_name, expected["name"]) in REMOVED_PARAMETERS:
                            continue
                        parameter = signature.parameters[expected["name"]]
                        assert parameter.kind.name == expected["kind"]
                        if expected["kind"] == "POSITIONAL_OR_KEYWORD":
                            positional.append("value")
                        else:
                            keywords[expected["name"]] = "value"
                        default = expected["default"]
                        if default["kind"] == "sentinel" and default["value"] == "OMIT":
                            assert isinstance(parameter.default, Omit)
                        elif default["kind"] == "sentinel" and default["value"] == "NOT_GIVEN":
                            assert parameter.default is NOT_GIVEN
                    signature.bind(*positional, **keywords)
                    if method_group == "streaming_methods":
                        assert not inspect.iscoroutinefunction(method)
    finally:
        if lane == "sync":
            cast(Composio, client).close()
        else:
            asyncio.run(cast(AsyncComposio, client).close())
