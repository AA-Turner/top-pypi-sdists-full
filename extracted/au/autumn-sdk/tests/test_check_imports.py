import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict

CHECK = Path(__file__).resolve().parents[1] / "scripts" / "check_imports.py"

# The smallest package shaped like the generated SDK: a client that loads its sub-SDKs on first use.
HEALTHY: Dict[str, str] = {
    "__init__.py": "from .sdk import Autumn\nVERSION = '0.0.0'\n",
    "sdk.py": """
import importlib


class Autumn:
    _sub_sdk_map = {"features": ("autumn_sdk.features", "Features")}

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def __getattr__(self, name):
        module_path, class_name = self._sub_sdk_map[name]
        return getattr(importlib.import_module(module_path), class_name)()
""",
    "features.py": "from autumn_sdk.models import createfeatureop\n\n\nclass Features:\n    pass\n",
    "models/__init__.py": """
from importlib import import_module

__all__ = ["Feature"]
_dynamic_imports = {"Feature": ".createfeatureop"}


def __getattr__(name):
    if name not in _dynamic_imports:
        raise AttributeError(name)
    return getattr(import_module(_dynamic_imports[name], __package__), name)
""",
    "models/createfeatureop.py": """
from __future__ import annotations
from typing import Union
from pydantic import BaseModel
from typing_extensions import TypeAliasType


class Tiered(BaseModel):
    tiers: int


Dimension = TypeAliasType("Dimension", Union[Tiered, str])


class Feature(BaseModel):
    dimension: Dimension
""",
}

# What Speakeasy generated for 1.2.0: the alias is built at import time, above a class it names.
ALIAS_ABOVE_ITS_CLASS = """
from __future__ import annotations
from typing import Union
from pydantic import BaseModel
from typing_extensions import TypeAliasType

Dimension = TypeAliasType("Dimension", Union[Tiered, str])


class Tiered(BaseModel):
    tiers: int
"""

NEVER_DEFINED = """
from __future__ import annotations
from pydantic import BaseModel


class Feature(BaseModel):
    dimension: Missing
"""


def run_check(files: Dict[str, str]) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as root:
        for name, source in files.items():
            path = Path(root, "autumn_sdk", name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source)
        return subprocess.run(
            [sys.executable, str(CHECK)],
            env={"PYTHONPATH": root},
            capture_output=True,
            text=True,
            check=False,
        )


class CheckImportsTests(unittest.TestCase):
    def test_passes_when_everything_imports(self):
        result = run_check(HEALTHY)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS autumn-sdk 0.0.0", result.stdout)

    def test_fails_on_an_alias_above_a_class_it_names(self):
        result = run_check({**HEALTHY, "models/createfeatureop.py": ALIAS_ABOVE_ITS_CLASS})
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL sub-SDK features: NameError: name 'Tiered' is not defined", result.stderr)
        self.assertIn("FAIL module autumn_sdk.models.createfeatureop: NameError", result.stderr)

    def test_fails_on_a_model_naming_a_type_that_is_never_defined(self):
        result = run_check({**HEALTHY, "models/getfeatureop.py": NEVER_DEFINED})
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL model autumn_sdk.models.getfeatureop.Feature", result.stderr)

    def test_fails_on_an_export_its_module_does_not_define(self):
        exports = HEALTHY["models/__init__.py"].replace('"Feature"', '"Gone"')
        result = run_check({**HEALTHY, "models/__init__.py": exports})
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL export autumn_sdk.models.Gone: AttributeError", result.stderr)

    def test_fails_on_a_module_that_exits_while_importing(self):
        for name in ("models/createfeatureop.py", "models/getfeatureop.py", "models/__init__.py"):
            with self.subTest(module=name):
                result = run_check({**HEALTHY, name: "raise SystemExit(0)\n"})
                self.assertEqual(result.returncode, 1)
                self.assertIn("an import exited with 0", result.stderr)

    def test_fails_when_the_client_lists_no_sub_sdks(self):
        sdk = HEALTHY["sdk.py"].replace("_sub_sdk_map", "_renamed_map")
        result = run_check({**HEALTHY, "sdk.py": sdk})
        self.assertEqual(result.returncode, 1)
        self.assertIn("lists no sub-SDKs", result.stderr)
