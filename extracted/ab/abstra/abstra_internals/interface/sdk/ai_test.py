from unittest import TestCase

from abstra_internals.interface.sdk.ai import normalize_format


class TestNormalizeFormat(TestCase):
    def test_normal(self):
        self.assertEqual(
            normalize_format({"a": {"type": "string"}}), {"a": {"type": "string"}}
        )

    def test_string(self):
        self.assertEqual(normalize_format({"a": "string"}), {"a": {"type": "string"}})

    def test_str(self):
        self.assertEqual(normalize_format({"a": str}), {"a": {"type": "string"}})

    def test_int(self):
        self.assertEqual(normalize_format({"a": int}), {"a": {"type": "integer"}})

    def test_float(self):
        self.assertEqual(normalize_format({"a": float}), {"a": {"type": "number"}})

    def test_bool(self):
        self.assertEqual(normalize_format({"a": bool}), {"a": {"type": "boolean"}})

    def test_enum(self):
        self.assertEqual(
            normalize_format({"a": ["b", "c"]}), {"a": {"enum": ["b", "c"]}}
        )

    def test_descriptive_string_type_is_coerced(self):
        # Authors write natural-language types; Kimi rejects them as-is.
        self.assertEqual(
            normalize_format({"a": "string (aprovar ou revisar)"}),
            {"a": {"type": "string", "description": "aprovar ou revisar"}},
        )

    def test_descriptive_number_type_is_coerced(self):
        self.assertEqual(
            normalize_format({"a": "number (0-100)"}),
            {"a": {"type": "number", "description": "0-100"}},
        )

    def test_array_of_strings_is_coerced(self):
        self.assertEqual(
            normalize_format({"a": "array of strings"}),
            {"a": {"type": "array", "items": {"type": "string"}}},
        )

    def test_list_alias_becomes_array(self):
        self.assertEqual(
            normalize_format({"a": "list"}),
            {"a": {"type": "array", "items": {"type": "string"}}},
        )

    def test_unknown_type_defaults_to_string_keeping_text(self):
        self.assertEqual(
            normalize_format({"a": "cpf number"}),
            {"a": {"type": "string", "description": "cpf number"}},
        )

    def test_prebuilt_dict_with_invalid_type_is_coerced(self):
        self.assertEqual(
            normalize_format({"a": {"type": "string (aprovar ou revisar)"}}),
            {"a": {"type": "string", "description": "aprovar ou revisar"}},
        )

    def test_prebuilt_dict_author_description_wins(self):
        self.assertEqual(
            normalize_format({"a": {"type": "number (0-100)", "description": "score"}}),
            {"a": {"type": "number", "description": "score"}},
        )
