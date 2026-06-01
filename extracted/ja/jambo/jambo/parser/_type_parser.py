from jambo.exceptions import InvalidSchemaException
from jambo.types.type_parser_options import JSONSchema, TypeParserOptions

from pydantic import Field, TypeAdapter
from typing_extensions import Annotated, Any, ClassVar, Generic, Self, TypeVar, Unpack

from abc import ABC, abstractmethod


T = TypeVar("T", bound=type)


class GenericTypeParser(ABC, Generic[T]):
    json_schema_type: ClassVar[str]

    type_mappings: dict[str, str] = {}

    default_mappings = {
        "default": "default",
        "description": "description",
        "examples": "examples",
        "title": "title",
        "deprecated": "deprecated",
    }

    @abstractmethod
    def from_properties_impl(
        self, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ) -> tuple[T, dict]:
        """
        Abstract method to convert properties to a type and its fields properties.
        :param name: The name of the type.
        :param properties: The properties of the type.
        :param kwargs: Additional options for type parsing.
        :return: A tuple containing the type and its properties.
        """

    def from_properties(
        self, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ) -> tuple[T, dict]:
        """
        Converts properties to a type and its fields properties.
        :param name: The name of the type.
        :param properties: The properties of the type.
        :param kwargs: Additional options for type parsing.
        :return: A tuple containing the type and its properties.
        """
        parsed_type, parsed_properties = self.from_properties_impl(
            name, properties, **kwargs
        )

        if not self._validate_default(parsed_type, parsed_properties):
            raise InvalidSchemaException(
                "Default value is not valid", invalid_field=name
            )

        if not self._validate_examples(parsed_type, parsed_properties):
            raise InvalidSchemaException(
                "Examples values are not valid", invalid_field=name
            )

        return parsed_type, parsed_properties

    @classmethod
    def type_from_properties(
        cls, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ) -> tuple[type, dict]:
        """
        Factory method to fetch the appropriate type parser based on properties
        and generates the equivalent type and fields.
        :param name: The name of the type to be created.
        :param properties: The properties that define the type.
        :param kwargs: Additional options for type parsing.
        :return: A tuple containing the type and its properties.
        """

        parser = cls._get_impl(cls._normalize_properties(properties))

        return parser().from_properties(name=name, properties=properties, **kwargs)

    @staticmethod
    def _normalize_properties(properties: JSONSchema) -> JSONSchema:
        """
        Normalizes the properties dictionary to ensure consistent structure.
        :param properties: The properties to be normalized.
        """
        type_value = properties.pop("type", None)

        if isinstance(type_value, str):
            properties["type"] = type_value
            return properties

        if isinstance(type_value, list) and len(type_value) == 0:
            raise InvalidSchemaException(
                "Invalid schema: 'type' list cannot be empty",
                invalid_field=str(properties),
            )

        if isinstance(type_value, list) and len(type_value) == 1:
            properties["type"] = type_value[0]
            return properties

        if isinstance(type_value, list):
            properties["anyOf"] = [{"type": t} for t in type_value]
            return properties

        return properties

    @classmethod
    def _get_impl(cls, properties: JSONSchema) -> type[Self]:
        for subcls in cls.__subclasses__():
            schema_type, schema_value = subcls._get_schema_type()

            if schema_type not in properties:
                continue

            if schema_value is None or schema_value == properties[schema_type]:  # type: ignore
                return subcls

        raise InvalidSchemaException(
            "No suitable type parser found", invalid_field=str(properties)
        )

    @classmethod
    def _get_schema_type(cls) -> tuple[str, str | None]:
        if cls.json_schema_type is None:
            raise RuntimeError(
                f"TypeParser: json_schema_type not defined for subclass {cls.__name__}"
            )

        schema_definition = cls.json_schema_type.split(":")

        if len(schema_definition) == 1:
            return schema_definition[0], None

        return schema_definition[0], schema_definition[1]

    def mappings_properties_builder(
        self, properties, **kwargs: Unpack[TypeParserOptions]
    ) -> dict[str, Any]:
        if not kwargs.get("required", False):
            properties["default"] = properties.get("default", None)

        mappings = self.default_mappings | self.type_mappings

        return {
            mappings[key]: value for key, value in properties.items() if key in mappings
        }

    @staticmethod
    def _validate_default(field_type: T, field_prop: dict) -> bool:
        value = field_prop.get("default")

        if value is None and field_prop.get("default_factory") is not None:
            value = field_prop["default_factory"]()

        if value is None:
            return True

        return GenericTypeParser._is_valid_value(field_type, field_prop, value)

    @staticmethod
    def _validate_examples(field_type: T, field_prop: dict) -> bool:
        examples = field_prop.get("examples")

        if examples is None:
            return True

        if not isinstance(examples, list):
            return False

        return all(
            GenericTypeParser._is_valid_value(field_type, field_prop, e)
            for e in examples
        )

    @staticmethod
    def _is_valid_value(field_type: T, field_prop: dict, value: Any) -> bool:
        try:
            field = Annotated[field_type, Field(**field_prop)]  # type: ignore
            TypeAdapter(field).validate_python(value)
        except Exception as _:
            return False

        return True
