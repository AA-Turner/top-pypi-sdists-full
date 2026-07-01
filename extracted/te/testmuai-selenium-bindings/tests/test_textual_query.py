"""Unit tests for testmu_selenium._helpers.textual_query."""
import unittest
from unittest.mock import MagicMock, patch

from testmu_selenium._helpers.textual_query import textualQuery


def _make_element(tag_name="div", attrs=None, text="", outer_html=""):
    el = MagicMock()
    el.tag_name = tag_name
    attrs_with_html = {**(attrs or {}), "outerHTML": outer_html}
    el.get_attribute.side_effect = lambda key: attrs_with_html.get(key, None)
    el.text = text
    el.is_selected.return_value = False
    el.is_enabled.return_value = True
    el.is_displayed.return_value = True
    el.value_of_css_property.return_value = ""
    el.get_property.return_value = text
    el.rect = {"x": 0, "y": 0, "width": 0, "height": 0}
    el.size = {"width": 0, "height": 0}
    el.aria_role = ""
    return el


class TextualQueryTests(unittest.TestCase):
    def setUp(self):
        self.driver = MagicMock()
        self.selector = [{"selector": "//div", "isXPath": True}]

    def _patch_find(self, element):
        return patch(
            "testmu_selenium._helpers.textual_query.findElement",
            return_value=element,
        )

    def test_text_attribute_no_regex(self):
        element = _make_element(tag_name="p", text="hello world")
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="text",
            )
        self.assertEqual(result, "hello world")

    def test_value_attribute_no_regex(self):
        element = _make_element(tag_name="input", attrs={"value": "input-text"})
        element.get_property.return_value = "input-text"
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="value",
            )
        self.assertEqual(result, "input-text")

    def test_regex_match_on_outerHTML(self):
        element = _make_element(
            tag_name="span",
            text="Total: $42",
            outer_html='<span>Total: $42</span>',
        )
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="text",
                regex_pattern=r"\$(\d+)",
            )
        self.assertEqual(result, "42")

    def test_regex_miss_returns_empty(self):
        element = _make_element(
            tag_name="span",
            text="No price here",
            outer_html='<span>No price here</span>',
        )
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="text",
                regex_pattern=r"\$(\d+)",
            )
        self.assertEqual(result, "")

    def test_img_returns_src_unchanged(self):
        element = _make_element(
            tag_name="img",
            attrs={"src": "https://example.com/photo.png"},
        )
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="src",
            )
        self.assertEqual(result, "https://example.com/photo.png")

    def test_canvas_returns_src_unchanged(self):
        element = _make_element(
            tag_name="canvas",
            attrs={"src": "data:image/png;base64,abc"},
        )
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="src",
            )
        self.assertEqual(result, "data:image/png;base64,abc")

    def test_href_attribute(self):
        element = _make_element(
            tag_name="a",
            attrs={"href": "https://lambdatest.com"},
        )
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="href",
            )
        self.assertEqual(result, "https://lambdatest.com")

    def test_return_type_number_coerces_to_float(self):
        element = _make_element(
            tag_name="span",
            text="42.5",
            outer_html='<span>42.5</span>',
        )
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="text",
                return_type="number",
            )
        self.assertEqual(result, 42.5)

    def test_unknown_attribute_raises(self):
        element = _make_element(tag_name="div")
        with self._patch_find(element):
            with self.assertRaises(ValueError):
                textualQuery(
                    self.driver,
                    selector=self.selector,
                    selected_attribute_name="not_a_real_attribute",
                )

    def test_css_color_attribute_returns_color_name(self):
        """_rgba_to_name converts rgba(255,0,0,1) → 'red' for the 'color' attribute."""
        element = _make_element(tag_name="span")
        element.value_of_css_property.return_value = "rgba(255, 0, 0, 1)"
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="color",
            )
        self.assertEqual(result, "red")

    def test_regex_miss_with_number_return_type_returns_empty_string(self):
        """Regex miss short-circuits before _coerce; returns "" even when return_type='number'."""
        element = _make_element(
            tag_name="span",
            text="No price here",
            outer_html="<span>No price here</span>",
        )
        with self._patch_find(element):
            result = textualQuery(
                self.driver,
                selector=self.selector,
                selected_attribute_name="text",
                regex_pattern=r"\$(\d+)",
                return_type="number",
            )
        self.assertEqual(result, "")

    def test_description_template_resolved_before_find(self):
        """The description passed to findElement must be the resolved string,
        not the ${p}/{{v}} template."""
        from testmu_selenium._vars import _test_params, set_var, clear_state

        clear_state()
        _test_params["p"] = "zeeshan"
        set_var("v", "world")
        element = _make_element(tag_name="p", text="hello")
        try:
            with patch(
                "testmu_selenium._helpers.textual_query.findElement",
                return_value=element,
            ) as find:
                textualQuery(
                    self.driver,
                    selector=self.selector,
                    selected_attribute_name="text",
                    description="Check ${p} and {{v}}",
                )
            self.assertEqual(
                find.call_args.kwargs["description"], "Check zeeshan and world"
            )
        finally:
            clear_state()


if __name__ == "__main__":
    unittest.main()
