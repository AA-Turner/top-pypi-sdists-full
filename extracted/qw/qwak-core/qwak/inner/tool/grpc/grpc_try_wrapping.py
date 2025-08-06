import grpc
from qwak.exceptions import QwakException


def grpc_try_catch_wrapper(exception_message):
    def decorator(function):
        def _inner_wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except grpc.RpcError as e:
                raise QwakException(exception_message + f". Error is: {e}.")

        return _inner_wrapper

    return decorator
