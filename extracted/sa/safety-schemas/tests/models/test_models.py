from enum import Enum
import inspect
import importlib
import json
from pathlib import Path
import pytest
from deepdiff import DeepDiff

MODULE_NAME = "safety_schemas.models"
DATA_DIR = Path("tests/models/lib")

from pydantic.version import VERSION as pydantic_version

class TestModels:

    EXCLUDE_PATHS = {"root['definitions']['MetadataModel']['properties']['timestamp']['default']", 
                     "root['properties']['MetadataModel']['timestamp']['default']",
                     "root['properties']['timestamp']['default']",
                     "root['$defs']['MetadataModel']['properties']['timestamp']['default']",
                     "root['properties']['installation']",
                     "root['$defs']['ConfigModel']['properties']['installation']",
                     "root['$defs']['Installation']",
                     "root['$defs']['InstallationAction']",
                     "root['$defs']['InstallationConfig']",
                     "root['$defs']['AuditLoggingConfig']",
                     "root['$defs']['AllowedInstallationConfig']",
                     "root['$defs']['DeniedInstallationConfig']",
                     "root['$defs']['DeniedPackagesCriteria']",
                     "root['$defs']['DeniedVulnerabilityCriteria']",
                     "root['$defs']['DeniedPackagesConfig']",
                     "root['$defs']['DeniedVulnerabilityConfig']",
                     "root['$defs']['PackageDefinition']",
                     "root['$defs']['VulnerabilityDefinition']",
                     "root['$defs']['PackageEcosystem']"}

    @pytest.mark.parametrize("model, model_name", [(model, name) for name, model in inspect.getmembers(importlib.import_module(MODULE_NAME), inspect.isclass) if hasattr(model, "__annotations__") and not issubclass(model, Enum)])
    def test_model(self, model, model_name):
        LIB_DIR = DATA_DIR

        if pydantic_version.startswith("1."):
            LIB_DIR = DATA_DIR / "pydantic1"
            current = model.__pydantic_model__.schema()
        else:
            from pydantic import TypeAdapter
            adapter = TypeAdapter(model)
            current = adapter.json_schema()

        schema_path = LIB_DIR / f"{model_name}_schema.json"

        with open(schema_path) as f:
            expected = json.load(f)

        # Compare the two JSON objects
        diff = DeepDiff(current, expected, exclude_paths=self.EXCLUDE_PATHS, ignore_order=True)
        assert not diff, f"{model_name} [{schema_path}] schema differs from old version: {diff}"
