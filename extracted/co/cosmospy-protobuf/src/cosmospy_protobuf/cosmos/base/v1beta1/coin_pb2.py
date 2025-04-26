"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ecosmos/base/v1beta1/coin.proto\x12\x13cosmos.base.v1beta1\x1a\x14gogoproto/gogo.proto"8\n\x04Coin\x12\r\n\x05denom\x18\x01 \x01(\t\x12\x1b\n\x06amount\x18\x02 \x01(\tB\x0b\xc8\xde\x1f\x00\xda\xde\x1f\x03Int:\x04\xe8\xa0\x1f\x01";\n\x07DecCoin\x12\r\n\x05denom\x18\x01 \x01(\t\x12\x1b\n\x06amount\x18\x02 \x01(\tB\x0b\xc8\xde\x1f\x00\xda\xde\x1f\x03Dec:\x04\xe8\xa0\x1f\x01"$\n\x08IntProto\x12\x18\n\x03int\x18\x01 \x01(\tB\x0b\xc8\xde\x1f\x00\xda\xde\x1f\x03Int"$\n\x08DecProto\x12\x18\n\x03dec\x18\x01 \x01(\tB\x0b\xc8\xde\x1f\x00\xda\xde\x1f\x03DecB,Z"github.com/cosmos/cosmos-sdk/types\xd8\xe1\x1e\x00\x80\xe2\x1e\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.v1beta1.coin_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z"github.com/cosmos/cosmos-sdk/types\xd8\xe1\x1e\x00\x80\xe2\x1e\x00'
    _COIN.fields_by_name['amount']._options = None
    _COIN.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Int'
    _COIN._options = None
    _COIN._serialized_options = b'\xe8\xa0\x1f\x01'
    _DECCOIN.fields_by_name['amount']._options = None
    _DECCOIN.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Dec'
    _DECCOIN._options = None
    _DECCOIN._serialized_options = b'\xe8\xa0\x1f\x01'
    _INTPROTO.fields_by_name['int']._options = None
    _INTPROTO.fields_by_name['int']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Int'
    _DECPROTO.fields_by_name['dec']._options = None
    _DECPROTO.fields_by_name['dec']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f\x03Dec'
    _globals['_COIN']._serialized_start = 77
    _globals['_COIN']._serialized_end = 133
    _globals['_DECCOIN']._serialized_start = 135
    _globals['_DECCOIN']._serialized_end = 194
    _globals['_INTPROTO']._serialized_start = 196
    _globals['_INTPROTO']._serialized_end = 232
    _globals['_DECPROTO']._serialized_start = 234
    _globals['_DECPROTO']._serialized_end = 270