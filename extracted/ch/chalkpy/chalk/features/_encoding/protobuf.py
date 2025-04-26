import pyarrow as pa
from google.protobuf.descriptor import Descriptor, FieldDescriptor
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


def convert_proto_message_type_to_pyarrow_type(proto_message_class: Descriptor) -> pa.DataType:
    """Converts a Protocol Buffer message class into an equivalent PyArrow struct type."""
    struct_fields = []
    for fd in proto_message_class.fields:
        if fd.type == FieldDescriptor.TYPE_MESSAGE:
            field_type = convert_proto_message_type_to_pyarrow_type(fd.message_type)
        else:
            field_type = _get_pyarrow_type_for_proto_field(fd)
        if fd.label == FieldDescriptor.LABEL_REPEATED:
            field_type = pa.large_list(field_type)
        struct_fields.append(pa.field(fd.name, field_type, fd.label != FieldDescriptor.LABEL_REQUIRED))
    return pa.struct(struct_fields)


def create_null_pyarrow_scalar_from_proto_type(proto_message: Message) -> pa.Scalar:
    """Creates a PyArrow scalar with None value but with type structure matching the Protocol Buffer message."""
    pa_type = convert_proto_message_type_to_pyarrow_type(proto_message.DESCRIPTOR)
    return pa.scalar(None, type=pa_type)
