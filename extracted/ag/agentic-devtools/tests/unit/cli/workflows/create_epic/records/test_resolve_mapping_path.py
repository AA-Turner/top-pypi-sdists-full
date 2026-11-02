from pathlib import Path

from agentic_devtools.cli.workflows.create_epic.records import resolve_mapping_path


def test_resolve_mapping_path_uses_state_directory(monkeypatch, tmp_path):
    tree_id = "12345678-1234-5678-1234-567812345678"
    monkeypatch.setattr(
        "agentic_devtools.cli.workflows.create_epic.records.state.get_state_dir",
        lambda *, create=True: tmp_path,
    )
    assert resolve_mapping_path(tree_id) == Path(tmp_path) / f"epic-create-mapping-{tree_id}"
