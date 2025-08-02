"""Utilities for supporting Django views."""

from enum import Enum
from http import HTTPStatus
from typing import List, Optional

from django.http import HttpResponse, JsonResponse
from django.utils.functional import lazy
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

DEFAULT_ICON_SIZE = 32
format_html_lazy = lazy(format_html, str)


class HttpResponseNoContent(HttpResponse):
    """Special HTTP response with no content, just headers.

    The content operations are ignored.
    """

    status_code = HTTPStatus.NO_CONTENT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # although we don't define a content-type, base class sets a
        # default one -- remove it, we're not returning content
        if hasattr(self, "headers") and "content-type" in self.headers:
            del self.headers["content-type"]
        else:
            raise ValueError("No header found")  # this should never be called


class JSONResponseMixin:
    """A mixin that can be used to render a JSON response for a class based view."""

    def render_to_json_response(self, context, **response_kwargs):
        """Return a JSON response, transforming 'context' to make the payload."""
        return JsonResponse(self.get_data(context), safe=False, **response_kwargs)

    def get_data(self, context):
        """Return an object that will be serialized as JSON by json.dumps()."""
        return context


class BootstrapStyle(str, Enum):
    """A Bootstrap context style names, e.g. for labels.

    DEPRECATED: This class works for Bootstrap 3 only, which is no longer supported by AA.
    """

    DANGER = "danger"  #:
    DEFAULT = "default"  #:
    INFO = "info"  #:
    PRIMARY = "primary"  #:
    SUCCESS = "success"  #:
    WARNING = "warning"  #:

    def __str__(self) -> str:
        return self.value


class BootstrapStyleBS5(str, Enum):
    """A Bootstrap context style name, e.g. for labels"""

    DANGER = "danger"  #:
    DEFAULT = "secondary"  #:
    INFO = "info"  #:
    PRIMARY = "primary"  #:
    SUCCESS = "success"  #:
    WARNING = "warning"  #:

    def __str__(self) -> str:
        return self.value


# old: add_bs_label_html
def bootstrap_label_html(text: str, label: str = "default") -> str:
    """Return HTML for a Bootstrap label."""
    return format_html('<span class="label label-{}">{}</span>', label, text)


# old: create_bs_glyph_html
def bootstrap_glyph_html(glyph_name: str) -> str:
    """Return HTML for a Bootstrap 3 glyph."""
    return format_html(
        '<span class="glyphicon glyphicon-{}"></span>', glyph_name.lower()
    )


# old: create_bs_glyph_2_html
def bootstrap_glyph_2_html(glyph_name, tooltip_text=None, color="initial") -> str:
    """Return HTML for a Bootstrap 3 glyph HTML. Can also have a tool tip and color."""
    if tooltip_text:
        tooltip_html = mark_safe(
            'aria-hidden="true" data-toggle="tooltip" data-placement="top" '
            f'title="{tooltip_text}"'
        )
    else:
        tooltip_html = ""
    return format_html(
        '<span class="glyphicon glyphicon-{}" style="color:{};"{}></span>',
        glyph_name.lower(),
        color,
        tooltip_html,
    )


def bootstrap_icon_plus_name_html(
    icon_url,
    name,
    size: int = DEFAULT_ICON_SIZE,
    avatar: bool = False,
    url: Optional[str] = None,
    text: Optional[str] = None,
) -> str:
    """Returns HTML to display an icon next to a name. Can also be a link.

    DEPRECATED. To be replaced by bootstrap_icon_plus_text_html.
    """
    name_html = link_html(url, name, new_window=False) if url else name
    if text:
        name_html = format_html("{}&nbsp;{}", name_html, text)

    return format_html(
        "{}&nbsp;&nbsp;&nbsp;{}",
        image_html(
            icon_url, classes=["ra-avatar", "img-circle"] if avatar else [], size=size
        ),
        name_html,
    )


def bootstrap_icon_plus_text_html(
    icon_url: str,
    text: str,
    size: int = DEFAULT_ICON_SIZE,
    avatar: bool = False,
    url: Optional[str] = None,
    suffix: Optional[str] = None,
) -> str:
    """Return HTML for a widget consisting of an icon with a text or link:

    `<Icon> <Text/Link> [<Suffix>]`

    Adds the class ``icon-plus-text`` to all images to enable styling.

    Args:
        - icon_url: URL to an icon file, supported by <img>, e.g. GIF, PNG
        - text: Text to be shown next to icon. Often a name.
        - size: Size of the icon in pixel
        - avatar: When enabled the icon will get Bootstrap 3 classes for avatars
        - url: A provided URL will transform the text into a link
        - suffix: Additional text to be shown after the main text.
            Will not be part of a link.
    """
    my_css_class = "icon-plus-text"
    if url:
        text_html = link_html(url, text, new_window=False, classes=[my_css_class])
    else:
        text_html = format_html('<span class="{}">{}</span>', my_css_class, text)

    if suffix:
        text_html = format_html("{} {}", text_html, suffix)

    my_image_html = image_html(
        icon_url, classes=["img-circle"] if avatar else [], size=size
    )
    return format_html("{} {}", my_image_html, text_html)


