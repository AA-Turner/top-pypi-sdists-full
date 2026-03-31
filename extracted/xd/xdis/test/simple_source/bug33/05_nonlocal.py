# From Python 3.6 functools.py
# Bug was in detecting "nonlocal" access
def not_bug() -> bool:
    cache_token = 5

    def register() -> bool:
        nonlocal cache_token
        return cache_token == 5

    return register()

assert not_bug()
