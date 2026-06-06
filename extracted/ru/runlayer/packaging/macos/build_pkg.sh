#!/bin/bash
# Build a macOS .pkg installer for AI Watch. See packaging/README.md for the
# full layout + signing + notarization env-var matrix.

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

ARCH="${AIWATCH_PKG_ARCH:-$(uname -m)}"
case "$ARCH" in
    arm64|x86_64) ;;
    *) echo "Unsupported arch: $ARCH (expected arm64 or x86_64)" >&2; exit 1 ;;
esac

if [ ! -d "$DIST_DIR/aiwatch" ] || [ ! -x "$DIST_DIR/aiwatch/aiwatch" ]; then
    echo "Error: dist/aiwatch/aiwatch not found. Run pyinstaller first." >&2
    exit 1
fi

# Refuse to package a binary that doesn't match the requested arch.
BIN_ARCHS=$(lipo -archs "$DIST_DIR/aiwatch/aiwatch" 2>/dev/null || file -b "$DIST_DIR/aiwatch/aiwatch")
if ! echo "$BIN_ARCHS" | grep -qw "$ARCH"; then
    echo "Error: dist/aiwatch/aiwatch arch ($BIN_ARCHS) does not include $ARCH" >&2
    exit 1
fi

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
mkdir -p "$BUILD_DIR/payload/Library/LaunchDaemons"
mkdir -p "$BUILD_DIR/scripts"

# ditto (not cp -R) keeps AppleDouble `._*` sidecars out of the payload.
ditto --noextattr --noqtn "$DIST_DIR/aiwatch" "$BUILD_DIR/payload/usr/local/lib/runlayer/aiwatch"

# Sign inner Mach-Os first so the top-level signature encloses them cleanly
# (`--deep` is deprecated for signing).
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

    # Top-level last so codesign records valid inner hashes. Identifier must
    # match the PPPC profile pin (com.runlayer.aiwatch). Single binary => single
    # Designated Requirement, so there's no second exe to share keychain ACLs
    # with (the legacy aiwatch-hook same-identifier dual-sign is gone).
    echo "  Signing aiwatch binary with identifier=com.runlayer.aiwatch..."
    codesign --force --options=runtime --timestamp \
        --entitlements "$ENTITLEMENTS" \
        --identifier com.runlayer.aiwatch \
        --sign "$SIGN_APP" \
        "$MAIN_BIN"

    codesign --verify --deep --strict --verbose=2 "$MAIN_BIN"
fi

ln -s "../lib/runlayer/aiwatch/aiwatch" "$BUILD_DIR/payload/usr/local/bin/aiwatch"

cp "$SCRIPT_DIR/com.runlayer.aiwatch.plist" \
    "$BUILD_DIR/payload/Library/LaunchAgents/com.runlayer.aiwatch.plist"
cp "$SCRIPT_DIR/com.runlayer.aiwatch.enroll.plist" \
    "$BUILD_DIR/payload/Library/LaunchAgents/com.runlayer.aiwatch.enroll.plist"
cp "$SCRIPT_DIR/com.runlayer.aiwatch.bootstrap.plist" \
    "$BUILD_DIR/payload/Library/LaunchDaemons/com.runlayer.aiwatch.bootstrap.plist"

cp "$SCRIPT_DIR/scripts/postinstall" "$BUILD_DIR/scripts/postinstall"
chmod +x "$BUILD_DIR/scripts/postinstall"

sed -e "s|__VERSION__|${VERSION}|g" -e "s|__ARCH__|${ARCH}|g" \
    "$SCRIPT_DIR/distribution.xml" \
    > "$BUILD_DIR/distribution.xml"

# Installer-GUI background (interactive double-click only; ignored on silent MDM
# installs). distribution.xml <background> refs aiwatch-icon-512.png by name.
RESOURCES_DIR="$BUILD_DIR/resources"
mkdir -p "$RESOURCES_DIR"
cp "$SCRIPT_DIR/../assets/aiwatch-icon-512.png" "$RESOURCES_DIR/aiwatch-icon-512.png"

pkgbuild \
    --root "$BUILD_DIR/payload" \
    --identifier com.runlayer.aiwatch \
    --version "$VERSION" \
    --install-location / \
    --scripts "$BUILD_DIR/scripts" \
    "$BUILD_DIR/aiwatch-component.pkg"

OUT="$DIST_DIR/aiwatch-${VERSION}-macos-${ARCH}.pkg"

# --timestamp is required for notarization to accept the .pkg.
if [ "$SIGNING_ENABLED" = true ]; then
    productbuild \
        --distribution "$BUILD_DIR/distribution.xml" \
        --package-path "$BUILD_DIR" \
        --resources "$RESOURCES_DIR" \
        --sign "$SIGN_PKG" \
        --timestamp \
        "$OUT"
else
    productbuild \
        --distribution "$BUILD_DIR/distribution.xml" \
        --package-path "$BUILD_DIR" \
        --resources "$RESOURCES_DIR" \
        "$OUT"
fi

# Signed-but-not-notarized .pkgs install via MDM but block on double-click.
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
    xcrun notarytool submit "$OUT" "${NOTARIZE_ARGS[@]}" --wait
    echo "  Stapling notary ticket..."
    xcrun stapler staple "$OUT"
    xcrun stapler validate "$OUT"
elif [ "$SIGNING_ENABLED" = true ]; then
    echo "  Skipping notarization (no AIWATCH_NOTARIZE_PROFILE / _APPLE_ID set)."
fi

echo "Built: $OUT"