# old: create_bs_button_html
def bootstrap_link_button_html(
    url: str, glyph_name: str, button_type: str, disabled: bool = False
) -> str:
    """Return HTML for a button with Bootstrap 3 glyphs."""
    return format_html(
        '<a href="{}" class="btn btn-{}"{}>{}</a>',
        url,
        button_type,
        mark_safe(' disabled="disabled"') if disabled else "",
        bootstrap_glyph_html(glyph_name),
    )


# old: create_fa_button_html
def fontawesome_link_button_html(
    url: str,
    fa_code: str,
    button_type: str,
    tooltip: Optional[str] = None,
    disabled: bool = False,
) -> str:
    """Return HTML for a button with fontawesome symbols."""
    return format_html(
        '<a href="{}" class="btn btn-{}"{}>{}{}</a>',
        url,
        button_type,
        mark_safe(f' title="{tooltip}"') if tooltip else "",
        mark_safe(' disabled="disabled"') if disabled else "",
        mark_safe(f'<i class="{fa_code}"></i>'),
    )


def fontawesome_modal_button_html(
    modal_id: str,
    fa_code: str,
    ajax_url: str = "",
    tooltip: str = "",
    style=BootstrapStyle.DEFAULT,
) -> str:
    """Return HTML for a modal button with fontawesome symbols.

    DEPRECATED: Only works with Bootstrap3, which is no longer supported by AA

    Args:
        modal_id: DOM ID of modal to invoke
        fa_code: fontawesome code, e.g. "fas fa-moon"
        ajax_url: URL to invoke via AJAX for loading modal content
        tooltip: text to appear as tooltip
        style: Bootstrap context style for the button
    """
    return format_html(
        '<button type="button" '
        'class="btn btn-{}" '
        'data-toggle="modal" '
        'data-target="#{}" '
        "{}"
        "{}>"
        '<i class="{}"></i>'
        "</button>",
        BootstrapStyle(style),
        modal_id,
        mark_safe(f'title="{tooltip}" ') if tooltip else "",
        mark_safe(f'data-ajax_url="{ajax_url}" ') if ajax_url else "",
        fa_code,
    )


def humanize_value(value: float, precision: int = 2) -> str:
    """Return a value in a human readable and abbreviated form
    e.g. ``1234678`` -> ``1.23m``.
    """
    value = float(value)
    for exponent, identifier in [(12, "t"), (9, "b"), (6, "m"), (3, "k")]:
        if value >= pow(10, exponent):
            return f"{value / pow(10, exponent):,.{precision}f}{identifier}"

    return f"{value:,.{precision}f}"


def image_html(
    src: str, classes: Optional[List[str]] = None, size: Optional[int] = None
) -> str:
    """Return HTML for an image with optional classes and size."""
    classes_html = _classes_html(classes) if classes else ""
    size_html = (
        format_html(' width="{}" height="{}"', int(size), int(size)) if size else ""
    )
    return format_html('<img{}{} src="{}">', classes_html, size_html, src)


# old: create_link_html
def link_html(
    url: str, label: str, new_window: bool = True, classes: Optional[List[str]] = None
) -> str:
    """Return HTML for a link.

    Args:
        - url: URL
        - label: Text describing the link
        - new_window: When enabled the link will open a new window
        - classes: Classes to be added to the a tag
    """
    classes_html = _classes_html(classes) if classes else ""
    target_html = mark_safe(' target="_blank"') if new_window else ""
    return format_html('<a{} href="{}"{}>{}</a>', classes_html, url, target_html, label)


def _classes_html(classes: List[str]) -> str:
    classes_html = format_html(' class="{}"', (" ".join(classes)))
    return classes_html


# old: add_no_wrap_html
def no_wrap_html(text: str) -> str:
    """Add no-wrap HTML to text with Bootstrap 3."""
    return format_html('<span class="text-nowrap">{}</span>', text)


def yesno_str(value: bool) -> str:
    """Return yes/no for boolean as string and with localization."""
    return _("yes") if value is True else _("no")


def yesnonone_str(value: Optional[bool]) -> str:
    """Return yes/no/none for boolean as string and with localization."""
    if value is True:
        return _("yes")
    if value is False:
        return _("no")
    return ""
