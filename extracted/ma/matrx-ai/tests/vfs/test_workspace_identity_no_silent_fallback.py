from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from matrx_ai.tools.vfs import (
    WorkspaceIdentityMissingError,
    clear_workspace_cache,
    get_workspace_fs,
    workspace_id_for,
)


@dataclass
class Ctx:
    user_id: str | None
    conversation_id: str | None


@pytest.mark.asyncio
async def test_real_workspace_call_refuses_shared_anonymous_identity() -> None:
    clear_workspace_cache()
    with pytest.raises(WorkspaceIdentityMissingError) as exc:
        await get_workspace_fs(Ctx(None, None))
    assert "WorkspaceContext.user_id" in str(exc.value)
    assert "get_workspace_fs_by_id" in str(exc.value)


def test_durable_safe_path_only_needs_authenticated_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("matrx_ai.tools.vfs.workspace._DURABLE_INSTALLED", True)
    assert workspace_id_for(Ctx("user-1", None)) == "user-1"


def test_source_guard_bans_shared_identity_substitution() -> None:
    import matrx_ai.tools.vfs.workspace as workspace
    source = Path(workspace.__file__).read_text()
    assert 'ctx.user_id or "anonymous"' not in source
    assert 'ctx.conversation_id or "default"' not in source
