__lazy_modules__ = ["allianceauth.theme.hooks", "collections.abc", "django.http", "django.template"]

from typing import TYPE_CHECKING, Any

from django import template
from django.conf import settings

from allianceauth.hooks import get_hooks

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.http import HttpRequest
    from django.template import Context

    from allianceauth.theme.hooks import ThemeHook

register = template.Library()


def hook_to_name(th: "ThemeHook") -> str:
    return f"{th.__class__.__module__}.{th.__class__.__name__}"


def get_theme_from_hooks(theme: str, hooks: "list[Callable[[], ThemeHook]]") -> "ThemeHook | None":
    for h in hooks:
        _h = h()
        _hn = hook_to_name(_h)
        if _hn == theme:
            return _h


def get_theme(request: "HttpRequest") -> "ThemeHook | None":
    theme = settings.DEFAULT_THEME
    hooks = get_hooks('theme_hook')

    try:
        theme = request.session.get('THEME', settings.DEFAULT_THEME)
    except AttributeError:
        pass

    theme_hook = get_theme_from_hooks(theme, hooks)

    if not theme_hook:
        theme_hook = get_theme_from_hooks(settings.DEFAULT_THEME, hooks)

    return theme_hook


def get_theme_context(request: "HttpRequest") -> dict[str, Any]:
    return {
        'theme': get_theme(request),
        'request': request
    }


@register.inclusion_tag('theme/theme_imports_css.html', takes_context=True)
def theme_css(context: "Context") -> dict[str, Any]:
    request = context['request']
    return get_theme_context(request)


@register.simple_tag(takes_context=True)
def theme_html_tags(context: "Context") -> str:
    request = context['request']
    theme = get_theme(request)
    return getattr(theme, "html_tags", "")


@register.simple_tag(takes_context=True)
def header_padding_size(context: "Context") -> str | None:
    request = context['request']
    theme = get_theme(request)
    return theme.header_padding


@register.inclusion_tag('theme/theme_imports_js.html', takes_context=True)
def theme_js(context: "Context") -> dict[str, Any]:
    request = context['request']
    return get_theme_context(request)


@register.inclusion_tag('theme/theme_select.html', takes_context=True)
def theme_select(context: "Context") -> dict[str, Any]:
    request = context['request']
    return {
        'next': request.path,
        'themes': get_hooks('theme_hook'),
        'selected_theme': get_theme(request)
    }
