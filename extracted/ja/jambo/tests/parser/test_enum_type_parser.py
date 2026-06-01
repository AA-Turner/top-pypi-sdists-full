from jambo.exceptions import InvalidSchemaException
from jambo.parser import EnumTypeParser

from enum import Enum
from unittest import TestCase


class TestEnumTypeParser(TestCase):
    def test_enum_type_parser_throws_enum_not_defined(self):
        parser = EnumTypeParser()

        schema = {}

        with self.assertRaises(InvalidSchemaException):
            parsed_type, parsed_properties = parser.from_properties_impl(
                "TestEnum",
                schema,
            )

    def test_enum_type_parser_throws_enum_not_list(self):
        parser = EnumTypeParser()

        schema = {
            "enum": "not_a_list",
        }

        with self.assertRaises(InvalidSchemaException):
            parsed_type, parsed_properties = parser.from_properties_impl(
                "TestEnum",
                schema,
            )

    def test_enum_type_parser_creates_enum(self):
        parser = EnumTypeParser()

        schema = {
            "enum": ["value1", "value2", "value3"],
        }

        parsed_type, parsed_properties = parser.from_properties_impl(
            "TestEnum",
            schema,
        )

        self.assertIsInstance(parsed_type, type)
        self.assertTrue(issubclass(parsed_type, Enum))
        self.assertEqual(
            set(parsed_type.__members__.keys()), {"VALUE1", "VALUE2", "VALUE3"}
        )
        self.assertEqual(parsed_properties, {"default": None})

    def test_enum_type_parser_creates_enum_with_description(self):
        parser = EnumTypeParser()

        schema = {
            "description": "an enum",
            "enum": ["value1"],
        }

        parsed_type, parsed_properties = parser.from_properties_impl(
            "TestEnum",
            schema,
        )
        self.assertEqual(parsed_type.__doc__, "an enum")

    def test_enum_type_parser_creates_enum_with_default(self):
        parser = EnumTypeParser()

        schema = {
            "enum": ["value1", "value2", "value3"],
            "default": "value2",
        }

        parsed_type, parsed_properties = parser.from_properties_impl(
            "TestEnum",
            schema,
        )

        self.assertIsInstance(parsed_type, type)
        self.assertTrue(issubclass(parsed_type, Enum))
        self.assertEqual(
            set(parsed_type.__members__.keys()), {"VALUE1", "VALUE2", "VALUE3"}
        )
        self.assertEqual(parsed_properties["default"].value, "value2")

    def test_enum_type_parser_throws_invalid_default(self):
        parser = EnumTypeParser()

        schema = {
            "enum": ["value1", "value2", "value3"],
            "default": "invalid_value",
        }

        with self.assertRaises(ValueError):
            parser.from_properties_impl("TestEnum", schema)

    def test_enum_type_parser_throws_invalid_enum_value(self):
        parser = EnumTypeParser()

        schema = {
            "enum": ["value1", 42, dict()],
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties_impl("TestEnum", schema)

    def test_enum_type_parser_creates_enum_with_examples(self):
        parser = EnumTypeParser()

        schema = {
            "enum": ["value1", "value2", "value3"],
            "examples": ["value1", "value3"],
        }

        parsed_type, parsed_properties = parser.from_properties_impl(
            "TestEnum",
            schema,
        )

        self.assertIsInstance(parsed_type, type)
        self.assertTrue(issubclass(parsed_type, Enum))
        self.assertEqual(
            set(parsed_type.__members__.keys()), {"VALUE1", "VALUE2", "VALUE3"}
        )
        self.assertEqual(parsed_properties["default"], None)
        self.assertEqual(
            parsed_properties["examples"],
            [getattr(parsed_type, "VALUE1"), getattr(parsed_type, "VALUE3")],
        )
