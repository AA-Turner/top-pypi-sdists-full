"""
Custom template tags for custom_css app
"""

# Django
from django.template.defaulttags import register

# Alliance Auth Custom CSS
from allianceauth.custom_css.models import CustomCSS


@register.simple_tag
def return_custom_css() -> str:
    """
    Template tag to load custom CSS

    :return:
    :rtype:
    """

    css = CustomCSS.get_solo()

    return css.css_compressed if css.css_compressed else ""
