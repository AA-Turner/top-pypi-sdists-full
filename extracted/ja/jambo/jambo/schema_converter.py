from jambo.exceptions import InvalidSchemaException, UnsupportedSchemaException
from jambo.parser import ObjectTypeParser, RefTypeParser
from jambo.types import JSONSchema, RefCacheDict

from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for
from pydantic import BaseModel
from typing_extensions import MutableMapping, Optional


class SchemaConverter:
    """
    Converts JSON Schema to Pydantic models.

    This class is responsible for converting JSON Schema definitions into Pydantic models.
    It validates the schema and generates the corresponding Pydantic model with appropriate
    fields and types. The generated model can be used for data validation and serialization.
    """

    _namespace_registry: MutableMapping[str, RefCacheDict]

    def __init__(
        self, namespace_registry: Optional[MutableMapping[str, RefCacheDict]] = None
    ) -> None:
        if namespace_registry is None:
            namespace_registry = dict()
        self._namespace_registry = namespace_registry

    def build_with_cache(
        self,
        schema: JSONSchema,
        ref_cache: Optional[RefCacheDict] = None,
        without_cache: bool = False,
    ) -> type[BaseModel]:
        """
        Converts a JSON Schema to a Pydantic model.
        This is the instance method version of `build` and uses the instance's reference cache if none is provided.
        Use this method if you want to utilize the instance's reference cache.

            :param schema: The JSON Schema to convert.
            :param ref_cache: An optional reference cache to use during conversion.
            :param without_cache: Whether to use a clean reference cache for this conversion.
            :return: The generated Pydantic model.
        """
        local_ref_cache: RefCacheDict

        if without_cache:
            local_ref_cache = dict()
        elif ref_cache is None:
            namespace = schema.get("$id", "default")
            local_ref_cache = self._namespace_registry.setdefault(namespace, dict())
        else:
            local_ref_cache = ref_cache

        return self.build(schema, local_ref_cache)

    @staticmethod
    def build(
        schema: JSONSchema, ref_cache: Optional[RefCacheDict] = None
    ) -> type[BaseModel]:
        """
        Converts a JSON Schema to a Pydantic model.
        This method doesn't use a reference cache if none is provided.
            :param schema: The JSON Schema to convert.
            :param ref_cache: An optional reference cache to use during conversion, if provided `with_clean_cache` will be ignored.
            :return: The generated Pydantic model.
        """
        if ref_cache is None:
            ref_cache = dict()

        try:
            validator = validator_for(schema)
            validator.check_schema(schema)  # type: ignore
        except SchemaError as err:
            raise InvalidSchemaException(
                "Validation of JSON Schema failed.", cause=err
            ) from err

        if "title" not in schema:
            raise InvalidSchemaException(
                "Schema must have a title.", invalid_field="title"
            )

        schema_type = SchemaConverter._get_schema_type(schema)

        match schema_type:
            case "object":
                return ObjectTypeParser.to_model(
                    schema["title"],
                    schema.get("properties", {}),
                    schema.get("required", []),
                    description=schema.get("description"),
                    context=schema,
                    ref_cache=ref_cache,
                    required=True,
                )

            case "$ref":
                parsed_model, _ = RefTypeParser().from_properties(
                    schema["title"],
                    schema,
                    context=schema,
                    ref_cache=ref_cache,
                    required=True,
                )
                return parsed_model
            case _:
                unsupported_type = (
                    f"type:{schema_type}" if schema_type else "missing type"
                )
                raise UnsupportedSchemaException(
                    "Only object and $ref schema types are supported.",
                    unsupported_field=unsupported_type,
                )

    def clear_ref_cache(self, namespace: Optional[str] = "default") -> None:
        """
        Clears the reference cache.
        """
        if namespace is None:
            self._namespace_registry.clear()
            return

        if namespace in self._namespace_registry:
            self._namespace_registry[namespace].clear()

    def get_cached_ref(
        self, ref_name: str, namespace: str = "default"
    ) -> Optional[type]:
        """
        Gets a cached reference from the reference cache.
        :param ref_name: The name of the reference to get.
        :return: The cached reference, or None if not found.
        """
        cached_type = self._namespace_registry.get(namespace, {}).get(ref_name)

        if isinstance(cached_type, type):
            return cached_type

        return None

    @staticmethod
    def _get_schema_type(schema: JSONSchema) -> str | None:
        """
        Returns the type of the schema.
        :param schema: The JSON Schema to check.
        :return: The type of the schema.
        """
        if "$ref" in schema:
            return "$ref"

        type_value = schema.get("type")
        if isinstance(type_value, list):
            raise InvalidSchemaException(
                "Invalid schema: 'type' cannot be a list at the top level",
                invalid_field=str(schema),
            )

        return type_value
