from __future__ import annotations

import sys
import typing as t

import marshmallow as ma
import marshmallow.validate
import marshmallow_oneofschema  # type: ignore

from . import create_patch_schema
from .schema_version_checker import verify_schema_version, version_safe_type_schemas


class DataTypeField(ma.fields.String):
    def __init__(self, value, *args, **kwargs) -> None:
        self._DATA_TYPE = value
        super().__init__(
            *args,
            dump_default=value,
            required=True,
            validate=ma.validate.Equal(value),
            metadata={"description": "Type of this document"},
            **kwargs,
        )


class OneOfSchema(marshmallow_oneofschema.OneOfSchema):
    _DATA_TYPE: t.ClassVar[str]
    private_schema: t.ClassVar[OneOfSchema]
    public_schema: t.ClassVar[OneOfSchema]
    patch_schema: t.ClassVar[OneOfSchema]

    metadata: t.ClassVar[t.Dict[str, t.Any]]

    private: t.ClassVar[t.List[str]] = []


class Schema(ma.Schema):
    _DATA_TYPE: t.ClassVar[str]
    DATA_TYPE: t.ClassVar[DataTypeField]

    metadata: t.ClassVar[t.Dict[str, t.Any]]

    @ma.validates("DATA_TYPE")
    def validate_data_type(self, data, **kwargs):
        verify_schema_version(data, self._DATA_TYPE)

    private_schema: t.ClassVar[Schema]
    public_schema: t.ClassVar[Schema]
    patch_schema: t.ClassVar[Schema]

    private: t.ClassVar[t.List[str]] = []


if sys.version_info < (3, 9):
    _type_schema = version_safe_type_schemas()
else:
    # After pyupgrade and there is no < (3, 9) branch, _type_schema can
    # be reintegrated below.
    _type_schema = version_safe_type_schemas[str, ma.Schema]()


class DataTypeSchema(marshmallow_oneofschema.OneOfSchema):
    type_field = "DATA_TYPE"
    type_schemas = _type_schema
    type_field_remove = False
    __oneof_schemas: t.ClassVar = {}

    def __getattr__(self, name):
        if name in self.__class__.__oneof_schemas:
            return self.__class__.__oneof_schemas[name]
        else:
            raise AttributeError(name)

    @property
    def schemas(self) -> t.List[Schema]:
        return list(self.__class__.__oneof_schemas.values())

    @classmethod
    def register_schema(
        cls,
        schema: Schema,
        register_data_type: bool = True,
        schema_base_name: t.Optional[str] = None,
        private: bool = False,
    ) -> None:
        DATA_TYPE = schema._DATA_TYPE

        if register_data_type:
            cls.type_schemas[DATA_TYPE] = schema

        base_data_type, version = DATA_TYPE.split("#", 1)

        if schema_base_name:
            base_name = schema_base_name
        else:
            base_name = base_data_type.title().replace("_", "")
        major, minor, patch = (int(i) for i in version.split("."))

        if major == 1:
            base_name_key = base_name
        else:
            base_name_key = f"{base_name}_{major}"

        if base_name_key not in cls.__oneof_schemas:

            class data_type_oneof(OneOfSchema):
                __doc__ = schema.__doc__
                _DATA_TYPE: t.ClassVar[str] = DATA_TYPE
                type_field = "DATA_TYPE"
                type_schemas = _type_schema
                type_field_remove = False
                metadata: t.ClassVar[t.Dict[str, t.Any]] = {}

                def get_obj_type(self, obj):
                    return self._DATA_TYPE

            data_type_oneof.__name__ = base_name_key
            instance = data_type_oneof(load_only=schema.private)
            cls.__oneof_schemas[base_name_key] = instance

            class data_type_oneof_private(OneOfSchema):
                __doc__ = schema.__doc__
                _DATA_TYPE: t.ClassVar[str] = DATA_TYPE
                type_field = "DATA_TYPE"
                type_schemas = _type_schema
                type_field_remove = False
                metadata: t.ClassVar[t.Dict[str, t.Any]] = {}

                def get_obj_type(self, obj):
                    return self._DATA_TYPE

            data_type_oneof_private.__name__ = f"{base_name_key}Private"

            class data_type_oneof_patch(OneOfSchema):
                __doc__ = schema.__doc__
                _DATA_TYPE: t.ClassVar[str] = DATA_TYPE
                type_field = "DATA_TYPE"
                type_schemas = _type_schema
                type_field_remove = False
                metadata: t.ClassVar[t.Dict[str, t.Any]] = {}

                def get_obj_type(self, obj):
                    return self._DATA_TYPE

            data_type_oneof_patch.__name__ = f"{base_name_key}Patch"

            if private:
                data_type_oneof.metadata["x-private"] = True
                data_type_oneof_private.metadata["x-private"] = True
                data_type_oneof_patch.metadata["x-private"] = True

            data_type_oneof.public_schema = instance
            data_type_oneof.private_schema = data_type_oneof_private()
            data_type_oneof.patch_schema = data_type_oneof_patch(partial=True)
            cls.__oneof_schemas[base_name_key] = data_type_oneof()

        oo = cls.__oneof_schemas[base_name_key]
        oo.type_schemas[DATA_TYPE] = schema
        for private_prop in schema.private:
            oo.load_only.add(private_prop)
        oo.private_schema.__class__.type_schemas[DATA_TYPE] = schema.private_schema
        oo.patch_schema.__class__.type_schemas[DATA_TYPE] = schema.patch_schema

        old_major, old_minor, old_patch = (
            int(i) for i in oo._DATA_TYPE.split("#", 1)[1].split(".")
        )
        if (
            major > old_major
            or (major == old_major and minor > old_minor)
            or (major == old_major and minor == old_minor and patch > old_patch)
        ):
            oo._DATA_TYPE = DATA_TYPE
            oo.private_schema._DATA_TYPE = DATA_TYPE
            oo.public_schema._DATA_TYPE = DATA_TYPE
            oo.public_schema.private = schema.private
            oo.patch_schema._DATA_TYPE = DATA_TYPE

            oo.__doc__ = schema.__doc__
            oo.private_schema.__doc__ = schema.__doc__
            oo.patch_schema.__doc__ = schema.__doc__

    @classmethod
    def schema_for(cls, DATA_TYPE) -> ma.Schema:
        return cls.type_schemas[DATA_TYPE]

    @classmethod
    def schema_for_base_name(cls, base_name: str) -> OneOfSchema:
        return cls.__oneof_schemas[base_name]


data_type_schema = DataTypeSchema()


T = t.TypeVar("T", bound=t.Type[Schema])


def data_type(
    discriminator: str,
    register_data_type: bool = True,
    private: bool = False,
    schema_base_name: t.Optional[str] = None,
) -> t.Callable[[T], T]:
    def decorator(cls: T) -> T:
        cls._DATA_TYPE = discriminator
        cls.DATA_TYPE = DataTypeField(discriminator)
        cls._declared_fields["DATA_TYPE"] = cls.DATA_TYPE
        cls.private_schema = cls()
        cls.public_schema = cls(load_only=cls.private)
        cls.patch_schema = create_patch_schema(cls)
        if not hasattr(cls, "metadata"):
            cls.metadata = {}

        if private:
            cls.metadata["x-private"] = True

        inst = cls.public_schema
        DataTypeSchema.register_schema(
            inst,
            register_data_type=register_data_type,
            schema_base_name=schema_base_name,
            private=private,
        )
        return cls

    return decorator
