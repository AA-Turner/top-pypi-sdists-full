# pyright: reportPrivateUsage = false

from __future__ import annotations

import dataclasses
import warnings
from typing import Any, Tuple, Type, Union

import typing_extensions

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.filter import Filter
from chalk.features.underscore import (
    SUPPORTED_UNDERSCORE_OPS_BINARY,
    SUPPORTED_UNDERSCORE_OPS_UNARY,
    DoubleUnderscore,
    Underscore,
    UnderscoreAttr,
    UnderscoreCall,
    UnderscoreCast,
    UnderscoreFunction,
    UnderscoreItem,
    UnderscoreRoot,
)
from chalk.utils.missing_dependency import missing_dependency_exception

if typing_extensions.TYPE_CHECKING:
    from chalk import Features

try:
    import polars as pl
except ModuleNotFoundError:
    pl = None


SUPPORTED_ARITHMETIC_OPS = {"+", "-", "*", "/", "//", "%", "**"}


def parse_underscore_in_context(exp: Underscore, context: Any, is_pydantic: bool = False) -> Any:
    """
    Parse a (potentially underscore) expression passed in under some "context".
    """
    parsed_exp = _parse_underscore_in_context(
        exp=exp,
        context=context,
        is_pydantic=is_pydantic,
    )
    assert not isinstance(parsed_exp, Underscore)
    return parsed_exp


def _parse_underscore_in_context(exp: Any, context: Any, is_pydantic: bool) -> Any:
    # Features of the dataframe are to be written as a dictionary of the fqn split up mapped to
    # the original features. The dictionary is represented immutably here.
    if not isinstance(exp, Underscore):
        # Recursive call hit non-underscore, deal with later
        return exp

    elif isinstance(exp, UnderscoreRoot):
        return context

    elif isinstance(exp, UnderscoreAttr):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        attr = exp._chalk__attr
        from chalk.features.dataframe import DataFrame

        if isinstance(parent_context, DataFrame) and is_pydantic:
            if attr not in parent_context._underlying.schema:
                warnings.warn(
                    f"Attribute {attr} not found in dataframe schema. Returning None. Found expression {exp}."
                )
                return None

            return attr
        else:
            return getattr(parent_context, attr)

    elif isinstance(exp, UnderscoreItem):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        key = exp._chalk__key
        return parent_context[key]

    elif isinstance(exp, UnderscoreCall):
        raise NotImplementedError(
            f"Calls on underscores in DataFrames is currently unsupported. Found expression {exp}"
        )

    elif isinstance(exp, UnderscoreFunction):
        if exp._chalk__function_name in SUPPORTED_UNDERSCORE_OPS_BINARY:
            if len(exp._chalk__args) != 2:
                raise ValueError(
                    f"Binary operation '{exp._chalk__function_name}' requires 2 operands; got {len(exp._chalk__args)} operands: {exp._chalk__args!r}"
                )
            left_val = exp._chalk__args[0]
            if isinstance(left_val, Underscore):
                left = _parse_underscore_in_context(exp=left_val, context=context, is_pydantic=is_pydantic)
            else:
                # The left value might be a literal, like `1` or `"::"` or `None`.
                left = left_val

            right_val = exp._chalk__args[1]
            if isinstance(right_val, Underscore):
                right = _parse_underscore_in_context(exp=right_val, context=context, is_pydantic=is_pydantic)
            else:
                # The right value might be a literal, like `1` or `"::"` or `None`.
                right = right_val

            if exp._chalk__function_name in SUPPORTED_ARITHMETIC_OPS:
                return _eval_arithmetic_expression(left, right, exp._chalk__function_name)
            else:
                return _eval_expression(left, right, exp._chalk__function_name)

        if exp._chalk__function_name in SUPPORTED_UNDERSCORE_OPS_UNARY:
            operand = _parse_underscore_in_context(exp=exp._chalk__args[0], context=context, is_pydantic=is_pydantic)
            return eval(f"{exp._chalk__function_name} operand", globals(), {"operand": operand})

    raise NotImplementedError(f"Unrecognized underscore expression {exp}")


