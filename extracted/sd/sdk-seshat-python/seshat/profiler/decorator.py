import functools


def track(func):
    from seshat.profiler.base import profiler

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return profiler.run(func, *args, **kwargs)

    return wrapper
