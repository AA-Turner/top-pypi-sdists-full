# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/cli/repo_diff__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.data import state_update__client_pb2 as tecton__proto_dot_data_dot_state__update____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(tecton_proto/cli/repo_diff__client.proto\x12\x10tecton_proto.cli\x1a,tecton_proto/data/state_update__client.proto\"w\n\x15TectonRepoDiffSummary\x12\x45\n\x0cobject_diffs\x18\x01 \x03(\x0b\x32\".tecton_proto.cli.TectonObjectDiffR\x0bobjectDiffs\x12\x17\n\x07plan_id\x18\x02 \x01(\tR\x06planId\"\xb3\x02\n\x10TectonObjectDiff\x12M\n\x0ftransition_type\x18\x01 \x01(\x0e\x32$.tecton_proto.data.FcoTransitionTypeR\x0etransitionType\x12\x63\n\x17transition_side_effects\x18\x04 \x01(\x0b\x32+.tecton_proto.data.FcoTransitionSideEffectsR\x15transitionSideEffects\x12O\n\x0fobject_metadata\x18\x02 \x01(\x0b\x32&.tecton_proto.cli.TectonObjectMetadataR\x0eobjectMetadata\x12\x1a\n\x08warnings\x18\x03 \x03(\tR\x08warnings\"\xa6\x02\n\x14TectonObjectMetadata\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x43\n\x0bobject_type\x18\x02 \x01(\x0e\x32\".tecton_proto.cli.TectonObjectTypeR\nobjectType\x12\x14\n\x05owner\x18\x03 \x01(\tR\x05owner\x12 \n\x0b\x64\x65scription\x18\x04 \x01(\tR\x0b\x64\x65scription\x12\x44\n\x04tags\x18\x05 \x03(\x0b\x32\x30.tecton_proto.cli.TectonObjectMetadata.TagsEntryR\x04tags\x1a\x37\n\tTagsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01*\xb3\x01\n\x10TectonObjectType\x12\x1e\n\x1aTECTON_OBJECT_TYPE_UNKNOWN\x10\x00\x12\n\n\x06\x45NTITY\x10\x01\x12\x0f\n\x0b\x44\x41TA_SOURCE\x10\x02\x12\x12\n\x0eTRANSFORMATION\x10\x03\x12\x10\n\x0c\x46\x45\x41TURE_VIEW\x10\x04\x12\x13\n\x0f\x46\x45\x41TURE_SERVICE\x10\x05\x12\x10\n\x0cSERVER_GROUP\x10\x06\x12\x15\n\x11RESOURCE_PROVIDER\x10\x07\x42\x17\n\x13\x63om.tecton.cli.diffP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.cli.repo_diff__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023com.tecton.cli.diffP\001'
  _TECTONOBJECTMETADATA_TAGSENTRY._options = None
  _TECTONOBJECTMETADATA_TAGSENTRY._serialized_options = b'8\001'
  _TECTONOBJECTTYPE._serialized_start=837
  _TECTONOBJECTTYPE._serialized_end=1016
  _TECTONREPODIFFSUMMARY._serialized_start=108
  _TECTONREPODIFFSUMMARY._serialized_end=227
  _TECTONOBJECTDIFF._serialized_start=230
  _TECTONOBJECTDIFF._serialized_end=537
  _TECTONOBJECTMETADATA._serialized_start=540
  _TECTONOBJECTMETADATA._serialized_end=834
  _TECTONOBJECTMETADATA_TAGSENTRY._serialized_start=779
  _TECTONOBJECTMETADATA_TAGSENTRY._serialized_end=834
# @@protoc_insertion_point(module_scope)
