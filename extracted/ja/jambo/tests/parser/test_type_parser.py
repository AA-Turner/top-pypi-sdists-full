from jambo.exceptions import InvalidSchemaException
from jambo.parser import StringTypeParser
from jambo.parser._type_parser import GenericTypeParser

from unittest import TestCase


class TestGenericTypeParser(TestCase):
    def test_get_impl(self):
        parser = GenericTypeParser._get_impl({"type": "string"})

        self.assertIsInstance(parser(), StringTypeParser)

    def test_get_impl_invalid_json_schema(self):
        with self.assertRaises(RuntimeError):
            StringTypeParser.json_schema_type = None
            GenericTypeParser._get_impl({"type": "string"})
        StringTypeParser.json_schema_type = "type:string"

    def test_get_impl_invalid_type(self):
        with self.assertRaises(InvalidSchemaException):
            GenericTypeParser._get_impl({"type": "invalid_type"})

    def test_invalid_examples_not_list(self):
        parser = StringTypeParser()

        properties = {
            "type": "integer",
            "examples": "this should be a list",
        }

        with self.assertRaises(InvalidSchemaException):
            parser.from_properties("placeholder", properties)
