from __future__ import absolute_import, division, print_function

from .optional_deps import (
    AppiumWebElement,
    ElementHandle,
    EventFiringWebElement,
    PlaywrightLocator,
    WebElement,
)


def is_list_or_tuple(elm):
    return isinstance(elm, (list, tuple))


def is_webelement(elm):
    return isinstance(
        elm,
        (
            WebElement,
            AppiumWebElement,
            EventFiringWebElement,
            PlaywrightLocator,
            ElementHandle,
        ),
    )
