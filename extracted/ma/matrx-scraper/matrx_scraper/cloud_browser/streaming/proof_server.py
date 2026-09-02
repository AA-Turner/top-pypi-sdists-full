"""Private real-host harness for the stream-ticket safety runbook.

This module is intentionally unusable unless explicitly enabled.  It exercises
the deployed FastAPI/gateway stack over a real network while keeping production
profiles, users, and browser-manager state completely out of the proof.
"""

from __future__ import annotations

import os
from pathlib import Path

from .access import FixtureAccessResolver
from .app import build_standalone_app
from .config import StreamingConfig

PROOF_ORIGIN = "https://aimatrx.com"
PROOF_USER = "browser-proof-user"
PROOF_PROFILE = "browser-proof-profile"


def _build_proof_app():
    if os.environ.get("MATRX_BROWSER_PROOF_SERVER") != "1":
        raise RuntimeError("The browser stream proof server must be explicitly enabled")
    key_path = os.environ.get("MATRX_BROWSER_PROOF_SIGNING_KEY_FILE")
    if not key_path:
        raise RuntimeError("MATRX_BROWSER_PROOF_SIGNING_KEY_FILE is required")

    config = StreamingConfig(
        stream_signing_key_pem=Path(key_path).read_text(),
        allowed_origins=frozenset({PROOF_ORIGIN}),
        turn_shared_secret=os.environ.get("MATRX_BROWSER_PROOF_TURN_KEY"),
        turn_realm="aimatrx.com",
        stun_urls=("stun:turn.aimatrx.com:3478",),
        turn_urls=("turn:turn.aimatrx.com:3478?transport=udp",),
        gateway_ws_base="wss://stream.aimatrx.com",
    )
    access = FixtureAccessResolver()
    access.grant(user_id=PROOF_USER, profile_id=PROOF_PROFILE, level="admin")
    proof_app = build_standalone_app(config, access)

    for suffix in ("primary", "expiry"):
        run_id = f"browser-proof-run-{suffix}"
        proof_app.state.plane.runs.create_run(
            run_id=run_id,
            profile_id=PROOF_PROFILE,
            worker_id="browser-proof-worker",
        )
        handoff_id = proof_app.state.plane.runs.open_handoff(run_id)
        setattr(proof_app.state, f"{suffix}_handoff_id", handoff_id)

    @proof_app.get("/proof/fixture")
    def fixture() -> dict[str, str]:
        return {
            "user_id": PROOF_USER,
            "origin": PROOF_ORIGIN,
            "primary_run_id": "browser-proof-run-primary",
            "primary_handoff_id": proof_app.state.primary_handoff_id,
            "expiry_handoff_id": proof_app.state.expiry_handoff_id,
        }

    return proof_app


app = _build_proof_app()
