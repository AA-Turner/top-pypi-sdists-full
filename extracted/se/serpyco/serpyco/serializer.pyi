import typing

from .encoder import FieldEncoder
from .util import JsonDict

D = typing.TypeVar("D")

class Serializer(typing.Generic[D]):
    def __init__(
        self,
        dataclass: typing.Type[D],
        omit_none: bool = ...,
        type_encoders: typing.Optional[typing.Dict[type, FieldEncoder]] = ...,
        only: typing.Optional[typing.List[str]] = ...,
        exclude: typing.Optional[typing.List[str]] = ...,
        strict: bool = ...,
        load_as_type: typing.Optional[type] = ...,
    ) -> None: ...
    def json_schema(self, many: bool = ...) -> JsonDict: ...
    def get_dict_path(self, obj_path: typing.Sequence[str]) -> typing.List[str]: ...
    def get_object_path(self, dict_path: typing.Sequence[str]) -> typing.List[str]: ...
    @classmethod
    def register_global_type(
        cls, field_type: typing.Any, encoder: FieldEncoder
    ) -> None: ...
    @classmethod
    def unregister_global_type(cls, field_type: typing.Any) -> None: ...
    def dataclass(self) -> type: ...
    @typing.overload
    def dump(
        self,
        obj: typing.Iterable[D],
        validate: bool,
        many: typing.Literal[True],
    ) -> typing.List[JsonDict]: ...
    @typing.overload
    def dump(
        self,
        obj: D,
        validate: bool = False,
        many: typing.Literal[False] = ...,
    ) -> JsonDict: ...
    @typing.overload
    def dump(
        self,
        obj: typing.Union[D, typing.Iterable[D]],
        validate: bool = False,
        many: bool = False,
    ) -> typing.Union[JsonDict, typing.List[JsonDict]]: ...
    @typing.overload
    def load(
        self,
        data: typing.Iterable[JsonDict],
        validate: bool,
        many: typing.Literal[True],
    ) -> typing.List[D]: ...
    @typing.overload
    def load(
        self, data: JsonDict, validate: bool = False, many: typing.Literal[False] = ...
    ) -> D: ...
    @typing.overload
    def load(
        self, data: JsonDict, validate: bool = ..., many: bool = ...
    ) -> typing.Union[D, typing.List[D]]: ...
    def dump_json(
        self,
        obj: typing.Union[D, typing.Iterable[D]],
        validate: bool = ...,
        many: bool = ...,
    ) -> str: ...
    @typing.overload
    def load_json(
        self, js: str, validate: bool = ..., many: typing.Literal[False] = ...
    ) -> D: ...
    @typing.overload
    def load_json(
        self, js: str, validate: bool, many: typing.Literal[True]
    ) -> typing.List[D]: ...
    @typing.overload
    def load_json(
        self, js: str, validate: bool = ..., many: bool = ...
    ) -> typing.Union[typing.List[D], D]: ...
