"""Regenerate the govnotes sample's precomputed Studio posture from a REAL run.

`efterlev studio --sample` serves `src/efterlev/samples/govnotes/posture.json`
instantly and keyless. To keep it honest, this regenerates it from an actual
`report run` (scan + gap) against the bundled sample — so `--sample` shows the
same verdicts a user gets from `efterlev studio --live --sample`, not an
optimistic heuristic.

Requires an LLM backend (it runs the real gap agent — slow, a few minutes).
`materialize_sample()` initializes the temp workspace with the best available
backend (a local `claude` subscription if present, else the Anthropic API).

Run: `python scripts/build_govnotes_sample.py`
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from typer.testing import CliRunner

from efterlev.cli.main import app
from efterlev.cli.plan import load_baseline_landscape
from efterlev.primitives.readiness.score import load_latest_claim_statuses
from efterlev.studio.server import materialize_sample
from efterlev.studio.web_data import build_studio_data

SAMPLE_POSTURE = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "efterlev"
    / "samples"
    / "govnotes"
    / "posture.json"
)


def main() -> None:
    t0 = time.time()
    ws = materialize_sample()
    print(f"materialized sample at {ws}", flush=True)

    result = CliRunner().invoke(
        app,
        [
            "report", "run", "--target", str(ws),
            "--skip-init", "--skip-document", "--skip-poam",
            "--skip-vdr", "--skip-inventory", "--skip-inspector",
        ],
    )  # fmt: skip
    if result.exit_code != 0:
        raise SystemExit(f"report run failed (exit {result.exit_code}):\n{result.output[-2000:]}")

    doc, _, _ = load_baseline_landscape()
    statuses = load_latest_claim_statuses(ws, baseline_ksi_ids=set(doc.indicators))
    if not statuses:
        raise SystemExit("no verdicts produced — the gap agent did not classify any KSIs")

    payload = build_studio_data(verdicts=dict(statuses), mode="sample")
    SAMPLE_POSTURE.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {SAMPLE_POSTURE}  (in {round(time.time() - t0)}s)", flush=True)
    print(f"  readiness: {payload['readiness']}%  ·  counts: {payload['counts']}", flush=True)


if __name__ == "__main__":
    main()
