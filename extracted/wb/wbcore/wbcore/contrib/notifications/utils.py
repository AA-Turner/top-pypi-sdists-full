import hashlib

from django.conf import settings
from django.contrib.sites.models import Site


def get_checksum(title: str, body: str | None, endpoint: str | None) -> str:
    content = title
    if body:
        content += ":" + body
    if endpoint:
        content += ":" + endpoint
    return hashlib.sha256(content.encode()).hexdigest()


def base_domain() -> str:
    """A utility method that assembles the current domain. Utilizes the site app from django

    Returns:
        A string containing the current domain as noted in the curret `Site` prefixed with the http scheme

    """
    scheme = "https" if settings.SECURE_SSL_REDIRECT else "http"
    base_domain = Site.objects.get_current().domain
    return f"{scheme}://{base_domain}"


def create_notification_type(
    code: str,
    title: str,
    help_text: str,
    web: bool = True,
    mobile: bool = True,
    email: bool = False,
    resource_button_label: str = "",
    is_lock: bool = False,  # set to true if user cannot modified the preference for this notification type
) -> tuple[str, str, str, bool, bool, bool, str, bool]:
    return (code, title, help_text, web, mobile, email, resource_button_label, is_lock)
