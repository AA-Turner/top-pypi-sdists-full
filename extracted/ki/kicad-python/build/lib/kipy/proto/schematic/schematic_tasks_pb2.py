"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'schematic/schematic_tasks.proto')
_sym_db = _symbol_database.Default()
from ..common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
from ..schematic import schematic_rules_pb2 as schematic_dot_schematic__rules__pb2
from ..common import tasks_pb2 as common_dot_tasks__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fschematic/schematic_tasks.proto\x12\x15kiapi.schematic.tasks\x1a\x1dcommon/types/base_types.proto\x1a\x1fschematic/schematic_rules.proto\x1a\x12common/tasks.proto"G\n\x0cStartErcTask\x127\n\x08document\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"@\n\x10GetErcTaskResult\x12,\n\x05token\x18\x01 \x01(\x0b2\x1d.kiapi.common.tasks.TaskToken"n\n\rErcTaskResult\x12.\n\nviolations\x18\x01 \x03(\x0b2\x1a.kiapi.schematic.ErcMarker\x12\x15\n\rignored_count\x18\x02 \x01(\x05\x12\x16\n\x0eexcluded_count\x18\x03 \x01(\x05b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'schematic.schematic_tasks_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_STARTERCTASK']._serialized_start = 142
    _globals['_STARTERCTASK']._serialized_end = 213
    _globals['_GETERCTASKRESULT']._serialized_start = 215
    _globals['_GETERCTASKRESULT']._serialized_end = 279
    _globals['_ERCTASKRESULT']._serialized_start = 281
    _globals['_ERCTASKRESULT']._serialized_end = 391