from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.staking.v1beta1 import staking_pb2 as _staking_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params', 'last_total_power', 'last_validator_powers', 'validators', 'delegations', 'unbonding_delegations', 'redelegations', 'exported', 'tokenize_share_records', 'last_tokenize_share_record_id', 'total_liquid_staked_tokens', 'tokenize_share_locks']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    LAST_TOTAL_POWER_FIELD_NUMBER: _ClassVar[int]
    LAST_VALIDATOR_POWERS_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    DELEGATIONS_FIELD_NUMBER: _ClassVar[int]
    UNBONDING_DELEGATIONS_FIELD_NUMBER: _ClassVar[int]
    REDELEGATIONS_FIELD_NUMBER: _ClassVar[int]
    EXPORTED_FIELD_NUMBER: _ClassVar[int]
    TOKENIZE_SHARE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    LAST_TOKENIZE_SHARE_RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_LIQUID_STAKED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOKENIZE_SHARE_LOCKS_FIELD_NUMBER: _ClassVar[int]
    params: _staking_pb2.Params
    last_total_power: bytes
    last_validator_powers: _containers.RepeatedCompositeFieldContainer[LastValidatorPower]
    validators: _containers.RepeatedCompositeFieldContainer[_staking_pb2.Validator]
    delegations: _containers.RepeatedCompositeFieldContainer[_staking_pb2.Delegation]
    unbonding_delegations: _containers.RepeatedCompositeFieldContainer[_staking_pb2.UnbondingDelegation]
    redelegations: _containers.RepeatedCompositeFieldContainer[_staking_pb2.Redelegation]
    exported: bool
    tokenize_share_records: _containers.RepeatedCompositeFieldContainer[_staking_pb2.TokenizeShareRecord]
    last_tokenize_share_record_id: int
    total_liquid_staked_tokens: bytes
    tokenize_share_locks: _containers.RepeatedCompositeFieldContainer[TokenizeShareLock]

    def __init__(self, params: _Optional[_Union[_staking_pb2.Params, _Mapping]]=..., last_total_power: _Optional[bytes]=..., last_validator_powers: _Optional[_Iterable[_Union[LastValidatorPower, _Mapping]]]=..., validators: _Optional[_Iterable[_Union[_staking_pb2.Validator, _Mapping]]]=..., delegations: _Optional[_Iterable[_Union[_staking_pb2.Delegation, _Mapping]]]=..., unbonding_delegations: _Optional[_Iterable[_Union[_staking_pb2.UnbondingDelegation, _Mapping]]]=..., redelegations: _Optional[_Iterable[_Union[_staking_pb2.Redelegation, _Mapping]]]=..., exported: bool=..., tokenize_share_records: _Optional[_Iterable[_Union[_staking_pb2.TokenizeShareRecord, _Mapping]]]=..., last_tokenize_share_record_id: _Optional[int]=..., total_liquid_staked_tokens: _Optional[bytes]=..., tokenize_share_locks: _Optional[_Iterable[_Union[TokenizeShareLock, _Mapping]]]=...) -> None:
        ...

class TokenizeShareLock(_message.Message):
    __slots__ = ['address', 'status', 'completion_time']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TIME_FIELD_NUMBER: _ClassVar[int]
    address: str
    status: str
    completion_time: _timestamp_pb2.Timestamp

    def __init__(self, address: _Optional[str]=..., status: _Optional[str]=..., completion_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class LastValidatorPower(_message.Message):
    __slots__ = ['address', 'power']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    address: str
    power: int

    def __init__(self, address: _Optional[str]=..., power: _Optional[int]=...) -> None:
        ...