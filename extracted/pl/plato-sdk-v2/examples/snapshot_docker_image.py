#!/usr/bin/env python3
"""Snapshot a custom Docker base image.

This example starts a blank VM with a custom Docker image (e.g., computer-use agent)
and creates a snapshot using the snapshot-store pipeline.

Usage:
    export PLATO_API_KEY=your-key
    python snapshot_docker_image.py
"""

import logging
import os

from dotenv import load_dotenv

from plato.v2 import Env, Plato
from plato.v2.types import SimConfigCompute

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Custom Docker image to snapshot
DOCKER_IMAGE = "383806609161.dkr.ecr.us-west-1.amazonaws.com/agents/plato/computer-use:1.3.0"

# Simulator name for the snapshot artifact
SIMULATOR_NAME = "computer-use-agent"


def main():
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        logger.error("PLATO_API_KEY not set")
        return 1

    logger.info("=" * 70)
    logger.info("SNAPSHOT DOCKER IMAGE EXAMPLE")
    logger.info("=" * 70)
    logger.info(f"Docker image: {DOCKER_IMAGE}")
    logger.info(f"Simulator name: {SIMULATOR_NAME}")
    logger.info("")

    plato = Plato()
    session = None

    try:
        # Create a blank VM with custom Docker image
        logger.info("Creating session with custom Docker image...")
        session = plato.from_envs(
            envs=[
                Env.resource(
                    simulator=SIMULATOR_NAME,
                    sim_config=SimConfigCompute(
                        cpus=4,
                        memory=8192,
                        disk=20480,
                    ),
                    docker_image_url=DOCKER_IMAGE,
                    alias="agent",
                )
            ],
            timeout=600,
        )

        logger.info(f"Session created: {session.session_id}")
        logger.info(f"Environment: {session.envs[0].job_id}")

        # Wait for VM to be fully ready
        logger.info("Waiting for VM to be ready...")
        session.wait_until_ready(timeout=300)

        # Optionally run some setup commands
        logger.info("Running setup commands...")
        result = session.execute("uname -a && df -h", timeout=30)
        for job_id, res in result.results.items():
            logger.info(f"  {job_id}: {res.stdout[:200] if res.stdout else '(no output)'}")

        # Create disk snapshot (disk-only, uses snapshot-store for chunk-based dedup)
        logger.info("Creating disk snapshot...")
        snapshot_result = session.disk_snapshot(
            override_service=SIMULATOR_NAME,
            override_version="1.3.0",
            override_dataset="base",
        )

        for job_id, info in snapshot_result.results.items():
            if info.artifact_id:
                logger.info(f"  {job_id}: artifact_id={info.artifact_id}")
            else:
                logger.error(f"  {job_id}: snapshot failed - {info.error}")

        logger.info("")
        logger.info("SUCCESS: Snapshot created!")
        logger.info("You can now use this artifact with:")
        logger.info(f'  Env.simulator("{SIMULATOR_NAME}", tag="1.3.0")')
        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        if session:
            logger.info("Closing session...")
            session.close()
        plato.close()


if __name__ == "__main__":
    exit(main())
