#!/usr/bin/env python3
"""Claim a sandbox from a service pool (async variant)"""

import asyncio
import os
import sys

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

    pool = await ServicePool.create(name="claim-demo", size=1, api_token=api_token)
    print(f"✓ Created pool {pool.id} (size {pool.size})")

    try:
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
        # caller: delete it like any other sandbox when done.
        sandbox = await AsyncSandbox.get_from_id(result.service_id, api_token=api_token)
        try:
            if not result.prewarmed:
                # Cold path: the claimed service was provisioned on demand.
                await wait_claim_ready_async(result, api_token=api_token)
                print("✓ Claimed sandbox is ready")

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
            await sandbox.delete()
            print("✓ Deleted the claimed sandbox service")
        return 0
    except PoolClaimError as e:
        print(f"Claim failed: {e}")
        return 1
    except SandboxError as e:
        print(f"Sandbox error: {e}")
        return 1
    finally:
        await pool.delete()
        print("✓ Deleted the pool")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
