import functools


def singleton(cls):
    """
    Decorator para criar uma classe singleton.

    Este decorador criará uma instância singleton da classe que é
    decorada com este decorador. A instância singleton será armazenada em um
    dicionário e reutilizada se a classe for instanciada novamente.

    :param cls: A classe a ser decorada
    :type cls: class
    :return: A instância singleton da classe
    :rtype: instância de cls
    """
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
