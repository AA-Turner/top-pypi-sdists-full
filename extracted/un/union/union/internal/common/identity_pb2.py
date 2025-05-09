# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common/identity.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from union.internal.common import identifier_pb2 as common_dot_identifier__pb2
from union.internal.common import policy_pb2 as common_dot_policy__pb2
from union.internal.common import role_pb2 as common_dot_role__pb2
from union.internal.validate.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63ommon/identity.proto\x12\x0f\x63loudidl.common\x1a\x17\x63ommon/identifier.proto\x1a\x13\x63ommon/policy.proto\x1a\x11\x63ommon/role.proto\x1a\x17validate/validate.proto\"\xcc\x01\n\x04User\x12/\n\x02id\x18\x01 \x01(\x0b\x32\x1f.cloudidl.common.UserIdentifierR\x02id\x12-\n\x04spec\x18\x02 \x01(\x0b\x32\x19.cloudidl.common.UserSpecR\x04spec\x12/\n\x05roles\x18\x03 \x03(\x0b\x32\x15.cloudidl.common.RoleB\x02\x18\x01R\x05roles\x12\x33\n\x08policies\x18\x04 \x03(\x0b\x32\x17.cloudidl.common.PolicyR\x08policies\"\xd6\x01\n\x08UserSpec\x12\x1d\n\nfirst_name\x18\x01 \x01(\tR\tfirstName\x12\x1b\n\tlast_name\x18\x02 \x01(\tR\x08lastName\x12\x14\n\x05\x65mail\x18\x03 \x01(\tR\x05\x65mail\x12\"\n\x0corganization\x18\x04 \x01(\tR\x0corganization\x12\x1f\n\x0buser_handle\x18\x05 \x01(\tR\nuserHandle\x12\x16\n\x06groups\x18\x06 \x03(\tR\x06groups\x12\x1b\n\tphoto_url\x18\x07 \x01(\tR\x08photoUrl\"s\n\x0b\x41pplication\x12\x36\n\x02id\x18\x01 \x01(\x0b\x32&.cloudidl.common.ApplicationIdentifierR\x02id\x12,\n\x04spec\x18\x02 \x01(\x0b\x32\x18.cloudidl.common.AppSpecR\x04spec\"A\n\x07\x41ppSpec\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\"\n\x0corganization\x18\x02 \x01(\tR\x0corganization\"\xa7\x01\n\x10\x45nrichedIdentity\x12\x35\n\x04user\x18\x01 \x01(\x0b\x32\x15.cloudidl.common.UserB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\x04user\x12J\n\x0b\x61pplication\x18\x02 \x01(\x0b\x32\x1c.cloudidl.common.ApplicationB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00R\x0b\x61pplicationB\x10\n\tprincipal\x12\x03\xf8\x42\x01\"\xa4\x01\n\x08Identity\x12:\n\x07user_id\x18\x01 \x01(\x0b\x32\x1f.cloudidl.common.UserIdentifierH\x00R\x06userId\x12O\n\x0e\x61pplication_id\x18\x02 \x01(\x0b\x32&.cloudidl.common.ApplicationIdentifierH\x00R\rapplicationIdB\x0b\n\tprincipalB\xae\x01\n\x13\x63om.cloudidl.commonB\rIdentityProtoH\x02P\x01Z)github.com/unionai/cloud/gen/pb-go/common\xa2\x02\x03\x43\x43X\xaa\x02\x0f\x43loudidl.Common\xca\x02\x0f\x43loudidl\\Common\xe2\x02\x1b\x43loudidl\\Common\\GPBMetadata\xea\x02\x10\x43loudidl::Commonb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.identity_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023com.cloudidl.commonB\rIdentityProtoH\002P\001Z)github.com/unionai/cloud/gen/pb-go/common\242\002\003CCX\252\002\017Cloudidl.Common\312\002\017Cloudidl\\Common\342\002\033Cloudidl\\Common\\GPBMetadata\352\002\020Cloudidl::Common'
  _USER.fields_by_name['roles']._options = None
  _USER.fields_by_name['roles']._serialized_options = b'\030\001'
  _ENRICHEDIDENTITY.oneofs_by_name['principal']._options = None
  _ENRICHEDIDENTITY.oneofs_by_name['principal']._serialized_options = b'\370B\001'
  _ENRICHEDIDENTITY.fields_by_name['user']._options = None
  _ENRICHEDIDENTITY.fields_by_name['user']._serialized_options = b'\372B\005\212\001\002\020\001'
  _ENRICHEDIDENTITY.fields_by_name['application']._options = None
  _ENRICHEDIDENTITY.fields_by_name['application']._serialized_options = b'\372B\005\212\001\002\020\001'
  _globals['_USER']._serialized_start=133
  _globals['_USER']._serialized_end=337
  _globals['_USERSPEC']._serialized_start=340
  _globals['_USERSPEC']._serialized_end=554
  _globals['_APPLICATION']._serialized_start=556
  _globals['_APPLICATION']._serialized_end=671
  _globals['_APPSPEC']._serialized_start=673
  _globals['_APPSPEC']._serialized_end=738
  _globals['_ENRICHEDIDENTITY']._serialized_start=741
  _globals['_ENRICHEDIDENTITY']._serialized_end=908
  _globals['_IDENTITY']._serialized_start=911
  _globals['_IDENTITY']._serialized_end=1075
# @@protoc_insertion_point(module_scope)
