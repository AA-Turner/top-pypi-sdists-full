from functools import cache
from typing import Any

import pyarrow as pa
from google.protobuf.descriptor import Descriptor, FieldDescriptor, FileDescriptor
from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb

PROTOBUF_TO_UNIT = {
    pb.TIME_UNIT_SECOND: "s",
    pb.TIME_UNIT_MILLISECOND: "ms",
    pb.TIME_UNIT_MICROSECOND: "us",
    pb.TIME_UNIT_NANOSECOND: "ns",
}


UNIT_TO_PROTOBUF = {
    "s": pb.TIME_UNIT_SECOND,
    "ms": pb.TIME_UNIT_MILLISECOND,
    "us": pb.TIME_UNIT_MICROSECOND,
    "ns": pb.TIME_UNIT_NANOSECOND,
}


def _get_pyarrow_type_for_proto_field(field_descriptor: FieldDescriptor) -> pa.DataType:
    """Maps protobuf primitive field types to PyArrow types."""
    type_mapping = {
        FieldDescriptor.TYPE_DOUBLE: pa.float64(),
        FieldDescriptor.TYPE_FLOAT: pa.float32(),
        FieldDescriptor.TYPE_INT64: pa.int64(),
        FieldDescriptor.TYPE_UINT64: pa.uint64(),
        FieldDescriptor.TYPE_INT32: pa.int32(),
        FieldDescriptor.TYPE_FIXED64: pa.uint64(),
        FieldDescriptor.TYPE_FIXED32: pa.uint32(),
        FieldDescriptor.TYPE_BOOL: pa.bool_(),
        FieldDescriptor.TYPE_STRING: pa.large_utf8(),
        FieldDescriptor.TYPE_BYTES: pa.binary(),
        FieldDescriptor.TYPE_UINT32: pa.uint32(),
        FieldDescriptor.TYPE_SFIXED32: pa.int32(),
        FieldDescriptor.TYPE_SFIXED64: pa.int64(),
        FieldDescriptor.TYPE_SINT32: pa.int32(),
        FieldDescriptor.TYPE_SINT64: pa.int64(),
        FieldDescriptor.TYPE_ENUM: pa.int32(),  # Could be refined further
    }
    return type_mapping.get(field_descriptor.type, pa.null())


@cache
def convert_proto_message_type_to_pyarrow_type(
    proto_message_class: Descriptor, proto_max_depth: int = 15
) -> pa.DataType:
    """Converts a Protocol Buffer message class into an equivalent PyArrow struct type."""

    def _convert_proto_message_type_to_pyarrow_type(
        proto_message_class: Descriptor, max_depth: int, self_referential_detector: set[Descriptor]
    ) -> pa.DataType:
        """Converts a Protocol Buffer message class into an equivalent PyArrow struct type."""
        if max_depth == 0:
            raise RecursionError(
                f"Recursion limit exceeded when converting proto message type to pyarrow. This error occurs if the resulting pyarrow structure would be over {proto_max_depth} levels deep."
            )
        struct_fields = []
        for fd in proto_message_class.fields:
            if fd.type == FieldDescriptor.TYPE_MESSAGE:
                new_message_type: Descriptor = fd.message_type
                if new_message_type in self_referential_detector:
                    raise RecursionError(
                        f"Infinitely recursive proto structure detected when converting proto message type to pyarrow - message '{new_message_type.full_name}' has a self-referential definition."
                    )
                self_referential_detector.add(new_message_type)
                field_type = _convert_proto_message_type_to_pyarrow_type(
                    new_message_type, max_depth=max_depth - 1, self_referential_detector=self_referential_detector
                )
                self_referential_detector.remove(new_message_type)
            else:
                field_type = _get_pyarrow_type_for_proto_field(fd)
            if fd.label == FieldDescriptor.LABEL_REPEATED:
                field_type = pa.large_list(field_type)
            struct_fields.append(pa.field(fd.name, field_type, fd.label != FieldDescriptor.LABEL_REQUIRED))
        return pa.struct(struct_fields)

    return _convert_proto_message_type_to_pyarrow_type(
        proto_message_class, max_depth=proto_max_depth, self_referential_detector=set()
    )


def create_empty_pyarrow_scalar_from_proto_type(proto_message: Message) -> pa.Scalar:
    """Creates a PyArrow scalar with None value but with type structure matching the Protobuf message."""
    pa_type = convert_proto_message_type_to_pyarrow_type(proto_message.DESCRIPTOR)
    return pa.scalar({}, type=pa_type)


@cache
def reconstruct_message_field_descriptor(serialized: bytes, full_name: str):
    file_descriptor_set = FileDescriptorSet()
    file_descriptor_set.ParseFromString(serialized)

    descriptor_pool = DescriptorPool()
    for file in file_descriptor_set.file:
        descriptor_pool.Add(file)

    return descriptor_pool.FindMessageTypeByName(full_name)


@cache
def serialize_message_file_descriptor(file_descriptor: Any) -> bytes:
    """Create a FileDescriptorSet containing the given Protobuf message file descriptor and its dependencies."""
    file_descriptor_set = FileDescriptorSet()
    processed_files = set()

    def add_file_and_deps(fd: FileDescriptor):
        if fd.name in processed_files:
            return

        for dep in fd.dependencies:
            add_file_and_deps(dep)

        fd_proto = FileDescriptorProto()
        fd.CopyToProto(fd_proto)

        file_descriptor_set.file.append(fd_proto)
        processed_files.add(fd.name)

    add_file_and_deps(file_descriptor)
    return file_descriptor_set.SerializeToString()
