import datetime
from pathlib import Path
from unittest.mock import MagicMock

import anyio
import httpx
import pytest

from runlayer_cli.api import SkillDetail, SkillFileDetail, SkillFileMetadata
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier
from runlayer_cli.skills.models import DiscoveredSkill, SkillFile
from runlayer_cli.skills.sync_engine import (
    _MAX_CONCURRENT,
    _async_sync_skill_files,
    sync_discovered_skills,
    sync_skills,
)

NAMESPACE = "myorg/repo"


def _make_skill_dir(tmp_path, rel_path, name="Test Skill", extra_files=None):
    skill_dir = tmp_path / rel_path
    skill_dir.mkdir(parents=True, exist_ok=True)
    fm = f"---\nname: {name}\ndescription: test\n---\n"
    (skill_dir / "SKILL.md").write_text(fm + "# Docs\n")
    if extra_files:
        for fname, content in extra_files.items():
            p = skill_dir / fname
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)


def _mock_client():
    client = MagicMock()
    client.list_skills.return_value = []
    return client


def _ts():
    return datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)


@pytest.mark.asyncio
async def test_sync_create_new(tmp_path):
    _make_skill_dir(tmp_path, "skills/hello", name="Hello Skill")
    client = _mock_client()
    client.create_skill.return_value = SkillDetail(
        id="new-id",
        name="Hello Skill",
        path="skills/hello",
        namespace=NAMESPACE,
        files=[
            SkillFileMetadata(
                id="f1", skill_id="new-id", title="SKILL.md", updated_at=_ts()
            )
        ],
    )
    result = await sync_skills(tmp_path, client, namespace=NAMESPACE)
    assert result.created == 1
    client.create_skill.assert_called_once()
    call_kwargs = client.create_skill.call_args
    assert call_kwargs.kwargs.get("namespace") == NAMESPACE
    assert call_kwargs.kwargs.get("path") == "skills/hello"


@pytest.mark.asyncio
async def test_sync_create_new_public(tmp_path):
    _make_skill_dir(tmp_path, "skills/hello", name="Hello Skill")
    client = _mock_client()
    client.create_skill.return_value = SkillDetail(
        id="new-id",
        name="Hello Skill",
        path="skills/hello",
        namespace=NAMESPACE,
        is_public=True,
        files=[
            SkillFileMetadata(
                id="f1", skill_id="new-id", title="SKILL.md", updated_at=_ts()
            )
        ],
    )

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, is_public=True)

    assert result.created == 1
    client.create_skill.assert_called_once()
    assert client.create_skill.call_args.kwargs.get("is_public") is True


@pytest.mark.asyncio
async def test_sync_create_root_skill_uses_root_dir_name(tmp_path):
    _make_skill_dir(tmp_path, ".", name="Root Skill")
    client = _mock_client()
    client.create_skill.return_value = SkillDetail(
        id="root-id",
        name="Root Skill",
        path=tmp_path.name,
        namespace=NAMESPACE,
        files=[
            SkillFileMetadata(
                id="f1", skill_id="root-id", title="SKILL.md", updated_at=_ts()
            )
        ],
    )

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE)

    assert result.created == 1
    client.create_skill.assert_called_once()
    assert client.create_skill.call_args.kwargs.get("path") == tmp_path.name


@pytest.mark.asyncio
async def test_sync_update_existing(tmp_path):
    _make_skill_dir(tmp_path, "skills/demo", name="Demo Skill")
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="existing-id",
            name="Demo Skill",
            path="skills/demo",
            namespace=NAMESPACE,
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id="existing-id",
                    title="SKILL.md",
                    updated_at=_ts(),
                )
            ],
        )
    ]
    client.get_skill.return_value = SkillDetail(
        id="existing-id",
        name="Demo Skill",
        path="skills/demo",
        description="test",
        files=[
            SkillFileMetadata(
                id="f1",
                skill_id="existing-id",
                title="SKILL.md",
                updated_at=_ts(),
            )
        ],
    )
    fm = "---\nname: Demo Skill\ndescription: test\n---\n# Docs\n"
    client.get_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="existing-id", title="SKILL.md", content=fm
    )

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE)
    assert result.unchanged == 1
    assert result.updated == 0
    client.create_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_update_detects_changes(tmp_path):
    _make_skill_dir(tmp_path, "skills/demo", name="Demo Skill")
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="existing-id",
            name="Demo Skill",
            path="skills/demo",
            namespace=NAMESPACE,
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id="existing-id",
                    title="SKILL.md",
                    updated_at=_ts(),
                )
            ],
        )
    ]
    client.get_skill.return_value = SkillDetail(
        id="existing-id",
        name="Demo Skill",
        path="skills/demo",
        files=[
            SkillFileMetadata(
                id="f1",
                skill_id="existing-id",
                title="SKILL.md",
                updated_at=_ts(),
            )
        ],
    )
    client.get_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="existing-id", title="SKILL.md", content="old content"
    )
    client.update_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="existing-id", title="SKILL.md", content=""
    )

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE)
    assert result.updated == 1
    client.update_skill_file.assert_called()


