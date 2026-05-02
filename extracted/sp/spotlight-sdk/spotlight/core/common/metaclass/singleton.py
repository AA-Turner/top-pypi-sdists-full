import abc


class Singleton(type):
    """
    This is a metaclass used for turning classes into singleton objects

    ref: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

    Usage:
        class FooSingleton(metaclass=Singleton):
            def __init__(self):
                self.x = 5

        foo = FooSingleton()
        foo2 = FooSingleton()

        assert foo is foo2
        assert foo.x == foo2.x
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ABCSingleton(Singleton, abc.ABCMeta):
    """
    This singleton object is used when the class or the classes parent utilizes ABC

    ref: https://stackoverflow.com/questions/57349105/python-abc-inheritance-with-specified-metaclass
    """

    pass
