from __future__ import annotations

import abc
import inspect
import sys
import uuid
from dataclasses import dataclass
from typing import Any, Optional, cast

import executing
import pyarrow as pa

from chalk._expression.converter import (
    convert_literal_to_proto_expr,
    convert_pa_dtype_to_proto_expr,
    convert_proto_expr_to_literal,
)
from chalk._gen.chalk.expression.v1 import expression_pb2 as expr_pb2
from chalk.features._encoding.converter import TPrimitive
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.source_parsing import should_skip_source_code_parsing

SUPPORTED_UNDERSCORE_OPS_BINARY = set("+ - * / // % ** < <= > >= == != & | ^ << >>".split())
SUPPORTED_UNDERSCORE_OPS_UNARY = set("- + ~".split())

if sys.version_info < (3, 11):
    # On python < 3.11, this can cause a significant perf regression, so we always skip parsing
    CHALK_SKIP_PRECISE_UNDERSCORE_SOURCE_COLUMN = True
else:
    CHALK_SKIP_PRECISE_UNDERSCORE_SOURCE_COLUMN = env_var_bool("CHALK_SKIP_PRECISE_UNDERSCORE_SOURCE_COLUMN")
    """
    If this environment variable is set, then `Underscore` expressions will not attempt to record their
    location within a class.

    For feature classes with thousands of members, this can add up to several seconds of validation time.
    However, if this is enabled, then error messages cannot include accurate line/column numbers for
    underscore expressions.
    """


@dataclass
class UnderscoreDefinitionLocation:
    file: str
    line: int
    column: int


def convert_value_to_proto_expr(value: Any) -> expr_pb2.LogicalExprNode:
    if isinstance(value, Underscore):
        return value._to_proto()  # pyright: ignore[reportPrivateUsage]

    return convert_literal_to_proto_expr(value)


