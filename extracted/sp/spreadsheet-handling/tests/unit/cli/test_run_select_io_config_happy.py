import pytest

import spreadsheet_handling.cli.apps.run as runmod

pytestmark = pytest.mark.ftr("FTR-TEST-NAMING-AND-CONVENTIONS-P3C")


def test_select_io_config_returns_named_profile():
    cfg = {
        "io": {
            "profiles": {
                "local": {
                    "input": {"kind": "json_dir", "path": "in"},
                    "output": {"kind": "json_dir", "path": "out"},
                }
            }
        }
    }
    sel = runmod._select_io_config(cfg, profile="local")
    assert sel["input"]["kind"] == "json_dir"
