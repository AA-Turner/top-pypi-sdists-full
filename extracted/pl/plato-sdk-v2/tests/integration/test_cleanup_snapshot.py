"""Integration test for database cleanup and snapshot functionality."""

import asyncio
import logging
import os

import httpx

from plato.v2.async_.session import Session
from plato.v2.types import EnvFromSimulator

# Configure logging to see debug output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


async def main():
    """Test cleanup and snapshot with multiple environments."""
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        print("Error: PLATO_API_KEY environment variable not set", flush=True)
        return

    base_url = os.environ.get("PLATO_BASE_URL", "https://plato.so")

    print("=" * 60, flush=True)
    print("Database Cleanup & Snapshot Integration Test", flush=True)
    print("=" * 60, flush=True)

    async with httpx.AsyncClient(base_url=base_url, timeout=600.0) as http:
        # Create session with multiple environments
        envs = [
            EnvFromSimulator(simulator="odooemployees", alias="odooemployees"),
            # EnvFromSimulator(simulator="kanboard", alias="kanboard"),
            # EnvFromSimulator(simulator="twenty", alias="twenty"),
        ]

        print("\nCreating session with environments: twenty", flush=True)
        session = await Session.from_envs(
            http_client=http,
            api_key=api_key,
            envs=envs,
            timeout=1800,
        )

        print(f"Session created: {session.session_id}", flush=True)
        print(f"Environments: {[env.alias for env in session.envs]}", flush=True)

        try:
            # Get public URLs for each environment
            print("\n" + "-" * 60, flush=True)
            print("Public URLs (with navigation targets):", flush=True)
            print("-" * 60, flush=True)

            urls = await session.get_public_url()
            for env in session.envs:
                url = urls.get(env.alias, "")

                # Append target parameter for easy browser navigation
                if url:
                    nav_url = f"{url}?target={env.alias}.web.plato.so"
                    print(f"  {env.alias}: {nav_url}", flush=True)
                else:
                    print(f"  {env.alias}: URL not available", flush=True)

            # Wait for user to make mutations
            wait_minutes = 1
            print("\n" + "=" * 60, flush=True)
            print(f"Waiting {wait_minutes} minutes for you to make mutations...", flush=True)
            print("Open the URLs above in your browser and make some changes.", flush=True)
            print("=" * 60, flush=True)

            for remaining in range(wait_minutes * 60, 0, -30):
                mins, secs = divmod(remaining, 60)
                print(f"  Time remaining: {mins}m {secs}s", flush=True)
                await asyncio.sleep(30)

            print("\nTime's up! Running cleanup...", flush=True)

            # Run cleanup_databases
            print("\n" + "-" * 60, flush=True)
            print("Running cleanup_databases()...", flush=True)
            print("-" * 60, flush=True)

            cleanup_results = await session.cleanup_databases()
            for env in session.envs:
                result = cleanup_results.environments.get(env.alias)
                if not result:
                    print(f"\n  {env.alias}: No result", flush=True)
                    continue
                print(f"\n  {env.alias}:", flush=True)
                print(
                    f"    API cleanup: success={result.api_cleanup.success}, skipped={result.api_cleanup.skipped}",
                    flush=True,
                )
                if result.api_cleanup.reason:
                    print(f"    API cleanup reason: {result.api_cleanup.reason}", flush=True)
                print(f"    Databases cleaned: {len(result.databases)}", flush=True)
                for db_name, db_result in result.databases.items():
                    print(
                        f"      {db_name}: success={db_result.success}, tables={db_result.tables_truncated}", flush=True
                    )
                    if db_result.error:
                        print(f"        error: {db_result.error}", flush=True)
                print(f"    Cache cleared: {result.cache_cleared}", flush=True)
                if result.cache_clear_error:
                    print(f"    Cache clear error: {result.cache_clear_error}", flush=True)

            # Run snapshot
            print("\n" + "-" * 60, flush=True)
            print("Running snapshot()...", flush=True)
            print("-" * 60, flush=True)

            snapshot_results = await session.snapshot()
            print(f"Snapshot results: {snapshot_results}", flush=True)

            # Log artifact IDs for validation
            print("\n" + "=" * 60, flush=True)
            print("SNAPSHOT ARTIFACT IDs (for validation):", flush=True)
            print("=" * 60, flush=True)

            if "results" in snapshot_results:
                for env in session.envs:
                    result = snapshot_results["results"].get(env.job_id, {})
                    artifact_id = result.get("artifact_id", "N/A")
                    print(f"  {env.alias}: {artifact_id}", flush=True)
            else:
                print(f"  Raw results: {snapshot_results}", flush=True)

            print("\n" + "=" * 60, flush=True)
            print("Test complete!", flush=True)
            print("=" * 60, flush=True)

        finally:
            print("\nClosing session...", flush=True)
            await session.close()
            print("Session closed.", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