class Underscore:
    """An unevaluated underscore expression.

    Examples
    --------
    >>> class X:
    ...     y: DataFrame[Y] = has_many(...)
    ...     s: int = _.y[_.z].sum()
    """

    def __init__(self, expr_id: Optional[str] = None):
        super().__init__()
        current_frame = inspect.currentframe()
        while current_frame is not None and current_frame.f_code.co_filename.endswith("/chalk/features/underscore.py"):
            current_frame = current_frame.f_back
        if current_frame is not None:
            definition_location = UnderscoreDefinitionLocation(
                file=current_frame.f_code.co_filename,
                line=current_frame.f_lineno,
                column=1,
                # Currently, this is just a guess, due to lack of reliable column info directly on Python frame
            )
            if not should_skip_source_code_parsing() and not CHALK_SKIP_PRECISE_UNDERSCORE_SOURCE_COLUMN:
                # Attempt to get the exact AST node to get a more-precise caller location
                # for error reporting purposes:
                source_node = executing.Source.executing(current_frame).node
                if hasattr(source_node, "lineno") and source_node.lineno is not None:  # pyright: ignore
                    definition_location.line = source_node.lineno  # pyright: ignore
                if hasattr(source_node, "col_offset") and source_node.col_offset is not None:  # pyright: ignore
                    definition_location.column = source_node.col_offset  # pyright: ignore
        else:
            definition_location = None

        self._chalk_definition_location: Optional[UnderscoreDefinitionLocation] = definition_location
        self._chalk__expr_id = expr_id if expr_id is not None else str(uuid.uuid4())

    def __getattr__(self, attr: str) -> "Underscore":
        if attr.startswith("__") or attr.startswith("_chalk__"):
            raise AttributeError(f"{self.__class__.__name__!r} {attr!r}")
        return UnderscoreAttr(self, attr)

    def __getitem__(self, key: Any) -> "Underscore":
        return UnderscoreItem(self, key)

    def __call__(self, *args: Any, **kwargs: Any) -> "Underscore":
        return UnderscoreCall(self, *args, **kwargs)

    def __add__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("+", self, other)

    def __radd__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("+", other, self)

    def __sub__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("-", self, other)

    def __rsub__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("-", other, self)

    def __mul__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("*", self, other)

    def __rmul__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("*", other, self)

    def __truediv__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("/", self, other)

    def __rtruediv__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("/", other, self)

    def __floordiv__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("//", self, other)

    def __rfloordiv__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("//", other, self)

    def __mod__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("%", self, other)

    def __rmod__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("%", other, self)

    def __pow__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("**", self, other)

    def __rpow__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("**", other, self)

    def __lt__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("<", self, other)

    def __le__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("<=", self, other)

    def __gt__(self, other: Any) -> "Underscore":
        return UnderscoreFunction(">", self, other)

    def __ge__(self, other: Any) -> "Underscore":
        return UnderscoreFunction(">=", self, other)

    def __eq__(self, other: Any) -> "Underscore":  # pyright: ignore[reportIncompatibleMethodOverride]
        return UnderscoreFunction("==", self, other)

    def __ne__(self, other: Any) -> "Underscore":  # pyright: ignore[reportIncompatibleMethodOverride]
        return UnderscoreFunction("!=", self, other)

    def __and__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("&", self, other)

    def __rand__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("&", other, self)

    def __or__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("|", self, other)

    def __ror__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("|", other, self)

    def __xor__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("^", self, other)

    def __rxor__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("^", other, self)

    def __lshift__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("<<", self, other)

    def __rlshift__(self, other: Any) -> "Underscore":
        return UnderscoreFunction("<<", other, self)

    def __rshift__(self, other: Any) -> "Underscore":
        return UnderscoreFunction(">>", self, other)

    def __rrshift__(self, other: Any) -> "Underscore":
        return UnderscoreFunction(">>", other, self)

    def __neg__(self) -> "Underscore":
        return UnderscoreFunction("negate", self)

    def __pos__(self) -> "Underscore":
        # Returning self as "+" by itself really doesn't make sense
        return self

    def __invert__(self) -> "Underscore":
        return UnderscoreFunction("~", self)

    def __hash__(self):
        # Underscores may not be hashable, so hashing the type instead. This probably won't cause a perf bomb because it's unlikely to have a hash table of underscore expressions
        return hash(type(self))

    @abc.abstractmethod
    def _is_equal(self, other: Underscore) -> bool:
        """Return whether this underscore is equal to another underscore. Normally == would provide this, but we override it to allow
        composite building over underscore expressions"""
        raise NotImplementedError

    @abc.abstractmethod
    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        raise NotImplementedError

    @classmethod
    def _from_proto(cls, node: expr_pb2.LogicalExprNode) -> Underscore | TPrimitive | pa.Scalar:
        value = cls._from_proto_dispatch(node)
        if isinstance(value, Underscore):
            if node.expr_id:
                value._chalk__expr_id = node.expr_id
        return value

    @classmethod
    def _from_proto_dispatch(cls, node: expr_pb2.LogicalExprNode) -> Underscore | TPrimitive | pa.Scalar:
        if node.HasField("identifier"):
            if node.identifier.name == "_":
                return UnderscoreRoot()
            elif node.identifier.name == "__":
                return DoubleUnderscore()
            else:
                raise ValueError(f"Unknown identifier: {node.identifier.name}")
        elif node.HasField("get_attribute"):
            parent = cls._from_proto(node.get_attribute.parent)
            if not isinstance(parent, Underscore):
                raise TypeError(f"Parent is not an underscore. Got {parent}")
            return UnderscoreAttr(
                parent=parent,
                attr=node.get_attribute.attribute.name,
            )
        elif node.HasField("get_subscript"):
            parent = cls._from_proto(node.get_subscript.parent)
            if not isinstance(parent, Underscore):
                raise TypeError(f"Parent is not an underscore. Got {parent}")
            subscripts = tuple(cls._from_proto(sub) for sub in node.get_subscript.subscript)
            if len(subscripts) > 0:
                return UnderscoreItem(parent=parent, key=subscripts)
            else:
                raise ValueError("empty subscript")
        elif node.HasField("call"):
            args = node.call.args
            if not node.call.func.HasField("identifier"):
                func = cls._from_proto(node.call.func)
                if not isinstance(func, Underscore):
                    raise TypeError(f"Func is not an underscore. Got {func}")
                return UnderscoreCall(
                    func,
                    *[cls._from_proto(arg) for arg in args],
                    _chalk__expr_id=node.expr_id,
                    **{k: cls._from_proto(v) for k, v in node.call.kwargs.items()},
                )
            func_name = node.call.func.identifier.name

            if func_name == "cast":
                # Cast is special, because it needs to have the output dtype
                if len(args) != 2:
                    raise ValueError("cast should have exactly two args -- the parent, and a pseudoarg for the dtype")
                parent = cls._from_proto(args[0])
                if not isinstance(parent, Underscore):
                    raise ValueError(f"The parent for cast should be an underscore; got {parent}")
                dest_dummy_scalar = cls._from_proto(args[1])
                if not isinstance(dest_dummy_scalar, pa.Scalar):
                    raise ValueError(f"The pseudoarg for cast should be a pyarrow scalar; got {dest_dummy_scalar}")
                return UnderscoreCast(parent, cast(pa.Scalar, dest_dummy_scalar).type)
            return UnderscoreFunction(
                func_name,
                *[cls._from_proto(arg) for arg in args],
                _chalk__expr_id=node.expr_id,
                **{k: cls._from_proto(v) for k, v in node.call.kwargs.items()},
            )
        elif node.HasField("literal_value"):
            return convert_proto_expr_to_literal(node)
        else:
            raise ValueError(f"Unknown LogicalExprNode type for underscores: {node.WhichOneof('expr_form')}")

    def __iter__(self):
        raise TypeError(f"{self.__class__.__name__} object is not iterable")


