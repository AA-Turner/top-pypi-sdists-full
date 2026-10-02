"""The public surface the code generator emits calls against.

`BINDING_PUBLIC_SURFACE` below is the reconciled binding↔generator contract. The
cgf lane's `test_verb_table.BINDING_PUBLIC_SURFACE` carries the SAME table; the two
must be edited together, because between them they are the only thing standing
between a renamed parameter and a generated test that fails at replay time.

Each row is `verb → (target_mode, {every accepted keyword parameter})`. The
parameter set is exact, not a subset: an ADDED parameter fails this test just as a
removed one does, so a widening on either side has to be agreed rather than
discovered.
"""
import inspect

import pytest

import testmu_appium

#: verb → (target_mode, exact set of accepted keyword parameters, excluding `driver`)
BINDING_PUBLIC_SURFACE = {
    # ── Element mode: settle → find → act → heal. Always takes `selectors`. ──
    "click": ("element", {
        "selectors", "description", "fallback_coordinates", "click_modifier",
        "surface", "frame_path", "grounded_by",
    }),
    "type": ("element", {
        "selectors", "text", "description", "fallback_coordinates",
        "clear_first", "delay_ms", "multiple_inputs", "manual_interaction_tag",
        "surface", "frame_path", "grounded_by",
    }),
    "search": ("element", {
        "selectors", "text", "description", "fallback_coordinates",
        "clear_first", "submit_key", "delay_ms",
        "multiple_inputs", "manual_interaction_tag",
        "surface", "frame_path", "grounded_by",
    }),
    "clear": ("element", {
        "selectors", "description", "fallback_coordinates", "grounded_by",
    }),
    "select": ("element", {
        "selectors", "value", "label", "index", "description", "mode",
        "fallback_coordinates",
    }),
    "scroll": ("element", {
        "selectors", "kind", "direction", "value", "description",
        "fallback_coordinates",
    }),
    "scroll_until": ("element", {
        "selectors", "description", "direction", "condition", "container_selectors",
        "max_scrolls", "visibility_threshold", "fallback_coordinates",
        "surface", "frame_path",
    }),

    # ── Mode-polymorphic: selectors decide, as they do for `scroll`. With them
    #    the control is found and the gesture measured against the live screen;
    #    without them, two recorded bases and no element. ──
    "drag": ("element", {
        "selectors", "source_coordinates", "target_coordinates",
        "direction", "fraction", "source_description", "target_description",
        "grounded_by", "target_selectors", "target_grounded_by",
        "hold_duration_ms", "move_duration_ms", "hold_at_destination_ms",
        "description",
    }),

    # ── Driver mode: acts on the session. Never takes `selectors`. ──
    "navigate": ("driver", {"url", "package", "description"}),
    "keyevent": ("driver", {"key", "description"}),
    "app_lifecycle": ("driver", {"kind", "app_id", "duration_ms", "description"}),
    "device_control": ("driver", {"kind", "value", "description"}),
    "device_control_query": ("driver", {"kind", "description"}),
    "set_geolocation": ("driver", {"latitude", "longitude", "description"}),
    "wait": ("driver", {"seconds", "ms", "description"}),
    "smartui_screenshot": ("driver", {"name", "description"}),
    "set_cookies": ("driver", {"cookies", "description"}),
    "delete_cookies": ("driver", {"names", "description"}),
    "clear_cookies": ("driver", {"description"}),
    "set_local_storage": ("driver", {"items", "description"}),
    "delete_local_storage": ("driver", {"keys", "description"}),
    "clear_local_storage": ("driver", {"description"}),
    "set_clipboard": ("driver", {"text", "description"}),
    "paste_clipboard": ("driver", {"description"}),
    "clear_clipboard": ("driver", {"description"}),
    "go_back": ("driver", {"surface", "description"}),
    "go_forward": ("driver", {"surface", "description"}),
    "refresh": ("driver", {"surface", "description"}),
    "accessibility_scan": ("driver", {"description"}),
    "new_tab": ("driver", {"url"}),
    "switch_tab": ("driver", {"index", "title"}),
    "close_tab": ("driver", {"index", "title"}),
    "inject_media": ("driver", {"kind", "media_id", "description"}),
    "network_throttle": ("driver", {
        "profile", "download_kbps", "upload_kbps", "latency_ms", "description",
    }),
    "network_mock": ("driver", {
        "action", "uid", "urls", "configurations", "description",
    }),

    # ── Value / query. The tree-shaped pair is what the generator emits. ──
    "verify_assertion": ("driver", {"tree", "description", "return_result"}),
    "evaluate_math": ("value", {"tree", "output_variable", "description"}),
    "evaluate_branch": ("value", {"sub_checks", "composite_operator"}),
    "check_until_condition": ("driver", {"condition", "perception"}),
    "execute_kane_cli": ("driver", {"objective", "description"}),
    "assertion": ("driver", {
        "claim", "composite_operator", "sub_checks", "description",
    }),
    "math": ("value", {"expression", "output_variable", "description"}),
    "textual_query": ("driver", {
        "query", "description", "output_variable", "return_type", "expected_value",
        "selectors", "selected_attribute_name",
    }),
    "vision_query": ("driver", {
        "query", "description", "output_variable", "return_type", "expected_value",
        "perception",
    }),
    "execute_api": ("value", {
        "method", "url", "headers", "body", "params", "authorization",
        "timeout", "timeout_ms", "verify", "settings", "output_variable", "description",
    }),
    "execute_js": ("driver", {
        "script", "timeout_sec", "output_variable", "description",
    }),
    "execute_db": ("value", {
        "query", "db_id", "db_name", "timeout", "tunnel_id", "auth_header",
        "automind_url", "output_variable", "description",
    }),
    "network_query": ("driver", {
        "method", "url", "index", "network_log_id",
        "polling_interval", "max_polling_time", "output_variable", "description",
    }),
    "network_capture_query": ("driver", {"contract"}),
    "network_capture_capabilities": ("value", set()),
    "evaluate_network_assertion": ("value", {"assertion_tree", "contract_version"}),
    "textual_analyzer": ("driver", {
        "code", "capture_baseline", "extraction_description",
    }),
    "textual_analyzer_authoring": ("driver", {"code"}),
}

