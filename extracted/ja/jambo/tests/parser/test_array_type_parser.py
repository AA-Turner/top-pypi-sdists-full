from jambo.exceptions import InvalidSchemaException
from jambo.parser import ArrayTypeParser

from typing_extensions import get_args

from unittest import TestCase


class TestArrayTypeParser(TestCase):
    def test_array_parser_no_options(self):
        parser = ArrayTypeParser()

        properties = {"items": {"type": "string"}}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        element_type = get_args(type_parsing)[0]

        self.assertEqual(type_parsing.__origin__, list)
        self.assertEqual(element_type, str)

    def test_array_parser_with_no_items(self):
        parser = ArrayTypeParser()

        properties = {
            "default": ["a", "b", "c", "d"],
            "maxItems": 3,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_array_parser_with_options_unique(self):
        parser = ArrayTypeParser()

        properties = {"items": {"type": "string"}, "uniqueItems": True}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing.__origin__, set)

    def test_array_parser_with_options_max_min(self):
        parser = ArrayTypeParser()

        properties = {"items": {"type": "string"}, "maxItems": 10, "minItems": 1}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing.__origin__, list)
        self.assertEqual(type_validator["max_length"], 10)
        self.assertEqual(type_validator["min_length"], 1)

    def test_array_parser_with_options_default_list(self):
        parser = ArrayTypeParser()

        properties = {"items": {"type": "string"}, "default": ["a", "b", "c"]}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing.__origin__, list)
        self.assertEqual(type_validator["default_factory"](), ["a", "b", "c"])

    def test_array_parse_with_options_default_set(self):
        parser = ArrayTypeParser()

        properties = {
            "items": {"type": "string"},
            "uniqueItems": True,
            "default": ["a", "b", "c"],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing.__origin__, set)
        self.assertEqual(type_validator["default_factory"](), {"a", "b", "c"})

    def test_array_parser_with_invalid_default_elem_type(self):
        parser = ArrayTypeParser()

        properties = {"items": {"type": "string"}, "default": ["a", 1, "c"]}

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_array_parser_with_invalid_default_type(self):
        parser = ArrayTypeParser()

        properties = {"items": {"type": "string"}, "default": 000}

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties=properties)

    def test_array_parser_with_invalid_default_min(self):
        parser = ArrayTypeParser()

        properties = {"items": {"type": "string"}, "default": ["a"], "minItems": 2}

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_array_parser_with_invalid_default_max(self):
        parser = ArrayTypeParser()

        properties = {
            "items": {"type": "string"},
            "default": ["a", "b", "c", "d"],
            "maxItems": 3,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_array_parser_with_examples(self):
        parser = ArrayTypeParser()

        properties = {
            "items": {"type": "integer"},
            "examples": [
                [1, 2, 3],
                [4, 5, 6],
            ],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing.__origin__, list)
        self.assertEqual(type_validator["examples"], [[1, 2, 3], [4, 5, 6]])
