# From 3.6 test_abc.py
# Bug was Receiver() class definition
import abc
import unittest
class TestABCWithInitSubclass(unittest.TestCase):
    def test_works_with_init_subclass(self) -> None:
        class ReceivesClassKwargs:
            def __init_subclass__(cls, **kwargs) -> None:
                super().__init_subclass__()
        class Receiver(ReceivesClassKwargs, abc.ABC, x=1, y=2, z=3):
            pass

def test_abstractmethod_integration(self) -> None:
    for abstractthing in [abc.abstractmethod]:
        class C(metaclass=abc.ABCMeta):
            @abstractthing
            def foo(self) -> None: pass  # abstract
