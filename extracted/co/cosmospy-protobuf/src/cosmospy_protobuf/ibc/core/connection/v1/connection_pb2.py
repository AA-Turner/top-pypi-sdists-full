"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....ibc.core.commitment.v1 import commitment_pb2 as ibc_dot_core_dot_commitment_dot_v1_dot_commitment__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'ibc/core/connection/v1/connection.proto\x12\x16ibc.core.connection.v1\x1a\x14gogoproto/gogo.proto\x1a\'ibc/core/commitment/v1/commitment.proto"\x90\x02\n\rConnectionEnd\x12\'\n\tclient_id\x18\x01 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"client_id"\x121\n\x08versions\x18\x02 \x03(\x0b2\x1f.ibc.core.connection.v1.Version\x12,\n\x05state\x18\x03 \x01(\x0e2\x1d.ibc.core.connection.v1.State\x12@\n\x0ccounterparty\x18\x04 \x01(\x0b2$.ibc.core.connection.v1.CounterpartyB\x04\xc8\xde\x1f\x00\x12-\n\x0cdelay_period\x18\x05 \x01(\x04B\x17\xf2\xde\x1f\x13yaml:"delay_period":\x04\x88\xa0\x1f\x00"\xb2\x02\n\x14IdentifiedConnection\x12\x19\n\x02id\x18\x01 \x01(\tB\r\xf2\xde\x1f\tyaml:"id"\x12\'\n\tclient_id\x18\x02 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"client_id"\x121\n\x08versions\x18\x03 \x03(\x0b2\x1f.ibc.core.connection.v1.Version\x12,\n\x05state\x18\x04 \x01(\x0e2\x1d.ibc.core.connection.v1.State\x12@\n\x0ccounterparty\x18\x05 \x01(\x0b2$.ibc.core.connection.v1.CounterpartyB\x04\xc8\xde\x1f\x00\x12-\n\x0cdelay_period\x18\x06 \x01(\x04B\x17\xf2\xde\x1f\x13yaml:"delay_period":\x04\x88\xa0\x1f\x00"\xaa\x01\n\x0cCounterparty\x12\'\n\tclient_id\x18\x01 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"client_id"\x12/\n\rconnection_id\x18\x02 \x01(\tB\x18\xf2\xde\x1f\x14yaml:"connection_id"\x12:\n\x06prefix\x18\x03 \x01(\x0b2$.ibc.core.commitment.v1.MerklePrefixB\x04\xc8\xde\x1f\x00:\x04\x88\xa0\x1f\x00"\x1c\n\x0bClientPaths\x12\r\n\x05paths\x18\x01 \x03(\t"I\n\x0fConnectionPaths\x12\'\n\tclient_id\x18\x01 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"client_id"\x12\r\n\x05paths\x18\x02 \x03(\t"5\n\x07Version\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x10\n\x08features\x18\x02 \x03(\t:\x04\x88\xa0\x1f\x00"U\n\x06Params\x12K\n\x1bmax_expected_time_per_block\x18\x01 \x01(\x04B&\xf2\xde\x1f"yaml:"max_expected_time_per_block"*\x99\x01\n\x05State\x126\n\x1fSTATE_UNINITIALIZED_UNSPECIFIED\x10\x00\x1a\x11\x8a\x9d \rUNINITIALIZED\x12\x18\n\nSTATE_INIT\x10\x01\x1a\x08\x8a\x9d \x04INIT\x12\x1e\n\rSTATE_TRYOPEN\x10\x02\x1a\x0b\x8a\x9d \x07TRYOPEN\x12\x18\n\nSTATE_OPEN\x10\x03\x1a\x08\x8a\x9d \x04OPEN\x1a\x04\x88\xa3\x1e\x00B>Z<github.com/cosmos/ibc-go/v4/modules/core/03-connection/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ibc.core.connection.v1.connection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z<github.com/cosmos/ibc-go/v4/modules/core/03-connection/types'
    _STATE._options = None
    _STATE._serialized_options = b'\x88\xa3\x1e\x00'
    _STATE.values_by_name['STATE_UNINITIALIZED_UNSPECIFIED']._options = None
    _STATE.values_by_name['STATE_UNINITIALIZED_UNSPECIFIED']._serialized_options = b'\x8a\x9d \rUNINITIALIZED'
    _STATE.values_by_name['STATE_INIT']._options = None
    _STATE.values_by_name['STATE_INIT']._serialized_options = b'\x8a\x9d \x04INIT'
    _STATE.values_by_name['STATE_TRYOPEN']._options = None
    _STATE.values_by_name['STATE_TRYOPEN']._serialized_options = b'\x8a\x9d \x07TRYOPEN'
    _STATE.values_by_name['STATE_OPEN']._options = None
    _STATE.values_by_name['STATE_OPEN']._serialized_options = b'\x8a\x9d \x04OPEN'
    _CONNECTIONEND.fields_by_name['client_id']._options = None
    _CONNECTIONEND.fields_by_name['client_id']._serialized_options = b'\xf2\xde\x1f\x10yaml:"client_id"'
    _CONNECTIONEND.fields_by_name['counterparty']._options = None
    _CONNECTIONEND.fields_by_name['counterparty']._serialized_options = b'\xc8\xde\x1f\x00'
    _CONNECTIONEND.fields_by_name['delay_period']._options = None
    _CONNECTIONEND.fields_by_name['delay_period']._serialized_options = b'\xf2\xde\x1f\x13yaml:"delay_period"'
    _CONNECTIONEND._options = None
    _CONNECTIONEND._serialized_options = b'\x88\xa0\x1f\x00'
    _IDENTIFIEDCONNECTION.fields_by_name['id']._options = None
    _IDENTIFIEDCONNECTION.fields_by_name['id']._serialized_options = b'\xf2\xde\x1f\tyaml:"id"'
    _IDENTIFIEDCONNECTION.fields_by_name['client_id']._options = None
    _IDENTIFIEDCONNECTION.fields_by_name['client_id']._serialized_options = b'\xf2\xde\x1f\x10yaml:"client_id"'
    _IDENTIFIEDCONNECTION.fields_by_name['counterparty']._options = None
    _IDENTIFIEDCONNECTION.fields_by_name['counterparty']._serialized_options = b'\xc8\xde\x1f\x00'
    _IDENTIFIEDCONNECTION.fields_by_name['delay_period']._options = None
    _IDENTIFIEDCONNECTION.fields_by_name['delay_period']._serialized_options = b'\xf2\xde\x1f\x13yaml:"delay_period"'
    _IDENTIFIEDCONNECTION._options = None
    _IDENTIFIEDCONNECTION._serialized_options = b'\x88\xa0\x1f\x00'
    _COUNTERPARTY.fields_by_name['client_id']._options = None
    _COUNTERPARTY.fields_by_name['client_id']._serialized_options = b'\xf2\xde\x1f\x10yaml:"client_id"'
    _COUNTERPARTY.fields_by_name['connection_id']._options = None
    _COUNTERPARTY.fields_by_name['connection_id']._serialized_options = b'\xf2\xde\x1f\x14yaml:"connection_id"'
    _COUNTERPARTY.fields_by_name['prefix']._options = None
    _COUNTERPARTY.fields_by_name['prefix']._serialized_options = b'\xc8\xde\x1f\x00'
    _COUNTERPARTY._options = None
    _COUNTERPARTY._serialized_options = b'\x88\xa0\x1f\x00'
    _CONNECTIONPATHS.fields_by_name['client_id']._options = None
    _CONNECTIONPATHS.fields_by_name['client_id']._serialized_options = b'\xf2\xde\x1f\x10yaml:"client_id"'
    _VERSION._options = None
    _VERSION._serialized_options = b'\x88\xa0\x1f\x00'
    _PARAMS.fields_by_name['max_expected_time_per_block']._options = None
    _PARAMS.fields_by_name['max_expected_time_per_block']._serialized_options = b'\xf2\xde\x1f"yaml:"max_expected_time_per_block"'
    _globals['_STATE']._serialized_start = 1135
    _globals['_STATE']._serialized_end = 1288
    _globals['_CONNECTIONEND']._serialized_start = 131
    _globals['_CONNECTIONEND']._serialized_end = 403
    _globals['_IDENTIFIEDCONNECTION']._serialized_start = 406
    _globals['_IDENTIFIEDCONNECTION']._serialized_end = 712
    _globals['_COUNTERPARTY']._serialized_start = 715
    _globals['_COUNTERPARTY']._serialized_end = 885
    _globals['_CLIENTPATHS']._serialized_start = 887
    _globals['_CLIENTPATHS']._serialized_end = 915
    _globals['_CONNECTIONPATHS']._serialized_start = 917
    _globals['_CONNECTIONPATHS']._serialized_end = 990
    _globals['_VERSION']._serialized_start = 992
    _globals['_VERSION']._serialized_end = 1045
    _globals['_PARAMS']._serialized_start = 1047
    _globals['_PARAMS']._serialized_end = 1132