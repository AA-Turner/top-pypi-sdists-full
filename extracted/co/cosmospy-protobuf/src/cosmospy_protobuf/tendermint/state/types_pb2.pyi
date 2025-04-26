from gogoproto import gogo_pb2 as _gogo_pb2
from tendermint.abci import types_pb2 as _types_pb2
from tendermint.types import types_pb2 as _types_pb2_1
from tendermint.types import validator_pb2 as _validator_pb2
from tendermint.types import params_pb2 as _params_pb2
from tendermint.version import types_pb2 as _types_pb2_1_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ABCIResponses(_message.Message):
    __slots__ = ['deliver_txs', 'end_block', 'begin_block']
    DELIVER_TXS_FIELD_NUMBER: _ClassVar[int]
    END_BLOCK_FIELD_NUMBER: _ClassVar[int]
    BEGIN_BLOCK_FIELD_NUMBER: _ClassVar[int]
    deliver_txs: _containers.RepeatedCompositeFieldContainer[_types_pb2.ResponseDeliverTx]
    end_block: _types_pb2.ResponseEndBlock
    begin_block: _types_pb2.ResponseBeginBlock

    def __init__(self, deliver_txs: _Optional[_Iterable[_Union[_types_pb2.ResponseDeliverTx, _Mapping]]]=..., end_block: _Optional[_Union[_types_pb2.ResponseEndBlock, _Mapping]]=..., begin_block: _Optional[_Union[_types_pb2.ResponseBeginBlock, _Mapping]]=...) -> None:
        ...

class ValidatorsInfo(_message.Message):
    __slots__ = ['validator_set', 'last_height_changed']
    VALIDATOR_SET_FIELD_NUMBER: _ClassVar[int]
    LAST_HEIGHT_CHANGED_FIELD_NUMBER: _ClassVar[int]
    validator_set: _validator_pb2.ValidatorSet
    last_height_changed: int

    def __init__(self, validator_set: _Optional[_Union[_validator_pb2.ValidatorSet, _Mapping]]=..., last_height_changed: _Optional[int]=...) -> None:
        ...

class ConsensusParamsInfo(_message.Message):
    __slots__ = ['consensus_params', 'last_height_changed']
    CONSENSUS_PARAMS_FIELD_NUMBER: _ClassVar[int]
    LAST_HEIGHT_CHANGED_FIELD_NUMBER: _ClassVar[int]
    consensus_params: _params_pb2.ConsensusParams
    last_height_changed: int

    def __init__(self, consensus_params: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]]=..., last_height_changed: _Optional[int]=...) -> None:
        ...

class ABCIResponsesInfo(_message.Message):
    __slots__ = ['abci_responses', 'height']
    ABCI_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    abci_responses: ABCIResponses
    height: int

    def __init__(self, abci_responses: _Optional[_Union[ABCIResponses, _Mapping]]=..., height: _Optional[int]=...) -> None:
        ...

class Version(_message.Message):
    __slots__ = ['consensus', 'software']
    CONSENSUS_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_FIELD_NUMBER: _ClassVar[int]
    consensus: _types_pb2_1_1.Consensus
    software: str

    def __init__(self, consensus: _Optional[_Union[_types_pb2_1_1.Consensus, _Mapping]]=..., software: _Optional[str]=...) -> None:
        ...

class State(_message.Message):
    __slots__ = ['version', 'chain_id', 'initial_height', 'last_block_height', 'last_block_id', 'last_block_time', 'next_validators', 'validators', 'last_validators', 'last_height_validators_changed', 'consensus_params', 'last_height_consensus_params_changed', 'last_results_hash', 'app_hash']
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    INITIAL_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    LAST_BLOCK_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    LAST_BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_BLOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    NEXT_VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    LAST_VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    LAST_HEIGHT_VALIDATORS_CHANGED_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_PARAMS_FIELD_NUMBER: _ClassVar[int]
    LAST_HEIGHT_CONSENSUS_PARAMS_CHANGED_FIELD_NUMBER: _ClassVar[int]
    LAST_RESULTS_HASH_FIELD_NUMBER: _ClassVar[int]
    APP_HASH_FIELD_NUMBER: _ClassVar[int]
    version: Version
    chain_id: str
    initial_height: int
    last_block_height: int
    last_block_id: _types_pb2_1.BlockID
    last_block_time: _timestamp_pb2.Timestamp
    next_validators: _validator_pb2.ValidatorSet
    validators: _validator_pb2.ValidatorSet
    last_validators: _validator_pb2.ValidatorSet
    last_height_validators_changed: int
    consensus_params: _params_pb2.ConsensusParams
    last_height_consensus_params_changed: int
    last_results_hash: bytes
    app_hash: bytes

    def __init__(self, version: _Optional[_Union[Version, _Mapping]]=..., chain_id: _Optional[str]=..., initial_height: _Optional[int]=..., last_block_height: _Optional[int]=..., last_block_id: _Optional[_Union[_types_pb2_1.BlockID, _Mapping]]=..., last_block_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., next_validators: _Optional[_Union[_validator_pb2.ValidatorSet, _Mapping]]=..., validators: _Optional[_Union[_validator_pb2.ValidatorSet, _Mapping]]=..., last_validators: _Optional[_Union[_validator_pb2.ValidatorSet, _Mapping]]=..., last_height_validators_changed: _Optional[int]=..., consensus_params: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]]=..., last_height_consensus_params_changed: _Optional[int]=..., last_results_hash: _Optional[bytes]=..., app_hash: _Optional[bytes]=...) -> None:
        ...