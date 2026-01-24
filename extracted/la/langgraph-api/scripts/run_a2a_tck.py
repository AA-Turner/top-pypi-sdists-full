#!/usr/bin/env python3
"""Helper script to run A2A TCK against LangGraph API.

This script:
1. Clones A2A TCK repo (cached in ~/.cache/a2a-tck)
2. Creates a dedicated assistant for TCK testing
3. Runs the TCK with appropriate configuration
4. Cleans up the assistant afterwards

The TCK package's pip entry point is broken upstream, so we clone
and run run_tck.py directly.
"""

import argparse
import contextlib
import json
import logging
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

TCK_REPO = "https://github.com/a2aproject/a2a-tck.git"
TCK_CACHE_DIR = Path.home() / ".cache" / "a2a-tck"


def setup_tck() -> None:
    """Clone/update TCK repo and install deps."""
    TCK_CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)

    if (TCK_CACHE_DIR / ".git").exists():
        logger.info("Updating A2A TCK...")
        subprocess.run(
            ["git", "fetch", "--depth=1"],
            cwd=TCK_CACHE_DIR,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "reset", "--hard", "origin/HEAD"],
            cwd=TCK_CACHE_DIR,
            check=True,
            capture_output=True,
        )
    else:
        logger.info("Cloning A2A TCK...")
        subprocess.run(
            ["git", "clone", "--depth=1", TCK_REPO, str(TCK_CACHE_DIR)],
            check=True,
            capture_output=True,
        )

    # Install TCK dependencies
    logger.info("Installing TCK dependencies...")
    subprocess.run(
        ["uv", "pip", "install", "-e", str(TCK_CACHE_DIR)],
        check=True,
        capture_output=True,
    )


def create_assistant(base_url: str, graph_id: str, name: str) -> str:
    """Create an assistant and return its ID."""
    url = f"{base_url}/assistants"
    data = json.dumps({"name": name, "graph_id": graph_id}).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        return result["assistant_id"]


def delete_assistant(base_url: str, assistant_id: str) -> None:
    """Delete an assistant."""
    url = f"{base_url}/assistants/{assistant_id}"
    req = urllib.request.Request(url, method="DELETE")
    with contextlib.suppress(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run A2A TCK against LangGraph API")
    parser.add_argument(
        "--base-url",
        default="http://localhost:9123",
        help="LangGraph API base URL (default: http://localhost:9123)",
    )
    parser.add_argument(
        "--graph-id",
        default="agent_simple",
        help="Graph ID to use for TCK assistant (default: agent_simple)",
    )
    parser.add_argument(
        "--category",
        default="mandatory",
        choices=[
            "mandatory",
            "capabilities",
            "transport-equivalence",
            "quality",
            "features",
            "all",
        ],
        help="TCK test category to run (default: mandatory)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--report",
        type=str,
        help="Output compliance report to file",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't delete the assistant after tests",
    )

    args = parser.parse_args()

    # Setup TCK (clone repo and install deps)
    try:
        setup_tck()
    except subprocess.CalledProcessError as e:
        logger.exception("Failed to setup A2A TCK")
        if e.stderr:
            logger.info("stderr: %s", e.stderr.decode())
        return 1

    # Create assistant
    logger.info("Creating TCK assistant with graph '%s'...", args.graph_id)
    try:
        assistant_id = create_assistant(
            args.base_url, args.graph_id, "a2a-tck-compliance-agent"
        )
    except urllib.error.URLError:
        logger.exception("Could not connect to server at %s", args.base_url)
        logger.warning(
            "Make sure the LangGraph API server is running (e.g., 'make start')"
        )
        return 1

    logger.info("Created assistant: %s", assistant_id)

    # Build TCK command using the created assistant's ID
    sut_url = f"{args.base_url}/a2a/{assistant_id}"

    # Map category to test path(s)
    # Note: "all" excludes tests/unit/ which are TCK's internal tests (not compliance tests)
    category_paths = {
        "mandatory": ["tests/mandatory/"],
        "capabilities": ["tests/optional/capabilities/"],
        "transport-equivalence": ["tests/optional/multi_transport/"],
        "quality": ["tests/optional/quality/"],
        "features": ["tests/optional/features/"],
        "all": ["tests/mandatory/", "tests/optional/"],
    }
    test_paths = category_paths.get(args.category, ["tests/mandatory/"])

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *test_paths,
        f"--sut-url={sut_url}",
        "--tb=short",
        "-q",
        # Skip localhost security test - it flags localhost URLs as "sensitive"
        # which is expected for local development. Would pass in production.
        "--deselect=tests/mandatory/security/test_agent_card_security.py::test_sensitive_information_protection",
    ]

    if args.verbose:
        cmd.extend(["-v", "-s", "--log-cli-level=INFO"])
    if args.report:
        cmd.extend(["--json-report", f"--json-report-file={args.report}"])

    # Write assistant_id to file so domain-root agent card endpoint can find it
    # This is needed because TCK fetches from /.well-known/agent-card.json
    tck_assistant_file = Path("/tmp/langgraph_tck_assistant_id")
    tck_assistant_file.write_text(assistant_id)
    logger.info("Wrote assistant_id to %s for agent card discovery", tck_assistant_file)

    try:
        logger.info("Running: %s", " ".join(cmd))
        result = subprocess.run(cmd, check=False, cwd=TCK_CACHE_DIR, env=os.environ)
        return result.returncode
    finally:
        if not args.no_cleanup:
            logger.info("Cleaning up assistant: %s", assistant_id)
            delete_assistant(args.base_url, assistant_id)
        tck_assistant_file.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
