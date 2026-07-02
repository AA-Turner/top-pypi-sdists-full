from django.test import TestCase
from django.utils import translation
from django.utils.safestring import mark_safe

from app_utils.views import (
    HttpResponseNoContent,
    bootstrap_glyph_html,
    bootstrap_icon_plus_text_html,
    bootstrap_label_html,
    bootstrap_link_button_html,
    humanize_value,
    image_html,
    link_html,
    no_wrap_html,
    yesno_str,
)

MODULE_PATH = "app_utils"
CURRENT_PATH = "utils_test_app.tests.test_all"

ICON_URL = "https://images.evetech.net/types/670/icon?size=64"


class TestHttpResponseNoContent(TestCase):
    def test_can_create_objects(self):
        # when
        res = HttpResponseNoContent()
        # then
        self.assertEqual(res.status_code, 204)
        if hasattr(res, "_headers"):  # Django<3.2
            self.assertNotIn("content-type", res._headers)
        elif hasattr(res, "headers"):  # Django>=3.2
            self.assertNotIn("content-type", res.headers)
        else:
            self.fail("No headers found")


class TestHtmlHelper(TestCase):
    def test_add_no_wrap_html(self):
        expected = '<span class="text-nowrap">Dummy</span>'
        self.assertEqual(no_wrap_html("Dummy"), expected)

    def test_yesno_str(self):
        with translation.override("en"):
            self.assertEqual(yesno_str(True), "yes")
            self.assertEqual(yesno_str(False), "no")
            self.assertEqual(yesno_str(None), "no")
            self.assertEqual(yesno_str(123), "no")
            self.assertEqual(yesno_str("xxxx"), "no")

    def test_add_bs_label_html(self):
        expected = '<span class="label label-danger">Dummy</span>'
        self.assertEqual(bootstrap_label_html("Dummy", "danger"), expected)

    def test_create_bs_button_html_default(self):
        expected = (
            '<a href="https://www.example.com" class="btn btn-info">'
            '<span class="glyphicon glyphicon-example"></span></a>'
        )
        self.assertEqual(
            bootstrap_link_button_html("https://www.example.com", "example", "info"),
            expected,
        )

    def test_create_bs_button_html_disabled(self):
        expected = (
            '<a href="https://www.example.com" class="btn btn-info"'
            ' disabled="disabled">'
            '<span class="glyphicon glyphicon-example"></span></a>'
        )
        self.assertEqual(
            bootstrap_link_button_html(
                "https://www.example.com", "example", "info", True
            ),
            expected,
        )


class TestLinkHtml(TestCase):
    def test_create_link_html_default(self):
        # when
        result = link_html("https://www.example.com", "Example Link")
        # then
        expected = '<a href="https://www.example.com" target="_blank">Example Link</a>'
        self.assertEqual(result, expected)

    def test_create_link_html(self):
        expected = '<a href="https://www.example.com">Example Link</a>'
        self.assertEqual(
            link_html("https://www.example.com", "Example Link", False), expected
        )
        expected = (
            '<a href="https://www.example.com">' "<strong>Example Link</strong></a>"
        )
        self.assertEqual(
            link_html(
                "https://www.example.com",
                mark_safe("<strong>Example Link</strong>"),
                False,
            ),
            expected,
        )

    def test_should_create_link_with_classes(self):
        # when
        result = link_html(
            "https://www.example.com", "Example Link", classes=["green", "blue"]
        )
        # then
        expected = (
            '<a class="green blue" href="https://www.example.com" '
            'target="_blank">Example Link</a>'
        )
        self.assertEqual(result, expected)


class TestImageUrl(TestCase):
    def test_should_create_simple_image_url(self):
        # when
        result = image_html(ICON_URL)
        # then
        expected = '<img src="https://images.evetech.net/types/670/icon?size=64">'
        self.assertEqual(result, expected)

    def test_should_include_one_class(self):
        # when
        result = image_html(ICON_URL, classes=["green"])
        # then
        expected = '<img class="green" src="https://images.evetech.net/types/670/icon?size=64">'
        self.assertEqual(result, expected)

    def test_should_include_multiple_classes(self):
        # when
        result = image_html(ICON_URL, classes=["green", "blue"])
        # then
        expected = '<img class="green blue" src="https://images.evetech.net/types/670/icon?size=64">'
        self.assertEqual(result, expected)

    def test_should_include_size(self):
        # when
        result = image_html(ICON_URL, size=128)
        # then
        expected = '<img width="128" height="128" src="https://images.evetech.net/types/670/icon?size=64">'
        self.assertEqual(result, expected)

    def test_should_include_classes_and_size(self):
        # when
        result = image_html(ICON_URL, classes=["green", "blue"], size=128)
        # then
        expected = '<img class="green blue" width="128" height="128" src="https://images.evetech.net/types/670/icon?size=64">'
        self.assertEqual(result, expected)


class TestBootstrapIconPlusTextHtml(TestCase):
    def test_should_create_minimal(self):
        # when
        result = bootstrap_icon_plus_text_html(icon_url=ICON_URL, text="Alpha")
        # then
        self.assertEqual(
            result,
            (
                '<img width="32" height="32" '
                'src="https://images.evetech.net/types/670/icon?size=64"> '
                '<span class="icon-plus-text">Alpha</span>'
            ),
        )

    def test_should_create_link(self):
        # when
        result = bootstrap_icon_plus_text_html(
            icon_url=ICON_URL, text="Alpha", url="www.example.com"
        )
        # then
        self.assertEqual(
            result,
            (
                '<img width="32" height="32" '
                'src="https://images.evetech.net/types/670/icon?size=64"> '
                '<a class="icon-plus-text" href="www.example.com">Alpha</a>'
            ),
        )


class TestBootstrapGlyphHtml(TestCase):
    def test_should_return_simply_glyph(self):
        expected = '<span class="glyphicon glyphicon-example"></span>'
        self.assertEqual(bootstrap_glyph_html("example"), expected)


class TestFormatIskValue(TestCase):
    def test_defaults(self):
        self.assertEqual(humanize_value(0.9), "0.90")
        self.assertEqual(humanize_value(1), "1.00")
        self.assertEqual(humanize_value(1.1), "1.10")
        self.assertEqual(humanize_value(1000), "1.00k")
        self.assertEqual(humanize_value(1100), "1.10k")
        self.assertEqual(humanize_value(551100), "551.10k")
        self.assertEqual(humanize_value(1000000), "1.00m")
        self.assertEqual(humanize_value(1000000000), "1.00b")
        self.assertEqual(humanize_value(1000000000000), "1.00t")

    def test_precision(self):
        self.assertEqual(humanize_value(12340000000, 1), "12.3b")