def _unwrap_and_validate_features(left: FeatureWrapper, right: FeatureWrapper) -> Tuple[Feature, Feature]:
    f_left = unwrap_feature(left)
    f_right = unwrap_feature(right)

    if f_left.root_namespace != f_right.root_namespace:
        raise TypeError(
            f"{f_left} and {f_right} belong to different namespaces. Operations can only be performed on features of the same namespace."
        )

    return f_left, f_right


def _eval_expression(left: Union[FeatureWrapper, Filter], right: Any, op: str):
    try:
        if op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "&":
            return left & right
        elif op == "|":
            return left | right
        elif op == "__getitem__":
            assert isinstance(left, FeatureWrapper)
            return left[right]
        elif op == "__getattr__":
            return getattr(left, right)
    except:
        raise NotImplementedError(
            f"Operation {op} not implemented for {type(left).__name__} and {type(right).__name__}"
        )


def _eval_arithmetic_expression(
    left: Union[FeatureWrapper, float, int],
    right: Union[FeatureWrapper, float, int],
    op: str,
):
    if pl is None:
        raise missing_dependency_exception("chalkpy[runtime]")

    if isinstance(left, FeatureWrapper) and isinstance(right, FeatureWrapper):
        # If both are features, ensure they are in the same namespace
        _unwrap_and_validate_features(left, right)

    if isinstance(left, FeatureWrapper):
        left_col = pl.col(str(left))
    else:
        left_col = pl.lit(left)

    if isinstance(right, FeatureWrapper):
        right_col = pl.col(str(right))
    else:
        right_col = pl.lit(right)

    if op == "+":
        return left_col + right_col
    elif op == "-":
        return left_col - right_col
    elif op == "*":
        return left_col * right_col
    elif op == "/":
        return left_col / right_col
    elif op == "//":
        return left_col // right_col
    elif op == "%":
        return left_col % right_col
    elif op == "**":
        return left_col**right_col

    raise NotImplementedError(f"{op} is not implemented")


@dataclasses.dataclass
class NamedUnderscoreExpr:
    """
    Associated a name with an underscore expression. Used to simulate 'creating' features in notebooks that can then be referred to in queries on the engine.
    """

    fqn: str
    short_name: str
    expr: Underscore

    def __str__(self):
        return f"{self.expr} as _.{self.short_name}"


@dataclasses.dataclass(frozen=True)
class NamedUnderscoreParseContext:
    current_namespace: str
    current_substitutions: tuple[str, ...]  # Each element is the fqn of a NamedUnderscoreExpression

    def with_substitution(self, new_expr: NamedUnderscoreExpr) -> NamedUnderscoreParseContext:
        return dataclasses.replace(self, current_substitutions=self.current_substitutions + (new_expr.fqn,))

    def with_namespace(self, new_namespace: str):
        return dataclasses.replace(self, current_namespace=new_namespace)


def process_named_underscore_expr(expr: NamedUnderscoreExpr):
    namespace = expr.fqn.split(".")[0]
    return _process_named_underscore_expr(
        expr=expr.expr, ctx=NamedUnderscoreParseContext(current_namespace=namespace, current_substitutions=tuple())
    )


