"""
Integration test for the Plato Sandbox SDK.

This test verifies the basic functionality of the sandbox SDK including:
- Client initialization
- Sandbox creation from artifact
- Getting environment state
- Closing sandbox

Usage:
    PLATO_API_KEY=your_api_key python test_sandbox_sdk.py

Or with a .env file containing PLATO_API_KEY:
    python test_sandbox_sdk.py
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def test_sandbox_sdk():
    """Test basic sandbox SDK operations."""
    from plato.sandbox_sdk import PlatoSandboxClient

    # Get API key from environment
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        print("ERROR: PLATO_API_KEY environment variable is not set")
        print("Set it via: export PLATO_API_KEY=your_api_key")
        sys.exit(1)

    # Use staging by default, can be overridden
    base_url = os.getenv("PLATO_BASE_URL", "https://staging.plato.so/api")

    print(f"Initializing PlatoSandboxClient with base_url={base_url}")
    client = PlatoSandboxClient(api_key, base_url=base_url)
    print(f"Client initialized with client_id={client._client_id}")

    sandbox = None
    try:
        # List available simulators to find an artifact_id
        print("\n--- Listing simulators ---")
        simulators = client.list_simulators()
        print(f"Found {len(simulators)} simulators")
        for sim in simulators[:3]:  # Show first 3
            print(f"  - {sim.name}: {sim.artifact_id}")

        if not simulators:
            print("No simulators available, skipping sandbox creation test")
            return

        # Use the first simulator's artifact_id
        artifact_id = simulators[0].artifact_id
        print(f"\n--- Creating sandbox from artifact: {artifact_id} ---")

        # Create sandbox (wait=True by default)
        sandbox = client.create_sandbox(
            artifact_id="2ea954c0-7e5a-4a12-82fd-12cb46538827",
            wait=True,
            timeout=300,  # 5 minute timeout
        )
        print("Sandbox created!")
        print(f"  public_id: {sandbox.public_id}")
        print(f"  job_group_id: {sandbox.job_group_id}")
        print(f"  status: {sandbox.status}")
        print(f"  url: {sandbox.url}")

        # Test get_state
        print(f"\n--- Getting state for job_group_id={sandbox.job_group_id} ---")
        state = client.get_state(sandbox.job_group_id)
        print("State retrieved successfully!")
        print(f"  State keys: {list(state.keys()) if isinstance(state, dict) else 'N/A'}")
        if isinstance(state, dict) and len(state) > 0:
            # Print first few key-value pairs
            for i, (k, v) in enumerate(state.items()):
                if i >= 3:
                    print(f"  ... and {len(state) - 3} more keys")
                    break
                print(f"  {k}: {v}")

        # Test get_state with merge_mutations=True
        print("\n--- Getting state with merge_mutations=True ---")
        state_merged = client.get_state(sandbox.job_group_id, merge_mutations=True)
        print("State with merged mutations retrieved successfully!")
        print(
            f"  State keys: {list(state_merged.keys()) if isinstance(state_merged, dict) else 'N/A'}"
        )

        print("\n--- All tests passed! ---")

    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
        raise

    finally:
        # Always close the sandbox
        if sandbox:
            print(f"\n--- Closing sandbox {sandbox.public_id} ---")
            try:
                client.close_sandbox(sandbox.public_id)
                print("Sandbox closed successfully")
            except Exception as e:
                print(f"Warning: Failed to close sandbox: {e}")


def test_client_initialization():
    """Test that client initialization works correctly."""
    from plato.sandbox_sdk import PlatoSandboxClient

    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        print("Skipping test_client_initialization: PLATO_API_KEY not set")
        return

    base_url = os.getenv("PLATO_BASE_URL", "https://staging.plato.so/api")

    # Test basic initialization
    client = PlatoSandboxClient(api_key, base_url=base_url)
    assert client._client_id is not None
    assert client._client_id.startswith("client_")
    print(f"test_client_initialization: PASSED (client_id={client._client_id})")


def test_list_simulators():
    """Test listing simulators."""
    from plato.sandbox_sdk import PlatoSandboxClient

    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        print("Skipping test_list_simulators: PLATO_API_KEY not set")
        return

    base_url = os.getenv("PLATO_BASE_URL", "https://staging.plato.so/api")

    client = PlatoSandboxClient(api_key, base_url=base_url)
    simulators = client.list_simulators()

    assert isinstance(simulators, list)
    print(f"test_list_simulators: PASSED (found {len(simulators)} simulators)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test Plato Sandbox SDK")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick tests only (no sandbox creation)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full integration test including sandbox creation",
    )
    args = parser.parse_args()

    if args.quick:
        print("Running quick tests...\n")
        test_client_initialization()
        test_list_simulators()
        print("\nQuick tests completed!")
    elif args.full:
        print("Running full integration test...\n")
        test_sandbox_sdk()
    else:
        # Default: run quick tests
        print("Running quick tests (use --full for full integration test)...\n")
        test_client_initialization()
        test_list_simulators()
        print("\nQuick tests completed!")