@pytest.mark.asyncio
async def test_sync_update_detects_public_visibility_change(tmp_path):
    _make_skill_dir(tmp_path, "skills/demo", name="Demo Skill")
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="existing-id",
            name="Demo Skill",
            path="skills/demo",
            namespace=NAMESPACE,
            is_public=False,
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id="existing-id",
                    title="SKILL.md",
                    updated_at=_ts(),
                )
            ],
        )
    ]
    client.get_skill.return_value = SkillDetail(
        id="existing-id",
        name="Demo Skill",
        path="skills/demo",
        description="test",
        is_public=False,
        namespace=NAMESPACE,
        files=[
            SkillFileMetadata(
                id="f1",
                skill_id="existing-id",
                title="SKILL.md",
                updated_at=_ts(),
            )
        ],
    )
    fm = "---\nname: Demo Skill\ndescription: test\n---\n# Docs\n"
    client.get_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="existing-id", title="SKILL.md", content=fm
    )

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, is_public=True)

    assert result.updated == 1
    client.update_skill.assert_called_once_with(
        "existing-id",
        name="Demo Skill",
        description="test",
        is_public=True,
    )


@pytest.mark.asyncio
async def test_sync_update_preserves_public_visibility_without_override(tmp_path):
    _make_skill_dir(tmp_path, "skills/demo", name="Demo Skill")
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="existing-id",
            name="Demo Skill",
            path="skills/demo",
            namespace=NAMESPACE,
            is_public=True,
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id="existing-id",
                    title="SKILL.md",
                    updated_at=_ts(),
                )
            ],
        )
    ]
    client.get_skill.return_value = SkillDetail(
        id="existing-id",
        name="Demo Skill",
        path="skills/demo",
        description="test",
        is_public=True,
        namespace=NAMESPACE,
        files=[
            SkillFileMetadata(
                id="f1",
                skill_id="existing-id",
                title="SKILL.md",
                updated_at=_ts(),
            )
        ],
    )
    fm = "---\nname: Demo Skill\ndescription: test\n---\n# Docs\n"
    client.get_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="existing-id", title="SKILL.md", content=fm
    )

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, is_public=None)

    assert result.unchanged == 1
    client.update_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_dry_run_no_api_writes(tmp_path):
    _make_skill_dir(tmp_path, "skills/demo", name="Demo Skill")
    client = _mock_client()

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, dry_run=True)
    assert result.created == 1
    client.create_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_prune_deletes_remote_only(tmp_path):
    """Remote has skill not on disk -> deleted when prune=True."""
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="old-id", name="Gone Skill", path="skills/gone", namespace=NAMESPACE
        )
    ]
    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, prune=True)
    assert result.deleted == 1
    client.delete_skill.assert_called_once_with("old-id")


@pytest.mark.asyncio
async def test_sync_no_prune_keeps_remote(tmp_path):
    """Remote has skill not on disk but prune=False -> not deleted."""
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="old-id", name="Gone Skill", path="skills/gone", namespace=NAMESPACE
        )
    ]
    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, prune=False)
    assert result.deleted == 0
    client.delete_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_delete_404_no_error(tmp_path):
    """API returns 404 on delete -> no error reported."""
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="old-id", name="Gone Skill", path="skills/gone", namespace=NAMESPACE
        )
    ]
    response = httpx.Response(404, request=httpx.Request("DELETE", "http://test"))
    client.delete_skill.side_effect = httpx.HTTPStatusError(
        "Not Found", request=response.request, response=response
    )
    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, prune=True)
    assert result.errors == []


