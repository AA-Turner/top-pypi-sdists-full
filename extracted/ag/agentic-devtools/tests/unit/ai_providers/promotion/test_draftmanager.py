import json
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pytest

from agentic_devtools.ai_providers.errors import ProviderError
from agentic_devtools.ai_providers.promotion import DraftManager, compute_sha256


def _install_tracking_lock(
    monkeypatch: pytest.MonkeyPatch,
) -> list[tuple[Path, str, bool]]:
    lock_calls: list[tuple[Path, str, bool]] = []

    @contextmanager
    def tracking_lock(path: Path, mode: str = "r+", exclusive: bool = True, **_: object) -> Generator[object]:
        lock_calls.append((path, mode, exclusive))
        yield object()

    monkeypatch.setattr("agentic_devtools.ai_providers.promotion.locked_file", tracking_lock)
    return lock_calls


def test_draft_manager(tmp_path: Path):
    manager = DraftManager(tmp_path)

    # Save drafts
    manager.save_drafts(1, '{"foo": "bar", "token": "secret"}', "# Hello")
    assert manager.get_meta_draft_path(1).exists()
    assert manager.get_body_draft_path(1).exists()
    assert json.loads(manager.get_meta_draft_path(1).read_text(encoding="utf-8")) == {
        "foo": "bar",
        "token": "<redacted>",
    }

    # Promote drafts
    manifest = manager.promote_drafts(1)
    assert manifest.round_id == 1
    assert manifest.status == "accepted"

    # Verify canonical
    canonical_meta = manager.get_canonical_meta_path()
    canonical_body = manager.get_canonical_body_path()
    assert canonical_meta.exists()
    assert canonical_body.exists()

    # Ensure manifest exists
    assert manager.get_manifest_path().exists()

    # Verify via method
    verified = manager.verify_canonical_pair()
    assert verified.round_id == 1
    assert verified.meta_sha256 == manifest.meta_sha256

    # Modify a canonical file to trigger failure
    canonical_meta.write_text('{"foo": "baz"}')
    with pytest.raises(ProviderError, match="Canonical files do not match manifest hashes"):
        manager.verify_canonical_pair()


@pytest.mark.parametrize("bad_round_id", ["1", "1/../../outside", True, False, 1.0, None])
def test_get_meta_draft_path_rejects_non_integer_round_id(tmp_path: Path, bad_round_id: object):
    manager = DraftManager(tmp_path)
    with pytest.raises(ProviderError, match="round_id must be a non-bool integer."):
        manager.get_meta_draft_path(bad_round_id)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad_round_id", ["1", "1/../../outside", True, False, 1.0, None])
def test_get_body_draft_path_rejects_non_integer_round_id(tmp_path: Path, bad_round_id: object):
    manager = DraftManager(tmp_path)
    with pytest.raises(ProviderError, match="round_id must be a non-bool integer."):
        manager.get_body_draft_path(bad_round_id)  # type: ignore[arg-type]


def test_promote_drafts_missing(tmp_path: Path):
    manager = DraftManager(tmp_path)
    with pytest.raises(ProviderError, match="Drafts for round 2 do not exist"):
        manager.promote_drafts(2)


def test_save_drafts_rejects_invalid_meta_json(tmp_path: Path):
    manager = DraftManager(tmp_path)

    with pytest.raises(ProviderError, match="meta_content must be valid JSON"):
        manager.save_drafts(1, "{bad json}", "# Hello")


@pytest.mark.parametrize("meta_content", ["[]", '"text"', "null", "1"])
def test_save_drafts_rejects_non_object_meta_json(tmp_path: Path, meta_content: str):
    manager = DraftManager(tmp_path)

    with pytest.raises(ProviderError, match="meta_content must decode to a JSON object."):
        manager.save_drafts(1, meta_content, "# Hello")


def test_save_drafts_restores_previous_round_content_on_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")

    def failing_replace(source: Path, target: Path) -> None:
        if target == manager.get_body_draft_path(1):
            raise OSError("boom")
        source.replace(target)

    monkeypatch.setattr(
        "agentic_devtools.ai_providers.promotion._replace_file",
        failing_replace,
    )

    with pytest.raises(OSError, match="boom"):
        manager.save_drafts(1, '{"foo": "baz"}', "# Updated")

    assert json.loads(manager.get_meta_draft_path(1).read_text(encoding="utf-8")) == {"foo": "bar"}
    assert manager.get_body_draft_path(1).read_text(encoding="utf-8") == "# Hello"


