#!/usr/bin/env python3
"""Interactive evaluation script.

Spins up a Plato session from a simulator, resets with a testcase, opens a Playwright
browser and logs in, then waits for the user to type 'done' before running evaluate.

Usage:
    uv run python scripts/interactive_eval.py <testcase_name_or_id>

Examples:
    uv run python scripts/interactive_eval.py update_opportunity_amount_from_tier_pricing
    uv run python scripts/interactive_eval.py fef0ad8b-1a18-42d8-b815-4a6ec6d290c3
    uv run python scripts/interactive_eval.py update_opportunity_amount_from_tier_pricing --env staging
"""

import argparse

# UUID pattern: 8-4-4-4-12 hex chars
import re

from playwright.sync_api import sync_playwright

from plato._generated.api.v1.session import update_session_testcase
from plato._generated.api.v1.testcases import get_testcases
from plato._generated.models import UpdateSessionTestCaseRequest
from plato.v2 import Env, Plato

_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


def lookup_testcase(http_client, api_key: str, name_or_id: str) -> tuple[int, str, str]:
    """Look up a testcase by name or public_id. Returns (integer_id, name, artifact_public_id)."""
    if _UUID_RE.match(name_or_id):
        result = get_testcases.sync(client=http_client, test_case_public_id=name_or_id, x_api_key=api_key)
    else:
        result = get_testcases.sync(client=http_client, name=name_or_id, x_api_key=api_key)

    cases = result.get("testcases") or result.get("testCases") or []
    if not cases:
        raise RuntimeError(f"No testcase found for {name_or_id!r}")
    if len(cases) > 1:
        matches = [c["name"] for c in cases[:5]]
        raise RuntimeError(f"Multiple testcases matched {name_or_id!r}: {matches} — be more specific")

    tc = cases[0]
    artifacts = tc.get("testCaseArtifacts") or []
    if artifacts:
        artifact_id = artifacts[0]["simulatorArtifact"]["publicId"]
    elif tc.get("simulatorArtifactId"):
        artifact_id = tc["simulatorArtifactId"]
    else:
        raise RuntimeError(f"Testcase {tc['name']!r} has no artifacts")
    return tc["id"], tc["name"], artifact_id


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Spin up a Plato env from a testcase artifact, login, and evaluate on demand."
    )
    parser.add_argument("testcase", help="Testcase name or public UUID")
    parser.add_argument(
        "--env", choices=["prod", "staging"], default="prod", help="Environment to target (default: prod)"
    )
    parser.add_argument("--base-url", default=None, help="Override base URL directly (overrides --env)")
    args = parser.parse_args()

    ENV_URLS = {
        "prod": "https://plato.so",
        "staging": "https://staging.plato.so",
    }
    base_url = args.base_url or ENV_URLS[args.env]
    plato = Plato(base_url=base_url)

    try:
        print(f"Looking up testcase: {args.testcase}")
        testcase_id, testcase_name, artifact_id = lookup_testcase(plato._http, plato.api_key, args.testcase)
        print(f"Found: {testcase_name!r} (id={testcase_id}, artifact={artifact_id})")

        print(f"Creating session from artifact: {artifact_id}")
        session = plato.sessions.create(envs=[Env.artifact(artifact_id)])
        print(f"Session ready: {session.session_id}")

        try:
            print("Linking testcase to session...")
            update_session_testcase.sync(
                client=plato._http,
                session_id=session.session_id,
                body=UpdateSessionTestCaseRequest(testCaseId=testcase_id),
                x_api_key=plato.api_key,
            )

            print("Resetting...")
            session.reset(task_id=testcase_id)
            print("Reset complete.")

            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=False)
                try:
                    print("Logging in...")
                    session.login(browser)
                    print(f"Logged in. Task: {testcase_name}")
                    print("\nBrowser is open. Do your thing, then type 'done' and press Enter to evaluate.")
                    while True:
                        try:
                            user_input = input("> ").strip().lower()
                        except EOFError:
                            break
                        if user_input == "done":
                            break
                        print("Type 'done' to evaluate and exit.")

                    print("Flushing mutations via get_state()...")
                    session.get_state()

                    print("Running evaluate...")
                    resp = plato._http.post(
                        f"/api/v2/sessions/{session.session_id}/evaluate",
                        json={},
                        headers={"X-API-Key": plato.api_key},
                    )
                    resp.raise_for_status()
                    print(f"\nEvaluation result:\n{resp.json()}")

                finally:
                    browser.close()

        finally:
            print("Closing session...")
            session.close()

    finally:
        plato.close()
        print("Done.")


if __name__ == "__main__":
    main()
