#!/bin/bash
set -euo pipefail

# Cross-compiles the Rust parser (ffi/c) and assembles it into
# ios/DiscordMarkdownC.xcframework, which the podspec vendors so CocoaPods links it into the
# consuming app. Runs from the example app's Podfile when building inside the
# discord/markdown repo; npm consumers receive the xcframework prebuilt, and this script only
# checks that it exists.
#
# Set PLATFORM_NAME=iphoneos or =iphonesimulator to build a single platform (e.g. in CI);
# by default both are built, which requires all three Rust iOS targets:
#   rustup target add aarch64-apple-ios aarch64-apple-ios-sim x86_64-apple-ios

# -P resolves symlinks (e.g. the pnpm workspace link in the example app), so the in-repo
# Rust workspace is detected from the script's real location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd -P)"
PREBUILT_DIR="$SCRIPT_DIR/prebuilt"
XCFRAMEWORK="$SCRIPT_DIR/DiscordMarkdownC.xcframework"
LIB=libdiscord_markdown_c.a

case "${PLATFORM_NAME:-}" in
iphoneos | iphonesimulator)
	PLATFORMS=("$PLATFORM_NAME")
	;;
"")
	PLATFORMS=(iphoneos iphonesimulator)
	;;
*)
	echo "error: unsupported platform '$PLATFORM_NAME'" >&2
	exit 1
	;;
esac

if [[ ! -f "$REPO_ROOT/ffi/c/Cargo.toml" ]]; then
	# Not building inside the repo; the prebuilt xcframework must already exist.
	if [[ ! -d "$XCFRAMEWORK" ]]; then
		echo "error: no Rust workspace found and ios/DiscordMarkdownC.xcframework is missing; this package was published without its prebuilt libraries" >&2
		exit 1
	fi
	exit 0
fi

# Xcode's environment breaks cargo: SDKROOT/IPHONEOS_DEPLOYMENT_TARGET leak into host builds
# of proc macros and build scripts, and PATH may not include cargo.
unset SDKROOT IPHONEOS_DEPLOYMENT_TARGET
export PATH="$HOME/.cargo/bin:$PATH"

build() {
	local platform="$1"
	shift
	local built=()
	for target in "$@"; do
		cargo build --manifest-path "$REPO_ROOT/Cargo.toml" -p discord-markdown-c --release --target "$target"
		built+=("$REPO_ROOT/target/$target/release/$LIB")
	done
	mkdir -p "$PREBUILT_DIR/$platform"
	if [[ ${#built[@]} -eq 1 ]]; then
		cp "${built[0]}" "$PREBUILT_DIR/$platform/$LIB"
	else
		lipo -create "${built[@]}" -output "$PREBUILT_DIR/$platform/$LIB"
	fi
}

XCFRAMEWORK_ARGS=()
for platform in "${PLATFORMS[@]}"; do
	case "$platform" in
	iphoneos)
		build iphoneos aarch64-apple-ios
		;;
	iphonesimulator)
		build iphonesimulator aarch64-apple-ios-sim x86_64-apple-ios
		;;
	esac
	XCFRAMEWORK_ARGS+=(-library "$PREBUILT_DIR/$platform/$LIB")
done

rm -rf "$XCFRAMEWORK"
xcodebuild -create-xcframework "${XCFRAMEWORK_ARGS[@]}" -output "$XCFRAMEWORK"
