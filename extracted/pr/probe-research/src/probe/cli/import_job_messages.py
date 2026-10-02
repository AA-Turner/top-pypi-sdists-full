"""Report the durable job's actual state after an enqueue or repeated approval."""

from __future__ import annotations


def enqueue_report(job: dict, label: str) -> list[str]:
    """An existing failed or completed approval was not queued again."""
    state = job.get("state", "queued")
    job_id = job["id"]
    if state == "succeeded":
        return [f"{label} already complete: {job_id}", "View its results in Existing imports."]
    if state in {"failed", "interrupted"}:
        status = "needs attention" if state == "failed" else "interrupted"
        return [
            f"{label} {status}: {job_id}",
            *([str(job["error"])] if job.get("error") else []),
            "Review or resume it in Existing imports.",
        ]
    if state in {"queued", "running"}:
        status = "queued" if state == "queued" else "already running"
        return [
            f"{label} {status}: {job_id}",
            "Runs in the background. Progress: Existing imports.",
        ]
    return [f"{label} saved: {job_id}", "Status: Existing imports."]
