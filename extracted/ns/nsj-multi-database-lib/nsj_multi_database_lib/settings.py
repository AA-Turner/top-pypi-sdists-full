import logging
import os
import time

MULTIDATABASE_API_URL = os.getenv(
    "MULTIDATABASE_API_URL", "https://api.nasajon.com.br/multidb-api/v1/erp/credentials"
)


def get_logger():
    APP_NAME = os.getenv("APP_NAME", "nsj_multi_database_lib")
    return logging.getLogger(APP_NAME)


def get_crypt_key():
    if CRYPT_KEY is None:
        raise Exception("Faltando chave de criptografia")

    return CRYPT_KEY.encode()


CRYPT_KEY = os.getenv("CRYPT_KEY", None)
if CRYPT_KEY is None:
    get_logger().warning(
        "Faltando chave de criptografia na variável de ambiente: CRYPT_KEY"
    )


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
