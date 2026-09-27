"""Tests for the public `normalize()` API."""

import unittest

from pyunormalize import normalize


class TestNormalize(unittest.TestCase):

    def test_dispatches_each_normalization_form(self):
        # This input produces a distinct result in each normalization form
        source = "\ufb03\u00e9"

        expected = {
            "NFC": "\ufb03\u00e9",
            "NFD": "\ufb03e\u0301",
            "NFKC": "ffi\u00e9",
            "NFKD": "ffie\u0301",
        }

        for form, result in expected.items():
            with self.subTest(form=form):
                self.assertEqual(normalize(form, source), result)

    def test_rejects_an_invalid_normalization_form(self):
        with self.assertRaises(ValueError):
            normalize("NORM", "test")


if __name__ == "__main__":
    unittest.main()
