from typing import Any, Callable, Union

def main_thread(func: Callable[..., Any]) -> Callable[..., None]:
    from functools import wraps
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> None:
        try:
            from android_utils import run_on_ui_thread
            run_on_ui_thread(lambda: func(*args, **kwargs))
        except ImportError:
            func(*args, **kwargs)
    return wrapper

run_on_ui = main_thread

def background_thread(queue: Union[str, Callable[..., Any]] = "plugins", delay: int = 0) -> Any:
    def decorator(func: Callable[..., Any]) -> Callable[..., None]:
        from functools import wraps
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            try:
                from client_utils import run_on_queue, PLUGINS_QUEUE, GLOBAL_QUEUE, EXTERNAL_NETWORK_QUEUE, SEARCH_QUEUE
                q_map = {
                    "plugins": PLUGINS_QUEUE,
                    "global": GLOBAL_QUEUE,
                    "network": EXTERNAL_NETWORK_QUEUE,
                    "search": SEARCH_QUEUE
                }
                q_name = queue if isinstance(queue, str) else "plugins"
                target_queue = q_map.get(q_name, PLUGINS_QUEUE)
                run_on_queue(lambda: func(*args, **kwargs), target_queue, int(delay))
            except ImportError:
                func(*args, **kwargs)
        return wrapper

    if callable(queue):
        f = queue
        queue = "plugins"
        return decorator(f)
    return decorator

run_on_background = background_thread

def run_main(func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    try:
        from android_utils import run_on_ui_thread
        run_on_ui_thread(lambda: func(*args, **kwargs))
    except ImportError:
        func(*args, **kwargs)

def run_bg(func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    queue = kwargs.pop("queue", "plugins")
    delay = kwargs.pop("delay", 0)
    try:
        from client_utils import run_on_queue, PLUGINS_QUEUE, GLOBAL_QUEUE, EXTERNAL_NETWORK_QUEUE, SEARCH_QUEUE
        q_map = {
            "plugins": PLUGINS_QUEUE,
            "global": GLOBAL_QUEUE,
            "network": EXTERNAL_NETWORK_QUEUE,
            "search": SEARCH_QUEUE
        }
        target_queue = q_map.get(queue, PLUGINS_QUEUE)
        run_on_queue(lambda: func(*args, **kwargs), target_queue, int(delay))
    except ImportError:
        func(*args, **kwargs)
