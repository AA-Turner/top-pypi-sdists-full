from __future__ import annotations

import importlib.util
from copy import deepcopy
from pathlib import Path

from ruamel.yaml import YAML

SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "generate-runta-openapi-client.py"
)
spec = importlib.util.spec_from_file_location("generate_runta_openapi_client", SCRIPT)
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)


def test_generator_normalizes_status_codes_without_changing_source(
    tmp_path, monkeypatch
):
    source = tmp_path / "source.yaml"
    content = """openapi: 3.1.0
paths:
  /containers:
    parameters: []
    get:
      responses:
        200:
          description: OK
        '404':
          description: Missing
        default:
          description: Error
"""
    source.write_text(content)
    monkeypatch.setattr(generate, "CONTRACT", source)
    output = tmp_path / "normalized.yaml"

    generate._write_generator_spec(output)

    normalized = YAML(typ="safe").load(output.read_text())
    assert normalized["paths"]["/containers"]["get"]["responses"] == {
        "200": {"description": "OK"},
        "404": {"description": "Missing"},
        "default": {"description": "Error"},
    }
    assert source.read_text() == content


def test_container_resources_reuse_component_only_when_schemas_match():
    resources = {"type": "object", "properties": {"requested": {"type": "integer"}}}
    different = {"type": "object", "properties": {"extra": {"type": "string"}}}
    schemas = {
        "ContainerV2Resources": resources,
        "ContainerV2": {
            "properties": {
                "resources": deepcopy(resources),
                "applied_resources": deepcopy(resources),
            }
        },
        "ContainerV2Spec": {"properties": {"resources": different}},
    }

    generate._reuse_container_resource_schema({"components": {"schemas": schemas}})

    reference = {"$ref": "#/components/schemas/ContainerV2Resources"}
    assert schemas["ContainerV2"]["properties"] == {
        "resources": reference,
        "applied_resources": reference,
    }
    assert schemas["ContainerV2Spec"]["properties"]["resources"] == different
    assert schemas["ContainerV2Resources"] == resources
