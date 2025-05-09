# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: yandex/cloud/organizationmanager/v1/group_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'yandex/cloud/organizationmanager/v1/group_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from yandex.cloud.api import operation_pb2 as yandex_dot_cloud_dot_api_dot_operation__pb2
from yandex.cloud.organizationmanager.v1 import group_pb2 as yandex_dot_cloud_dot_organizationmanager_dot_v1_dot_group__pb2
from yandex.cloud.access import access_pb2 as yandex_dot_cloud_dot_access_dot_access__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7yandex/cloud/organizationmanager/v1/group_service.proto\x12#yandex.cloud.organizationmanager.v1\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a yandex/cloud/api/operation.proto\x1a/yandex/cloud/organizationmanager/v1/group.proto\x1a yandex/cloud/access/access.proto\x1a&yandex/cloud/operation/operation.proto\x1a\x1dyandex/cloud/validation.proto\"1\n\x0fGetGroupRequest\x12\x1e\n\x08group_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\x95\x01\n\x11ListGroupsRequest\x12%\n\x0forganization_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1e\n\npage_token\x18\x03 \x01(\tB\n\x8a\xc8\x31\x06<=2000\x12\x1a\n\x06\x66ilter\x18\x04 \x01(\tB\n\x8a\xc8\x31\x06<=1000\"i\n\x12ListGroupsResponse\x12:\n\x06groups\x18\x01 \x03(\x0b\x32*.yandex.cloud.organizationmanager.v1.Group\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x92\x01\n\x12\x43reateGroupRequest\x12%\n\x0forganization_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x35\n\x04name\x18\x02 \x01(\tB\'\xe8\xc7\x31\x01\xf2\xc7\x31\x1f[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12\x1e\n\x0b\x64\x65scription\x18\x03 \x01(\tB\t\x8a\xc8\x31\x05<=256\"\'\n\x13\x43reateGroupMetadata\x12\x10\n\x08group_id\x18\x01 \x01(\t\"\xb9\x01\n\x12UpdateGroupRequest\x12\x1e\n\x08group_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x32\n\x04name\x18\x03 \x01(\tB$\xf2\xc7\x31 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?\x12\x1e\n\x0b\x64\x65scription\x18\x04 \x01(\tB\t\x8a\xc8\x31\x05<=256\"\'\n\x13UpdateGroupMetadata\x12\x10\n\x08group_id\x18\x01 \x01(\t\"4\n\x12\x44\x65leteGroupRequest\x12\x1e\n\x08group_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"\'\n\x13\x44\x65leteGroupMetadata\x12\x10\n\x08group_id\x18\x01 \x01(\t\"{\n\x1aListGroupOperationsRequest\x12\x1e\n\x08group_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1e\n\npage_token\x18\x03 \x01(\tB\n\x8a\xc8\x31\x06<=2000\"m\n\x1bListGroupOperationsResponse\x12\x35\n\noperations\x18\x01 \x03(\x0b\x32!.yandex.cloud.operation.Operation\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"x\n\x17ListGroupMembersRequest\x12\x1e\n\x08group_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12\x1d\n\tpage_size\x18\x02 \x01(\x03\x42\n\xfa\xc7\x31\x06\x30-1000\x12\x1e\n\npage_token\x18\x03 \x01(\tB\n\x8a\xc8\x31\x06<=2000\"v\n\x18ListGroupMembersResponse\x12\x41\n\x07members\x18\x01 \x03(\x0b\x32\x30.yandex.cloud.organizationmanager.v1.GroupMember\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"7\n\x0bGroupMember\x12\x12\n\nsubject_id\x18\x01 \x01(\t\x12\x14\n\x0csubject_type\x18\x02 \x01(\t\"\x90\x01\n\x19UpdateGroupMembersRequest\x12\x1e\n\x08group_id\x18\x01 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12S\n\rmember_deltas\x18\x02 \x03(\x0b\x32\x30.yandex.cloud.organizationmanager.v1.MemberDeltaB\n\x82\xc8\x31\x06\x31-1000\".\n\x1aUpdateGroupMembersMetadata\x12\x10\n\x08group_id\x18\x01 \x01(\t\"\xc8\x01\n\x0bMemberDelta\x12S\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32=.yandex.cloud.organizationmanager.v1.MemberDelta.MemberActionB\x04\xe8\xc7\x31\x01\x12 \n\nsubject_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\"B\n\x0cMemberAction\x12\x1d\n\x19MEMBER_ACTION_UNSPECIFIED\x10\x00\x12\x07\n\x03\x41\x44\x44\x10\x01\x12\n\n\x06REMOVE\x10\x02\x32\xee\x11\n\x0cGroupService\x12\x9b\x01\n\x03Get\x12\x34.yandex.cloud.organizationmanager.v1.GetGroupRequest\x1a*.yandex.cloud.organizationmanager.v1.Group\"2\x82\xd3\xe4\x93\x02,\x12*/organization-manager/v1/groups/{group_id}\x12\xa0\x01\n\x04List\x12\x36.yandex.cloud.organizationmanager.v1.ListGroupsRequest\x1a\x37.yandex.cloud.organizationmanager.v1.ListGroupsResponse\"\'\x82\xd3\xe4\x93\x02!\x12\x1f/organization-manager/v1/groups\x12\xb0\x01\n\x06\x43reate\x12\x37.yandex.cloud.organizationmanager.v1.CreateGroupRequest\x1a!.yandex.cloud.operation.Operation\"J\xb2\xd2*\x1c\n\x13\x43reateGroupMetadata\x12\x05Group\x82\xd3\xe4\x93\x02$\"\x1f/organization-manager/v1/groups:\x01*\x12\xbb\x01\n\x06Update\x12\x37.yandex.cloud.organizationmanager.v1.UpdateGroupRequest\x1a!.yandex.cloud.operation.Operation\"U\xb2\xd2*\x1c\n\x13UpdateGroupMetadata\x12\x05Group\x82\xd3\xe4\x93\x02/2*/organization-manager/v1/groups/{group_id}:\x01*\x12\xc8\x01\n\x06\x44\x65lete\x12\x37.yandex.cloud.organizationmanager.v1.DeleteGroupRequest\x1a!.yandex.cloud.operation.Operation\"b\xb2\xd2*,\n\x13\x44\x65leteGroupMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02,**/organization-manager/v1/groups/{group_id}\x12\xd2\x01\n\x0eListOperations\x12?.yandex.cloud.organizationmanager.v1.ListGroupOperationsRequest\x1a@.yandex.cloud.organizationmanager.v1.ListGroupOperationsResponse\"=\x82\xd3\xe4\x93\x02\x37\x12\x35/organization-manager/v1/groups/{group_id}/operations\x12\xca\x01\n\x0bListMembers\x12<.yandex.cloud.organizationmanager.v1.ListGroupMembersRequest\x1a=.yandex.cloud.organizationmanager.v1.ListGroupMembersResponse\">\x82\xd3\xe4\x93\x02\x38\x12\x36/organization-manager/v1/groups/{group_id}:listMembers\x12\xee\x01\n\rUpdateMembers\x12>.yandex.cloud.organizationmanager.v1.UpdateGroupMembersRequest\x1a!.yandex.cloud.operation.Operation\"z\xb2\xd2*3\n\x1aUpdateGroupMembersMetadata\x12\x15google.protobuf.Empty\x82\xd3\xe4\x93\x02=\"8/organization-manager/v1/groups/{group_id}:updateMembers:\x01*\x12\xbf\x01\n\x12ListAccessBindings\x12..yandex.cloud.access.ListAccessBindingsRequest\x1a/.yandex.cloud.access.ListAccessBindingsResponse\"H\x82\xd3\xe4\x93\x02\x42\x12@/organization-manager/v1/groups/{resource_id}:listAccessBindings\x12\xfe\x01\n\x11SetAccessBindings\x12-.yandex.cloud.access.SetAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"\x96\x01\xb2\xd2*H\n access.SetAccessBindingsMetadata\x12$access.AccessBindingsOperationResult\x82\xd3\xe4\x93\x02\x44\"?/organization-manager/v1/groups/{resource_id}:setAccessBindings:\x01*\x12\x8a\x02\n\x14UpdateAccessBindings\x12\x30.yandex.cloud.access.UpdateAccessBindingsRequest\x1a!.yandex.cloud.operation.Operation\"\x9c\x01\xb2\xd2*K\n#access.UpdateAccessBindingsMetadata\x12$access.AccessBindingsOperationResult\x82\xd3\xe4\x93\x02G\"B/organization-manager/v1/groups/{resource_id}:updateAccessBindings:\x01*B\x86\x01\n\'yandex.cloud.api.organizationmanager.v1Z[github.com/yandex-cloud/go-genproto/yandex/cloud/organizationmanager/v1;organizationmanagerb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yandex.cloud.organizationmanager.v1.group_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\'yandex.cloud.api.organizationmanager.v1Z[github.com/yandex-cloud/go-genproto/yandex/cloud/organizationmanager/v1;organizationmanager'
  _globals['_GETGROUPREQUEST'].fields_by_name['group_id']._loaded_options = None
  _globals['_GETGROUPREQUEST'].fields_by_name['group_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTGROUPSREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_LISTGROUPSREQUEST'].fields_by_name['organization_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTGROUPSREQUEST'].fields_by_name['page_size']._loaded_options = None
  _globals['_LISTGROUPSREQUEST'].fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _globals['_LISTGROUPSREQUEST'].fields_by_name['page_token']._loaded_options = None
  _globals['_LISTGROUPSREQUEST'].fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _globals['_LISTGROUPSREQUEST'].fields_by_name['filter']._loaded_options = None
  _globals['_LISTGROUPSREQUEST'].fields_by_name['filter']._serialized_options = b'\212\3101\006<=1000'
  _globals['_CREATEGROUPREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_CREATEGROUPREQUEST'].fields_by_name['organization_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_CREATEGROUPREQUEST'].fields_by_name['name']._loaded_options = None
  _globals['_CREATEGROUPREQUEST'].fields_by_name['name']._serialized_options = b'\350\3071\001\362\3071\037[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _globals['_CREATEGROUPREQUEST'].fields_by_name['description']._loaded_options = None
  _globals['_CREATEGROUPREQUEST'].fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _globals['_UPDATEGROUPREQUEST'].fields_by_name['group_id']._loaded_options = None
  _globals['_UPDATEGROUPREQUEST'].fields_by_name['group_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_UPDATEGROUPREQUEST'].fields_by_name['name']._loaded_options = None
  _globals['_UPDATEGROUPREQUEST'].fields_by_name['name']._serialized_options = b'\362\3071 |[a-z]([-a-z0-9]{0,61}[a-z0-9])?'
  _globals['_UPDATEGROUPREQUEST'].fields_by_name['description']._loaded_options = None
  _globals['_UPDATEGROUPREQUEST'].fields_by_name['description']._serialized_options = b'\212\3101\005<=256'
  _globals['_DELETEGROUPREQUEST'].fields_by_name['group_id']._loaded_options = None
  _globals['_DELETEGROUPREQUEST'].fields_by_name['group_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTGROUPOPERATIONSREQUEST'].fields_by_name['group_id']._loaded_options = None
  _globals['_LISTGROUPOPERATIONSREQUEST'].fields_by_name['group_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTGROUPOPERATIONSREQUEST'].fields_by_name['page_size']._loaded_options = None
  _globals['_LISTGROUPOPERATIONSREQUEST'].fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _globals['_LISTGROUPOPERATIONSREQUEST'].fields_by_name['page_token']._loaded_options = None
  _globals['_LISTGROUPOPERATIONSREQUEST'].fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _globals['_LISTGROUPMEMBERSREQUEST'].fields_by_name['group_id']._loaded_options = None
  _globals['_LISTGROUPMEMBERSREQUEST'].fields_by_name['group_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_LISTGROUPMEMBERSREQUEST'].fields_by_name['page_size']._loaded_options = None
  _globals['_LISTGROUPMEMBERSREQUEST'].fields_by_name['page_size']._serialized_options = b'\372\3071\0060-1000'
  _globals['_LISTGROUPMEMBERSREQUEST'].fields_by_name['page_token']._loaded_options = None
  _globals['_LISTGROUPMEMBERSREQUEST'].fields_by_name['page_token']._serialized_options = b'\212\3101\006<=2000'
  _globals['_UPDATEGROUPMEMBERSREQUEST'].fields_by_name['group_id']._loaded_options = None
  _globals['_UPDATEGROUPMEMBERSREQUEST'].fields_by_name['group_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_UPDATEGROUPMEMBERSREQUEST'].fields_by_name['member_deltas']._loaded_options = None
  _globals['_UPDATEGROUPMEMBERSREQUEST'].fields_by_name['member_deltas']._serialized_options = b'\202\3101\0061-1000'
  _globals['_MEMBERDELTA'].fields_by_name['action']._loaded_options = None
  _globals['_MEMBERDELTA'].fields_by_name['action']._serialized_options = b'\350\3071\001'
  _globals['_MEMBERDELTA'].fields_by_name['subject_id']._loaded_options = None
  _globals['_MEMBERDELTA'].fields_by_name['subject_id']._serialized_options = b'\350\3071\001\212\3101\004<=50'
  _globals['_GROUPSERVICE'].methods_by_name['Get']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['Get']._serialized_options = b'\202\323\344\223\002,\022*/organization-manager/v1/groups/{group_id}'
  _globals['_GROUPSERVICE'].methods_by_name['List']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['List']._serialized_options = b'\202\323\344\223\002!\022\037/organization-manager/v1/groups'
  _globals['_GROUPSERVICE'].methods_by_name['Create']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['Create']._serialized_options = b'\262\322*\034\n\023CreateGroupMetadata\022\005Group\202\323\344\223\002$\"\037/organization-manager/v1/groups:\001*'
  _globals['_GROUPSERVICE'].methods_by_name['Update']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['Update']._serialized_options = b'\262\322*\034\n\023UpdateGroupMetadata\022\005Group\202\323\344\223\002/2*/organization-manager/v1/groups/{group_id}:\001*'
  _globals['_GROUPSERVICE'].methods_by_name['Delete']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['Delete']._serialized_options = b'\262\322*,\n\023DeleteGroupMetadata\022\025google.protobuf.Empty\202\323\344\223\002,**/organization-manager/v1/groups/{group_id}'
  _globals['_GROUPSERVICE'].methods_by_name['ListOperations']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['ListOperations']._serialized_options = b'\202\323\344\223\0027\0225/organization-manager/v1/groups/{group_id}/operations'
  _globals['_GROUPSERVICE'].methods_by_name['ListMembers']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['ListMembers']._serialized_options = b'\202\323\344\223\0028\0226/organization-manager/v1/groups/{group_id}:listMembers'
  _globals['_GROUPSERVICE'].methods_by_name['UpdateMembers']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['UpdateMembers']._serialized_options = b'\262\322*3\n\032UpdateGroupMembersMetadata\022\025google.protobuf.Empty\202\323\344\223\002=\"8/organization-manager/v1/groups/{group_id}:updateMembers:\001*'
  _globals['_GROUPSERVICE'].methods_by_name['ListAccessBindings']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['ListAccessBindings']._serialized_options = b'\202\323\344\223\002B\022@/organization-manager/v1/groups/{resource_id}:listAccessBindings'
  _globals['_GROUPSERVICE'].methods_by_name['SetAccessBindings']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['SetAccessBindings']._serialized_options = b'\262\322*H\n access.SetAccessBindingsMetadata\022$access.AccessBindingsOperationResult\202\323\344\223\002D\"?/organization-manager/v1/groups/{resource_id}:setAccessBindings:\001*'
  _globals['_GROUPSERVICE'].methods_by_name['UpdateAccessBindings']._loaded_options = None
  _globals['_GROUPSERVICE'].methods_by_name['UpdateAccessBindings']._serialized_options = b'\262\322*K\n#access.UpdateAccessBindingsMetadata\022$access.AccessBindingsOperationResult\202\323\344\223\002G\"B/organization-manager/v1/groups/{resource_id}:updateAccessBindings:\001*'
  _globals['_GETGROUPREQUEST']._serialized_start=348
  _globals['_GETGROUPREQUEST']._serialized_end=397
  _globals['_LISTGROUPSREQUEST']._serialized_start=400
  _globals['_LISTGROUPSREQUEST']._serialized_end=549
  _globals['_LISTGROUPSRESPONSE']._serialized_start=551
  _globals['_LISTGROUPSRESPONSE']._serialized_end=656
  _globals['_CREATEGROUPREQUEST']._serialized_start=659
  _globals['_CREATEGROUPREQUEST']._serialized_end=805
  _globals['_CREATEGROUPMETADATA']._serialized_start=807
  _globals['_CREATEGROUPMETADATA']._serialized_end=846
  _globals['_UPDATEGROUPREQUEST']._serialized_start=849
  _globals['_UPDATEGROUPREQUEST']._serialized_end=1034
  _globals['_UPDATEGROUPMETADATA']._serialized_start=1036
  _globals['_UPDATEGROUPMETADATA']._serialized_end=1075
  _globals['_DELETEGROUPREQUEST']._serialized_start=1077
  _globals['_DELETEGROUPREQUEST']._serialized_end=1129
  _globals['_DELETEGROUPMETADATA']._serialized_start=1131
  _globals['_DELETEGROUPMETADATA']._serialized_end=1170
  _globals['_LISTGROUPOPERATIONSREQUEST']._serialized_start=1172
  _globals['_LISTGROUPOPERATIONSREQUEST']._serialized_end=1295
  _globals['_LISTGROUPOPERATIONSRESPONSE']._serialized_start=1297
  _globals['_LISTGROUPOPERATIONSRESPONSE']._serialized_end=1406
  _globals['_LISTGROUPMEMBERSREQUEST']._serialized_start=1408
  _globals['_LISTGROUPMEMBERSREQUEST']._serialized_end=1528
  _globals['_LISTGROUPMEMBERSRESPONSE']._serialized_start=1530
  _globals['_LISTGROUPMEMBERSRESPONSE']._serialized_end=1648
  _globals['_GROUPMEMBER']._serialized_start=1650
  _globals['_GROUPMEMBER']._serialized_end=1705
  _globals['_UPDATEGROUPMEMBERSREQUEST']._serialized_start=1708
  _globals['_UPDATEGROUPMEMBERSREQUEST']._serialized_end=1852
  _globals['_UPDATEGROUPMEMBERSMETADATA']._serialized_start=1854
  _globals['_UPDATEGROUPMEMBERSMETADATA']._serialized_end=1900
  _globals['_MEMBERDELTA']._serialized_start=1903
  _globals['_MEMBERDELTA']._serialized_end=2103
  _globals['_MEMBERDELTA_MEMBERACTION']._serialized_start=2037
  _globals['_MEMBERDELTA_MEMBERACTION']._serialized_end=2103
  _globals['_GROUPSERVICE']._serialized_start=2106
  _globals['_GROUPSERVICE']._serialized_end=4392
# @@protoc_insertion_point(module_scope)