#: Verbs whose first positional parameter is the live driver. "value" verbs are
#: pure — they never touch the device, so the generator emits them without one.
_TAKES_DRIVER = {
    name for name, (mode, _) in BINDING_PUBLIC_SURFACE.items() if mode != "value"
}

#: configure() keys the generator may emit.
CONFIGURE_KEYS = {
    "app_id", "platform", "udid", "target_kind",
    "device_name", "platform_version", "no_reset", "app",
    "appium_version",
    "tc_id", "environment_id", "uploaded_files",
    "build", "name", "capability", "custom_capabilities", "lt_options",
    "lt_options_fixed", "driver_settings", "test_metadata",
    "kane_version", "kane_run_v4",
    "default_action_timeout_ms", "settle_timeout_ms", "heal_timeout_ms",
    "new_command_timeout_s",
    "username", "accesskey", "test_id", "commit_id", "org_id",
    "appium_url", "lt_hub_url", "ai_api_host", "automind_url",
    "smart", "heal", "test_params", "variables", "global_variables",
    "screenshot_source", "mjpeg_port",
    "iwdp_binary",
}

LIFECYCLE = [
    "configure", "test_config_overrides", "test", "run", "step",
    "var", "set_var", "get_variable_value", "resolve_variable",
    "route_failure", "get_driver",
]

ERRORS = [
    "TestmuConfigError", "UnsupportedOnPlatform", "UnknownStrategy", "UnknownKeyEvent",
    "ElementNotFound", "ElementBlocked", "CoordinateFallbackUnavailable",
    "SmartUINotAvailable", "PickerModeNotSupported", "NetworkQueryUnavailable",
    "NetworkMockUnavailable",
    "ScreenshotUnavailable",
    "WebSurfaceUnavailable",
    "ViewportCaptureError", "DegenerateViewportCaptureError", "UnsupportedTreeContract",
    "ViewportSelectionDriftError", "ViewportResultMissError", "ViewportScriptCompileError",
    "ViewportScriptPolicyError", "ViewportScriptTimeoutError",
    "ViewportScriptRuntimeError", "ViewportResultTypeError",
    "NetworkCaptureError", "NetworkCaptureUnavailable", "NetworkCaptureTimeout",
    "NetworkCaptureNotFound", "NetworkCaptureContractError", "NetworkAssertionError",
]


def _parameters(name):
    return inspect.signature(getattr(testmu_appium, name)).parameters


@pytest.mark.parametrize("name", sorted(BINDING_PUBLIC_SURFACE))
def test_every_verb_is_exported_and_callable(name):
    assert name in testmu_appium.__all__
    assert callable(getattr(testmu_appium, name))


@pytest.mark.parametrize("name,expected", sorted(
    (n, params) for n, (_, params) in BINDING_PUBLIC_SURFACE.items()
))
def test_verb_signature_matches_the_contract_exactly(name, expected):
    actual = set(_parameters(name)) - {"driver"}
    assert actual == expected, (
        f"{name}() drifted from the contract — "
        f"missing {sorted(expected - actual)}, unexpected {sorted(actual - expected)}"
    )


@pytest.mark.parametrize("name", sorted(_TAKES_DRIVER))
def test_device_verbs_take_the_driver_first(name):
    parameters = list(_parameters(name))
    assert parameters[0] == "driver", f"{name}() must take driver as its first parameter"


def test_tab_required_parameters_match_codegen():
    assert _parameters("new_tab")["url"].default is None
    assert _parameters("switch_tab")["index"].default is inspect.Parameter.empty
    assert _parameters("switch_tab")["title"].default is None
    assert _parameters("close_tab")["index"].default is None
    assert _parameters("close_tab")["title"].default is None


