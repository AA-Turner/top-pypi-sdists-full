import abc
from pysingleton import PySingleton


class ABCSingleton(abc.ABCMeta, PySingleton):
    pass
