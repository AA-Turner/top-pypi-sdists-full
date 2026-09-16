import json

import pytest

import agentic_devtools.cli.workflows.create_epic.registry as registry


def test_read_registry_rejects_non_object_json(tmp_path):
    path = tmp_path / "registry.json"
    path.write_text(json.dumps([]))

    with pytest.raises(ValueError, match="Corrupt"):
        registry._read_registry(path)
