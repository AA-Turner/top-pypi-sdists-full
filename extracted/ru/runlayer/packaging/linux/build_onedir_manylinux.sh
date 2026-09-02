#!/bin/bash
# Build a PyInstaller onedir bundle inside a manylinux container so the frozen
# binary inherits the container's old glibc floor instead of the build host's.
#
# PyInstaller does not bundle glibc: a frozen app needs the glibc of the build
# host (or newer) at runtime. Building inside quay.io/pypa/manylinux2014_x86_64
# (CentOS 7) pins the floor at glibc 2.17, covering RHEL/CentOS 7+, Amazon
# Linux 2, Ubuntu 14.04+, and Debian 8+. Used by the `build-linux-legacy`
# release jobs and for local legacy-variant builds; the standard `build-linux`
# release jobs do not route through this script.
#
# GitHub Actions note: run this from a HOST job via `docker run`. A
# `container:` job cannot host the build — the runner injects node20-based
# actions (checkout, upload-artifact) into the job container, and node20 needs
# glibc 2.28+, which manylinux2014 (2.17) cannot provide.
#
# Usage (any cwd; paths derive from the script location):
#   SPEC=packaging/aiwatch.spec  ./cli/packaging/linux/build_onedir_manylinux.sh
#   SPEC=packaging/runlayer.spec ./cli/packaging/linux/build_onedir_manylinux.sh
#
# Env:
#   SPEC             PyInstaller spec, relative to cli/
#                    (default packaging/aiwatch.spec)
#   MANYLINUX_IMAGE  build image (default quay.io/pypa/manylinux2014_x86_64,
#                    glibc 2.17; e.g. quay.io/pypa/manylinux_2_28_x86_64 for a
#                    2.28 floor if manylinux2014 is ever retired)
#
# Output: cli/dist/<bundle>/ on the host, owned by the invoking user.
#
# Local floor check after building (exec only; no yum needed):
#   docker run --rm --platform linux/amd64 \
#       -v "$PWD/cli/dist/aiwatch:/a:ro" centos:7 /a/aiwatch --version

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPO_ROOT="$(cd "$CLI_DIR/.." && pwd)"

SPEC="${SPEC:-packaging/aiwatch.spec}"
MANYLINUX_IMAGE="${MANYLINUX_IMAGE:-quay.io/pypa/manylinux2014_x86_64}"
# Pinned to match .tool-versions / the release workflows.
UV_VERSION="0.9.18"

if [ ! -f "$CLI_DIR/$SPEC" ]; then
    echo "Error: spec not found: $CLI_DIR/$SPEC" >&2
    exit 1
fi
BUNDLE="$(basename "$SPEC" .spec)"

echo "Building $BUNDLE onedir bundle in $MANYLINUX_IMAGE..."

