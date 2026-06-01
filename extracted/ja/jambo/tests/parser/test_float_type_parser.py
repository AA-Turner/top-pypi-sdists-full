from jambo.exceptions import InvalidSchemaException
from jambo.parser import FloatTypeParser

from unittest import TestCase


class TestFloatTypeParser(TestCase):
    def test_float_parser_no_options(self):
        parser = FloatTypeParser()

        properties = {"type": "number"}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, float)
        self.assertEqual(type_validator, {"default": None})

    def test_float_parser_with_options(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "maximum": 10.5,
            "minimum": 1.0,
            "multipleOf": 0.5,
            "examples": [1.5, 2.5],
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, float)
        self.assertEqual(type_validator["le"], 10.5)
        self.assertEqual(type_validator["ge"], 1.0)
        self.assertEqual(type_validator["multiple_of"], 0.5)
        self.assertEqual(type_validator["examples"], [1.5, 2.5])

    def test_float_parser_with_default(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "default": 5.0,
            "maximum": 10.5,
            "minimum": 1.0,
            "multipleOf": 0.5,
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, float)
        self.assertEqual(type_validator["default"], 5.0)
        self.assertEqual(type_validator["le"], 10.5)
        self.assertEqual(type_validator["ge"], 1.0)
        self.assertEqual(type_validator["multiple_of"], 0.5)

    def test_float_parser_with_default_invalid_type(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "default": "invalid",  # Invalid default value
            "maximum": 10.5,
            "minimum": 1.0,
            "multipleOf": 0.5,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_float_parser_with_default_invalid_maximum(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "default": 15.0,
            "maximum": 10.5,
            "minimum": 1.0,
            "multipleOf": 0.5,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_float_parser_with_default_invalid_minimum(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "default": -5.0,
            "maximum": 10.5,
            "minimum": 1.0,
            "multipleOf": 0.5,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_float_parser_with_default_invalid_exclusive_maximum(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "default": 10.5,
            "exclusiveMaximum": 10.5,
            "minimum": 1.0,
            "multipleOf": 0.5,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_float_parser_with_default_invalid_exclusive_minimum(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "default": 1.0,
            "maximum": 10.5,
            "exclusiveMinimum": 1.0,
            "multipleOf": 0.5,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)

    def test_float_parser_with_default_invalid_multiple(self):
        parser = FloatTypeParser()

        properties = {
            "type": "number",
            "default": 5.0,
            "maximum": 10.5,
            "minimum": 1.0,
            "multipleOf": 2.0,
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)
