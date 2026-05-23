import ast
import unittest

from abstra_internals.repositories.linter.rules.main_block_in_stage import (
    MainBlockInStage,
)


class TestMainBlockInStage(unittest.TestCase):
    def setUp(self):
        self.rule = MainBlockInStage()

    def test_detects_classic_main_block(self):
        code = """
if __name__ == "__main__":
    print("hello")
"""
        tree = ast.parse(code)
        self.assertTrue(self.rule._has_main_block(tree))

    def test_detects_reversed_main_block(self):
        code = """
if "__main__" == __name__:
    print("hello")
"""
        tree = ast.parse(code)
        self.assertTrue(self.rule._has_main_block(tree))

    def test_ignores_other_string_comparison(self):
        code = """
if __name__ == "__other__":
    print("hello")
"""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_main_block(tree))

    def test_ignores_other_variable_comparison(self):
        code = """
if other_var == "__main__":
    print("hello")
"""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_main_block(tree))

    def test_ignores_empty_file(self):
        tree = ast.parse("")
        self.assertFalse(self.rule._has_main_block(tree))

    def test_ignores_unrelated_if(self):
        code = """
x = 1
if x > 0:
    print("positive")
"""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_main_block(tree))

    def test_detects_main_block_nested_in_function(self):
        code = """
def wrapper():
    if __name__ == "__main__":
        print("hello")
"""
        tree = ast.parse(code)
        self.assertTrue(self.rule._has_main_block(tree))

    def test_ignores_chained_comparison(self):
        code = """
if __name__ == "__main__" == something_else:
    print("hello")
"""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_main_block(tree))
