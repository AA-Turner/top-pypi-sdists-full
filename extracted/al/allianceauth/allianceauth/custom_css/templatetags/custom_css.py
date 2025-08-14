"""
Custom template tags for custom_css app
"""

# Alliance Auth Custom CSS
from allianceauth.custom_css.models import CustomCSS

# Django
from django.conf import settings
from django.template.defaulttags import register
from django.utils.safestring import mark_safe

from pathlib import Path


@register.simple_tag
def custom_css_static(path: str) -> str:
    """
    Versioned static URL
    This is to make sure to break the browser cache on CSS updates.

    Example: /static/allianceauth/custom-styles.css?v=1752004819.555084

    :param path:
    :type path:
    :return:
    :rtype:
    """

    try:
        Path(f"{settings.STATIC_ROOT}{path}").resolve(strict=True)
    except FileNotFoundError:
        return ""
    else:
        try:
            custom_css = CustomCSS.objects.get(pk=1)
        except CustomCSS.DoesNotExist:
            return ""
        else:
            custom_css_changed = custom_css.timestamp.timestamp()
            custom_css_version = (
                str(custom_css_changed).replace(" ", "").replace(":", "").replace("-", "")
            )  # remove spaces, colons, and dashes
            versioned_url = f"{settings.STATIC_URL}{path}?v={custom_css_version}"

            return mark_safe(f'<link rel="stylesheet" href="{versioned_url}">')
