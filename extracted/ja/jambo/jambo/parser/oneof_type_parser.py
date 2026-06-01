from jambo.exceptions import InvalidSchemaException
from jambo.parser._type_parser import GenericTypeParser
from jambo.types.type_parser_options import TypeParserOptions

from pydantic import BaseModel, BeforeValidator, Field, TypeAdapter, ValidationError
from typing_extensions import Annotated, Any, Union, Unpack, get_args


Annotation = Annotated[Any, ...]


class OneOfTypeParser(GenericTypeParser):
    mapped_type = Union

    json_schema_type = "oneOf"

    def from_properties_impl(
        self, name, properties, **kwargs: Unpack[TypeParserOptions]
    ):
        if "oneOf" not in properties:
            raise InvalidSchemaException(
                f"Invalid JSON Schema: {properties}", invalid_field="oneOf"
            )

        if not isinstance(properties["oneOf"], list) or len(properties["oneOf"]) == 0:
            raise InvalidSchemaException(
                f"Invalid JSON Schema: {properties['oneOf']}", invalid_field="oneOf"
            )

        mapped_properties = self.mappings_properties_builder(properties, **kwargs)

        sub_types = [
            GenericTypeParser.type_from_properties(
                f"{name}_sub{i}", subProperty, **kwargs
            )
            for i, subProperty in enumerate(properties["oneOf"])
        ]

        if not kwargs.get("required", False):
            mapped_properties["default"] = mapped_properties.get("default")

        subfield_types = [Annotated[t, Field(**v)] for t, v in sub_types]

        # Added with the understanding of discriminator are not in the JsonSchema Spec,
        # they were added by OpenAPI and not all implementations may support them,
        # and they do not always generate a model one-to-one to the Pydantic model
        # TL;DR: Discriminators were added by OpenAPI and not a Official JSON Schema feature
        if (discriminator := properties.get("discriminator")) is not None:
            validated_type = self._build_type_one_of_with_discriminator(
                subfield_types, discriminator
            )
        else:
            validated_type = self._build_type_one_of_with_func(subfield_types)

        return validated_type, mapped_properties

    @staticmethod
    def _build_type_one_of_with_discriminator(
        subfield_types: list[Annotation], discriminator_prop: dict
    ) -> Annotation:
        """
        Build a type with a discriminator.
        """
        if not isinstance(discriminator_prop, dict):
            raise InvalidSchemaException(
                "Discriminator must be a dictionary", invalid_field="discriminator"
            )

        for field in subfield_types:
            field_type, field_info = get_args(field)

            if issubclass(field_type, BaseModel):
                continue

            raise InvalidSchemaException(
                "When using a discriminator, all subfield types must be of type 'object'.",
                invalid_field="discriminator",
            )

        property_name = discriminator_prop.get("propertyName")
        if property_name is None or not isinstance(property_name, str):
            raise InvalidSchemaException(
                "Discriminator must have a 'propertyName' key",
                invalid_field="propertyName",
            )

        return Annotated[Union[(*subfield_types,)], Field(discriminator=property_name)]

    @staticmethod
    def _build_type_one_of_with_func(subfield_types: list[Annotation]) -> Annotation:
        """
        Build a type with a validation function for the oneOf constraint.
        """

        def validate_one_of(value: Any) -> Any:
            matched_count = 0

            for field_type in subfield_types:
                try:
                    TypeAdapter(field_type).validate_python(value)
                    matched_count += 1
                except ValidationError:
                    continue

            if matched_count == 0:
                raise ValueError("Value does not match any of the oneOf schemas")
            elif matched_count > 1:
                raise ValueError(
                    "Value matches multiple oneOf schemas, exactly one expected"
                )

            return value

        return Annotated[Union[(*subfield_types,)], BeforeValidator(validate_one_of)]
