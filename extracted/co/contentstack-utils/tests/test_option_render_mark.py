import json
import os
import unittest
from contentstack_utils import Utils
from contentstack_utils.render.options import Options
from tests.mocks.supercharged.results import Results


class TestOptionRenderMark(unittest.TestCase):

    def setUp(self):
        print("print for getting started option render mark")

    def test_option_render_mark_superscript_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("superscript", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("<sup>some_string_for_example</sup>", what_does_it_returns)

    def test_option_render_mark_subscript_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("subscript", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("<sub>some_string_for_example</sub>", what_does_it_returns)

    def test_option_render_mark_inline_code_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("inlineCode", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("<span>some_string_for_example</span>", what_does_it_returns)

    def test_option_render_mark_strikethrough_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("strikethrough", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("<strike>some_string_for_example</strike>", what_does_it_returns)

    def test_option_render_mark_underline_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("underline", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("<u>some_string_for_example</u>", what_does_it_returns)

    def test_option_render_mark_italic_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("italic", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("<em>some_string_for_example</em>", what_does_it_returns)

    def test_option_render_mark_bold_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("bold", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("<strong>some_string_for_example</strong>", what_does_it_returns)

    def test_option_render_mark_undefined_supercharged_stringify(self):
        what_does_it_returns = Options.render_mark("", "some_string_for_example")
        print(what_does_it_returns)
        self.assertEqual("some_string_for_example", what_does_it_returns)
