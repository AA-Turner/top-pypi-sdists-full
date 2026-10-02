"""Bounded model repair, durable restart, and safe diagnostics using synthetic drafts."""

import hashlib
import json

import pytest

from probe.cli import backfill_reconstruction as rec


@pytest.fixture
def inputs():
    return {
        "input_id": "synthetic-input",
        "sources": {"F001": {"url": "/artifacts/synthetic"}},
        "inventory_count": 1,
        "gaps": [],
    }


def response(count=1):
    return json.dumps(
        {
            "sections": [
                {
                    "title": "Purpose",
                    "claims": [
                        {"text": "The encoder is frozen.", "sources": ["F001"]}
                        for _ in range(count)
                    ],
                }
            ],
        }
    )


def test_cached_28_claims_repairs_once_preserves_bytes_and_reuses_valid_cache(
    tmp_path, monkeypatch, inputs
):
    original = response(28).encode()
    (tmp_path / "response.json").write_bytes(original)
    calls = []

    def launch(directory, prompt, **kwargs):
        calls.append(prompt)
        # The intent must be durable before a paid call begins.
        marker = json.loads((directory / "repair.json").read_text())
        assert marker["attempts"] == 1
        assert marker["validation_code"] == "claim_count"
        assert marker["input_hash"] == rec._hash(inputs)
        assert "28 claims; maximum is 24" in prompt
        assert str(directory / "evidence.json") in prompt
        assert str(directory / "response.rejected.json") in prompt
        assert (directory / "response.rejected.json").read_bytes() == original
        assert not (directory / "response.json").exists()
        assert kwargs["label"] == "repairing file reconstruction"
        (directory / "response.json").write_text(response(24))
        return True, ""

    monkeypatch.setattr(rec.bf, "launch_agent", launch)
    draft = rec._generate(inputs, tmp_path, agent=None)
    assert draft.count("[F001](/artifacts/synthetic)") == 24
    assert rec._generate(inputs, tmp_path, agent=None) == draft
    assert len(calls) == 1
    assert (tmp_path / "response.rejected.json").read_bytes() == original
    assert (tmp_path / "repair.json").stat().st_mode & 0o777 == 0o600


def test_fresh_invalid_draft_has_only_one_repair_launch(tmp_path, monkeypatch, inputs):
    labels = []

    def launch(directory, prompt, **kwargs):
        labels.append(kwargs["label"])
        (directory / "response.json").write_text(response(28 if len(labels) == 1 else 1))
        return True, ""

    monkeypatch.setattr(rec.bf, "launch_agent", launch)
    assert "[F001](/artifacts/synthetic)" in rec._generate(inputs, tmp_path, agent=None)
    assert labels == ["drafting file reconstruction", "repairing file reconstruction"]
    assert json.loads((tmp_path / "response.rejected.json").read_text()) == json.loads(response(28))


@pytest.mark.parametrize("failure", ["invalid", "missing", "failed", "interrupted"])
def test_failed_or_uncertain_repair_does_not_repeat_on_restart(
    tmp_path, monkeypatch, inputs, failure
):
    (tmp_path / "response.json").write_text(response(28))
    calls = []

    def launch(directory, prompt, **kwargs):
        calls.append(prompt)
        if failure == "interrupted":
            raise SystemExit(73)
        if failure == "invalid":
            (directory / "response.json").write_text(response(28))
        return failure != "failed", "untrusted agent output must not be reported"

    monkeypatch.setattr(rec.bf, "launch_agent", launch)
    with pytest.raises(SystemExit if failure == "interrupted" else rec.DraftValidationError):
        rec._generate(inputs, tmp_path, agent=None)
    for _ in range(2):
        with pytest.raises(rec.DraftValidationError, match="bounded repair already attempted"):
            rec._generate(inputs, tmp_path, agent=None)
    assert len(calls) == 1
    assert (tmp_path / "response.rejected.json").read_text() == response(28)


def test_repaired_output_survives_process_exit_before_checkpoint(tmp_path, monkeypatch, inputs):
    (tmp_path / "response.json").write_text(response(28))
    calls = []

    def launch(directory, prompt, **kwargs):
        calls.append(prompt)
        (directory / "response.json").write_text(response())
        raise SystemExit(73)

    monkeypatch.setattr(rec.bf, "launch_agent", launch)
    with pytest.raises(SystemExit):
        rec._generate(inputs, tmp_path, agent=None)
    assert "[F001](/artifacts/synthetic)" in rec._generate(inputs, tmp_path, agent=None)
    assert len(calls) == 1


def test_archive_before_repair_intent_crash_recovers_same_rejected_draft(
    tmp_path, monkeypatch, inputs
):
    original = response(28)
    (tmp_path / "response.rejected.json").write_text(original)
    calls = []

    def launch(directory, prompt, **kwargs):
        calls.append(kwargs["label"])
        assert "28 claims; maximum is 24" in prompt
        assert (directory / "response.rejected.json").read_text() == original
        (directory / "response.json").write_text(response())
        return True, ""

    monkeypatch.setattr(rec.bf, "launch_agent", launch)
    assert "[F001](/artifacts/synthetic)" in rec._generate(inputs, tmp_path, agent=None)
    assert calls == ["repairing file reconstruction"]


@pytest.mark.parametrize(
    "raw,code",
    [
        ("not-json SECRET", "json"),
        ("[]", "root"),
        ('{"sections":{}}', "sections"),
        ('{"sections":[null]}', "section"),
        ('{"sections":[{"title":[],"claims":[]}]}', "section"),
        ('{"sections":[{"title":"Purpose","claims":[null]}]}', "claim"),
        (response().replace("The encoder is frozen.", "SECRET<br>"), "claim_plaintext"),
        (response().replace('"F001"', '"SECRET"'), "citation_source"),
        (response().replace('["F001"]', "[]"), "citations"),
        (response().replace('"The encoder is frozen."', "42"), "claim_text"),
        (response().replace("The encoder is frozen.", "x" * 1201), "claim_length"),
        (response().replace("The encoder is frozen.", r"\ud800"), "claim_encoding"),
        (json.dumps({"sections": [{"title": "Purpose", "claims": []}] * 6}), "section_count"),
        (response(28), "claim_count"),
    ],
)
def test_distinct_validation_diagnostics_never_echo_generated_content(inputs, raw, code):
    with pytest.raises(rec.DraftValidationError) as caught:
        rec._render(raw, inputs)
    assert caught.value.code == code
    assert "SECRET" not in str(caught.value)
    assert len(str(caught.value)) < 200


@pytest.mark.parametrize(
    "raw,code",
    [
        (b"\xffnot UTF-8", "encoding"),
        (b"x" * (rec.MAX_OUTPUT_BYTES + 1), "output_size"),
    ],
)
def test_repair_preserves_nontext_or_oversized_rejected_output(
    tmp_path, monkeypatch, inputs, raw, code
):
    (tmp_path / "response.json").write_bytes(raw)

    def launch(directory, prompt, **kwargs):
        assert (
            hashlib.sha256((directory / "response.rejected.json").read_bytes()).digest()
            == hashlib.sha256(raw).digest()
        )
        assert json.loads((directory / "repair.json").read_text())["validation_code"] == code
        (directory / "response.json").write_text(response())
        return True, ""

    monkeypatch.setattr(rec.bf, "launch_agent", launch)
    assert "[F001](/artifacts/synthetic)" in rec._generate(inputs, tmp_path, agent=None)
