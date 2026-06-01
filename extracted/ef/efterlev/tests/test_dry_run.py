"""Tests for `efterlev agent {gap, document, remediate} --dry-run` (Tier 1 #2b, v0.1.20).

Covers the audit-credibility primitive end-to-end:
- Each agent's `--dry-run` path captures the assembled prompt(s) without
  invoking the LLM (asserted via `StubLLMClient` whose `complete()` is
  set to fail the test if called)
- The dumped JSON has the literal Anthropic API request envelope shape
- Per-prompt `_efterlev` metadata (iteration, label, token + cost estimates)
  is present
- Per-run nonced fences are visible in the captured user message
- `--dump-prompt PATH` writes the file; stdout stays empty (only a
  one-line stderr summary)
- `--dump-prompt PATH` refuses to overwrite existing PATH without `--force`
- `--dump-prompt PATH --force` overwrites cleanly
- `--force` without `--dump-prompt` errors fast (exit 2)
- The dry-run path writes ZERO new rows to the provenance store and ZERO
  lines to receipts.log — no side effects
"""

from __future__ import annotations

import json
from pathlib import Path

from efterlev.agents.dry_run import (
    DryRunSession,
    active_dry_run,
    get_active_dry_run_session,
)

# ---------- DryRunSession unit tests ----------


def test_session_capture_assigns_iteration_and_serializes() -> None:
    session = DryRunSession()
    session.capture(
        model="claude-sonnet-4-6",
        system="sys-prompt",
        messages=[{"role": "user", "content": "user-msg"}],
        max_tokens=4096,
        label="test_agent.first",
    )
    session.capture(
        model="claude-sonnet-4-6",
        system="sys-prompt",
        messages=[{"role": "user", "content": "second-user-msg"}],
        max_tokens=4096,
        label="test_agent.second",
    )
    assert len(session.prompts) == 2
    assert session.prompts[0].iteration == 1
    assert session.prompts[1].iteration == 2
    envelopes = session.to_json_array()
    assert envelopes[0]["model"] == "claude-sonnet-4-6"
    assert envelopes[0]["messages"] == [{"role": "user", "content": "user-msg"}]
    assert envelopes[0]["_efterlev"]["iteration"] == 1
    assert envelopes[0]["_efterlev"]["label"] == "test_agent.first"
    # Token estimate uses 4-chars-per-token approximation.
    assert envelopes[0]["_efterlev"]["token_estimate"] >= 1
    assert envelopes[0]["_efterlev"]["token_estimate_method"] == "approximate (4 chars/token)"
    # Cost estimate populated for a known model.
    assert envelopes[0]["_efterlev"]["cost_estimate_usd"] is not None


def test_session_unregistered_model_skips_dollar_cost() -> None:
    """Unknown model → tokens reported, dollars None."""
    session = DryRunSession()
    session.capture(
        model="claude-future-model-unregistered",
        system="x",
        messages=[{"role": "user", "content": "y"}],
        max_tokens=1000,
        label="x",
    )
    env = session.to_json_array()[0]
    assert env["_efterlev"]["token_estimate"] >= 1
    assert env["_efterlev"]["cost_estimate_usd"] is None


def test_active_dry_run_context_manager_sets_and_restores() -> None:
    assert get_active_dry_run_session() is None
    session = DryRunSession()
    with active_dry_run(session):
        assert get_active_dry_run_session() is session
    assert get_active_dry_run_session() is None


def test_total_cost_estimate_sums_across_prompts() -> None:
    session = DryRunSession()
    for _ in range(3):
        session.capture(
            model="claude-sonnet-4-6",
            system="x" * 4000,  # ~1000 tokens
            messages=[{"role": "user", "content": "y" * 4000}],  # ~1000 tokens
            max_tokens=2000,
            label="x",
        )
    # 3 prompts * (input ~2000 tokens * $3/MTok + output 2000 tokens * $15/MTok)
    #   = 3 * (0.006 + 0.030) = 3 * 0.036 = $0.108
    assert session.total_cost_estimate_usd > 0.05
    assert session.total_cost_estimate_usd < 0.20
    assert session.total_token_estimate >= 6000  # ~2000 per prompt * 3


# ---------- _invoke_llm short-circuit tests ----------


