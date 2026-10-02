import unittest
from abc import ABC, abstractmethod

from src.singleton import AbstractSingleton


class TestAbstractSingleton(ABC, metaclass=AbstractSingleton):
    @abstractmethod
    def __init__(self) -> None:
        pass


class TestSingleton(unittest.TestCase):
    def test_singleton(self) -> None:
        class IntSingleton(TestAbstractSingleton):
            def __init__(self, default: int = 0) -> None:
                self.i = default

        IntSingleton(10)
        a = IntSingleton()
        b = IntSingleton()

        self.assertEqual(a, b)
        self.assertEqual(id(a), id(b))
        self.assertEqual(a.i, 10)
        self.assertEqual(b.i, 10)
        a.i = 100
        self.assertEqual(b.i, 100)

        self.assertRaises(TypeError, TestAbstractSingleton)


if __name__ == "__main__":
    unittest.main()
