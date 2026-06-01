#!/bin/bash
# Build a macOS .pkg installer for AI Watch.
#
# Usage:
#   cd cli
#   ./packaging/macos/build_pkg.sh
#
# Layout shipped by the .pkg (onedir — see aiwatch.spec for rationale):
#   /usr/local/lib/runlayer/aiwatch/                   PyInstaller bundle (exe + dylibs)
#     aiwatch                                          (the real exe)
#     base_library.zip, lib*.dylib, ...
#   /usr/local/bin/aiwatch                             symlink → ../lib/runlayer/aiwatch/aiwatch
#   /Library/LaunchAgents/com.runlayer.aiwatch.plist   scan-on-schedule agent
#
# The LaunchAgent is bundled in the .pkg (not pushed via MDM) because macOS
# configuration profiles have no LaunchAgent payload type and most MDMs
# lack a standalone Launch Agent library item. The postinstall script
# bootstraps it into the console user's GUI domain.
#
# Tenant config (host, org API key value) is supplied at deploy time via an
# MDM Configuration Profile for domain `com.runlayer.aiwatch`. To suppress
# the macOS Ventura+ "Background Item Added" notification, also push the
# Login Items profile (com.runlayer.aiwatch.loginitems.mobileconfig). One
# .pkg ships to every tenant.
#
# Prerequisites: PyInstaller-built `dist/aiwatch/` directory must exist.
# Run `pyinstaller packaging/aiwatch.spec` first, or use
# `make package-aiwatch-macos` which does both steps.
#
# ---------- Signing + notarization (optional, required for MDM) ----------
#
# Without signing, the bundle is ad-hoc signed. The PPPC profile's
# CodeRequirement `identifier "com.runlayer.aiwatch"` will NOT match an
# ad-hoc PyInstaller identifier, so Full Disk Access grants fail and the
# scanner falls back to interactive TCC prompts — unusable from a
# background LaunchAgent. For fleet deployment you MUST sign + notarize.
#
# Required env vars (all or nothing — signing is skipped if APP identity
# is unset):
#
#   AIWATCH_SIGN_IDENTITY_APP   "Developer ID Application: Company (TEAMID)"
#   AIWATCH_SIGN_IDENTITY_PKG   "Developer ID Installer: Company (TEAMID)"
#
# Notarization (optional on top of signing; strongly recommended for any
# .pkg that Gatekeeper will evaluate on a first-launch Mac). Pick one of:
#
#   AIWATCH_NOTARIZE_PROFILE    Keychain profile stored via
#                               `xcrun notarytool store-credentials`
#     -- OR --
#   AIWATCH_NOTARIZE_APPLE_ID   Apple ID email
#   AIWATCH_NOTARIZE_TEAM_ID    10-char Developer Team ID
#   AIWATCH_NOTARIZE_PASSWORD   App-specific password (appleid.apple.com)
#
# Local one-time setup (preferred, keeps creds out of env / CI logs):
#   xcrun notarytool store-credentials aiwatch-notary \
#       --apple-id you@example.com --team-id ABCDE12345 \
#       --password <app-specific-password>
#   export AIWATCH_SIGN_IDENTITY_APP="Developer ID Application: Runlayer Inc. (ABCDE12345)"
#   export AIWATCH_SIGN_IDENTITY_PKG="Developer ID Installer: Runlayer Inc. (ABCDE12345)"
#   export AIWATCH_NOTARIZE_PROFILE=aiwatch-notary
#   make package-aiwatch-macos

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$CLI_DIR/build/pkg"
DIST_DIR="$CLI_DIR/dist"
ENTITLEMENTS="$SCRIPT_DIR/entitlements.plist"

VERSION=$(grep -E '^version = ' "$CLI_DIR/pyproject.toml" | head -1 | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Failed to read version from pyproject.toml" >&2
    exit 1
fi

# Arch the produced .pkg targets. Defaults to the host arch so a local
# `make package-aiwatch-macos` on Apple Silicon yields an arm64 pkg. CI sets
# AIWATCH_PKG_ARCH explicitly per matrix runner. Accepted: arm64, x86_64.
ARCH="${AIWATCH_PKG_ARCH:-$(uname -m)}"
case "$ARCH" in
    arm64|x86_64) ;;
    *) echo "Unsupported arch: $ARCH (expected arm64 or x86_64)" >&2; exit 1 ;;
esac

if [ ! -d "$DIST_DIR/aiwatch" ] || [ ! -x "$DIST_DIR/aiwatch/aiwatch" ]; then
    echo "Error: dist/aiwatch/aiwatch not found. Run pyinstaller first." >&2
    exit 1
fi