@pytest.mark.asyncio
async def test_sync_delete_500_reports_error(tmp_path):
    """API returns 500 on delete -> error reported."""
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="old-id", name="Gone Skill", path="skills/gone", namespace=NAMESPACE
        )
    ]
    response = httpx.Response(500, request=httpx.Request("DELETE", "http://test"))
    client.delete_skill.side_effect = httpx.HTTPStatusError(
        "Server Error", request=response.request, response=response
    )
    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, prune=True)
    assert len(result.errors) == 1


@pytest.mark.asyncio
async def test_sync_create_409_retries_as_update(tmp_path):
    """create_skill returns 409 (race) -> re-fetches and updates."""
    _make_skill_dir(tmp_path, "skills/demo", name="Demo Skill")
    client = _mock_client()

    response_409 = httpx.Response(409, request=httpx.Request("POST", "http://test"))
    client.create_skill.side_effect = httpx.HTTPStatusError(
        "Conflict", request=response_409.request, response=response_409
    )
    # list_skills is called twice: once in sync_skills, once in _retry_as_update
    client.list_skills.side_effect = [
        [],  # first call: no remote skills → triggers create
        [  # second call (retry): skill now exists
            SkillDetail(
                id="existing-id",
                name="Demo Skill",
                path="skills/demo",
                namespace=NAMESPACE,
                description="test",
                files=[
                    SkillFileMetadata(
                        id="f1",
                        skill_id="existing-id",
                        title="SKILL.md",
                        updated_at=_ts(),
                    )
                ],
            )
        ],
    ]
    client.get_skill.return_value = SkillDetail(
        id="existing-id",
        name="Demo Skill",
        path="skills/demo",
        description="test",
        files=[
            SkillFileMetadata(
                id="f1",
                skill_id="existing-id",
                title="SKILL.md",
                updated_at=_ts(),
            )
        ],
    )
    fm = "---\nname: Demo Skill\ndescription: test\n---\n# Docs\n"
    client.get_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="existing-id", title="SKILL.md", content=fm
    )

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE)
    assert result.errors == []
    assert result.unchanged == 1
    client.create_skill.assert_called_once()


@pytest.mark.asyncio
async def test_sync_dry_run_no_recreate_on_404(tmp_path):
    """dry_run + remote 404 on get_skill should not call create_skill."""
    _make_skill_dir(tmp_path, "skills/demo", name="Demo Skill")
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="stale-id",
            name="Demo Skill",
            path="skills/demo",
            namespace=NAMESPACE,
            files=[],
        )
    ]
    response = httpx.Response(404, request=httpx.Request("GET", "http://test"))
    client.get_skill.side_effect = httpx.HTTPStatusError(
        "Not Found", request=response.request, response=response
    )
    result = await sync_skills(tmp_path, client, namespace=NAMESPACE, dry_run=True)
    assert result.created == 1
    client.create_skill.assert_not_called()


@pytest.mark.asyncio
async def test_sync_update_deletes_removed_file(tmp_path):
    """Remote has extra file not on disk -> deleted."""
    _make_skill_dir(
        tmp_path, "skills/demo", name="Demo Skill", extra_files={"extra.md": "keep"}
    )
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="existing-id",
            name="Demo Skill",
            path="skills/demo",
            namespace=NAMESPACE,
            files=[
                SkillFileMetadata(
                    id="f1",
                    skill_id="existing-id",
                    title="SKILL.md",
                    updated_at=_ts(),
                ),
                SkillFileMetadata(
                    id="f2",
                    skill_id="existing-id",
                    title="extra.md",
                    updated_at=_ts(),
                ),
                SkillFileMetadata(
                    id="f3",
                    skill_id="existing-id",
                    title="gone.md",
                    updated_at=_ts(),
                ),
            ],
        )
    ]
    client.get_skill.return_value = SkillDetail(
        id="existing-id",
        name="Demo Skill",
        path="skills/demo",
        description="test",
        files=[
            SkillFileMetadata(
                id="f1",
                skill_id="existing-id",
                title="SKILL.md",
                updated_at=_ts(),
            ),
            SkillFileMetadata(
                id="f2",
                skill_id="existing-id",
                title="extra.md",
                updated_at=_ts(),
            ),
            SkillFileMetadata(
                id="f3",
                skill_id="existing-id",
                title="gone.md",
                updated_at=_ts(),
            ),
        ],
    )
    fm = "---\nname: Demo Skill\ndescription: test\n---\n# Docs\n"
    client.get_skill_file.side_effect = lambda sid, fid: {
        "f1": SkillFileDetail(id="f1", skill_id=sid, title="SKILL.md", content=fm),
        "f2": SkillFileDetail(id="f2", skill_id=sid, title="extra.md", content="keep"),
    }[fid]

    result = await sync_skills(tmp_path, client, namespace=NAMESPACE)
    assert result.updated == 1
    client.delete_skill_file.assert_called_once_with("existing-id", "f3")


