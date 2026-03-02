"""Tests for set_date functionality in Plato SDK v2.

This test verifies that the set_date function properly sets the system
date on VM environments and can be verified via the execute function.

Run with: pytest tests/test_set_date.py -v -s
"""

import asyncio
import logging
import os
from datetime import datetime

import pytest
from dotenv import load_dotenv

from plato.v2 import AsyncPlato, Env

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Skip if no API key is available
pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY environment variable not set",
)

# Spree artifact (same as test_heartbeat_keepalive.py)
SPREE_ARTIFACT_ID = "a4458137-a2b1-4438-b012-40f0b4fa0cac"


@pytest.mark.asyncio
async def test_set_date_env_level():
    """Test setting the system date on a single environment."""
    plato = AsyncPlato()
    session = None

    try:
        logger.info("=" * 60)
        logger.info("SET DATE TEST (environment level)")
        logger.info("=" * 60)

        # Create session with Spree artifact
        logger.info("[1/4] Creating session with Spree environment...")
        session = await plato.sessions.create(
            envs=[Env.artifact(SPREE_ARTIFACT_ID, alias="spree")],
            timeout=300,
        )

        logger.info(f"Session created: {session.session_id}")

        # Get the environment
        spree_env = session.get_env("spree")
        assert spree_env is not None, "Spree environment not found"

        # Set the date using datetime object
        target_dt = datetime(2023, 12, 25, 10, 0, 0)
        logger.info(f"[2/4] Setting date to: {target_dt}")

        breakpoint()
        result = await spree_env.set_date(target_dt)
        logger.info(f"Set date result: success={result.success}, stdout={result.stdout}")

        assert result.success, f"set_date failed: {result.error}"

        # Verify the date was set using execute
        logger.info("[3/4] Verifying date via execute...")
        exec_result = await spree_env.execute("date '+%Y-%m-%d %H:%M'")
        logger.info(f"Current date on VM: {exec_result.stdout.strip()}")

        # Check that the date contains expected components
        assert "2023-12-25" in exec_result.stdout, f"Date mismatch: expected 2023-12-25 in {exec_result.stdout}"
        assert "10:00" in exec_result.stdout, f"Time mismatch: expected 10:00 in {exec_result.stdout}"

        logger.info("[4/4] Test PASSED")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"TEST FAILED: {e}")
        raise

    finally:
        breakpoint()
        if session:
            await session.close()
        await plato.close()


@pytest.mark.asyncio
async def test_set_date_session_level():
    """Test setting the date at the session level (all environments)."""
    plato = AsyncPlato()
    session = None

    try:
        logger.info("=" * 60)
        logger.info("SET DATE TEST (session level)")
        logger.info("=" * 60)

        # Create session with Spree artifact
        logger.info("[1/4] Creating session...")
        session = await plato.sessions.create(
            envs=[Env.artifact(SPREE_ARTIFACT_ID, alias="spree")],
            timeout=300,
        )

        logger.info(f"Session created: {session.session_id}")

        # Set the date at session level
        target_dt = datetime(2025, 1, 1, 0, 0, 0)
        logger.info(f"[2/4] Setting date on all envs to: {target_dt}")

        result = await session.set_date(target_dt)
        logger.info(f"Set date response: {result.results}")

        # Check all results succeeded
        for job_id, job_result in result.results.items():
            assert job_result.success, f"set_date failed for {job_id}: {job_result.error}"
            logger.info(f"  {job_id}: success={job_result.success}")

        # Verify via execute at session level
        logger.info("[3/4] Verifying date via execute...")
        exec_response = await session.execute("date '+%Y-%m-%d'")

        for job_id, exec_result in exec_response.results.items():
            logger.info(f"  {job_id}: {exec_result.stdout.strip()}")
            assert "2025-01-01" in exec_result.stdout, f"Date mismatch for {job_id}"

        logger.info("[4/4] Test PASSED")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"TEST FAILED: {e}")
        raise

    finally:
        if session:
            await session.close()
        await plato.close()


if __name__ == "__main__":
    # Run all tests
    asyncio.run(test_set_date_env_level())
