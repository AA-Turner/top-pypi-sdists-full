#!/bin/bash
# Build STUB runlayer-aiwatch .deb/.rpm for the container smoke tests.
#
# The real aiwatch Linux binary is PyInstaller-built and cannot be produced on
# macOS (PyInstaller is not cross-platform). This helper fakes only the binary:
# a POSIX-sh stub stands in for dist/aiwatch/aiwatch, then the REAL
# nfpm-aiwatch.yaml packages it unmodified — so install layout, perms, cron
# registration, deps, and config|noreplace semantics are all the production
# metadata. What stubs canNOT cover: the glibc floor / real-binary execution
# (CI feeds real artifacts into run_smoke_tests.sh --deb/--rpm for that).
#
# Usage: build_stub_packages.sh <out-dir>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
TOOLS_DIR="$CLI_DIR/build/tools"
OUT_DIR="${1:?usage: build_stub_packages.sh <out-dir>}"
mkdir -p "$OUT_DIR"

VERSION=$(grep -E '^version = ' "$CLI_DIR/pyproject.toml" | head -1 | cut -d'"' -f2)
export VERSION

# nfpm for the HOST platform (build_packages.sh only handles Linux CI hosts).
. "$SCRIPT_DIR/ensure_host_nfpm.sh"
ensure_host_nfpm "$TOOLS_DIR"
NFPM_BIN="$(command -v nfpm)"

# Staging dir: stub dist/ + symlinked packaging/ so nfpm-aiwatch.yaml's
# relative src paths resolve exactly as in the real build (cwd = cli/).
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/dist/aiwatch"
ln -s "$CLI_DIR/packaging" "$STAGE/packaging"

# Generated version record consumed by nfpm-aiwatch.yaml (produced in the real
# build by build_aiwatch_packages.sh). Mirror it here so the stub packages carry
# the same /etc/runlayer/aiwatch/version.json layout the smoke test asserts.
mkdir -p "$STAGE/build"
printf '{"Version":"%s"}\n' "$VERSION" > "$STAGE/build/aiwatch-version.json"

cat >"$STAGE/dist/aiwatch/aiwatch" <<'EOF'
#!/bin/sh
# Stub aiwatch for package smoke tests — NOT the real scanner. Mirrors just
# enough CLI surface for the assertions in assert_inside_container.sh.
set -u
case "${1:-}" in
--version)
    echo "aiwatch ${STUB_VERSION:-0.0.0-stub} (smoke-test stub)"
    ;;
scan)
    username=unknown
    while [ $# -gt 0 ]; do
        if [ "$1" = "--username" ] && [ $# -gt 1 ]; then username=$2; fi
        shift
    done
    # Unwritable $HOME exits 0 quietly: system accounts with root-owned homes
    # (e.g. /usr/sbin) must not fail the wrapper's aggregate exit code.
    mkdir -p "$HOME/.runlayer/logs" 2>/dev/null || exit 0
    echo "stub scan user=$username" >"$HOME/.runlayer/logs/stub-scan-marker"
    ;;
self-update)
    [ "${RUNLAYER_API_KEY:-}" = stub ] || exit 3
    : >/tmp/aiwatch-update-marker
    ;;
*)
    echo "stub aiwatch: unsupported args: $*" >&2
    exit 2
    ;;
esac
exit 0
EOF
chmod 755 "$STAGE/dist/aiwatch/aiwatch"

# Bake the packaged version into the stub's --version so the version.json ==
# `aiwatch --version` assertion in assert_inside_container.sh holds (real builds
# match by construction; the stub otherwise reports 0.0.0-stub). sed -i.bak form
# is portable across BSD (macOS host) and GNU sed.
sed -i.bak "s/0.0.0-stub/${VERSION}/" "$STAGE/dist/aiwatch/aiwatch"
rm -f "$STAGE/dist/aiwatch/aiwatch.bak"

(
    cd "$STAGE"
    "$NFPM_BIN" pkg --config "$SCRIPT_DIR/../nfpm-aiwatch.yaml" --packager deb --target "$OUT_DIR/"
    "$NFPM_BIN" pkg --config "$SCRIPT_DIR/../nfpm-aiwatch.yaml" --packager rpm --target "$OUT_DIR/"
)

echo "Stub packages in $OUT_DIR:"
ls -1 "$OUT_DIR"
