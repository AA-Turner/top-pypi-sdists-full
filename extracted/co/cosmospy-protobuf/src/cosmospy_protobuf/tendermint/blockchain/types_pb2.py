"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...tendermint.types import block_pb2 as tendermint_dot_types_dot_block__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!tendermint/blockchain/types.proto\x12\x15tendermint.blockchain\x1a\x1ctendermint/types/block.proto"\x1e\n\x0cBlockRequest\x12\x0e\n\x06height\x18\x01 \x01(\x03"!\n\x0fNoBlockResponse\x12\x0e\n\x06height\x18\x01 \x01(\x03"7\n\rBlockResponse\x12&\n\x05block\x18\x01 \x01(\x0b2\x17.tendermint.types.Block"\x0f\n\rStatusRequest".\n\x0eStatusResponse\x12\x0e\n\x06height\x18\x01 \x01(\x03\x12\x0c\n\x04base\x18\x02 \x01(\x03"\xd5\x02\n\x07Message\x12<\n\rblock_request\x18\x01 \x01(\x0b2#.tendermint.blockchain.BlockRequestH\x00\x12C\n\x11no_block_response\x18\x02 \x01(\x0b2&.tendermint.blockchain.NoBlockResponseH\x00\x12>\n\x0eblock_response\x18\x03 \x01(\x0b2$.tendermint.blockchain.BlockResponseH\x00\x12>\n\x0estatus_request\x18\x04 \x01(\x0b2$.tendermint.blockchain.StatusRequestH\x00\x12@\n\x0fstatus_response\x18\x05 \x01(\x0b2%.tendermint.blockchain.StatusResponseH\x00B\x05\n\x03sumB>Z<github.com/tendermint/tendermint/proto/tendermint/blockchainb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tendermint.blockchain.types_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z<github.com/tendermint/tendermint/proto/tendermint/blockchain'
    _globals['_BLOCKREQUEST']._serialized_start = 90
    _globals['_BLOCKREQUEST']._serialized_end = 120
    _globals['_NOBLOCKRESPONSE']._serialized_start = 122
    _globals['_NOBLOCKRESPONSE']._serialized_end = 155
    _globals['_BLOCKRESPONSE']._serialized_start = 157
    _globals['_BLOCKRESPONSE']._serialized_end = 212
    _globals['_STATUSREQUEST']._serialized_start = 214
    _globals['_STATUSREQUEST']._serialized_end = 229
    _globals['_STATUSRESPONSE']._serialized_start = 231
    _globals['_STATUSRESPONSE']._serialized_end = 277
    _globals['_MESSAGE']._serialized_start = 280
    _globals['_MESSAGE']._serialized_end = 621