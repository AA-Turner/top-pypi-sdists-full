from jambo.exceptions import InvalidSchemaException
from jambo.parser._type_parser import GenericTypeParser
from jambo.types.json_schema_type import JSONSchemaNativeTypes
from jambo.types.type_parser_options import JSONSchema, TypeParserOptions

from typing_extensions import Unpack

from enum import Enum


class EnumTypeParser(GenericTypeParser):
    json_schema_type = "enum"

    def from_properties_impl(
        self, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ):
        if "enum" not in properties:
            raise InvalidSchemaException(
                f"Enum type {name} must have 'enum' property defined.",
                invalid_field="enum",
            )

        enum_values = properties["enum"]

        if not isinstance(enum_values, list):
            raise InvalidSchemaException(
                f"Enum type {name} must have 'enum' as a list of values.",
                invalid_field="enum",
            )

        if any(not isinstance(value, JSONSchemaNativeTypes) for value in enum_values):
            raise InvalidSchemaException(
                f"Enum type {name} must have 'enum' values of allowed types: {JSONSchemaNativeTypes}.",
                invalid_field="enum",
            )

        # Create a new Enum type dynamically
        enum_type = Enum(name, {str(value).upper(): value for value in enum_values})  # type: ignore
        enum_type.__doc__ = properties.get("description")

        parsed_properties = self.mappings_properties_builder(properties, **kwargs)

        if "default" in parsed_properties and parsed_properties["default"] is not None:
            parsed_properties["default"] = enum_type(parsed_properties["default"])

        if "examples" in parsed_properties:
            parsed_properties["examples"] = [
                enum_type(example) for example in parsed_properties["examples"]
            ]

        return enum_type, parsed_properties
