"""Driver-level tab management helpers.

Maps to V3 codegen handlers:
- new_tab handler — currently emits 2-3 LOC inline
- switch_tab handler — currently emits up to ~13 LOC for title-search
- close_tab handler — currently emits up to ~13 LOC

This module encapsulates that logic so the generated test.py becomes one-liners.
"""
from __future__ import annotations

import logging

from selenium.common.exceptions import NoSuchWindowException

_log = logging.getLogger(__name__)


def new_tab(driver, *, url: str | None = None) -> None:
    """Open a new tab, switch to it, and optionally navigate to ``url``.

    V3 emission reference: ``window.open()`` + ``switch_to.window(handles[-1])`` + optional ``driver.get(url)``.
    Note: unlike V3's no-url path, we do NOT navigate to google.com when url is None.
    """
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url if url is not None else "https://www.google.com")


def switch_tab(driver, *, index: int | None = None, title: str | None = None) -> None:
    """Switch to a tab by ``index`` or ``title``.

    - Both provided: switch to handles[index]; if title doesn't match, linear search.
    - Only index: switch directly by index.
    - Only title: linear search through all handles.
    - Neither: raise ValueError.
    """
    if index is None and title is None:
        raise ValueError("switch_tab requires index or title")

    target = f"index={index}" if index is not None else f"title={title!r}"
    _log.info("    [switch_tab] target=%s current_tabs=%d", target, len(driver.window_handles))

    if title is not None and index is not None:
        all_window_handles = driver.window_handles
        if len(all_window_handles) >= index:
            driver.switch_to.window(all_window_handles[index])
            if driver.title != title:
                tab_identifier_index = -1
                for _, handle in enumerate(all_window_handles):
                    driver.switch_to.window(handle)
                    if driver.title == title:
                        tab_identifier_index = _
                        break
                if tab_identifier_index == -1:
                    raise NoSuchWindowException("Tab identifier not found in the list of open tabs")
        else:
            driver.switch_to.window(driver.window_handles[index])
    elif index is not None:
        driver.switch_to.window(driver.window_handles[index])
    else:
        # title only — linear search
        all_window_handles = driver.window_handles
        tab_identifier_index = -1
        for _, handle in enumerate(all_window_handles):
            driver.switch_to.window(handle)
            if driver.title == title:
                tab_identifier_index = _
                break
        if tab_identifier_index == -1:
            raise NoSuchWindowException("Tab identifier not found in the list of open tabs")

    _log.info("    [switch_tab] switched (url=%s, title=%r)", driver.current_url, driver.title)


def close_tab(driver, *, index: int | None = None, title: str | None = None) -> None:
    """Close a tab by ``index`` or ``title``, then switch to the most recent remaining tab.

    With neither argument: close the current tab.
    """
    if len(driver.window_handles) <= 1:
        raise RuntimeError("Cannot close the only open tab")
    if title is not None and index is not None:
        all_window_handles = driver.window_handles
        if len(all_window_handles) >= index:
            driver.switch_to.window(all_window_handles[index])
            if driver.title != title:
                tab_identifier_index = -1
                for _, handle in enumerate(all_window_handles):
                    driver.switch_to.window(handle)
                    if driver.title == title:
                        tab_identifier_index = _
                        break
                if tab_identifier_index == -1:
                    raise NoSuchWindowException("Tab identifier not found in the list of open tabs")
        else:
            driver.switch_to.window(driver.window_handles[index])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    elif index is not None:
        driver.switch_to.window(driver.window_handles[index])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    elif title is not None:
        all_window_handles = driver.window_handles
        tab_identifier_index = -1
        for _, handle in enumerate(all_window_handles):
            driver.switch_to.window(handle)
            if driver.title == title:
                tab_identifier_index = _
                break
        if tab_identifier_index == -1:
            raise NoSuchWindowException("Tab identifier not found in the list of open tabs")
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    else:
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])


__all__ = ["new_tab", "switch_tab", "close_tab"]
