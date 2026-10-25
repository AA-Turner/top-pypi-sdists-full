"""Every metadata key Matrx 2 writes on ai.device_model_file is registered as system state.

The live gate (matrx_validation_gate) refuses an unregistered top-level metadata key, which is how
ai_122 / ai_124 were found missing only after the desktop published (the whole batch was refused).
The shipped contract fixture lists the keys the desktop writes; a static scan of db/migrations must
find an INSERT into platform.metadata_reserved_keys for each, under 'ai_device_model_file'.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
FIXTURE = REPO / "apps" / "shared" / "desktop-protocol" / "fixtures" / "device-model-contract.json"
ENTITY = "ai_device_model_file"


def registered_keys(migrations: Path, entity: str = ENTITY) -> set[str]:
    """Keys registered for `entity` by INSERT INTO platform.metadata_reserved_keys in any migration file."""
    found: set[str] = set()
    pattern = re.compile(r"\(\s*'" + re.escape(entity) + r"'\s*,\s*'([A-Za-z0-9_]+)'")
    for path in migrations.glob("*.sql"):
        text = path.read_text()
        for statement in re.split(r";\s*\n", text):
            if re.search(r"INSERT\s+INTO\s+platform\.metadata_reserved_keys", statement, re.I):
                found.update(pattern.findall(statement))
    return found


def test_every_reserved_key_the_desktop_writes_is_registered_by_a_migration() -> None:
    wanted = json.loads(FIXTURE.read_text())["reserved_metadata_keys"][ENTITY]
    assert wanted, "the fixture lists no reserved keys"
    missing = sorted(set(wanted) - registered_keys(REPO / "db" / "migrations"))
    assert missing == [], f"{ENTITY} metadata keys the desktop writes but no migration registers: {missing}"


def test_the_scan_can_fail(tmp_path: Path) -> None:
    (tmp_path / "a.sql").write_text("INSERT INTO platform.metadata_reserved_keys (table_token, key, reason)\nVALUES ('ai_device_model_file', 'model_key', 'x');\n")
    assert registered_keys(tmp_path) == {"model_key"}
    (tmp_path / "b.sql").write_text("-- ('ai_device_model_file', 'gguf') only in a comment, no INSERT\n")
    assert "gguf" not in registered_keys(tmp_path)

