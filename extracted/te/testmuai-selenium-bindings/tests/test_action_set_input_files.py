"""Tests for testmu_selenium.set_input_files — high-level upload wrapper.

Strategy: stub _run_action at the wrapper-module path so we can assert the
runtime kwargs/spec the wrapper threads through, without exercising the
full engine again (engine itself is covered in test_action_engine.py).

Groups:
  A — kwarg threading (selector, description, file_path, file_paths, autoheal, tiers)
  B — _set_input_files_runner invokes element.send_keys(file path)
  C — spec uses default recoverable exceptions
  D — coord_runner bridges a DESKTOP_LOCATE-healed pixel to the file <input> via
      elementFromPoint+JS. A bare coordinate has no <input> to send_keys to, so the
      coord_runner JS resolver is the glue that makes DESKTOP_LOCATE usable for upload.
"""
import pytest
from unittest.mock import MagicMock, patch

from testmu_selenium import _action_set_input_files as sif
from testmu_selenium._action_set_input_files import (
    set_input_files, _SET_INPUT_FILES_SPEC, _set_input_files_runner,
    _set_input_files_coord_runner, _RESOLVE_FILE_INPUT_JS,
    _resolve_file_input_dom, _FIND_FIRST_FILE_INPUT_JS,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE
from selenium.common.exceptions import NoSuchElementException


PRIMARY = [{"selector": "//input[@type='file']", "isXPath": True}]


# ---------------------------------------------------------------------------
# Group A — kwarg threading
# ---------------------------------------------------------------------------

def test_set_input_files_calls_run_action_with_spec():
    """set_input_files() routes through _run_action, passing the spec + selector."""
    driver = MagicMock(name="driver")
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        result = set_input_files(driver, PRIMARY, file_path="/tmp/sample.txt")

    assert result is None
    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _SET_INPUT_FILES_SPEC
    assert args[2] is PRIMARY


def test_set_input_files_threads_file_path_as_runner_kwarg():
    """file_path must reach the runner via runner_kwargs (engine forwards to ctx)."""
    driver = MagicMock(name="driver")
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, PRIMARY, file_path="/tmp/sample.txt")

    kw = m_run.call_args.kwargs
    assert kw["file_path"] == "/tmp/sample.txt"
    assert kw["file_paths"] is None


def test_set_input_files_threads_file_paths_as_runner_kwarg():
    driver = MagicMock(name="driver")
    paths = ["/tmp/a.txt", "/tmp/b.txt"]
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, PRIMARY, file_paths=paths)

    kw = m_run.call_args.kwargs
    assert kw["file_paths"] == paths
    assert kw["file_path"] is None


def test_set_input_files_threads_description_kwarg():
    driver = MagicMock(name="driver")
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, PRIMARY, file_path="/tmp/x", description="choose file")

    kw = m_run.call_args.kwargs
    assert kw["description"] == "choose file"


def test_set_input_files_threads_autoheal_false():
    driver = MagicMock(name="driver")
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, PRIMARY, file_path="/tmp/x", autoheal=False)

    kw = m_run.call_args.kwargs
    assert kw["autoheal"] is False


def test_set_input_files_threads_tiers_kwarg():
    driver = MagicMock(name="driver")
    custom_tiers = ["LIST_XPATHS"]
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, PRIMARY, file_path="/tmp/x", tiers=custom_tiers)

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == custom_tiers  # explicit tiers always win


def test_set_input_files_default_tiers():
    """Default tier is DESKTOP_LOCATE only. LIST_XPATHS is dropped: it 'succeeds'
    on any non-empty xpaths list (even an unusable relative xpath), so as the first
    tier it monopolized the retry budget and the working coordinate tier never ran
    (observed in production: 3× LIST_XPATHS, 0× coordinate, upload failed).
    VISION_QUERY stays out (needs absent tagify). DESKTOP_LOCATE (/v2/locate/desktop
    — viewport screenshot) is the working tier for upload heal.
    Reverting _HEAL_TIERS to ('COORDINATE',) turns this RED."""
    driver = MagicMock(name="driver")
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, PRIMARY, file_path="/tmp/x")  # no tiers passed

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == ("DESKTOP_LOCATE",)
    assert "LIST_XPATHS" not in kw["tiers"]
    assert "VISION_QUERY" not in kw["tiers"]
    assert "COORDINATE" not in kw["tiers"]