class UnderscoreRoot(Underscore):
    # _
    def __repr__(self):
        return "_"

    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        return expr_pb2.LogicalExprNode(identifier=expr_pb2.Identifier(name="_"), expr_id=self._chalk__expr_id)

    def _is_equal(self, other: Underscore):
        return isinstance(other, UnderscoreRoot)  # All root underscores are equal to each other

    @property
    def chalk_window(self):
        """Refers to the specific window being evaluated in the context of
        defining an underscore expression.

        Examples
        --------
        >>> from datetime import timedelta
        >>> from chalk.features import features
        >>> from chalk import _, Windowed, DataFrame, windowed
        >>> @features
        ... class Transaction:
        ...     id: int
        ...     user_id: "User.id"
        ...     amount: int
        >>> @features
        ... class User:
        ...     id: int
        ...     transactions: DataFrame[Transaction]
        ...     sum_amounts: Windowed[int] = windowed(
        ...         "30d", "90d",
        ...         expression=_.transactions[
        ...             _.amount,
        ...             _.ts > _.chalk_window
        ...         ].sum(),
        ...     )
        """
        return UnderscoreAttr(self, "chalk_window")

    @property
    def chalk_now(self):
        """Refers to the specific window being evaluated in the context of
        defining an underscore expression.

        Examples
        --------
        >>> from datetime import timedelta
        >>> from chalk.features import features
        >>> from chalk import _, Windowed, DataFrame, windowed
        >>> @features
        ... class Transaction:
        ...     id: int
        ...     user_id: "User.id"
        ...     amount: int
        >>> @features
        ... class User:
        ...     id: int
        ...     transactions: DataFrame[Transaction]
        ...     sum_old_amounts: int = _.transactions[
        ...         _.amount,
        ...         _.ts < _.chalk_now - timedelta(days=30),
        ...     ].sum()
        """
        return UnderscoreAttr(self, "chalk_now")

    def if_then_else(
        self,
        condition: Underscore,
        if_true: Any,
        if_false: Any,
    ) -> Underscore:
        """
        Create a conditional expression, roughly equivalent to

        ```
        if condition:
            return if_true
        else:
            return if_false
        ```

        Unlike a Python if/else, all three inputs `(condition, if_true, if_false)` are evaluated
        in parallel for all rows, and then the correct side is selected based on the result of
        the condition expression.

        Examples
        --------
        >>> from chalk import _
        >>> from chalk.features import features
        >>> @features
        ... class Transaction:
        ...    id: int
        ...    amount: int
        ...    risk_score: bool = _.if_then_else(
        ...        _.amount > 10_000,
        ...        _.amount * 0.1,
        ...        _.amount * 0.05,
        ...    )
        """
        return UnderscoreFunction("if_else", condition, if_true, if_false)


class DoubleUnderscore(Underscore):
    # __
    def __repr__(self):
        return "__"

    def _is_equal(self, other: Underscore) -> bool:
        return isinstance(other, DoubleUnderscore)  # all double underscores are equal to each other

    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        return expr_pb2.LogicalExprNode(identifier=expr_pb2.Identifier(name="__"))


class UnderscoreAttr(Underscore):
    # _.a
    def __init__(self, parent: Underscore, attr: str, *, expr_id: Optional[str] = None):
        super().__init__(expr_id)
        self._chalk__parent = parent
        self._chalk__attr = attr

    def __repr__(self):
        return f"{self._chalk__parent}.{self._chalk__attr}"

    def _is_equal(self, other: Underscore) -> bool:
        if self is other:
            return True
        if not isinstance(other, UnderscoreAttr):
            return False
        return self._chalk__parent._is_equal(other._chalk__parent) and self._chalk__attr == other._chalk__attr

    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        return expr_pb2.LogicalExprNode(
            expr_id=self._chalk__expr_id,
            get_attribute=expr_pb2.ExprGetAttribute(
                parent=convert_value_to_proto_expr(self._chalk__parent),
                attribute=expr_pb2.Identifier(name=self._chalk__attr),
            ),
        )


