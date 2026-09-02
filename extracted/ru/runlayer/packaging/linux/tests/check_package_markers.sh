#!/bin/bash
# Runs INSIDE debian:12 (deb) or rockylinux:9 (rpm) for test_variant_suffix.sh.
# Checks every /nc/<expected-package-name>__<label>.<ext> package's payload:
# label "variant" must ship the variant marker (/usr/lib/runlayer/variant for
# runlayer, /usr/lib/runlayer/aiwatch/variant for runlayer-aiwatch) with the
# exact expected content; any other label must ship no variant path at all.
#
# Usage: check_package_markers.sh <deb|rpm> <expected-marker-content>

set -euo pipefail

EXT="$1"
EXPECTED="$2"

# rockylinux:9 base image lacks cpio (needed to read the rpm payload).
if [ "$EXT" = "rpm" ] && ! command -v cpio >/dev/null; then
    dnf -yq install cpio >/dev/null
fi

list_paths() { # <pkg> — payload paths, format-native prefixes
    case "$EXT" in
        deb) dpkg-deb -c "$1" | awk '{print $6}' ;;
        rpm) rpm -qpl "$1" ;;
    esac
}

read_file() { # <pkg> <path without leading slash>
    case "$EXT" in
        deb) dpkg-deb --fsys-tarfile "$1" | tar -xO "./$2" ;;
        # Leading glob: nfpm rpm payload names carry no ./ prefix.
        rpm) rpm2cpio "$1" | cpio -i --to-stdout --quiet "*$2" ;;
    esac
}

# Empty glob must fail loudly, not pass vacuously or hit the tools with a
# literal "/nc/*.deb".
shopt -s nullglob
packages=(/nc/*."$EXT")
if [ ${#packages[@]} -eq 0 ]; then
    echo "FAIL: no .$EXT packages staged in /nc" >&2
    exit 1
fi

for f in "${packages[@]}"; do
    base=$(basename "$f")
    name="${base%%__*}"
    label="${base##*__}"
    label="${label%.*}"
    marker="usr/lib/runlayer/variant"
    [ "$name" = "runlayer-aiwatch" ] && marker="usr/lib/runlayer/aiwatch/variant"
    variant_paths=$(list_paths "$f" | grep -E '(^|/)variant$' || true)
    if [ "$label" = "variant" ]; then
        # Exactly the expected marker and no other variant-named path — a
        # second/mispathed marker would let the reader resolve the wrong file.
        [ "$(printf '%s\n' "$variant_paths" | grep -c .)" -eq 1 ] \
            || { echo "FAIL: $base wants exactly one variant path, got: ${variant_paths:-none}" >&2; exit 1; }
        printf '%s\n' "$variant_paths" | grep -Eq "^\.?/$marker\$" \
            || { echo "FAIL: $base marker at '$variant_paths', want /$marker" >&2; exit 1; }
        content=$(read_file "$f" "$marker")
        [ "$content" = "$EXPECTED" ] \
            || { echo "FAIL: $base marker content '$content' != '$EXPECTED'" >&2; exit 1; }
    elif [ -n "$variant_paths" ]; then
        echo "FAIL: $base must not ship a variant marker" >&2
        exit 1
    fi
done
echo "ok: $EXT marker payload checks passed"
