from google.api import annotations_pb2 as _annotations_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from interchain_security.ccv.v1 import ccv_pb2 as _ccv_pb2
from interchain_security.ccv.consumer.v1 import genesis_pb2 as _genesis_pb2
from interchain_security.ccv.provider.v1 import provider_pb2 as _provider_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryConsumerGenesisRequest(_message.Message):
    __slots__ = ['chain_id']
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    chain_id: str

    def __init__(self, chain_id: _Optional[str]=...) -> None:
        ...

class QueryConsumerGenesisResponse(_message.Message):
    __slots__ = ['genesis_state']
    GENESIS_STATE_FIELD_NUMBER: _ClassVar[int]
    genesis_state: _genesis_pb2.GenesisState

    def __init__(self, genesis_state: _Optional[_Union[_genesis_pb2.GenesisState, _Mapping]]=...) -> None:
        ...

class QueryConsumerChainsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryConsumerChainsResponse(_message.Message):
    __slots__ = ['chains']
    CHAINS_FIELD_NUMBER: _ClassVar[int]
    chains: _containers.RepeatedCompositeFieldContainer[Chain]

    def __init__(self, chains: _Optional[_Iterable[_Union[Chain, _Mapping]]]=...) -> None:
        ...

class QueryConsumerChainStartProposalsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryConsumerChainStartProposalsResponse(_message.Message):
    __slots__ = ['proposals']
    PROPOSALS_FIELD_NUMBER: _ClassVar[int]
    proposals: _provider_pb2.ConsumerAdditionProposals

    def __init__(self, proposals: _Optional[_Union[_provider_pb2.ConsumerAdditionProposals, _Mapping]]=...) -> None:
        ...

class QueryConsumerChainStopProposalsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryConsumerChainStopProposalsResponse(_message.Message):
    __slots__ = ['proposals']
    PROPOSALS_FIELD_NUMBER: _ClassVar[int]
    proposals: _provider_pb2.ConsumerRemovalProposals

    def __init__(self, proposals: _Optional[_Union[_provider_pb2.ConsumerRemovalProposals, _Mapping]]=...) -> None:
        ...

class Chain(_message.Message):
    __slots__ = ['chain_id', 'client_id']
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    client_id: str

    def __init__(self, chain_id: _Optional[str]=..., client_id: _Optional[str]=...) -> None:
        ...

class QueryValidatorConsumerAddrRequest(_message.Message):
    __slots__ = ['chain_id', 'provider_address']
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    provider_address: str

    def __init__(self, chain_id: _Optional[str]=..., provider_address: _Optional[str]=...) -> None:
        ...

class QueryValidatorConsumerAddrResponse(_message.Message):
    __slots__ = ['consumer_address']
    CONSUMER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    consumer_address: str

    def __init__(self, consumer_address: _Optional[str]=...) -> None:
        ...

class QueryValidatorProviderAddrRequest(_message.Message):
    __slots__ = ['chain_id', 'consumer_address']
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    consumer_address: str

    def __init__(self, chain_id: _Optional[str]=..., consumer_address: _Optional[str]=...) -> None:
        ...

class QueryValidatorProviderAddrResponse(_message.Message):
    __slots__ = ['provider_address']
    PROVIDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    provider_address: str

    def __init__(self, provider_address: _Optional[str]=...) -> None:
        ...

class QueryThrottleStateRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryThrottleStateResponse(_message.Message):
    __slots__ = ['slash_meter', 'slash_meter_allowance', 'next_replenish_candidate', 'packets']
    SLASH_METER_FIELD_NUMBER: _ClassVar[int]
    SLASH_METER_ALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    NEXT_REPLENISH_CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    PACKETS_FIELD_NUMBER: _ClassVar[int]
    slash_meter: int
    slash_meter_allowance: int
    next_replenish_candidate: _timestamp_pb2.Timestamp
    packets: _containers.RepeatedCompositeFieldContainer[ThrottledSlashPacket]

    def __init__(self, slash_meter: _Optional[int]=..., slash_meter_allowance: _Optional[int]=..., next_replenish_candidate: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., packets: _Optional[_Iterable[_Union[ThrottledSlashPacket, _Mapping]]]=...) -> None:
        ...

class QueryThrottledConsumerPacketDataRequest(_message.Message):
    __slots__ = ['chain_id']
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    chain_id: str

    def __init__(self, chain_id: _Optional[str]=...) -> None:
        ...

class QueryThrottledConsumerPacketDataResponse(_message.Message):
    __slots__ = ['chain_id', 'size', 'packetDataInstances']
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    PACKETDATAINSTANCES_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    size: int
    packetDataInstances: _containers.RepeatedCompositeFieldContainer[ThrottledPacketDataWrapper]

    def __init__(self, chain_id: _Optional[str]=..., size: _Optional[int]=..., packetDataInstances: _Optional[_Iterable[_Union[ThrottledPacketDataWrapper, _Mapping]]]=...) -> None:
        ...

class ThrottledSlashPacket(_message.Message):
    __slots__ = ['global_entry', 'data']
    GLOBAL_ENTRY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    global_entry: _provider_pb2.GlobalSlashEntry
    data: _ccv_pb2.SlashPacketData

    def __init__(self, global_entry: _Optional[_Union[_provider_pb2.GlobalSlashEntry, _Mapping]]=..., data: _Optional[_Union[_ccv_pb2.SlashPacketData, _Mapping]]=...) -> None:
        ...

class ThrottledPacketDataWrapper(_message.Message):
    __slots__ = ['slash_packet', 'vsc_matured_packet']
    SLASH_PACKET_FIELD_NUMBER: _ClassVar[int]
    VSC_MATURED_PACKET_FIELD_NUMBER: _ClassVar[int]
    slash_packet: _ccv_pb2.SlashPacketData
    vsc_matured_packet: _ccv_pb2.VSCMaturedPacketData

    def __init__(self, slash_packet: _Optional[_Union[_ccv_pb2.SlashPacketData, _Mapping]]=..., vsc_matured_packet: _Optional[_Union[_ccv_pb2.VSCMaturedPacketData, _Mapping]]=...) -> None:
        ...

class QueryRegisteredConsumerRewardDenomsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryRegisteredConsumerRewardDenomsResponse(_message.Message):
    __slots__ = ['denoms']
    DENOMS_FIELD_NUMBER: _ClassVar[int]
    denoms: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, denoms: _Optional[_Iterable[str]]=...) -> None:
        ...