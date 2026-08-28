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

# Probe targeting 1.1.1.1 directly — used to positively confirm an
# allowlist entry actually permits traffic, not just that others are blocked.
PROBE_ALLOWED = (
    'python3 -c "import urllib.request; '
    "urllib.request.urlopen('http://1.1.1.1', timeout=5)\""
)


def assert_blocked(result, label):
    assert result.exit_code != 0, f"{label}: expected outbound request to fail"
    print(f"{label}: blocked (exit code {result.exit_code})")


def assert_allowed(result, label):
    assert result.exit_code == 0, f"{label}: expected outbound request to succeed"
    print(f"{label}: allowed (exit code {result.exit_code})")


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
        assert_blocked(result, "block_network=True → example.com")

        # Switch to an allowlist: only the listed destinations are reachable.
        # Entries are CIDRs or bare IPs (normalized to /32 for IPv4, /128 for
        # IPv6). This triggers a redeployment of the sandbox service.
        sandbox.update_network_policy(outbound_allowlist=["1.1.1.1", "9.9.0.0/16"])
        print("Egress policy updated to allowlist: 1.1.1.1/32, 9.9.0.0/16")

        # 1.1.1.1 is in the allowlist → should succeed
        result = sandbox.exec(PROBE_ALLOWED)
        assert_allowed(result, "allowlist=[1.1.1.1, ...] → 1.1.1.1")

        # example.com is NOT in the allowlist → should still fail
        result = sandbox.exec(PROBE)
        assert_blocked(result, "allowlist=[1.1.1.1, ...] → example.com")

        # Reset to the platform default (unrestricted outbound access)
        sandbox.update_network_policy()
        print("Egress policy reset to default")

        # Default mode → public internet reachable again
        result = sandbox.exec(PROBE)
        assert_allowed(result, "default → example.com")

        return 0
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
