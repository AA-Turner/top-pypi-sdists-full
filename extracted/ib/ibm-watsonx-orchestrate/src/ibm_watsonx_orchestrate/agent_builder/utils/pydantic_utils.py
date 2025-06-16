import json
from pathlib import Path
from typing import Any, Dict, Type, Literal

import jsonschema
from pydantic import BaseModel
from pydantic.json_schema import DEFAULT_REF_TEMPLATE, GenerateJsonSchema, JsonSchemaMode
from pydantic.main import IncEx
from typing_extensions import Self

from ibm_watsonx_orchestrate.agent_builder.tools import ToolRequestBody, ToolResponseBody, JsonSchemaObject


def generate_schema_only_base_model(schema: ToolRequestBody | ToolResponseBody | JsonSchemaObject) -> Type[BaseModel]:
    class SchemaOnlyBaseModel(BaseModel):
        __primitive__: Any
        model_config = {
            'extra': 'allow'
        }
        """
        The purpose of a SchemaOnlyBaseModel is to pass along the json schema represented by schema
        to a langchain tool's arg_schema
        :arg schema The json schema to emulate
        :returns a fake BaseModel that only returns a json schema
        """

        def __init__(self, /, *args, **kwargs: Any) -> None:
            if schema.type == 'object':
                super().__init__(**kwargs)
                for name, value in kwargs.items():
                    setattr(self, name, value)
            else:
                kwargs={}
                kwargs['__primitive__'] = args[0]
                super().__init__(**kwargs)
                setattr(self, '__primitive__', args[0])

        @classmethod
        def model_json_schema(cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE,
                              schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
                              mode: JsonSchemaMode = 'validation') -> dict[str, Any]:
            return schema.model_dump(exclude_unset=True, exclude_none=True)

        @classmethod
        def schema(cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE) -> Dict[str, Any]:
            return schema.model_dump(exclude_unset=True, exclude_none=True)

        @classmethod
        def schema_json(cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE,
                        **dumps_kwargs: Any) -> str:
            return schema.model_dump_json(exclude_unset=True, exclude_none=True)

        @classmethod
        def model_validate_json(cls, json_data: str | bytes | bytearray, *, strict: bool | None = None,
                                context: Any | None = None) -> Self:
            obj = json.loads(json_data)
            jsonschema.validate(obj, schema=schema.model_dump(exclude_unset=True))
            if schema.type == 'object':
                return SchemaOnlyBaseModel(**obj)
            else:
                return SchemaOnlyBaseModel(obj)

        @classmethod
        def model_validate(cls, obj: Any, *, strict: bool | None = None, from_attributes: bool | None = None,
                           context: Any | None = None) -> Self:
            jsonschema.validate(obj, schema=schema.model_dump(exclude_unset=True))
            if schema.type == 'object':
                return SchemaOnlyBaseModel(**obj)
            else:
                return SchemaOnlyBaseModel(obj)

        @classmethod
        def model_validate_strings(cls, obj: Any, *, strict: bool | None = None, context: Any | None = None) -> Self:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def validate(cls, value: Any) -> Self:
            jsonschema.validate(value, schema=schema.model_dump(exclude_unset=True))
            return SchemaOnlyBaseModel(**value)

        @classmethod
        def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def model_rebuild(cls, *, force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2,
                          _types_namespace: Any = None) -> bool | None:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def parse_obj(cls, obj: Any) -> Self:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def parse_raw(cls, b: str | bytes, *, content_type: str | None = None, encoding: str = 'utf8',
                      proto: Any | None = None, allow_pickle: bool = False) -> Self:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def parse_file(cls, path: str | Path, *, content_type: str | None = None, encoding: str = 'utf8',
                       proto: Any | None = None, allow_pickle: bool = False) -> Self:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def from_orm(cls, obj: Any) -> Self:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        @classmethod
        def update_forward_refs(cls, **localns: Any) -> None:
            raise NotImplementedError('unimplemented for SchemaOnlyBaseModel')

        def model_dump(self, *, mode: Literal['json', 'python'] | str = 'python', include: IncEx | None = None,
                       exclude: IncEx | None = None, context: Any | None = None, by_alias: bool = False,
                       exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False,
                       round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True,
                       serialize_as_any: bool = False) -> dict[str, Any]:
            primitive = getattr(self, '__primitive__', None)
            if primitive is not None:
                return primitive
            else:
                return super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias,
                                          exclude_unset=exclude_unset, exclude_defaults=exclude_defaults,
                                          exclude_none=exclude_none, round_trip=round_trip, warnings=warnings,
                                          serialize_as_any=serialize_as_any)

        def model_dump_json(self, *, indent: int | None = None, include: IncEx | None = None,
                            exclude: IncEx | None = None, context: Any | None = None, by_alias: bool = False,
                            exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False,
                            round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True,
                            serialize_as_any: bool = False) -> str:
            primitive = getattr(self, '__primitive__')
            if primitive is not None:
                return json.dumps(primitive)
            else:
                return super().model_dump_json(indent=indent, include=include, exclude=exclude, context=context,
                                           by_alias=by_alias, exclude_unset=exclude_unset,
                                           exclude_defaults=exclude_defaults, exclude_none=exclude_none,
                                           round_trip=round_trip, warnings=warnings, serialize_as_any=serialize_as_any)

    return SchemaOnlyBaseModel

