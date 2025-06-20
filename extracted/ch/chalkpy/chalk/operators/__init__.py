from __future__ import annotations

import abc
import collections.abc
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Mapping, Optional, Protocol, Sequence, Union, cast

import pyarrow as pa

from chalk._expression.converter import convert_literal_to_proto_expr, convert_proto_expr_to_literal
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb
from chalk.integrations.catalogs.base_catalog import BaseCatalog
from chalk.utils.collections import ensure_tuple

if TYPE_CHECKING:
    from chalk.operators._utils import ChalkDataFrame, DfPlaceholder

_NAME_SEPARATOR = "::"


class StaticExpression(abc.ABC):
    _chalk__expression_name: ClassVar[str]
    _chalk__expression_prefix: ClassVar[str] = f"static_expression{_NAME_SEPARATOR}"

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__()
        self._chalk__args = args
        self._chalk__kwargs = kwargs

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(other, StaticExpression):
            return False
        if self._chalk__expression_name != other._chalk__expression_name:
            return False

        if len(self._chalk__args) != len(other._chalk__args):
            return False
        for x, y in zip(self._chalk__args, other._chalk__args):
            if x != y:
                return False

        if len(self._chalk__kwargs) != len(other._chalk__kwargs):
            return False
        for k, x in self._chalk__kwargs.items():
            if k not in other._chalk__kwargs:
                return False
            y = other._chalk__kwargs[k]

            if x != y:
                return False
        return True

    def _to_proto(self) -> expr_pb.LogicalExprNode:
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name=self._chalk__expression_name)),
                args=[convert_literal_to_proto_expr(x) for x in self._chalk__args],
                kwargs={k: convert_literal_to_proto_expr(v) for (k, v) in self._chalk__kwargs.items()},
            )
        )

    @classmethod
    def _from_proto(cls, expr: expr_pb.LogicalExprNode) -> StaticExpression:
        from chalk.operators._column import ColumnExpression
        from chalk.operators._literal import LiteralExpression

        if not expr.HasField("call"):
            raise ValueError(f"Expected a call expression, found: {expr.WhichOneof('expr_form')}")
        if not expr.call.func.HasField("identifier"):
            raise ValueError(f"Expected a call expression with an identifier function, found: {expr.call.func}")
        expression_name = expr.call.func.identifier.name

        if expression_name == ColumnExpression._chalk__expression_name:  # pyright: ignore[reportPrivateUsage]
            return ColumnExpression(
                source_column=convert_proto_expr_to_literal(expr.call.kwargs["source_column"]),
                alias=convert_proto_expr_to_literal(expr.call.kwargs["aliased_name"]),
            )
        elif expression_name == LiteralExpression._chalk__expression_name:  # pyright: ignore[reportPrivateUsage]
            pa_value = convert_proto_expr_to_literal(expr.call.kwargs["pa_value"])
            if not isinstance(pa_value, pa.Scalar):
                raise ValueError(f"Expected a scalar, found: {pa_value}")
            return LiteralExpression(
                value=pa_value.as_py(),  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
                dtype=pa_value.type,  # pyright: ignore[reportAttributeAccessIssue, reportOptionalMemberAccess]
                name=convert_proto_expr_to_literal(expr.call.kwargs["literal_name"]),
            )
        else:
            raise ValueError(f"Unsupported static expression serialized as ExprCall with name: {expression_name}")


