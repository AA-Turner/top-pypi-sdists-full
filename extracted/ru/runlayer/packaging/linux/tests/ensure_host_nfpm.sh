#!/bin/bash
# Source (don't exec) to put a HOST-platform nfpm on PATH for the test scripts
# in this directory. The packaging scripts' own fallback only installs the
# Linux x86_64 binary (they run on CI hosts), so macOS dev machines need this.
# Single home for the NFPM_VERSION pin used by tests.

ensure_host_nfpm() { # <tools-dir>
    command -v nfpm >/dev/null && return 0
    local tools_dir="$1"
    if [ ! -x "$tools_dir/nfpm" ]; then
        echo "  nfpm not on PATH; installing into $tools_dir..."
        mkdir -p "$tools_dir"
        local nfpm_version="2.43.0" os arch
        os=$(uname -s) # Darwin/Linux — matches nfpm release asset naming
        arch=$(uname -m)
        [ "$arch" = "aarch64" ] && arch=arm64
        curl -sSfL \
            "https://github.com/goreleaser/nfpm/releases/download/v${nfpm_version}/nfpm_${nfpm_version}_${os}_${arch}.tar.gz" \
            | tar -xz -C "$tools_dir" nfpm
    fi
    PATH="$tools_dir:$PATH"
}
