import functools
import time


def rate_limit(calls_per_period: int, period: float) -> callable:
    """
    Um decorador que limita o número de vezes que uma função pode ser chamada em um determinado período.

    O decorador recebe dois argumentos:
    - calls_per_period: O número máximo de vezes que a função pode ser chamada em um determinado período.
    - period: O período durante o qual a função pode ser chamada.

    O decorador retorna uma função que encapsula a função original.

    A função encapsulada manterá o controle dos timestamps das últimas chamadas calls_per_period.
    Se o número de timestamps exceder calls_per_period, uma exceção será gerada.

    :param calls_per_period: O número máximo de vezes que a função pode ser chamada em um determinado período.
    :param period: O período durante o qual a função pode ser chamada.
    :return: A função decorada.
    """

    def decorator(func):
        timestamps = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal timestamps
            current_time = time.time()
            timestamps = [t for t in timestamps if current_time - t < period]
            if len(timestamps) >= calls_per_period:
                raise Exception("Limite de chamadas excedido")
            timestamps.append(current_time)
            return func(*args, **kwargs)

        return wrapper

    return decorator