class StaticOperator(abc.ABC):
    """Base class for all Static Operators.

    Instances of this class are provided as resolver inputs for static resolvers, and an instance of this operator should be returned for static resolvers.

    For resolvers that do not take inputs, use a factory function, such as ``scan_parquet``, to create a root operator.
    """

    column_names: tuple[str, ...]
    """The column names that are returned by this operator"""

    _chalk__operator_name: ClassVar[str]
    _chalk__operator_prefix: ClassVar[str] = f"static_operator{_NAME_SEPARATOR}"

    def __init__(
        self,
        parent: StaticOperator | None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__()
        self._chalk__args = args
        self._chalk__kwargs = kwargs
        self._chalk__parent = parent

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(other, StaticOperator):
            return False
        if self._chalk__operator_name != other._chalk__operator_name:
            return False

        if len(self._chalk__args) != len(other._chalk__args):
            return False
        for x, y in zip(self._chalk__args, other._chalk__args):
            if x != y:
                return False

        if len(self._chalk__kwargs) != len(other._chalk__kwargs):
            return False
        for k, x in self._chalk__kwargs.items():
            if k not in other._chalk__kwargs:
                return False
            y = other._chalk__kwargs[k]

            if x != y:
                return False

        if self._chalk__parent is None:
            return other._chalk__parent is None
        return self._chalk__parent == other._chalk__parent

    def rename_columns(self, names: Sequence[str] | Mapping[str, str]) -> StaticOperator:
        """Rename the columns.

        Parameters
        ----------
        names
            The new column names. This can either be a sequence of names, or a mapping of the old name to the new name.
            If a sequence, the length must match the number of existing columns, and columns will be renamed in-order.
            If a mapping, only the columns in the mapping will be renamed, and all other columns will be passed through
            as-is.

        Returns
        -------
        A static operator, which can be composed with other static operators.
        """

        from chalk.operators._rename import RenameOperator

        if not isinstance(names, collections.abc.Mapping):
            names = tuple(names)
            if len(names) != len(self.column_names):
                raise ValueError("If a list is given, the names must be the same length")
            names = {k: v for (k, v) in zip(self.column_names, names)}
        if not isinstance(names, collections.abc.Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The names must be a mapping of {from: to} or a list")
        for column in names:
            if column not in self.column_names:
                raise ValueError(f"Column '{column}' is not in the table")
        new_column_names: dict[str, None] = {}  # Using this like an ordered set
        for column in self.column_names:
            if column in names:
                new_name = names[column]
                if new_name in new_column_names:
                    raise ValueError(f"Column '{new_name}' would appear multiple times in the new table")
                # We are not dropping this column
                new_column_names[new_name] = None
            else:
                if column in new_column_names:
                    raise ValueError(f"Column '{column}' would appear multiple times in the new table")
                new_column_names[column] = None

        return RenameOperator(parent=self, column_names=tuple(new_column_names), old_name_to_new_name_map=names)

    def select(self, *expressions: StaticExpression) -> StaticOperator:
        from chalk.operators._select import SelectOperator

        return SelectOperator(self, expressions=tuple(expressions))

    def with_columns(self, *expressions: StaticExpression) -> StaticOperator:
        from chalk.operators._select import SelectOperator, get_name_for_expression

        name_to_expr: dict[str, StaticExpression] = {k: column(k) for k in self.column_names}
        for expr in expressions:
            name_to_expr[get_name_for_expression(expr)] = expr

        return SelectOperator(parent=self, expressions=tuple(name_to_expr.values()))

    @staticmethod
    def convert_arg_to_proto_expr(value: Any) -> expr_pb.LogicalExprNode:
        if isinstance(value, StaticExpression):
            return value._to_proto()  # pyright: ignore[reportPrivateUsage]
        return convert_literal_to_proto_expr(value)

    def _to_proto(self) -> expr_pb.LogicalExprNode:
        args = [self.convert_arg_to_proto_expr(arg) for arg in self._chalk__args]
        kwargs = {k: self.convert_arg_to_proto_expr(v) for k, v in self._chalk__kwargs.items()}
        if self._chalk__parent is not None:
            return expr_pb.LogicalExprNode(
                call=expr_pb.ExprCall(
                    func=expr_pb.LogicalExprNode(
                        get_attribute=expr_pb.ExprGetAttribute(
                            parent=self._chalk__parent._to_proto(),
                            attribute=expr_pb.Identifier(name=self._chalk__operator_name),
                        )
                    ),
                    args=args,
                    kwargs=kwargs,
                )
            )
        return expr_pb.LogicalExprNode(
            call=expr_pb.ExprCall(
                func=expr_pb.LogicalExprNode(identifier=expr_pb.Identifier(name=self._chalk__operator_name)),
                args=[self.convert_arg_to_proto_expr(x) for x in self._chalk__args],
                kwargs={k: self.convert_arg_to_proto_expr(v) for (k, v) in self._chalk__kwargs.items()},
            )
        )

    @classmethod
    def _from_proto(cls, expr: expr_pb.LogicalExprNode) -> StaticOperator | DfPlaceholder | ChalkDataFrame:
        from chalk.operators._iceberg_scan import IcebergScanOperator
        from chalk.operators._parquet_scan import ParquetScanOperator
        from chalk.operators._rename import RenameOperator
        from chalk.operators._select import SelectOperator

        if expr.HasField("call"):
            call = expr.call
            func = expr.call.func
            if func.HasField("identifier"):
                if func.identifier.name == "static_df_placeholder":
                    from chalk.operators._utils import DfPlaceholder

                    return DfPlaceholder(schema_dict={})
                if func.identifier.name == "chalk_data_frame":
                    from chalk.operators._utils import ChalkDataFrame

                    return ChalkDataFrame()
                if func.identifier.name == ParquetScanOperator._chalk__operator_name:
                    if "files" not in call.kwargs:
                        raise ValueError("ParquetScanOperator requires 'files' argument")
                    if "column_names" not in call.kwargs:
                        raise ValueError("ParquetScanOperator requires 'column_names' argument")

                    return ParquetScanOperator(
                        files=tuple(convert_proto_expr_to_literal(call.kwargs["files"])),
                        column_names=tuple(convert_proto_expr_to_literal(call.kwargs["column_names"])),
                        aws_role_arn=convert_proto_expr_to_literal(call.kwargs["aws_role_arn"])
                        if "aws_role_arn" in call.kwargs
                        else None,
                    )
                elif func.identifier.name == IcebergScanOperator._chalk__operator_name:
                    if "target" not in call.kwargs:
                        raise ValueError("IcebergScanOperator requires 'target' argument")
                    if "catalog_options" not in call.kwargs:
                        raise ValueError("IcebergScanOperator requires 'catalog_options' argument")
                    if "column_names" not in call.kwargs:
                        raise ValueError("IcebergScanOperator requires 'column_names' argument")
                    if "custom_partitions" not in call.kwargs:
                        raise ValueError("IcebergScanOperator requires 'custom_partitions' argument")

                    return IcebergScanOperator(
                        target=convert_proto_expr_to_literal(call.kwargs["target"]),
                        catalog_options=cast(
                            Mapping[str, Union[str, int, None]],
                            convert_proto_expr_to_literal(call.kwargs["catalog_options"]),
                        ),
                        column_names=tuple(convert_proto_expr_to_literal(call.kwargs["column_names"])),
                        custom_partitions=cast(
                            dict[str, tuple[Literal["date_trunc(day)"], str]],
                            convert_proto_expr_to_literal(call.kwargs["custom_partitions"]),
                        ),
                        partition_column=(
                            convert_proto_expr_to_literal(call.kwargs["partition_column"])
                            if "partition_column" in call.kwargs
                            else None
                        ),
                    )
                else:
                    raise ValueError(
                        f"Unrecognized static operator serialized as ExprCall with identifier: {func.identifier.name}"
                    )

            elif func.HasField("get_attribute"):
                if (
                    func.get_attribute.attribute.name == RenameOperator._chalk__operator_name
                ):  # pyright: ignore[reportPrivateUsage]
                    if "column_names" not in call.kwargs:
                        raise ValueError("RenameOperator requires 'column_names' argument")
                    if "old_name_to_new_name_map" not in call.kwargs:
                        raise ValueError("RenameOperator requires 'old_name_to_new_name_map' argument")
                    parent = cls._from_proto(func.get_attribute.parent)
                    if not isinstance(parent, StaticOperator):
                        raise ValueError("RenameOperator parent must be a StaticOperator")
                    return RenameOperator(
                        parent=parent,
                        column_names=tuple(convert_proto_expr_to_literal(call.kwargs["column_names"])),
                        old_name_to_new_name_map=convert_proto_expr_to_literal(call.kwargs["old_name_to_new_name_map"]),
                    )
                elif (
                    func.get_attribute.attribute.name == SelectOperator._chalk__operator_name
                ):  # pyright: ignore[reportPrivateUsage]
                    parent = cls._from_proto(func.get_attribute.parent)
                    if not isinstance(parent, StaticOperator):
                        raise ValueError("SelectOperator parent must be a StaticOperator")
                    return SelectOperator(
                        parent=parent,
                        expressions=tuple(
                            [StaticExpression._from_proto(e) for e in call.args]  # pyright: ignore[reportPrivateUsage]
                        ),
                    )
                else:
                    raise ValueError(
                        f"Unrecognized static operator serialized as ExprCall with attribute name: "
                        + f"{func.get_attribute.attribute.name}"
                    )
            else:
                raise ValueError(f"Unrecognized static operator serialized as ExprCall with func: {call.func}")

        else:
            raise ValueError(f"Unrecognized static operator serialized as {type(expr).__name__}: {expr}")


def scan_parquet(
    files: str | Sequence[str], columns: Sequence[str], *, aws_role_arn: str | None = None
) -> StaticOperator:
    """The Parquet Scan operator scans a filesystem or cloud bucket for data encoded in parquet files.


    Parameters
    ----------
    files
        A glob pattern, URI, or sequence of glob patterns or URIs for the parquet files to ingest. Each URI should be of the form
        ``protocol://bucket/path/to/files/``, where protocol can be ``gs`` for Google Cloud Storage, ``s3`` for Amazon S3, or `local`` for a
        local filepath. Absolute paths (beginning with '/') are treated as local files.
    columns
        A list of columns to select from the parquet files.
    """
    from chalk.operators._parquet_scan import ParquetScanOperator

    return ParquetScanOperator(files=ensure_tuple(files), column_names=ensure_tuple(columns), aws_role_arn=aws_role_arn)


_empty_mapping = {}


class BaseScanCatalog(BaseCatalog, Protocol):
    def to_scan_options(self) -> Mapping[str, str | int | None]:
        ...


def scan_iceberg(
    target: str,
    catalog: BaseScanCatalog,
    *,
    columns: Sequence[str],
    custom_partitions: Mapping[str, tuple[Literal["date_trunc(day)"], str]] = _empty_mapping,
    partition_column: Optional[str] = None,
) -> StaticOperator:
    """The Iceberg Scan operator scans a filesystem or cloud bucket for data encoded in Iceberg files, using the specified
    catalog to resolve tables.


    Parameters
    ----------
    target
        A glob pattern, URI, or sequence of glob patterns or URIs for the Iceberg tables to ingest. Each URI should be of the form

    catalog
        The catalog to use to resolve the tables.

    columns
        The names of the columns to select from the table. Use the `.rename_columns(...)` function to map these to your Chalk feature names.

    custom_partitions
        Iceberg tables automatically track partitions, including automatically applying transformation like date_trunc to timestamp columns.
        However, if you are partitioned by a column e.g. `event_date: date` which is the truncation of another column `event_timestamp: datetime`
        then you can provide information about this relationship in order to optimize queries made with Chalk.

    partition_column
        The name of the partition column to use for the Iceberg table. E.g., if you are partitioned by DAY(transaction_timestamp),
        you would set this to 'transaction_timestamp'.

    """
    from chalk.operators._iceberg_scan import IcebergScanOperator

    return IcebergScanOperator(
        target=target,
        catalog_options=catalog.to_scan_options(),
        column_names=ensure_tuple(columns),
        custom_partitions=dict(custom_partitions),
        partition_column=partition_column,
    )


def literal(value: Any, dtype: pa.DataType) -> StaticExpression:
    """Create a literal operator.

    Parameters
    ----------
    value
        The literal value to return.
    dtype
        The data type of the literal value.
    """
    from chalk.operators._literal import LiteralExpression

    return LiteralExpression(value, dtype, name=None)


def column(name: str) -> StaticExpression:
    """Create a column reference operator.

    Parameters
    ----------
    name
        The name of the column to reference.
    """
    from chalk.operators._column import ColumnExpression

    return ColumnExpression(name)
