"""Integration tests for Plato SDK v2 Multi-Simulator Session API.

This test creates a session with multiple simulators (signoz, gitea, kanboard),
retrieves public URLs, waits for user interaction, and captures state mutations.

Run with: pytest tests/test_v2_multisim_integration.py -v -s
"""

import asyncio
import logging
import os

import pytest
from dotenv import load_dotenv

from plato.v2 import AsyncPlato, Env

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Skip if no API key is available
pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY environment variable not set",
)


@pytest.mark.asyncio
async def test_multisim_session_with_mutations():
    """Test creating a session with multiple simulators and capturing mutations.

    This test:
    1. Creates environments (signoz, gitea, kanboard)
    2. Gets public URLs for browser access
    3. Waits 5 minutes for user to perform actions
    4. Retrieves state mutations from all environments
    """
    plato = AsyncPlato()
    session = None

    try:
        logger.info("=" * 60)
        logger.info("MULTISIM INTEGRATION TEST")
        logger.info("=" * 60)

        # 1. Create session with multiple simulators
        logger.info("[1/3] Creating session with signoz, gitea, and kanboard...")
        session = await plato.sessions.create(
            envs=[
                Env.simulator("signoz", alias="signoz"),
                Env.simulator("gitea", dataset="blank", alias="gitea"),
                Env.simulator("kanboard", alias="kanboard"),
            ],
            timeout=600,  # 10 minutes timeout for environment creation
        )

        logger.info(f"Session created: {session.session_id}")
        logger.info(f"Environments: {len(session.envs)}")
        for env in session.envs:
            logger.info(f"  - {env.alias}: job_id={env.job_id}")

        # 2. Get public URLs
        logger.info("[2/3] Getting public URLs...")
        public_urls = await session.get_public_url()

        logger.info("Public URLs (open in browser):")
        logger.info("-" * 40)
        for alias, url in public_urls.items():
            logger.info(f"  {alias}: {url}")
        logger.info("-" * 40)

        # 3. Reset and get state/mutations
        logger.info("[3/3] Resetting and retrieving state mutations...")
        await session.reset()
        state = await session.get_state()

        logger.info("State Mutations by Environment:")
        logger.info("=" * 60)

        if state.results:
            for job_id, result in state.results.items():
                # Find alias for this job
                alias = next((env.alias for env in session.envs if env.job_id == job_id), job_id)
                logger.info(f"{alias} ({job_id}):")
                logger.info("-" * 40)

                if hasattr(result, "state") and result.state:
                    env_state = result.state
                    # Pretty print the state (limit depth for readability)
                    state_str = str(env_state)
                    logger.info(state_str[:2000])
                    if len(state_str) > 2000:
                        logger.info("... (truncated)")
                else:
                    logger.info(f"  Raw result: {result}")
        else:
            logger.info(f"Raw state response: {state}")

        logger.info("=" * 60)
        logger.info("TEST COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

        # Assertions
        assert session.session_id is not None
        assert len(session.envs) == 3

        # Verify all environments exist
        aliases = {env.alias for env in session.envs}
        assert "signoz" in aliases
        assert "gitea" in aliases
        assert "kanboard" in aliases

    except Exception as e:
        logger.error(f"ERROR: {e}")
        raise

    finally:
        # Cleanup
        if session:
            logger.info("Closing session...")
            await session.close()
        await plato.close()
        logger.info("Cleanup complete.")


@pytest.mark.asyncio
async def test_multisim_quick_state_check():
    """Quick test to verify state retrieval works without waiting.

    Creates environments, immediately gets state, and closes.
    Useful for verifying the API integration works.
    """
    plato = AsyncPlato()
    session = None

    try:
        logger.info("[Quick Test] Creating session with espocrm and invoiceninja...")
        session = await plato.sessions.create(
            envs=[
                Env.simulator("espocrm", alias="espocrm"),
                Env.simulator("invoiceninja", alias="invoiceninja"),
            ],
            timeout=600,
        )

        logger.info(f"Session created: {session.session_id}")

        # Get public URLs
        public_urls = await session.get_public_url()
        logger.info(f"Public URLs retrieved: {len(public_urls)} URLs")

        # Reset environments (required before get_state)
        logger.info("Resetting environments...")
        reset_result = await session.reset()
        logger.info(f"Reset result: {reset_result is not None}")

        # Get state after reset
        logger.info("Getting state after reset...")
        post_reset_state = await session.get_state()
        logger.info(
            f"Post-reset state keys: {list(post_reset_state.results.keys()) if post_reset_state.results else []}"
        )

        assert session.session_id is not None
        assert len(session.envs) == 2

        logger.info("[Quick Test] PASSED")

    finally:
        if session:
            await session.close()
        await plato.close()


@pytest.mark.asyncio
async def test_individual_env_operations():
    """Test operations on individual environments within a session."""
    plato = AsyncPlato()
    session = None

    try:
        logger.info("[Individual Env Test] Creating session...")
        session = await plato.sessions.create(
            envs=[
                Env.simulator("gitea", dataset="blank", alias="gitea"),
                Env.simulator("kanboard", alias="kanboard"),
            ],
            timeout=600,
        )

        logger.info(f"Session created: {session.session_id}")

        # Get individual environments
        gitea_env = session.get_env("gitea")
        kanboard_env = session.get_env("kanboard")

        assert gitea_env is not None, "Gitea environment not found"
        assert kanboard_env is not None, "Kanboard environment not found"

        # Execute command on gitea
        logger.info(f"Executing command on gitea (job_id={gitea_env.job_id})...")
        exec_result = await gitea_env.execute("whoami")
        logger.info(f"Gitea whoami result: {exec_result}")

        # Execute command on kanboard
        logger.info(f"Executing command on kanboard (job_id={kanboard_env.job_id})...")
        exec_result = await kanboard_env.execute("ls -la /app")
        logger.info(f"Kanboard ls result: {exec_result}")

        # Reset and get state from individual env
        logger.info("Resetting and getting state from gitea...")
        await gitea_env.reset()
        gitea_state = await gitea_env.get_state()
        logger.info(f"Gitea state: {gitea_state}")

        logger.info("[Individual Env Test] PASSED")

    finally:
        if session:
            await session.close()
        await plato.close()


if __name__ == "__main__":
    # Run the main test directly
    asyncio.run(test_multisim_session_with_mutations())
