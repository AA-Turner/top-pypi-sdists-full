import os
import pickle
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

T = TypeVar("T")


def cache_result(cache_dir: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    os.makedirs(cache_dir, exist_ok=True)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            cache_file = os.path.join(cache_dir, f"{func.__name__}.pkl")
            if os.path.exists(cache_file):
                with open(cache_file, "rb") as f:
                    return cast(T, pickle.load(f))  # Type: ignore[no-any-return]
            result = func(*args, **kwargs)
            with open(cache_file, "wb") as f:
                pickle.dump(result, f)
            return result

        return wrapper

    return decorator
