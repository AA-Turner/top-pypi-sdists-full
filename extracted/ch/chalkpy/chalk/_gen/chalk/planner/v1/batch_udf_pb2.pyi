from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatchUDF(_message.Message):
    __slots__ = ("batch_udf_type", "arguments")
    class ArgumentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: BatchUDFArgument
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[BatchUDFArgument, _Mapping]] = ...
        ) -> None: ...

    BATCH_UDF_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    batch_udf_type: str
    arguments: _containers.MessageMap[str, BatchUDFArgument]
    def __init__(
        self, batch_udf_type: _Optional[str] = ..., arguments: _Optional[_Mapping[str, BatchUDFArgument]] = ...
    ) -> None: ...

class BatchUDFArgument(_message.Message):
    __slots__ = ("py_obj",)
    PY_OBJ_FIELD_NUMBER: _ClassVar[int]
    py_obj: PyObject
    def __init__(self, py_obj: _Optional[_Union[PyObject, _Mapping]] = ...) -> None: ...

class PyObject(_message.Message):
    __slots__ = ("py_callable", "py_int", "py_string")
    PY_CALLABLE_FIELD_NUMBER: _ClassVar[int]
    PY_INT_FIELD_NUMBER: _ClassVar[int]
    PY_STRING_FIELD_NUMBER: _ClassVar[int]
    py_callable: PyCallable
    py_int: int
    py_string: str
    def __init__(
        self,
        py_callable: _Optional[_Union[PyCallable, _Mapping]] = ...,
        py_int: _Optional[int] = ...,
        py_string: _Optional[str] = ...,
    ) -> None: ...

class PyCallable(_message.Message):
    __slots__ = ("callable_name", "kwargs")
    class KwargsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PyObject
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PyObject, _Mapping]] = ...) -> None: ...

    CALLABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    callable_name: str
    kwargs: _containers.MessageMap[str, PyObject]
    def __init__(
        self, callable_name: _Optional[str] = ..., kwargs: _Optional[_Mapping[str, PyObject]] = ...
    ) -> None: ...
