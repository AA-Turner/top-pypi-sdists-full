# jnjrender/tests/test_renderer.py
import unittest
from jnjrender.renderer import render_jinja_to_yaml

class TestRenderer(unittest.TestCase):
    def test_render_jinja_to_yaml(self):
        template_str = "key: {{ value }}"
        context = {"value": "example"}
        result = render_jinja_to_yaml(template_str, context)
        self.assertEqual(result["key"], "example")

if __name__ == "__main__":
    unittest.main()

