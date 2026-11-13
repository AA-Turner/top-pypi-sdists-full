"""An install with no central inventory of its own answers with what discovery publishes."""
import sqlite3

from hugpy_core.registry import central_store
from hugpy_core.web import recovered_surfaces


class Table:
    """Core's database for this test: an empty central_models and a two-row catalog."""

    def __init__(self):
        self.result = []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql, params=()):
        self.result = ([("acme/Seen-GGUF", "gguf", "text-generation", {"tasks": ["text-generation"], "hub_id": "acme/Seen-GGUF"})]
                       if "FROM models" in sql else [])
        return self

    def fetchone(self):
        return self.result[0] if self.result else None

    def fetchall(self):
        return self.result


def test_central_list_and_drives_come_from_discovery_when_core_has_none(tmp_path, monkeypatch):
    central = tmp_path / "central"
    (central / "acme" / "Seen-GGUF").mkdir(parents=True)          # there; acme/Gone-GGUF is listed but not there
    export = tmp_path / "export"
    export.mkdir()
    db = sqlite3.connect(export / "discovery.sqlite3")
    db.execute("CREATE TABLE api_units_v1 (key, variation, central_dir, central_root, task, own_weight_bytes, gguf_model)")
    db.execute("CREATE TABLE api_drives_v1 (role, root, capacity_bytes, free_bytes, model_budget_bytes, budget_remaining_bytes)")
    for key, variation, size in (("acme/Seen-GGUF", "q4.gguf", 4), ("acme/Seen-GGUF", "q8.gguf", 8), ("acme/Gone-GGUF", "q4.gguf", 5)):
        db.execute("INSERT INTO api_units_v1 VALUES (?,?,?,?,?,?,1)", (key, variation, f"{central}/{key}", str(central), "text-generation", size))
    db.execute("INSERT INTO api_drives_v1 VALUES ('central', ?, 100, 60, 80, 40)", (str(central),))
    db.execute("INSERT INTO api_drives_v1 VALUES ('worker', '/elsewhere', 1, 1, 1, 1)")
    db.commit()
    db.close()
    monkeypatch.setenv("HUGPY_DISCOVERY_EXPORT", str(export))
    monkeypatch.setattr(central_store, "_db", Table)
    monkeypatch.setattr(central_store, "_DISCOVERED", {"at": 0.0, "rows": []})

    rows = central_store.rows()
    assert [(r["model_key"], r["rel"], r["bytes"], r["framework"], r["tasks"]) for r in rows] == [
        ("acme/Seen-GGUF", "acme/Seen-GGUF", 12, "gguf", ["text-generation"])]
    assert [r["model_key"] for r in central_store.rows(include_missing=True) if r["missing"]] == ["acme/Gone-GGUF"]
    assert central_store.view_root() == str(central)

    from hugpy_core.registry import drive_display
    monkeypatch.setattr(drive_display, "declared_drives", lambda: [])
    listed = recovered_surfaces.central_drives()
    assert listed["source"] == "discovery"
    assert [(d["path"], d["fs_total"], d["fs_free"], d["copies"], d["held_bytes"], d["models"]) for d in listed["drives"]] == [
        (str(central), 100, 60, 1, 12, ["acme/Seen-GGUF"])]
