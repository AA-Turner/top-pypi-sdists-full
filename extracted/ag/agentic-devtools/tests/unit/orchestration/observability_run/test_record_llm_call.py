"""Tests for record_llm_call function."""

import json
import threading
from pathlib import Path

from agentic_devtools.orchestration.observability_run import (
    WorkflowRun,
    record_llm_call,
)


class TestRecordLLMCall:
    """Tests for record_llm_call."""

    def test_priced_call_returns_cost(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens=1000,
                output_tokens=500,
                latency_ms=2000,
                validation_result="pass",
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["type"] == "llm_call"
        assert events[0]["estimated_cost_usd"] is not None
        assert events[0]["estimated_cost_usd"] > 0

    def test_unpriced_model_returns_null_cost(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="totally-unknown-model",
                input_tokens=1000,
                output_tokens=500,
                latency_ms=2000,
                validation_result="pass",
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["estimated_cost_usd"] is None

    def test_null_tokens_returns_null_cost(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens=None,
                output_tokens=None,
                latency_ms=1000,
                validation_result="pass",
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["estimated_cost_usd"] is None
        assert events[0]["input_tokens"] is None
        assert events[0]["output_tokens"] is None

    def test_validation_result_recorded(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens=100,
                output_tokens=50,
                latency_ms=500,
                validation_result="failed",
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["validation_result"] == "failed"

    def test_all_required_fields_present(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="plan",
                node_type="work",
                model="gpt-4o",
                input_tokens=500,
                output_tokens=200,
                latency_ms=1500,
                validation_result="pass",
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        event = events[0]
        # Envelope fields
        assert event["version"] == 1
        assert event["event_seq"] == 1
        assert event["type"] == "llm_call"
        assert event["run_id"] == run.run_id
        assert "timestamp" in event
        # LLM-specific fields
        assert event["node_name"] == "plan"
        assert event["node_type"] == "work"
        assert event["model"] == "gpt-4o"
        assert event["input_tokens"] == 500
        assert event["output_tokens"] == 200
        assert event["latency_ms"] == 1500
        assert event["validation_result"] == "pass"

    def test_summary_stats_accumulated(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="n1",
                node_type="t1",
                model="gpt-4o",
                input_tokens=1000,
                output_tokens=500,
                latency_ms=1000,
                validation_result="pass",
            )
            record_llm_call(
                run,
                node_name="n2",
                node_type="t2",
                model="gpt-4o-mini",
                input_tokens=2000,
                output_tokens=1000,
                latency_ms=500,
                validation_result="pass",
            )
            assert run.llm_call_count == 2
            assert run.total_input_tokens == 3000
            assert run.total_output_tokens == 1500
            assert len(run.per_model_stats) == 2

    def test_multiple_calls_same_model_accumulate(self, tmp_path: Path) -> None:
        """Multiple calls to the same model accumulate in per_model_stats."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="n1",
                node_type="t1",
                model="gpt-4o",
                input_tokens=1000,
                output_tokens=500,
                latency_ms=1000,
                validation_result="pass",
            )
            record_llm_call(
                run,
                node_name="n2",
                node_type="t2",
                model="gpt-4o",
                input_tokens=2000,
                output_tokens=1000,
                latency_ms=500,
                validation_result="pass",
            )
            assert run.per_model_stats["gpt-4o"]["calls"] == 2
            assert run.per_model_stats["gpt-4o"]["input_tokens"] == 3000
            assert run.per_model_stats["gpt-4o"]["output_tokens"] == 1500
            assert run.per_model_stats["gpt-4o"]["cost"] is not None
            assert run.per_model_stats["gpt-4o"]["cost"] > 0

    def test_stats_accumulate_correctly_under_concurrency(self, tmp_path: Path) -> None:
        """LLM counters and per-model stats are accurate under concurrent calls."""
        n_threads = 20
        tokens_per_call = 500

        with WorkflowRun(state_dir=tmp_path) as run:
            threads = []
            for i in range(n_threads):
                model = "gpt-4o" if i % 2 == 0 else "gpt-4o-mini"
                t = threading.Thread(
                    target=record_llm_call,
                    kwargs={
                        "run": run,
                        "node_name": f"node_{i}",
                        "node_type": "review",
                        "model": model,
                        "input_tokens": tokens_per_call,
                        "output_tokens": tokens_per_call,
                        "latency_ms": 100,
                        "validation_result": "pass",
                    },
                )
                threads.append(t)

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            assert run.llm_call_count == n_threads
            assert run.total_input_tokens == n_threads * tokens_per_call
            assert run.total_output_tokens == n_threads * tokens_per_call
            # 10 calls each for gpt-4o and gpt-4o-mini
            assert run.per_model_stats["gpt-4o"]["calls"] == 10
            assert run.per_model_stats["gpt-4o-mini"]["calls"] == 10

    def test_bool_input_tokens_coerced_to_none(self, tmp_path: Path) -> None:
        """bool input_tokens (True/False) are treated as missing, not as 1/0."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens=True,
                output_tokens=False,
                latency_ms=500,
                validation_result="pass",
            )
            # Bools coerced to None → counted as missing-token call, not as 1/0 tokens
            assert run.llm_calls_without_tokens == 1
            assert run.total_input_tokens == 0
            assert run.total_output_tokens == 0
            # Cost must be None (no tokens available after coercion)
            assert run.total_estimated_cost is None

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["input_tokens"] is None
        assert events[0]["output_tokens"] is None
        assert events[0]["estimated_cost_usd"] is None

    def test_bool_output_tokens_only_coerced_to_none(self, tmp_path: Path) -> None:
        """A valid input_tokens + bool output_tokens → missing-token call."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens=1000,
                output_tokens=True,
                latency_ms=500,
                validation_result="pass",
            )
            assert run.llm_calls_without_tokens == 1
            assert run.total_input_tokens == 0
            assert run.total_output_tokens == 0

    def test_noops_after_exit(self, tmp_path: Path) -> None:
        run = WorkflowRun(state_dir=tmp_path)
        run.__enter__()
        run.__exit__(None, None, None)

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        before = log_file.read_text() if log_file.exists() else ""

        record_llm_call(
            run,
            node_name="analyze",
            node_type="review",
            model="gpt-4o",
            input_tokens=100,
            output_tokens=50,
            latency_ms=500,
            validation_result="pass",
        )

        after = log_file.read_text() if log_file.exists() else ""
        assert before == after
        assert run.llm_call_count == 0

    def test_float_tokens_coerced_to_int(self, tmp_path: Path) -> None:
        """Float token counts are coerced to int without crashing."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens=1000.7,
                output_tokens=500.3,
                latency_ms=500,
                validation_result="pass",
            )
            assert run.llm_calls_without_tokens == 0
            assert run.total_input_tokens == 1000
            assert run.total_output_tokens == 500

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["input_tokens"] == 1000
        assert events[0]["output_tokens"] == 500

    def test_string_tokens_coerced_to_int(self, tmp_path: Path) -> None:
        """Numeric string token counts are coerced to int without crashing."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens="800",
                output_tokens="400",
                latency_ms=500,
                validation_result="pass",
            )
            assert run.llm_calls_without_tokens == 0
            assert run.total_input_tokens == 800
            assert run.total_output_tokens == 400

    def test_non_numeric_string_tokens_treated_as_none(self, tmp_path: Path) -> None:
        """Non-numeric string tokens are treated as unavailable (no crash)."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens="not-a-number",
                output_tokens=500,
                latency_ms=500,
                validation_result="pass",
            )
            assert run.llm_calls_without_tokens == 1
            assert run.total_input_tokens == 0

    def test_per_model_tokens_excluded_when_either_count_missing(self, tmp_path: Path) -> None:
        """Per-model token totals match overall totals: only counted when both are present."""
        with WorkflowRun(state_dir=tmp_path) as run:
            # Call with valid input but missing output — excluded from overall and per-model
            record_llm_call(
                run,
                node_name="n1",
                node_type="t1",
                model="gpt-4o",
                input_tokens=1000,
                output_tokens=True,  # bool → coerced to None
                latency_ms=500,
                validation_result="pass",
            )
            # Call with both tokens valid — counted in both overall and per-model
            record_llm_call(
                run,
                node_name="n2",
                node_type="t1",
                model="gpt-4o",
                input_tokens=200,
                output_tokens=100,
                latency_ms=500,
                validation_result="pass",
            )
            # Overall totals reflect only the call with complete token data
            assert run.total_input_tokens == 200
            assert run.total_output_tokens == 100
            assert run.llm_calls_without_tokens == 1
            # Per-model totals are consistent with overall totals
            assert run.per_model_stats["gpt-4o"]["input_tokens"] == 200
            assert run.per_model_stats["gpt-4o"]["output_tokens"] == 100
