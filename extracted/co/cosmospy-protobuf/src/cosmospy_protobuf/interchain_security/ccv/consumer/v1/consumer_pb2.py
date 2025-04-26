"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....interchain_security.ccv.v1 import ccv_pb2 as interchain__security_dot_ccv_dot_v1_dot_ccv__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2interchain_security/ccv/consumer/v1/consumer.proto\x12#interchain_security.ccv.consumer.v1\x1a$interchain_security/ccv/v1/ccv.proto\x1a\x19google/protobuf/any.proto\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xf9\x03\n\x06Params\x12\x0f\n\x07enabled\x18\x01 \x01(\x08\x12,\n$blocks_per_distribution_transmission\x18\x02 \x01(\x03\x12)\n!distribution_transmission_channel\x18\x03 \x01(\t\x12"\n\x1aprovider_fee_pool_addr_str\x18\x04 \x01(\t\x12?\n\x12ccv_timeout_period\x18\x05 \x01(\x0b2\x19.google.protobuf.DurationB\x08\xc8\xde\x1f\x00\x98\xdf\x1f\x01\x12D\n\x17transfer_timeout_period\x18\x06 \x01(\x0b2\x19.google.protobuf.DurationB\x08\xc8\xde\x1f\x00\x98\xdf\x1f\x01\x12(\n consumer_redistribution_fraction\x18\x07 \x01(\t\x12\x1a\n\x12historical_entries\x18\x08 \x01(\x03\x12=\n\x10unbonding_period\x18\t \x01(\x0b2\x19.google.protobuf.DurationB\x08\xc8\xde\x1f\x00\x98\xdf\x1f\x01\x12\x1e\n\x16soft_opt_out_threshold\x18\n \x01(\t\x12\x15\n\rreward_denoms\x18\x0b \x03(\t\x12\x1e\n\x16provider_reward_denoms\x18\x0c \x03(\t"-\n\x1bLastTransmissionBlockHeight\x12\x0e\n\x06height\x18\x01 \x01(\x03"\x90\x01\n\x13CrossChainValidator\x12\x0f\n\x07address\x18\x01 \x01(\x0c\x12\r\n\x05power\x18\x02 \x01(\x03\x12Y\n\x06pubkey\x18\x03 \x01(\x0b2\x14.google.protobuf.AnyB3\xf2\xde\x1f\x17yaml:"consensus_pubkey"\xca\xb4-\x14cosmos.crypto.PubKey"_\n\x11MaturingVSCPacket\x12\r\n\x05vscId\x18\x01 \x01(\x04\x12;\n\rmaturity_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01B?Z=github.com/cosmos/interchain-security/v2/x/ccv/consumer/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'interchain_security.ccv.consumer.v1.consumer_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z=github.com/cosmos/interchain-security/v2/x/ccv/consumer/types'
    _PARAMS.fields_by_name['ccv_timeout_period']._options = None
    _PARAMS.fields_by_name['ccv_timeout_period']._serialized_options = b'\xc8\xde\x1f\x00\x98\xdf\x1f\x01'
    _PARAMS.fields_by_name['transfer_timeout_period']._options = None
    _PARAMS.fields_by_name['transfer_timeout_period']._serialized_options = b'\xc8\xde\x1f\x00\x98\xdf\x1f\x01'
    _PARAMS.fields_by_name['unbonding_period']._options = None
    _PARAMS.fields_by_name['unbonding_period']._serialized_options = b'\xc8\xde\x1f\x00\x98\xdf\x1f\x01'
    _CROSSCHAINVALIDATOR.fields_by_name['pubkey']._options = None
    _CROSSCHAINVALIDATOR.fields_by_name['pubkey']._serialized_options = b'\xf2\xde\x1f\x17yaml:"consensus_pubkey"\xca\xb4-\x14cosmos.crypto.PubKey'
    _MATURINGVSCPACKET.fields_by_name['maturity_time']._options = None
    _MATURINGVSCPACKET.fields_by_name['maturity_time']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _globals['_PARAMS']._serialized_start = 271
    _globals['_PARAMS']._serialized_end = 776
    _globals['_LASTTRANSMISSIONBLOCKHEIGHT']._serialized_start = 778
    _globals['_LASTTRANSMISSIONBLOCKHEIGHT']._serialized_end = 823
    _globals['_CROSSCHAINVALIDATOR']._serialized_start = 826
    _globals['_CROSSCHAINVALIDATOR']._serialized_end = 970
    _globals['_MATURINGVSCPACKET']._serialized_start = 972
    _globals['_MATURINGVSCPACKET']._serialized_end = 1067