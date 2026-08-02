import time
import threading
from functools import wraps
from typing import Any

def cached_request(ttl_seconds: float = 300.0) -> Any:
    def decorator(func: Any) -> Any:
        cache: Any = {}
        lock = threading.Lock()

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                key = (args, frozenset(kwargs.items()))
            except TypeError:
                key = (str(args), str(kwargs))

            now = time.time()
            with lock:
                # Clean up expired cache items to prevent memory leaks
                expired_keys = [k for k, (_, exp) in cache.items() if now >= exp]
                for k in expired_keys:
                    del cache[k]

                if key in cache:
                    val, expiry = cache[key]
                    if now < expiry:
                        return val

            result = func(*args, **kwargs)

            with lock:
                cache[key] = (result, now + ttl_seconds)
            return result

        wrapper.clear_cache = lambda: cache.clear()  # type: ignore
        return wrapper
    return decorator

def rate_limit(max_calls: int, period_seconds: float = 1.0) -> Any:
    def decorator(func: Any) -> Any:
        history: Any = []
        lock = threading.Lock()

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            while True:
                now = time.time()
                with lock:
                    cutoff = now - period_seconds
                    while history and history[0] < cutoff:
                        history.pop(0)

                    if len(history) < max_calls:
                        history.append(now)
                        break
                    
                    wait_time = history[0] + period_seconds - now

                if wait_time > 0:
                    time.sleep(wait_time)

            return func(*args, **kwargs)
        return wrapper
    return decorator
