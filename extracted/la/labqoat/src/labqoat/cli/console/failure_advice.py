"""Evidence-based next commands for unsuccessful logical runs."""

import shlex

from labqoat.json_document import JsonDocument


class FailureAdvice:
    """Offer targeted diagnostics without inferring OOM from a process signal."""

    @staticmethod
    def lines(run: JsonDocument) -> list[str]:
        """Use only retained failure reasons and explicit status to select advice."""
        if run.get("status") not in ("failed", "completed_with_errors"):
            return []
        reference = shlex.quote(str(run.get("id", "RUN")))
        detail = run.get("failure_detail")
        detail = detail if isinstance(detail, dict) else {}
        reason = detail.get("reason")
        if reason == "build_failed":
            return [f"Full build output: lab run logs {reference} --source build --build-output full"]
        if reason == "runtime_lost":
            return ["Worker runtime was lost. Use retries or checkpoint recovery for interrupted work."]
        if reason == "out_of_memory":
            return ["The work needed more memory than it asked for. Raise memory= (MiB) or hold less at once."]
        if reason == "state_deadline_exceeded":
            return FailureAdvice.deadline(str(detail.get("stage", "")), reference)
        return [f"Inspect diagnostics: lab run logs {reference} --level warning"]

    @staticmethod
    def deadline(stage: str, reference: str) -> list[str]:
        """Distinguish placement waiting from execution time and cleanup deadlines."""
        if stage == "queued":
            return [
                f"Inspect placement: lab run placement {reference}; adjust queue_timeout, location, or GPU requirements."
            ]
        if stage == "running":
            return ["Execution reached its deadline. Adjust timeout or resume from a retained checkpoint."]
        return [f"Inspect attempts: lab run attempts list {reference}"]
