#!/bin/bash
# Build Linux distribution artifacts for the Runlayer CLI:
#   - runlayer-<version>-linux-x86_64.tar.gz  (raw onedir bundle)
#   - runlayer_<version>_amd64.deb            (nfpm)
#   - runlayer-<version>.x86_64.rpm           (nfpm)
#   - SHA256SUMS                              (integrity for all of the above)
#
# Linux has no exec-time signature check (unlike macOS Gatekeeper / Windows
# Authenticode), so SHA256SUMS is the integrity artifact today. To add GPG /
# cosign signing later, sign the artifacts + SHA256SUMS at the marked hook
# below; no key material is wired in yet.
#
# Usage:
#   cd cli
#   ./packaging/linux/build_packages.sh
#
# Prerequisites:
#   - PyInstaller-built dist/runlayer/ directory (onedir) must exist
#   - nfpm is installed automatically into build/tools if not on PATH

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIST_DIR="$CLI_DIR/dist"
TOOLS_DIR="$CLI_DIR/build/tools"

VERSION=$(grep -E '^version = ' "$CLI_DIR/pyproject.toml" | head -1 | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Failed to read version from pyproject.toml" >&2
    exit 1
fi
export VERSION

if [ ! -d "$DIST_DIR/runlayer" ] || [ ! -x "$DIST_DIR/runlayer/runlayer" ]; then
    echo "Error: dist/runlayer/runlayer not found. Run pyinstaller first." >&2
    exit 1
fi

cd "$CLI_DIR"

echo "Building Runlayer CLI Linux artifacts v${VERSION}..."

# --- Raw tarball ---
TARBALL="$DIST_DIR/runlayer-${VERSION}-linux-x86_64.tar.gz"
tar -czf "$TARBALL" -C "$DIST_DIR" runlayer
echo "  Built: $TARBALL"

# --- nfpm (.deb + .rpm) ---
NFPM_BIN="$(command -v nfpm || true)"
if [ -z "$NFPM_BIN" ]; then
    echo "  nfpm not on PATH; installing into $TOOLS_DIR..."
    mkdir -p "$TOOLS_DIR"
    NFPM_VERSION="2.43.0"
    curl -sSfL \
        "https://github.com/goreleaser/nfpm/releases/download/v${NFPM_VERSION}/nfpm_${NFPM_VERSION}_Linux_x86_64.tar.gz" \
        | tar -xz -C "$TOOLS_DIR" nfpm
    NFPM_BIN="$TOOLS_DIR/nfpm"
fi

"$NFPM_BIN" pkg --config "$SCRIPT_DIR/nfpm.yaml" --packager deb --target "$DIST_DIR/"
"$NFPM_BIN" pkg --config "$SCRIPT_DIR/nfpm.yaml" --packager rpm --target "$DIST_DIR/"

# --- Signing hook (future) ---
# GPG: rpm --addsign + detached .asc; cosign: cosign sign-blob --yes <artifact>.
# Intentionally not wired yet — see plan / packaging/README.md.

# --- Checksums ---
( cd "$DIST_DIR" && sha256sum \
    "runlayer-${VERSION}-linux-x86_64.tar.gz" \
    runlayer_${VERSION}_amd64.deb \
    runlayer-${VERSION}*.rpm \
    > SHA256SUMS )
echo "  Built: $DIST_DIR/SHA256SUMS"

echo "Done. Linux artifacts in $DIST_DIR:"
ls -1 "$DIST_DIR" | grep -E '^(runlayer.*(deb|rpm|tar\.gz)|SHA256SUMS)$' || true
