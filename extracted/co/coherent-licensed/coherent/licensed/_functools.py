import functools


# from jaraco.functools 4.1
def compose(*funcs):
    def compose_two(f1, f2):
        return lambda *args, **kwargs: f1(f2(*args, **kwargs))

    return functools.reduce(compose_two, funcs)


def apply(transform):
    def wrap(func):
        return functools.wraps(func)(compose(transform, func))

    return wrap


def result_invoke(action):
    def wrap(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            action(result)
            return result

        return wrapper

    return wrap


def identity(x):
    return x


def bypass_when(check, *, _op=identity):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(param, /):
            return param if _op(check) else func(param)

        return wrapper

    return decorate