def test_resolve_file_input_js_is_shadow_aware():
    """The coord_runner's resolver must cross OPEN shadow boundaries and have a
    global fallback — elementFromPoint alone misses inputs nested in shadow
    roots or scrolled below the fold (prod page domComplexity=shadow, input at
    y=2166 in an open shadow root). Reverting to the light-DOM-only
    elementFromPoint/querySelector resolver fails this."""
    assert "shadowRoot" in _RESOLVE_FILE_INPUT_JS, \
        "resolver must recurse open shadow roots"
    assert "getRootNode" in _RESOLVE_FILE_INPUT_JS, \
        "resolver must ascend out of shadow roots via getRootNode()"


# ---------------------------------------------------------------------------
# Group B — _set_input_files_runner invokes element.send_keys(path)
# ---------------------------------------------------------------------------

def test_runner_sends_single_file_path():
    """Runner reads file_path from ctx and calls element.send_keys(str(path))."""
    element = MagicMock(name="element")
    ctx = {"driver": MagicMock(), "frame_info": None,
           "file_path": "/tmp/sample.txt", "file_paths": None}

    result = _set_input_files_runner(element, ctx)

    element.send_keys.assert_called_once_with("/tmp/sample.txt")
    assert result is None


def test_runner_sends_multiple_file_paths_newline_joined():
    """Selenium multi-upload convention: newline-join the paths in one send_keys."""
    element = MagicMock(name="element")
    ctx = {"driver": MagicMock(), "frame_info": None,
           "file_path": None, "file_paths": ["/tmp/a.txt", "/tmp/b.txt"]}

    _set_input_files_runner(element, ctx)

    element.send_keys.assert_called_once_with("/tmp/a.txt\n/tmp/b.txt")


def test_runner_prefers_file_paths_when_both_present():
    """If both supplied, file_paths (the list form) wins."""
    element = MagicMock(name="element")
    ctx = {"driver": MagicMock(), "frame_info": None,
           "file_path": "/tmp/single.txt", "file_paths": ["/tmp/a.txt"]}

    _set_input_files_runner(element, ctx)

    element.send_keys.assert_called_once_with("/tmp/a.txt")


# ---------------------------------------------------------------------------
# Group C — default recoverable
# ---------------------------------------------------------------------------

def test_spec_uses_default_recoverable():
    assert _SET_INPUT_FILES_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


# ---------------------------------------------------------------------------
# Group D — coord_runner bridges a healed coordinate to the file <input>
# ---------------------------------------------------------------------------

def test_spec_has_coord_runner():
    """DESKTOP_LOCATE is a usable tier for upload via the elementFromPoint bridge,
    so the spec wires the coord_runner (the engine dispatches to it when the
    heal cascade resolves to viewport coordinates)."""
    assert _SET_INPUT_FILES_SPEC.coord_runner is _set_input_files_coord_runner


def test_coord_runner_resolves_element_and_sends_keys():
    """coord_runner resolves the file input via execute_script(elementFromPoint
    JS) and send_keys the path to it."""
    driver = MagicMock(name="driver")
    element = MagicMock(name="element")
    driver.execute_script.return_value = element
    ctx = {"driver": driver, "frame_info": None,
           "file_path": "/tmp/sample.txt", "file_paths": None}

    result = _set_input_files_coord_runner(driver, 100, 200, ctx)

    driver.execute_script.assert_called_once()
    args = driver.execute_script.call_args.args
    assert args[1:] == (100, 200)  # x, y threaded to the resolver JS
    element.send_keys.assert_called_once_with("/tmp/sample.txt")
    assert result is None


def test_coord_runner_raises_when_no_file_input_resolved():
    """If elementFromPoint resolves nothing (execute_script -> None), the runner
    raises NoSuchElementException rather than calling send_keys on None."""
    driver = MagicMock(name="driver")
    driver.execute_script.return_value = None
    ctx = {"driver": driver, "frame_info": None,
           "file_path": "/tmp/sample.txt", "file_paths": None}

    with pytest.raises(NoSuchElementException):
        _set_input_files_coord_runner(driver, 1, 2, ctx)


# ---------------------------------------------------------------------------
# Group E — selectorless (empty selector) DOM-first resolution
#
# V2 parity: handle_upload located the <input type=file> via PURE DOM (no
# vision/coordinates). The Vision Agent can persist an upload op with no
# selector at all (selector absent), which codegen emits as
# set_input_files(driver, [], description='choose file'). The ONLY runtime
# fallback was the COORDINATE vision heal, which dies when no visible "choose
# file" element exists (prod: AutohealExhausted "Coordinates not resolved for
# choose file"). DOM-first restores V2 handle_upload: find input[type=file]
# across light + open shadow, first match wins (V2 Strategy 3), no vision.
# ---------------------------------------------------------------------------

