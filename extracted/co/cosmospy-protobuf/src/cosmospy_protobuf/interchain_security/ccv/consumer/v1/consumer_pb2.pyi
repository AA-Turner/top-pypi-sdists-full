from interchain_security.ccv.v1 import ccv_pb2 as _ccv_pb2
from google.protobuf import any_pb2 as _any_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['enabled', 'blocks_per_distribution_transmission', 'distribution_transmission_channel', 'provider_fee_pool_addr_str', 'ccv_timeout_period', 'transfer_timeout_period', 'consumer_redistribution_fraction', 'historical_entries', 'unbonding_period', 'soft_opt_out_threshold', 'reward_denoms', 'provider_reward_denoms']
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_PER_DISTRIBUTION_TRANSMISSION_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_TRANSMISSION_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FEE_POOL_ADDR_STR_FIELD_NUMBER: _ClassVar[int]
    CCV_TIMEOUT_PERIOD_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_TIMEOUT_PERIOD_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_REDISTRIBUTION_FRACTION_FIELD_NUMBER: _ClassVar[int]
    HISTORICAL_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    UNBONDING_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SOFT_OPT_OUT_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    REWARD_DENOMS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_REWARD_DENOMS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    blocks_per_distribution_transmission: int
    distribution_transmission_channel: str
    provider_fee_pool_addr_str: str
    ccv_timeout_period: _duration_pb2.Duration
    transfer_timeout_period: _duration_pb2.Duration
    consumer_redistribution_fraction: str
    historical_entries: int
    unbonding_period: _duration_pb2.Duration
    soft_opt_out_threshold: str
    reward_denoms: _containers.RepeatedScalarFieldContainer[str]
    provider_reward_denoms: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, enabled: bool=..., blocks_per_distribution_transmission: _Optional[int]=..., distribution_transmission_channel: _Optional[str]=..., provider_fee_pool_addr_str: _Optional[str]=..., ccv_timeout_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., transfer_timeout_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., consumer_redistribution_fraction: _Optional[str]=..., historical_entries: _Optional[int]=..., unbonding_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., soft_opt_out_threshold: _Optional[str]=..., reward_denoms: _Optional[_Iterable[str]]=..., provider_reward_denoms: _Optional[_Iterable[str]]=...) -> None:
        ...

class LastTransmissionBlockHeight(_message.Message):
    __slots__ = ['height']
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int

    def __init__(self, height: _Optional[int]=...) -> None:
        ...

class CrossChainValidator(_message.Message):
    __slots__ = ['address', 'power', 'pubkey']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    power: int
    pubkey: _any_pb2.Any

    def __init__(self, address: _Optional[bytes]=..., power: _Optional[int]=..., pubkey: _Optional[_Union[_any_pb2.Any, _Mapping]]=...) -> None:
        ...

class MaturingVSCPacket(_message.Message):
    __slots__ = ['vscId', 'maturity_time']
    VSCID_FIELD_NUMBER: _ClassVar[int]
    MATURITY_TIME_FIELD_NUMBER: _ClassVar[int]
    vscId: int
    maturity_time: _timestamp_pb2.Timestamp

    def __init__(self, vscId: _Optional[int]=..., maturity_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...