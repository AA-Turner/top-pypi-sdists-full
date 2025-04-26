"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....interchain_security.ccv.v1 import ccv_pb2 as interchain__security_dot_ccv_dot_v1_dot_ccv__pb2
from .....interchain_security.ccv.provider.v1 import provider_pb2 as interchain__security_dot_ccv_dot_provider_dot_v1_dot_provider__pb2
from .....interchain_security.ccv.consumer.v1 import consumer_pb2 as interchain__security_dot_ccv_dot_consumer_dot_v1_dot_consumer__pb2
from .....interchain_security.ccv.consumer.v1 import genesis_pb2 as interchain__security_dot_ccv_dot_consumer_dot_v1_dot_genesis__pb2
from .....tendermint.crypto import keys_pb2 as tendermint_dot_crypto_dot_keys__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1interchain_security/ccv/provider/v1/genesis.proto\x12#interchain_security.ccv.provider.v1\x1a\x14gogoproto/gogo.proto\x1a$interchain_security/ccv/v1/ccv.proto\x1a2interchain_security/ccv/provider/v1/provider.proto\x1a2interchain_security/ccv/consumer/v1/consumer.proto\x1a1interchain_security/ccv/consumer/v1/genesis.proto\x1a\x1ctendermint/crypto/keys.proto"\xe2\x07\n\x0cGenesisState\x12\x18\n\x10valset_update_id\x18\x01 \x01(\x04\x12k\n\x0fconsumer_states\x18\x02 \x03(\x0b22.interchain_security.ccv.provider.v1.ConsumerStateB\x1e\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"consumer_states"\x12M\n\runbonding_ops\x18\x03 \x03(\x0b20.interchain_security.ccv.provider.v1.UnbondingOpB\x04\xc8\xde\x1f\x00\x12M\n\x14mature_unbonding_ops\x18\x04 \x01(\x0b2/.interchain_security.ccv.v1.MaturedUnbondingOps\x12e\n\x1avalset_update_id_to_height\x18\x05 \x03(\x0b2;.interchain_security.ccv.provider.v1.ValsetUpdateIdToHeightB\x04\xc8\xde\x1f\x00\x12h\n\x1bconsumer_addition_proposals\x18\x06 \x03(\x0b2=.interchain_security.ccv.provider.v1.ConsumerAdditionProposalB\x04\xc8\xde\x1f\x00\x12f\n\x1aconsumer_removal_proposals\x18\x07 \x03(\x0b2<.interchain_security.ccv.provider.v1.ConsumerRemovalProposalB\x04\xc8\xde\x1f\x00\x12A\n\x06params\x18\x08 \x01(\x0b2+.interchain_security.ccv.provider.v1.ParamsB\x04\xc8\xde\x1f\x00\x12f\n\x1avalidator_consumer_pubkeys\x18\t \x03(\x0b2<.interchain_security.ccv.provider.v1.ValidatorConsumerPubKeyB\x04\xc8\xde\x1f\x00\x12g\n\x1bvalidators_by_consumer_addr\x18\n \x03(\x0b2<.interchain_security.ccv.provider.v1.ValidatorByConsumerAddrB\x04\xc8\xde\x1f\x00\x12`\n\x17consumer_addrs_to_prune\x18\x0b \x03(\x0b29.interchain_security.ccv.provider.v1.ConsumerAddrsToPruneB\x04\xc8\xde\x1f\x00"\x88\x03\n\rConsumerState\x12\x10\n\x08chain_id\x18\x01 \x01(\t\x12\x12\n\nchannel_id\x18\x02 \x01(\t\x12\x11\n\tclient_id\x18\x03 \x01(\t\x12\x16\n\x0einitial_height\x18\x04 \x01(\x04\x12Q\n\x10consumer_genesis\x18\x05 \x01(\x0b21.interchain_security.ccv.consumer.v1.GenesisStateB\x04\xc8\xde\x1f\x00\x12^\n\x16pending_valset_changes\x18\x06 \x03(\x0b28.interchain_security.ccv.v1.ValidatorSetChangePacketDataB\x04\xc8\xde\x1f\x00\x12\x1a\n\x12slash_downtime_ack\x18\x07 \x03(\t\x12W\n\x13unbonding_ops_index\x18\x08 \x03(\x0b24.interchain_security.ccv.provider.v1.VscUnbondingOpsB\x04\xc8\xde\x1f\x00"B\n\x16ValsetUpdateIdToHeight\x12\x18\n\x10valset_update_id\x18\x01 \x01(\x04\x12\x0e\n\x06height\x18\x02 \x01(\x04B?Z=github.com/cosmos/interchain-security/v2/x/ccv/provider/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'interchain_security.ccv.provider.v1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z=github.com/cosmos/interchain-security/v2/x/ccv/provider/types'
    _GENESISSTATE.fields_by_name['consumer_states']._options = None
    _GENESISSTATE.fields_by_name['consumer_states']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"consumer_states"'
    _GENESISSTATE.fields_by_name['unbonding_ops']._options = None
    _GENESISSTATE.fields_by_name['unbonding_ops']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['valset_update_id_to_height']._options = None
    _GENESISSTATE.fields_by_name['valset_update_id_to_height']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['consumer_addition_proposals']._options = None
    _GENESISSTATE.fields_by_name['consumer_addition_proposals']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['consumer_removal_proposals']._options = None
    _GENESISSTATE.fields_by_name['consumer_removal_proposals']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['validator_consumer_pubkeys']._options = None
    _GENESISSTATE.fields_by_name['validator_consumer_pubkeys']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['validators_by_consumer_addr']._options = None
    _GENESISSTATE.fields_by_name['validators_by_consumer_addr']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['consumer_addrs_to_prune']._options = None
    _GENESISSTATE.fields_by_name['consumer_addrs_to_prune']._serialized_options = b'\xc8\xde\x1f\x00'
    _CONSUMERSTATE.fields_by_name['consumer_genesis']._options = None
    _CONSUMERSTATE.fields_by_name['consumer_genesis']._serialized_options = b'\xc8\xde\x1f\x00'
    _CONSUMERSTATE.fields_by_name['pending_valset_changes']._options = None
    _CONSUMERSTATE.fields_by_name['pending_valset_changes']._serialized_options = b'\xc8\xde\x1f\x00'
    _CONSUMERSTATE.fields_by_name['unbonding_ops_index']._options = None
    _CONSUMERSTATE.fields_by_name['unbonding_ops_index']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_GENESISSTATE']._serialized_start = 336
    _globals['_GENESISSTATE']._serialized_end = 1330
    _globals['_CONSUMERSTATE']._serialized_start = 1333
    _globals['_CONSUMERSTATE']._serialized_end = 1725
    _globals['_VALSETUPDATEIDTOHEIGHT']._serialized_start = 1727
    _globals['_VALSETUPDATEIDTOHEIGHT']._serialized_end = 1793