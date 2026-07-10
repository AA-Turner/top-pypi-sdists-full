#!/usr/bin/env python3
"""Egress network policy: block all outbound traffic or restrict it to an allowlist"""

import os
import random
import string
import sys

from koyeb import Sandbox
from koyeb.sandbox import EgressPolicyError

# Outbound probe run inside the sandbox; fails when egress is blocked
PROBE = (
    'python3 -c "import urllib.request; '
    "urllib.request.urlopen('https://example.com', timeout=5)\""
)


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # block_network and outbound_allowlist are mutually exclusive; passing
    # both is rejected client-side, before any API call
    try:
        Sandbox.create(
            name=f"egress-{suffix}",
            api_token=api_token,
            block_network=True,
            outbound_allowlist=["1.1.1.1"],
        )
        raise AssertionError("Expected EgressPolicyError")
    except EgressPolicyError as e:
        print(f"Conflicting arguments rejected: {e}")

    sandbox = None
    try:
        # Create a sandbox with all outbound network access blocked
        sandbox = Sandbox.create(
            image="koyeb/sandbox",
            name=f"egress-{suffix}",
            wait_ready=True,
            api_token=api_token,
            block_network=True,
        )
        print(f"Created sandbox with block_network=True: {sandbox.name}")

        # Outbound requests from inside the sandbox fail
        result = sandbox.exec(PROBE)
        assert result.exit_code != 0, "Expected outbound request to fail"
        print(f"Outbound request blocked (exit code {result.exit_code})")

        # Switch to an allowlist: only the listed destinations are reachable.
        # Entries are CIDRs or bare IPs (normalized to /32 for IPv4, /128 for
        # IPv6). This triggers a redeployment of the sandbox service.
        sandbox.update_network_policy(outbound_allowlist=["1.1.1.1", "9.9.0.0/16"])
        print("Egress policy updated to allowlist: 1.1.1.1/32, 9.9.0.0/16")

        # Reset to the platform default (unrestricted outbound access)
        sandbox.update_network_policy()
        print("Egress policy reset to default")

        return 0
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
