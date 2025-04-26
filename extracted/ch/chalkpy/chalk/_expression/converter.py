from typing import Union, cast

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as arrow_pb
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk.features._encoding.converter import PrimitiveFeatureConverter
from chalk.features._encoding.primitive import TPrimitive


def convert_pa_dtype_to_proto_expr(dtype: pa.DataType) -> expr_pb.LogicalExprNode:
    """
    This is kind of a hack - use the 'null' literal for a dtype to convey the dtype information.
    """

    return expr_pb.LogicalExprNode(
        literal_value=expr_pb.ExprLiteral(
            # HACK: Using this to store a dtype. This is not really a scalar value.
            value=arrow_pb.ScalarValue(null_value=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(dtype)),
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
    converter = PrimitiveFeatureConverter(
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
    scalar_val = PrimitiveFeatureConverter.from_protobuf_to_pyarrow(node.literal_value.value)
    if node.literal_value.is_arrow_scalar_object:
        return scalar_val
    else:
        return cast(TPrimitive, scalar_val.as_py())
