"""Test run() lifecycle for the local branch (TESTMU_RUN_TARGET=local).

The local path must launch webdriver.Chrome / webdriver.Firefox directly and
must NOT touch webdriver.Remote — no LT hub round-trip in dev iteration.
"""
import pytest
from unittest.mock import MagicMock, patch

from testmu_selenium._session import run
from testmu_selenium._helpers.driver import _drivers


@pytest.fixture(autouse=True)
def reset_drivers():
    _drivers.clear()
    yield
    _drivers.clear()


@pytest.fixture(autouse=True)
def force_local_run_target():
    with patch("testmu_selenium._config.run_target", "local"):
        yield


@patch("testmu_selenium._session.webdriver.Remote")
@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_does_not_call_remote(mock_chrome, mock_remote):
    mock_chrome.return_value = MagicMock()
    run(lambda driver: None)
    mock_remote.assert_not_called()
    mock_chrome.assert_called_once()


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_default_browser_is_chrome(mock_chrome, monkeypatch):
    monkeypatch.delenv("LT_BROWSER", raising=False)
    fake = MagicMock()
    mock_chrome.return_value = fake
    run(lambda driver: None)
    mock_chrome.assert_called_once()


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_chrome_when_lt_browser_chrome(mock_chrome, monkeypatch):
    monkeypatch.setenv("LT_BROWSER", "chrome")
    mock_chrome.return_value = MagicMock()
    run(lambda driver: None)
    mock_chrome.assert_called_once()


@patch("testmu_selenium._session.webdriver.Firefox")
def test_local_firefox_when_lt_browser_firefox(mock_firefox, monkeypatch):
    monkeypatch.setenv("LT_BROWSER", "firefox")
    mock_firefox.return_value = MagicMock()
    run(lambda driver: None)
    mock_firefox.assert_called_once()


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_invokes_fn_with_driver(mock_chrome):
    fake = MagicMock()
    mock_chrome.return_value = fake
    received = {}
    run(lambda driver: received.setdefault("d", driver))
    assert received["d"] is fake


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_quits_in_finally(mock_chrome):
    fake = MagicMock()
    mock_chrome.return_value = fake
    run(lambda driver: None)
    fake.quit.assert_called_once()


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_quits_even_on_failure(mock_chrome):
    fake = MagicMock()
    mock_chrome.return_value = fake
    def boom(driver):
        raise ValueError("boom")
    with pytest.raises(ValueError):
        run(boom)
    fake.quit.assert_called_once()


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_headless_default_true(mock_chrome, monkeypatch):
    """Default TESTMU_HEADLESS unset -> --headless=new arg present."""
    monkeypatch.delenv("TESTMU_HEADLESS", raising=False)
    mock_chrome.return_value = MagicMock()
    run(lambda driver: None)
    options = mock_chrome.call_args.kwargs.get("options") or mock_chrome.call_args.args[0]
    assert "--headless=new" in options.arguments


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_headless_disabled_when_false(mock_chrome, monkeypatch):
    monkeypatch.setenv("TESTMU_HEADLESS", "false")
    mock_chrome.return_value = MagicMock()
    run(lambda driver: None)
    options = mock_chrome.call_args.kwargs.get("options") or mock_chrome.call_args.args[0]
    assert "--headless=new" not in options.arguments


@patch("testmu_selenium._session.webdriver.Firefox")
def test_local_firefox_headless_arg(mock_firefox, monkeypatch):
    monkeypatch.setenv("LT_BROWSER", "firefox")
    monkeypatch.delenv("TESTMU_HEADLESS", raising=False)
    mock_firefox.return_value = MagicMock()
    run(lambda driver: None)
    options = mock_firefox.call_args.kwargs.get("options") or mock_firefox.call_args.args[0]
    assert "-headless" in options.arguments


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_registers_driver(mock_chrome):
    fake = MagicMock()
    mock_chrome.return_value = fake
    captured = {}
    def my_test(driver):
        from testmu_selenium._helpers.driver import get_driver
        captured["d"] = get_driver("default")
    run(my_test)
    assert captured["d"] is fake


@patch("testmu_selenium._session.webdriver.Chrome")
def test_local_clears_driver_registry_after(mock_chrome):
    mock_chrome.return_value = MagicMock()
    run(lambda driver: None)
    assert _drivers == {}
