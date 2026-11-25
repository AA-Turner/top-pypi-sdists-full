"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'board/board_tasks.proto')
_sym_db = _symbol_database.Default()
from ..common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
from ..board import board_rules_pb2 as board_dot_board__rules__pb2
from ..common import tasks_pb2 as common_dot_tasks__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17board/board_tasks.proto\x12\x11kiapi.board.tasks\x1a\x1dcommon/types/base_types.proto\x1a\x17board/board_rules.proto\x1a\x12common/tasks.proto"u\n\x14StartRefillZonesTask\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\'\n\x05zones\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIID"\xa2\x01\n\x0cStartDrcTask\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\x1f\n\x17report_all_track_errors\x18\x02 \x01(\x08\x12\x1d\n\x15test_schematic_parity\x18\x03 \x01(\x08\x12\x1c\n\x14require_zones_filled\x18\x04 \x01(\x08"@\n\x10GetDrcTaskResult\x12,\n\x05token\x18\x01 \x01(\x0b2\x1d.kiapi.common.tasks.TaskToken"j\n\rDrcTaskResult\x12*\n\nviolations\x18\x01 \x03(\x0b2\x16.kiapi.board.DrcMarker\x12\x15\n\rignored_count\x18\x02 \x01(\x05\x12\x16\n\x0eexcluded_count\x18\x03 \x01(\x05b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'board.board_tasks_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_STARTREFILLZONESTASK']._serialized_start = 122
    _globals['_STARTREFILLZONESTASK']._serialized_end = 239
    _globals['_STARTDRCTASK']._serialized_start = 242
    _globals['_STARTDRCTASK']._serialized_end = 404
    _globals['_GETDRCTASKRESULT']._serialized_start = 406
    _globals['_GETDRCTASKRESULT']._serialized_end = 470
    _globals['_DRCTASKRESULT']._serialized_start = 472
    _globals['_DRCTASKRESULT']._serialized_end = 578