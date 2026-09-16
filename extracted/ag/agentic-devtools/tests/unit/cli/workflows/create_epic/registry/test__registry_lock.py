import agentic_devtools.cli.workflows.create_epic.registry as registry


def test_registry_lock_acquires_and_releases(tmp_path):
    path = tmp_path / "registry.json"

    with registry._registry_lock(path):
        assert path.with_suffix(".lock").exists()

    assert path.with_suffix(".lock").exists()
