"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ......ibc.applications.interchain_accounts.controller.v1 import controller_pb2 as ibc_dot_applications_dot_interchain__accounts_dot_controller_dot_v1_dot_controller__pb2
from ......gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ......google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n>ibc/applications/interchain_accounts/controller/v1/query.proto\x122ibc.applications.interchain_accounts.controller.v1\x1aCibc/applications/interchain_accounts/controller/v1/controller.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto"_\n\x1dQueryInterchainAccountRequest\x12\r\n\x05owner\x18\x01 \x01(\t\x12/\n\rconnection_id\x18\x02 \x01(\tB\x18\xf2\xde\x1f\x14yaml:"connection_id""1\n\x1eQueryInterchainAccountResponse\x12\x0f\n\x07address\x18\x01 \x01(\t"\x14\n\x12QueryParamsRequest"a\n\x13QueryParamsResponse\x12J\n\x06params\x18\x01 \x01(\x0b2:.ibc.applications.interchain_accounts.controller.v1.Params2\xfc\x03\n\x05Query\x12\x9a\x02\n\x11InterchainAccount\x12Q.ibc.applications.interchain_accounts.controller.v1.QueryInterchainAccountRequest\x1aR.ibc.applications.interchain_accounts.controller.v1.QueryInterchainAccountResponse"^\x82\xd3\xe4\x93\x02X\x12V/ibc/apps/interchain_accounts/controller/v1/owners/{owner}/connections/{connection_id}\x12\xd5\x01\n\x06Params\x12F.ibc.applications.interchain_accounts.controller.v1.QueryParamsRequest\x1aG.ibc.applications.interchain_accounts.controller.v1.QueryParamsResponse":\x82\xd3\xe4\x93\x024\x122/ibc/apps/interchain_accounts/controller/v1/paramsBRZPgithub.com/cosmos/ibc-go/v4/modules/apps/27-interchain-accounts/controller/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ibc.applications.interchain_accounts.controller.v1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZPgithub.com/cosmos/ibc-go/v4/modules/apps/27-interchain-accounts/controller/types'
    _QUERYINTERCHAINACCOUNTREQUEST.fields_by_name['connection_id']._options = None
    _QUERYINTERCHAINACCOUNTREQUEST.fields_by_name['connection_id']._serialized_options = b'\xf2\xde\x1f\x14yaml:"connection_id"'
    _QUERY.methods_by_name['InterchainAccount']._options = None
    _QUERY.methods_by_name['InterchainAccount']._serialized_options = b'\x82\xd3\xe4\x93\x02X\x12V/ibc/apps/interchain_accounts/controller/v1/owners/{owner}/connections/{connection_id}'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x024\x122/ibc/apps/interchain_accounts/controller/v1/params'
    _globals['_QUERYINTERCHAINACCOUNTREQUEST']._serialized_start = 239
    _globals['_QUERYINTERCHAINACCOUNTREQUEST']._serialized_end = 334
    _globals['_QUERYINTERCHAINACCOUNTRESPONSE']._serialized_start = 336
    _globals['_QUERYINTERCHAINACCOUNTRESPONSE']._serialized_end = 385
    _globals['_QUERYPARAMSREQUEST']._serialized_start = 387
    _globals['_QUERYPARAMSREQUEST']._serialized_end = 407
    _globals['_QUERYPARAMSRESPONSE']._serialized_start = 409
    _globals['_QUERYPARAMSRESPONSE']._serialized_end = 506
    _globals['_QUERY']._serialized_start = 509
    _globals['_QUERY']._serialized_end = 1017