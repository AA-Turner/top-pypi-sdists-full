# decorators/deprecation.py
import functools
import warnings


def deprecated(func):
    """
    Um decorator para marcar funções como obsoletas.

    Emissão de um DeprecationWarning para a função decorada, informando que
    a mesma está obsoleta e ser removida em versões futuras.

    :param func: A função a ser decorada.
    :type func: callable
    :return: A função decorada.
    :rtype: callable
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} está obsoleta e será removida em versões futuras.",
            DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return wrapper
