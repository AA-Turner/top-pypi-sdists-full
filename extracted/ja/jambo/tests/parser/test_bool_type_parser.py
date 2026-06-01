from jambo.exceptions import InvalidSchemaException
from jambo.parser import BooleanTypeParser

from unittest import TestCase


class TestBoolTypeParser(TestCase):
    def test_bool_parser_no_options(self):
        parser = BooleanTypeParser()

        properties = {"type": "boolean"}

        type_parsing, type_validator = parser.from_properties_impl(
            "placeholder", properties
        )

        self.assertEqual(type_parsing, bool)
        self.assertEqual(type_validator, {"default": None})

    def test_bool_parser_with_default(self):
        parser = BooleanTypeParser()

        properties = {
            "type": "boolean",
            "default": True,
        }

        type_parsing, type_validator = parser.from_properties_impl(
            "placeholder", properties
        )

        self.assertEqual(type_parsing, bool)
        self.assertEqual(type_validator["default"], True)

    def test_bool_parser_with_invalid_default(self):
        parser = BooleanTypeParser()

        properties = {
            "type": "boolean",
            "default": "invalid",
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties_impl("placeholder", properties)

    def test_bool_parser_with_examples(self):
        parser = BooleanTypeParser()

        properties = {
            "type": "boolean",
            "examples": [True, False],
        }

        type_parsing, type_validator = parser.from_properties_impl(
            "placeholder", properties
        )

        self.assertEqual(type_parsing, bool)
        self.assertEqual(type_validator["default"], None)
        self.assertEqual(type_validator["examples"], [True, False])
