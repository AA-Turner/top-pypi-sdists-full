#!/bin/bash
# Build Linux distribution artifacts for the Runlayer CLI:
#   - runlayer-<version>-linux-x86_64[-<variant>].tar.gz  (raw onedir bundle)
#   - runlayer_<version>_amd64[.<variant>].deb            (nfpm)
#   - runlayer-<version>-1.x86_64[.<variant>].rpm         (nfpm; appends release "-1")
#   - SHA256SUMS[-<variant>]                              (integrity for all of the above)
#
# Linux has no exec-time signature check (unlike macOS Gatekeeper / Windows
# Authenticode), so SHA256SUMS is the integrity artifact today. To add GPG /
# cosign signing later, sign the artifacts + SHA256SUMS at the marked hook
# below; no key material is wired in yet.
#
# VARIANT_SUFFIX (optional, e.g. glibc2.17) tags a build-variant in the artifact
# FILENAMES and ships a variant marker for self-update pinning (see the Variant
# marker section below). The package name inside the .deb/.rpm stays runlayer,
# so a machine upgrades cleanly across variants and only ever has one
# installed. Empty (default) produces the exact current filenames.
#
# Usage:
#   cd cli
#   ./packaging/linux/build_packages.sh
#   VARIANT_SUFFIX=glibc2.17 ./packaging/linux/build_packages.sh
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

# glibc-shaped tags only: the CDN manifest publisher keys its legacy-variant
# filter on this shape (scripts/publish_distribution_manifest.py) — any other
# tag would be advertised to self-updaters as a second linux installer — and
# the shipped variant marker reuses the value verbatim, so this bounds it too.
VARIANT_SUFFIX="${VARIANT_SUFFIX:-}"
if [ -n "$VARIANT_SUFFIX" ] && ! [[ "$VARIANT_SUFFIX" =~ ^glibc[0-9]+\.[0-9]+$ ]]; then
    echo "Error: VARIANT_SUFFIX must be glibc<major>.<minor> (got '$VARIANT_SUFFIX')" >&2
    exit 1
fi
DEB_FILE="runlayer_${VERSION}_amd64${VARIANT_SUFFIX:+.$VARIANT_SUFFIX}.deb"
RPM_FILE="runlayer-${VERSION}-1.x86_64${VARIANT_SUFFIX:+.$VARIANT_SUFFIX}.rpm"
SUMS_FILE="SHA256SUMS${VARIANT_SUFFIX:+-$VARIANT_SUFFIX}"

if [ ! -d "$DIST_DIR/runlayer" ] || [ ! -x "$DIST_DIR/runlayer/runlayer" ]; then
    echo "Error: dist/runlayer/runlayer not found. Run pyinstaller first." >&2
    exit 1
fi

cd "$CLI_DIR"

echo "Building Runlayer CLI Linux artifacts v${VERSION}${VARIANT_SUFFIX:+ ($VARIANT_SUFFIX variant)}..."

# --- Variant marker ---
# Rides the nfpm tree + tarball to /usr/lib/runlayer/variant: one line, the
# suffix verbatim, trailing newline (readers strip). chmod pins world-readable
# — tar/nfpm preserve on-disk mode, so a hardened build-host umask would
# otherwise ship it unreadable to non-root readers. Cleared up front AND on
# exit: dist/ is shared across sequential builds, and a stale marker would
# make a standard package masquerade as legacy. Standard builds ship NO marker
# (plain tree content, not a conffile), so a legacy→standard upgrade removes
# it.
rm -f "$DIST_DIR/runlayer/variant"
if [ -n "$VARIANT_SUFFIX" ]; then
    printf '%s\n' "$VARIANT_SUFFIX" > "$DIST_DIR/runlayer/variant"
    chmod 644 "$DIST_DIR/runlayer/variant"
    trap 'rm -f "$DIST_DIR/runlayer/variant"' EXIT
fi

# --- Raw tarball ---
TARBALL="$DIST_DIR/runlayer-${VERSION}-linux-x86_64${VARIANT_SUFFIX:+-$VARIANT_SUFFIX}.tar.gz"
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

# Explicit --target file paths (not the directory form): nfpm's directory
# default can't carry the variant tag. The unsuffixed names match nfpm's
# conventional output exactly, so the default build is unchanged.
"$NFPM_BIN" pkg --config "$SCRIPT_DIR/nfpm.yaml" --packager deb --target "$DIST_DIR/$DEB_FILE"
"$NFPM_BIN" pkg --config "$SCRIPT_DIR/nfpm.yaml" --packager rpm --target "$DIST_DIR/$RPM_FILE"

# --- Signing hook (future) ---
# GPG: rpm --addsign + detached .asc; cosign: cosign sign-blob --yes <artifact>.
# Intentionally not wired yet — see plan / packaging/README.md.

# --- Checksums ---
# Explicit filenames (no globs): a dist/ that holds both variants' outputs must
# never leak the other variant's packages into this manifest.
( cd "$DIST_DIR" && sha256sum \
    "$(basename "$TARBALL")" \
    "$DEB_FILE" \
    "$RPM_FILE" \
    > "$SUMS_FILE" )
echo "  Built: $DIST_DIR/$SUMS_FILE"

echo "Done. Linux artifacts in $DIST_DIR:"
ls -1 "$DIST_DIR" | grep -E '^(runlayer.*(deb|rpm|tar\.gz)|SHA256SUMS(-.+)?)$' || true
