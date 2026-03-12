from __future__ import annotations

import json

import pytest

from plato.cli.chronos.test.config import TestConfig


def test_test_config_defaults(tmp_path):
    config_path = tmp_path / "chronos-test.json"
    config_path.write_text(
        json.dumps(
            {
                "world": {
                    "package": "plato-world-webclone:0.3.10",
                    "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096}},
                    "config": {"clone_name": "test", "session_ids": ["s1"], "recording_processor": {}},
                },
                "dev": {"world": "../../worlds/webclone", "sync_sdk": True, "agents": {}},
            }
        )
    )

    cfg = TestConfig.from_file(config_path)
    assert cfg.test.workdir == "/world"
    assert [p.name for p in cfg.test.phases] == ["integration"]


def test_test_config_duplicate_phase_name_rejected(tmp_path):
    config_path = tmp_path / "chronos-test.json"
    config_path.write_text(
        json.dumps(
            {
                "world": {
                    "package": "plato-world-webclone:0.3.10",
                    "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096}},
                    "config": {"clone_name": "test", "session_ids": ["s1"], "recording_processor": {}},
                },
                "dev": {"world": "../../worlds/webclone", "sync_sdk": True, "agents": {}},
                "test": {
                    "phases": [
                        {"name": "unit", "command": "pytest tests/unit"},
                        {"name": "unit", "command": "pytest tests/integration"},
                    ]
                },
            }
        )
    )

    with pytest.raises(ValueError, match="duplicate test phase name"):
        TestConfig.from_file(config_path)
