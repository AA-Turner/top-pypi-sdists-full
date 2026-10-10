from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Image(_message.Message):
    __slots__ = ("content", "path")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    path: str
    def __init__(self, content: _Optional[bytes] = ..., path: _Optional[str] = ...) -> None: ...

class RepresentRequest(_message.Message):
    __slots__ = ("img", "model_name", "detector_backend", "enforce_detection", "align", "anti_spoofing", "max_faces")
    IMG_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DETECTOR_BACKEND_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_DETECTION_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    ANTI_SPOOFING_FIELD_NUMBER: _ClassVar[int]
    MAX_FACES_FIELD_NUMBER: _ClassVar[int]
    img: Image
    model_name: str
    detector_backend: str
    enforce_detection: bool
    align: bool
    anti_spoofing: bool
    max_faces: int
    def __init__(self, img: _Optional[_Union[Image, _Mapping]] = ..., model_name: _Optional[str] = ..., detector_backend: _Optional[str] = ..., enforce_detection: bool = ..., align: bool = ..., anti_spoofing: bool = ..., max_faces: _Optional[int] = ...) -> None: ...

class VerifyRequest(_message.Message):
    __slots__ = ("img1", "img2", "model_name", "detector_backend", "distance_metric", "enforce_detection", "align", "anti_spoofing")
    IMG1_FIELD_NUMBER: _ClassVar[int]
    IMG2_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DETECTOR_BACKEND_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_METRIC_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_DETECTION_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    ANTI_SPOOFING_FIELD_NUMBER: _ClassVar[int]
    img1: Image
    img2: Image
    model_name: str
    detector_backend: str
    distance_metric: str
    enforce_detection: bool
    align: bool
    anti_spoofing: bool
    def __init__(self, img1: _Optional[_Union[Image, _Mapping]] = ..., img2: _Optional[_Union[Image, _Mapping]] = ..., model_name: _Optional[str] = ..., detector_backend: _Optional[str] = ..., distance_metric: _Optional[str] = ..., enforce_detection: bool = ..., align: bool = ..., anti_spoofing: bool = ...) -> None: ...

class AnalyzeRequest(_message.Message):
    __slots__ = ("img", "actions", "detector_backend", "enforce_detection", "align", "anti_spoofing")
    IMG_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    DETECTOR_BACKEND_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_DETECTION_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    ANTI_SPOOFING_FIELD_NUMBER: _ClassVar[int]
    img: Image
    actions: _containers.RepeatedScalarFieldContainer[str]
    detector_backend: str
    enforce_detection: bool
    align: bool
    anti_spoofing: bool
    def __init__(self, img: _Optional[_Union[Image, _Mapping]] = ..., actions: _Optional[_Iterable[str]] = ..., detector_backend: _Optional[str] = ..., enforce_detection: bool = ..., align: bool = ..., anti_spoofing: bool = ...) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ("img", "img_name", "model_name", "detector_backend", "enforce_detection", "align", "l2_normalize", "expand_percentage", "normalization", "anti_spoofing")
    IMG_FIELD_NUMBER: _ClassVar[int]
    IMG_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DETECTOR_BACKEND_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_DETECTION_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    L2_NORMALIZE_FIELD_NUMBER: _ClassVar[int]
    EXPAND_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    NORMALIZATION_FIELD_NUMBER: _ClassVar[int]
    ANTI_SPOOFING_FIELD_NUMBER: _ClassVar[int]
    img: Image
    img_name: str
    model_name: str
    detector_backend: str
    enforce_detection: bool
    align: bool
    l2_normalize: bool
    expand_percentage: int
    normalization: str
    anti_spoofing: bool
    def __init__(self, img: _Optional[_Union[Image, _Mapping]] = ..., img_name: _Optional[str] = ..., model_name: _Optional[str] = ..., detector_backend: _Optional[str] = ..., enforce_detection: bool = ..., align: bool = ..., l2_normalize: bool = ..., expand_percentage: _Optional[int] = ..., normalization: _Optional[str] = ..., anti_spoofing: bool = ...) -> None: ...

class SearchRequest(_message.Message):
    __slots__ = ("img", "model_name", "detector_backend", "enforce_detection", "align", "distance_metric", "l2_normalize", "search_method", "expand_percentage", "normalization", "anti_spoofing", "similarity_search", "k")
    IMG_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DETECTOR_BACKEND_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_DETECTION_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_METRIC_FIELD_NUMBER: _ClassVar[int]
    L2_NORMALIZE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_METHOD_FIELD_NUMBER: _ClassVar[int]
    EXPAND_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    NORMALIZATION_FIELD_NUMBER: _ClassVar[int]
    ANTI_SPOOFING_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_SEARCH_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    img: Image
    model_name: str
    detector_backend: str
    enforce_detection: bool
    align: bool
    distance_metric: str
    l2_normalize: bool
    search_method: str
    expand_percentage: int
    normalization: str
    anti_spoofing: bool
    similarity_search: bool
    k: int
    def __init__(self, img: _Optional[_Union[Image, _Mapping]] = ..., model_name: _Optional[str] = ..., detector_backend: _Optional[str] = ..., enforce_detection: bool = ..., align: bool = ..., distance_metric: _Optional[str] = ..., l2_normalize: bool = ..., search_method: _Optional[str] = ..., expand_percentage: _Optional[int] = ..., normalization: _Optional[str] = ..., anti_spoofing: bool = ..., similarity_search: bool = ..., k: _Optional[int] = ...) -> None: ...

class BuildIndexRequest(_message.Message):
    __slots__ = ("model_name", "detector_backend", "align", "l2_normalize")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DETECTOR_BACKEND_FIELD_NUMBER: _ClassVar[int]
    ALIGN_FIELD_NUMBER: _ClassVar[int]
    L2_NORMALIZE_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    detector_backend: str
    align: bool
    l2_normalize: bool
    def __init__(self, model_name: _Optional[str] = ..., detector_backend: _Optional[str] = ..., align: bool = ..., l2_normalize: bool = ...) -> None: ...

class DeepFaceResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _struct_pb2.Struct
    def __init__(self, result: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