def test_invoke_llm_short_circuits_in_dry_run_without_calling_client() -> None:
    """The whole point: when a session is active, the LLM client's
    `complete()` is never called. Asserts via a stub client that fails
    the test if `complete()` is invoked."""
    from efterlev.agents.gap import GapAgent

    class FailIfCalledClient:
        """Stub LLMClient that fails the test if `complete()` runs."""

        def complete(self, **kwargs: object) -> object:
            raise AssertionError(
                "LLMClient.complete() was called during a dry-run path "
                "— the dry-run interception failed."
            )

    agent = GapAgent(client=FailIfCalledClient())  # type: ignore[arg-type]
    session = DryRunSession()
    with active_dry_run(session):
        # Direct call to _invoke_llm — agent.run() exercises the same
        # path but requires a full input shape; the unit test exercises
        # just the _invoke_llm machinery.
        output, response, _system_prompt = agent._invoke_llm(
            user_message="hello",
            max_tokens=4096,
            dry_run_label="test.unit",
        )

    assert len(session.prompts) == 1
    captured = session.prompts[0]
    assert captured.model == agent.model
    assert captured.system  # non-empty (loaded from gap_prompt.md)
    assert captured.messages == [{"role": "user", "content": "hello"}]
    assert captured.label == "test.unit"
    # The stub output must be structurally valid (would have failed
    # Pydantic validation otherwise).
    from efterlev.agents.gap import GapReport

    assert isinstance(output, GapReport)
    assert output.ksi_classifications == []
    assert response.input_tokens == 0
    assert response.output_tokens == 0


# ---------- ProvenanceStore.write_record short-circuit tests ----------


def test_provenance_store_write_record_is_noop_in_dry_run(tmp_path: Path) -> None:
    """Dry-run mode must not write to SQLite, blob store, or receipts.log.
    The returned ProvenanceRecord is a sentinel structurally-valid stub
    so callers (which use record.record_id downstream) don't crash."""
    from efterlev.provenance import ProvenanceStore

    with ProvenanceStore(tmp_path) as store:
        baseline_blob_count = sum(1 for _ in store.iter_records())
        baseline_receipt_lines = (
            len((tmp_path / ".efterlev" / "receipts.log").read_text().splitlines())
            if (tmp_path / ".efterlev" / "receipts.log").exists()
            else 0
        )

        session = DryRunSession()
        with active_dry_run(session):
            stub = store.write_record(
                payload={"key": "value"},
                record_type="claim",
                derived_from=[],
                primitive=None,
                agent="test_agent",
                model="claude-sonnet-4-6",
                prompt_hash="sha256:" + "a" * 64,
            )

        # Stub returned but no rows written.
        assert stub.record_id.startswith("sha256:")
        assert stub.record_type == "claim"
        post_blob_count = sum(1 for _ in store.iter_records())
        post_receipt_lines = (
            len((tmp_path / ".efterlev" / "receipts.log").read_text().splitlines())
            if (tmp_path / ".efterlev" / "receipts.log").exists()
            else 0
        )
        assert post_blob_count == baseline_blob_count
        assert post_receipt_lines == baseline_receipt_lines


# ---------- CLI flag-validation tests ----------


