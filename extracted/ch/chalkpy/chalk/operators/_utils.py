from __future__ import annotations

import dataclasses
import traceback
from typing import Callable, Optional, Sequence, Union

import pyarrow

from chalk import DataFrame, Features, StaticOperator
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk.client import ChalkError, ChalkException, ErrorCode, ErrorCodeCategory
from chalk.features.feature_field import Feature


class _GetStaticOperatorError(Exception):
    underlying_error: ChalkError

    def __init__(self, resolver_fqn: str, message: str, underlying_exception: Optional[Exception]):
        super().__init__(f"Failed to get a static operator from the resolver '{resolver_fqn}': {message}")

        def get_stacktrace(exc: Exception):
            try:
                return "".join(traceback.format_exception(exc))
            except TypeError:
                return "".join(traceback.format_exception(type(exc), exc, None))

        self.underlying_error = ChalkError.create(
            code=ErrorCode.RESOLVER_FAILED if underlying_exception else ErrorCode.VALIDATION_FAILED,
            category=ErrorCodeCategory.REQUEST,
            message=message,
            resolver=resolver_fqn,
            exception=ChalkException.create(
                kind=type(underlying_exception).__name__,
                message=str(underlying_exception),
                stacktrace=get_stacktrace(underlying_exception),
            )
            if underlying_exception
            else None,
        )


@dataclasses.dataclass
class DfPlaceholder:
    schema_dict: dict[str, pyarrow.DataType]

    def _to_proto(self) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="static_df_placeholder")),
                args=[],
                kwargs={},
            )
        )


@dataclasses.dataclass
class ChalkDataFrame:
    def _to_proto(self) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name="chalk_data_frame")),
                args=[],
                kwargs={},
            )
        )


def schema_for_input(input_type: Union[Feature, type[DataFrame]]) -> dict[str, pyarrow.DataType]:
    if isinstance(input_type, Feature):
        return {input_type.name: input_type.converter.pyarrow_dtype}
    elif issubclass(input_type, DataFrame):  # pyright: ignore [reportUnnecessaryIsInstance]
        return {feat.root_fqn: feat.converter.pyarrow_dtype for feat in input_type.columns}
    else:
        raise ValueError(f"Unexpected input type: {input_type}")


def static_resolver_to_operator(
    fqn: str,
    fn: Callable,
    inputs: Sequence[Union[Feature, type[DataFrame]]],
    output: Optional[type[Features]],
) -> StaticOperator | DfPlaceholder | ChalkDataFrame:
    if output is None:
        raise _GetStaticOperatorError(
            resolver_fqn=fqn,
            message="Static resolver must specify a return type",
            underlying_exception=None,
        )

    # TODO CHA-5893: Re-enable this check and permit DF -> DF and () -> DF
    if not (
        len(output.features) == 1 and isinstance(output.features[0], type) and issubclass(output.features[0], DataFrame)
    ):
        raise _GetStaticOperatorError(
            resolver_fqn=fqn,
            message="Static resolver must take no arguments and have exactly one DataFrame output",
            underlying_exception=None,
        )
    try:
        placeholder_inputs = [DfPlaceholder(schema_dict=schema_for_input(input_type)) for input_type in inputs]
        static_operator = fn(*placeholder_inputs)
    except Exception as e:
        # Weird hacky way to return a placeholder even if the resolver fails.
        if len(inputs) > 0:
            return DfPlaceholder(schema_dict={})
        raise _GetStaticOperatorError(
            resolver_fqn=fqn, message="Resolver failed with an exception", underlying_exception=e
        )
    else:
        if (
            not isinstance(static_operator, (StaticOperator, DfPlaceholder))
            and not static_operator.__class__.__name__ == "ChalkDataFrame"
            and not static_operator.__class__.__name__ == "LazyFrame"
        ):
            raise _GetStaticOperatorError(
                resolver_fqn=fqn,
                message=f"Static resolver must return a StaticOperator, found {type(static_operator).__name__}",
                underlying_exception=None,
            )
        return static_operator
