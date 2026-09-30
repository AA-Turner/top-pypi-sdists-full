#!/usr/bin/env python3
"""Egress network policy: block all outbound traffic or restrict it to an allowlist"""

import os
import random
import string
import sys
import time

from koyeb import Sandbox
from koyeb.sandbox import EgressPolicyError, SandboxError

# Outbound probe run inside the sandbox; fails when egress is blocked
PROBE = (
    'python3 -c "import urllib.request; '
    "urllib.request.urlopen('https://example.com', timeout=5)\""
)

# Probe targeting 1.1.1.1 directly — used to positively confirm an allowlist
# entry actually permits traffic, not just that others are blocked. It opens a
# raw TCP connection using AI_NUMERICHOST so no name resolution is attempted:
# in allowlist mode the DNS resolver is unreachable, and a plain
# urllib/getaddrinfo call would fail with a name-resolution error even for a
# literal IP.
PROBE_ALLOWED = (
    'python3 -c "import socket; '
    "addr = socket.getaddrinfo('1.1.1.1', 80, socket.AF_INET, socket.SOCK_STREAM, 0, socket.AI_NUMERICHOST)[0][4]; "
    "s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); "
    's.settimeout(5); s.connect(addr); s.close()"'
)


def wait_for_probe(sandbox, probe, expect_allowed, label, timeout=120, interval=3):
    """Run a probe repeatedly until it reaches the expected allowed/blocked state.

    A network-policy change redeploys the sandbox. Even after wait_ready()
    reports the new deployment healthy, the data plane needs a few more seconds
    to actually enforce the new egress rules, and the instance can briefly
    return 503s or drop connections while routing to the replacement settles.
    Poll until the probe result is stable instead of asserting on a single shot.
    """
    deadline = time.time() + timeout
    last = "no result"
    while time.time() < deadline:
        try:
            result = sandbox.exec(probe)
        except SandboxError as e:
            # Instance momentarily unreachable during the rollout; retry.
            last = f"exec error: {e}"
            time.sleep(interval)
            continue
        allowed = result.exit_code == 0
        if allowed == expect_allowed:
            state = "allowed" if allowed else "blocked"
            print(f"{label}: {state} (exit code {result.exit_code})")
            return result
        last = f"exit_code={result.exit_code}"
        time.sleep(interval)
    raise AssertionError(
        f"{label}: expected {'allowed' if expect_allowed else 'blocked'} "
        f"within {timeout}s, last observed {last}"
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
        wait_for_probe(sandbox, PROBE, False, "block_network=True → example.com")

        # Switch to an allowlist: only the listed destinations are reachable.
        # Entries are CIDRs or bare IPs (normalized to /32 for IPv4, /128 for
        # IPv6). This triggers a redeployment of the sandbox service.
        sandbox.update_network_policy(outbound_allowlist=["1.1.1.1", "9.9.0.0/16"])
        print("Egress policy updated to allowlist: 1.1.1.1/32, 9.9.0.0/16")

        # The policy update redeploys the sandbox; wait for the new instance to
        # be ready before probing it again.
        sandbox.wait_ready()

        # 1.1.1.1 is in the allowlist → should succeed (once the new egress
        # rules finish propagating to the data plane)
        wait_for_probe(
            sandbox, PROBE_ALLOWED, True, "allowlist=[1.1.1.1, ...] → 1.1.1.1"
        )

        # example.com is NOT in the allowlist → should still fail
        wait_for_probe(sandbox, PROBE, False, "allowlist=[1.1.1.1, ...] → example.com")

        # Reset to the platform default (unrestricted outbound access)
        sandbox.update_network_policy()
        print("Egress policy reset to default")

        # The reset redeploys the sandbox; wait for the new instance to be ready
        # before probing it again.
        sandbox.wait_ready()

        # Default mode → public internet reachable again
        wait_for_probe(sandbox, PROBE, True, "default → example.com")

        return 0
    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
