#!/bin/bash
# Build a macOS .pkg installer for the full Runlayer CLI.
#
# Unlike build_pkg.sh (AI Watch), this ships the binary + a PATH symlink + one
# root hourly update LaunchDaemon + one per-user scheduler LaunchAgent
# (`runlayer schedule`; pre-approved on managed fleets via the login-items
# payload in com.runlayer.cli.mobileconfig). MDM (Jamf / Kandji / Intune)
# deploys the notarized .pkg silently.
#
# Signing / notarization env-var matrix (all optional; absent => ad-hoc):
#   INCLUDE_DESKTOP                 1 bundles Runlayer.app (default: 0)
#   RUNLAYER_PKG_ARCH               arm64 | x86_64 (default: uname -m)
#   RUNLAYER_SIGN_IDENTITY_APP      Developer ID Application identity
#   RUNLAYER_SIGN_IDENTITY_PKG      Developer ID Installer identity
#   RUNLAYER_NOTARIZE_PROFILE       notarytool keychain profile, OR
#   RUNLAYER_NOTARIZE_APPLE_ID + _TEAM_ID + _PASSWORD

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPO_ROOT="$(cd "$CLI_DIR/.." && pwd)"
BUILD_DIR="$CLI_DIR/build/pkg-runlayer"
DIST_DIR="$CLI_DIR/dist"
ENTITLEMENTS="$SCRIPT_DIR/entitlements.plist"
DESKTOP_APP="$REPO_ROOT/desktop/macos/build/Runlayer.app"

INCLUDE_DESKTOP="${INCLUDE_DESKTOP:-0}"
case "$INCLUDE_DESKTOP" in
    0)
        PACKAGE_NAME="Runlayer CLI"
        PACKAGE_ID="com.runlayer.cli"
        PACKAGE_SLUG="cli"
        ARTIFACT_PREFIX="runlayer"
        ;;
    1)
        PACKAGE_NAME="Runlayer"
        PACKAGE_ID="com.runlayer.desktop"
        PACKAGE_SLUG="desktop"
        ARTIFACT_PREFIX="runlayer-desktop"
        ;;
    *)
        echo "Error: INCLUDE_DESKTOP must be 0 or 1." >&2
        exit 1
        ;;
esac

VERSION=$(grep -E '^version = ' "$CLI_DIR/pyproject.toml" | head -1 | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Failed to read version from pyproject.toml" >&2
    exit 1
fi

ARCH="${RUNLAYER_PKG_ARCH:-$(uname -m)}"
case "$ARCH" in
    arm64|x86_64) ;;
    *) echo "Unsupported arch: $ARCH (expected arm64 or x86_64)" >&2; exit 1 ;;
esac

if [ ! -d "$DIST_DIR/runlayer" ] || [ ! -x "$DIST_DIR/runlayer/runlayer" ]; then
    echo "Error: dist/runlayer/runlayer not found. Run pyinstaller first." >&2
    exit 1
fi
if [ "$INCLUDE_DESKTOP" = 1 ] \
    && { [ ! -d "$DESKTOP_APP" ] || [ ! -x "$DESKTOP_APP/Contents/MacOS/Runlayer" ]; }; then
    echo "Error: desktop/macos/build/Runlayer.app not found. Run desktop/macos/build-app.sh first." >&2
    exit 1
fi

# Refuse to package a binary that doesn't match the requested arch.
BIN_ARCHS=$(lipo -archs "$DIST_DIR/runlayer/runlayer" 2>/dev/null || file -b "$DIST_DIR/runlayer/runlayer")
if ! echo "$BIN_ARCHS" | grep -qw "$ARCH"; then
    echo "Error: dist/runlayer/runlayer arch ($BIN_ARCHS) does not include $ARCH" >&2
    exit 1
fi
if [ "$INCLUDE_DESKTOP" = 1 ]; then
    APP_ARCHS=$(lipo -archs "$DESKTOP_APP/Contents/MacOS/Runlayer" 2>/dev/null || file -b "$DESKTOP_APP/Contents/MacOS/Runlayer")
    if ! echo "$APP_ARCHS" | grep -qw "$ARCH"; then
        echo "Error: Runlayer.app arch ($APP_ARCHS) does not include $ARCH" >&2
        exit 1
    fi
fi

SIGN_APP="${RUNLAYER_SIGN_IDENTITY_APP:-}"
SIGN_PKG="${RUNLAYER_SIGN_IDENTITY_PKG:-}"
SIGNING_ENABLED=false
if [ -n "$SIGN_APP" ] && [ -n "$SIGN_PKG" ]; then
    SIGNING_ENABLED=true
elif [ -n "$SIGN_APP" ] || [ -n "$SIGN_PKG" ]; then
    echo "Error: signing requires both RUNLAYER_SIGN_IDENTITY_APP and RUNLAYER_SIGN_IDENTITY_PKG." >&2
    echo "       App identity: ${SIGN_APP:-<unset>}" >&2
    echo "       Pkg identity: ${SIGN_PKG:-<unset>}" >&2
    exit 1
fi

echo "Building ${PACKAGE_NAME} .pkg v${VERSION} (${ARCH})..."
if [ "$SIGNING_ENABLED" = true ]; then
    echo "  Signing: enabled (app=${SIGN_APP}, pkg=${SIGN_PKG})"
else
    echo "  Signing: DISABLED (ad-hoc). Gatekeeper will block double-click installs."
    echo "  Set RUNLAYER_SIGN_IDENTITY_APP / _PKG to produce a fleet-ready pkg."
