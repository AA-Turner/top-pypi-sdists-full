#!/bin/bash
# Build a macOS .pkg installer for aiwatch-enforce (the hook binary).
#
# Usage:
#   cd cli
#   ./packaging/aiwatch-enforce-macos/build_pkg.sh
#
# Layout shipped by the .pkg (onedir):
#   /usr/local/lib/runlayer/aiwatch-enforce/         PyInstaller bundle
#     aiwatch-enforce                                (the real exe)
#     base_library.zip, lib*.dylib, ...
#   /usr/local/bin/aiwatch-enforce                   symlink → ../lib/runlayer/aiwatch-enforce/aiwatch-enforce
#
# No LaunchAgent — the hook is invoked on-demand by AI coding clients.
# No tenant config — credentials are in ~/.runlayer/config.yaml.
#
# Prerequisites: PyInstaller-built `dist/aiwatch-enforce/` directory must exist.
# Run `pyinstaller packaging/aiwatch-enforce.spec` first, or use
# `make package-enforce-macos` which does both steps.
#
# ---------- Signing + notarization (optional, required for MDM) ----------
#
# Same signing model as aiwatch. Required env vars (all or nothing):
#
#   ENFORCE_SIGN_IDENTITY_APP   "Developer ID Application: Company (TEAMID)"
#   ENFORCE_SIGN_IDENTITY_PKG   "Developer ID Installer: Company (TEAMID)"
#
# Falls back to AIWATCH_SIGN_IDENTITY_APP / _PKG if ENFORCE_ variants unset.
#
# Notarization (optional):
#   ENFORCE_NOTARIZE_PROFILE    Keychain profile via `xcrun notarytool store-credentials`
#     -- OR --
#   ENFORCE_NOTARIZE_APPLE_ID / _TEAM_ID / _PASSWORD
#
# Falls back to AIWATCH_NOTARIZE_* if ENFORCE_ variants unset.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$CLI_DIR/build/enforce-pkg"
DIST_DIR="$CLI_DIR/dist"
ENTITLEMENTS="$SCRIPT_DIR/../macos/entitlements.plist"

VERSION=$(grep -E '^version = ' "$CLI_DIR/pyproject.toml" | head -1 | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Failed to read version from pyproject.toml" >&2
    exit 1
fi

ARCH="${ENFORCE_PKG_ARCH:-$(uname -m)}"
case "$ARCH" in
    arm64|x86_64) ;;
    *) echo "Unsupported arch: $ARCH (expected arm64 or x86_64)" >&2; exit 1 ;;
esac

if [ ! -d "$DIST_DIR/aiwatch-enforce" ] || [ ! -x "$DIST_DIR/aiwatch-enforce/aiwatch-enforce" ]; then
    echo "Error: dist/aiwatch-enforce/aiwatch-enforce not found. Run pyinstaller first." >&2
    exit 1
fi

BIN_ARCHS=$(lipo -archs "$DIST_DIR/aiwatch-enforce/aiwatch-enforce" 2>/dev/null || file -b "$DIST_DIR/aiwatch-enforce/aiwatch-enforce")
if ! echo "$BIN_ARCHS" | grep -qw "$ARCH"; then
    echo "Error: dist/aiwatch-enforce/aiwatch-enforce arch ($BIN_ARCHS) does not include $ARCH" >&2
    exit 1
fi

# Signing — fall back to AIWATCH_ env vars if ENFORCE_ not set
SIGN_APP="${ENFORCE_SIGN_IDENTITY_APP:-${AIWATCH_SIGN_IDENTITY_APP:-}}"
SIGN_PKG="${ENFORCE_SIGN_IDENTITY_PKG:-${AIWATCH_SIGN_IDENTITY_PKG:-}}"
SIGNING_ENABLED=false
if [ -n "$SIGN_APP" ] && [ -n "$SIGN_PKG" ]; then
    SIGNING_ENABLED=true
