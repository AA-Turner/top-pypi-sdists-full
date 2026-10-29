"""
Tests for the custom_css template tag.
"""

from django.test import TestCase

from allianceauth.custom_css.models import CustomCSS
from allianceauth.custom_css.templatetags.custom_css import return_custom_css


class TestCustomCssTemplateTag(TestCase):
    """
    Test the custom_css template tag
    """

    def test_returns_empty_string_when_css_compressed_is_empty(self):
        """
        Test that the custom_css template tag returns an empty string when css_compressed is empty.

        :return:
        :rtype:
        """

        CustomCSS.objects.create(
            pk=CustomCSS.singleton_instance_id, css="", css_compressed=""
        )
        result = return_custom_css()

        self.assertEqual(result, "")

    def test_returns_compressed_css_when_css_compressed_is_not_empty(self):
        """
        Test that the custom_css template tag returns the compressed CSS when css_compressed is not empty.

        :return:
        :rtype:
        """

        CustomCSS.objects.create(
            pk=CustomCSS.singleton_instance_id,
            css="body { color: red }",
            css_compressed="body{color:red}",
        )
        result = return_custom_css()

        self.assertEqual(result, "body{color:red}")
