#!/bin/bash
# Build the disposable, payload-free macOS AI Watch uninstall package.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$CLI_DIR/build/aiwatch-uninstall-pkg"
DIST_DIR="$CLI_DIR/dist"
SOURCE_BUNDLE="$DIST_DIR/aiwatch-uninstall"
SOURCE_MAIN="$SOURCE_BUNDLE/aiwatch-uninstall"
PACKAGE_ID="com.runlayer.aiwatch.uninstall"

VERSION=$(grep -E '^version = ' "$CLI_DIR/pyproject.toml" | head -1 | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Failed to read version from pyproject.toml" >&2
    exit 1
fi

if [ ! -x "$SOURCE_MAIN" ]; then
    echo "Error: dist/aiwatch-uninstall/aiwatch-uninstall not found or not executable." >&2
    echo "Run pyinstaller packaging/aiwatch_uninstall.spec first." >&2
    exit 1
fi

ARCH="${AIWATCH_PKG_ARCH:-$(uname -m)}"
case "$ARCH" in
    arm64|x86_64) ;;
    *)
        echo "Unsupported arch: $ARCH (expected arm64 or x86_64)" >&2
        exit 1
        ;;
esac

MAIN_ARCHS=$(lipo -archs "$SOURCE_MAIN" 2>/dev/null || file -b "$SOURCE_MAIN")
if ! printf '%s\n' "$MAIN_ARCHS" | grep -qw "$ARCH"; then
    echo "Error: aiwatch-uninstall arch ($MAIN_ARCHS) does not include $ARCH" >&2
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

echo "Building AI Watch uninstall .pkg v${VERSION} (${ARCH})..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/scripts"

# pkgbuild archives the whole scripts directory. The frozen onedir therefore
# exists only in the installer's temporary scripts area and leaves no payload.
STAGED_BUNDLE="$BUILD_DIR/scripts/aiwatch-uninstall"
ditto --noextattr --noqtn "$SOURCE_BUNDLE" "$STAGED_BUNDLE"
STAGED_MAIN="$STAGED_BUNDLE/aiwatch-uninstall"
chmod 755 "$STAGED_MAIN"

cp "$SCRIPT_DIR/uninstall-pkg/postinstall" "$BUILD_DIR/scripts/postinstall"
chmod 755 "$BUILD_DIR/scripts/postinstall"

if [ "$SIGNING_ENABLED" = true ]; then
    echo "  Signing inner Mach-O files..."
    SIGN_COUNT=0
    while IFS= read -r -d '' file_path; do
        if [ "$file_path" = "$STAGED_MAIN" ]; then
            continue
        fi
        if ! file -b "$file_path" 2>/dev/null | grep -q 'Mach-O'; then
            continue
        fi
        codesign --force --options=runtime --timestamp \
            --sign "$SIGN_APP" "$file_path" >/dev/null
        SIGN_COUNT=$((SIGN_COUNT + 1))
    done < <(find "$STAGED_BUNDLE" -type f -print0)
    echo "    Signed $SIGN_COUNT inner Mach-O files."

    echo "  Signing aiwatch-uninstall with identifier=${PACKAGE_ID}..."
    codesign --force --options=runtime --timestamp \
        --identifier "$PACKAGE_ID" \
        --entitlements "$SCRIPT_DIR/entitlements.plist" \
        --sign "$SIGN_APP" \
        "$STAGED_MAIN"
    codesign --verify --deep --strict --verbose=2 "$STAGED_MAIN"
else
    echo "  Signing: DISABLED."
    echo "  Set AIWATCH_SIGN_IDENTITY_APP / _PKG for a fleet-ready package."
fi

xattr -cr "$BUILD_DIR/scripts" 2>/dev/null || true
export COPYFILE_DISABLE=1

OUT="$DIST_DIR/aiwatch-uninstall-${VERSION}.pkg"
rm -f "$OUT"
if [ "$SIGNING_ENABLED" = true ]; then
    pkgbuild \
        --nopayload \
        --identifier "$PACKAGE_ID" \
        --version "$VERSION" \
        --scripts "$BUILD_DIR/scripts" \
        --sign "$SIGN_PKG" \
        --timestamp \
        "$OUT"
else
    pkgbuild \
        --nopayload \
        --identifier "$PACKAGE_ID" \
        --version "$VERSION" \
        --scripts "$BUILD_DIR/scripts" \
        "$OUT"
fi

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
