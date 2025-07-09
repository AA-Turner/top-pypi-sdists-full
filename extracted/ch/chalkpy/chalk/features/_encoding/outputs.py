# pyright: reportPrivateUsage=false
# ^ Underscore objects have chalk-specific fields that are prefixed with _chalk__ to disambiguate from expressions of the form `a.b`
import base64
import dataclasses
from typing import Any, List, Sequence, Union

from chalk._gen.chalk.common.v1.online_query_pb2 import FeatureExpression
from chalk.client.models import OutputExpression
from chalk.features import Feature, FeatureWrapper, Resolver
from chalk.features.feature_set import is_features_cls
from chalk.features.underscore import UnderscoreAttr, UnderscoreCall
from chalk.features.underscore_features import NamedUnderscoreExpr, Underscore, process_named_underscore_expr


@dataclasses.dataclass
class EncodedOutputs:
    string_outputs: List[str]
    feature_expressions_proto: List[FeatureExpression]
    feature_expressions_base64: List[str]  # B64 encoded


@dataclasses.dataclass
class NamespacelessUnderscoreExpr:
    short_name: str
    expr: Underscore


def encode_namespaceless_underscore_proto(expr: NamespacelessUnderscoreExpr) -> FeatureExpression:
    return FeatureExpression(
        namespace="",
        output_column_name=expr.short_name,
        expr=expr.expr._to_proto(),  # pyright: ignore[reportPrivateUsage]
    )


def encode_feature_expression_proto(expr: NamedUnderscoreExpr) -> FeatureExpression:
    """Deprecated. Build features and use `overlay_graph` instead or aliased underscore expressions."""
    processed_expr = process_named_underscore_expr(expr)
    return FeatureExpression(
        namespace=expr.fqn.split(".")[0],
        output_column_name=expr.fqn,
        expr=processed_expr._to_proto(),  # pyright: ignore[reportPrivateUsage]
    )


def encode_feature_expression_base64(expr: FeatureExpression) -> str:
    b = expr.SerializeToString(deterministic=True)
    return base64.b64encode(b).decode("utf-8")


def parse_underscore_aliased_column(u: Underscore) -> tuple[str, Underscore]:
    """
    Given an expression of the form (_.something.etc...).alias("column_name"),
    extracts the underlying expression `_.something.etc....` and the column name.
    i.e. The expected form of `u` is UnderscoreCall(UnderscoreAttr(_.something.etc...., "alias"), "column_name")
    :return: A tuiple of the column name and the underlying expression.
    """
    if not isinstance(u, UnderscoreCall):
        raise ValueError(
            f"Cannot use the given expression '{u}' as a query output -- it must be of the form x.alias('output_column_name')"
        )
    parent = u._chalk__parent
    if not isinstance(parent, UnderscoreAttr) or parent._chalk__attr != "alias":
        raise ValueError(
            f"Cannot use the given expression '{u}' as a query output -- it must be of the form x.alias('output_column_name')"
        )
    original_expr = parent._chalk__parent
    if len(u._chalk__args) != 1:
        raise ValueError(
            f"Cannot use the given expression '{u}' as a query output -- 'alias' method takes one argument, a string column name, e.g. x.alias('output_column_name')"
        )
    column_name = str(u._chalk__args[0])
    return column_name, original_expr


def encode_underscore_alias_proto(column_name: str, expr: Underscore) -> FeatureExpression:
    return FeatureExpression(
        namespace="",
        output_column_name=column_name,
        expr=expr._to_proto(),
    )


def encode_outputs(output: Sequence[Union[str, NamedUnderscoreExpr, Underscore, Any]]) -> EncodedOutputs:
    """Returns a list of encoded outputs and warnings"""
    string_outputs: List[str] = []
    feature_expressions_base64: List[str] = []
    feature_expressions_proto: List[FeatureExpression] = []
    for o in output:
        if isinstance(o, (Feature, FeatureWrapper)):
            string_outputs.append(str(o))
        elif is_features_cls(o):
            string_outputs.append(o.namespace)
        elif isinstance(o, Resolver):
            string_outputs.append(o.fqn.split(".")[-1])
        elif isinstance(o, NamedUnderscoreExpr):
            fe = encode_feature_expression_proto(o)
            feature_expressions_proto.append(fe)
            feature_expressions_base64.append(encode_feature_expression_base64(fe))
        elif isinstance(o, Underscore):
            colname, expr = parse_underscore_aliased_column(o)
            fe = encode_underscore_alias_proto(column_name=colname, expr=expr)
            feature_expressions_proto.append(fe)
            feature_expressions_base64.append(encode_feature_expression_base64(fe))
        else:
            string_outputs.append(str(o))
    return EncodedOutputs(
        string_outputs=string_outputs,
        feature_expressions_base64=feature_expressions_base64,
        feature_expressions_proto=feature_expressions_proto,
    )


def encode_named_underscore(output: NamedUnderscoreExpr) -> OutputExpression:
    """Deprecated. Construct `OutputExpression`s using `encode_outputs` instead."""
    fe = encode_feature_expression_proto(output)
    base64_proto = encode_feature_expression_base64(fe)
    return OutputExpression(
        base64_proto=base64_proto,
        python_repr=repr(output),
    )
