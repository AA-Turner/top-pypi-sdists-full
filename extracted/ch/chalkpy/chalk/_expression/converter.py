from typing import Union, cast

import pyarrow as pa

from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk.features._encoding.converter import make_primitive_converter, proto_to_pa_scalar
from chalk.features._encoding.primitive import TPrimitive


def convert_pa_dtype_to_proto_expr(dtype: pa.DataType) -> expr_pb.LogicalExprNode:
    """
    This is kind of a hack - use the 'null' literal for a dtype to convey the dtype information.
    """
    converter = make_primitive_converter(
        name="convert_pa_dtype_to_proto_expr",
        is_nullable=True,
        pyarrow_dtype=dtype,
    )

    return expr_pb.LogicalExprNode(
        literal_value=expr_pb.ExprLiteral(
            # HACK: Using this to store a dtype. This is not really a scalar value.
            value=converter.from_pyarrow_to_protobuf(pa.nulls(1, type=dtype)[0]),
            is_arrow_scalar_object=True,
        )
    )


def convert_literal_to_proto_expr(value: Union[TPrimitive, pa.DataType]) -> expr_pb.LogicalExprNode:
    is_arrow_scalar_object = False
    if isinstance(value, pa.Scalar):
        pa_dtype = value.type  # pyright: ignore[reportOptionalMemberAccess,reportAttributeAccessIssue]
        is_arrow_scalar_object = True
    elif isinstance(value, pa.DataType):
        return convert_pa_dtype_to_proto_expr(value)
    else:
        try:
            pa_dtype = pa.scalar(value).type
        except Exception as e:
            raise ValueError(f"Could not infer literal type for value `{value}`") from e
    converter = make_primitive_converter(
        name="convert_literal_to_proto_expr",
        is_nullable=False,
        pyarrow_dtype=pa_dtype,
    )
    return expr_pb.LogicalExprNode(
        literal_value=expr_pb.ExprLiteral(
            value=converter.from_primitive_to_protobuf(value), is_arrow_scalar_object=is_arrow_scalar_object
        )
    )


def convert_proto_expr_to_literal(node: expr_pb.LogicalExprNode) -> TPrimitive:
    if not node.HasField("literal_value"):
        raise ValueError("Expected a literal expression")
    scalar_val = proto_to_pa_scalar(node.literal_value.value)
    if node.literal_value.is_arrow_scalar_object:
        return scalar_val
    else:
        return cast(TPrimitive, scalar_val.as_py())
