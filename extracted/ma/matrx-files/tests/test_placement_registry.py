"""The placement registry: one declaration of where every file goes and what it is called.

Each test would fail against a registry that let a person's output hide, let automated output into
the person's roots, let a live row change audience/root, or let a writer pick its own folder.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from matrx_files import placement as P
from matrx_files.system_paths import list_system_folders

_TOKENS = {"source": "example.com", "master": "m1", "file_id": "f1", "record": "r1",
           "conversation": "c1", "run": "u1", "session": "s1", "record_type": "agent"}


def _resolve(key: str, **kw):
    kw.setdefault("tokens", _TOKENS)
    kw.setdefault("original_name", "report.pdf")
    kw.setdefault("now", datetime(2026, 10, 30, 14, 5, 9, tzinfo=UTC))
    return P.resolve(key, **kw)


@pytest.mark.parametrize("pathway", [p.key for p in P.list_pathways()])
def test_every_declared_pathway_resolves_inside_its_root(pathway: str) -> None:
    p = P.get_pathway(pathway)
    placed = _resolve(pathway, prompt="a red barn at dusk", content=b"bytes", extension="png")
    root = P.core_root(p.root)
    assert placed.folder_path == root.path or placed.folder_path.startswith(root.path + "/")
    assert "/" not in placed.file_name and placed.file_name
    assert "{" not in placed.file_path
    if p.audience == "person":
        assert root.kind == "person" and placed.metadata_stamp() == {}
        assert p.in_recents and p.in_tree and p.in_pick_lists
    else:
        assert root.kind in ("system", "temp")
        assert placed.metadata_stamp() == {"system_artifact": True, "artifact_domain": pathway}
        assert not p.in_recents


def test_every_legacy_system_folder_has_exactly_one_pathway() -> None:
    for folder in list_system_folders():
        owners = [p.key for p in P.list_pathways() if p.system_folder == folder.name]
        assert len(owners) == 1, f"system folder {folder.name!r} is owned by {owners}"
        placed_base = P.pathway_for_system_folder(folder.name)
        assert placed_base is not None


def test_person_output_can_never_be_declared_under_system() -> None:
    with pytest.raises(P.PathwayError, match="not a person root"):
        P.register_pathway("zz.hidden_person", owner_feature="x", audience="person", root="system",
                           naming="id_only", description="x")


def test_automated_output_can_never_be_declared_under_a_person_root() -> None:
    with pytest.raises(P.PathwayError, match="person root"):
        P.register_pathway("zz.leaky", owner_feature="x", audience="automated", root="images",
                           naming="id_only", description="x")


def test_unknown_tokens_and_org_in_path_are_refused() -> None:
    with pytest.raises(P.PathwayError, match="unknown token"):
        P.register_pathway("zz.org_in_path", owner_feature="x", audience="automated", root="system",
                           subfolder="web/{org}", naming="id_only", description="x")


def test_person_chooses_honours_the_persons_folder_and_registry_refuses_one() -> None:
    assert _resolve("files.user_upload", chosen_folder="/Clients/Acme/").file_path == "Clients/Acme/report.pdf"
    assert _resolve("files.user_upload").file_path == "My Files/report.pdf"
    with pytest.raises(P.PathwayError, match="decides its own folder"):
        _resolve("media.image_generation", chosen_folder="Elsewhere", prompt="x")


def test_naming_strategies() -> None:
    gen = _resolve("media.image_generation", prompt="A sunset over the Rocky Mountains", content=b"x",
                   extension="png")
    assert gen.file_path.startswith("Images/Generated/sunset-over-rocky-mountains-") and gen.file_name.endswith(".png")
    rec = _resolve("audio.recording", original_name=None, extension="webm")
    assert rec.file_path == "Audio/Recordings/Recording 2026-10-30 14.05.webm"
    var = _resolve("files.variant", extension="webp")
    assert var.file_path == "system-files/variants/m1/f1.webp"
    att = _resolve("chat.attachment", original_name="../../etc/passwd")
    assert att.file_path == "Chat Attachments/2026-10/passwd"


def test_missing_token_names_the_pathway_and_token() -> None:
    with pytest.raises(P.PathwayError, match=r"files\.variant.*\{master\}"):
        P.resolve("files.variant", tokens={"file_id": "f"}, extension="png")


def test_a_live_row_changes_only_the_live_editable_fields() -> None:
    row = {"subfolder": "Generated/{yyyy}-{mm}", "naming": "timestamp",
           "naming_pattern": "Image {yyyy}-{mm}-{dd}", "audience": "automated", "root": "system"}
    placed = _resolve("media.image_generation", row=row, extension="png")
    assert placed.audience == "person"  # audience is a migration, never a live edit
    assert placed.file_path == "Images/Generated/2026-10/Image 2026-10-30.png"


def test_a_live_row_that_breaks_a_rule_is_refused() -> None:
    with pytest.raises(P.PathwayError, match="needs a naming_pattern"):
        _resolve("media.image_generation", row={"naming": "timestamp", "naming_pattern": ""})


def test_missing_live_row_is_announced() -> None:
    seen: list[str] = []
    P.configure_pathway_rows(lambda key: None, on_row_missing=lambda key, why: seen.append(key))
    try:
        _resolve("chat.attachment")
    finally:
        P.configure_pathway_rows(None)
    assert seen == ["chat.attachment"]


def test_ai_title_is_born_with_a_deterministic_name_and_flagged() -> None:
    placed = _resolve("media.image_generation", row={"naming": "ai_title"}, prompt="blue whale", content=b"z",
                      extension="png")
    assert placed.ai_naming_pending and placed.file_name.startswith("blue-whale-")


def test_pathway_for_path_finds_the_longest_destination() -> None:
    assert P.pathway_for_path("system-files/pdf-extractions/x/y.txt").key == "pdf.extraction"
    assert P.pathway_for_path("Images/Generated/a.png").key == "media.image_generation"
    assert P.pathway_for_path("Clients/a.pdf") is None


# ── S3: the stamp point (PLAN § 4.2a) ───────────────────────────────────────


def test_stamp_for_write_automated_pathway_stamps_the_system_marker():
    from matrx_files.placement import stamp_for_write

    meta, key = stamp_for_write("files.variant", "Photos/v/x.webp", {"a": 1})
    assert key == "files.variant"
    assert meta == {"a": 1, "system_artifact": True, "artifact_domain": "files.variant"}
    # a writer's own domain wins
    meta, _ = stamp_for_write("files.variant", "Photos/v/x.webp", {"artifact_domain": "own"})
    assert meta["artifact_domain"] == "own"


def test_stamp_for_write_person_pathway_stamps_nothing_but_the_key():
    from matrx_files.placement import stamp_for_write

    meta, key = stamp_for_write("files.user_upload", "My Files/a.pdf", {"b": 2})
    assert (meta, key) == ({"b": 2}, "files.user_upload")


def test_stamp_for_write_unknown_pathway_is_refused():
    from matrx_files.placement import PathwayError, stamp_for_write

    with pytest.raises((PathwayError, KeyError)):
        stamp_for_write("nope.nothing", "x/a.txt", None)


def test_stamp_for_write_without_pathway_keeps_the_path_marker_and_reports(caplog):
    from matrx_files.placement import stamp_for_write

    with caplog.at_level("WARNING", logger="matrx_files.placement.unregistered"):
        meta, key = stamp_for_write(None, "coding-sessions/s/a.json", {})
    assert key is None
    assert meta.get("system_artifact") is True
    assert any("file-placement-unregistered" in r.getMessage() for r in caplog.records)


def test_tus_upload_may_name_only_a_person_pathway():
    from matrx_files.cloud_sync.transports.tus import _person_pathway_or_none

    m = {"file_pathway": "files.user_upload", "x": 1}
    assert _person_pathway_or_none(m) == "files.user_upload" and "file_pathway" not in m
    assert _person_pathway_or_none({"file_pathway": "files.variant"}) is None
    assert _person_pathway_or_none({"file_pathway": "nope.nothing"}) is None
    assert _person_pathway_or_none({"y": 1}) is None
