#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
pin="$(sed 's/^[[:space:]]*//;s/[[:space:]]*$//' "$script_dir/actionlint-version.txt")"

go install "github.com/rhysd/actionlint/cmd/actionlint@$pin"

host_os="$(go env GOHOSTOS)"
go_bin="$(go env GOBIN)"
if [ -z "$go_bin" ]; then
    gopath="$(go env GOPATH)"
    if [ "$host_os" = windows ]; then
        go_bin="${gopath%%;*}"
    else
        go_bin="${gopath%%:*}"
    fi
    go_bin="$go_bin/bin"
fi
if [ "$host_os" = windows ]; then
    go_bin="$(cygpath -u "$go_bin")"
fi
go_bin="$(cd -- "$go_bin" && pwd -P)"
if [ "$host_os" = windows ]; then
    go_bin="$(cygpath -m "$go_bin")"
fi
exe="$(go env GOEXE)"
version_output="$("$go_bin/actionlint$exe" -version)"
reported="$(printf '%s\n' "$version_output" | sed -n '1{s/^[[:space:]]*//;s/[[:space:]]*$//;p;}')"
if [ "${reported#v}" != "${pin#v}" ]; then
    printf 'actionlint version mismatch: expected %s, got %s\n' "$pin" "$reported" >&2
    exit 1
fi

if [ -n "${GITHUB_PATH:-}" ]; then
    printf '%s\n' "$go_bin" >> "$GITHUB_PATH"
fi
printf 'Verified actionlint %s at %s/actionlint%s\n' "$reported" "$go_bin" "$exe"
