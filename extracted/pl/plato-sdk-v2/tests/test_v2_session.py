"""Tests for Plato SDK v2 Session API."""

import os

import pytest

from plato.v2 import Env, Plato

# Skip if no API key is available
pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY environment variable not set",
)


def test_session_create_and_close():
    """Test creating a session with multiple environments and closing it."""
    # Create plato client
    plato = Plato()

    try:
        # Create a session with multiple environments
        # By default, sessions.create waits for all environments to be ready (RUNNING status)
        session = plato.sessions.create(
            envs=[
                Env.simulator("espocrm:staging-latest"),
                Env.simulator("espocrm:staging-latest", alias="espocrm-2"),
            ],
            timeout=300,
        )

        # Verify session was created and all envs are ready
        assert session.session_id is not None
        assert len(session.envs) == 2

        # Verify first env
        assert session.envs[0].job_id is not None
        assert session.envs[0].artifact_id is not None

        # Verify second env
        assert session.envs[1].alias == "espocrm-2"
        assert session.envs[1].job_id is not None
        assert session.envs[1].artifact_id is not None

        # Close the session
        session.close()

    finally:
        # Close the plato client
        plato.close()
