import ast
import unittest

from abstra_internals.repositories.linter.rules.missing_render_in_page import (
    MissingRenderInPage,
)


class TestMissingRenderInPage(unittest.TestCase):
    def setUp(self):
        self.rule = MissingRenderInPage()

    def test_detects_render_function(self):
        code = """
from abstra.pages import register_function

@register_function
def __render__():
    return '<div>hello</div>'
"""
        tree = ast.parse(code)
        self.assertTrue(self.rule._has_render_function(tree))

    def test_detects_render_with_module_decorator(self):
        code = """
import abstra.pages as pages

@pages.register_function
def __render__():
    return '<div>hello</div>'
"""
        tree = ast.parse(code)
        self.assertTrue(self.rule._has_render_function(tree))

    def test_flags_missing_render(self):
        code = """
from abstra.pages import register_function

@register_function
def get_data():
    return {}
"""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_render_function(tree))

    def test_flags_render_without_decorator(self):
        code = """
def __render__():
    return '<div>hello</div>'
"""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_render_function(tree))

    def test_flags_empty_file(self):
        code = ""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_render_function(tree))

    def test_flags_wrong_function_name_with_decorator(self):
        code = """
from abstra.pages import register_function

@register_function
def render():
    return '<div>hello</div>'
"""
        tree = ast.parse(code)
        self.assertFalse(self.rule._has_render_function(tree))

    def test_detects_render_alongside_other_functions(self):
        code = """
from abstra.pages import register_function

@register_function
def get_data():
    return {}

@register_function
def __render__():
    return '<div>hello</div>'
"""
        tree = ast.parse(code)
        self.assertTrue(self.rule._has_render_function(tree))
