"""Data types for the menu system."""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    """Single interactive menu item definition.

    Parameters
    ----------
    label:
        Display text shown in the menu.
    aliases:
        Accepted text inputs that resolve to this item (non-TTY fallback).
    handler:
        Callable invoked when the item is selected.  Must return an exit code.
    visible:
        Optional predicate evaluated at menu-build time.  When provided and
        returning ``False`` the item is excluded from the rendered menu.
        Defaults to ``None`` (always visible).
    disabled:
        Optional predicate evaluated at menu-build time.  When provided and
        returning a non-empty string, the item is shown but greyed out and
        unselectable.  The string is displayed as a hint (e.g. "already added").
        Defaults to ``None`` (enabled).
    """

    label: str
    aliases: tuple[str, ...]
    handler: Callable[[], int]
    visible: Callable[[], bool] | None = None
    disabled: Callable[[], str] | None = None


def filter_visible(items: list[MenuItem]) -> list[MenuItem]:
    """Return only items whose ``visible`` predicate is absent or truthy."""

    return [item for item in items if item.visible is None or item.visible()]


def resolve_disabled(item: MenuItem) -> str:
    """Return the disabled hint for *item*, or empty string if enabled."""

    if item.disabled is None:
        return ""
    return item.disabled()
