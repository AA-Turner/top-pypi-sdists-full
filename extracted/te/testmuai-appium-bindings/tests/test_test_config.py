"""V2-parity coverage for test-config to LT:Options translation."""

from testmu_appium._test_config import _build_lt_options


def test_device_region_is_not_forwarded_to_lt_options(monkeypatch):
    monkeypatch.delenv("DEVICE_REGION", raising=False)

    options = _build_lt_options({
        "platform_name": "android",
        "region": "ap-south-2",
    })

    assert "region" not in options


def test_device_region_environment_does_not_add_region_capability(monkeypatch):
    monkeypatch.setenv("DEVICE_REGION", "eu-central-1")

    options = _build_lt_options({
        "platform_name": "ios",
        "mobile_region": "us-east-1",
    })

    assert "region" not in options
