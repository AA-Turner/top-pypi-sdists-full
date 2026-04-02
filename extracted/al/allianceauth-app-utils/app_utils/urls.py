"""Utilities related to URLs."""

import re
from typing import Optional
from urllib.parse import urljoin

from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse


# old: get_absolute_url
def reverse_absolute(viewname: str, args: Optional[list] = None) -> str:
    """Return absolute URL for a view name.

    Similar to Django's ``reverse()``, but returns an absolute URL.
    """
    return urljoin(site_absolute_url(), reverse(viewname, args=args))


# TODO: Only enable for alliance auth
# old: get_site_base_url
def site_absolute_url() -> str:
    """Return absolute URL for this Alliance Auth site."""
    try:
        match = re.match(r"(.+)\/sso\/callback", settings.ESI_SSO_CALLBACK_URL)
        if match:
            return match.group(1)
    except AttributeError:
        pass

    return ""


def static_file_absolute_url(file_path: str) -> str:
    """Return absolute URL to a static file.

    Args:
        file_path: relative path to a static file
    """
    return urljoin(site_absolute_url(), static(file_path))
