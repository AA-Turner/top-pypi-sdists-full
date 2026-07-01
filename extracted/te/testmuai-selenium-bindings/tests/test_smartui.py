import builtins
import sys
import types

import pytest


def test_smartui_snapshot_delegates_with_options(monkeypatch):
    calls = []

    def sdk_smartui_snapshot(driver, name, options={}):
        calls.append((driver, name, options))
        return {"status": "ok"}

    fake_sdk = types.ModuleType("lambdatest_selenium_driver")
    fake_sdk.smartui_snapshot = sdk_smartui_snapshot
    monkeypatch.setitem(sys.modules, "lambdatest_selenium_driver", fake_sdk)

    from testmu_selenium import smartui_snapshot

    driver = object()
    options = {"fullPage": True}

    assert smartui_snapshot(driver, "checkout", options) == {"status": "ok"}
    assert calls == [(driver, "checkout", options)]


def test_smartui_snapshot_defaults_options_to_empty_dict(monkeypatch):
    calls = []

    def sdk_smartui_snapshot(driver, name, options={}):
        calls.append((driver, name, options))
        return None

    fake_sdk = types.ModuleType("lambdatest_selenium_driver")
    fake_sdk.smartui_snapshot = sdk_smartui_snapshot
    monkeypatch.setitem(sys.modules, "lambdatest_selenium_driver", fake_sdk)

    from testmu_selenium import smartui_snapshot

    driver = object()

    assert smartui_snapshot(driver, "checkout") is None
    assert calls == [(driver, "checkout", {})]


def test_smartui_snapshot_import_error_surfaces(monkeypatch):
    monkeypatch.delitem(sys.modules, "lambdatest_selenium_driver", raising=False)
    real_import = builtins.__import__

    def raise_for_sdk(name, *args, **kwargs):
        if name == "lambdatest_selenium_driver":
            raise ImportError("missing lambdatest_selenium_driver")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", raise_for_sdk)

    from testmu_selenium._helpers.smartui import smartui_snapshot

    with pytest.raises(ImportError, match="missing lambdatest_selenium_driver"):
        smartui_snapshot(object(), "checkout")
