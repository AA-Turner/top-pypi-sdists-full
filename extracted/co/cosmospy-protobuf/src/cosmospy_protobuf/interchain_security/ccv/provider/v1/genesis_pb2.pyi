from gogoproto import gogo_pb2 as _gogo_pb2
from interchain_security.ccv.v1 import ccv_pb2 as _ccv_pb2
from interchain_security.ccv.provider.v1 import provider_pb2 as _provider_pb2
from interchain_security.ccv.consumer.v1 import consumer_pb2 as _consumer_pb2
from interchain_security.ccv.consumer.v1 import genesis_pb2 as _genesis_pb2
from tendermint.crypto import keys_pb2 as _keys_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['valset_update_id', 'consumer_states', 'unbonding_ops', 'mature_unbonding_ops', 'valset_update_id_to_height', 'consumer_addition_proposals', 'consumer_removal_proposals', 'params', 'validator_consumer_pubkeys', 'validators_by_consumer_addr', 'consumer_addrs_to_prune']
    VALSET_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_STATES_FIELD_NUMBER: _ClassVar[int]
    UNBONDING_OPS_FIELD_NUMBER: _ClassVar[int]
    MATURE_UNBONDING_OPS_FIELD_NUMBER: _ClassVar[int]
    VALSET_UPDATE_ID_TO_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ADDITION_PROPOSALS_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_REMOVAL_PROPOSALS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_CONSUMER_PUBKEYS_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_BY_CONSUMER_ADDR_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ADDRS_TO_PRUNE_FIELD_NUMBER: _ClassVar[int]
    valset_update_id: int
    consumer_states: _containers.RepeatedCompositeFieldContainer[ConsumerState]
    unbonding_ops: _containers.RepeatedCompositeFieldContainer[_provider_pb2.UnbondingOp]
    mature_unbonding_ops: _ccv_pb2.MaturedUnbondingOps
    valset_update_id_to_height: _containers.RepeatedCompositeFieldContainer[ValsetUpdateIdToHeight]
    consumer_addition_proposals: _containers.RepeatedCompositeFieldContainer[_provider_pb2.ConsumerAdditionProposal]
    consumer_removal_proposals: _containers.RepeatedCompositeFieldContainer[_provider_pb2.ConsumerRemovalProposal]
    params: _provider_pb2.Params
    validator_consumer_pubkeys: _containers.RepeatedCompositeFieldContainer[_provider_pb2.ValidatorConsumerPubKey]
    validators_by_consumer_addr: _containers.RepeatedCompositeFieldContainer[_provider_pb2.ValidatorByConsumerAddr]
    consumer_addrs_to_prune: _containers.RepeatedCompositeFieldContainer[_provider_pb2.ConsumerAddrsToPrune]

    def __init__(self, valset_update_id: _Optional[int]=..., consumer_states: _Optional[_Iterable[_Union[ConsumerState, _Mapping]]]=..., unbonding_ops: _Optional[_Iterable[_Union[_provider_pb2.UnbondingOp, _Mapping]]]=..., mature_unbonding_ops: _Optional[_Union[_ccv_pb2.MaturedUnbondingOps, _Mapping]]=..., valset_update_id_to_height: _Optional[_Iterable[_Union[ValsetUpdateIdToHeight, _Mapping]]]=..., consumer_addition_proposals: _Optional[_Iterable[_Union[_provider_pb2.ConsumerAdditionProposal, _Mapping]]]=..., consumer_removal_proposals: _Optional[_Iterable[_Union[_provider_pb2.ConsumerRemovalProposal, _Mapping]]]=..., params: _Optional[_Union[_provider_pb2.Params, _Mapping]]=..., validator_consumer_pubkeys: _Optional[_Iterable[_Union[_provider_pb2.ValidatorConsumerPubKey, _Mapping]]]=..., validators_by_consumer_addr: _Optional[_Iterable[_Union[_provider_pb2.ValidatorByConsumerAddr, _Mapping]]]=..., consumer_addrs_to_prune: _Optional[_Iterable[_Union[_provider_pb2.ConsumerAddrsToPrune, _Mapping]]]=...) -> None:
        ...

class ConsumerState(_message.Message):
    __slots__ = ['chain_id', 'channel_id', 'client_id', 'initial_height', 'consumer_genesis', 'pending_valset_changes', 'slash_downtime_ack', 'unbonding_ops_index']
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    INITIAL_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_GENESIS_FIELD_NUMBER: _ClassVar[int]
    PENDING_VALSET_CHANGES_FIELD_NUMBER: _ClassVar[int]
    SLASH_DOWNTIME_ACK_FIELD_NUMBER: _ClassVar[int]
    UNBONDING_OPS_INDEX_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    channel_id: str
    client_id: str
    initial_height: int
    consumer_genesis: _genesis_pb2.GenesisState
    pending_valset_changes: _containers.RepeatedCompositeFieldContainer[_ccv_pb2.ValidatorSetChangePacketData]
    slash_downtime_ack: _containers.RepeatedScalarFieldContainer[str]
    unbonding_ops_index: _containers.RepeatedCompositeFieldContainer[_provider_pb2.VscUnbondingOps]

    def __init__(self, chain_id: _Optional[str]=..., channel_id: _Optional[str]=..., client_id: _Optional[str]=..., initial_height: _Optional[int]=..., consumer_genesis: _Optional[_Union[_genesis_pb2.GenesisState, _Mapping]]=..., pending_valset_changes: _Optional[_Iterable[_Union[_ccv_pb2.ValidatorSetChangePacketData, _Mapping]]]=..., slash_downtime_ack: _Optional[_Iterable[str]]=..., unbonding_ops_index: _Optional[_Iterable[_Union[_provider_pb2.VscUnbondingOps, _Mapping]]]=...) -> None:
        ...

class ValsetUpdateIdToHeight(_message.Message):
    __slots__ = ['valset_update_id', 'height']
    VALSET_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    valset_update_id: int
    height: int

    def __init__(self, valset_update_id: _Optional[int]=..., height: _Optional[int]=...) -> None:
        ...