# Mount the repo ROOT, not cli/: cli has an editable path dependency on
# ../packages/python, so both trees must be visible inside the container.
# The venv, uv cache, and PyInstaller workpath all live OUTSIDE the mount so
# the container build never clobbers the host cli/.venv and no root-owned
# intermediates land in the repo; dist/ is the only host-visible output and is
# chowned back to the invoking user.
docker run --rm \
    --platform linux/amd64 \
    -v "$REPO_ROOT:/src" \
    -w /src/cli \
    -e SPEC="$SPEC" \
    -e BUNDLE="$BUNDLE" \
    -e UV_VERSION="$UV_VERSION" \
    -e HOST_UID="$(id -u)" \
    -e HOST_GID="$(id -g)" \
    "$MANYLINUX_IMAGE" \
    bash -euo pipefail -c '
        # Restore host ownership even on failure — a partial root-owned dist/
        # on the host would break the next build or a plain rm -rf.
        trap "chown -R \"$HOST_UID:$HOST_GID\" dist 2>/dev/null || true" EXIT
        # Pinned uv installer — same idiom as packaging/container/Dockerfile.
        export UV_INSTALL_DIR=/usr/local/bin UV_UNMANAGED_INSTALL=1 UV_LINK_MODE=copy
        curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | sh
        export UV_PROJECT_ENVIRONMENT=/opt/venv UV_CACHE_DIR=/opt/uv-cache
        # google-re2 ships no manylinux2014 wheel (its Linux x86_64 wheels
        # floor at glibc 2.27), so uv builds it from the sdist here. That
        # sdist is only the pybind11 binding: it needs RE2 + abseil headers
        # and libs, which manylinux2014 does not carry. Build both from
        # pinned sources first. RE2_TAG must stay in step with the
        # google-re2 pin in pyproject.toml (its version IS the RE2 release
        # date), or the frozen binary ships a different engine than every
        # other platform.
        ABSL_TAG=20250127.1
        RE2_TAG=2025-11-05
        for pkg in "abseil-cpp:$ABSL_TAG:https://github.com/abseil/abseil-cpp" \
                   "re2:$RE2_TAG:https://github.com/google/re2"; do
            name="${pkg%%:*}"; rest="${pkg#*:}"; tag="${rest%%:*}"; url="${rest#*:}"
            curl -LsS -o "/tmp/$name.tgz" "$url/archive/refs/tags/$tag.tar.gz"
            tar xzf "/tmp/$name.tgz" -C /tmp
            # Shared, not static: setup.py links only -lre2, so a static RE2
            # leaves absl symbols unresolved at import. Shared libs pull
            # their deps in via DT_NEEDED, and PyInstaller bundles them by
            # following ldd on the extension.
            cmake -S "/tmp/$name-$tag" -B "/tmp/$name-build" \
                -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON \
                -DCMAKE_CXX_STANDARD=17 -DABSL_PROPAGATE_CXX_STD=ON \
                -DRE2_BUILD_TESTING=OFF >/dev/null
            cmake --build "/tmp/$name-build" -j"$(nproc)" >/dev/null
            cmake --install "/tmp/$name-build" >/dev/null
        done
        printf "/usr/local/lib\n/usr/local/lib64\n" > /etc/ld.so.conf.d/re2.conf
        ldconfig
        # The sdist is a pybind11 binding but declares no build-requires (it
        # is a legacy setup.py), so uv builds it in an isolated env that has
        # only setuptools — the pybind11 headers have to come in via the
        # include path. C++17 likewise: CFLAGS does not reach the compile
        # line (setuptools builds .cc through CC), so set the compiler.
        # Pinned and installed through uv: an unpinned install would make two
        # builds of the same CLI tag non-reproducible, and a future pybind11
        # release could break both legacy release jobs without a code change.
        PYBIND11_VERSION=3.0.4
        uv pip install --python /opt/python/cp313-cp313/bin/python \
            "pybind11==${PYBIND11_VERSION}"
        PYBIND_INC="$(/opt/python/cp313-cp313/bin/python -c "
import pybind11, sys
sys.stdout.write(pybind11.get_include())")"
        export CC="g++ -std=c++17 -I$PYBIND_INC"
        export CXX="g++ -std=c++17 -I$PYBIND_INC"
        export LDSHARED="g++ -shared"
        export LDFLAGS="-L/usr/local/lib -L/usr/local/lib64"
        uv sync --frozen --no-dev
        unset CC CXX LDSHARED LDFLAGS
        uv pip install --python /opt/venv/bin/python pyinstaller
        # Fail loudly here rather than shipping a bundle whose RE2 extension
        # cannot load at runtime.
        /opt/venv/bin/python -c "import re2; assert re2.compile(\"(?i)a+\").search(\"AAA\")"
        # --noconfirm: replace any pre-existing dist/<bundle> instead of
        # merging over it. Without it a stale local build leaks into the
        # output (e.g. an old runlayer-X.Y.Z.dist-info that the frozen app
        # then reports as its version). CI is always clean; local runs not.
        /opt/venv/bin/pyinstaller --noconfirm --workpath /opt/build --distpath dist "$SPEC"
        test -x "dist/$BUNDLE/$BUNDLE"
    '

echo "Built: $CLI_DIR/dist/$BUNDLE/"
