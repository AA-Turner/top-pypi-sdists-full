from __future__ import annotations

import inspect
import sys
import types
from collections.abc import Mapping, Sequence, Set as ABCSet
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    TypeVar,
)

from seeq.spy._errors import SPyTypeError

_NONE_TYPE = type(None)


def _safe_get_type_hints(func: Callable) -> Dict[str, object]:
    # Get the module where the function is defined to use its globals for evaluation
    # This "globalns" variable is needed for the get_type_hints() function
    # noinspection PyUnresolvedReferences
    globalns = getattr(sys.modules.get(func.__module__, None), '__dict__', {})

    try:
        return get_type_hints(func, globalns=globalns, include_extras=True)  # py>=3.9
    except TypeError as e:
        # Python 3.8 doesn't have include_extras parameter
        try:
            return get_type_hints(func, globalns=globalns)  # py<=3.8 behavior
        except Exception as inner_e:
            # noinspection PyUnresolvedReferences
            raise SPyTypeError(
                f"Failed to resolve type hints for function {func.__module__}.{func.__qualname__}. "
                f"This is likely due to missing imports or forward references that can't be evaluated. "
                f"Original error: {inner_e}"
            ) from inner_e
    except Exception as e:
        # noinspection PyUnresolvedReferences
        raise SPyTypeError(
            f"Failed to resolve type hints for function {func.__module__}.{func.__qualname__}. "
            f"This is likely due to missing imports or forward references that can't be evaluated. "
            f"Original error: {e}"
        ) from e


def _is_runtime_type(tp: object) -> bool:
    try:
        return isinstance(tp, type)
    except Exception:
        return False


def _type_name(tp: object, for_union: bool = False) -> str:
    try:
        # types and classes
        if _is_runtime_type(tp):
            return tp.__name__  # type: ignore[attr-defined]

        # Special handling for Union types
        origin = get_origin(tp)
        args = get_args(tp)
        if origin is Union and args:
            # Filter out NoneType for readability
            non_none_args = [arg for arg in args if arg not in (_NONE_TYPE, type(None))]

            # If only one non-None type remains, just show that type
            if len(args) == 2 and len(non_none_args) == 1:
                # This is Optional[T], return just T's name
                return _type_name(non_none_args[0], for_union=for_union)

            # For Union with multiple non-None types, format as "X or Y or Z"
            if len(non_none_args) > 1:
                type_names = []
                for arg in non_none_args:
                    # When formatting union alternatives, always show full generic types
                    name = _type_name(arg, for_union=True)
                    type_names.append(name)
                return ' or '.join(type_names)

        # For generic types like List[str], Dict[str, int]
        if origin is not None and _is_runtime_type(origin):
            if for_union and args:
                # Show full generic type for Union error messages
                result = str(tp).replace('typing.', '')
                return result
            else:
                # Show just the origin type name for container mismatch errors
                return origin.__name__  # type: ignore[attr-defined]

        # Convert to string and clean up typing module prefixes for readability
        result = str(tp)
        # For Optional[X], strip Optional wrapper to show just X
        if 'Optional[' in result:
            # Extract the inner type from Optional[X]
            start = result.find('Optional[') + 9
            # Find matching closing bracket
            depth = 1
            i = start
            while i < len(result) and depth > 0:
                if result[i] == '[':
                    depth += 1
                elif result[i] == ']':
                    depth -= 1
                i += 1
            if depth == 0:
                result = result[start:i - 1]
        result = result.replace('typing.', '')
        return result
    except Exception:
        return repr(tp)


def _format_value_type(value: object) -> str:
    try:
        return type(value).__name__
    except Exception:
        return "<unknown>"


def _append(errors: List[str], path: str, expected: object, value: object, why: Union[str, None] = None,
            for_union: bool = False) -> None:
    msg = f"Argument '{path}' should be type {_type_name(expected, for_union=for_union)}, but is type {_format_value_type(value)}"
    if why:
        msg += f" ({why})"
    errors.append(msg)


