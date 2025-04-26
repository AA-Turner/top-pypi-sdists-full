"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....interchain_security.ccv.v1 import ccv_pb2 as interchain__security_dot_ccv_dot_v1_dot_ccv__pb2
from .....interchain_security.ccv.consumer.v1 import consumer_pb2 as interchain__security_dot_ccv_dot_consumer_dot_v1_dot_consumer__pb2
from .....tendermint.abci import types_pb2 as tendermint_dot_abci_dot_types__pb2
from .....ibc.lightclients.tendermint.v1 import tendermint_pb2 as ibc_dot_lightclients_dot_tendermint_dot_v1_dot_tendermint__pb2
from .....ibc.core.channel.v1 import channel_pb2 as ibc_dot_core_dot_channel_dot_v1_dot_channel__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1interchain_security/ccv/consumer/v1/genesis.proto\x12#interchain_security.ccv.consumer.v1\x1a$interchain_security/ccv/v1/ccv.proto\x1a2interchain_security/ccv/consumer/v1/consumer.proto\x1a\x1btendermint/abci/types.proto\x1a/ibc/lightclients/tendermint/v1/tendermint.proto\x1a!ibc/core/channel/v1/channel.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x14gogoproto/gogo.proto"\xfe\x06\n\x0cGenesisState\x12A\n\x06params\x18\x01 \x01(\x0b2+.interchain_security.ccv.consumer.v1.ParamsB\x04\xc8\xde\x1f\x00\x12\x1a\n\x12provider_client_id\x18\x02 \x01(\t\x12\x1b\n\x13provider_channel_id\x18\x03 \x01(\t\x12\x11\n\tnew_chain\x18\x04 \x01(\x08\x12J\n\x15provider_client_state\x18\x05 \x01(\x0b2+.ibc.lightclients.tendermint.v1.ClientState\x12P\n\x18provider_consensus_state\x18\x06 \x01(\x0b2..ibc.lightclients.tendermint.v1.ConsensusState\x12V\n\x10maturing_packets\x18\x07 \x03(\x0b26.interchain_security.ccv.consumer.v1.MaturingVSCPacketB\x04\xc8\xde\x1f\x00\x12?\n\x0finitial_val_set\x18\x08 \x03(\x0b2 .tendermint.abci.ValidatorUpdateB\x04\xc8\xde\x1f\x00\x12e\n\x1aheight_to_valset_update_id\x18\t \x03(\x0b2;.interchain_security.ccv.consumer.v1.HeightToValsetUpdateIDB\x04\xc8\xde\x1f\x00\x12e\n\x1doutstanding_downtime_slashing\x18\n \x03(\x0b28.interchain_security.ccv.consumer.v1.OutstandingDowntimeB\x04\xc8\xde\x1f\x00\x12Z\n\x18pending_consumer_packets\x18\x0b \x01(\x0b22.interchain_security.ccv.v1.ConsumerPacketDataListB\x04\xc8\xde\x1f\x00\x12n\n\x1elast_transmission_block_height\x18\x0c \x01(\x0b2@.interchain_security.ccv.consumer.v1.LastTransmissionBlockHeightB\x04\xc8\xde\x1f\x00\x12\x0e\n\x06preCCV\x18\r \x01(\x08"B\n\x16HeightToValsetUpdateID\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x18\n\x10valset_update_id\x18\x02 \x01(\x04":\n\x13OutstandingDowntime\x12#\n\x1bvalidator_consensus_address\x18\x01 \x01(\tB?Z=github.com/cosmos/interchain-security/v2/x/ccv/consumer/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'interchain_security.ccv.consumer.v1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z=github.com/cosmos/interchain-security/v2/x/ccv/consumer/types'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['maturing_packets']._options = None
    _GENESISSTATE.fields_by_name['maturing_packets']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['initial_val_set']._options = None
    _GENESISSTATE.fields_by_name['initial_val_set']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['height_to_valset_update_id']._options = None
    _GENESISSTATE.fields_by_name['height_to_valset_update_id']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['outstanding_downtime_slashing']._options = None
    _GENESISSTATE.fields_by_name['outstanding_downtime_slashing']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['pending_consumer_packets']._options = None
    _GENESISSTATE.fields_by_name['pending_consumer_packets']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['last_transmission_block_height']._options = None
    _GENESISSTATE.fields_by_name['last_transmission_block_height']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_GENESISSTATE']._serialized_start = 348
    _globals['_GENESISSTATE']._serialized_end = 1242
    _globals['_HEIGHTTOVALSETUPDATEID']._serialized_start = 1244
    _globals['_HEIGHTTOVALSETUPDATEID']._serialized_end = 1310
    _globals['_OUTSTANDINGDOWNTIME']._serialized_start = 1312
    _globals['_OUTSTANDINGDOWNTIME']._serialized_end = 1370