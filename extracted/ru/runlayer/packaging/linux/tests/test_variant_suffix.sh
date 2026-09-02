#!/bin/bash
# Filename-contract test for VARIANT_SUFFIX in build_packages.sh +
# build_aiwatch_packages.sh (ENG-4579 legacy glibc variant).
#
# Runs the REAL packaging scripts against a staged fake cli/ tree (stub
# binaries, real nfpm configs) three times per product — default,
# VARIANT_SUFFIX=glibc2.17, then default again — and asserts:
#   1. the default run produces the exact historical filenames (regression
#      guard: empty suffix must stay byte-identical in naming) and ships NO
#      variant marker,
#   2. the suffixed run produces exactly the default names with the variant
#      tag inserted ("-<v>" before .tar.gz, ".<v>" before .deb/.rpm,
#      "SHA256SUMS-<v>"), with the checksum manifest listing only its own
#      variant's files, and ships the variant marker
#      (/usr/lib/runlayer/variant for the CLI, /usr/lib/runlayer/aiwatch/
#      variant for aiwatch; content glibc2.17) — self-updater variant
#      pinning,
#   3. a default run AFTER a variant run in the same dist/ ships NO marker —
#      sequential builds share dist/, a stale marker must not leak,
#   4. a non-glibc-shaped VARIANT_SUFFIX is rejected, and
#   5. (docker only) the package NAME inside every deb/rpm is identical
#      across variants for both products — the cross-variant upgrade
#      contract — and every deb/rpm's marker presence + content matches its
#      variant (dpkg-deb / rpm2cpio inside debian:12 / rockylinux:9).
# Marker checks on the tarball run host-side (tar); deb/rpm payload checks
# need dpkg-deb/rpm2cpio, so they live in the docker section.
#
# Usage: test_variant_suffix.sh          (needs sha256sum; docker optional)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SUFFIX="glibc2.17"
VERSION="9.9.9"

fail() { echo "FAIL: $*" >&2; exit 1; }

. "$SCRIPT_DIR/ensure_host_nfpm.sh"
ensure_host_nfpm "$CLI_DIR/build/tools"

# Staged fake cli/ tree: the scripts derive CLI_DIR from their own location,
# so a packaging/ symlink makes them treat the stage as cli/ (build_stub_
# packages.sh idiom) — real scripts, real nfpm configs, stub binaries.
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
ln -s "$CLI_DIR/packaging" "$STAGE/packaging"
printf 'version = "%s"\n' "$VERSION" > "$STAGE/pyproject.toml"
for bundle in runlayer aiwatch; do
    mkdir -p "$STAGE/dist/$bundle"
    printf '#!/bin/sh\nexit 0\n' > "$STAGE/dist/$bundle/$bundle"
    chmod 755 "$STAGE/dist/$bundle/$bundle"
done
# Packages staged for the docker package-name + marker checks, named
# <expected-package-name>__<label>.<ext>; label "variant" expects the marker,
# anything else expects none.
mkdir -p "$STAGE/namecheck"

assert_dist() { # <sums-file> <expected artifact file...>
    local sums="$1"; shift
    for f in "$sums" "$@"; do
        [ -f "$STAGE/dist/$f" ] || fail "expected $f in dist/, have: $(ls "$STAGE/dist")"
    done
    local listed expected
    listed=$(awk '{print $2}' "$STAGE/dist/$sums" | sort)
    expected=$(printf '%s\n' "$@" | sort)
    [ "$listed" = "$expected" ] || fail "$sums lists [$listed], expected [$expected]"
    (cd "$STAGE/dist" && sha256sum --quiet -c "$sums") || fail "$sums verification failed"
}

reset_dist() {
    # Top-level artifacts only — dist/<bundle>/ (incl. any marker) persists
    # across runs on purpose, mirroring sequential local builds.
    find "$STAGE/dist" -maxdepth 1 -type f -delete
}

assert_tar_marker() { # <tarball> <path-in-tar>
    local content
    content=$(tar -xzOf "$STAGE/dist/$1" "$2") \
        || fail "$1 missing marker $2"
    [ "$content" = "$SUFFIX" ] || fail "$1 marker content '$content' != '$SUFFIX'"
}