def _check(value: object, expected: object, path: str, errors: List[str]) -> None:
    # No annotation / Any => accept
    if expected is inspect._empty or expected is Any:
        return

    # Handle typing.ForwardRef already resolved by get_type_hints in normal cases.
    # Still, guard against odd cases.
    if expected is None:
        if value is not None:
            _append(errors, path, expected, value)
        return

    # NewType support: expected.__supertype__
    supertype = getattr(expected, "__supertype__", None)
    if supertype is not None:
        _check(value, supertype, path, errors)
        return

    origin = get_origin(expected)
    args = get_args(expected)

    # Annotated[T, ...] => validate T
    annotated_type = getattr(__import__("typing"), "Annotated", None)
    if annotated_type is not None and origin is annotated_type:
        if args:
            _check(value, args[0], path, errors)
        return

    # Literal
    if origin is Literal:
        if value not in args:
            _append(errors, path, expected, value, why=f"allowed values: {args!r}")
        return

    # TypeVar
    if isinstance(expected, TypeVar):
        # If constrained, accept if matches any constraint
        if expected.__constraints__:
            for c in expected.__constraints__:
                tmp: List[str] = []
                _check(value, c, path, tmp)
                if not tmp:
                    return
            _append(errors, path, expected, value, why=f"constraints: {expected.__constraints__!r}")
            return
        # If bounded, validate against the bound
        if expected.__bound__ is not None:
            _check(value, expected.__bound__, path, errors)
        # Else unconstrained TypeVar => can't validate
        return

    # Union / Optional / PEP 604 (A | B)
    # In 3.10+, get_origin(int | str) is types.UnionType; in typing.Union it's typing.Union
    union_types = tuple(
        t for t in (getattr(types, "UnionType", None), getattr(__import__("typing"), "Union", None)) if t is not None)
    if origin in union_types:
        # Accept if any branch accepts
        best_errors: List[str] = []
        for alt in args:
            tmp: List[str] = []
            _check(value, alt, path, tmp)
            if not tmp:
                return
            # Keep track of the best (most specific) error - prefer errors from non-None types
            if not best_errors or (len(tmp) <= len(best_errors) and alt is not _NONE_TYPE):
                best_errors = tmp

        # If the best error is more specific (has a path like "items[0]"), use it
        # Otherwise, generate a Union-level error message
        if best_errors and '[' in best_errors[0]:
            # This is a nested error (e.g., "items[0] should be..."), use it as-is
            errors.extend(best_errors)
        else:
            # Top-level Union mismatch, show all alternatives in error message
            _append(errors, path, expected, value, for_union=True)
        return

    # NoneType
    if expected is _NONE_TYPE:
        if value is not None:
            _append(errors, path, expected, value)
        return

    # typing.Type[T] => a class object that is subclass of T
    if origin is type:
        if not isinstance(value, type):
            _append(errors, path, expected, value, why="value is not a class/type")
            return
        # If parametrized, enforce subclass check
        if args:
            target = args[0]
            target_origin = get_origin(target) or target
            if _is_runtime_type(target_origin):
                if not issubclass(value, target_origin):  # type: ignore[arg-type]
                    _append(errors, path, expected, value, why=f"not a subclass of {_type_name(target_origin)}")
            # else: can't strict-check
        return

    # Callable[...] => only check callability (signature/arg types are not reliably enforceable at runtime)
    if origin is Callable or expected is Callable:
        if not callable(value):
            _append(errors, path, expected, value, why="not callable")
        return

    # Builtin generics: list[T], set[T], frozenset[T]
    if origin in (list, set, frozenset):
        if not isinstance(value, origin):
            _append(errors, path, expected, value)
            return
        elem_t = args[0] if args else Any
        for i, v in enumerate(value):  # type: ignore[assignment]
            _check(v, elem_t, f"{path}[{i}]", errors)
        return

    # tuple[T1, T2] or tuple[T, ...]
    if origin is tuple:
        if not isinstance(value, tuple):
            _append(errors, path, expected, value)
            return
        if not args:
            return
        # tuple[T, ...]
        if len(args) == 2 and args[1] is Ellipsis:
            elem_t = args[0]
            for i, v in enumerate(value):
                _check(v, elem_t, f"{path}[{i}]", errors)
            return
        # tuple[T1, T2, ...]
        if len(value) != len(args):
            _append(errors, path, expected, value, why=f"tuple length {len(value)} != {len(args)}")
            return
        for i, (v, t) in enumerate(zip(value, args)):
            _check(v, t, f"{path}[{i}]", errors)
        return

    # dict[K, V]
    if origin is dict:
        if not isinstance(value, dict):
            _append(errors, path, expected, value)
            return
        k_t, v_t = args if len(args) == 2 else (Any, Any)
        for k, v in value.items():
            _check(k, k_t, f"{path}.keys()", errors)
            _check(v, v_t, f"{path}[{k!r}]", errors)
        return

    # collections.abc generics (Mapping[K,V], Sequence[T], Set[T], etc.)
    # We do a best-effort isinstance check against the origin, then optionally validate elements.
    if origin is not None:
        try:
            if not isinstance(value, origin):  # type: ignore[arg-type]
                _append(errors, path, expected, value)
                return
        except TypeError:
            # Not runtime-checkable (e.g., Protocol without @runtime_checkable)
            # Best-effort: don't fail hard.
            return

        # Element checking for common ABCs:
        # Mapping[K,V]
        if isinstance(value, Mapping):
            if len(args) >= 2:
                k_t, v_t = args[0], args[1]
                for k, v in value.items():
                    _check(k, k_t, f"{path}.keys()", errors)
                    _check(v, v_t, f"{path}[{k!r}]", errors)
            return

        # Avoid treating str/bytes as sequences of elements unless explicitly annotated as such
        if isinstance(value, (str, bytes, bytearray)):
            return

        # Sequence[T]
        if isinstance(value, Sequence):
            if args:
                elem_t = args[0]
                # Only iterate if it's finite / indexable; Sequence is indexable by contract.
                for i, v in enumerate(value):
                    _check(v, elem_t, f"{path}[{i}]", errors)
            return

        # Set[T]
        if isinstance(value, ABCSet):
            if args:
                elem_t = args[0]
                for v in value:
                    _check(v, elem_t, f"{path}[*]", errors)
            return

    # Plain class/type
    if _is_runtime_type(expected):
        # Special case: bool is subclass of int in Python, but for type validation
        # we want to treat them as distinct types
        if expected is int and isinstance(value, bool):
            _append(errors, path, expected, value)
            return
        if not isinstance(value, expected):  # type: ignore[arg-type]
            _append(errors, path, expected, value)
        return

    # Last resort: try isinstance, but never crash due to typing objects
    try:
        if not isinstance(value, expected):  # type: ignore[arg-type]
            _append(errors, path, expected, value)
    except TypeError:
        # Not runtime-checkable; skip
        return


