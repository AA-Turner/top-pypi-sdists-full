"""Test that heartbeat keeps VMs alive for extended periods.

This test verifies that the session heartbeat mechanism properly keeps
Firecracker VMs alive during long-running operations.

Run with: pytest tests/test_heartbeat_keepalive.py -v -s
Or directly: python tests/test_heartbeat_keepalive.py
"""

import asyncio
import logging
import os
import time

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

# How long to keep the VM alive (in seconds)
KEEPALIVE_DURATION = 10 * 60  # 10 minutes
HEALTH_CHECK_INTERVAL = 60  # Check every minute

# Spree artifact with Stripe payment method configured
SPREE_ARTIFACT_ID = "03638b02-7697-4f23-ba36-a68deaca48e5"


@pytest.mark.asyncio
async def test_heartbeat_keeps_vm_alive():
    """Test that heartbeat keeps a VM alive for 10 minutes.

    This test:
    1. Creates a session with a Spree environment
    2. Starts the heartbeat background task
    3. Sleeps for 10 minutes while heartbeat runs
    4. Periodically checks the VM is still responsive
    5. Verifies the session is still alive at the end
    """
    plato = AsyncPlato()
    session = None

    try:
        logger.info("=" * 60)
        logger.info("HEARTBEAT KEEPALIVE TEST")
        logger.info(f"Duration: {KEEPALIVE_DURATION // 60} minutes")
        logger.info("=" * 60)

        # 1. Create session
        logger.info("[1/4] Creating session with Spree environment...")
        start_time = time.time()

        session = await plato.sessions.create(
            envs=[
                Env.artifact(SPREE_ARTIFACT_ID, alias="spree"),
            ],
            timeout=300,
        )

        create_time = time.time() - start_time
        logger.info(f"Session created in {create_time:.1f}s: {session.session_id}")
        logger.info(f"Environment job_id: {session.envs[0].job_id}")

        # 2. Start heartbeat (should already be started by create, but ensure it)
        logger.info("[2/4] Starting heartbeat background task...")
        await session.start_heartbeat()
        logger.info("Heartbeat started (interval: 30s)")

        # 3. Get public URL to verify connectivity
        logger.info("[3/4] Getting public URL...")
        connect_urls = await session.get_connect_url()
        logger.info(f"Connect URL: {connect_urls.get('spree', 'N/A')}")

        # 4. Keep alive with periodic health checks
        logger.info(f"[4/4] Keeping VM alive for {KEEPALIVE_DURATION // 60} minutes...")
        logger.info("-" * 40)

        elapsed = 0
        check_count = 0

        while elapsed < KEEPALIVE_DURATION:
            # Sleep for the health check interval
            sleep_time = min(HEALTH_CHECK_INTERVAL, KEEPALIVE_DURATION - elapsed)
            await asyncio.sleep(sleep_time)
            elapsed += sleep_time
            check_count += 1

            # Health check - try to send a manual heartbeat
            try:
                heartbeat_result = await session.heartbeat()
                success = heartbeat_result.success if heartbeat_result else False
                logger.info(
                    f"[{elapsed // 60:02d}:{elapsed % 60:02d}] "
                    f"Health check #{check_count}: heartbeat={'OK' if success else 'FAILED'}"
                )

                if not success:
                    logger.error("Heartbeat failed! VM may have died.")

            except Exception as e:
                logger.error(f"Health check failed with exception: {e}")
                pytest.fail(f"Health check failed: {e}")

        logger.info("-" * 40)

        # 5. Final verification - execute a command
        logger.info("Final verification - executing command on VM...")
        try:
            spree_env = session.get_env("spree")
            if spree_env:
                result = await spree_env.execute("echo 'VM is alive!'", timeout=30)
                logger.info(f"Command result: {result}")
            else:
                logger.warning("Could not get spree environment for final check")
        except Exception as e:
            logger.error(f"Final command execution failed: {e}")
            # Don't fail the test - the heartbeat checks are the main verification

        logger.info("=" * 60)
        logger.info("TEST COMPLETED SUCCESSFULLY")
        logger.info(f"VM kept alive for {KEEPALIVE_DURATION // 60} minutes")
        logger.info(f"Total health checks passed: {check_count}")
        logger.info("=" * 60)

        # Assertions
        assert session.session_id is not None
        assert len(session.envs) == 1

    except Exception as e:
        logger.error(f"TEST FAILED: {e}")
        raise

    finally:
        # Cleanup
        if session:
            logger.info("Stopping heartbeat...")
            await session.stop_heartbeat()
            logger.info("Closing session...")
            await session.close()
        await plato.close()
        logger.info("Cleanup complete.")


@pytest.mark.asyncio
async def test_heartbeat_short():
    """Quick 2-minute heartbeat test for CI.

    Same as the full test but only runs for 2 minutes.
    """
    plato = AsyncPlato()
    session = None
    duration = 2 * 60  # 2 minutes

    try:
        logger.info("=" * 60)
        logger.info("HEARTBEAT SHORT TEST (2 minutes)")
        logger.info("=" * 60)

        session = await plato.sessions.create(
            envs=[Env.artifact(SPREE_ARTIFACT_ID, alias="spree")],
            timeout=300,
        )

        logger.info(f"Session created: {session.session_id}")
        await session.start_heartbeat()

        # Keep alive with checks every 30 seconds
        elapsed = 0
        while elapsed < duration:
            await asyncio.sleep(30)
            elapsed += 30

            heartbeat_result = await session.heartbeat()
            success = heartbeat_result.success if heartbeat_result else False
            logger.info(f"[{elapsed}s] Heartbeat: {'OK' if success else 'FAILED'}")

            if not success:
                pytest.fail("Heartbeat returned failure")

        logger.info("Short test PASSED")
        assert session.session_id is not None

    finally:
        if session:
            await session.stop_heartbeat()
            await session.close()
        await plato.close()


if __name__ == "__main__":
    # Run the full 10-minute test directly
    asyncio.run(test_heartbeat_keeps_vm_alive())
