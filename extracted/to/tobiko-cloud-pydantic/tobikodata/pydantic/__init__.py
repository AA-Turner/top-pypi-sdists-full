from __future__ import annotations

import json
import typing as t

import pydantic
from pydantic.fields import FieldInfo
from typing_extensions import Self

from tobikodata.pydantic.utils import value_to_json

if t.TYPE_CHECKING:
    BaseModelType = t.TypeVar("BaseModelType", bound=pydantic.BaseModel)  # noqa: TID251


T = t.TypeVar("T")
DEFAULT_ARGS = {"exclude_none": True, "by_alias": True}
PRIVATE_FIELDS = "__pydantic_private__"
PYDANTIC_MAJOR_VERSION, PYDANTIC_MINOR_VERSION = [int(p) for p in pydantic.__version__.split(".")][
    :2
]


if t.TYPE_CHECKING:
    from sqlglot import Expression  # pants: no-infer-dep


class PydanticModel(pydantic.BaseModel):  # noqa: TID251
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        protected_namespaces=(),
    )

    _hash_func_mapping: t.ClassVar[t.Dict[t.Type[t.Any], t.Callable[[t.Any], int]]] = {}

    @classmethod
    def fields(cls) -> t.Iterable[str]:
        return cls.model_fields.keys()

    def dump(self, fields: t.Optional[t.Iterable[str]] = None) -> t.Dict[str, t.Any]:
        if fields is None:
            fields = self.fields()
        payload = {}
        for field in fields:
            value = getattr(self, field)
            if isinstance(value, (list, dict, pydantic.BaseModel)):  # noqa: TID251
                payload[field] = value_to_json(value)
            else:
                payload[field] = value
        return payload

    def dict(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        kwargs = {**DEFAULT_ARGS, **kwargs}
        return super().model_dump(**kwargs)  # type: ignore

    def json(
        self,
        **kwargs: t.Any,
    ) -> str:
        kwargs = {**DEFAULT_ARGS, **kwargs}
        # Pydantic v2 doesn't support arbitrary arguments for json.dump().
        if kwargs.pop("sort_keys", False):
            return json.dumps(super().model_dump(mode="json", **kwargs), sort_keys=True)

        return super().model_dump_json(**kwargs)

    def copy(self: "BaseModelType", **kwargs: t.Any) -> "BaseModelType":
        return super().model_copy(**kwargs)

    @property
    def fields_set(self: "BaseModelType") -> t.Set[str]:
        return self.__pydantic_fields_set__

    @classmethod
    def parse_obj(cls: t.Type["BaseModelType"], obj: t.Any) -> "BaseModelType":
        return super().model_validate(obj)

    @classmethod
    def parse_raw(
        cls: t.Type["BaseModelType"], b: t.Union[str, bytes], **kwargs: t.Any
    ) -> "BaseModelType":
        return super().model_validate_json(b, **kwargs)

    @classmethod
    def missing_required_fields(
        cls: t.Type["PydanticModel"], provided_fields: t.Set[str]
    ) -> t.Set[str]:
        return cls.required_fields() - provided_fields

    @classmethod
    def extra_fields(cls: t.Type["PydanticModel"], provided_fields: t.Set[str]) -> t.Set[str]:
        return provided_fields - cls.all_fields()

    @classmethod
    def all_fields(cls: t.Type["PydanticModel"]) -> t.Set[str]:
        return cls._fields()

    @classmethod
    def all_field_infos(cls: t.Type["PydanticModel"]) -> t.Dict[str, FieldInfo]:
        return cls.model_fields

    @classmethod
    def required_fields(cls: t.Type["PydanticModel"]) -> t.Set[str]:
        return cls._fields(lambda field: field.is_required())

    @classmethod
    def _fields(
        cls: t.Type["PydanticModel"],
        predicate: t.Callable[[t.Any], bool] = lambda _: True,
    ) -> t.Set[str]:
        return {
            field_info.alias if field_info.alias else field_name
            for field_name, field_info in cls.all_field_infos().items()
            if predicate(field_info)
        }

    def __eq__(self, other: t.Any) -> bool:
        if (PYDANTIC_MAJOR_VERSION, PYDANTIC_MINOR_VERSION) < (2, 6):
            if isinstance(other, pydantic.BaseModel):  # noqa: TID251
                return self.dict() == other.dict()
            else:
                return self.dict() == other
        return super().__eq__(other)

    def __hash__(self) -> int:
        if (PYDANTIC_MAJOR_VERSION, PYDANTIC_MINOR_VERSION) < (2, 6):
            obj = {k: v for k, v in self.__dict__.items() if k in self.all_field_infos()}
            return hash(self.__class__) + hash(tuple(obj.values()))

        from pydantic._internal._model_construction import make_hash_func  # type: ignore

        if self.__class__ not in PydanticModel._hash_func_mapping:
            PydanticModel._hash_func_mapping[self.__class__] = make_hash_func(self.__class__)

        return PydanticModel._hash_func_mapping[self.__class__](self)

    def __str__(self) -> str:
        args = []

        for k, info in self.all_field_infos().items():
            v = getattr(self, k)

            if type(v) != type(info.default) or v != info.default:
                args.append(f"{k}: {v}")

        return f"{self.__class__.__name__}<{', '.join(args)}>"

    def __repr__(self) -> str:
        return str(self)


class ForwardCompatiblePydanticModel(PydanticModel):
    model_config = pydantic.ConfigDict(
        **{
            **PydanticModel.model_config,
            **{
                "extra": "allow",
            },
        }
    )


class ComputedColumn:
    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    @classmethod
    def is_computed_column(cls, field_info: FieldInfo) -> bool:
        """Helper function to determine if a Pydantic field has a ComputedColumn annotation."""
        for metadata in field_info.metadata:
            if isinstance(metadata, cls):
                return True
        return False

    @classmethod
    def get_expression(cls, field_info: FieldInfo) -> Expression:
        """Helper function to get a ComputedColumn's SQLGlot expression from a Pydantic FieldInfo object."""
        for metadata in field_info.metadata:
            if isinstance(metadata, cls):
                return metadata.expression
        raise ValueError("Field is not a computed column")


class PydanticRecord(PydanticModel):
    @classmethod
    def fields(cls) -> t.List[str]:
        return [k for k, v in cls.model_fields.items() if not ComputedColumn.is_computed_column(v)]


class PydanticVersionRecord(PydanticModel):
    @classmethod
    def no_version(cls) -> Self:
        kwargs = {
            name: 0 if field_info.annotation == int else "0.0.0"
            for name, field_info in cls.model_fields.items()
        }
        return cls.parse_obj(kwargs)
