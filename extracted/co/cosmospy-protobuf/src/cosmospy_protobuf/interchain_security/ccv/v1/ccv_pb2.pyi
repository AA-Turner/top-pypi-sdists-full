from cosmos.staking.v1beta1 import staking_pb2 as _staking_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from tendermint.abci import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ConsumerPacketDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CONSUMER_PACKET_TYPE_UNSPECIFIED: _ClassVar[ConsumerPacketDataType]
    CONSUMER_PACKET_TYPE_SLASH: _ClassVar[ConsumerPacketDataType]
    CONSUMER_PACKET_TYPE_VSCM: _ClassVar[ConsumerPacketDataType]
CONSUMER_PACKET_TYPE_UNSPECIFIED: ConsumerPacketDataType
CONSUMER_PACKET_TYPE_SLASH: ConsumerPacketDataType
CONSUMER_PACKET_TYPE_VSCM: ConsumerPacketDataType

class ValidatorSetChangePacketData(_message.Message):
    __slots__ = ['validator_updates', 'valset_update_id', 'slash_acks']
    VALIDATOR_UPDATES_FIELD_NUMBER: _ClassVar[int]
    VALSET_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    SLASH_ACKS_FIELD_NUMBER: _ClassVar[int]
    validator_updates: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    valset_update_id: int
    slash_acks: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, validator_updates: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]]=..., valset_update_id: _Optional[int]=..., slash_acks: _Optional[_Iterable[str]]=...) -> None:
        ...

class ValidatorSetChangePackets(_message.Message):
    __slots__ = ['list']
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedCompositeFieldContainer[ValidatorSetChangePacketData]

    def __init__(self, list: _Optional[_Iterable[_Union[ValidatorSetChangePacketData, _Mapping]]]=...) -> None:
        ...

class VSCMaturedPacketData(_message.Message):
    __slots__ = ['valset_update_id']
    VALSET_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    valset_update_id: int

    def __init__(self, valset_update_id: _Optional[int]=...) -> None:
        ...

class SlashPacketData(_message.Message):
    __slots__ = ['validator', 'valset_update_id', 'infraction']
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    VALSET_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    INFRACTION_FIELD_NUMBER: _ClassVar[int]
    validator: _types_pb2.Validator
    valset_update_id: int
    infraction: _staking_pb2.InfractionType

    def __init__(self, validator: _Optional[_Union[_types_pb2.Validator, _Mapping]]=..., valset_update_id: _Optional[int]=..., infraction: _Optional[_Union[_staking_pb2.InfractionType, str]]=...) -> None:
        ...

class MaturedUnbondingOps(_message.Message):
    __slots__ = ['ids']
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, ids: _Optional[_Iterable[int]]=...) -> None:
        ...

class ConsumerPacketData(_message.Message):
    __slots__ = ['type', 'slashPacketData', 'vscMaturedPacketData']
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SLASHPACKETDATA_FIELD_NUMBER: _ClassVar[int]
    VSCMATUREDPACKETDATA_FIELD_NUMBER: _ClassVar[int]
    type: ConsumerPacketDataType
    slashPacketData: SlashPacketData
    vscMaturedPacketData: VSCMaturedPacketData

    def __init__(self, type: _Optional[_Union[ConsumerPacketDataType, str]]=..., slashPacketData: _Optional[_Union[SlashPacketData, _Mapping]]=..., vscMaturedPacketData: _Optional[_Union[VSCMaturedPacketData, _Mapping]]=...) -> None:
        ...

class ConsumerPacketDataList(_message.Message):
    __slots__ = ['list']
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedCompositeFieldContainer[ConsumerPacketData]

    def __init__(self, list: _Optional[_Iterable[_Union[ConsumerPacketData, _Mapping]]]=...) -> None:
        ...