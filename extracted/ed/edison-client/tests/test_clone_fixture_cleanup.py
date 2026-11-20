"""Fixture maintenance may delete only explicitly journaled test workspaces."""

import errno
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import httpx
import pytest

from edison_client.clients.rest_client import RestClient


@pytest.fixture(name="maintenance")
def fixture_maintenance(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    path = (
        Path(__file__).resolve().parents[2]
        / "crow-service/scripts/sdk_clone_fixture.py"
    )
    spec = importlib.util.spec_from_file_location("sdk_clone_fixture", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(name="filesystem")
def fixture_filesystem(tmp_path: Path) -> MagicMock:
    filesystem = MagicMock()
    filesystem.lstat.side_effect = lambda path: (tmp_path / path.lstrip("/")).lstat()
    filesystem.listdir.side_effect = lambda path: sorted(
        p.name for p in (tmp_path / path.lstrip("/")).iterdir()
    )
    filesystem.open.side_effect = lambda path, mode="r": (
        tmp_path / path.lstrip("/")
    ).open(mode)
    filesystem.unlink.side_effect = lambda path: (tmp_path / path.lstrip("/")).unlink()
    filesystem.rmdir.side_effect = lambda path: (tmp_path / path.lstrip("/")).rmdir()
    return filesystem


def directory(tmp_path: Path, workspace_id: UUID, content: dict[str, str]) -> Path:
    path = tmp_path / "sandboxes" / str(workspace_id)
    path.mkdir(parents=True)
    for name, value in content.items():
        (path / name).write_text(value)
    return path


def test_cleanup_preserves_other_workspaces_and_can_resume(
    maintenance: ModuleType, filesystem: MagicMock, tmp_path: Path
) -> None:
    owned, other = uuid4(), uuid4()
    owned_path = directory(
        tmp_path, owned, {maintenance.SENTINEL: maintenance.SENTINEL_CONTENT}
    )
    other_path = directory(tmp_path, other, {"important.txt": "keep"})
    maintenance.remove_clone_directory(filesystem, owned)
    maintenance.remove_clone_directory(filesystem, owned)
    assert not owned_path.exists()
    assert (other_path / "important.txt").read_text() == "keep"


@pytest.mark.parametrize(
    "contents", [{"important.txt": "keep"}, {".edison-client-clone-seed": "wrong"}]
)
def test_cleanup_refuses_unexpected_content(
    maintenance: ModuleType,
    filesystem: MagicMock,
    tmp_path: Path,
    contents: dict[str, str],
) -> None:
    workspace_id = uuid4()
    path = directory(tmp_path, workspace_id, contents)
    with pytest.raises(ValueError, match="Refusing"):
        maintenance.remove_clone_directory(filesystem, workspace_id)
    assert {p.name: p.read_text() for p in path.iterdir()} == contents


def test_cleanup_propagates_storage_errors(
    maintenance: ModuleType, filesystem: MagicMock
) -> None:
    filesystem.lstat.side_effect = PermissionError(errno.EACCES, "denied")
    with pytest.raises(PermissionError):
        maintenance.remove_clone_directory(filesystem, uuid4())


def test_cleanup_refuses_symlink_to_another_workspace(
    maintenance: ModuleType, filesystem: MagicMock, tmp_path: Path
) -> None:
    target_id, link_id = uuid4(), uuid4()
    target = directory(
        tmp_path, target_id, {maintenance.SENTINEL: maintenance.SENTINEL_CONTENT}
    )
    (target.parent / str(link_id)).symlink_to(target, target_is_directory=True)
    with pytest.raises(ValueError, match="non-directory"):
        maintenance.remove_clone_directory(filesystem, link_id)
    assert (target / maintenance.SENTINEL).read_text() == maintenance.SENTINEL_CONTENT


def test_full_cleanup_repeats_api_deletions_and_removes_only_owned_files(
    maintenance: ModuleType,
    filesystem: MagicMock,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed_id, seed_persona_id, seed_workspace_id, owned_id, workspace_id, wm_id = (
        uuid4() for _ in range(6)
    )
    seed_path = directory(
        tmp_path,
        seed_workspace_id,
        {maintenance.SENTINEL: maintenance.SENTINEL_CONTENT},
    )
    owned_path = directory(
        tmp_path, workspace_id, {maintenance.SENTINEL: maintenance.SENTINEL_CONTENT}
    )
    remaining = {
        f"/v0.1/projects/{owned_id}",
        f"/v0.1/data-storage/workspaces/{workspace_id}",
        f"/v0.1/world-models/{wm_id}",
    }

    def handle(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "DELETE":
            if path in remaining:
                remaining.remove(path)
                return httpx.Response(204)
            return httpx.Response(404)
        if path == f"/v0.1/projects/{seed_id}":
            return httpx.Response(
                200, json={"persona_project_id": str(seed_persona_id)}
            )
        if path == f"/v0.1/data-storage/workspaces/by-project/{seed_persona_id}":
            return httpx.Response(
                200, json={"data_storage": {"id": str(seed_workspace_id)}}
            )
        assert path == f"/v0.1/projects/{owned_id}"
        return (
            httpx.Response(200, json={"metadata": maintenance.FIXTURE_METADATA})
            if path in remaining
            else httpx.Response(404)
        )

    manifest = tmp_path / "clone-resources.json"
    manifest.write_text(
        json.dumps({
            "seed_project_id": str(seed_id),
            "persona_ids": [str(owned_id)],
            "workspace_ids": [str(workspace_id)],
            "world_model_ids": [str(wm_id)],
        })
    )
    with httpx.Client(
        base_url="https://example.com", transport=httpx.MockTransport(handle)
    ) as sync:
        monkeypatch.setattr(RestClient, "client", property(lambda _: sync))
        client = RestClient(api_key="test-only-not-a-secret", cleanup_on_exit=False)
        maintenance.cleanup(client, filesystem, seed_id, [manifest], workers=1)
        maintenance.cleanup(client, filesystem, seed_id, [manifest], workers=1)
    assert not remaining
    assert not owned_path.exists()
    assert (
        seed_path / maintenance.SENTINEL
    ).read_text() == maintenance.SENTINEL_CONTENT


def test_cleanup_validates_later_manifests_before_any_deletion(
    maintenance: ModuleType,
    filesystem: MagicMock,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed_id, seed_persona_id, seed_workspace_id, owned_id, other_id, wm_id = (
        uuid4() for _ in range(6)
    )
    deleted = []

    def handle(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "DELETE":
            deleted.append(path)
            return httpx.Response(204)
        if path == f"/v0.1/projects/{seed_id}":
            return httpx.Response(
                200, json={"persona_project_id": str(seed_persona_id)}
            )
        if path == f"/v0.1/data-storage/workspaces/by-project/{seed_persona_id}":
            return httpx.Response(
                200, json={"data_storage": {"id": str(seed_workspace_id)}}
            )
        if path == f"/v0.1/projects/{owned_id}":
            return httpx.Response(200, json={"metadata": maintenance.FIXTURE_METADATA})
        assert path == f"/v0.1/projects/{other_id}"
        return httpx.Response(200, json={"metadata": None})

    manifests = []
    for index, persona_id in enumerate([owned_id, other_id]):
        path = tmp_path / f"clone-resources-{index}.json"
        path.write_text(
            json.dumps({
                "seed_project_id": str(seed_id),
                "persona_ids": [str(persona_id)],
                "workspace_ids": [],
                "world_model_ids": [str(wm_id)],
            })
        )
        manifests.append(path)
    with httpx.Client(
        base_url="https://example.com", transport=httpx.MockTransport(handle)
    ) as sync:
        monkeypatch.setattr(RestClient, "client", property(lambda _: sync))
        client = RestClient(api_key="test-only-not-a-secret", cleanup_on_exit=False)
        with pytest.raises(ValueError, match="non-fixture"):
            maintenance.cleanup(client, filesystem, seed_id, manifests, workers=1)
    assert deleted == []
    filesystem.unlink.assert_not_called()
    filesystem.rmdir.assert_not_called()


@pytest.mark.parametrize("include_seed", ["persona", "workspace", "different_seed"])
def test_cleanup_refuses_seed_before_any_deletion(
    maintenance: ModuleType,
    filesystem: MagicMock,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    include_seed: str,
) -> None:
    seed_id, persona_id, workspace_id = (uuid4() for _ in range(3))

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/v0.1/projects/{seed_id}":
            return httpx.Response(200, json={"persona_project_id": str(persona_id)})
        if request.url.path == f"/v0.1/data-storage/workspaces/by-project/{persona_id}":
            return httpx.Response(200, json={"data_storage": {"id": str(workspace_id)}})
        raise AssertionError(f"Unexpected request: {request.method} {request.url.path}")

    manifest = tmp_path / "clone-resources.json"
    manifest.write_text(
        json.dumps({
            "seed_project_id": str(
                uuid4() if include_seed == "different_seed" else seed_id
            ),
            "persona_ids": [str(persona_id)] if include_seed == "persona" else [],
            "workspace_ids": [str(workspace_id)] if include_seed == "workspace" else [],
            "world_model_ids": [],
        })
    )
    with httpx.Client(
        base_url="https://example.com", transport=httpx.MockTransport(handle)
    ) as sync:
        monkeypatch.setattr(RestClient, "client", property(lambda _: sync))
        client = RestClient(api_key="test-only-not-a-secret", cleanup_on_exit=False)
        with pytest.raises(ValueError, match="seed"):
            maintenance.cleanup(client, filesystem, seed_id, [manifest], workers=1)
    filesystem.unlink.assert_not_called()
    filesystem.rmdir.assert_not_called()
