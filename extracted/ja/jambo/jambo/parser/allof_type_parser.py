from jambo.exceptions import InvalidSchemaException
from jambo.parser._type_parser import GenericTypeParser
from jambo.types.json_schema_type import JSONSchema
from jambo.types.type_parser_options import TypeParserOptions

from typing_extensions import Unpack


class AllOfTypeParser(GenericTypeParser):
    mapped_type = any

    json_schema_type = "allOf"

    def from_properties_impl(
        self, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ):
        sub_properties = properties.get("allOf", [])

        root_type = properties.get("type")
        if root_type is not None:
            for sub_property in sub_properties:
                sub_property["type"] = root_type

        parser = self._get_type_parser(sub_properties)

        combined_properties = self._rebuild_properties_from_subproperties(
            sub_properties
        )

        if (examples := properties.get("examples")) is not None:
            combined_properties["examples"] = examples

        return parser().from_properties_impl(name, combined_properties, **kwargs)

    @staticmethod
    def _get_type_parser(
        sub_properties: list[JSONSchema],
    ) -> type[GenericTypeParser]:
        if not sub_properties:
            raise InvalidSchemaException(
                "'allOf' must contain at least one schema", invalid_field="allOf"
            )

        parsers: set[type[GenericTypeParser]] = set(
            GenericTypeParser._get_impl(sub_property) for sub_property in sub_properties
        )
        if len(parsers) != 1:
            raise InvalidSchemaException(
                "All sub-schemas in 'allOf' must resolve to the same type",
                invalid_field="allOf",
            )

        return parsers.pop()

    @staticmethod
    def _rebuild_properties_from_subproperties(
        sub_properties: list[JSONSchema],
    ) -> JSONSchema:
        properties: JSONSchema = {}
        for subProperty in sub_properties:
            for name, prop in subProperty.items():
                if name not in properties:
                    properties[name] = prop  # type: ignore
                else:
                    # Merge properties if they exist in both sub-properties
                    properties[name] = AllOfTypeParser._validate_prop(  # type: ignore
                        name,
                        properties[name],  # type: ignore
                        prop,
                    )
        return properties

    @staticmethod
    def _validate_prop(prop_name, old_value, new_value):
        if prop_name == "description":
            return f"{old_value} | {new_value}"

        if prop_name == "default":
            if old_value != new_value:
                raise InvalidSchemaException(
                    f"Conflicting defaults for '{prop_name}'", invalid_field=prop_name
                )
            return old_value

        if prop_name == "required":
            return old_value + new_value

        if prop_name in ("maxLength", "maximum", "exclusiveMaximum"):
            return old_value if old_value > new_value else new_value

        if prop_name in ("minLength", "minimum", "exclusiveMinimum"):
            return old_value if old_value < new_value else new_value

        if prop_name == "properties":
            for key, value in new_value.items():
                if key not in old_value:
                    old_value[key] = value
                    continue

                for sub_key, sub_value in value.items():
                    if sub_key not in old_value[key]:
                        old_value[key][sub_key] = sub_value
                    else:
                        # Merge properties if they exist in both sub-properties
                        old_value[key][sub_key] = AllOfTypeParser._validate_prop(
                            sub_key, old_value[key][sub_key], sub_value
                        )

        # Handle other properties by just returning the first valued
        return old_value