@pytest.mark.asyncio
async def test_sync_skill_files_deletes_orphan_remote_files(tmp_path):
    """_async_sync_skill_files deletes remote files not present locally."""
    client = _mock_client()
    skill = DiscoveredSkill(
        path="plugins/__root__",
        name="__root__",
        files=[
            SkillFile(
                title="commands/review.md", path=Path("review.md"), content="# Review"
            ),
        ],
    )
    # Remote has an orphan SKILL.md auto-created by backend
    remote_file_ids = {"SKILL.md": "orphan-f1", "commands/review.md": "f2"}
    limiter = anyio.CapacityLimiter(_MAX_CONCURRENT)

    await _async_sync_skill_files(client, "skill-1", skill, remote_file_ids, limiter)

    # Should delete orphan SKILL.md
    client.delete_skill_file.assert_called_once_with("skill-1", "orphan-f1")
    # Should update the existing local file
    client.update_skill_file.assert_called_once()


# ---------------------------------------------------------------------------
# Merkle identifier short-circuit tests
# ---------------------------------------------------------------------------


def _skill_with_files(
    path: str, name: str, description: str | None, file_contents: dict[str, str]
) -> DiscoveredSkill:
    return DiscoveredSkill(
        path=path,
        name=name,
        description=description,
        files=[
            SkillFile(title=title, path=Path(title), content=content)
            for title, content in file_contents.items()
        ],
    )


def _identifier_for(file_contents: dict[str, str]) -> str:
    inputs = [SkillFileInput(name=t, content=c) for t, c in file_contents.items()]
    return compute_skill_identifier(inputs).root


@pytest.mark.asyncio
async def test_identifier_match_skips_file_fetches():
    """Matching identifier + unchanged metadata -> unchanged, no file API calls."""
    files = {"SKILL.md": "# Hello"}
    identifier = _identifier_for(files)
    skill = _skill_with_files("skills/a", "A", "desc", files)
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="s1",
            name="A",
            path="skills/a",
            description="desc",
            namespace=NAMESPACE,
            identifier=identifier,
            files=[
                SkillFileMetadata(
                    id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
                )
            ],
        )
    ]

    result = await sync_discovered_skills([skill], client, namespace=NAMESPACE)

    assert result.unchanged == 1
    client.get_skill.assert_not_called()
    client.get_skill_file.assert_not_called()


@pytest.mark.asyncio
async def test_identifier_match_metadata_changed_updates_skill():
    """Matching identifier but different name -> updates metadata, no file fetches."""
    files = {"SKILL.md": "# Hello"}
    identifier = _identifier_for(files)
    skill = _skill_with_files("skills/a", "New Name", "new desc", files)
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="s1",
            name="Old Name",
            path="skills/a",
            description="old desc",
            namespace=NAMESPACE,
            identifier=identifier,
            files=[
                SkillFileMetadata(
                    id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
                )
            ],
        )
    ]

    result = await sync_discovered_skills([skill], client, namespace=NAMESPACE)

    assert result.updated == 1
    client.update_skill.assert_called_once_with(
        "s1", name="New Name", description="new desc", is_public=False
    )
    client.get_skill.assert_not_called()
    client.get_skill_file.assert_not_called()


