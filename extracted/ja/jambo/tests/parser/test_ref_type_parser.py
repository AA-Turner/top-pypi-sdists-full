from jambo.exceptions import InternalAssertionException, InvalidSchemaException
from jambo.parser import ObjectTypeParser, RefTypeParser

from pydantic import ValidationError
from typing_extensions import ForwardRef

from unittest import TestCase


class TestRefTypeParser(TestCase):
    def test_ref_type_parser_throws_without_ref(self):
        properties = {
            "title": "person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name", "age"],
        }

        with self.assertRaises(InvalidSchemaException):
            RefTypeParser().from_properties(
                "person",
                properties,
                context=properties,
                ref_cache={},
                required=True,
            )

    def test_ref_type_parser_throws_without_context(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        with self.assertRaises(InternalAssertionException):
            RefTypeParser().from_properties(
                "person",
                properties,
                ref_cache={},
                required=True,
            )

    def test_ref_type_parser_throws_without_ref_cache(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        with self.assertRaises(InternalAssertionException):
            RefTypeParser().from_properties(
                "person",
                properties,
                context=properties,
                required=True,
            )

    def test_ref_type_parser_throws_if_network_ref_type(self):
        properties = {
            "title": "person",
            "$ref": "https://example.com/schemas/person.json",
        }

        with self.assertRaises(InvalidSchemaException):
            RefTypeParser().from_properties(
                "person",
                properties,
                context=properties,
                ref_cache={},
                required=True,
            )

    def test_ref_type_parser_throws_if_non_root_or_def_ref(self):
        # This is invalid because object3 is referencing object2,
        # but object2 is not defined in $defs or as a root reference.
        properties = {
            "title": "object1",
            "type": "object",
            "properties": {
                "object2": {
                    "type": "object",
                    "properties": {
                        "attr1": {
                            "type": "string",
                        },
                        "attr2": {
                            "type": "integer",
                        },
                    },
                },
                "object3": {
                    "$ref": "#/$defs/object2",
                },
            },
        }

        with self.assertRaises(InvalidSchemaException):
            ObjectTypeParser().from_properties(
                "person",
                properties,
                context=properties,
                ref_cache={},
                required=True,
            )

    def test_ref_type_parser_throws_if_def_doesnt_exists(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/employee",
            "$defs": {},
        }

        with self.assertRaises(InvalidSchemaException):
            RefTypeParser().from_properties(
                "person",
                properties,
                context=properties,
                ref_cache={},
                required=True,
            )

    def test_ref_type_parser_throws_if_ref_property_doesnt_exists(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {"person": None},
        }

        with self.assertRaises(InvalidSchemaException):
            RefTypeParser().from_properties(
                "person",
                properties,
                context=properties,
                ref_cache={},
                required=True,
            )

    def test_ref_type_parser_with_def(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        type_parsing, type_validator = RefTypeParser().from_properties(
            "person",
            properties,
            context=properties,
            ref_cache={},
            required=True,
        )

        self.assertIsInstance(type_parsing, type)

        obj = type_parsing(name="John", age=30)

        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)

    def test_ref_type_parser_with_forward_ref(self):
        properties = {
            "title": "person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "emergency_contact": {
                    "$ref": "#",
                },
            },
            "required": ["name", "age"],
        }

        model, type_validator = ObjectTypeParser().from_properties(
            "person",
            properties,
            context=properties,
            ref_cache={},
            required=True,
        )

        obj = model(
            name="John",
            age=30,
            emergency_contact=model(
                name="Jane",
                age=28,
            ),
        )

        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)
        self.assertIsInstance(obj.emergency_contact, model)
        self.assertEqual(obj.emergency_contact.name, "Jane")
        self.assertEqual(obj.emergency_contact.age, 28)

    def test_ref_type_parser_invalid_forward_ref(self):
        properties = {
            # Doesn't have a title, which is required for forward references
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "emergency_contact": {
                    "$ref": "#",
                },
            },
            "required": ["name", "age"],
        }

        with self.assertRaises(InvalidSchemaException):
            ObjectTypeParser().from_properties(
                "person",
                properties,
                context=properties,
                ref_cache={},
                required=True,
            )

    def test_ref_type_parser_forward_ref_can_checks_validation(self):
        properties = {
            "title": "person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "emergency_contact": {
                    "$ref": "#",
                },
            },
            "required": ["name", "age"],
        }

        model, type_validator = ObjectTypeParser().from_properties(
            "person",
            properties,
            context=properties,
            ref_cache={},
            required=True,
        )

        # checks if when created via FowardRef the model is validated correctly.
        with self.assertRaises(ValidationError):
            model(
                name="John",
                age=30,
                emergency_contact=model(
                    name="Jane",
                ),
            )

    def test_ref_type_parser_with_ciclic_def(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                        "emergency_contact": {
                            "$ref": "#/$defs/person",
                        },
                    },
                }
            },
        }

        model, type_validator = RefTypeParser().from_properties(
            "person",
            properties,
            context=properties,
            ref_cache={},
            required=True,
        )

        obj = model(
            name="John",
            age=30,
            emergency_contact=model(
                name="Jane",
                age=28,
            ),
        )

        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)
        self.assertIsInstance(obj.emergency_contact, model)
        self.assertEqual(obj.emergency_contact.name, "Jane")
        self.assertEqual(obj.emergency_contact.age, 28)

    def test_ref_type_parser_with_repeated_ref(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                        "emergency_contact": {
                            "$ref": "#/$defs/person",
                        },
                        "friends": {
                            "type": "array",
                            "items": {
                                "$ref": "#/$defs/person",
                            },
                        },
                    },
                }
            },
        }

        model, type_validator = RefTypeParser().from_properties(
            "person",
            properties,
            context=properties,
            ref_cache={},
            required=True,
        )

        obj = model(
            name="John",
            age=30,
            emergency_contact=model(
                name="Jane",
                age=28,
            ),
            friends=[
                model(name="Alice", age=25),
                model(name="Bob", age=26),
            ],
        )

        self.assertEqual(
            type(obj.emergency_contact),
            type(obj.friends[0]),
            "Emergency contact and friends should be of the same type",
        )

    def test_ref_type_parser_pre_computed_ref_cache(self):
        ref_cache = {}

        parent_properties = {
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        properties1 = {
            "title": "person1",
            "$ref": "#/$defs/person",
        }
        model1, _ = RefTypeParser().from_properties(
            "person",
            properties1,
            context=parent_properties,
            ref_cache=ref_cache,
            required=True,
        )

        properties2 = {
            "title": "person2",
            "$ref": "#/$defs/person",
        }
        model2, _ = RefTypeParser().from_properties(
            "person",
            properties2,
            context=parent_properties,
            ref_cache=ref_cache,
            required=True,
        )

        self.assertIs(model1, model2, "Models should be the same instance")

    def test_parse_from_strategy_invalid_ref_strategy(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        with self.assertRaises(InvalidSchemaException):
            ref_strategy, ref_name, ref_property = RefTypeParser()._parse_from_strategy(
                "invalid_strategy",
                "person",
                properties,
            )

    def test_parse_from_strategy_forward_ref(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        parsed_type = RefTypeParser()._parse_from_strategy(
            "forward_ref",
            "person",
            properties,
        )

        self.assertIsInstance(parsed_type, ForwardRef)

    def test_parse_from_strategy_def_ref(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        parsed_type = RefTypeParser()._parse_from_strategy(
            "def_ref",
            "person",
            properties,
            context=properties,
            ref_cache={},
            required=True,
        )

        obj = parsed_type(
            name="John",
            age=30,
        )

        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)

    def test_ref_type_parser_with_def_with_examples(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
            "examples": [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25},
            ],
        }

        _, type_validator = RefTypeParser().from_properties(
            "person",
            properties,
            context=properties,
            ref_cache={},
            required=True,
        )

        self.assertEqual(
            type_validator.get("examples"),
            [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25},
            ],
        )
