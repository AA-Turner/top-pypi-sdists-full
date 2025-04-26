from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.api import annotations_pb2 as _annotations_pb2
from tendermint.p2p import types_pb2 as _types_pb2
from tendermint.types import block_pb2 as _block_pb2
from tendermint.types import types_pb2 as _types_pb2_1
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GetValidatorSetByHeightRequest(_message.Message):
    __slots__ = ['height', 'pagination']
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    height: int
    pagination: _pagination_pb2.PageRequest

    def __init__(self, height: _Optional[int]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class GetValidatorSetByHeightResponse(_message.Message):
    __slots__ = ['block_height', 'validators', 'pagination']
    BLOCK_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    block_height: int
    validators: _containers.RepeatedCompositeFieldContainer[Validator]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, block_height: _Optional[int]=..., validators: _Optional[_Iterable[_Union[Validator, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class GetLatestValidatorSetRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class GetLatestValidatorSetResponse(_message.Message):
    __slots__ = ['block_height', 'validators', 'pagination']
    BLOCK_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    block_height: int
    validators: _containers.RepeatedCompositeFieldContainer[Validator]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, block_height: _Optional[int]=..., validators: _Optional[_Iterable[_Union[Validator, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class Validator(_message.Message):
    __slots__ = ['address', 'pub_key', 'voting_power', 'proposer_priority']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    VOTING_POWER_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    address: str
    pub_key: _any_pb2.Any
    voting_power: int
    proposer_priority: int

    def __init__(self, address: _Optional[str]=..., pub_key: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., voting_power: _Optional[int]=..., proposer_priority: _Optional[int]=...) -> None:
        ...

class GetBlockByHeightRequest(_message.Message):
    __slots__ = ['height']
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int

    def __init__(self, height: _Optional[int]=...) -> None:
        ...

class GetBlockByHeightResponse(_message.Message):
    __slots__ = ['block_id', 'block']
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    block_id: _types_pb2_1.BlockID
    block: _block_pb2.Block

    def __init__(self, block_id: _Optional[_Union[_types_pb2_1.BlockID, _Mapping]]=..., block: _Optional[_Union[_block_pb2.Block, _Mapping]]=...) -> None:
        ...

class GetLatestBlockRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class GetLatestBlockResponse(_message.Message):
    __slots__ = ['block_id', 'block']
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    block_id: _types_pb2_1.BlockID
    block: _block_pb2.Block

    def __init__(self, block_id: _Optional[_Union[_types_pb2_1.BlockID, _Mapping]]=..., block: _Optional[_Union[_block_pb2.Block, _Mapping]]=...) -> None:
        ...

class GetSyncingRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class GetSyncingResponse(_message.Message):
    __slots__ = ['syncing']
    SYNCING_FIELD_NUMBER: _ClassVar[int]
    syncing: bool

    def __init__(self, syncing: bool=...) -> None:
        ...

class GetNodeInfoRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class GetNodeInfoResponse(_message.Message):
    __slots__ = ['default_node_info', 'application_version']
    DEFAULT_NODE_INFO_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_VERSION_FIELD_NUMBER: _ClassVar[int]
    default_node_info: _types_pb2.DefaultNodeInfo
    application_version: VersionInfo

    def __init__(self, default_node_info: _Optional[_Union[_types_pb2.DefaultNodeInfo, _Mapping]]=..., application_version: _Optional[_Union[VersionInfo, _Mapping]]=...) -> None:
        ...

class VersionInfo(_message.Message):
    __slots__ = ['name', 'app_name', 'version', 'git_commit', 'build_tags', 'go_version', 'build_deps', 'cosmos_sdk_version']
    NAME_FIELD_NUMBER: _ClassVar[int]
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    BUILD_TAGS_FIELD_NUMBER: _ClassVar[int]
    GO_VERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_DEPS_FIELD_NUMBER: _ClassVar[int]
    COSMOS_SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    app_name: str
    version: str
    git_commit: str
    build_tags: str
    go_version: str
    build_deps: _containers.RepeatedCompositeFieldContainer[Module]
    cosmos_sdk_version: str

    def __init__(self, name: _Optional[str]=..., app_name: _Optional[str]=..., version: _Optional[str]=..., git_commit: _Optional[str]=..., build_tags: _Optional[str]=..., go_version: _Optional[str]=..., build_deps: _Optional[_Iterable[_Union[Module, _Mapping]]]=..., cosmos_sdk_version: _Optional[str]=...) -> None:
        ...

class Module(_message.Message):
    __slots__ = ['path', 'version', 'sum']
    PATH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SUM_FIELD_NUMBER: _ClassVar[int]
    path: str
    version: str
    sum: str

    def __init__(self, path: _Optional[str]=..., version: _Optional[str]=..., sum: _Optional[str]=...) -> None:
        ...