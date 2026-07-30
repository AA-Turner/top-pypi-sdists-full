"""Tests for testmu_selenium._helpers.tabs."""
from __future__ import annotations

import logging

import pytest
from unittest.mock import MagicMock, call

from selenium.common.exceptions import NoSuchWindowException

from testmu_selenium._helpers.tabs import new_tab, switch_tab, close_tab


def _make_driver(handles=None, title="Page"):
    """Return a MagicMock driver with window_handles and title set."""
    driver = MagicMock()
    driver.window_handles = handles if handles is not None else ["h0", "h1"]
    driver.title = title
    return driver


def _make_url_driver(tabs):
    """Return a MagicMock driver whose title+current_url change per handle.

    ``tabs`` is a list of ``(handle, title, url)`` tuples. Switching to a
    handle updates both ``driver.title`` and ``driver.current_url`` to match,
    mirroring real Selenium where those reflect the focused window.
    """
    driver = MagicMock()
    driver.window_handles = [h for h, _, _ in tabs]
    info = {h: (t, u) for h, t, u in tabs}

    def switch_side_effect(handle):
        driver.title, driver.current_url = info[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title, driver.current_url = info[tabs[0][0]]
    return driver


# ---------------------------------------------------------------------------
# new_tab
# ---------------------------------------------------------------------------


def test_new_tab_opens_window_and_switches():
    driver = _make_driver(handles=["h0", "h1"])
    new_tab(driver)
    driver.execute_script.assert_called_once_with("window.open()")
    driver.switch_to.window.assert_called_once_with("h1")


def test_new_tab_navigates_when_url_provided():
    driver = _make_driver(handles=["h0", "h1"])
    new_tab(driver, url="https://example.com")
    driver.execute_script.assert_called_once_with("window.open()")
    driver.switch_to.window.assert_called_once_with("h1")
    driver.get.assert_called_once_with("https://example.com")


def test_new_tab_navigates_google_when_url_none():
    driver = _make_driver(handles=["h0", "h1"])
    new_tab(driver, url=None)
    driver.get.assert_called_once_with("https://www.google.com")


# ---------------------------------------------------------------------------
# switch_tab
# ---------------------------------------------------------------------------


def test_switch_tab_by_index():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    switch_tab(driver, index=2)
    driver.switch_to.window.assert_called_once_with("h2")


def test_switch_tab_by_title_searches_handles():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    # title changes as we iterate — mock side effects
    titles = {"h0": "Home", "h1": "About", "h2": "Contact"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    switch_tab(driver, title="About")

    # resolves to the tab titled "About" (h1) and ends focused there
    assert driver.switch_to.window.call_args_list[-1] == call("h1")


def test_switch_tab_with_index_and_title_validates_title_after_switch():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    titles = {"h0": "Home", "h1": "About", "h2": "Contact"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    # First switch to index=0 → "Home", then search for "About"
    driver.title = "Home"

    switch_tab(driver, index=0, title="About")

    # switched to h0 first (by index), then searched and found h1
    calls = driver.switch_to.window.call_args_list
    assert calls[0] == call("h0")
    assert call("h1") in calls


def test_switch_tab_raises_on_neither_arg():
    driver = _make_driver()
    with pytest.raises(ValueError, match="switch_tab requires index or title"):
        switch_tab(driver)


def test_switch_tab_title_not_found_raises():
    driver = _make_driver(handles=["h0", "h1"])
    titles = {"h0": "Home", "h1": "About"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    with pytest.raises(NoSuchWindowException):
        switch_tab(driver, title="Missing")


# ---------------------------------------------------------------------------
# switch_tab — URL-aware matching (V2-authored "switch to tab with URL X")
# ---------------------------------------------------------------------------


def test_switch_tab_by_url_host_when_no_title_match():
    """Bare-domain identifier with no matching title resolves by URL host.

    Repro of the V2->V3 export bug: a "switch to tab with url github.com" op is
    emitted as ``switch_tab(driver, index=0, title='github.com')``. No tab's
    title equals 'github.com', so the tab must be found by its URL host.
    """
    tabs = [
        ("h0", "Google", "https://www.google.com/"),
        ("h1", "GitHub: where the world builds", "https://github.com/some/repo"),
    ]
    driver = _make_url_driver(tabs)
    switch_tab(driver, index=0, title="github.com")
    assert driver.switch_to.window.call_args_list[-1] == call("h1")


def test_switch_tab_url_host_excludes_subdomain():
    """A bare-domain identifier matches the exact host, not a subdomain."""
    tabs = [
        ("h0", "Gist", "https://gist.github.com/abc"),
        ("h1", "Repo", "https://github.com/owner/repo"),
    ]
    driver = _make_url_driver(tabs)
    switch_tab(driver, title="github.com")
    assert driver.switch_to.window.call_args_list[-1] == call("h1")


def test_switch_tab_url_host_excludes_lookalike():
    """'github.com' must not match a look-alike host 'github.com.evil.com'."""
    tabs = [
        ("h0", "Phish", "https://github.com.evil.com/login"),
        ("h1", "Real", "https://github.com/"),
    ]
    driver = _make_url_driver(tabs)
    switch_tab(driver, title="github.com")
    assert driver.switch_to.window.call_args_list[-1] == call("h1")


def test_switch_tab_exact_title_preferred_over_url_host():
    """An exact title match wins over a URL-host match on another tab."""
    tabs = [
        ("h0", "github.com", "https://example.com/"),
        ("h1", "Other", "https://github.com/"),
    ]
    driver = _make_url_driver(tabs)
    switch_tab(driver, title="github.com")
    assert driver.switch_to.window.call_args_list[-1] == call("h0")


def test_switch_tab_by_exact_url_with_path():
    """A full authored URL matches by host + path prefix."""
    tabs = [
        ("h0", "A", "https://example.com/home"),
        ("h1", "B", "https://example.com/checkout?step=2"),
    ]
    driver = _make_url_driver(tabs)
    switch_tab(driver, title="https://example.com/checkout")
    assert driver.switch_to.window.call_args_list[-1] == call("h1")


def test_switch_tab_multiple_matches_warns_and_picks_first(caplog):
    """Genuine duplicates (same host) → first-in-order + a warning log."""
    tabs = [
        ("h0", "First", "https://github.com/a"),
        ("h1", "Second", "https://github.com/b"),
    ]
    driver = _make_url_driver(tabs)
    with caplog.at_level(logging.WARNING):
        switch_tab(driver, title="github.com")
    assert driver.switch_to.window.call_args_list[-1] == call("h0")
    assert any("matched identifier" in r.message for r in caplog.records)


def test_switch_tab_url_identifier_not_found_raises():
    """A URL identifier with no host match raises (no silent pass)."""
    tabs = [
        ("h0", "A", "https://example.com/"),
        ("h1", "B", "https://other.com/"),
    ]
    driver = _make_url_driver(tabs)
    with pytest.raises(NoSuchWindowException):
        switch_tab(driver, title="github.com")


# ---------------------------------------------------------------------------
# close_tab
# ---------------------------------------------------------------------------


def test_close_tab_current_when_no_args():
    driver = _make_driver(handles=["h0", "h1"])
    close_tab(driver)
    driver.close.assert_called_once()
    driver.switch_to.window.assert_called_once_with("h1")


def test_close_tab_by_index_then_switches_to_last():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    close_tab(driver, index=1)
    driver.switch_to.window.assert_any_call("h1")
    driver.close.assert_called_once()
    # final switch is to handles[-1] = "h2"
    assert driver.switch_to.window.call_args_list[-1] == call("h2")


def test_close_tab_by_title():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    titles = {"h0": "Home", "h1": "Target", "h2": "Other"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    close_tab(driver, title="Target")

    # Should have found and switched to h1, closed, then switched to last
    switch_calls = driver.switch_to.window.call_args_list
    assert call("h1") in switch_calls
    driver.close.assert_called_once()
    assert switch_calls[-1] == call("h2")


def test_close_tab_by_url_host():
    """close_tab resolves a bare-domain identifier by URL host, then closes it."""
    tabs = [
        ("h0", "Google", "https://google.com/"),
        ("h1", "GitHub", "https://github.com/owner/repo"),
        ("h2", "Other", "https://other.com/"),
    ]
    driver = _make_url_driver(tabs)
    close_tab(driver, title="github.com")
    switch_calls = driver.switch_to.window.call_args_list
    assert call("h1") in switch_calls
    driver.close.assert_called_once()
    assert switch_calls[-1] == call("h2")  # final switch to last handle


def test_close_tab_with_index_and_title():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    titles = {"h0": "Home", "h1": "About", "h2": "Target"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    # index=0 → "Home", but title="Target" → should search and find h2
    close_tab(driver, index=0, title="Target")

    switch_calls = driver.switch_to.window.call_args_list
    assert call("h2") in switch_calls
    driver.close.assert_called_once()
    assert switch_calls[-1] == call("h2")


def test_switch_tab_partial_title_contains_match():
    """Grid-found: authored 'IP Data Intelligence' vs real title
    'IP Data Intelligence & API Provider | IPinfo' — authors type fragments;
    V2 never title-matched at all, so exact-only is stricter than any authored
    expectation. Case-insensitive contains is the last tier."""
    driver = _make_driver(handles=["h0", "h1"])
    titles = {"h0": "Dashboard", "h1": "IP Data Intelligence & API Provider | IPinfo"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Dashboard"

    switch_tab(driver, index=0, title="IP Data Intelligence")

    assert driver.switch_to.window.call_args_list[-1] == call("h1")


def test_switch_tab_title_case_insensitive_exact():
    driver = _make_driver(handles=["h0", "h1"])
    titles = {"h0": "Home", "h1": "GitHub"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    switch_tab(driver, title="github")

    assert driver.switch_to.window.call_args_list[-1] == call("h1")


def test_switch_tab_exact_title_beats_substring():
    """A tab titled exactly 'News' wins over one merely containing 'News'."""
    driver = _make_driver(handles=["h0", "h1"])
    titles = {"h0": "Breaking News Today", "h1": "News"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Breaking News Today"

    switch_tab(driver, title="News")

    assert driver.switch_to.window.call_args_list[-1] == call("h1")


# ---------------------------------------------------------------------------
# automind intent resolution (V2 kaneai_switch_tab_heal parity)
# ---------------------------------------------------------------------------

def _automind_env(monkeypatch):
    monkeypatch.setenv("LT_USERNAME", "user")
    monkeypatch.setenv("LT_ACCESS_KEY", "key")
    import testmu_selenium
    monkeypatch.setattr(
        testmu_selenium._config, "get",
        lambda k, d=None: "https://automind.test" if k == "automind_url" else d,
    )


def _mk_close_driver():
    """3 tabs: C=ipinfo (index 0), A=postman (1, CURRENT), B=github (2)."""
    driver = _make_driver(handles=["hC", "hA", "hB"])
    titles = {"hC": "IP Data Intelligence | IPinfo", "hA": "Postman", "hB": "GitHub"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.current_window_handle = "hA"
    driver.title = titles["hA"]
    driver.session_id = "sess-1"
    driver.capabilities = {"platformName": "linux"}
    return driver


def test_close_tab_description_resolves_via_automind(monkeypatch):
    """Grid-found: 'Close the current tab' emitted close_tab(index=0) and
    killed the ipinfo tab. With a description, automind resolves the CURRENT
    tab (index 1) and the placeholder index is ignored."""
    _automind_env(monkeypatch)
    driver = _mk_close_driver()

    import testmu_selenium._helpers.tabs as tabs_mod
    resp = MagicMock(status_code=200)
    resp.json.return_value = {"tab_index": 1, "tab_title": "Postman"}
    post = MagicMock(return_value=resp)
    monkeypatch.setattr(tabs_mod.httpx, "post", post)

    close_tab(driver, index=0, description="Close the current tab")

    assert driver.close.called
    # last switch BEFORE close targeted hA (automind's index 1), not hC (index 0)
    switch_calls = [c.args[0] for c in driver.switch_to.window.call_args_list]
    close_pos_target = switch_calls[-2]  # [-1] is the post-close switch to handles[-1]
    assert close_pos_target == "hA"
    body = post.call_args.kwargs["json"]
    assert body["operation_type"] == "CLOSE_TAB"
    assert body["intent"] == "Close the current tab"
    assert body["open_tabs"] == ["IP Data Intelligence | IPinfo", "Postman", "GitHub"]


def test_close_tab_automind_error_falls_back_to_index(monkeypatch):
    _automind_env(monkeypatch)
    driver = _mk_close_driver()

    import testmu_selenium._helpers.tabs as tabs_mod
    monkeypatch.setattr(tabs_mod.httpx, "post", MagicMock(side_effect=RuntimeError("down")))

    close_tab(driver, index=0, description="Close the current tab")

    assert driver.close.called
    switch_calls = [c.args[0] for c in driver.switch_to.window.call_args_list]
    assert switch_calls[-2] == "hC"  # fallback to authored index 0


def test_switch_tab_identifier_miss_rescued_by_automind(monkeypatch):
    _automind_env(monkeypatch)
    driver = _mk_close_driver()

    import testmu_selenium._helpers.tabs as tabs_mod
    resp = MagicMock(status_code=200)
    resp.json.return_value = {"tab_index": 0}
    monkeypatch.setattr(tabs_mod.httpx, "post", MagicMock(return_value=resp))

    switch_tab(driver, index=0, title="Nowhere To Be Found",
               description="Switch to the IP data tab")

    assert driver.switch_to.window.call_args_list[-1] == call("hC")


def test_switch_tab_identifier_miss_automind_down_still_raises(monkeypatch):
    _automind_env(monkeypatch)
    driver = _mk_close_driver()

    import testmu_selenium._helpers.tabs as tabs_mod
    monkeypatch.setattr(tabs_mod.httpx, "post", MagicMock(side_effect=RuntimeError("down")))

    with pytest.raises(NoSuchWindowException):
        switch_tab(driver, title="Nowhere To Be Found", description="whatever")
