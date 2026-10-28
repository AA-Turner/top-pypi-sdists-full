#!/usr/bin/env python3
"""Service pool lifecycle: create, list, update, and delete a pool.

A service pool keeps a target number of warm sandboxes ready so that
claiming (see examples/29_pool_claim.py) hands out a pre-provisioned
service instead of provisioning one on demand.
"""

import os
import sys
import uuid

from koyeb.sandbox import ServicePool


def main() -> int:
    api_token = os.environ.get("KOYEB_API_TOKEN")
    if not api_token:
        print("KOYEB_API_TOKEN is not set", file=sys.stderr)
        return 1

    # Use a unique name so concurrent or repeated runs don't collide on the
    # server-side unique (name, workspace) index.
    pool_name = f"my-pool-{uuid.uuid4().hex[:8]}"

    pool = None
    try:
        # Create a pool of 3 warm sandboxes. Definition options mirror
        # Sandbox.create (image, instance_type, env, region, ...).
        pool = ServicePool.create(name=pool_name, size=3, api_token=api_token)
        print(f"✓ Created {pool}")
        assert pool.id, "Pool creation returned no id"

        # List every pool the caller can see.
        pools = ServicePool.list(api_token=api_token)
        print(f"✓ Listed {len(pools)} pool(s)")
        assert any(p.id == pool.id for p in pools), "Created pool missing from list"

        # Update the pool's target size.
        pool.update(size=5)
        print("✓ Updated: size=5")

        # Refresh returns a new handle: read state from it, not the stale one.
        pool = pool.refresh()
        print(f"✓ Refreshed, ready_count={pool.ready_count}, status={pool.status}")
        assert pool.size == 5, f"Expected size 5 after update, got {pool.size}"
    except Exception as e:  # noqa: BLE001 - surface any failure but still clean up
        print(f"✗ Service pool example failed: {e}", file=sys.stderr)
        return 1
    finally:
        # Delete the pool no matter what. The server fences it until
        # outstanding claims drain.
        if pool is not None:
            try:
                pool.delete()
                print("✓ Deleted")
            except Exception as e:  # noqa: BLE001 - best-effort cleanup
                print(f"⚠ Could not delete pool {pool.id}: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
