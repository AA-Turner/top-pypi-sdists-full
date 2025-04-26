from functools import wraps
from typing import Callable, cast, Dict, Type, TypeVar

from typing_extensions import ParamSpec


P = ParamSpec("P")
T = TypeVar("T")


_LAZY_SDK_SINGLETONS: Dict[str, Callable] = {}


def sdk_command(
    key: str, sdk_cls: Type, *, doc_py_example: str, arg_docstrings: Dict[str, str],
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to automatically inject an `_sdk` arg into the wrapped function.

    The arguments to this class are a unique key for the singleton and its type
    (the constructor will be called with no arguments).
    """

    # The P and T type hints allow f's type hints to pass through this decorator.
    # Without them, f's type hints would not be visible to the developer.
    # See https://github.com/anyscale/product/pull/27738.
    def _inject_typed_sdk_singleton(f: Callable[P, T]) -> Callable[P, T]:
        if not doc_py_example:
            raise ValueError(
                f"SDK command '{f.__name__}' must provide a non-empty 'doc_py_example'."
            )

        # TODO: validate docstrings.

        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # We disable the mypy linter here because it treats kwargs as a
            # P.kwargs object. mypy wrongly thinks kwargs can't be indexed.
            if "_private_sdk" not in kwargs:  # type: ignore
                if key not in _LAZY_SDK_SINGLETONS:
                    _LAZY_SDK_SINGLETONS[key] = sdk_cls()

                kwargs["_private_sdk"] = _LAZY_SDK_SINGLETONS[key]  # type: ignore

            return f(*args, **kwargs)

        # TODO(edoakes): move to parsing docstrings instead.
        wrapper.__doc_py_example__ = doc_py_example  # type: ignore
        wrapper.__arg_docstrings__ = arg_docstrings  # type: ignore

        return wrapper

    return _inject_typed_sdk_singleton


def sdk_docs(
    *, doc_py_example: str, arg_docstrings: Dict[str, str],
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator to add documentation for an SDK command."""

    # The P and T type hints allow f's type hints to pass through this decorator.
    # Without them, f's type hints would not be visible to the developer.
    # See https://github.com/anyscale/product/pull/27738.
    def _add_doc_magic_attrs(f: Callable[P, T]) -> Callable[P, T]:
        if not doc_py_example:
            raise ValueError(
                f"SDK command '{f.__name__}' must provide a non-empty 'doc_py_example'."
            )

        # TODO(edoakes): validate docstrings.
        # TODO(edoakes): move to parsing docstrings instead.
        f.__doc_py_example__ = doc_py_example  # type: ignore
        f.__arg_docstrings__ = arg_docstrings  # type: ignore

        return f

    return _add_doc_magic_attrs


def sdk_command_v2(
    *, doc_py_example: str, arg_docstrings: Dict[str, str],
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Similar to `@sdk_command`, but relies on the SDK function initializing `sdk()` in the function body.

    Decorates the function with the provided `doc_py_example` and `arg_docstrings`.
    """

    def _wrap_sdk_function(f: Callable[P, T]) -> Callable[P, T]:
        if not doc_py_example:
            raise ValueError(
                f"SDK command '{f.__name__}' must provide a non-empty 'doc_py_example'."
            )

        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return f(*args, **kwargs)

        wrapper.__doc_py_example__ = doc_py_example  # type: ignore
        wrapper.__arg_docstrings__ = arg_docstrings  # type: ignore

        return wrapper

    return _wrap_sdk_function
