"""Load source data into a Plato sim via DatagenSession.

Launches a DatagenSession against an artifact (so the db MCP gets wired
via ``/api/v1/simulator/{artifact_id}/db_config``), sends one prompt
containing the records inline, polls until the agent finishes, prints
the agent's structured JSON report.

    export PLATO_API_KEY=...
    export PLATO_ARTIFACT_ID=18ad7d5c-...
    cd python-sdk
    uv run --python 3.12 python examples/load_source_data.py
"""

from __future__ import annotations

import json
import os
import sys
import time

from plato.v2 import DATA_LOAD_INSTRUCTION, Env, Plato


def main() -> int:
    artifact_id = os.environ.get("PLATO_ARTIFACT_ID")
    if not artifact_id:
        sys.exit("PLATO_ARTIFACT_ID required")

    rows = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Carol", "email": "carol@example.com"},
    ]

    plato = Plato()
    session = plato.datagen_sessions.create(
        envs=[Env.artifact(artifact_id, alias="main")],
        experiment="agent-data-load",
        instruction=DATA_LOAD_INSTRUCTION,
    )
    try:
        session.send_message(f"Insert into the users table on env main:\n{json.dumps(rows)}")
        while True:
            resp = session.poll_message()
            if resp.status != "running":
                break
            print(f"  status={resp.status} iter={resp.iteration} ...")
            time.sleep(5)
        print(f"final status={resp.status} iter={resp.iteration}")
        if resp.error:
            print(f"error: {resp.error}")
        if resp.text:
            print(resp.text)
    finally:
        session.close()
        plato.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
