import functools
from collections.abc import Callable


def hybrid_syntax(decorator: Callable) -> Callable:
    """
    Enhances a decorator to support both parameterized and non-parameterized usage.

    This allows the decorator to be used as either:

    - ``@decorator`` (equivalent to ``@decorator()``)
    - ``@decorator(...)`` with parameters.

    Args:
        decorator (Callable): The decorator to enhance.

    Returns:
        Callable: The modified decorator supporting both usages.
    """

    @functools.wraps(decorator)
    def wrapper(*dec_args, **dec_kwargs) -> Callable:
        # Check if @decorator syntax is used: the first argument is the function to decorate.
        if len(dec_args) == 1 and callable(dec_args[0]):
            return decorator()(dec_args[0])

        # Otherwise, @decorator(...) syntax is used: pass parameters to the decorator.
        return decorator(*dec_args, **dec_kwargs)

    return wrapper
