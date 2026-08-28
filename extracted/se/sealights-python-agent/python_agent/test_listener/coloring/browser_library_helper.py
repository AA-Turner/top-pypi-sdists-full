"""Coloring adapter for robotframework-browser (contracts C6, C7a).

This library keeps no Python page object at all: Playwright runs in a Node
process behind gRPC, and the only handles are the page ids in
`get_browser_catalog()`. Duck typing therefore cannot work here, which is why
the catalog route is mandatory rather than a preference.

Ported by hand from `robot/SLListener.py`, including the four SLDEV-28058 fixes
that file carries. Each of those is marked below, because every one of them was
a silent failure: nothing raised, and coverage simply went to the wrong place or
nowhere.
"""

import json
import logging

from python_agent.test_listener.coloring.playwright_helper import (
    SEND_FOOTPRINTS_JS,
    SET_BAGGAGE_JS,
    baggage_arguments,
)
from python_agent.test_listener.coloring.robot_coloring import ColoringAdapter

log = logging.getLogger(__name__)

BROWSER_LIBRARY_NAME = "Browser"
BROWSER_CATALOG_KEYWORD = "get_browser_catalog"


def set_context_script(execution_id, test_name):
    """The shared `set:context` payload, arrow-wrapped with its values baked in.

    Two constraints meet here. `evaluate_javascript` rejects a bare statement
    and wants an arrow function (`SLListener.md` §Browser Library
    instrumentation), and it has an `arg=` that would feed `SET_BAGGAGE_JS` its
    argument directly, but whether a selector-less call forwards that arg to the
    function is unproven against the Node sidecar, and getting it wrong is
    silent. Baking the values into a call of the shared constant satisfies the
    first and does not depend on the second, while keeping the constant the
    single source of truth for what the page receives.

    The values go through `json.dumps`, which is the SLDEV-28058 `49533ef` fix:
    interpolating them into a quoted JavaScript string let a test name
    containing a double quote break out of the literal. `baggage_arguments`
    carries the `8696fc7` half, that an identity never reaches the page as a
    JavaScript `null` or as a bare number.
    """
    arguments = baggage_arguments(execution_id, test_name)
    return "() => (%s)(%s)" % (SET_BAGGAGE_JS, json.dumps(arguments))


def flatten_pages(catalog):
    """`{page id: url}` across every browser and context in the catalog.

    A page with no id cannot be switched to, so it is not a handle. A URL of
    `None` is kept: it is a page that has not navigated yet, and it is a state
    the seam has to be able to see change.
    """
    pages = {}
    for browser in catalog or []:
        for context in browser.get("contexts") or []:
            for page in context.get("pages") or []:
                page_id = page.get("id")
                if page_id is not None:
                    pages[page_id] = page.get("url")
    return pages


def active_page_id(catalog):
    """The one page Robot's Browser focus is on, or `None`.

    SLDEV-28058 `8696fc7`: every context keeps its own `activePage`, including
    contexts that are not focused, so taking the first non-null one picks a
    stale page. The active page exists only under the active browser's active
    context, which is how the library resolves it itself.
    """
    for browser in catalog or []:
        if not browser.get("activeBrowser"):
            continue
        active_context_id = browser.get("activeContext")
        for context in browser.get("contexts") or []:
            if context.get("id") == active_context_id:
                return context.get("activePage")
    return None


class BrowserLibraryPage(object):
    """One page, and what it takes to run a script on it.

    Switching is per page rather than once per batch, which costs one extra
    switch for each page that is not the active one. That is the price of the
    seam's per-handle guarding, and it buys the common single-page case a run
    with no switch at all.
    """

    def __init__(self, library, page_id, active_page_id):
        self.library = library
        self.page_id = page_id
        self.active_page_id = active_page_id

    def evaluate(self, script):
        # SLDEV-28058 `49533ef`: the switch used to be skipped whenever the
        # catalog reported no active page, and `evaluate_javascript(None, ...)`
        # means "the current page", so every page in the loop was handed the
        # script for whichever page happened to be current.
        switched = False
        if self.page_id != self.active_page_id:
            self.library.switch_page(self.page_id)
            switched = True
        try:
            self.library.evaluate_javascript(None, script)
        finally:
            # SLDEV-28058 `48bd51c`: restoring unconditionally spent a gRPC
            # round trip putting the focus back where it already was.
            if switched and self.active_page_id is not None:
                self.library.switch_page(self.active_page_id)


class BrowserLibraryAdapter(ColoringAdapter):
    """Handles for `robotframework-browser`.

    The staleness token is the page URL, which is contract C7a for this stack:
    a page that is new or has navigated needs the identity injected again, and
    the seam's comparison is the `_diff_browser_catalog_pages` of the standalone
    listener expressed once for every stack instead of once here.
    """

    name = BROWSER_LIBRARY_NAME

    def targets(self):
        library = self.seam.library_instance(
            BROWSER_LIBRARY_NAME, BROWSER_CATALOG_KEYWORD
        )
        if library is None:
            return []
        catalog = library.get_browser_catalog()
        active = active_page_id(catalog)
        return [
            (page_id, url, BrowserLibraryPage(library, page_id, active))
            for page_id, url in flatten_pages(catalog).items()
        ]

    def color(self, handle, execution_id, test_name):
        handle.evaluate(set_context_script(execution_id, test_name))

    def flush(self, handle):
        handle.evaluate(SEND_FOOTPRINTS_JS)