def _runner_invoke(*args: str, env: dict[str, str] | None = None) -> tuple[int, str, str]:
    """Invoke `efterlev` via subprocess to test CLI integration."""
    import os
    import subprocess
    import sys

    full_env = {**os.environ, **(env or {})}
    proc = subprocess.run(  # nosemgrep
        [sys.executable, "-m", "efterlev", *args],
        capture_output=True,
        text=True,
        env=full_env,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_force_without_dump_prompt_errors_fast(tmp_path: Path) -> None:
    """`--force` requires `--dump-prompt`. Without it, the CLI exits 2
    with a clear message before any agent setup runs."""
    code, _stdout, stderr = _runner_invoke("agent", "gap", "--target", str(tmp_path), "--force")
    assert code == 2
    assert "--force requires --dump-prompt" in stderr


# ---------- End-to-end: agent gap dry-run via subprocess ----------


def test_agent_gap_dry_run_captures_prompt_via_subprocess(tmp_path: Path) -> None:
    """Full integration: lay down a fixture, init + scan, then invoke
    `efterlev agent gap --dry-run` against a dummy ANTHROPIC_API_KEY.
    The dummy key would normally cause an auth failure, but in dry-run
    mode no network call happens — proving the interception works."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')

    code, _, _ = _runner_invoke("init", "--target", str(target))
    assert code == 0
    code, _, _ = _runner_invoke("scan", "--target", str(target))
    assert code == 0

    code, stdout, stderr = _runner_invoke(
        "agent",
        "gap",
        "--target",
        str(target),
        "--dry-run",
        env={"ANTHROPIC_API_KEY": "dummy-not-used-in-dry-run"},
    )
    assert code == 0, f"dry-run exited {code}; stderr={stderr}"

    # Stdout is the JSON envelope.
    envelopes = json.loads(stdout)
    assert isinstance(envelopes, list)
    assert len(envelopes) >= 1
    env = envelopes[0]
    assert "model" in env
    assert "system" in env
    assert "messages" in env
    assert "max_tokens" in env
    assert env["messages"][0]["role"] == "user"
    # Per-run nonce visible in the user message (proves the fence
    # wrapping ran — exactly what an auditor needs to see).
    assert "<evidence_" in env["messages"][0]["content"]
    # Per-prompt metadata namespace.
    assert env["_efterlev"]["iteration"] == 1
    assert env["_efterlev"]["token_estimate"] >= 1


def test_agent_gap_dump_prompt_writes_file_and_keeps_stdout_clean(tmp_path: Path) -> None:
    """`--dump-prompt PATH` writes the JSON to PATH; stdout stays empty;
    a one-line summary goes to stderr."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')
    _runner_invoke("init", "--target", str(target))
    _runner_invoke("scan", "--target", str(target))

    dump_path = tmp_path / "prompts.json"
    code, stdout, stderr = _runner_invoke(
        "agent",
        "gap",
        "--target",
        str(target),
        "--dump-prompt",
        str(dump_path),
        env={"ANTHROPIC_API_KEY": "dummy"},
    )
    assert code == 0, f"exited {code}; stderr={stderr}"
    assert stdout == "", f"stdout should be empty when --dump-prompt is set; got: {stdout!r}"
    assert "wrote 1 dry-run prompt(s) to" in stderr
    assert dump_path.exists()
    envelopes = json.loads(dump_path.read_text(encoding="utf-8"))
    assert len(envelopes) == 1
    assert "_efterlev" in envelopes[0]


def test_agent_gap_dump_prompt_refuses_overwrite_without_force(tmp_path: Path) -> None:
    """Existing PATH + no --force → exit 2 with a clear message."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')
    _runner_invoke("init", "--target", str(target))
    _runner_invoke("scan", "--target", str(target))

    dump_path = tmp_path / "prompts.json"
    dump_path.write_text("PRE-EXISTING — must not be overwritten without --force")

    code, _, stderr = _runner_invoke(
        "agent",
        "gap",
        "--target",
        str(target),
        "--dump-prompt",
        str(dump_path),
        env={"ANTHROPIC_API_KEY": "dummy"},
    )
    assert code == 2
    assert "exists; pass --force to overwrite" in stderr
    # File NOT clobbered.
    assert dump_path.read_text() == "PRE-EXISTING — must not be overwritten without --force"


def test_agent_gap_dump_prompt_force_overwrites(tmp_path: Path) -> None:
    """Existing PATH + --force → overwrites cleanly, exit 0."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')
    _runner_invoke("init", "--target", str(target))
    _runner_invoke("scan", "--target", str(target))

    dump_path = tmp_path / "prompts.json"
    dump_path.write_text("OLD CONTENT")

    code, _, stderr = _runner_invoke(
        "agent",
        "gap",
        "--target",
        str(target),
        "--dump-prompt",
        str(dump_path),
        "--force",
        env={"ANTHROPIC_API_KEY": "dummy"},
    )
    assert code == 0, f"exited {code}; stderr={stderr}"
    assert dump_path.read_text() != "OLD CONTENT"
    envelopes = json.loads(dump_path.read_text(encoding="utf-8"))
    assert len(envelopes) >= 1


def test_agent_gap_dry_run_writes_no_new_store_rows(tmp_path: Path) -> None:
    """Side-effect-free contract: zero new SQLite rows or receipts.log
    lines from a dry-run path."""
    target = tmp_path / "repo"
    target.mkdir()
    (target / "main.tf").write_text('resource "aws_s3_bucket" "x" { bucket = "x" }\n')
    _runner_invoke("init", "--target", str(target))
    _runner_invoke("scan", "--target", str(target))

    receipts = target / ".efterlev" / "receipts.log"
    pre_receipts = receipts.read_text().splitlines() if receipts.exists() else []
    pre_db_size = (target / ".efterlev" / "store.db").stat().st_size

    code, _, _ = _runner_invoke(
        "agent",
        "gap",
        "--target",
        str(target),
        "--dry-run",
        env={"ANTHROPIC_API_KEY": "dummy"},
    )
    assert code == 0

    post_receipts = receipts.read_text().splitlines() if receipts.exists() else []
    post_db_size = (target / ".efterlev" / "store.db").stat().st_size
    assert post_receipts == pre_receipts, (
        "dry-run must not append to receipts.log; "
        f"added {len(post_receipts) - len(pre_receipts)} line(s)"
    )
    # SQLite may grow slightly due to free-list churn even on read-only
    # ops; allow a small slack but not a real-row-write magnitude.
    growth = post_db_size - pre_db_size
    assert growth <= 4096, f"store.db grew by {growth} bytes; suggests a write happened"
