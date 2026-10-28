#!/usr/bin/env python3
"""Claim a sandbox from a service pool (async variant)"""

import asyncio
import os
import sys
import uuid

from koyeb.sandbox import (
    AsyncSandbox,
    PoolClaimError,
    SandboxError,
    ServicePool,
    claim_async,
    get_claim_async,
    wait_claim_ready_async,
)


async def main() -> int:
    api_token = os.environ.get("KOYEB_API_TOKEN")
    if not api_token:
        print("KOYEB_API_TOKEN is not set", file=sys.stderr)
        return 1

    # Use a unique name so concurrent or repeated runs don't collide on the
    # server-side unique (name, workspace) index.
    pool_name = f"claim-demo-{uuid.uuid4().hex[:8]}"

    pool = None
    try:
        pool = await ServicePool.create(name=pool_name, size=1, api_token=api_token)
        print(f"✓ Created pool {pool.id} (size {pool.size})")

        # Claim a sandbox from the pool. The request id is generated once
        # and preserved across internal retries.
        result = await claim_async(pool.id, api_token=api_token)
        print("✓ Claim fulfilled")
        print(f"  Claim ID:    {result.claim_id}")
        print(f"  Service ID:  {result.service_id}")
        print(f"  Prewarmed:   {result.prewarmed}")
        print(f"  Request ID:  {result.request_id}")

        # Fetch the claim record by id.
        info = await get_claim_async(result.claim_id, api_token=api_token)
        print(f"  Claim status: {info.status}")

        # A claimed service is detached from the pool and owned by the
        # caller: delete it like any other sandbox when done. Resolve AFTER
        # the cold path settles — the claimed service's deployment (and its
        # platform-minted SANDBOX_SECRET) is created asynchronously, so an
        # early resolution races it and fails.
        try:
            if not result.prewarmed:
                # Cold path: the claimed service was provisioned on demand.
                await wait_claim_ready_async(result, api_token=api_token)
                print("✓ Claimed sandbox is ready")

            sandbox = await AsyncSandbox.get_from_id(
                result.service_id, api_token=api_token
            )
            out = await sandbox.exec("echo 'Hello from a claimed sandbox!'")
            print(f"  Output: {out.stdout.strip()}")
            assert out.stdout.strip() == "Hello from a claimed sandbox!"

            # Replay demo: the same (pool_id, request_id) returns the same
            # claim — safe to retry after a network failure.
            replay = await claim_async(
                pool.id, request_id=result.request_id, api_token=api_token
            )
            assert replay.service_id == result.service_id
            print("✓ Replay with the same request_id returned the same service")
        finally:
            # Best-effort teardown resolution so a failed cold path still
            # cleans up the claimed service.
            try:
                (
                    await AsyncSandbox.get_from_id(
                        result.service_id, api_token=api_token
                    )
                ).delete()
            except Exception:  # noqa: BLE001 - cleanup must not mask failures
                pass
            print("✓ Deleted the claimed sandbox service")
        return 0
    except PoolClaimError as e:
        print(f"Claim failed: {e}")
        return 1
    except SandboxError as e:
        print(f"Sandbox error: {e}")
        return 1
    finally:
        # Delete the pool no matter what. The server fences it until
        # outstanding claims drain.
        if pool is not None:
            try:
                await pool.delete()
                print("✓ Deleted the pool")
            except Exception as e:  # noqa: BLE001 - best-effort cleanup
                print(f"⚠ Could not delete pool {pool.id}: {e}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
