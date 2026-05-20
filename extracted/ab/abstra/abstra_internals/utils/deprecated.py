from functools import wraps
from typing import Callable, Optional, Tuple


def deprecated(new_function: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(
                f"[WARNING] Function '{func.__name__}' is deprecated. Please use '{new_function}' instead."
            )
            return func(*args, **kwargs)

        setattr(wrapper, "__is_deprecated__", True)
        setattr(wrapper, "__new_function__", new_function)
        return wrapper

    return decorator


def deprecated_kwarg(*pairs: Tuple[str, Optional[str]]):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for old, new in pairs:
                if old not in kwargs:
                    continue
                if new is None:
                    print(
                        f"[WARNING] Parameter '{old}' of function '{func.__name__}' is deprecated, avoid using it."
                    )
                    continue
                if new in kwargs:
                    raise Exception(
                        f"Cannot pass both '{new}' and '{old}' to '{func.__name__}'; use '{new}'."
                    )
                print(
                    f"[WARNING] Parameter '{old}' of function '{func.__name__}' is deprecated. Please use '{new}' instead."
                )
                kwargs[new] = kwargs.pop(old)
            return func(*args, **kwargs)

        setattr(wrapper, "__has_deprecated_kwarg__", True)
        setattr(wrapper, "__deprecated_kwargs__", tuple(pairs))
        return wrapper

    return decorator