def get_spy_function_name(func: Callable) -> str:
    # noinspection PyUnresolvedReferences
    function_name = f"{func.__module__}.{func.__qualname__}"
    function_name_parts = function_name.split(".")
    function_name_parts_filtered = [n for n in function_name_parts if n != "seeq" and not n.startswith('_')]
    return ".".join(function_name_parts_filtered)


def validate_argument_types(func: Callable, args: tuple, kwargs: Dict) -> None:
    if kwargs is None:
        kwargs = {}

    sig = inspect.signature(func)
    hints = _safe_get_type_hints(func)

    # Bind args/kwargs to the signature (this enforces correct call shape)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()

    # Check for missing type hints (developer error detection)
    missing_hints = []
    for name, param in sig.parameters.items():
        # Skip 'self' and 'cls' parameters (they don't need type hints)
        if name in ('self', 'cls'):
            continue

        # Get the annotation for this parameter
        annotation = hints.get(name,
                               param.annotation if param.annotation is not inspect.Parameter.empty else inspect._empty)

        # Check if the parameter is missing a type hint
        if annotation is inspect._empty:
            missing_hints.append(name)

    if missing_hints:
        # noinspection PyUnresolvedReferences
        raise TypeError(
            f"Function {func.__module__}.{func.__qualname__} is missing type hints for parameters: {', '.join(missing_hints)}. "
            f"All parameters must have type hints for validation to work properly."
        )

    errors: List[str] = []

    log_message = [f'{get_spy_function_name(func)}() called with arguments:']

    # Validate each bound argument
    for name, value in bound.arguments.items():
        try:
            log_message.append(f'    {name} = {value!r}')
        except Exception:
            log_message.append(f'    {name} = <unrepresentable value> (type: {_format_value_type(value)})')

        expected = hints.get(name, sig.parameters[name].annotation if name in sig.parameters else inspect._empty)

        # If parameter is *args / **kwargs, validate appropriately:
        param = sig.parameters.get(name)
        if param is not None and param.kind is inspect.Parameter.VAR_POSITIONAL:
            # Annotation is the element type for *args
            elem_expected = expected
            for i, v in enumerate(value):
                _check(v, elem_expected, f"*{name}[{i}]", errors)
            continue

        if param is not None and param.kind is inspect.Parameter.VAR_KEYWORD:
            # Annotation is the value type for **kwargs
            val_expected = expected
            for k, v in value.items():
                _check(v, val_expected, f"**{name}[{k!r}]", errors)
            continue

        _check(value, expected, name, errors)

    if errors:
        # Raise the first error as SPyTypeError (for backward compatibility with test expectations)
        raise SPyTypeError(errors[0])

    if bound.arguments.get('status') is not None:
        bound.arguments['status'].log("\n".join(log_message))
