#!/bin/bash
# Container smoke tests for the runlayer-aiwatch Linux packages.
#
# Matrix: debian:12 + ubuntu:22.04 install the .deb, rockylinux:9 installs the
# .rpm; each runs assert_inside_container.sh. Packages are amd64-only, so
# containers run with --platform linux/amd64 (Rosetta/qemu on arm64 hosts).
#
# Usage:
#   run_smoke_tests.sh                          # stub mode: build stub pkgs first
#   run_smoke_tests.sh --deb <path> --rpm <path>  # real artifacts (CI/release)
#
# Stub mode validates packaging/wrapper behavior only; the glibc floor and
# real-binary execution need real artifacts — see README.md.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEB="" RPM=""

while [ $# -gt 0 ]; do
    case "$1" in
    --deb) DEB="${2:?--deb needs a path}"; shift 2 ;;
    --rpm) RPM="${2:?--rpm needs a path}"; shift 2 ;;
    *) echo "usage: $0 [--deb <path> --rpm <path>]" >&2; exit 2 ;;
    esac
done

if [ -z "$DEB" ] && [ -z "$RPM" ]; then
    echo "No packages given — building stub packages..."
    STUB_DIR=$(mktemp -d)
    trap 'rm -rf "$STUB_DIR"' EXIT
    "$SCRIPT_DIR/build_stub_packages.sh" "$STUB_DIR"
    DEB=$(ls "$STUB_DIR"/*.deb)
    RPM=$(ls "$STUB_DIR"/*.rpm)
elif [ -z "$DEB" ] || [ -z "$RPM" ]; then
    echo "Provide both --deb and --rpm, or neither (stub mode)." >&2
    exit 2
fi
DEB="$(cd "$(dirname "$DEB")" && pwd)/$(basename "$DEB")"
RPM="$(cd "$(dirname "$RPM")" && pwd)/$(basename "$RPM")"

run_one() { # <image> <deb|rpm> <pkg path>
    docker run --rm --platform linux/amd64 \
        -v "$3:/pkg/pkg.$2:ro" \
        -v "$SCRIPT_DIR/assert_inside_container.sh:/pkg/assert.sh:ro" \
        "$1" bash /pkg/assert.sh "$2" "/pkg/pkg.$2"
}

MATRIX=(
    "debian:12 deb"
    "ubuntu:22.04 deb"
    "rockylinux:9 rpm"
)
# No associative arrays: macOS ships bash 3.2.
RESULTS=()
overall=0

for entry in "${MATRIX[@]}"; do
    read -r image pkg_type <<<"$entry"
    pkg_path=$DEB
    [ "$pkg_type" = rpm ] && pkg_path=$RPM
    echo
    echo "=== $image ($pkg_type: $(basename "$pkg_path")) ==="
    if run_one "$image" "$pkg_type" "$pkg_path"; then
        RESULTS+=("$image PASS")
    else
        RESULTS+=("$image FAIL")
        overall=1
    fi
done

echo
echo "=== Smoke test results ==="
printf '%-16s %s\n' DISTRO RESULT
for line in "${RESULTS[@]}"; do
    read -r image status <<<"$line"
    printf '%-16s %s\n' "$image" "$status"
done
exit $overall