def _are_args_equal(x: object, y: object):
    if isinstance(x, Underscore):
        if not isinstance(y, Underscore):
            return False
        return x._is_equal(y)  # pyright: ignore[reportPrivateUsage]
    else:
        return x == y


class UnderscoreItem(Underscore):
    # _[k]
    def __init__(self, parent: Underscore, key: Any, *, expr_id: Optional[str] = None):
        super().__init__(expr_id)
        self._chalk__parent = parent
        self._chalk__key = key if isinstance(key, tuple) else (key,)

    def __repr__(self):
        keys = ", ".join(f"{key}" for key in self._chalk__key)
        return f"{self._chalk__parent}[{keys}]"

    def _is_equal(self, other: Underscore) -> bool:
        if self is other:
            return True
        if not isinstance(other, UnderscoreItem):
            return False
        if not self._chalk__parent._is_equal(other._chalk__parent):
            return False
        if len(self._chalk__key) != len(other._chalk__key):
            return False
        for x, y in zip(self._chalk__key, other._chalk__key):
            if not _are_args_equal(x, y):
                return False
        return True

    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        raw_key = self._chalk__key
        converted_keys: list[expr_pb2.LogicalExprNode] = []
        converted_keys.extend(convert_value_to_proto_expr(k) for k in raw_key)

        return expr_pb2.LogicalExprNode(
            expr_id=self._chalk__expr_id,
            get_subscript=expr_pb2.ExprGetSubscript(
                parent=convert_value_to_proto_expr(self._chalk__parent),
                subscript=converted_keys,
            ),
        )


class UnderscoreCall(Underscore):
    # _(args, kwargs)
    def __init__(self, parent: Underscore, *args: Any, _chalk__expr_id: Optional[str] = None, **kwargs: Any):
        super().__init__(_chalk__expr_id)
        self._chalk__parent = parent
        self._chalk__args = args
        self._chalk__kwargs = kwargs

    def __repr__(self):
        args: list[str] = []
        COMMA = ", "
        for arg in self._chalk__args:
            args.append(f"{arg}")
        for key, arg in self._chalk__kwargs.items():
            args.append(f"{key}={arg}")
        return f"{self._chalk__parent}({COMMA.join(args)})"

    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        args = [convert_value_to_proto_expr(arg) for arg in self._chalk__args]
        kwargs = {k: convert_value_to_proto_expr(v) for k, v in self._chalk__kwargs.items()}
        return expr_pb2.LogicalExprNode(
            expr_id=self._chalk__expr_id,
            call=expr_pb2.ExprCall(
                func=convert_value_to_proto_expr(self._chalk__parent),
                args=args,
                kwargs=kwargs,
            ),
        )

    def _is_equal(self, other: Underscore) -> bool:
        if self is other:
            return True
        if not isinstance(other, UnderscoreCall):
            return False
        if not self._chalk__parent._is_equal(other._chalk__parent):
            return False

        if len(self._chalk__args) != len(other._chalk__args):
            return False
        for x, y in zip(self._chalk__args, other._chalk__args):
            if not _are_args_equal(x, y):
                return False

        if len(self._chalk__kwargs) != len(other._chalk__kwargs):
            return False
        for k, x in self._chalk__kwargs.items():
            if k not in other._chalk__kwargs:
                return False
            y = other._chalk__kwargs[k]

            if not _are_args_equal(x, y):
                return False
        return True


def coerce_dtype_args_to_scalar(arg: Any) -> Any:
    """
    Currently Chalk underscore gRPC can only transport scalars, so we need to convert any dtype arguments to a pa.scalar.
    """

    if isinstance(arg, pa.DataType):
        return pa.scalar(None, arg)
    return arg