assert_tar_no_marker() { # <tarball>
    local listing
    listing=$(tar -tzf "$STAGE/dist/$1")
    if printf '%s\n' "$listing" | grep -Eq '(^|/)variant$'; then
        fail "$1 must not ship a variant marker"
    fi
}

run_case() { # <runlayer|aiwatch> <label> [suffix] — build + assert one run
    local bundle="$1" label="$2" suffix="${3:-}"
    local script pkg
    case "$bundle" in
        runlayer) script=build_packages.sh; pkg=runlayer ;;
        aiwatch) script=build_aiwatch_packages.sh; pkg=runlayer-aiwatch ;;
    esac
    reset_dist
    VARIANT_SUFFIX=$suffix "$STAGE/packaging/linux/$script"
    local tarball="${bundle}-${VERSION}-linux-x86_64${suffix:+-$suffix}.tar.gz"
    local deb="${pkg}_${VERSION}_amd64${suffix:+.$suffix}.deb"
    local rpm="${pkg}-${VERSION}-1.x86_64${suffix:+.$suffix}.rpm"
    assert_dist "SHA256SUMS${suffix:+-$suffix}" "$tarball" "$deb" "$rpm"
    if [ -n "$suffix" ]; then
        assert_tar_marker "$tarball" "$bundle/variant"
    else
        assert_tar_no_marker "$tarball"
    fi
    cp "$STAGE/dist/$deb" "$STAGE/namecheck/${pkg}__${label}.deb"
    cp "$STAGE/dist/$rpm" "$STAGE/namecheck/${pkg}__${label}.rpm"
}

for bundle in runlayer aiwatch; do
    echo "=== $bundle: default filenames ==="
    run_case "$bundle" default
    echo "=== $bundle: ${SUFFIX} variant filenames + marker ==="
    run_case "$bundle" variant "$SUFFIX"
    echo "=== $bundle: default after variant leaves no stale marker ==="
    run_case "$bundle" postvariant
done

echo "=== non-glibc-shaped VARIANT_SUFFIX is rejected ==="
reset_dist
if VARIANT_SUFFIX=el7 "$STAGE/packaging/linux/build_packages.sh" 2>/dev/null; then
    fail "VARIANT_SUFFIX=el7 should have been rejected"
fi

# Cross-variant upgrade contract: the variant tag lives in the FILENAME only;
# the package name inside deb/rpm metadata must not change. One docker run per
# package manager checks every staged <expected-name>__<label> package.
if command -v docker >/dev/null; then
    echo "=== package-name invariance across variants (docker) ==="
    check_names() { # <image> <query command for $f>
        docker run --rm --platform linux/amd64 -v "$STAGE/namecheck:/nc:ro" "$1" \
            bash -c 'for f in /nc/*.'"$3"'; do echo "$(basename "$f")|'"$2"'"; done' |
        while IFS='|' read -r file actual; do
            expected="${file%%__*}"
            [ "$actual" = "$expected" ] || fail "$file: package name '$actual' != '$expected'"
        done
    }
    check_names debian:12 '$(dpkg-deb -f "$f" Package)' deb
    check_names rockylinux:9 '$(rpm -qp --qf "%{NAME}" "$f" 2>/dev/null)' rpm

    echo "=== marker presence + content inside deb/rpm payloads (docker) ==="
    check_markers() { # <image> <ext>
        docker run --rm --platform linux/amd64 \
            -v "$STAGE/namecheck:/nc:ro" -v "$SCRIPT_DIR:/tests:ro" "$1" \
            bash /tests/check_package_markers.sh "$2" "$SUFFIX" \
            || fail "marker payload check failed for $2 packages"
    }
    check_markers debian:12 deb
    check_markers rockylinux:9 rpm
else
    echo "NOTE: docker not available — skipped package-name invariance and deb/rpm marker payload checks."
fi

echo "PASS: variant-suffix filename + marker contract holds for both products."
