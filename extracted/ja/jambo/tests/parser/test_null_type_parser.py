from jambo.parser import NullTypeParser

from unittest import TestCase


class TestNullTypeParser(TestCase):
    def test_null_parser_no_options(self):
        parser = NullTypeParser()

        properties = {"type": "null"}

        type_parsing, type_validator = parser.from_properties_impl(
            "placeholder", properties
        )

        self.assertEqual(type_parsing, type(None))
        self.assertEqual(type_validator, {"default": None})

    def test_null_parser_with_examples(self):
        parser = NullTypeParser()

        properties = {
            "type": "null",
            "examples": [None],
        }

        type_parsing, type_validator = parser.from_properties_impl(
            "placeholder", properties
        )

        self.assertEqual(type_parsing, type(None))
        self.assertEqual(type_validator["default"], None)
        self.assertEqual(type_validator["examples"], [None])

    def test_null_parser_with_invalid_default(self):
        parser = NullTypeParser()

        properties = {"type": "null", "default": "invalid"}

        type_parsing, type_validator = parser.from_properties_impl(
            "placeholder", properties
        )

        self.assertEqual(type_parsing, type(None))
        self.assertEqual(type_validator, {"default": None})