@pytest.mark.parametrize("name", sorted(
    set(BINDING_PUBLIC_SURFACE) - _TAKES_DRIVER
))
def test_value_verbs_take_no_driver(name):
    assert "driver" not in _parameters(name)


@pytest.mark.parametrize("name", sorted(
    n for n, (mode, _) in BINDING_PUBLIC_SURFACE.items() if mode == "element"
))
def test_element_verbs_take_selectors_and_a_description(name):
    parameters = _parameters(name)
    assert "selectors" in parameters
    assert "description" in parameters


@pytest.mark.parametrize("name", sorted(
    n for n, (mode, _) in BINDING_PUBLIC_SURFACE.items()
    if mode != "element" and n != "textual_query"
))
def test_non_element_verbs_never_take_selectors(name):
    assert "selectors" not in _parameters(name)


def test_textual_query_accepts_selectors_without_becoming_an_element_verb():
    """Its selectors opportunistically read a value; they never act or heal."""
    assert BINDING_PUBLIC_SURFACE["textual_query"][0] == "driver"
    assert "selectors" in _parameters("textual_query")


@pytest.mark.parametrize("name", sorted(
    n for n, (mode, _) in BINDING_PUBLIC_SURFACE.items()
    if mode == "element" and n not in ("scroll_until", "drag")
))
def test_element_verbs_accept_the_recorded_coordinate_basis(name):
    """Every element verb accepts fallback_coordinates; whether it can USE one is
    the verb's own decision (clear and the scroll family deliberately cannot).
    scroll_until accepts it too but is excluded from the "must use" reading."""
    assert "fallback_coordinates" in _parameters(name)


def test_an_element_drag_has_no_positional_fallback_at_all():
    """drag is the one element verb that does not even ACCEPT the fallback.

    A recorded position describes the layout that has just failed to produce the
    element, and a drag aimed at the wrong place moves something rather than
    missing it. Its bases are carried as provenance under other names and are
    never a resolution path.
    """
    assert "fallback_coordinates" not in _parameters("drag")


@pytest.mark.parametrize("name", sorted(
    n for n, (_, params) in BINDING_PUBLIC_SURFACE.items() if "description" in params
))
def test_description_is_the_heal_intent_carrier(name):
    """`description` reaches autoheal as action_instruction, so every verb that can
    heal — and every verb that reports a step — has to accept it."""
    assert _parameters(name)["description"].default == ""


@pytest.mark.parametrize("name", LIFECYCLE + ERRORS)
def test_lifecycle_and_error_surface_is_exported(name):
    assert name in testmu_appium.__all__
    assert getattr(testmu_appium, name) is not None


#: Exported for external consumers (the v16 runner and auteur) to parse a page
#: source; not callable steps, so they carry no verb contract row.
PERCEPTION = [
    "parse_tree", "format_for_prompt", "find_by_fingerprint", "position_hint",
    "ELEMENT_CONTRACT", "get_tabs",
]


@pytest.mark.parametrize("name", PERCEPTION)
def test_perception_surface_is_exported(name):
    assert name in testmu_appium.__all__
    assert getattr(testmu_appium, name) is not None


def test_contract_covers_every_exported_verb():
    """No verb may reach the public surface without a row in the contract."""
    non_verbs = set(LIFECYCLE) | set(ERRORS) | set(PERCEPTION) | {
        "HealHit", "HealNoMatch", "HealUnavailable", "HealDisabled", "HealProtocolError",
    }
    exported_verbs = set(testmu_appium.__all__) - non_verbs
    assert exported_verbs == set(BINDING_PUBLIC_SURFACE)


def test_configure_accepts_exactly_the_contract_keys():
    from testmu_appium._configure import _ALLOWED_KWARGS

    assert _ALLOWED_KWARGS == CONFIGURE_KEYS


def test_configure_rejects_a_key_outside_the_contract():
    from testmu_appium._errors import TestmuConfigError

    with pytest.raises(TestmuConfigError):
        testmu_appium.configure(action_timeout_ms=5000)


def test_the_tree_shaped_pair_is_what_the_generator_emits():
    """verify_assertion/evaluate_math take the recorded tree; assertion/math are the
    flat-argument forms behind them. Both pairs stay exported."""
    assert "tree" in _parameters("verify_assertion")
    assert "tree" in _parameters("evaluate_math")
    assert "sub_checks" in _parameters("assertion")
    assert "expression" in _parameters("math")


def test_version_is_exposed():
    assert testmu_appium.__version__


def test_importing_the_package_does_not_start_a_session():
    """Import must be inert: the generated test.py imports at module top, long
    before run() decides which target to connect to."""
    from testmu_appium._helpers.driver import get_driver

    assert get_driver() is None


def test_import_does_not_mutate_the_environment():
    import importlib
    import os

    before = dict(os.environ)
    importlib.reload(testmu_appium)
    assert dict(os.environ) == before
