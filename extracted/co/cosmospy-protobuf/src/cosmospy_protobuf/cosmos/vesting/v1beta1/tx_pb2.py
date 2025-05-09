"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fcosmos/vesting/v1beta1/tx.proto\x12\x16cosmos.vesting.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x8e\x02\n\x17MsgCreateVestingAccount\x12-\n\x0cfrom_address\x18\x01 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"from_address"\x12)\n\nto_address\x18\x02 \x01(\tB\x15\xf2\xde\x1f\x11yaml:"to_address"\x12[\n\x06amount\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12%\n\x08end_time\x18\x04 \x01(\x03B\x13\xf2\xde\x1f\x0fyaml:"end_time"\x12\x0f\n\x07delayed\x18\x05 \x01(\x08:\x04\xe8\xa0\x1f\x01"!\n\x1fMsgCreateVestingAccountResponse2\x88\x01\n\x03Msg\x12\x80\x01\n\x14CreateVestingAccount\x12/.cosmos.vesting.v1beta1.MsgCreateVestingAccount\x1a7.cosmos.vesting.v1beta1.MsgCreateVestingAccountResponseB3Z1github.com/cosmos/cosmos-sdk/x/auth/vesting/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.vesting.v1beta1.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z1github.com/cosmos/cosmos-sdk/x/auth/vesting/types'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['from_address']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['from_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"from_address"'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['to_address']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['to_address']._serialized_options = b'\xf2\xde\x1f\x11yaml:"to_address"'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['amount']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGCREATEVESTINGACCOUNT.fields_by_name['end_time']._options = None
    _MSGCREATEVESTINGACCOUNT.fields_by_name['end_time']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"end_time"'
    _MSGCREATEVESTINGACCOUNT._options = None
    _MSGCREATEVESTINGACCOUNT._serialized_options = b'\xe8\xa0\x1f\x01'
    _globals['_MSGCREATEVESTINGACCOUNT']._serialized_start = 114
    _globals['_MSGCREATEVESTINGACCOUNT']._serialized_end = 384
    _globals['_MSGCREATEVESTINGACCOUNTRESPONSE']._serialized_start = 386
    _globals['_MSGCREATEVESTINGACCOUNTRESPONSE']._serialized_end = 419
    _globals['_MSG']._serialized_start = 422
    _globals['_MSG']._serialized_end = 558