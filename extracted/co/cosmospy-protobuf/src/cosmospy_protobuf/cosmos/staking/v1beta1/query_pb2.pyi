from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.staking.v1beta1 import staking_pb2 as _staking_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryValidatorsRequest(_message.Message):
    __slots__ = ['status', 'pagination']
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    status: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, status: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryValidatorsResponse(_message.Message):
    __slots__ = ['validators', 'pagination']
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    validators: _containers.RepeatedCompositeFieldContainer[_staking_pb2.Validator]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, validators: _Optional[_Iterable[_Union[_staking_pb2.Validator, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryValidatorRequest(_message.Message):
    __slots__ = ['validator_addr']
    VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    validator_addr: str

    def __init__(self, validator_addr: _Optional[str]=...) -> None:
        ...

class QueryValidatorResponse(_message.Message):
    __slots__ = ['validator']
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    validator: _staking_pb2.Validator

    def __init__(self, validator: _Optional[_Union[_staking_pb2.Validator, _Mapping]]=...) -> None:
        ...

class QueryValidatorDelegationsRequest(_message.Message):
    __slots__ = ['validator_addr', 'pagination']
    VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    validator_addr: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, validator_addr: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryValidatorDelegationsResponse(_message.Message):
    __slots__ = ['delegation_responses', 'pagination']
    DELEGATION_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    delegation_responses: _containers.RepeatedCompositeFieldContainer[_staking_pb2.DelegationResponse]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, delegation_responses: _Optional[_Iterable[_Union[_staking_pb2.DelegationResponse, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryValidatorUnbondingDelegationsRequest(_message.Message):
    __slots__ = ['validator_addr', 'pagination']
    VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    validator_addr: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, validator_addr: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryValidatorUnbondingDelegationsResponse(_message.Message):
    __slots__ = ['unbonding_responses', 'pagination']
    UNBONDING_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    unbonding_responses: _containers.RepeatedCompositeFieldContainer[_staking_pb2.UnbondingDelegation]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, unbonding_responses: _Optional[_Iterable[_Union[_staking_pb2.UnbondingDelegation, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryDelegationRequest(_message.Message):
    __slots__ = ['delegator_addr', 'validator_addr']
    DELEGATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    delegator_addr: str
    validator_addr: str

    def __init__(self, delegator_addr: _Optional[str]=..., validator_addr: _Optional[str]=...) -> None:
        ...

class QueryDelegationResponse(_message.Message):
    __slots__ = ['delegation_response']
    DELEGATION_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    delegation_response: _staking_pb2.DelegationResponse

    def __init__(self, delegation_response: _Optional[_Union[_staking_pb2.DelegationResponse, _Mapping]]=...) -> None:
        ...

class QueryUnbondingDelegationRequest(_message.Message):
    __slots__ = ['delegator_addr', 'validator_addr']
    DELEGATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    delegator_addr: str
    validator_addr: str

    def __init__(self, delegator_addr: _Optional[str]=..., validator_addr: _Optional[str]=...) -> None:
        ...

class QueryUnbondingDelegationResponse(_message.Message):
    __slots__ = ['unbond']
    UNBOND_FIELD_NUMBER: _ClassVar[int]
    unbond: _staking_pb2.UnbondingDelegation

    def __init__(self, unbond: _Optional[_Union[_staking_pb2.UnbondingDelegation, _Mapping]]=...) -> None:
        ...

class QueryDelegatorDelegationsRequest(_message.Message):
    __slots__ = ['delegator_addr', 'pagination']
    DELEGATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    delegator_addr: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, delegator_addr: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryDelegatorDelegationsResponse(_message.Message):
    __slots__ = ['delegation_responses', 'pagination']
    DELEGATION_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    delegation_responses: _containers.RepeatedCompositeFieldContainer[_staking_pb2.DelegationResponse]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, delegation_responses: _Optional[_Iterable[_Union[_staking_pb2.DelegationResponse, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryDelegatorUnbondingDelegationsRequest(_message.Message):
    __slots__ = ['delegator_addr', 'pagination']
    DELEGATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    delegator_addr: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, delegator_addr: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryDelegatorUnbondingDelegationsResponse(_message.Message):
    __slots__ = ['unbonding_responses', 'pagination']
    UNBONDING_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    unbonding_responses: _containers.RepeatedCompositeFieldContainer[_staking_pb2.UnbondingDelegation]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, unbonding_responses: _Optional[_Iterable[_Union[_staking_pb2.UnbondingDelegation, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryRedelegationsRequest(_message.Message):
    __slots__ = ['delegator_addr', 'src_validator_addr', 'dst_validator_addr', 'pagination']
    DELEGATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    SRC_VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    DST_VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    delegator_addr: str
    src_validator_addr: str
    dst_validator_addr: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, delegator_addr: _Optional[str]=..., src_validator_addr: _Optional[str]=..., dst_validator_addr: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryRedelegationsResponse(_message.Message):
    __slots__ = ['redelegation_responses', 'pagination']
    REDELEGATION_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    redelegation_responses: _containers.RepeatedCompositeFieldContainer[_staking_pb2.RedelegationResponse]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, redelegation_responses: _Optional[_Iterable[_Union[_staking_pb2.RedelegationResponse, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryDelegatorValidatorsRequest(_message.Message):
    __slots__ = ['delegator_addr', 'pagination']
    DELEGATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    delegator_addr: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, delegator_addr: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryDelegatorValidatorsResponse(_message.Message):
    __slots__ = ['validators', 'pagination']
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    validators: _containers.RepeatedCompositeFieldContainer[_staking_pb2.Validator]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, validators: _Optional[_Iterable[_Union[_staking_pb2.Validator, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryDelegatorValidatorRequest(_message.Message):
    __slots__ = ['delegator_addr', 'validator_addr']
    DELEGATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDR_FIELD_NUMBER: _ClassVar[int]
    delegator_addr: str
    validator_addr: str

    def __init__(self, delegator_addr: _Optional[str]=..., validator_addr: _Optional[str]=...) -> None:
        ...

class QueryDelegatorValidatorResponse(_message.Message):
    __slots__ = ['validator']
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    validator: _staking_pb2.Validator

    def __init__(self, validator: _Optional[_Union[_staking_pb2.Validator, _Mapping]]=...) -> None:
        ...

class QueryHistoricalInfoRequest(_message.Message):
    __slots__ = ['height']
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int

    def __init__(self, height: _Optional[int]=...) -> None:
        ...

class QueryHistoricalInfoResponse(_message.Message):
    __slots__ = ['hist']
    HIST_FIELD_NUMBER: _ClassVar[int]
    hist: _staking_pb2.HistoricalInfo

    def __init__(self, hist: _Optional[_Union[_staking_pb2.HistoricalInfo, _Mapping]]=...) -> None:
        ...

class QueryPoolRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryPoolResponse(_message.Message):
    __slots__ = ['pool']
    POOL_FIELD_NUMBER: _ClassVar[int]
    pool: _staking_pb2.Pool

    def __init__(self, pool: _Optional[_Union[_staking_pb2.Pool, _Mapping]]=...) -> None:
        ...

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _staking_pb2.Params

    def __init__(self, params: _Optional[_Union[_staking_pb2.Params, _Mapping]]=...) -> None:
        ...

class QueryTokenizeShareRecordByIdRequest(_message.Message):
    __slots__ = ['id']
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int

    def __init__(self, id: _Optional[int]=...) -> None:
        ...

class QueryTokenizeShareRecordByIdResponse(_message.Message):
    __slots__ = ['record']
    RECORD_FIELD_NUMBER: _ClassVar[int]
    record: _staking_pb2.TokenizeShareRecord

    def __init__(self, record: _Optional[_Union[_staking_pb2.TokenizeShareRecord, _Mapping]]=...) -> None:
        ...

class QueryTokenizeShareRecordByDenomRequest(_message.Message):
    __slots__ = ['denom']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str

    def __init__(self, denom: _Optional[str]=...) -> None:
        ...

class QueryTokenizeShareRecordByDenomResponse(_message.Message):
    __slots__ = ['record']
    RECORD_FIELD_NUMBER: _ClassVar[int]
    record: _staking_pb2.TokenizeShareRecord

    def __init__(self, record: _Optional[_Union[_staking_pb2.TokenizeShareRecord, _Mapping]]=...) -> None:
        ...

class QueryTokenizeShareRecordsOwnedRequest(_message.Message):
    __slots__ = ['owner']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    owner: str

    def __init__(self, owner: _Optional[str]=...) -> None:
        ...

class QueryTokenizeShareRecordsOwnedResponse(_message.Message):
    __slots__ = ['records']
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[_staking_pb2.TokenizeShareRecord]

    def __init__(self, records: _Optional[_Iterable[_Union[_staking_pb2.TokenizeShareRecord, _Mapping]]]=...) -> None:
        ...

class QueryAllTokenizeShareRecordsRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class QueryAllTokenizeShareRecordsResponse(_message.Message):
    __slots__ = ['records', 'pagination']
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[_staking_pb2.TokenizeShareRecord]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, records: _Optional[_Iterable[_Union[_staking_pb2.TokenizeShareRecord, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class QueryLastTokenizeShareRecordIdRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryLastTokenizeShareRecordIdResponse(_message.Message):
    __slots__ = ['id']
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int

    def __init__(self, id: _Optional[int]=...) -> None:
        ...

class QueryTotalTokenizeSharedAssetsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryTotalTokenizeSharedAssetsResponse(_message.Message):
    __slots__ = ['value']
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _coin_pb2.Coin

    def __init__(self, value: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class QueryTotalLiquidStaked(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryTotalLiquidStakedResponse(_message.Message):
    __slots__ = ['tokens']
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: str

    def __init__(self, tokens: _Optional[str]=...) -> None:
        ...

class QueryTokenizeShareLockInfo(_message.Message):
    __slots__ = ['address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str

    def __init__(self, address: _Optional[str]=...) -> None:
        ...

class QueryTokenizeShareLockInfoResponse(_message.Message):
    __slots__ = ['status', 'expiration_time']
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    status: str
    expiration_time: str

    def __init__(self, status: _Optional[str]=..., expiration_time: _Optional[str]=...) -> None:
        ...