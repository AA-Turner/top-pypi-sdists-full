"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n tendermint/statesync/types.proto\x12\x14tendermint.statesync"\x98\x02\n\x07Message\x12C\n\x11snapshots_request\x18\x01 \x01(\x0b2&.tendermint.statesync.SnapshotsRequestH\x00\x12E\n\x12snapshots_response\x18\x02 \x01(\x0b2\'.tendermint.statesync.SnapshotsResponseH\x00\x12;\n\rchunk_request\x18\x03 \x01(\x0b2".tendermint.statesync.ChunkRequestH\x00\x12=\n\x0echunk_response\x18\x04 \x01(\x0b2#.tendermint.statesync.ChunkResponseH\x00B\x05\n\x03sum"\x12\n\x10SnapshotsRequest"c\n\x11SnapshotsResponse\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x0e\n\x06format\x18\x02 \x01(\r\x12\x0e\n\x06chunks\x18\x03 \x01(\r\x12\x0c\n\x04hash\x18\x04 \x01(\x0c\x12\x10\n\x08metadata\x18\x05 \x01(\x0c"=\n\x0cChunkRequest\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x0e\n\x06format\x18\x02 \x01(\r\x12\r\n\x05index\x18\x03 \x01(\r"^\n\rChunkResponse\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x0e\n\x06format\x18\x02 \x01(\r\x12\r\n\x05index\x18\x03 \x01(\r\x12\r\n\x05chunk\x18\x04 \x01(\x0c\x12\x0f\n\x07missing\x18\x05 \x01(\x08B=Z;github.com/tendermint/tendermint/proto/tendermint/statesyncb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tendermint.statesync.types_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z;github.com/tendermint/tendermint/proto/tendermint/statesync'
    _globals['_MESSAGE']._serialized_start = 59
    _globals['_MESSAGE']._serialized_end = 339
    _globals['_SNAPSHOTSREQUEST']._serialized_start = 341
    _globals['_SNAPSHOTSREQUEST']._serialized_end = 359
    _globals['_SNAPSHOTSRESPONSE']._serialized_start = 361
    _globals['_SNAPSHOTSRESPONSE']._serialized_end = 460
    _globals['_CHUNKREQUEST']._serialized_start = 462
    _globals['_CHUNKREQUEST']._serialized_end = 523
    _globals['_CHUNKRESPONSE']._serialized_start = 525
    _globals['_CHUNKRESPONSE']._serialized_end = 619