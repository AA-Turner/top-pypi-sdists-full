#!/usr/bin/env python3
"""Docker-in-Docker (DIND) using privileged mode"""

import os
import sys
import time
import random
import string

from koyeb import Sandbox

# Startup script based on https://github.com/google/gvisor/blob/master/images/basic/docker/start-dockerd.sh
# Sets up networking and launches dockerd with iptables disabled.
START_DOCKERD_SCRIPT = """\
#!/bin/sh
set -x

# Set up NAT for outbound traffic.
dev=$(ip route show default | awk '/default/ {print $5}')
addr=$(ip addr show dev "$dev" | awk '/inet / {split($2, a, "/"); print a[1]}')

echo 1 > /proc/sys/net/ipv4/ip_forward || true
iptables-legacy -t nat -A POSTROUTING -o "$dev" -j SNAT --to-source "$addr" -p tcp || true
iptables-legacy -t nat -A POSTROUTING -o "$dev" -j SNAT --to-source "$addr" -p udp || true

exec dockerd --iptables=false --ip6tables=false --storage-driver=vfs
"""


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    sandbox = None
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    try:
        print("Creating privileged sandbox with docker:dind...")
        sandbox = Sandbox.create(
            image="docker:dind",
            name=f"dind-example-{suffix}",
            privileged=True,
            entrypoint=["sh"],
            command="/scripts/start-dockerd.sh",
            config_files={
                "/scripts/start-dockerd.sh": START_DOCKERD_SCRIPT,
            },
            wait_ready=True,
            api_token=api_token,
        )
        print("Sandbox created")

        # Wait for the Docker daemon to be ready
        print("\nWaiting for Docker daemon...")
        for i in range(30):
            result = sandbox.exec("docker info", timeout=5)
            if result.exit_code == 0:
                break
            time.sleep(2)
        else:
            print("Error: Docker daemon did not start in time")
            return 1
        print("Docker daemon is ready")

        # Pull a small image
        print("\nPulling alpine image...")
        result = sandbox.exec("docker pull alpine", timeout=60)
        print(result.stdout.strip())
        assert result.exit_code == 0, f"docker pull failed: {result.stderr}"

        # Run a container inside the sandbox
        print("\nRunning container...")
        result = sandbox.exec("docker run --rm alpine echo 'Hello from DIND!'")
        output = result.stdout.strip()
        print(f"Output: {output}")
        assert result.exit_code == 0, f"docker run failed: {result.stderr}"
        assert "Hello from DIND!" in output

        # List running containers
        print("\nDocker images:")
        result = sandbox.exec("docker images")
        print(result.stdout.strip())

        print("\nDIND example completed successfully!")
        return 0

    finally:
        if sandbox:
            sandbox.delete()


if __name__ == "__main__":
    sys.exit(main())
