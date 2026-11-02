"""A folder the system owns is marked at the one folder door (V5-B, 2026-09-30).

"Use existing → Folders" listed 56,037 folders for the test account — capture sites under
``page-captures-<org>/``, coding-session folders, variant folders — because no folder carried the
``metadata.system_artifact`` marker ``platform._inventory_filter`` reads. These pin the rule and
prove the door stamps it, so a new writer cannot forget.
"""

from __future__ import annotations

import pytest

from matrx_files.cloud_sync.db import _with_system_folder_marker
from matrx_files.user_visible import (
    MACHINE_CARRIED_ROOTS,
    MACHINE_NAMESPACE_DOMAINS,
    PERSON_CARRIED_ROOTS,
    system_folder_marker,
)

ORG = "23c2ac41-8044-49ed-9af9-35761370e5c0"


@pytest.mark.parametrize("root", sorted(MACHINE_CARRIED_ROOTS))
def test_every_machine_carried_root_folder_is_a_system_folder(root: str) -> None:
    assert system_folder_marker(f"{root}-{ORG}")["system_artifact"] is True
    assert system_folder_marker(f"{root}-{ORG}/en-wikipedia-org")["system_artifact"] is True


@pytest.mark.parametrize("namespace", sorted(MACHINE_NAMESPACE_DOMAINS))
def test_machine_namespace_folders_are_system_folders(namespace: str) -> None:
    assert system_folder_marker(f"{namespace}/{ORG}") == {
        "system_artifact": True,
        "artifact_domain": MACHINE_NAMESPACE_DOMAINS[namespace],
    }


def test_variant_folders_are_system_folders() -> None:
    assert system_folder_marker(f"Images/Brand Library/v/{ORG}")["artifact_domain"] == "file_variant"
    assert system_folder_marker("Images/Brand Library/v")["system_artifact"] is True


@pytest.mark.parametrize(
    "path",
    ["My Files", "Images/Brand Library", "v", "Projects/v1", f"Projects/v/{ORG}/notes"]
    + [f"{root}-{ORG}/letters" for root in sorted(PERSON_CARRIED_ROOTS)],
)
def test_a_persons_folder_is_never_marked(path: str) -> None:
    assert system_folder_marker(path) == {}


def test_the_folder_door_stamps_and_keeps_the_writers_domain() -> None:
    stamped = _with_system_folder_marker(
        {"folder_path": f"web-crawls-{ORG}/site", "metadata": {"artifact_domain": "web_crawl"}}
    )
    assert stamped["metadata"] == {"artifact_domain": "web_crawl", "system_artifact": True}
    person = {"folder_path": "My Files/Taxes", "metadata": None}
    assert _with_system_folder_marker(person) is person