elif [ -n "$SIGN_APP" ] || [ -n "$SIGN_PKG" ]; then
    echo "Error: signing requires both app and pkg identities." >&2
    exit 1
fi

echo "Building aiwatch-enforce .pkg v${VERSION} (${ARCH})..."
if [ "$SIGNING_ENABLED" = true ]; then
    echo "  Signing: enabled (app=${SIGN_APP}, pkg=${SIGN_PKG})"
else
    echo "  Signing: DISABLED (ad-hoc)."
fi

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/payload/usr/local/lib"
mkdir -p "$BUILD_DIR/payload/usr/local/bin"
mkdir -p "$BUILD_DIR/scripts"

ditto --noextattr --noqtn "$DIST_DIR/aiwatch-enforce" "$BUILD_DIR/payload/usr/local/lib/runlayer/aiwatch-enforce"

if [ "$SIGNING_ENABLED" = true ]; then
    echo "  Signing inner Mach-O files..."
    PAYLOAD_BUNDLE="$BUILD_DIR/payload/usr/local/lib/runlayer/aiwatch-enforce"
    MAIN_BIN="$PAYLOAD_BUNDLE/aiwatch-enforce"
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

    echo "  Signing main binary with identifier=com.runlayer.aiwatch-enforce..."
    codesign --force --options=runtime --timestamp \
        --entitlements "$ENTITLEMENTS" \
        --identifier com.runlayer.aiwatch-enforce \
        --sign "$SIGN_APP" \
        "$MAIN_BIN"

    codesign --verify --deep --strict --verbose=2 "$MAIN_BIN"
fi

ln -s "../lib/runlayer/aiwatch-enforce/aiwatch-enforce" "$BUILD_DIR/payload/usr/local/bin/aiwatch-enforce"

cp "$SCRIPT_DIR/scripts/postinstall" "$BUILD_DIR/scripts/postinstall"
chmod +x "$BUILD_DIR/scripts/postinstall"

sed -e "s|__VERSION__|${VERSION}|g" -e "s|__ARCH__|${ARCH}|g" \
    "$SCRIPT_DIR/distribution.xml" \
    > "$BUILD_DIR/distribution.xml"

pkgbuild \
    --root "$BUILD_DIR/payload" \
    --identifier com.runlayer.aiwatch-enforce \
    --version "$VERSION" \
    --install-location / \
    --scripts "$BUILD_DIR/scripts" \
    "$BUILD_DIR/aiwatch-enforce-component.pkg"

OUT="$DIST_DIR/aiwatch-enforce-${VERSION}-macos-${ARCH}.pkg"

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
NOTARIZE_PROFILE="${ENFORCE_NOTARIZE_PROFILE:-${AIWATCH_NOTARIZE_PROFILE:-}}"
NOTARIZE_APPLE_ID="${ENFORCE_NOTARIZE_APPLE_ID:-${AIWATCH_NOTARIZE_APPLE_ID:-}}"
NOTARIZE_TEAM_ID="${ENFORCE_NOTARIZE_TEAM_ID:-${AIWATCH_NOTARIZE_TEAM_ID:-}}"
NOTARIZE_PASSWORD="${ENFORCE_NOTARIZE_PASSWORD:-${AIWATCH_NOTARIZE_PASSWORD:-}}"

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
    echo "Error: notarization via Apple ID requires all three env vars." >&2
    exit 1
fi

if [ "$SIGNING_ENABLED" = true ] && [ ${#NOTARIZE_ARGS[@]} -gt 0 ]; then
    echo "  Submitting to Apple notary service..."
    xcrun notarytool submit "$OUT" "${NOTARIZE_ARGS[@]}" --wait
    echo "  Stapling notary ticket..."
    xcrun stapler staple "$OUT"
    xcrun stapler validate "$OUT"
elif [ "$SIGNING_ENABLED" = true ]; then
    echo "  Skipping notarization (no notary credentials set)."
fi

echo "Built: $OUT"
