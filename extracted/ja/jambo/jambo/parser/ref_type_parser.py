from jambo.exceptions import InternalAssertionException, InvalidSchemaException
from jambo.parser import GenericTypeParser
from jambo.types import RefCacheDict
from jambo.types.json_schema_type import JSONSchema
from jambo.types.type_parser_options import TypeParserOptions

from typing_extensions import ForwardRef, Literal, Union, Unpack


RefType = Union[type, ForwardRef]

RefStrategy = Literal["forward_ref", "def_ref"]


class RefTypeParser(GenericTypeParser):
    json_schema_type = "$ref"

    def from_properties_impl(
        self, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ) -> tuple[RefType, dict]:
        if "$ref" not in properties:
            raise InvalidSchemaException(
                f"Missing $ref in properties for {name}", invalid_field="$ref"
            )

        if kwargs.get("context") is None:
            raise InternalAssertionException(
                "`context` must be provided in kwargs for RefTypeParser"
            )

        ref_cache = kwargs.get("ref_cache")
        if ref_cache is None:
            raise InternalAssertionException(
                "`ref_cache` must be provided in kwargs for RefTypeParser"
            )

        mapped_properties = self.mappings_properties_builder(properties, **kwargs)

        ref_strategy, ref_name, ref_property = self._examine_ref_strategy(
            name, properties, **kwargs
        )

        ref_state = self._get_ref_from_cache(ref_name, ref_cache)
        if ref_state is not None:
            # If the reference is either processing or already cached
            return ref_state, mapped_properties

        ref = self._parse_from_strategy(ref_strategy, ref_name, ref_property, **kwargs)
        ref_cache[ref_name] = ref

        return ref, mapped_properties

    def _parse_from_strategy(
        self,
        ref_strategy: RefStrategy,
        ref_name: str,
        ref_property: JSONSchema,
        **kwargs: Unpack[TypeParserOptions],
    ) -> RefType:
        mapped_type: RefType
        match ref_strategy:
            case "forward_ref":
                mapped_type = ForwardRef(ref_name)
            case "def_ref":
                mapped_type, _ = GenericTypeParser.type_from_properties(
                    ref_name, ref_property, **kwargs
                )
            case _:
                raise InvalidSchemaException(
                    f"Unsupported $ref {ref_property['$ref']}", invalid_field="$ref"
                )

        return mapped_type

    def _get_ref_from_cache(
        self, ref_name: str, ref_cache: RefCacheDict
    ) -> RefType | type | None:
        try:
            ref_state = ref_cache[ref_name]

            if ref_state is None:
                # If the reference is being processed, we return a ForwardRef
                return ForwardRef(ref_name)

            # If the reference is already cached, we return it
            return ref_state
        except KeyError:
            # If the reference is not in the cache, we will set it to None
            ref_cache[ref_name] = None

        return None

    def _examine_ref_strategy(
        self, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ) -> tuple[RefStrategy, str, JSONSchema]:
        if properties.get("$ref") == "#":
            ref_name = kwargs["context"].get("title")
            if ref_name is None:
                raise InvalidSchemaException(
                    "Missing title in properties for $ref of Root Reference",
                    invalid_field="title",
                )
            return "forward_ref", ref_name, {}

        if properties.get("$ref", "").startswith("#/$defs/"):
            target_name, target_property = self._extract_target_ref(
                name, properties, **kwargs
            )
            return "def_ref", target_name, target_property

        raise InvalidSchemaException(
            "Only Root and $defs references are supported at the moment",
            invalid_field="$ref",
        )

    def _extract_target_ref(
        self, name: str, properties: JSONSchema, **kwargs: Unpack[TypeParserOptions]
    ) -> tuple[str, JSONSchema]:
        target_name = None
        target_property = kwargs["context"]
        for prop_name in properties["$ref"].split("/")[1:]:
            if prop_name not in target_property:
                raise InvalidSchemaException(
                    f"Missing {prop_name} in properties for $ref {properties['$ref']}",
                    invalid_field=prop_name,
                )
            target_name = prop_name
            target_property = target_property[prop_name]  # type: ignore

        if not isinstance(target_name, str) or target_property is None:
            raise InvalidSchemaException(
                f"Invalid $ref {properties['$ref']}", invalid_field="$ref"
            )

        return target_name, target_property
