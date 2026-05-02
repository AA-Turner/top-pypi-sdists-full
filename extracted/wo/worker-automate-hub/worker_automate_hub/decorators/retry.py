import functools
import time


def retry(max_retries=3, delay=1):
    """
    Decorador para retry em funcões.

    Args:
        max_retries (int, optional): Número máximo de tentativas. Defaults to 3.
        delay (int, optional): Tempo de espera entre tentativas. Defaults to 1.

    Returns:
        callable: Função decorada com retry.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Erro: {e}. Tentativa {retries + 1} de {max_retries}")
                    retries += 1
                    time.sleep(delay)
            raise Exception(f"Falha após {max_retries} tentativas")

        return wrapper

    return decorator
