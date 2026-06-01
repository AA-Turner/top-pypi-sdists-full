from jambo.types.json_schema_type import JSONSchema

from typing_extensions import ForwardRef, MutableMapping, TypedDict


RefCacheDict = MutableMapping[str, ForwardRef | type | None]


class TypeParserOptions(TypedDict):
    required: bool
    context: JSONSchema
    ref_cache: RefCacheDict
