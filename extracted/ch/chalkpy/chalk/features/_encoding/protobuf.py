from functools import cache
from typing import Any

import pyarrow as pa
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet
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
def convert_proto_message_type_to_pyarrow_type(proto_message_class: Descriptor) -> pa.DataType:
    default_max_depth = 15

    def _convert_proto_message_type_to_pyarrow_type(
        proto_message_class: Descriptor, max_depth: int, infinite_recursion_detector: set[Descriptor]
    ) -> pa.DataType:
        """Converts a Protocol Buffer message class into an equivalent PyArrow struct type."""
        if max_depth == 0:
            raise RecursionError(
                f"Recursion limit exceeded when converting proto message type to pyarrow. This error occurs if the resulting pyarrow structure would be over {default_max_depth} levels deep."
            )
        struct_fields = []
        for fd in proto_message_class.fields:
            if fd.type == FieldDescriptor.TYPE_MESSAGE:
                new_message_type: Descriptor = fd.message_type
                if fd.message_type in infinite_recursion_detector:
                    raise RecursionError(
                        f"Infinitely recursive proto structure detected when converting proto message type to pyarrow - message '{new_message_type.full_name}' has a self-referential definition."
                    )
                infinite_recursion_detector.add(new_message_type)
                field_type = _convert_proto_message_type_to_pyarrow_type(
                    new_message_type, max_depth=max_depth - 1, infinite_recursion_detector=infinite_recursion_detector
                )
                infinite_recursion_detector.remove(new_message_type)
            else:
                field_type = _get_pyarrow_type_for_proto_field(fd)
            if fd.label == FieldDescriptor.LABEL_REPEATED:
                field_type = pa.large_list(field_type)
            struct_fields.append(pa.field(fd.name, field_type, fd.label != FieldDescriptor.LABEL_REQUIRED))
        return pa.struct(struct_fields)

    return _convert_proto_message_type_to_pyarrow_type(
        proto_message_class, max_depth=default_max_depth, infinite_recursion_detector=set()
    )


def create_empty_pyarrow_scalar_from_proto_type(proto_message: Message) -> pa.Scalar:
    """Creates a PyArrow scalar with None value but with type structure matching the Protocol Buffer message."""
    pa_type = convert_proto_message_type_to_pyarrow_type(proto_message.DESCRIPTOR)
    return pa.scalar({}, type=pa_type)


@cache
def serialize_proto_descriptor(file_descriptor: Any) -> bytes:
    # Create a FileDescriptorSet and add your FileDescriptorProto
    file_descriptor_set = FileDescriptorSet()

    def add_dependencies(file_descriptor: Any):
        for dependency in file_descriptor.dependencies:
            add_dependencies(dependency)
        file_descriptor_proto = FileDescriptorProto()
        file_descriptor.CopyToProto(file_descriptor_proto)
        if file_descriptor_proto not in file_descriptor_set.file:
            file_descriptor_set.file.append(file_descriptor_proto)

    add_dependencies(file_descriptor)

    # Serialize to bytes
    return file_descriptor_set.SerializeToString()
