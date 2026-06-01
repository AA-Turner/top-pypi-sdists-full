from jambo.exceptions import InternalAssertionException
from jambo.parser import ObjectTypeParser

from unittest import TestCase


class TestObjectTypeParser(TestCase):
    def test_object_type_parser_throws_without_ref_cache(self):
        parser = ObjectTypeParser()

        properties = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
        }

        with self.assertRaises(InternalAssertionException):
            parser.from_properties_impl("placeholder", properties)

    def test_object_type_parser(self):
        parser = ObjectTypeParser()

        properties = {
            "type": "object",
            "description": "obj desc",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
        }

        Model, _args = parser.from_properties_impl(
            "placeholder", properties, ref_cache={}
        )
        self.assertEqual(Model.__doc__, "obj desc")

        obj = Model(name="name", age=10)

        self.assertEqual(obj.name, "name")
        self.assertEqual(obj.age, 10)

    def test_object_type_parser_with_object_example(self):
        parser = ObjectTypeParser()

        properties = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "examples": [
                {
                    "name": "example_name",
                    "age": 30,
                }
            ],
        }

        _, type_validator = parser.from_properties_impl(
            "placeholder", properties, ref_cache={}
        )

        test_example = type_validator["examples"][0]

        self.assertEqual(test_example.name, "example_name")
        self.assertEqual(test_example.age, 30)

    def test_object_type_parser_with_default(self):
        parser = ObjectTypeParser()

        properties = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "default": {
                "name": "default_name",
                "age": 20,
            },
        }

        _, type_validator = parser.from_properties_impl(
            "placeholder", properties, ref_cache={}
        )

        # Check default value
        default_obj = type_validator["default_factory"]()
        self.assertEqual(default_obj.name, "default_name")
        self.assertEqual(default_obj.age, 20)

        # Chekc default factory new object id
        new_obj = type_validator["default_factory"]()
        self.assertNotEqual(id(default_obj), id(new_obj))

    def test_object_type_parser_warns_if_object_override_in_cache(self):
        ref_cache = {}

        parser = ObjectTypeParser()

        properties = {"type": "object", "properties": {}}

        with self.assertWarns(UserWarning):
            _, type_validator = parser.from_properties_impl(
                "placeholder", properties, ref_cache=ref_cache
            )
            _, type_validator = parser.from_properties_impl(
                "placeholder", properties, ref_cache=ref_cache
            )