fi

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/payload/usr/local/lib/runlayer"
mkdir -p "$BUILD_DIR/payload/usr/local/bin"
mkdir -p "$BUILD_DIR/payload/Library/LaunchDaemons"
mkdir -p "$BUILD_DIR/payload/Library/LaunchAgents"
mkdir -p "$BUILD_DIR/scripts"

# ditto (not cp -R) keeps AppleDouble `._*` sidecars out of the payload.
ditto --noextattr --noqtn "$DIST_DIR/runlayer" "$BUILD_DIR/payload/usr/local/lib/runlayer/runlayer"
printf '%s\n' "$PACKAGE_SLUG" > "$BUILD_DIR/payload/usr/local/lib/runlayer/product"
if [ "$INCLUDE_DESKTOP" = 1 ]; then
    mkdir -p "$BUILD_DIR/payload/Applications"
    ditto --noextattr --noqtn "$DESKTOP_APP" "$BUILD_DIR/payload/Applications/Runlayer.app"
fi

# Sign inner Mach-Os first so the top-level signature encloses them cleanly
# (`--deep` is deprecated for signing).
if [ "$SIGNING_ENABLED" = true ]; then
    echo "  Signing inner Mach-O files..."
    PAYLOAD_BUNDLE="$BUILD_DIR/payload/usr/local/lib/runlayer/runlayer"
    MAIN_BIN="$PAYLOAD_BUNDLE/runlayer"
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

    echo "  Signing runlayer binary with identifier=com.runlayer.cli..."
    codesign --force --options=runtime --timestamp \
        --entitlements "$ENTITLEMENTS" \
        --identifier com.runlayer.cli \
        --sign "$SIGN_APP" \
        "$MAIN_BIN"

    codesign --verify --deep --strict --verbose=2 "$MAIN_BIN"

    if [ "$INCLUDE_DESKTOP" = 1 ]; then
        echo "  Signing Runlayer.app with identifier=com.runlayer.desktop..."
        codesign --force --options=runtime --timestamp \
            --identifier com.runlayer.desktop \
            --sign "$SIGN_APP" \
            "$BUILD_DIR/payload/Applications/Runlayer.app"
        codesign --verify --deep --strict --verbose=2 \
            "$BUILD_DIR/payload/Applications/Runlayer.app"
    fi
elif [ "$INCLUDE_DESKTOP" = 1 ]; then
    codesign --force --sign - --identifier com.runlayer.desktop \
        "$BUILD_DIR/payload/Applications/Runlayer.app"
fi

ln -s "../lib/runlayer/runlayer/runlayer" "$BUILD_DIR/payload/usr/local/bin/runlayer"
cp "$SCRIPT_DIR/com.runlayer.cli.update.plist" \
    "$BUILD_DIR/payload/Library/LaunchDaemons/com.runlayer.cli.update.plist"
cp "$SCRIPT_DIR/com.runlayer.cli.schedule.plist" \
    "$BUILD_DIR/payload/Library/LaunchAgents/com.runlayer.cli.schedule.plist"

cp "$SCRIPT_DIR/scripts/preinstall-runlayer" "$BUILD_DIR/scripts/preinstall"
chmod +x "$BUILD_DIR/scripts/preinstall"
cp "$SCRIPT_DIR/scripts/postinstall-runlayer" "$BUILD_DIR/scripts/postinstall"
chmod +x "$BUILD_DIR/scripts/postinstall"

sed \
    -e "s|__VERSION__|${VERSION}|g" \
    -e "s|__ARCH__|${ARCH}|g" \
    -e "s|__PACKAGE_ID__|${PACKAGE_ID}|g" \
    -e "s|__PACKAGE_NAME__|${PACKAGE_NAME}|g" \
    "$SCRIPT_DIR/distribution.runlayer.xml" \
    > "$BUILD_DIR/distribution.xml"

pkgbuild \
    --root "$BUILD_DIR/payload" \
    --identifier "$PACKAGE_ID" \
    --version "$VERSION" \
    --install-location / \
    --scripts "$BUILD_DIR/scripts" \
    "$BUILD_DIR/runlayer-component.pkg"

OUT="$DIST_DIR/${ARTIFACT_PREFIX}-${VERSION}-macos-${ARCH}.pkg"

# --timestamp is required for notarization to accept the .pkg.
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

# Signed-but-not-notarized .pkgs install via MDM but block on double-click.
NOTARIZE_PROFILE="${RUNLAYER_NOTARIZE_PROFILE:-}"
NOTARIZE_APPLE_ID="${RUNLAYER_NOTARIZE_APPLE_ID:-}"
NOTARIZE_TEAM_ID="${RUNLAYER_NOTARIZE_TEAM_ID:-}"
NOTARIZE_PASSWORD="${RUNLAYER_NOTARIZE_PASSWORD:-}"

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
    echo "Error: notarization via Apple ID requires all of RUNLAYER_NOTARIZE_APPLE_ID," >&2
    echo "       RUNLAYER_NOTARIZE_TEAM_ID, and RUNLAYER_NOTARIZE_PASSWORD." >&2
    exit 1
fi

if [ "$SIGNING_ENABLED" = true ] && [ ${#NOTARIZE_ARGS[@]} -gt 0 ]; then
    echo "  Submitting to Apple notary service (this can take 1–10 min)..."
    xcrun notarytool submit "$OUT" "${NOTARIZE_ARGS[@]}" --wait
    echo "  Stapling notary ticket..."
    xcrun stapler staple "$OUT"
    xcrun stapler validate "$OUT"
elif [ "$SIGNING_ENABLED" = true ]; then
    echo "  Skipping notarization (no RUNLAYER_NOTARIZE_PROFILE / _APPLE_ID set)."
fi

echo "Built: $OUT"
