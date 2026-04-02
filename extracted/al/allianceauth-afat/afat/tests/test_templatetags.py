"""
Test our template tags
"""

# Django
from django.template import Context, Template

# Alliance Auth AFAT
from afat.tests import BaseTestCase


class TestAfatFilters(BaseTestCase):
    """
    Test template filters
    """

    def test_month_name_filter(self):
        """
        Test month_name

        :return:
        """

        context = Context(dict_={"month": 5})
        template_to_render = Template(
            template_string="{% load afat %} {{ month|month_name }}"
        )

        rendered_template = template_to_render.render(context=context)

        self.assertInHTML(needle="May", haystack=rendered_template)


class TestSumValuesFilter(BaseTestCase):
    """
    Test the sum_values filter
    """

    def test_sum_values(self):
        """
        Test sum_values

        :return:
        :rtype:
        """

        context = Context(dict_={"test_dict": {"a": 1, "b": 2, "c": 3}})
        template_to_render = Template(
            template_string="{% load afat %} {{ test_dict|sum_values }}"
        )

        rendered_template = template_to_render.render(context=context)

        self.assertInHTML(needle="6", haystack=rendered_template)