def _process_named_underscore_expr(*, expr: Any, ctx: NamedUnderscoreParseContext):
    if isinstance(expr, NamedUnderscoreExpr):
        # Special case for if a user writes `FClass.some_new_feat` instead of `_.some_new_feat` in an expr
        # TODO check namespace here? `Rectangle.area = _.width * Square.height` is no good.
        return _process_named_underscore_expr(expr=expr.expr, ctx=ctx)

    if not isinstance(expr, Underscore):
        # If it's not an Underscore, return as-is
        return expr

    elif isinstance(expr, UnderscoreRoot):
        return expr
    elif isinstance(expr, UnderscoreAttr):
        parent_processed = _process_named_underscore_expr(expr=expr._chalk__parent, ctx=ctx)
        attr = expr._chalk__attr
        # For _.a.b.c, 'c' is in the namespace of "B" instead of the root namespace
        parent_namespace = get_namespace_of_underscore_expr(ctx.current_namespace, parent_processed)
        if parent_namespace is not None:
            if (named_expr := parent_namespace.__chalk_notebook_feature_expressions__.get(attr)) is not None:
                if named_expr.fqn in ctx.current_substitutions:
                    names = ctx.current_substitutions + (named_expr.fqn,)
                    cycle_str = " > ".join(names)
                    raise ValueError(
                        f"Circular reference when substituting locally-defined expressions with existing features: {cycle_str}"
                    )
                return _process_named_underscore_expr(
                    expr=named_expr.expr,
                    ctx=ctx.with_substitution(named_expr).with_namespace(parent_namespace.namespace),
                )
        return UnderscoreAttr(parent=parent_processed, attr=attr, expr_id=expr._chalk__expr_id)
    elif isinstance(expr, UnderscoreItem):
        # For _.a[_.b], b is a feature of the namespace of A
        parent_processed = _process_named_underscore_expr(expr=expr._chalk__parent, ctx=ctx)
        parent_namespace = get_namespace_of_underscore_expr(ctx.current_namespace, parent_processed)
        nested_ctx = ctx.with_namespace(parent_namespace.namespace) if parent_namespace is not None else ctx
        key_processed = tuple(_process_named_underscore_expr(expr=k, ctx=nested_ctx) for k in expr._chalk__key)
        return UnderscoreItem(parent=parent_processed, key=key_processed, expr_id=expr._chalk__expr_id)
    elif isinstance(expr, UnderscoreCall):
        parent_processed = _process_named_underscore_expr(expr=expr._chalk__parent, ctx=ctx)
        kwargs_processed = {k: _process_named_underscore_expr(expr=v, ctx=ctx) for k, v in expr._chalk__kwargs.items()}
        args_processed = [_process_named_underscore_expr(expr=a, ctx=ctx) for a in expr._chalk__args]
        return UnderscoreCall(
            parent=parent_processed, *args_processed, _chalk__expr_id=expr._chalk__expr_id, **kwargs_processed
        )
    elif isinstance(expr, UnderscoreFunction):
        kwargs_processed = {k: _process_named_underscore_expr(expr=v, ctx=ctx) for k, v in expr._chalk__kwargs.items()}
        args_processed = [_process_named_underscore_expr(expr=a, ctx=ctx) for a in expr._chalk__args]
        return UnderscoreFunction(
            expr._chalk__function_name, *args_processed, _chalk__expr_id=expr._chalk__expr_id, **kwargs_processed
        )
    elif isinstance(expr, UnderscoreCast):
        value_processed = _process_named_underscore_expr(expr=expr._chalk__value, ctx=ctx)
        return UnderscoreCast(to_type=expr._chalk__to_type, value=value_processed, expr_id=expr._chalk__expr_id)
    elif isinstance(expr, DoubleUnderscore):
        return expr

    raise NotImplementedError(f"Unrecognized underscore expression {expr}")


def get_namespace_of_underscore_expr(root_namespace: str, expr: Underscore) -> Type[Features] | None:
    if isinstance(expr, UnderscoreRoot):
        from chalk.features import FeatureSetBase

        return FeatureSetBase.registry.get(root_namespace)
    elif isinstance(expr, UnderscoreAttr):
        new_ns = get_namespace_of_underscore_expr(root_namespace, expr._chalk__parent)
        if new_ns is None:
            return None
        feat = None
        for x in new_ns.features:
            if x.name == expr._chalk__attr:
                feat = x
                break
        if feat is None:
            return None
        if feat.is_has_one:
            return feat.typ.as_features_cls()
        elif feat.is_has_many:
            df = feat.typ.as_dataframe()
            return df.references_feature_set if df is not None else None
    elif isinstance(expr, UnderscoreItem):
        # _.a[_.stuff] has the same namespace as _.a
        return get_namespace_of_underscore_expr(root_namespace, expr._chalk__parent)
    return None
