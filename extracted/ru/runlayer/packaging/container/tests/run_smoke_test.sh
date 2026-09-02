#!/bin/bash
# Container entrypoint smoke test (stub binary).
#
# Builds a lightweight debian:12-slim image carrying util-linux, a STUB aiwatch
# binary, and the REAL scan-host-users.sh entrypoint, then runs
# assert_inside_container.sh inside it. This validates the fan-out entrypoint
# (numeric-uid setpriv drop, all-users enumeration, dedupe, empty-key gate)
# WITHOUT the manylinux/PyInstaller image build — that full build is exercised
# in CI/release.
#
# Usage: run_smoke_test.sh
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONTAINER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" # cli/packaging/container (build context)
IMAGE="runlayer-aiwatch-entrypoint-stub:test"

echo "=== Building stub entrypoint image ($IMAGE) ==="
# Context = the container packaging dir so both scan-host-users.sh and the stub
# are COPY-able. Native host arch (nothing arch-specific in the stub path).
docker build -t "$IMAGE" -f - "$CONTAINER_DIR" <<'DOCKERFILE'
FROM debian:12-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends util-linux coreutils \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/lib/runlayer/aiwatch
COPY tests/stub-aiwatch.sh /usr/lib/runlayer/aiwatch/aiwatch
COPY scan-host-users.sh /usr/lib/runlayer/scan-host-users.sh
RUN chmod 0755 /usr/lib/runlayer/aiwatch/aiwatch /usr/lib/runlayer/scan-host-users.sh
# Mirrors the real Dockerfile's baked Detect-only managed config.
RUN mkdir -p /etc/runlayer/aiwatch \
    && printf '{\n  "Sessions": false,\n  "Enforcement": false\n}\n' \
        > /etc/runlayer/aiwatch/config.json \
    && chmod 0644 /etc/runlayer/aiwatch/config.json
ENTRYPOINT ["/usr/lib/runlayer/scan-host-users.sh"]
DOCKERFILE

echo
echo "=== Running entrypoint assertions ==="
docker run --rm \
    --entrypoint bash \
    -v "$SCRIPT_DIR/assert_inside_container.sh:/test/assert.sh:ro" \
    "$IMAGE" /test/assert.sh
rc=$?

echo
if [ "$rc" -eq 0 ]; then
    echo "SMOKE TEST: PASS"
else
    echo "SMOKE TEST: FAIL (rc=$rc)"
fi
exit "$rc"