# Sanity check: refuse to package a binary that doesn't match the requested
# arch. Catches the "built x86_64 PyInstaller bundle on arm runner" footgun
# that previously produced .pkgs prompting users to install Rosetta.
BIN_ARCHS=$(lipo -archs "$DIST_DIR/aiwatch/aiwatch" 2>/dev/null || file -b "$DIST_DIR/aiwatch/aiwatch")
if ! echo "$BIN_ARCHS" | grep -qw "$ARCH"; then
    echo "Error: dist/aiwatch/aiwatch arch ($BIN_ARCHS) does not include $ARCH" >&2
    exit 1
fi

# Signing switches the whole pipeline: sign every inner Mach-O with
# Developer ID Application, sign the outer .pkg with Developer ID
# Installer, optionally notarize + staple. When unset, produce the
# ad-hoc signed artifact (fast local iteration; not suitable for MDM).
SIGN_APP="${AIWATCH_SIGN_IDENTITY_APP:-}"
SIGN_PKG="${AIWATCH_SIGN_IDENTITY_PKG:-}"
SIGNING_ENABLED=false
if [ -n "$SIGN_APP" ] && [ -n "$SIGN_PKG" ]; then
    SIGNING_ENABLED=true
elif [ -n "$SIGN_APP" ] || [ -n "$SIGN_PKG" ]; then
    echo "Error: signing requires both AIWATCH_SIGN_IDENTITY_APP and AIWATCH_SIGN_IDENTITY_PKG." >&2
    echo "       App identity: ${SIGN_APP:-<unset>}" >&2
    echo "       Pkg identity: ${SIGN_PKG:-<unset>}" >&2
    exit 1
fi

echo "Building AI Watch .pkg v${VERSION} (${ARCH})..."
if [ "$SIGNING_ENABLED" = true ]; then
    echo "  Signing: enabled (app=${SIGN_APP}, pkg=${SIGN_PKG})"
else
    echo "  Signing: DISABLED (ad-hoc). PPPC CodeRequirement will NOT match."
    echo "  Set AIWATCH_SIGN_IDENTITY_APP / _PKG to produce a fleet-ready pkg."
fi

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/payload/usr/local/lib"
mkdir -p "$BUILD_DIR/payload/usr/local/bin"
mkdir -p "$BUILD_DIR/payload/Library/LaunchAgents"
mkdir -p "$BUILD_DIR/scripts"

# `ditto --noextattr --noqtn` (rather than `cp -R`) to avoid AppleDouble `._*`
# sidecar files landing in the payload when the source tree carries xattrs.
ditto --noextattr --noqtn "$DIST_DIR/aiwatch" "$BUILD_DIR/payload/usr/local/lib/runlayer/aiwatch"

# Sign every Mach-O inside the bundle (dylibs, .so, frameworks, inner exes)
# with our Developer ID cert + hardened runtime. We do this inner-to-outer
# so that when codesign reaches the top-level `aiwatch` Mach-O, every
# dependency already has a valid Developer ID signature — avoids the
# "resource envelope is obsolete" / nested-content errors.
#
# `--deep` is deprecated by Apple for signing (only valid for verifying), so
# we iterate manually. Skip files that aren't Mach-O (Python scripts, data
# blobs, __pycache__/*.pyc, etc.).
if [ "$SIGNING_ENABLED" = true ]; then
    echo "  Signing inner Mach-O files..."
    PAYLOAD_BUNDLE="$BUILD_DIR/payload/usr/local/lib/runlayer/aiwatch"
    MAIN_BIN="$PAYLOAD_BUNDLE/aiwatch"
    SIGN_COUNT=0
    while IFS= read -r -d '' f; do
        if [ "$f" = "$MAIN_BIN" ]; then
            continue
        fi
        if ! file -b "$f" 2>/dev/null | grep -q 'Mach-O'; then
            continue
        fi
        codesign --force --options=runtime --timestamp \
            --sign "$SIGN_APP" "$f" >/dev/null
        SIGN_COUNT=$((SIGN_COUNT + 1))
    done < <(find "$PAYLOAD_BUNDLE" -type f -print0)
    echo "    Signed $SIGN_COUNT inner Mach-O files."

    # Top-level binary: pin the TCC-matched identifier + attach entitlements.
    # Must be signed LAST because codesign records hashes of inner content.
    echo "  Signing main binary with identifier=com.runlayer.aiwatch..."
    codesign --force --options=runtime --timestamp \
        --entitlements "$ENTITLEMENTS" \
        --identifier com.runlayer.aiwatch \
        --sign "$SIGN_APP" \
        "$MAIN_BIN"

    # Verify the thing we just signed parses cleanly. `--deep --strict`
    # catches nested content mismatches that would otherwise only surface
    # at first launch on a customer Mac.
    codesign --verify --deep --strict --verbose=2 "$MAIN_BIN"
