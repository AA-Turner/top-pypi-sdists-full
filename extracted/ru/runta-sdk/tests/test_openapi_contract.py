from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "runta-api.openapi.yaml"
GENERATED = ROOT / "src" / "runta" / "_internal" / "openapi"


def _load_spec() -> dict[str, Any]:
    yaml = YAML(typ="safe")
    with CONTRACT.open(encoding="utf-8") as handle:
        return yaml.load(handle)


def _operations(spec: dict[str, Any]) -> dict[str, tuple[str, str, list[str]]]:
    operations = {}
    for path, item in spec["paths"].items():
        for method, operation in item.items():
            if method.lower() in {"delete", "get", "head", "patch", "post", "put"}:
                operations[operation["operationId"]] = (
                    method.upper(),
                    path,
                    list(operation.get("tags", [])),
                )
    return operations


def _snake(value: str) -> str:
    value = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value)
    return value.strip("_").lower()


class OpenApiContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = _load_spec()

    def test_sdk_operations_exist(self) -> None:
        expected = {
            "healthz": ("GET", "/healthz"),
            "headHealthz": ("HEAD", "/healthz"),
            "listRuntimes": ("GET", "/v2/runtimes"),
            "createRuntime": ("POST", "/v2/runtimes"),
            "getRuntime": ("GET", "/v2/runtimes/{runtime_id}"),
            "deleteRuntime": ("DELETE", "/v2/runtimes/{runtime_id}"),
            "patchRuntime": ("PATCH", "/v2/runtimes/{runtime_id}"),
            "startRuntime": ("POST", "/v2/runtimes/{runtime_id}/start"),
            "pauseRuntime": ("POST", "/v2/runtimes/{runtime_id}/pause"),
            "resumeRuntime": ("POST", "/v2/runtimes/{runtime_id}/resume"),
            "stopRuntime": ("POST", "/v2/runtimes/{runtime_id}/stop"),
            "readRuntimeFile": ("GET", "/v2/runtimes/{runtime_id}/files"),
            "writeRuntimeFile": ("PUT", "/v2/runtimes/{runtime_id}/files"),
            "setSecret": ("PUT", "/v2/secrets/{secret_id}"),
            "getSecret": ("GET", "/v2/secrets/{secret_id}"),
            "listSecrets": ("GET", "/v2/secrets"),
            "deleteSecret": ("DELETE", "/v2/secrets/{secret_id}"),
            "createCheckpoint": ("POST", "/v2/runtimes/{runtime_id}/checkpoints"),
            "listCheckpoints": ("GET", "/v2/checkpoints"),
            "getCheckpoint": ("GET", "/v2/checkpoints/{checkpoint_id}"),
            "deleteCheckpoint": ("DELETE", "/v2/checkpoints/{checkpoint_id}"),
        }
        operations = _operations(self.spec)
        for operation_id, expected_route in expected.items():
            method, path, _tags = operations[operation_id]
            self.assertEqual((method, path), expected_route, operation_id)

    def test_generated_endpoint_modules_cover_every_operation(self) -> None:
        operations = _operations(self.spec)
        self.assertIn("createRuntime", operations)
        for operation_id, (_method, _path, tags) in operations.items():
            self.assertTrue(tags, operation_id)
            module = GENERATED / "api" / _snake(tags[0]) / f"{_snake(operation_id)}.py"
            self.assertTrue(
                module.exists(),
                f"missing generated endpoint for {operation_id}: {module}",
            )

    def test_codegen_check_passes_and_contract_is_not_modified(self) -> None:
        try:
            import openapi_python_client  # noqa: F401
        except ImportError:
            self.skipTest("openapi-python-client is not available on this Python")

        before = CONTRACT.read_bytes()
        subprocess.run(
            [sys.executable, "scripts/generate-runta-openapi-client.py", "--check"],
            cwd=ROOT,
            check=True,
        )
        self.assertEqual(CONTRACT.read_bytes(), before)

    def test_runtime_resource_schemas_are_nested(self) -> None:
        schemas = self.spec["components"]["schemas"]
        create_runtime = schemas["FreshRuntimeCreateRequest"]["properties"]
        patch_runtime = schemas["PatchRuntimeRequest"]["properties"]
        runtime = schemas["Runtime"]["properties"]

        self.assertIn("resources", create_runtime)
        self.assertIn("resources", patch_runtime)
        self.assertIn("resources", runtime)
        self.assertIn("idle_policy", create_runtime)
        self.assertIn("idle_policy", patch_runtime)
        self.assertIn("idle_policy", runtime)
        self.assertEqual(
            schemas["IdlePolicy"]["oneOf"],
            [
                {"$ref": "#/components/schemas/DisabledIdlePolicy"},
                {"$ref": "#/components/schemas/SuspendOnlyIdlePolicy"},
                {"$ref": "#/components/schemas/SuspendAndWakeupIdlePolicy"},
            ],
        )
        legacy_fields = [f"{prefix}_memory_mib" for prefix in ("cur", "min", "max")]
        self.assertNotIn(legacy_fields[0], create_runtime)
        self.assertNotIn(legacy_fields[1], patch_runtime)
        self.assertNotIn(legacy_fields[2], runtime)
        self.assertIn("requests", schemas["RuntimeResources"]["properties"])
        self.assertIn("limits", schemas["RuntimeResources"]["properties"])
        self.assertIn(
            "disk_gib", schemas["CreateRuntimeResourceRequests"]["properties"]
        )
        self.assertIn("disk_gib", schemas["RuntimeResourceRequests"]["required"])

    def test_checkpoint_full_kind_remains_available(self) -> None:
        kind = self.spec["components"]["schemas"]["CreateCheckpointRequest"][
            "properties"
        ]["kind"]
        self.assertIn("full", kind["enum"])

    def test_runtime_create_uses_checkpoint_id(self) -> None:
        schemas = self.spec["components"]["schemas"]
        create_runtime = schemas["CreateRuntimeRequest"]
        self.assertEqual(
            create_runtime["oneOf"],
            [
                {"$ref": "#/components/schemas/FreshRuntimeCreateRequest"},
                {"$ref": "#/components/schemas/CheckpointRuntimeRestoreRequest"},
            ],
        )
        self.assertIn(
            "checkpoint_id", schemas["CheckpointRuntimeRestoreRequest"]["properties"]
        )
        self.assertNotIn(
            "runtime_agent", schemas["FreshRuntimeCreateRequest"]["properties"]
        )

    def test_public_metadata_schemas_do_not_expose_internal_fields(self) -> None:
        schemas = self.spec["components"]["schemas"]
        runtime = schemas["Runtime"]
        checkpoint = schemas["Checkpoint"]
        egress_policy = schemas["PublicEgressPolicy"]

        for schema in (runtime, checkpoint):
            properties = schema["properties"]
            self.assertNotIn("arch", properties)
            self.assertNotIn("base_image_hash", properties)
            self.assertNotIn("agent_image_hash", properties)
            self.assertNotIn("kernel_image_hash", properties)
        self.assertEqual(egress_policy["discriminator"]["propertyName"], "mode")
        self.assertEqual(len(egress_policy["oneOf"]), 2)
        self.assertIn("allowed_hosts", schemas["AllowlistEgressPolicy"]["properties"])
        self.assertIn("denied_hosts", schemas["DenylistEgressPolicy"]["properties"])

    def test_secrets_use_set_request_schema(self) -> None:
        schemas = self.spec["components"]["schemas"]
        secrets = self.spec["paths"]["/v2/secrets/{secret_id}"]

        self.assertEqual(secrets["put"]["operationId"], "setSecret")
        request_schema = secrets["put"]["requestBody"]["content"]["application/json"][
            "schema"
        ]
        self.assertEqual(
            request_schema["$ref"], "#/components/schemas/SetSecretRequest"
        )
        self.assertIn("SetSecretRequest", schemas)
        self.assertIn("CreateSecretRequest", schemas)

    def test_secret_stubs_are_removed(self) -> None:
        paths = self.spec["paths"]
        schemas = self.spec["components"]["schemas"]
        self.assertFalse(any("secret-stub" in path for path in paths))
        self.assertNotIn("DefaultSecretStub", schemas)
        self.assertNotIn("SecretStub", schemas)

    def test_files_are_exposed_as_octet_stream(self) -> None:
        files = self.spec["paths"]["/v2/runtimes/{runtime_id}/files"]
        self.assertIn(
            "application/octet-stream", files["get"]["responses"]["200"]["content"]
        )
        self.assertIn(
            "application/octet-stream", files["put"]["requestBody"]["content"]
        )


if __name__ == "__main__":
    unittest.main()
