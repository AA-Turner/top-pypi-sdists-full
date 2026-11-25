"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'common/tasks.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12common/tasks.proto\x12\x12kiapi.common.tasks"\x1a\n\tTaskToken\x12\r\n\x05value\x18\x01 \x01(\t"=\n\rGetTaskStatus\x12,\n\x05token\x18\x01 \x01(\x0b2\x1d.kiapi.common.tasks.TaskToken"Y\n\x12TaskStatusResponse\x12,\n\x05state\x18\x01 \x01(\x0e2\x1d.kiapi.common.tasks.TaskState\x12\x15\n\rerror_message\x18\x02 \x01(\t"A\n\x11StartTaskResponse\x12,\n\x05token\x18\x01 \x01(\x0b2\x1d.kiapi.common.tasks.TaskToken*^\n\tTaskState\x12\x0e\n\nTS_UNKNOWN\x10\x00\x12\x0e\n\nTS_RUNNING\x10\x01\x12\x10\n\x0cTS_COMPLETED\x10\x02\x12\r\n\tTS_FAILED\x10\x03\x12\x10\n\x0cTS_CANCELLED\x10\x04b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.tasks_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_TASKSTATE']._serialized_start = 291
    _globals['_TASKSTATE']._serialized_end = 385
    _globals['_TASKTOKEN']._serialized_start = 42
    _globals['_TASKTOKEN']._serialized_end = 68
    _globals['_GETTASKSTATUS']._serialized_start = 70
    _globals['_GETTASKSTATUS']._serialized_end = 131
    _globals['_TASKSTATUSRESPONSE']._serialized_start = 133
    _globals['_TASKSTATUSRESPONSE']._serialized_end = 222
    _globals['_STARTTASKRESPONSE']._serialized_start = 224
    _globals['_STARTTASKRESPONSE']._serialized_end = 289