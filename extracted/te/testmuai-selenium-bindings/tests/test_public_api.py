"""Public API drift gate.

Asserts __all__ contains every symbol the V3 codegen emits as a bare reference
in generated test.py. Drift here surfaces immediately as a test failure.
"""
import testmu_selenium


# This list MUST stay in sync with the symbols emitted by V3 codegen
# in the V3 Python/Selenium code generator module.
EXPECTED_BARE_SYMBOLS = {
    # Lifecycle
    "configure", "test", "run", "step",
    # Variable store
    "var", "set_var",
    # Runtime helpers
    "findElement", "get_driver", "clickElement", "input_value", "executeJS", "visionQuery", "smartui_snapshot",
    # Driver-agnostic helpers
    "get_url", "get_title",
    "evaluate_math", "evaluate_network_assertion",
    "execute_api", "execute_db",
    # Heal
    "_heal_cascade", "HealResult",
    # Exception classes that codegen-emitted code may catch
    "TestmuConfigError", "AutohealExhausted", "ClickAllMethodsFailed",
}


_NEW_HELPERS = {
    "get_url", "get_title",
    "evaluate_math", "evaluate_network_assertion",
    "execute_api", "execute_db",
}


def test_public_api_includes_new_helpers():
    """The new driver-agnostic helpers are exported and importable."""
    actual = set(testmu_selenium.__all__)
    assert _NEW_HELPERS.issubset(actual), (
        f"missing from __all__: {_NEW_HELPERS - actual}"
    )
    for name in _NEW_HELPERS:
        assert hasattr(testmu_selenium, name), (
            f"{name} listed but not importable from testmu_selenium"
        )


def test_all_includes_expected_symbols():
    """Every expected codegen-emitted symbol is in __all__."""
    actual = set(testmu_selenium.__all__)
    missing = EXPECTED_BARE_SYMBOLS - actual
    assert not missing, f"missing from __all__: {missing}"


def test_all_symbols_resolve():
    """Every symbol in __all__ is actually importable from the package."""
    for name in testmu_selenium.__all__:
        assert hasattr(testmu_selenium, name), f"{name} listed in __all__ but not importable"


def test_version_attribute_present():
    """Version is at minimum a string (real or fallback)."""
    assert isinstance(testmu_selenium.__version__, str)
    assert testmu_selenium.__version__  # non-empty


def test_webelement_clickElement_monkey_patched():
    """Auto-monkey-patch on import: WebElement.clickElement exists."""
    from selenium.webdriver.remote.webelement import WebElement
    assert hasattr(WebElement, "clickElement"), \
        "WebElement.clickElement should be monkey-patched on testmu_selenium import"