def test_save_drafts_staging_failure_does_not_attempt_restore(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")

    from agentic_devtools.ai_providers import promotion

    original_write_temp_bytes = promotion._write_temp_bytes

    def failing_write_temp_bytes(target: Path, content: bytes) -> Path:
        if target == manager.get_body_draft_path(1):
            raise OSError("disk full")
        return original_write_temp_bytes(target, content)

    def fail_if_restore_attempted(target: Path, previous_content: bytes | None) -> None:
        raise AssertionError(f"rollback unexpectedly attempted for {target.name}")

    monkeypatch.setattr(
        "agentic_devtools.ai_providers.promotion._write_temp_bytes",
        failing_write_temp_bytes,
    )
    monkeypatch.setattr(
        "agentic_devtools.ai_providers.promotion._restore_file",
        fail_if_restore_attempted,
    )

    with pytest.raises(OSError, match="disk full"):
        manager.save_drafts(1, '{"foo": "baz"}', "# Updated")


def test_verify_canonical_pair_missing_manifest(tmp_path: Path):
    manager = DraftManager(tmp_path)
    with pytest.raises(ProviderError, match="Promotion manifest does not exist."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_missing_files(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    # Delete the canonical body
    manager.get_canonical_body_path().unlink()

    with pytest.raises(ProviderError, match="Canonical files missing."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_mixed_round_canonical_files(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"round": 1}', "# Round 1")
    manager.promote_drafts(1)
    round_1_meta = manager.get_meta_draft_path(1).read_text(encoding="utf-8")

    manager.save_drafts(2, '{"round": 2}', "# Round 2")
    manager.promote_drafts(2)

    canonical_meta = manager.get_canonical_meta_path()
    canonical_meta.write_text(round_1_meta, encoding="utf-8")

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["round_id"] = 1
    data["meta_sha256"] = compute_sha256(canonical_meta)
    data["body_sha256"] = compute_sha256(manager.get_canonical_body_path())
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="Canonical files do not match promoted round 1."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_missing_promoted_round_files(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manager._get_promoted_body_path(1).unlink()

    with pytest.raises(ProviderError, match="Promoted round 1 files are missing."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_path_traversal(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    # Modify manifest to reference an unexpected sibling file
    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["meta_path"] = "other.json"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="Manifest must reference canonical filenames only."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_invalid_manifest_schema(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["meta_sha256"] = "bad"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(
        ProviderError,
        match="meta_sha256 must be a 64-character lowercase hex digest.",
    ):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_invalid_manifest_json(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manager.get_manifest_path().write_text("{bad json}", encoding="utf-8")

    with pytest.raises(ProviderError, match="Promotion manifest must be a valid UTF-8 encoded JSON file."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_non_utf8_manifest(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manager.get_manifest_path().write_bytes(b"\xff\xfe invalid utf-8")

    with pytest.raises(ProviderError, match="Promotion manifest must be a valid UTF-8 encoded JSON file."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_non_object_manifest(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manager.get_manifest_path().write_text("[]", encoding="utf-8")

    with pytest.raises(ProviderError, match="Promotion manifest must be a JSON object."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_unknown_manifest_fields(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["injected_field"] = "evil"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="Promotion manifest contains unknown fields: injected_field."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_non_integer_round_id(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["round_id"] = "1"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="round_id must be an integer."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_invalid_body_hash(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["body_sha256"] = "bad"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(
        ProviderError,
        match="body_sha256 must be a 64-character lowercase hex digest.",
    ):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_invalid_status(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["status"] = "unknown"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="status must be one of:"):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_unhashable_status(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["status"] = ["accepted"]
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="status must be one of:"):
        manager.verify_canonical_pair()


@pytest.mark.parametrize("status", ["pending", "rejected"])
def test_verify_canonical_pair_rejects_non_accepted_status(tmp_path: Path, status: str):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["status"] = status
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="Promotion manifest status must be accepted."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_invalid_timestamp_shape(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["verification_timestamp"] = "bad"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="verification_timestamp must be a valid ISO-8601 timestamp."):
        manager.verify_canonical_pair()


def test_verify_canonical_pair_rejects_invalid_timestamp_value(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manifest_path = manager.get_manifest_path()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["verification_timestamp"] = "2026-13-01T00:00:00Z"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProviderError, match="verification_timestamp must be a valid ISO-8601 timestamp."):
        manager.verify_canonical_pair()


def test_promote_drafts_rolls_back_partial_first_publication(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")

    replace_attempts: list[tuple[str, str]] = []

    def failing_replace(source: Path, target: Path) -> None:
        replace_attempts.append((source.name, target.name))
        if target == manager.get_canonical_body_path():
            raise OSError("boom")
        source.replace(target)

    monkeypatch.setattr(
        "agentic_devtools.ai_providers.promotion._replace_file",
        failing_replace,
    )

    with pytest.raises(OSError, match="boom"):
        manager.promote_drafts(1)

    assert replace_attempts
    assert not manager.get_canonical_meta_path().exists()
    assert not manager.get_canonical_body_path().exists()
    assert not manager.get_manifest_path().exists()


def test_promote_drafts_restores_previous_publication_on_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    first_manifest = manager.promote_drafts(1)

    manager.save_drafts(2, '{"foo": "baz"}', "# Updated")

    def failing_replace(source: Path, target: Path) -> None:
        if target == manager.get_manifest_path():
            raise OSError("boom")
        source.replace(target)

    monkeypatch.setattr(
        "agentic_devtools.ai_providers.promotion._replace_file",
        failing_replace,
    )

    with pytest.raises(OSError, match="boom"):
        manager.promote_drafts(2)

    verified = manager.verify_canonical_pair()
    assert verified == first_manifest
    assert manager.get_canonical_body_path().read_text(encoding="utf-8") == "# Hello"


def test_promote_drafts_rejects_overwriting_retained_round_snapshot(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manager.save_drafts(1, '{"foo": "baz"}', "# Updated")

    with pytest.raises(
        ProviderError,
        match="Round 1 promoted metadata does not match the current drafts.",
    ):
        manager.promote_drafts(1)


def test_promote_drafts_rejects_overwriting_retained_round_body_snapshot(tmp_path: Path):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")
    manager.promote_drafts(1)

    manager._get_promoted_body_path(1).write_text("# Different", encoding="utf-8")
    manager.save_drafts(1, '{"foo": "bar"}', "# Hello")

    with pytest.raises(
        ProviderError,
        match="Round 1 promoted body does not match the current drafts.",
    ):
        manager.promote_drafts(1)


def test_save_drafts_uses_publication_lock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    manager = DraftManager(tmp_path)
    lock_calls = _install_tracking_lock(monkeypatch)

    manager.save_drafts(1, '{"foo":"bar"}', "# Hello")

    assert lock_calls == [(manager._publication_lock_path(), "a+", True)]


def test_promote_drafts_uses_publication_lock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo":"bar"}', "# Hello")
    lock_calls = _install_tracking_lock(monkeypatch)

    manager.promote_drafts(1)

    assert lock_calls == [(manager._publication_lock_path(), "a+", True)]


def test_verify_canonical_pair_uses_publication_lock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    manager = DraftManager(tmp_path)
    manager.save_drafts(1, '{"foo":"bar"}', "# Hello")
    manager.promote_drafts(1)
    lock_calls = _install_tracking_lock(monkeypatch)

    manager.verify_canonical_pair()

    assert lock_calls == [(manager._publication_lock_path(), "a+", True)]


def test_save_drafts_canonicalization_is_key_order_independent(tmp_path: Path):
    manager = DraftManager(tmp_path)

    manager.save_drafts(1, '{"b": 2, "a": 1}', "# Hello")
    hash_ba = compute_sha256(manager.get_meta_draft_path(1))

    manager2 = DraftManager(tmp_path / "other")
    manager2.save_drafts(1, '{"a": 1, "b": 2}', "# Hello")
    hash_ab = compute_sha256(manager2.get_meta_draft_path(1))

    assert hash_ba == hash_ab


def test_promote_drafts_missing_has_validation_error_category(tmp_path: Path):
    manager = DraftManager(tmp_path)
    with pytest.raises(ProviderError) as exc_info:
        manager.promote_drafts(2)
    assert exc_info.value.category == "validation_error"