@pytest.mark.asyncio
async def test_identifier_match_is_public_changed_updates_skill():
    """Matching identifier but is_public flipped -> updates metadata with is_public."""
    files = {"SKILL.md": "# Hello"}
    identifier = _identifier_for(files)
    skill = _skill_with_files("skills/a", "A", "desc", files)
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="s1",
            name="A",
            path="skills/a",
            description="desc",
            namespace=NAMESPACE,
            identifier=identifier,
            is_public=False,
            files=[
                SkillFileMetadata(
                    id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
                )
            ],
        )
    ]

    result = await sync_discovered_skills(
        [skill], client, namespace=NAMESPACE, is_public=True
    )

    assert result.updated == 1
    client.update_skill.assert_called_once_with(
        "s1", name="A", description="desc", is_public=True
    )
    client.get_skill.assert_not_called()
    client.get_skill_file.assert_not_called()


@pytest.mark.asyncio
async def test_identifier_match_is_public_none_preserves_remote():
    """Matching identifier + is_public=None -> no change when remote is already public."""
    files = {"SKILL.md": "# Hello"}
    identifier = _identifier_for(files)
    skill = _skill_with_files("skills/a", "A", "desc", files)
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="s1",
            name="A",
            path="skills/a",
            description="desc",
            namespace=NAMESPACE,
            identifier=identifier,
            is_public=True,
            files=[
                SkillFileMetadata(
                    id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
                )
            ],
        )
    ]

    result = await sync_discovered_skills(
        [skill], client, namespace=NAMESPACE, is_public=None
    )

    assert result.unchanged == 1
    client.update_skill.assert_not_called()


@pytest.mark.asyncio
async def test_identifier_mismatch_falls_through_to_full_sync():
    """Different identifier -> full sync (calls get_skill + get_skill_file)."""
    files = {"SKILL.md": "# Hello"}
    skill = _skill_with_files("skills/a", "A", "desc", files)
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="s1",
            name="A",
            path="skills/a",
            description="desc",
            namespace=NAMESPACE,
            identifier="different-identifier",
            files=[
                SkillFileMetadata(
                    id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
                )
            ],
        )
    ]
    client.get_skill.return_value = SkillDetail(
        id="s1",
        name="A",
        path="skills/a",
        description="desc",
        files=[
            SkillFileMetadata(
                id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
            )
        ],
    )
    client.get_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="s1", title="SKILL.md", content="# Old"
    )
    client.update_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="s1", title="SKILL.md", content="# Hello"
    )

    result = await sync_discovered_skills([skill], client, namespace=NAMESPACE)

    assert result.updated == 1
    client.get_skill.assert_called_once()
    client.get_skill_file.assert_called_once()


@pytest.mark.asyncio
async def test_identifier_none_falls_through_to_full_sync():
    """Remote identifier is None -> full sync (no short-circuit)."""
    files = {"SKILL.md": "# Hello"}
    skill = _skill_with_files("skills/a", "A", "desc", files)
    client = _mock_client()
    client.list_skills.return_value = [
        SkillDetail(
            id="s1",
            name="A",
            path="skills/a",
            description="desc",
            namespace=NAMESPACE,
            identifier=None,
            files=[
                SkillFileMetadata(
                    id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
                )
            ],
        )
    ]
    client.get_skill.return_value = SkillDetail(
        id="s1",
        name="A",
        path="skills/a",
        description="desc",
        files=[
            SkillFileMetadata(
                id="f1", skill_id="s1", title="SKILL.md", updated_at=_ts()
            )
        ],
    )
    client.get_skill_file.return_value = SkillFileDetail(
        id="f1", skill_id="s1", title="SKILL.md", content="# Hello"
    )

    result = await sync_discovered_skills([skill], client, namespace=NAMESPACE)

    assert result.unchanged == 1
    client.get_skill.assert_called_once()
    client.get_skill_file.assert_called_once()


@pytest.mark.asyncio
async def test_new_skill_no_identifier_comparison():
    """New skill (no remote) -> creates normally, no identifier logic."""
    files = {"SKILL.md": "# Hello"}
    skill = _skill_with_files("skills/new", "New Skill", None, files)
    client = _mock_client()
    client.create_skill.return_value = SkillDetail(
        id="new-id",
        name="New Skill",
        path="skills/new",
        namespace=NAMESPACE,
        files=[
            SkillFileMetadata(
                id="f1", skill_id="new-id", title="SKILL.md", updated_at=_ts()
            )
        ],
    )

    result = await sync_discovered_skills([skill], client, namespace=NAMESPACE)

    assert result.created == 1
    client.create_skill.assert_called_once()
    client.get_skill.assert_not_called()