def test_empty_selector_resolves_via_dom_then_send_keys():
    """Empty selector + a file input present in the DOM: resolve it directly and
    send_keys, WITHOUT entering _run_action / the vision heal cascade."""
    driver = MagicMock(name="driver")
    element = MagicMock(name="file_input")
    driver.execute_script.return_value = element  # DOM probe finds the input
    with patch.object(sif, "_run_action") as m_run:
        result = set_input_files(driver, [], file_path="/tmp/sample.txt",
                                 description="choose file")

    element.send_keys.assert_called_once_with("/tmp/sample.txt")
    m_run.assert_not_called()
    assert result is None


def test_empty_selector_dom_miss_falls_back_to_run_action():
    """Empty selector but no file input in the DOM (probe -> None): fall through
    to _run_action (existing COORDINATE heal), unchanged."""
    driver = MagicMock(name="driver")
    driver.execute_script.return_value = None  # DOM probe misses
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, [], file_path="/tmp/sample.txt",
                        description="choose file")

    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[2] == []  # selector still threaded through unchanged


def test_empty_selector_dom_multiple_paths_newline_joined():
    """DOM-first honours the multi-file send_keys convention (newline-joined)."""
    driver = MagicMock(name="driver")
    element = MagicMock(name="file_input")
    driver.execute_script.return_value = element
    with patch.object(sif, "_run_action"):
        set_input_files(driver, [], file_paths=["/tmp/a.txt", "/tmp/b.txt"])

    element.send_keys.assert_called_once_with("/tmp/a.txt\n/tmp/b.txt")


def test_nonempty_selector_does_not_use_dom_first():
    """A present selector takes the normal find path; no DOM-first probe."""
    driver = MagicMock(name="driver")
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, PRIMARY, file_path="/tmp/x")

    driver.execute_script.assert_not_called()  # DOM-first skipped
    m_run.assert_called_once()


def test_dom_first_skipped_when_search_root_set():
    """A shadow-context search_root constrains the find; don't global-search the
    whole document for a file input. Defer to _run_action."""
    driver = MagicMock(name="driver")
    root = MagicMock(name="shadow_root")
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, [], file_path="/tmp/x", search_root=root)

    driver.execute_script.assert_not_called()
    m_run.assert_called_once()
    assert m_run.call_args.kwargs["search_root"] is root


def test_dom_first_skipped_when_autoheal_false():
    """autoheal=False means strict find with no relocation; DOM discovery (the
    parity replacement for the heal) is also suppressed."""
    driver = MagicMock(name="driver")
    with patch.object(sif, "_run_action") as m_run:
        set_input_files(driver, [], file_path="/tmp/x", autoheal=False)

    driver.execute_script.assert_not_called()
    m_run.assert_called_once()


def test_dom_first_send_keys_error_falls_back_to_run_action():
    """If the resolved element rejects send_keys (detached/non-interactable),
    DOM-first must not propagate — fall through to _run_action."""
    driver = MagicMock(name="driver")
    element = MagicMock(name="file_input")
    element.send_keys.side_effect = RuntimeError("stale element")
    driver.execute_script.return_value = element
    with patch.object(sif, "_run_action", return_value=None) as m_run:
        set_input_files(driver, [], file_path="/tmp/x", description="choose file")

    m_run.assert_called_once()


def test_resolve_file_input_dom_returns_probe_result():
    """_resolve_file_input_dom runs the JS probe and returns its element, None on
    a thrown error (never raises)."""
    driver = MagicMock(name="driver")
    el = MagicMock(name="el")
    driver.execute_script.return_value = el
    assert _resolve_file_input_dom(driver) is el

    driver.execute_script.side_effect = RuntimeError("boom")
    assert _resolve_file_input_dom(driver) is None


def test_find_first_file_input_js_is_shadow_aware_no_visibility_filter():
    """The probe must recurse OPEN shadow roots and must NOT filter by
    visibility — file inputs are commonly display:none behind a styled trigger
    (the exact case that broke coordinate-heal); send_keys works on hidden
    inputs."""
    assert "shadowRoot" in _FIND_FIRST_FILE_INPUT_JS, \
        "probe must recurse open shadow roots"
    assert "input[type=file]" in _FIND_FIRST_FILE_INPUT_JS
    for visibility_token in ("offsetParent", "getBoundingClientRect", "visible", "offsetWidth"):
        assert visibility_token not in _FIND_FIRST_FILE_INPUT_JS, \
            f"probe must NOT filter by visibility (found {visibility_token!r})"
