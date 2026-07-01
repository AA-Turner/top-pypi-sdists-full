"""Test the HE test-run JSON capability reader."""
import json
import pytest
from testmu_selenium import _test_config
from testmu_selenium._test_config import get_cap_value, load_test_config


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    for k in ("TEST_RUN_ID", "TEST_CONFIG_FILE", "TEST_INSTANCE_ID", "LT_PLATFORM", "VIDEO"):
        monkeypatch.delenv(k, raising=False)
    _test_config._reset()
    yield
    _test_config._reset()


def _write_config(tmp_path, payload):
    p = tmp_path / "run.json"
    p.write_text(json.dumps(payload))
    return str(p)


class TestLoadTestConfig:
    def test_returns_none_without_config(self):
        assert load_test_config() is None

    def test_loads_matching_instance_via_explicit_file(self, tmp_path, monkeypatch):
        path = _write_config(tmp_path, {"linux": [{"test_instance_id": "1", "video": True}]})
        monkeypatch.setenv("TEST_CONFIG_FILE", path)
        monkeypatch.setenv("LT_PLATFORM", "linux")
        cfg = load_test_config()
        assert cfg == {"test_instance_id": "1", "video": True}

    def test_instance_selected_by_test_instance_id_env(self, tmp_path, monkeypatch):
        path = _write_config(tmp_path, {"linux": [
            {"test_instance_id": "1", "video": True},
            {"test_instance_id": "2", "video": False},
        ]})
        monkeypatch.setenv("TEST_CONFIG_FILE", path)
        monkeypatch.setenv("LT_PLATFORM", "linux")
        monkeypatch.setenv("TEST_INSTANCE_ID", "2")
        assert load_test_config()["video"] is False


class TestGetCapValue:
    def test_config_value_wins_over_env(self, tmp_path, monkeypatch):
        path = _write_config(tmp_path, {"linux": [{"test_instance_id": "1", "video": False}]})
        monkeypatch.setenv("TEST_CONFIG_FILE", path)
        monkeypatch.setenv("LT_PLATFORM", "linux")
        monkeypatch.setenv("VIDEO", "true")
        assert get_cap_value("VIDEO", True) is False

    def test_env_used_when_no_config(self, monkeypatch):
        monkeypatch.setenv("VIDEO", "envval")
        assert get_cap_value("VIDEO", "default") == "envval"

    def test_default_when_no_config_no_env(self, monkeypatch):
        monkeypatch.delenv("VIDEO", raising=False)
        assert get_cap_value("VIDEO", "default") == "default"
