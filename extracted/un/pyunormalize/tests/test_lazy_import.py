"""Tests for lazy imports in the public package namespace."""

import importlib
import sys
import unittest

EXPECTED_UNICODE_VERSION = "18.0.0"
EXPECTED_UCD_VERSION = "18.0.0"

PYUNORMALIZE_MODULES = (
    "pyunormalize",
    "pyunormalize.normalization",
    "pyunormalize._unicode_data",
    "pyunormalize._table_canonical_decomposition",
    "pyunormalize._table_compatibility_decomposition",
    "pyunormalize._table_canonical_composition",
)

RUNTIME_TABLE_MODULES = (
    "pyunormalize.normalization",
    "pyunormalize._unicode_data",
    "pyunormalize._table_canonical_decomposition",
    "pyunormalize._table_compatibility_decomposition",
    "pyunormalize._table_canonical_composition",
)


class TestLazyImport(unittest.TestCase):

    def setUp(self):
        self._saved_modules = {
            name: sys.modules[name]
            for name in PYUNORMALIZE_MODULES
            if name in sys.modules
        }

        for name in PYUNORMALIZE_MODULES:
            sys.modules.pop(name, None)

    def tearDown(self):
        for name in PYUNORMALIZE_MODULES:
            sys.modules.pop(name, None)

        sys.modules.update(self._saved_modules)

    def test_top_level_import_does_not_load_runtime_tables(self):
        module = importlib.import_module("pyunormalize")

        self.assertEqual(module.UNICODE_VERSION, EXPECTED_UNICODE_VERSION)
        self.assertEqual(module.UCD_VERSION, EXPECTED_UCD_VERSION)
        self.assertTrue(hasattr(module, "__version__"))

        for name in RUNTIME_TABLE_MODULES:
            with self.subTest(module=name):
                self.assertNotIn(name, sys.modules)

    def test_public_function_access_loads_normalization_lazily(self):
        module = importlib.import_module("pyunormalize")

        self.assertNotIn("pyunormalize.normalization", sys.modules)

        nfc = module.NFC

        self.assertIn("pyunormalize.normalization", sys.modules)
        self.assertIs(nfc, sys.modules["pyunormalize.normalization"].NFC)


if __name__ == "__main__":
    unittest.main()
