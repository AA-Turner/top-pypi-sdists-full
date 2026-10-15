"""Keep the Python projection complete and tied to its canonical contract."""

import asyncio
import importlib.util
import inspect
import re
import sys
from importlib.resources import files
from pathlib import Path
from typing import Protocol, runtime_checkable

import httpx
import pytest
from jsonschema import Draft202012Validator
from pydantic import BaseModel, JsonValue, TypeAdapter

from recursion_sdk import AsyncRecursion, Recursion

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH_ENVIRONMENT_VARIABLE = "RECURSION_PYTHON_SDK_CONTRACT_PATH"
STREAMING_OPERATIONS = frozenset(
    {"managedAgentsStreamSessionGestalt", "managedAgentsStreamSessionEvents"}
)
HTTP_METHODS = frozenset({"delete", "get", "head", "options", "patch", "post", "put", "trace"})
JSON_OBJECT = TypeAdapter(dict[str, JsonValue])
API_KEY_PAYLOAD_LENGTH = 43
API_KEY = "rma_" + "A" * API_KEY_PAYLOAD_LENGTH


@runtime_checkable
class ModelGenerator(Protocol):
    OUTPUT_ROOT: Path
    MODEL_MODULE_NAME: str

    def contract_path(self) -> Path: ...

    def main(self) -> None: ...

    def operation_projection(
        self, document: dict[str, JsonValue]
    ) -> tuple[dict[str, JsonValue], object]: ...


@pytest.fixture
def generator(monkeypatch: pytest.MonkeyPatch) -> ModelGenerator:
    specification = importlib.util.spec_from_file_location(
        "sdk_generator_compiler_admission", PACKAGE_ROOT / "tools/generate.py"
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    monkeypatch.setitem(sys.modules, specification.name, module)
    specification.loader.exec_module(module)
    assert isinstance(module, ModelGenerator)
    return module


def python_name(name: str) -> str:
    result = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", result).lower()


def test_every_request_response_operation_has_sync_and_async_access(
    generator: ModelGenerator,
) -> None:
    bundled = files("recursion_sdk").joinpath("_generated/openapi.json").read_bytes()
    assert bundled == generator.contract_path().read_bytes()
    document = JSON_OBJECT.validate_json(bundled, strict=True)
    paths = JSON_OBJECT.validate_python(document["paths"], strict=True)
    expected: set[str] = set()
    excluded: set[str] = set()
    for item in paths.values():
        path_item = JSON_OBJECT.validate_python(item, strict=True)
        for method, value in path_item.items():
            if method not in HTTP_METHODS:
                continue
            operation = JSON_OBJECT.validate_python(value, strict=True)
            operation_id = operation["operationId"]
            assert isinstance(operation_id, str)
            if operation_id in STREAMING_OPERATIONS:
                excluded.add(operation_id)
                continue
            sdk_path = operation["x-sdk-path"]
            assert isinstance(sdk_path, list) and len(sdk_path) == 2
            assert sdk_path[0] == "managedAgents" and isinstance(sdk_path[1], str)
            expected.add(python_name(sdk_path[1]))
    assert excluded == STREAMING_OPERATIONS
    assert expected
    client = Recursion(
        api_key=API_KEY, transport=httpx.MockTransport(lambda _: httpx.Response(500))
    )
    async_client = AsyncRecursion(
        api_key=API_KEY, transport=httpx.MockTransport(lambda _: httpx.Response(500))
    )
    try:
        for resource in (client.managed_agents, async_client.managed_agents):
            actual = {
                name
                for name, method in vars(type(resource)).items()
                if not name.startswith("_") and callable(method)
            }
            assert actual == expected
            for name in actual:
                method = getattr(resource, name)
                assert inspect.iscoroutinefunction(method) == (
                    resource is async_client.managed_agents
                )
                assert inspect.signature(method).return_annotation is not inspect.Signature.empty
    finally:
        client.close()
        asyncio.run(async_client.aclose())


def test_default_contract_matches_evaluations_enabled_production(
    generator: ModelGenerator, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(CONTRACT_PATH_ENVIRONMENT_VARIABLE, raising=False)
    expected = PACKAGE_ROOT.parents[1] / (
        "apps/managed-agents/api/src/openapi/recursion-public-openapi.preview.generated.json"
    )
    assert generator.contract_path() == expected
    document = JSON_OBJECT.validate_json(expected.read_bytes(), strict=True)
    paths = JSON_OBJECT.validate_python(document["paths"], strict=True)
    assert "/managed-agents/v1/evaluations" in paths


@pytest.mark.parametrize("override", ["", "relative.json", "missing", "directory"])
def test_invalid_contract_override_rejects_before_generation(
    override: str,
    generator: ModelGenerator,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if override == "missing":
        override = str(tmp_path / "missing.json")
    elif override == "directory":
        override = str(tmp_path)
    monkeypatch.setenv(CONTRACT_PATH_ENVIRONMENT_VARIABLE, override)
    output = tmp_path / "generated"
    monkeypatch.setattr(generator, "OUTPUT_ROOT", output)
    with pytest.raises(ValueError, match=CONTRACT_PATH_ENVIRONMENT_VARIABLE):
        generator.main()
    assert not output.exists()


def test_nullable_closed_empty_object_preserves_wire_contract_through_generation(
    generator: ModelGenerator, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = JSON_OBJECT.validate_json(generator.contract_path().read_bytes(), strict=True)
    components = document["components"]
    assert isinstance(components, dict)
    schemas = components["schemas"]
    assert isinstance(schemas, dict)
    schema_name = "NullableClosedEmptyObject"
    schema: dict[str, JsonValue] = {
        "type": ["object", "null"],
        "additionalProperties": False,
    }
    schemas[schema_name] = schema
    projection, _ = generator.operation_projection(document)
    validators = (
        Draft202012Validator(schema),
        Draft202012Validator({"$ref": f"#/components/schemas/{schema_name}", **projection}),
    )
    # Pydantic owns the generated annotations; the canonical JSON Schema owns
    # full wire constraints. Normalization preserves its closed-object boundary.
    for validator in validators:
        assert validator.is_valid({})
        assert validator.is_valid(None)
        assert not validator.is_valid({"unexpected": True})
    contract_path = tmp_path / "openapi.json"
    contract_path.write_bytes(JSON_OBJECT.dump_json(document))
    monkeypatch.setenv(CONTRACT_PATH_ENVIRONMENT_VARIABLE, str(contract_path))
    monkeypatch.setattr(generator, "OUTPUT_ROOT", tmp_path / "generated")

    previous_model_module = sys.modules.get(generator.MODEL_MODULE_NAME)
    try:
        # The actual generation entrypoint compiles with the package's stock
        # options and rejects unrestricted Any before publishing any models.
        generator.main()
        assert (generator.OUTPUT_ROOT / "openapi.json").read_bytes() == contract_path.read_bytes()
        model: object = getattr(sys.modules[generator.MODEL_MODULE_NAME], schema_name)
        assert isinstance(model, type) and issubclass(model, BaseModel)
        assert model.model_validate_json("{}").model_dump_json() == "{}"
        assert model.model_validate_json("null").model_dump_json() == "null"
    finally:
        if previous_model_module is None:
            sys.modules.pop(generator.MODEL_MODULE_NAME, None)
        else:
            sys.modules[generator.MODEL_MODULE_NAME] = previous_model_module
