from interchain_security.ccv.v1 import ccv_pb2 as _ccv_pb2
from interchain_security.ccv.consumer.v1 import consumer_pb2 as _consumer_pb2
from tendermint.abci import types_pb2 as _types_pb2
from ibc.lightclients.tendermint.v1 import tendermint_pb2 as _tendermint_pb2
from ibc.core.channel.v1 import channel_pb2 as _channel_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params', 'provider_client_id', 'provider_channel_id', 'new_chain', 'provider_client_state', 'provider_consensus_state', 'maturing_packets', 'initial_val_set', 'height_to_valset_update_id', 'outstanding_downtime_slashing', 'pending_consumer_packets', 'last_transmission_block_height', 'preCCV']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_CHAIN_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CLIENT_STATE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONSENSUS_STATE_FIELD_NUMBER: _ClassVar[int]
    MATURING_PACKETS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_VAL_SET_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_TO_VALSET_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    OUTSTANDING_DOWNTIME_SLASHING_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONSUMER_PACKETS_FIELD_NUMBER: _ClassVar[int]
    LAST_TRANSMISSION_BLOCK_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PRECCV_FIELD_NUMBER: _ClassVar[int]
    params: _consumer_pb2.Params
    provider_client_id: str
    provider_channel_id: str
    new_chain: bool
    provider_client_state: _tendermint_pb2.ClientState
    provider_consensus_state: _tendermint_pb2.ConsensusState
    maturing_packets: _containers.RepeatedCompositeFieldContainer[_consumer_pb2.MaturingVSCPacket]
    initial_val_set: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    height_to_valset_update_id: _containers.RepeatedCompositeFieldContainer[HeightToValsetUpdateID]
    outstanding_downtime_slashing: _containers.RepeatedCompositeFieldContainer[OutstandingDowntime]
    pending_consumer_packets: _ccv_pb2.ConsumerPacketDataList
    last_transmission_block_height: _consumer_pb2.LastTransmissionBlockHeight
    preCCV: bool

    def __init__(self, params: _Optional[_Union[_consumer_pb2.Params, _Mapping]]=..., provider_client_id: _Optional[str]=..., provider_channel_id: _Optional[str]=..., new_chain: bool=..., provider_client_state: _Optional[_Union[_tendermint_pb2.ClientState, _Mapping]]=..., provider_consensus_state: _Optional[_Union[_tendermint_pb2.ConsensusState, _Mapping]]=..., maturing_packets: _Optional[_Iterable[_Union[_consumer_pb2.MaturingVSCPacket, _Mapping]]]=..., initial_val_set: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]]=..., height_to_valset_update_id: _Optional[_Iterable[_Union[HeightToValsetUpdateID, _Mapping]]]=..., outstanding_downtime_slashing: _Optional[_Iterable[_Union[OutstandingDowntime, _Mapping]]]=..., pending_consumer_packets: _Optional[_Union[_ccv_pb2.ConsumerPacketDataList, _Mapping]]=..., last_transmission_block_height: _Optional[_Union[_consumer_pb2.LastTransmissionBlockHeight, _Mapping]]=..., preCCV: bool=...) -> None:
        ...

class HeightToValsetUpdateID(_message.Message):
    __slots__ = ['height', 'valset_update_id']
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    VALSET_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    height: int
    valset_update_id: int

    def __init__(self, height: _Optional[int]=..., valset_update_id: _Optional[int]=...) -> None:
        ...

class OutstandingDowntime(_message.Message):
    __slots__ = ['validator_consensus_address']
    VALIDATOR_CONSENSUS_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    validator_consensus_address: str

    def __init__(self, validator_consensus_address: _Optional[str]=...) -> None:
        ...