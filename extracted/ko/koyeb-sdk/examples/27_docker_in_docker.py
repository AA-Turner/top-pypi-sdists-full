#!/usr/bin/env python3
"""Docker-in-Docker: run containers inside a sandbox

Uses the `koyeb/sandbox:dind` image, which ships the Docker daemon and CLI,
builds a container image inside the sandbox, and runs it. The Docker daemon
requires a privileged sandbox, and building/running nested containers is
memory-hungry, so we use an instance type above the default micro
(medium here).

The image is built `FROM scratch` from a static binary already present in the
sandbox image (`runc`), so the example does not pull anything from a registry.
That keeps it deterministic: no external rate limits (e.g. Docker Hub), no
flakes from network egress.
"""

import os
import random
import string
import sys
import time

from koyeb import Sandbox
from koyeb.sandbox import SandboxError

# Seconds to wait for dockerd to accept connections before giving up
DOCKERD_TIMEOUT = 60


def wait_for_docker(sandbox, timeout=DOCKERD_TIMEOUT, interval=2):
    """Poll until the Docker daemon inside the sandbox answers.

    The daemon is started by the image entrypoint and may still be
    initializing when the sandbox first accepts commands.
    """
    deadline = time.time() + timeout
    last = "no result"
    while time.time() < deadline:
        result = sandbox.exec("docker info")
        if result.exit_code == 0:
            print("Docker daemon is ready")
            return
        last = f"exit_code={result.exit_code}: {result.stderr.strip()[:200]}"
        time.sleep(interval)
    raise AssertionError(f"Docker daemon not ready within {timeout}s, last: {last}")


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    sandbox = None
    try:
        print(
            "Creating privileged sandbox (image koyeb/sandbox:dind, instance_type=medium)..."
        )
        create_start = time.time()
        sandbox = Sandbox.create(
            image="koyeb/sandbox:dind",
            name=f"docker-in-docker-{suffix}",
            wait_ready=True,
            instance_type="medium",
            privileged=True,
            api_token=api_token,
        )
        print(
            f"Created sandbox: {sandbox.service_id} (took {time.time() - create_start:.1f}s)"
        )

        # The image entrypoint starts the Docker daemon; it can take a few
        # seconds to accept connections after the sandbox is ready.
        wait_for_docker(sandbox)

        # Build an image entirely offline: `FROM scratch`, with `runc` (a
        # static binary already present in the sandbox image) as the
        # entrypoint. No registry pull is involved at any point.
        print("Building image from scratch (no registry pull)...")
        build_start = time.time()
        result = sandbox.exec(
            "mkdir -p /tmp/ctx && cd /tmp/ctx && "
            "cp $(command -v runc) ./app && "
            'printf \'FROM scratch\\nCOPY app /app\\nENTRYPOINT ["/app", "--version"]\\n\' > Dockerfile && '
            "docker build -q -t hello-offline ."
        )
        if result.exit_code != 0:
            print(f"docker build failed (exit code {result.exit_code}):")
            print(result.stderr)
            return 1
        print(
            f"Built image {result.stdout.strip()} (took {time.time() - build_start:.1f}s)"
        )

        # --pull=never makes the run fail loudly if the image were missing,
        # instead of silently falling back to a registry pull.
        print("Running the container (docker run --pull=never)...")
        run_start = time.time()
        result = sandbox.exec("docker run --pull=never hello-offline")
        run_duration = time.time() - run_start

        if result.exit_code != 0:
            print(f"docker run failed (exit code {result.exit_code}):")
            print(result.stderr)
            return 1

        print(result.stdout)
        # Match the prefix only: the exact runc version depends on the image build
        assert (
            "runc version" in result.stdout
        ), "Expected runc version banner from the container"
        print(f"Container run succeeded (took {run_duration:.1f}s)")
        print("Docker-in-Docker works, fully offline")

        return 0
    except (AssertionError, SandboxError) as e:
        print(f"Error: {e}")
        return 1
    finally:
        if sandbox:
            sandbox.delete()
            print("Sandbox deleted")


if __name__ == "__main__":
    sys.exit(main())
