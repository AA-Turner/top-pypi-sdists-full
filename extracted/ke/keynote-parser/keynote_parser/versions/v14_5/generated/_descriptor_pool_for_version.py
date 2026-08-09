"""Private Protobuf descriptor pool for one bundled version of Keynote.

Generated code! Edit dumper/rewrite_descriptor_pool.py instead.

Generated modules normally register into descriptor_pool.Default(), which is
global to the process and keyed by .proto filename. Every Keynote version
compiles the same filenames, so two versions sharing the default pool collide
with "duplicate file name". Each version gets its own pool instead.
"""

from google.protobuf import descriptor_pb2, descriptor_pool

POOL = descriptor_pool.DescriptorPool()

# A fresh pool does not carry the well-known types, and these schemas import
# google/protobuf/descriptor.proto (TSP.FieldOptions extends FieldOptions).
# Seed them from the default pool's copies.
for _well_known_descriptor in (descriptor_pb2.DESCRIPTOR,):
    _file_descriptor_proto = descriptor_pb2.FileDescriptorProto()
    _well_known_descriptor.CopyToProto(_file_descriptor_proto)
    POOL.Add(_file_descriptor_proto)