class UnderscoreFunction(Underscore):
    __name__ = "function"

    def __init__(self, name: str, *args: Any, _chalk__expr_id: Optional[str] = None, **kwargs: Any):
        super().__init__(_chalk__expr_id)
        self._chalk__args = args
        self._chalk__kwargs = kwargs
        self._chalk__args = [coerce_dtype_args_to_scalar(arg) for arg in args]

        self._chalk__function_name = name

    def __repr__(self):
        if self._chalk__function_name in SUPPORTED_UNDERSCORE_OPS_UNARY and len(self._chalk__args) == 1:
            return f"({self._chalk__function_name} {self._chalk__args[0]!r})"
        if self._chalk__function_name in SUPPORTED_UNDERSCORE_OPS_BINARY and len(self._chalk__args) == 2:
            return f"({self._chalk__args[0]!r} {self._chalk__function_name} {self._chalk__args[1]!r})"
        else:
            fn: list[str] = [f"_.{self._chalk__function_name}("]
            fn.append(", ".join(repr(x) for x in self._chalk__args))
            if self._chalk__args and self._chalk__kwargs:
                fn.append(", ")
            fn.append(", ".join(f"{k}={v!r}" for k, v in self._chalk__kwargs.items()))
            fn.append(")")
            return "".join(fn)

    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        return expr_pb2.LogicalExprNode(
            expr_id=self._chalk__expr_id,
            call=expr_pb2.ExprCall(
                func=expr_pb2.LogicalExprNode(identifier=expr_pb2.Identifier(name=self._chalk__function_name)),
                args=[convert_value_to_proto_expr(x) for x in self._chalk__args],
                kwargs={k: convert_value_to_proto_expr(v) for (k, v) in self._chalk__kwargs.items()},
            ),
        )

    def _is_equal(self, other: Underscore) -> bool:
        if self is other:
            return True
        if not isinstance(other, UnderscoreFunction):
            return False
        if self._chalk__function_name != other._chalk__function_name:
            return False

        if len(self._chalk__args) != len(other._chalk__args):
            return False
        for x, y in zip(self._chalk__args, other._chalk__args):
            if not _are_args_equal(x, y):
                return False

        if len(self._chalk__kwargs) != len(other._chalk__kwargs):
            return False
        for k, x in self._chalk__kwargs.items():
            if k not in other._chalk__kwargs:
                return False
            y = other._chalk__kwargs[k]

            if not _are_args_equal(x, y):
                return False
        return True

    def __bool__(self):
        # because __eq__ is overridden, `if underscore_1 == underscore_2: ...` would always return True
        # To fix that, we'll manually override bool for the case when the expression is an UnderscoreFunction and the operator is == or !=
        if self._chalk__function_name == "==":
            lhs = self._chalk__args[0]
            rhs = self._chalk__args[1]
            return _are_args_equal(lhs, rhs)
        if self._chalk__function_name == "!=":
            lhs = self._chalk__args[0]
            rhs = self._chalk__args[1]
            return not _are_args_equal(lhs, rhs)
        # Ideally, we would raise, but this causes issues when using the ast-parsing syntax like
        # cheap_and_good_tacos = df[_.price <= 12 and _.rating >= 4.0]
        # Retuning True to match the default behavior of python's __bool__
        return True


class UnderscoreCast(Underscore):
    __name__ = "cast"
    __qualname__ = "chalk.functions.cast"

    def __init__(self, value: Underscore, to_type: pa.DataType, *, expr_id: Optional[str] = None):
        super().__init__(expr_id)
        self._chalk__value = value
        self._chalk__to_type = to_type

    def _is_equal(self, other: Underscore) -> bool:
        if self is other:
            return True
        if not isinstance(other, UnderscoreCast):
            return False
        if not self._chalk__value._is_equal(other._chalk__value):
            return False
        if self._chalk__to_type != other._chalk__to_type:
            return False
        return True

    def __repr__(self):
        return f"chalk.functions.cast({self._chalk__value}, {self._chalk__to_type})"

    def _to_proto(self) -> expr_pb2.LogicalExprNode:
        return expr_pb2.LogicalExprNode(
            expr_id=self._chalk__expr_id,
            call=expr_pb2.ExprCall(
                func=expr_pb2.LogicalExprNode(identifier=expr_pb2.Identifier(name="cast")),
                args=[
                    convert_value_to_proto_expr(self._chalk__value),
                    convert_pa_dtype_to_proto_expr(self._chalk__to_type),
                ],
            ),
        )


_ = underscore = UnderscoreRoot()
__ = DoubleUnderscore()

# NEED `__all__` because `_` is private and can't be auto-imported by i.e. IntelliJ.
__all__ = (
    "SUPPORTED_UNDERSCORE_OPS_BINARY",
    "SUPPORTED_UNDERSCORE_OPS_UNARY",
    "Underscore",
    "UnderscoreAttr",
    "UnderscoreCall",
    "UnderscoreCast",
    "UnderscoreFunction",
    "UnderscoreItem",
    "UnderscoreRoot",
    "_",
    "__",
    "underscore",
)
