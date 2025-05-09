# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: variant2.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from . import variant_pb2 as variant__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='variant2.proto',
  package='com.rookout',
  syntax='proto3',
  serialized_options=b'\n\031com.rookout.rook.protobufZ2github.com/Rookout/management/pkg/protos/protobuf2',
  serialized_pb=b'\n\x0evariant2.proto\x12\x0b\x63om.rookout\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\rvariant.proto\"\xa0\x01\n\x06\x45rror2\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12)\n\nparameters\x18\x03 \x01(\x0b\x32\x15.com.rookout.Variant2\x12\"\n\x03\x65xc\x18\x04 \x01(\x0b\x32\x15.com.rookout.Variant2\x12(\n\ttraceback\x18\x05 \x01(\x0b\x32\x15.com.rookout.Variant2\"\xe1\x04\n\x08Variant2\x12\x1e\n\x16variant_type_max_depth\x18\x01 \x01(\r\x12$\n\x1coriginal_type_index_in_cache\x18\x02 \x01(\r\x12 \n\x18\x61ttribute_names_in_cache\x18\x03 \x03(\r\x12/\n\x10\x61ttribute_values\x18\x04 \x03(\x0b\x32\x15.com.rookout.Variant2\x12\x15\n\roriginal_size\x18\x05 \x01(\r\x12\x12\n\nlong_value\x18\x06 \x01(\x03\x12\x1c\n\x14\x62ytes_index_in_cache\x18\x07 \x01(\r\x12.\n\x0f\x63ollection_keys\x18\x08 \x03(\x0b\x32\x15.com.rookout.Variant2\x12\x30\n\x11\x63ollection_values\x18\t \x03(\x0b\x32\x15.com.rookout.Variant2\x12\x14\n\x0c\x64ouble_value\x18\n \x01(\x01\x12\x34\n\x0b\x63ode_values\x18\x0b \x03(\x0b\x32\x1f.com.rookout.Variant.CodeObject\x12.\n\ntime_value\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x0b\x65rror_value\x18\x10 \x01(\x0b\x32\x13.com.rookout.Error2\x12\x33\n\rcomplex_value\x18\x11 \x01(\x0b\x32\x1c.com.rookout.Variant.Complex\x12\x36\n\x08livetail\x18\x12 \x01(\x0b\x32$.com.rookout.Variant.LiveTailMessageBO\n\x19\x63om.rookout.rook.protobufZ2github.com/Rookout/management/pkg/protos/protobuf2b\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,variant__pb2.DESCRIPTOR,])




_ERROR2 = _descriptor.Descriptor(
  name='Error2',
  full_name='com.rookout.Error2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='com.rookout.Error2.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='com.rookout.Error2.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='com.rookout.Error2.parameters', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='exc', full_name='com.rookout.Error2.exc', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='traceback', full_name='com.rookout.Error2.traceback', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=240,
)


_VARIANT2 = _descriptor.Descriptor(
  name='Variant2',
  full_name='com.rookout.Variant2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='variant_type_max_depth', full_name='com.rookout.Variant2.variant_type_max_depth', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='original_type_index_in_cache', full_name='com.rookout.Variant2.original_type_index_in_cache', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attribute_names_in_cache', full_name='com.rookout.Variant2.attribute_names_in_cache', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attribute_values', full_name='com.rookout.Variant2.attribute_values', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='original_size', full_name='com.rookout.Variant2.original_size', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='long_value', full_name='com.rookout.Variant2.long_value', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bytes_index_in_cache', full_name='com.rookout.Variant2.bytes_index_in_cache', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection_keys', full_name='com.rookout.Variant2.collection_keys', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collection_values', full_name='com.rookout.Variant2.collection_values', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='double_value', full_name='com.rookout.Variant2.double_value', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='code_values', full_name='com.rookout.Variant2.code_values', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time_value', full_name='com.rookout.Variant2.time_value', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error_value', full_name='com.rookout.Variant2.error_value', index=12,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='complex_value', full_name='com.rookout.Variant2.complex_value', index=13,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='livetail', full_name='com.rookout.Variant2.livetail', index=14,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=243,
  serialized_end=852,
)

_ERROR2.fields_by_name['parameters'].message_type = _VARIANT2
_ERROR2.fields_by_name['exc'].message_type = _VARIANT2
_ERROR2.fields_by_name['traceback'].message_type = _VARIANT2
_VARIANT2.fields_by_name['attribute_values'].message_type = _VARIANT2
_VARIANT2.fields_by_name['collection_keys'].message_type = _VARIANT2
_VARIANT2.fields_by_name['collection_values'].message_type = _VARIANT2
_VARIANT2.fields_by_name['code_values'].message_type = variant__pb2._VARIANT_CODEOBJECT
_VARIANT2.fields_by_name['time_value'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_VARIANT2.fields_by_name['error_value'].message_type = _ERROR2
_VARIANT2.fields_by_name['complex_value'].message_type = variant__pb2._VARIANT_COMPLEX
_VARIANT2.fields_by_name['livetail'].message_type = variant__pb2._VARIANT_LIVETAILMESSAGE
DESCRIPTOR.message_types_by_name['Error2'] = _ERROR2
DESCRIPTOR.message_types_by_name['Variant2'] = _VARIANT2
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Error2 = _reflection.GeneratedProtocolMessageType('Error2', (_message.Message,), {
  'DESCRIPTOR' : _ERROR2,
  '__module__' : 'variant2_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.Error2)
  })
_sym_db.RegisterMessage(Error2)

Variant2 = _reflection.GeneratedProtocolMessageType('Variant2', (_message.Message,), {
  'DESCRIPTOR' : _VARIANT2,
  '__module__' : 'variant2_pb2'
  # @@protoc_insertion_point(class_scope:com.rookout.Variant2)
  })
_sym_db.RegisterMessage(Variant2)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
