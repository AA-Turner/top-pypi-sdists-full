"""What the person asked an AI to make is THEIR file — in the tree AND Recents (Arman 2026-10-30).

"You do image generation inside of a chat, and then you go to your files and it's not there.
That's not an automated thing the system is doing. That's the user generating an image."

Until 2026-10-30 ``ai_images`` / ``ai_audio`` / ``ai_video`` / ``ai_documents`` were registered
under the hidden ``generations/`` root, so 2,882 generations were invisible. The registry now
declares each folder's AUDIENCE; these tests hold both directions:

* every ``audience="person"`` folder files where the person sees it (tree + Recents), and every
  ``audience="system"`` folder files where they never do — first by the declaration, then (live)
  by the database functions themselves;
* the person's AI output features are person folders — re-registering one under a system root
  turns this red.
"""

from __future__ import annotations

import os
import re

import pytest

from matrx_files.system_paths import (
    SystemPathRegistry,
    get_system_folder,
    is_system_path,
    list_system_folders,
    register_system_folder,
)
from matrx_files.user_visible import (
    CARRIED_ROOT_SEGMENT_PATTERN,
    MACHINE_NAMESPACES,
    RECENT_EXCLUDED_ROOTS,
)

PERSON_AI_FEATURES = {
    "ai_images": "Images/Generated",
    "ai_audio": "Audio/Generated",
    "ai_video": "Video/Generated",
    "ai_documents": "Documents/Generated",
}


def _under(path: str, root: str) -> bool:
    return path == root or path.startswith(root + "/")


@pytest.mark.parametrize("feature,root", sorted(PERSON_AI_FEATURES.items()))
def test_the_persons_ai_output_is_a_person_folder(feature: str, root: str) -> None:
    folder = get_system_folder(feature)
    assert folder.audience == "person", f"{feature} must be the person's output, not the system's"
    assert folder.root == root
    assert not is_system_path(folder.path("x.png"))


@pytest.mark.parametrize("folder", list_system_folders(), ids=lambda f: f.name)
def test_every_folder_files_where_its_audience_says(folder) -> None:  # noqa: ANN001
    path = folder.path("sample.bin")
    first = path.split("/", 1)[0]
    if folder.audience == "system":
        assert is_system_path(path), f"system folder {folder.name} files outside the system roots"
        return
    assert not is_system_path(path)
    assert first not in MACHINE_NAMESPACES and first != ".matrx-tmp"
    assert not re.match(CARRIED_ROOT_SEGMENT_PATTERN, first)
    hidden = [r for r in RECENT_EXCLUDED_ROOTS if _under(path, r)]
    assert not hidden, f"person folder {folder.name} files under Recents-excluded root {hidden}"


def test_registration_refuses_a_folder_whose_root_contradicts_its_audience() -> None:
    with pytest.raises(ValueError, match="cannot live under a system root"):
        register_system_folder("zz_person_hidden", root="generations/zz", description="x", audience="person")
    with pytest.raises(ValueError, match="must start with one of"):
        register_system_folder("zz_system_visible", root="Images/zz", description="x")
    with pytest.raises(ValueError, match="audience must be one of"):
        register_system_folder("zz_bad", root="system-files/zz", description="x", audience="org")  # type: ignore[arg-type]
    assert not {"zz_person_hidden", "zz_system_visible", "zz_bad"} & set(SystemPathRegistry._features)


# ---------------------------------------------------------------------------
# Live — the database's own functions agree with the declaration (SELECT only).
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.asyncio
async def test_the_live_database_shows_person_folders_and_hides_system_ones() -> None:
    missing = [n for n in ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD") if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    folders = list_system_folders()
    paths = [f.path("sample.png") for f in folders]
    async with acquire_connection(bootstrap_db()) as conn:
        rows = await conn.fetch(
            "SELECT p, files.is_user_visible_path(p) AS visible, files.is_recent_activity_path(p) AS recent "
            "FROM unnest($1::text[]) AS p",
            paths,
        )
    got = {r["p"]: (r["visible"], r["recent"]) for r in rows}
    wrong = []
    for folder, path in zip(folders, paths, strict=True):
        want = (True, True) if folder.audience == "person" else (False, False)
        if got[path] != want:
            wrong.append(f"{folder.name} ({folder.audience}) {path}: live={got[path]} want={want}")
    assert not wrong, "live visibility disagrees with the registry:\n" + "\n".join(wrong)
