import logging
import os
import time

def get_logger():
    APP_NAME = os.getenv('APP_NAME', 'nsj_rest_lib')
    return logging.getLogger(APP_NAME)

def log_time(msg: str):
    """Decorator para monitoria de performance de métodos (via log)."""

    def decorator(function):
        def wrapper(*arg, **kwargs):
            t = time.perf_counter()
            res = function(*arg, **kwargs)
            get_logger().debug(
                f"{msg} - Tempo de resposta: {str(round(time.perf_counter()-t, 3))} segundos."
            )
            return res

        return wrapper

    return decorator