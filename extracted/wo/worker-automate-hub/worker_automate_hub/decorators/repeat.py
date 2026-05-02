import functools
import time


def repeat(times=5, delay=15):
    """
    Decorador para repetir uma função um número específico de vezes.

    Args:
        times (int, optional): Número de repetições. Defaults to 5.

    Returns:
        callable: Função decorada que é chamada repetidamente.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                result = await func(*args, **kwargs)
                time.sleep(delay)
            return result

        return wrapper

    return decorator