fi

# Relative symlink so `/usr/local/bin/aiwatch` → `/usr/local/lib/runlayer/aiwatch/aiwatch`
# survives admins moving the prefix around (rare) and is what pkgbuild expects
# to own as a single file in the receipt.
ln -s "../lib/runlayer/aiwatch/aiwatch" "$BUILD_DIR/payload/usr/local/bin/aiwatch"

cp "$SCRIPT_DIR/com.runlayer.aiwatch.plist" \
    "$BUILD_DIR/payload/Library/LaunchAgents/com.runlayer.aiwatch.plist"

cp "$SCRIPT_DIR/scripts/postinstall" "$BUILD_DIR/scripts/postinstall"
chmod +x "$BUILD_DIR/scripts/postinstall"

sed -e "s|__VERSION__|${VERSION}|g" -e "s|__ARCH__|${ARCH}|g" \
    "$SCRIPT_DIR/distribution.xml" \
    > "$BUILD_DIR/distribution.xml"

pkgbuild \
    --root "$BUILD_DIR/payload" \
    --identifier com.runlayer.aiwatch \
    --version "$VERSION" \
    --install-location / \
    --scripts "$BUILD_DIR/scripts" \
    "$BUILD_DIR/aiwatch-component.pkg"

OUT="$DIST_DIR/aiwatch-${VERSION}-macos-${ARCH}.pkg"

# productbuild signs inline when --sign is passed. --timestamp hits Apple's
# Secure Timestamp server; without it, notarization rejects.
if [ "$SIGNING_ENABLED" = true ]; then
    productbuild \
        --distribution "$BUILD_DIR/distribution.xml" \
        --package-path "$BUILD_DIR" \
        --sign "$SIGN_PKG" \
        --timestamp \
        "$OUT"
else
    productbuild \
        --distribution "$BUILD_DIR/distribution.xml" \
        --package-path "$BUILD_DIR" \
        "$OUT"
fi

# ---------- Notarization (optional) ----------
#
# Only attempt if both signing is on AND notary creds are provided. A signed
# but un-notarized .pkg still installs via MDM (MDM push bypasses
# Gatekeeper's first-launch check for pkgs delivered through InstallApplication),
# but Gatekeeper WILL block it on a manually double-clicked install. Notarize
# for belt-and-suspenders.
NOTARIZE_PROFILE="${AIWATCH_NOTARIZE_PROFILE:-}"
NOTARIZE_APPLE_ID="${AIWATCH_NOTARIZE_APPLE_ID:-}"
NOTARIZE_TEAM_ID="${AIWATCH_NOTARIZE_TEAM_ID:-}"
NOTARIZE_PASSWORD="${AIWATCH_NOTARIZE_PASSWORD:-}"

NOTARIZE_ARGS=()
if [ -n "$NOTARIZE_PROFILE" ]; then
    NOTARIZE_ARGS=(--keychain-profile "$NOTARIZE_PROFILE")
elif [ -n "$NOTARIZE_APPLE_ID" ] && [ -n "$NOTARIZE_TEAM_ID" ] && [ -n "$NOTARIZE_PASSWORD" ]; then
    NOTARIZE_ARGS=(
        --apple-id "$NOTARIZE_APPLE_ID"
        --team-id "$NOTARIZE_TEAM_ID"
        --password "$NOTARIZE_PASSWORD"
    )
elif [ -n "$NOTARIZE_APPLE_ID$NOTARIZE_TEAM_ID$NOTARIZE_PASSWORD" ]; then
    echo "Error: notarization via Apple ID requires all of AIWATCH_NOTARIZE_APPLE_ID," >&2
    echo "       AIWATCH_NOTARIZE_TEAM_ID, and AIWATCH_NOTARIZE_PASSWORD." >&2
    exit 1
fi

if [ "$SIGNING_ENABLED" = true ] && [ ${#NOTARIZE_ARGS[@]} -gt 0 ]; then
    echo "  Submitting to Apple notary service (this can take 1–10 min)..."
    # `--wait` blocks until Apple returns Accepted/Invalid; otherwise we'd
    # have to poll with `notarytool info <id>` and couldn't staple in-line.
    xcrun notarytool submit "$OUT" "${NOTARIZE_ARGS[@]}" --wait
    echo "  Stapling notary ticket..."
    xcrun stapler staple "$OUT"
    xcrun stapler validate "$OUT"
elif [ "$SIGNING_ENABLED" = true ]; then
    echo "  Skipping notarization (no AIWATCH_NOTARIZE_PROFILE / _APPLE_ID set)."
fi

echo "Built: $OUT"
