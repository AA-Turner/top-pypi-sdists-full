import os
from pathlib import Path
import pytest
import sage.games.assets.sprites as sprites
import sage.games.assets.meshes as meshes

@pytest.fixture(autouse=True, scope="session")
def setup_games_testing_environment():
    # Force SAGE_TESTING=1 to bypass actual headless builds on Unity/Godot/etc.
    os.environ["SAGE_TESTING"] = "1"

@pytest.fixture(autouse=True)
def mock_asset_generators(request, monkeypatch):
    # Check if the test is in test_assets.py or test_3d_asset_pipeline.py
    filename = request.node.fspath.basename if hasattr(request.node, "fspath") else ""
    if filename in ("test_assets.py", "test_3d_asset_pipeline.py"):
        # Let these tests handle their own mocking
        return

    # Otherwise mock them globally
    # Mock sprite generation
    monkeypatch.setattr(sprites, "_vertex_available", lambda: True)
    monkeypatch.setattr(
        sprites,
        "_imagen_generate",
        lambda prompt, size, out_path, style: out_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    )
    # Mock Blender lookup so mesh generation doesn't throw MeshMissingBackendError
    monkeypatch.setattr(meshes, "_find_blender", lambda: Path("/usr/local/bin/blender"))
    monkeypatch.setattr(
        meshes,
        "_blender_export",
        lambda blender, prim, out_path: out_path.write_bytes(b"glTF")
    )
    monkeypatch.setattr(
        meshes,
        "_blender_export_character",
        lambda blender, out_path: out_path.write_bytes(b"glTF")
    )
