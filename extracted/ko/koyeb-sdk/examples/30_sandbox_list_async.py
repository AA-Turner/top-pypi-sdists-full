#!/usr/bin/env python3
"""List sandboxes with AsyncSandbox.list() and connect a lazy handle (async)"""

import asyncio
import os
import sys

from koyeb.sandbox import AsyncSandbox, NoSandboxSecretError


async def main() -> int:
    api_token = os.environ.get("KOYEB_API_TOKEN")
    if not api_token:
        print("KOYEB_API_TOKEN is not set", file=sys.stderr)
        return 1

    # Create one sandbox so the listing has something of ours to find.
    ours = await AsyncSandbox.create(name="list-demo", api_token=api_token)
    print(f"✓ Created {ours.service_id}")

    try:
        handles = await AsyncSandbox.list(api_token=api_token)
        print(f"✓ Listed {len(handles)} sandbox service(s)")
        for handle in handles[:5]:
            print(f"  {handle.id}  {handle.name}")

        # Lazy handles have no executor secret...
        raised = False
        try:
            ours_handle = next(h for h in handles if h.id == ours.service_id)
            await ours_handle.exec("echo hi")
        except NoSandboxSecretError:
            raised = True
            print("✓ Lazy handle has no secret, as documented")
        assert raised, "Lazy handle should not carry an executor secret"

        # ...so connect through get_from_id before running commands.
        connected = await AsyncSandbox.get_from_id(
            ours.service_id, api_token=api_token
        )
        out = await connected.exec("echo hello from the list demo")
        print(f"✓ Connected handle output: {out.stdout.strip()}")
        assert out.stdout.strip() == "hello from the list demo"
    finally:
        await ours.delete()
        print("✓ Cleaned up")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
