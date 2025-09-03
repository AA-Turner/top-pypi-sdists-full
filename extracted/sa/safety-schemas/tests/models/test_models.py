from enum import Enum
import inspect
import importlib
import json
from pathlib import Path
import pytest
from deepdiff import DeepDiff
from packaging.specifiers import SpecifierSet

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


    _COMMON_PYDANTIC_EXCLUDE_PATHS = {
        "root['$defs']['ScanConfigModel']['properties']['include_files']['propertyNames']",
        "root['$defs']['ReportSchemaVersion']['const']"
    }

    # TODO: Once we require a higher version of Pydantic, we can remove the following exclusions.

    # NOTE: Pydantic has been updating the way ENUMS are generated in the JSON schema export.
    # The following exclusions are not a breaking change for us,
    # as we are not doing codegen (yet) based on this.
    EXCLUDE_PATHS_PER_PYDANTIC_VERSION = [
        (SpecifierSet(">=2.10.0,<2.10.3"), {
            "root['$defs']['FileType']['type']",
            "root['$defs']['FileType']['title']",                        
        }),

        # the https://github.com/pydantic/pydantic/pull/10989 PR
        # [Do not resolve the JSON Schema reference for dict core schema keys]
        # makes the ENUMS used as dict keys *not* be resolved in the JSON schema export.
        # This exclusion is redundant with the others related to FileType, but I'm keeping it as
        # a reminder of the change.
        (SpecifierSet(">=2.10.3"), {
            "root['$defs']['FileType']",
        })
    ]

    @pytest.mark.parametrize("model, model_name", [(model, name) for name, model in inspect.getmembers(importlib.import_module(MODULE_NAME), inspect.isclass) if hasattr(model, "__annotations__") and not issubclass(model, Enum)])
    def test_model(self, model, model_name):
        LIB_DIR = DATA_DIR

        exclude_paths = set(self.EXCLUDE_PATHS) | self._COMMON_PYDANTIC_EXCLUDE_PATHS

        for specifier, exclusions in self.EXCLUDE_PATHS_PER_PYDANTIC_VERSION:
            if specifier.contains(pydantic_version):
                exclude_paths.update(exclusions)

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
        diff = DeepDiff(current, expected, exclude_paths=exclude_paths, ignore_order=True)
        assert not diff, f"{model_name} [{schema_path}] schema differs from old version: {diff}"
