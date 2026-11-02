"""
Pytest configuration and fixtures for SDK contract testing.

This module provides fixtures for validating SDK requests against the OpenAPI spec.
"""

import importlib
import inspect
import json
import pkgutil
import pytest
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# OpenAPI spec loading
# ---------------------------------------------------------------------------

SPEC_PATH = Path(__file__).parent.parent.parent / "openapi.json"


@pytest.fixture(scope="session")
def openapi_spec() -> dict:
    """Load the OpenAPI specification."""
    if not SPEC_PATH.exists():
        pytest.skip(
            f"OpenAPI spec not found at {SPEC_PATH}. "
            "Run ./scripts/generate-openapi-spec.sh first."
        )
    with open(SPEC_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def spec_paths(openapi_spec: dict) -> dict:
    """Extract paths from the OpenAPI spec."""
    return openapi_spec.get("paths", {})


@pytest.fixture(scope="session")
def spec_schemas(openapi_spec: dict) -> dict:
    """Extract component schemas from the OpenAPI spec."""
    return openapi_spec.get("components", {}).get("schemas", {})


@pytest.fixture(scope="session")
def spec_route_index(openapi_spec: dict) -> Dict[str, Dict[str, Any]]:
    """Build an index of {path: {method: operation_spec}} from the OpenAPI spec."""
    paths = openapi_spec.get("paths", {})
    index: Dict[str, Dict[str, Any]] = {}
    for path, path_item in paths.items():
        index[path] = {}
        for method in ("get", "post", "put", "delete", "patch", "head", "options"):
            if method in path_item:
                index[path][method] = path_item[method]
    return index


# ---------------------------------------------------------------------------
# Module discovery
# ---------------------------------------------------------------------------


def discover_api_modules_with_get_kwargs() -> List[Tuple[str, str]]:
    """Discover active API endpoint modules (ones with _get_kwargs)."""
    import octostar.api as api_pkg

    modules = []
    for _importer, modname, ispkg in pkgutil.walk_packages(
        api_pkg.__path__, prefix="octostar.api."
    ):
        if ispkg or modname.endswith("__init__"):
            continue
        try:
            module = importlib.import_module(modname)
            if hasattr(module, "_get_kwargs"):
                endpoint_name = modname.split(".")[-1]
                modules.append((modname, endpoint_name))
        except Exception:
            pass
    return modules


def discover_all_api_modules() -> List[Tuple[str, str, str]]:
    """Discover ALL API modules, classified as active/deprecated/migration_pending.

    Returns list of (module_name, endpoint_name, classification) tuples.
    """
    import octostar.api as api_pkg

    modules: List[Tuple[str, str, str]] = []
    for _importer, modname, ispkg in pkgutil.walk_packages(
        api_pkg.__path__, prefix="octostar.api."
    ):
        if ispkg or modname.endswith("__init__"):
            continue
        try:
            module = importlib.import_module(modname)
            endpoint_name = modname.split(".")[-1]

            if hasattr(module, "_get_kwargs"):
                modules.append((modname, endpoint_name, "active"))
            elif hasattr(module, "sync"):
                source = inspect.getsource(module.sync)
                if "DeprecatedEndpointError" in source:
                    modules.append((modname, endpoint_name, "deprecated"))
                elif "V1MigrationPendingError" in source:
                    modules.append((modname, endpoint_name, "migration_pending"))
                else:
                    modules.append((modname, endpoint_name, "unknown"))
        except Exception:
            pass
    return modules


# Module-level constants (discovered at import time)
API_MODULES = discover_api_modules_with_get_kwargs()
ALL_API_MODULES = discover_all_api_modules()


# ---------------------------------------------------------------------------
# RequestValidator
# ---------------------------------------------------------------------------


class RequestValidator:
    """Validates SDK request kwargs against OpenAPI specification."""

    def __init__(self, openapi_spec: dict):
        self.spec = openapi_spec
        self.paths = openapi_spec.get("paths", {})
        self.schemas = openapi_spec.get("components", {}).get("schemas", {})

    def validate_request(
        self,
        kwargs: Dict[str, Any],
        expected_path: Optional[str] = None,
    ) -> "ValidationResult":
        """Validate a request kwargs dict from _get_kwargs() against the spec."""
        errors = []

        method = kwargs.get("method", "").lower()
        url = kwargs.get("url", "")
        json_body = kwargs.get("json")
        params = kwargs.get("params", {})

        parsed = urlparse(url)
        path = parsed.path

        spec_path, _path_params = self._match_path(path)

        if not spec_path:
            errors.append(f"Path not found in OpenAPI spec: {path}")
            return ValidationResult(errors)

        if expected_path and spec_path != expected_path:
            errors.append(f"Path mismatch: expected {expected_path}, got {spec_path}")

        path_spec = self.paths.get(spec_path, {})
        operation_spec = path_spec.get(method)

        if not operation_spec:
            allowed = [
                m.upper()
                for m in path_spec
                if m in ("get", "post", "put", "delete", "patch")
            ]
            errors.append(
                f"Method {method.upper()} not allowed for {spec_path} "
                f"(allowed: {', '.join(allowed)})"
            )
            return ValidationResult(errors)

        if json_body is not None:
            body_errors = self._validate_request_body(json_body, operation_spec)
            errors.extend(body_errors)

        if params:
            param_errors = self._validate_query_params(params, operation_spec)
            errors.extend(param_errors)

        return ValidationResult(errors)

    def validate_method(self, kwargs: Dict[str, Any]) -> "ValidationResult":
        """Validate that the SDK's HTTP method matches the spec."""
        errors = []
        method = kwargs.get("method", "").lower()
        url = kwargs.get("url", "")

        parsed = urlparse(url)
        path = parsed.path

        spec_path, _path_params = self._match_path(path)
        if not spec_path:
            errors.append(f"Path not found in spec: {path}")
            return ValidationResult(errors)

        path_spec = self.paths.get(spec_path, {})
        if method not in path_spec:
            allowed = [
                m.upper()
                for m in path_spec
                if m in ("get", "post", "put", "delete", "patch")
            ]
            errors.append(
                f"Method mismatch: SDK uses {method.upper()} but spec allows "
                f"[{', '.join(allowed)}] for {spec_path}"
            )
        return ValidationResult(errors)

    def _match_path(self, actual_path: str) -> tuple:
        """Match actual path to OpenAPI path pattern."""
        actual_path = actual_path.rstrip("/")

        if actual_path in self.paths:
            return actual_path, {}
        if actual_path + "/" in self.paths:
            return actual_path + "/", {}

        actual_parts = actual_path.split("/")

        # First pass: exact segment count matches
        for spec_path in self.paths:
            normalized_spec = spec_path.rstrip("/")
            spec_parts = normalized_spec.split("/")

            if len(spec_parts) != len(actual_parts):
                continue

            match = True
            path_params = {}
            for spec_part, actual_part in zip(spec_parts, actual_parts):
                if spec_part.startswith("{") and spec_part.endswith("}"):
                    param_name = spec_part[1:-1]
                    path_params[param_name] = actual_part
                elif spec_part != actual_part:
                    match = False
                    break

            if match:
                return spec_path, path_params

        # Second pass: catch-all matches
        catchall_candidates = []
        for spec_path in self.paths:
            normalized_spec = spec_path.rstrip("/")
            spec_parts = normalized_spec.split("/")

            if len(actual_parts) <= len(spec_parts):
                continue
            if not (spec_parts[-1].startswith("{") and spec_parts[-1].endswith("}")):
                continue

            match = True
            path_params = {}
            for i in range(len(spec_parts) - 1):
                spec_part = spec_parts[i]
                actual_part = actual_parts[i]
                if spec_part.startswith("{") and spec_part.endswith("}"):
                    param_name = spec_part[1:-1]
                    path_params[param_name] = actual_part
                elif spec_part != actual_part:
                    match = False
                    break

            if match:
                param_name = spec_parts[-1][1:-1]
                path_params[param_name] = "/".join(actual_parts[len(spec_parts) - 1 :])
                catchall_candidates.append((spec_path, path_params, len(spec_parts)))

        if catchall_candidates:
            catchall_candidates.sort(key=lambda x: x[2])
            return catchall_candidates[0][0], catchall_candidates[0][1]

        return None, {}

    def _validate_request_body(self, body: Any, operation_spec: dict) -> list:
        """Validate request body against operation's requestBody schema."""
        errors = []
        request_body_spec = operation_spec.get("requestBody")
        if not request_body_spec:
            errors.append("Request body provided but not expected by spec")
            return errors

        content_spec = request_body_spec.get("content", {})
        json_spec = content_spec.get("application/json", {})
        schema = json_spec.get("schema", {})
        if not schema:
            return errors

        schema = self._resolve_ref(schema)
        body_errors = self._validate_against_schema(body, schema, "body")
        errors.extend(body_errors)
        return errors

    def _validate_query_params(self, params: dict, operation_spec: dict) -> list:
        """Validate query parameters against operation spec."""
        errors = []
        spec_params = operation_spec.get("parameters", [])
        query_params = {p["name"]: p for p in spec_params if p.get("in") == "query"}

        for param_name in params:
            if param_name not in query_params:
                errors.append(f"Unknown query parameter: {param_name}")

        for param_name, param_spec in query_params.items():
            if param_spec.get("required") and param_name not in params:
                errors.append(f"Missing required query parameter: {param_name}")

        return errors

    def _resolve_ref(self, schema: dict) -> dict:
        """Resolve $ref in schema."""
        if "$ref" not in schema:
            return schema
        ref = schema["$ref"]
        if ref.startswith("#/components/schemas/"):
            schema_name = ref.split("/")[-1]
            return self.schemas.get(schema_name, {})
        return schema

    def _validate_against_schema(self, value: Any, schema: dict, path: str) -> list:
        """Basic validation of value against JSON schema."""
        errors = []
        schema = self._resolve_ref(schema)
        schema_type = schema.get("type")

        if "anyOf" in schema or "oneOf" in schema:
            return errors

        if schema_type == "array":
            if not isinstance(value, list):
                errors.append(f"{path}: expected array, got {type(value).__name__}")
            else:
                items_schema = schema.get("items", {})
                for i, item in enumerate(value[:3]):
                    item_errors = self._validate_against_schema(
                        item, items_schema, f"{path}[{i}]"
                    )
                    errors.extend(item_errors)
            return errors

        if schema_type == "object" or "properties" in schema:
            if not isinstance(value, dict):
                errors.append(f"{path}: expected object, got {type(value).__name__}")
                return errors

            properties = schema.get("properties", {})
            required = schema.get("required", [])

            for prop_name in required:
                if prop_name not in value:
                    errors.append(f"{path}: missing required property '{prop_name}'")

            for prop_name, prop_value in value.items():
                if prop_name in properties:
                    prop_schema = properties[prop_name]
                    prop_errors = self._validate_against_schema(
                        prop_value, prop_schema, f"{path}.{prop_name}"
                    )
                    errors.extend(prop_errors)
            return errors

        if schema_type == "string" and not isinstance(value, str):
            if value is not None:
                errors.append(f"{path}: expected string, got {type(value).__name__}")
        elif schema_type == "integer" and not isinstance(value, int):
            if value is not None:
                errors.append(f"{path}: expected integer, got {type(value).__name__}")
        elif schema_type == "number" and not isinstance(value, (int, float)):
            if value is not None:
                errors.append(f"{path}: expected number, got {type(value).__name__}")
        elif schema_type == "boolean" and not isinstance(value, bool):
            if value is not None:
                errors.append(f"{path}: expected boolean, got {type(value).__name__}")

        return errors


class ValidationResult:
    """Result of validating a request against OpenAPI spec."""

    def __init__(self, errors: list):
        self.errors = errors

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        if self.is_valid:
            return "ValidationResult(valid=True)"
        return f"ValidationResult(errors={self.errors})"

    def raise_if_invalid(self):
        """Raise AssertionError if validation failed."""
        if not self.is_valid:
            raise AssertionError(
                "Request does not conform to OpenAPI spec:\n"
                + "\n".join(f"  - {e}" for e in self.errors)
            )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def request_validator(openapi_spec: dict) -> RequestValidator:
    """Create a RequestValidator instance."""
    return RequestValidator(openapi_spec)


@pytest.fixture
def mock_client():
    """Create a mock client for testing _get_kwargs()."""
    from octostar.client import Client

    return Client(
        base_url="https://home.example.com",
        headers={"Authorization": "Bearer test-token"},
        timeout=30.0,
    )


# ---------------------------------------------------------------------------
# Terminal summary
# ---------------------------------------------------------------------------


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print summary of xfailed tests (SDK/API contract mismatches) at end of session."""
    xfailed = terminalreporter.stats.get("xfailed", [])

    if not xfailed:
        return

    terminalreporter.write_sep("=", "SDK/API Contract Mismatches (xfail)")
    terminalreporter.write_line("")
    terminalreporter.write_line(
        "The following endpoints have known mismatches between SDK and API spec:"
    )
    terminalreporter.write_line("")

    for report in xfailed:
        test_name = report.nodeid.split("::")[-1]
        reason = getattr(report, "wasxfail", None) or "No reason provided"

        terminalreporter.write_line(f"  - {test_name}")
        terminalreporter.write_line(f"    Reason: {reason}")
        terminalreporter.write_line("")

    terminalreporter.write_line(
        "These mismatches should be resolved by updating the SDK "
        "or adding the missing backend routes."
    )
    terminalreporter.write_line("")
