from jambo.exceptions import InvalidSchemaException
from jambo.parser._type_parser import GenericTypeParser
from jambo.types.json_schema_type import JSONSchemaNativeTypes
from jambo.types.type_parser_options import TypeParserOptions

from pydantic import AfterValidator
from typing_extensions import Annotated, Any, Literal, Unpack


class ConstTypeParser(GenericTypeParser):
    json_schema_type = "const"

    default_mappings = {
        "const": "default",
        "description": "description",
        "examples": "examples",
    }

    def from_properties_impl(
        self, name, properties, **kwargs: Unpack[TypeParserOptions]
    ):
        if "const" not in properties:
            raise InvalidSchemaException(
                f"Const type {name} must have 'const' property defined.",
                invalid_field="const",
            )

        const_value = properties["const"]

        if not isinstance(const_value, JSONSchemaNativeTypes):
            raise InvalidSchemaException(
                f"Const type {name} must have 'const' value of allowed types: {JSONSchemaNativeTypes}.",
                invalid_field="const",
            )

        const_type = self._build_const_type(const_value)
        parsed_properties = self.mappings_properties_builder(properties, **kwargs)

        return const_type, parsed_properties

    def _build_const_type(self, const_value):
        # Try to use Literal for hashable types (required for discriminated unions)
        # Fall back to validator approach for non-hashable types
        try:
            # Test if the value is hashable (can be used in Literal)
            hash(const_value)
            return Literal[const_value]
        except TypeError:
            # Non-hashable type (like list, dict), use validator approach
            def _validate_const_value(value: Any) -> Any:
                if value != const_value:
                    raise ValueError(
                        f"Value must be equal to the constant value: {const_value}"
                    )
                return value

            return Annotated[type(const_value), AfterValidator(_validate_const_value)]
