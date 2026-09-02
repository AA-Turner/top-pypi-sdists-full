#!/usr/bin/env bash
set -euo pipefail

test_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
script="${test_dir}/../install.sh"
fixture="${test_dir}/fixtures/targets.json"
legacy_fixture="${test_dir}/fixtures/targets-glibc2.17.json"
temp_dir="$(mktemp -d)"
trap 'rm -rf "$temp_dir"' EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_contains() {
  local haystack="$1"
  local needle="$2"
  [[ "$haystack" == *"$needle"* ]] || fail "expected output to contain: $needle"
}

assert_not_contains() {
  local haystack="$1"
  local needle="$2"
  [[ "$haystack" != *"$needle"* ]] || fail "expected output not to contain: $needle"
}

assert_log_has_line() {
  local log_path="$1"
  local expected="$2"
  awk -v expected="$expected" '
    $0 == expected { found = 1 }
    END { exit !found }
  ' "$log_path" || fail "expected command log line: $expected"
}

assert_log_lacks_line() {
  local log_path="$1"
  local unexpected="$2"
  awk -v unexpected="$unexpected" '
    $0 == unexpected { found = 1 }
    END { exit found }
  ' "$log_path" || fail "unexpected command log line: $unexpected"
}

make_mocks() {
  local mock_dir="$1"
  mkdir -p "$mock_dir"

  cat >"$mock_dir/uname" <<'EOF'
#!/usr/bin/env bash
case "${1:-}" in
  -s) printf '%s\n' "${MOCK_UNAME_S:-Darwin}" ;;
  -m) printf '%s\n' "${MOCK_UNAME_M:-arm64}" ;;
  *) exit 2 ;;
esac
EOF

  cat >"$mock_dir/osascript" <<'EOF'
#!/usr/bin/env bash
args=()
while (($#)); do
  case "$1" in
    -l|-e)
      shift 2
      ;;
    *)
      args+=("$1")
      shift
      ;;
  esac
done
input_path="${args[0]}"
package="${args[1]}"
version="$(awk -F'"' '$2 == "version" { print $4; exit }' "$input_path")"
if [[ "$package" == "cli" ]]; then
  filename="runlayer-${version}-macos-arm64.pkg"
else
  filename="aiwatch-${version}-macos-arm64.pkg"
fi
printf '%s\t%s\t%s\t%s\n' \
  "$version" \
  "$filename" \
  '4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392' \
  '20'
EOF

  cat >"$mock_dir/curl" <<'EOF'
#!/usr/bin/env bash
output=""
headers=""
url=""
max_filesize=""
while (($#)); do
  case "$1" in
    -o|--output)
      output="$2"
      shift 2
      ;;
    -D|--dump-header)
      headers="$2"
      shift 2
      ;;
    -w|--write-out|-H|--header|--connect-timeout|--max-time|--max-filesize)
      if [[ "$1" == "--max-filesize" ]]; then
        max_filesize="$2"
      fi
      shift 2
      ;;
    -s|-S|-f|--silent|--show-error|--fail|--location|--no-progress-meter)
      shift
      ;;
    http://*|https://*)
      url="$1"
      shift
      ;;
    *)
      shift
      ;;
  esac
done

if [[ "${MOCK_REQUIRE_MAX_FILESIZE:-0}" == "1" ]]; then
  if [[ "$url" == */api/v1/binary-packages/targets* ]]; then
    [[ "$max_filesize" == "1048576" ]] || exit 63
  else
    [[ "$max_filesize" == "536870912" ]] || exit 63
  fi
fi

if [[ -n "${MOCK_CURL_LOG:-}" ]]; then
  printf '%s\n' "$url" >>"$MOCK_CURL_LOG"
fi

if [[ "$url" == */api/v1/binary-packages/targets* ]]; then
  if [[ "$url" == *"variant=glibc2.17"* ]]; then
    cp "$MOCK_LEGACY_TARGETS_FILE" "$output"
  else
    cp "$MOCK_TARGETS_FILE" "$output"
  fi
  printf '%s' "${MOCK_TARGETS_STATUS:-200}"
  exit 0
fi

download_status="${MOCK_DOWNLOAD_STATUS:-200}"
if [[ "$download_status" == "200" ]]; then
  printf '%s' 'signed-package-bytes' >"$output"
  if [[ -n "$headers" ]]; then
    printf 'HTTP/1.1 200 OK\r\nx-runlayer-sha256: %s\r\n\r\n' \
      '4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392' >"$headers"
  fi
fi
printf '%s' "$download_status"
EOF

  cat >"$mock_dir/pkgutil" <<'EOF'
#!/usr/bin/env bash
if [[ "${1:-}" == "--expand" ]]; then
  artifact_path="$2"
  destination="$3"
  artifact_name="${artifact_path##*/}"
  if [[ "$artifact_name" == runlayer-* ]]; then
    package_id="${MOCK_MACOS_PACKAGE_ID:-com.runlayer.cli}"
  else
    package_id="${MOCK_MACOS_PACKAGE_ID:-com.runlayer.aiwatch}"
  fi
  mkdir -p "$destination/component.pkg"
  printf '<pkg-info identifier="%s" version="%s"/>\n' \
    "$package_id" "${MOCK_MACOS_PACKAGE_VERSION:-0.29.15}" \
    >"$destination/component.pkg/PackageInfo"
  printf '<installer-gui-script><options hostArchitectures="%s"/></installer-gui-script>\n' \
    "${MOCK_MACOS_PACKAGE_ARCH:-arm64}" >"$destination/Distribution"
  exit 0
fi
printf '%s\n' \
  'Package "installer.pkg":' \
  '   Status: signed by a developer certificate issued by Apple for distribution' \
  '   Certificate Chain:' \
  '    1. Developer ID Installer: Runlayer Inc. (AF2M8HC7A2)'
EOF

  cat >"$mock_dir/xmllint" <<'EOF'
#!/usr/bin/env bash
xpath="$2"
input_path="$3"
case "$xpath" in
  *identifier*)
    sed -n 's/.*identifier="\([^"]*\)".*/\1/p' "$input_path"
    ;;
  *version*)
    sed -n 's/.*version="\([^"]*\)".*/\1/p' "$input_path"
    ;;
  *hostArchitectures*)
    sed -n 's/.*hostArchitectures="\([^"]*\)".*/\1/p' "$input_path"
    ;;
  *)
    exit 2
    ;;
esac
EOF

  cat >"$mock_dir/spctl" <<'EOF'
#!/usr/bin/env bash
echo 'source=Notarized Developer ID' >&2
EOF

  cat >"$mock_dir/sudo" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$*" >>"$MOCK_COMMAND_LOG"
case "${1:-}" in
  test)
    [[ "${MOCK_CLI_UPDATE_PRESENT:-1}" == "1" ]]
    ;;
  launchctl)
    exit "${MOCK_LAUNCHCTL_EXIT:-0}"
    ;;
  dpkg)
    exit "${MOCK_DPKG_EXIT:-0}"
    ;;
  apt-get)
    exit "${MOCK_APT_GET_EXIT:-0}"
    ;;
  /usr/bin/mktemp)
    mkdir -p "$MOCK_PRIVILEGED_TMPDIR"
    /usr/bin/mktemp -d \
      "${MOCK_PRIVILEGED_TMPDIR}/${3##*/}"
    ;;
  /bin/chmod)
    /bin/chmod "${@:2}"
    ;;
  /usr/bin/install)
    destination="${@: -1}"
    if [[ "$destination" == "$MOCK_PRIVILEGED_TMPDIR"/* ]]; then
      /usr/bin/install "${@:2}"
      if [[ "${MOCK_TAMPER_STAGED_ARTIFACT:-0}" == "1" ]]; then
        printf 'tampered-artifact!!!' >"$destination"
      fi
    fi
    ;;
  /bin/rm)
    target="${@: -1}"
    if [[ "$target" == "$MOCK_PRIVILEGED_TMPDIR"/* ]]; then
      /bin/rm "${@:2}"
    fi
    ;;
  /usr/lib/runlayer/run-cli-update.sh)
    exit "${MOCK_CLI_UPDATE_EXIT:-0}"
    ;;
esac
EOF

  cat >"$mock_dir/dpkg" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF

  cat >"$mock_dir/dpkg-query" <<'EOF'
#!/usr/bin/env bash
[[ "${MOCK_DPKG_QUERY_EXIT:-0}" == "0" ]] || exit "$MOCK_DPKG_QUERY_EXIT"
printf '%s\t%s' \
  "${MOCK_INSTALLED_DEB_STATUS:-install ok installed}" \
  "${MOCK_INSTALLED_DEB_VERSION:-0.29.15}"
EOF

  cat >"$mock_dir/dpkg-deb" <<'EOF'
#!/usr/bin/env bash
case "${@: -1}" in
  Package) printf '%s\n' "${MOCK_DEB_PACKAGE:-runlayer-aiwatch}" ;;
  Version) printf '%s\n' "${MOCK_DEB_VERSION:-0.29.15}" ;;
  Architecture) printf '%s\n' "${MOCK_DEB_ARCH:-amd64}" ;;
  *) exit 2 ;;
esac
EOF

  cat >"$mock_dir/getconf" <<'EOF'
#!/usr/bin/env bash
if [[ "${1:-}" == "GNU_LIBC_VERSION" ]]; then
  printf 'glibc %s\n' "${MOCK_GLIBC_VERSION:-2.35}"
  exit 0
fi
exit 2
EOF

  cat >"$mock_dir/apt-get" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF

  chmod +x "$mock_dir"/*
}

run_install() {
  local mock_dir="$1"
  shift
  PATH="$mock_dir:$PATH" \
    MOCK_TARGETS_FILE="${MOCK_TARGETS_FILE:-$fixture}" \
    MOCK_LEGACY_TARGETS_FILE="${MOCK_LEGACY_TARGETS_FILE:-$legacy_fixture}" \
    MOCK_COMMAND_LOG="${MOCK_COMMAND_LOG:-$temp_dir/commands.log}" \
    MOCK_PRIVILEGED_TMPDIR="${MOCK_PRIVILEGED_TMPDIR:-$temp_dir/privileged}" \
    MOCK_UNAME_S="${MOCK_UNAME_S:-Darwin}" \
    MOCK_UNAME_M="${MOCK_UNAME_M:-arm64}" \
    MOCK_DOWNLOAD_STATUS="${MOCK_DOWNLOAD_STATUS:-200}" \
    RUNLAYER_OSASCRIPT_BIN="$mock_dir/osascript" \
    RUNLAYER_XMLLINT_BIN="$mock_dir/xmllint" \
    bash "$script" "$@" 2>&1
}

test_requires_arguments() {
  local output
  if output="$(bash "$script" 2>&1)"; then
    fail "missing arguments should fail"
  fi
  assert_contains "$output" "--host is required"
  assert_not_contains "$output" "installed successfully"
}

test_rejects_unsupported_package() {
  local output
  if output="$(bash "$script" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package desktop 2>&1)"; then
    fail "unsupported package should fail"
  fi
  assert_contains "$output" "--package must be ai-watch or cli"
}

test_installs_macos_ai_watch() {
  local mock_dir="$temp_dir/macos-mocks"
  local command_log="$temp_dir/macos-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_COMMAND_LOG="$command_log"
  export MOCK_COMMAND_LOG

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"

  assert_contains "$output" "Runlayer AI Watch installed successfully."
  assert_contains "$(cat "$command_log")" "installer -pkg"
  assert_contains "$(cat "$command_log")" \
    "/usr/local/bin/aiwatch setup config --host https://tenant.runlayer.com --org-api-key rl_org_test"
  assert_not_contains "$(cat "$command_log")" \
    "launchctl kickstart system/com.runlayer.cli.update"
}

test_limits_http_download_sizes() {
  local mock_dir="$temp_dir/max-filesize-mocks"
  local output
  make_mocks "$mock_dir"
  MOCK_REQUIRE_MAX_FILESIZE=1
  export MOCK_REQUIRE_MAX_FILESIZE

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"

  assert_contains "$output" "Runlayer AI Watch installed successfully."
  unset MOCK_REQUIRE_MAX_FILESIZE
}

test_reverifies_protected_installer_copy() {
  local mock_dir="$temp_dir/tamper-mocks"
  local command_log="$temp_dir/tamper-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_COMMAND_LOG="$command_log"
  MOCK_TAMPER_STAGED_ARTIFACT=1
  export MOCK_COMMAND_LOG MOCK_TAMPER_STAGED_ARTIFACT

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "tampered protected installer should fail"
  fi

  assert_contains "$output" "installer checksum does not match"
  assert_not_contains "$(cat "$command_log")" "/usr/sbin/installer"
  unset MOCK_TAMPER_STAGED_ARTIFACT
}

test_rejects_wrong_macos_package_identity() {
  local mock_dir="$temp_dir/wrong-macos-package-mocks"
  local command_log="$temp_dir/wrong-macos-package-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_COMMAND_LOG="$command_log"
  MOCK_MACOS_PACKAGE_ID=com.runlayer.cli
  export MOCK_COMMAND_LOG MOCK_MACOS_PACKAGE_ID

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "wrong macOS package identity should fail"
  fi

  assert_contains "$output" "unexpected macOS package identity"
  assert_not_contains "$(cat "$command_log")" "/usr/sbin/installer"
  unset MOCK_MACOS_PACKAGE_ID
}

test_installs_macos_cli() {
  local mock_dir="$temp_dir/cli-mocks"
  local command_log="$temp_dir/cli-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_COMMAND_LOG="$command_log"
  export MOCK_COMMAND_LOG

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package cli)"

  assert_contains "$output" "Runlayer CLI installed successfully."
  assert_contains "$(cat "$command_log")" \
    "/usr/local/bin/runlayer setup config --host https://tenant.runlayer.com --org-api-key rl_org_test"
  assert_contains "$(cat "$command_log")" \
    "launchctl kickstart system/com.runlayer.cli.update"
}

test_macos_cli_update_kick_failure_is_non_fatal() {
  local mock_dir="$temp_dir/cli-kick-fail-mocks"
  local command_log="$temp_dir/cli-kick-fail-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_COMMAND_LOG="$command_log"
  MOCK_LAUNCHCTL_EXIT=1
  export MOCK_COMMAND_LOG MOCK_LAUNCHCTL_EXIT

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package cli)"

  assert_contains "$output" "Runlayer CLI installed successfully."
  assert_contains "$output" "could not trigger the update check now"
  assert_contains "$(cat "$command_log")" \
    "launchctl kickstart system/com.runlayer.cli.update"
  unset MOCK_LAUNCHCTL_EXIT
}

test_rejects_old_macos_target() {
  local mock_dir="$temp_dir/old-mocks"
  local old_fixture="$temp_dir/old-targets.json"
  local curl_log="$temp_dir/old-curl.log"
  local output
  make_mocks "$mock_dir"
  sed 's/0\.29\.15/0.29.14/g' "$fixture" >"$old_fixture"
  MOCK_TARGETS_FILE="$old_fixture"
  MOCK_CURL_LOG="$curl_log"
  export MOCK_TARGETS_FILE MOCK_CURL_LOG

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "old macOS target should fail"
  fi

  assert_contains "$output" "requires package version 0.29.15 or newer"
  assert_contains "$output" "https://docs.runlayer.com/shadow-ai/deploy/test-device"
  assert_not_contains "$output" "installed successfully"
  assert_not_contains "$(cat "$curl_log")" "/api/v1/binary-packages/ai-watch/"
  unset MOCK_TARGETS_FILE MOCK_CURL_LOG
}

test_reports_artifact_cache_miss() {
  local mock_dir="$temp_dir/cache-mocks"
  local output
  make_mocks "$mock_dir"
  MOCK_DOWNLOAD_STATUS=409
  export MOCK_DOWNLOAD_STATUS

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "409 artifact download should fail"
  fi

  assert_contains "$output" "not cached yet"
  assert_contains "$output" "retry"
  assert_not_contains "$output" "installed successfully"
}

test_installs_legacy_linux_variant() {
  local mock_dir="$temp_dir/legacy-linux-mocks"
  local curl_log="$temp_dir/legacy-linux-curl.log"
  local command_log="$temp_dir/legacy-linux-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.34
  MOCK_CURL_LOG="$curl_log"
  MOCK_COMMAND_LOG="$command_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_CURL_LOG
  export MOCK_COMMAND_LOG

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"

  assert_contains "$output" "Runlayer AI Watch installed successfully."
  assert_contains "$(cat "$curl_log")" \
    "/api/v1/binary-packages/targets?variant=glibc2.17"
  assert_contains "$(cat "$command_log")" \
    "runlayer-aiwatch_0.29.15_amd64.glibc2.17.deb"
  assert_contains "$(cat "$command_log")" "dpkg -i"
  assert_not_contains "$(cat "$command_log")" "run-cli-update.sh"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_CURL_LOG
  unset MOCK_COMMAND_LOG
}

test_installs_legacy_linux_variant_after_apt_fix_recovery() {
  local mock_dir="$temp_dir/legacy-recovery-linux-mocks"
  local command_log="$temp_dir/legacy-recovery-linux-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.34
  MOCK_COMMAND_LOG="$command_log"
  MOCK_DPKG_EXIT=1
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_COMMAND_LOG
  export MOCK_DPKG_EXIT

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"

  assert_contains "$output" "Runlayer AI Watch installed successfully."
  assert_contains "$(cat "$command_log")" "apt-get install -f -y"
  assert_contains "$(cat "$command_log")" "install -m 600"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_COMMAND_LOG
  unset MOCK_DPKG_EXIT
}

test_fails_when_legacy_deb_recovery_leaves_package_uninstalled() {
  local mock_dir="$temp_dir/legacy-unrecovered-linux-mocks"
  local command_log="$temp_dir/legacy-unrecovered-linux-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.34
  MOCK_COMMAND_LOG="$command_log"
  MOCK_DPKG_EXIT=1
  MOCK_DPKG_QUERY_EXIT=1
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_COMMAND_LOG
  export MOCK_DPKG_EXIT MOCK_DPKG_QUERY_EXIT

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "dpkg failure not repaired by apt-get -f should fail"
  fi

  assert_contains "$output" "did not finish installing"
  assert_not_contains "$output" "installed successfully"
  assert_not_contains "$(cat "$command_log")" "install -m 600"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_COMMAND_LOG
  unset MOCK_DPKG_EXIT MOCK_DPKG_QUERY_EXIT
}

test_fails_when_legacy_deb_recovery_leaves_broken_state() {
  local mock_dir="$temp_dir/legacy-broken-linux-mocks"
  local command_log="$temp_dir/legacy-broken-linux-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.34
  MOCK_COMMAND_LOG="$command_log"
  MOCK_DPKG_EXIT=1
  MOCK_INSTALLED_DEB_STATUS="install reinstreq half-installed"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_COMMAND_LOG
  export MOCK_DPKG_EXIT MOCK_INSTALLED_DEB_STATUS

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "half-installed package after apt-get -f should fail"
  fi

  assert_contains "$output" "did not finish installing"
  assert_not_contains "$(cat "$command_log")" "install -m 600"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_COMMAND_LOG
  unset MOCK_DPKG_EXIT MOCK_INSTALLED_DEB_STATUS
}

test_installs_legacy_linux_with_portable_json_fallback() {
  local mock_dir="$temp_dir/legacy-portable-linux-mocks"
  local curl_log="$temp_dir/legacy-portable-linux-curl.log"
  local command_log="$temp_dir/legacy-portable-linux-commands.log"
  local output
  make_mocks "$mock_dir"
  cat >"$mock_dir/python3" <<'EOF'
#!/usr/bin/env bash
exit 127
EOF
  cat >"$mock_dir/sha256sum" <<'EOF'
#!/usr/bin/env bash
printf '%s  %s\n' \
  '4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392' \
  "$1"
EOF
  chmod +x "$mock_dir/python3" "$mock_dir/sha256sum"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.34
  MOCK_CURL_LOG="$curl_log"
  MOCK_COMMAND_LOG="$command_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_CURL_LOG
  export MOCK_COMMAND_LOG

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"

  assert_contains "$output" "Runlayer AI Watch installed successfully."
  assert_contains "$(cat "$curl_log")" \
    "/api/v1/binary-packages/targets?variant=glibc2.17"
  assert_contains "$(cat "$command_log")" \
    "runlayer-aiwatch_0.29.15_amd64.glibc2.17.deb"
  assert_contains "$(cat "$command_log")" "dpkg -i"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_CURL_LOG
  unset MOCK_COMMAND_LOG
}

test_reports_unavailable_legacy_linux_variant() {
  local mock_dir="$temp_dir/missing-legacy-linux-mocks"
  local curl_log="$temp_dir/missing-legacy-linux-curl.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.34
  MOCK_LEGACY_TARGETS_FILE="$fixture"
  MOCK_CURL_LOG="$curl_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION
  export MOCK_LEGACY_TARGETS_FILE MOCK_CURL_LOG

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "missing legacy variant should fail"
  fi

  assert_contains "$output" "no compatible legacy Linux installer is available"
  assert_contains "$output" "legacy-distributions-glibc-217"
  assert_not_contains "$(cat "$curl_log")" \
    "/api/v1/binary-packages/ai-watch/"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION
  unset MOCK_LEGACY_TARGETS_FILE MOCK_CURL_LOG
}

test_rejects_unsupported_linux_glibc_before_target_resolution() {
  local mock_dir="$temp_dir/unsupported-glibc-linux-mocks"
  local curl_log="$temp_dir/unsupported-glibc-linux-curl.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.16
  MOCK_CURL_LOG="$curl_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_CURL_LOG

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "glibc older than 2.17 should fail before target resolution"
  fi

  assert_contains "$output" "requires glibc 2.17 or newer"
  assert_contains "$output" "legacy-distributions-glibc-217"
  [[ ! -e "$curl_log" ]] ||
    assert_not_contains "$(cat "$curl_log")" "/api/v1/binary-packages/targets"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_CURL_LOG
}

test_rejects_invalid_json_when_python_is_available() {
  local mock_dir="$temp_dir/invalid-json-mocks"
  local invalid_fixture="$temp_dir/invalid-targets.json"
  local output
  make_mocks "$mock_dir"
  {
    cat "$fixture"
    printf 'not-json\n'
  } >"$invalid_fixture"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_TARGETS_FILE="$invalid_fixture"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_TARGETS_FILE

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "invalid JSON should fail closed when Python is available"
  fi

  assert_contains "$output" "invalid or unavailable ai-watch target"
  assert_not_contains "$output" "installed successfully"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_TARGETS_FILE
}

test_rejects_wrong_linux_package_identity() {
  local mock_dir="$temp_dir/wrong-linux-package-mocks"
  local command_log="$temp_dir/wrong-linux-package-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_DEB_PACKAGE="unexpected-package"
  MOCK_COMMAND_LOG="$command_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"; then
    fail "wrong Linux package identity should fail"
  fi

  assert_contains "$output" "unexpected Linux package identity"
  assert_not_contains "$(cat "$command_log")" "apt-get install"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
}

test_installs_linux_cli() {
  local mock_dir="$temp_dir/linux-cli-mocks"
  local command_log="$temp_dir/linux-cli-commands.log"
  local curl_log="$temp_dir/linux-cli-curl.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_DEB_PACKAGE=runlayer
  MOCK_COMMAND_LOG="$command_log"
  MOCK_CURL_LOG="$curl_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
  export MOCK_CURL_LOG

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package cli)"

  assert_contains "$output" "Runlayer CLI installed successfully."
  assert_contains "$(cat "$curl_log")" \
    "/api/v1/binary-packages/cli/0.29.15/runlayer_0.29.15_amd64.deb"
  assert_contains "$(cat "$command_log")" "apt-get install -y"
  assert_contains "$(cat "$command_log")" "/etc/runlayer/aiwatch/config.json"
  assert_contains "$(cat "$command_log")" "install -m 600"
  assert_contains "$(cat "$command_log")" "/etc/runlayer/aiwatch/credentials"
  assert_contains "$output" "Triggering the first update check..."
  assert_contains "$(cat "$command_log")" \
    "test -x /usr/lib/runlayer/run-cli-update.sh"
  assert_log_has_line "$command_log" "/usr/lib/runlayer/run-cli-update.sh"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
  unset MOCK_CURL_LOG
}

test_linux_cli_update_kick_failure_is_non_fatal() {
  local mock_dir="$temp_dir/linux-cli-kick-fail-mocks"
  local command_log="$temp_dir/linux-cli-kick-fail-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_DEB_PACKAGE=runlayer
  MOCK_COMMAND_LOG="$command_log"
  MOCK_CLI_UPDATE_EXIT=1
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
  export MOCK_CLI_UPDATE_EXIT

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package cli)"

  assert_contains "$output" "Runlayer CLI installed successfully."
  assert_contains "$output" "could not trigger the update check now"
  assert_contains "$output" "hourly cron schedule will run it instead"
  assert_log_has_line "$command_log" "/usr/lib/runlayer/run-cli-update.sh"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
  unset MOCK_CLI_UPDATE_EXIT
}

test_linux_cli_without_update_wrapper_skips_kick() {
  local mock_dir="$temp_dir/linux-cli-no-wrapper-mocks"
  local command_log="$temp_dir/linux-cli-no-wrapper-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_DEB_PACKAGE=runlayer
  MOCK_COMMAND_LOG="$command_log"
  MOCK_CLI_UPDATE_PRESENT=0
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
  export MOCK_CLI_UPDATE_PRESENT

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package cli)"

  assert_contains "$output" "Runlayer CLI installed successfully."
  assert_not_contains "$output" "Triggering the first update check..."
  assert_log_has_line "$command_log" \
    "test -x /usr/lib/runlayer/run-cli-update.sh"
  assert_log_lacks_line "$command_log" "/usr/lib/runlayer/run-cli-update.sh"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
  unset MOCK_CLI_UPDATE_PRESENT
}

test_rejects_wrong_linux_cli_package_identity() {
  local mock_dir="$temp_dir/wrong-linux-cli-package-mocks"
  local command_log="$temp_dir/wrong-linux-cli-package-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_DEB_PACKAGE=runlayer-aiwatch
  MOCK_COMMAND_LOG="$command_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG

  if output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package cli)"; then
    fail "an ai-watch deb offered as the cli package should fail"
  fi

  assert_contains "$output" "unexpected Linux package identity"
  assert_not_contains "$(cat "$command_log")" "apt-get install"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_DEB_PACKAGE MOCK_COMMAND_LOG
}

test_installs_legacy_linux_cli_variant() {
  local mock_dir="$temp_dir/legacy-linux-cli-mocks"
  local curl_log="$temp_dir/legacy-linux-cli-curl.log"
  local command_log="$temp_dir/legacy-linux-cli-commands.log"
  local output
  make_mocks "$mock_dir"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_GLIBC_VERSION=2.34
  MOCK_DEB_PACKAGE=runlayer
  MOCK_CURL_LOG="$curl_log"
  MOCK_COMMAND_LOG="$command_log"
  unset MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_DEB_PACKAGE
  export MOCK_CURL_LOG MOCK_COMMAND_LOG

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test \
    --package cli)"

  assert_contains "$output" "Runlayer CLI installed successfully."
  assert_contains "$(cat "$curl_log")" \
    "/api/v1/binary-packages/targets?variant=glibc2.17"
  assert_contains "$(cat "$command_log")" \
    "runlayer_0.29.15_amd64.glibc2.17.deb"
  assert_contains "$(cat "$command_log")" "dpkg -i"
  unset MOCK_UNAME_S MOCK_UNAME_M MOCK_GLIBC_VERSION MOCK_DEB_PACKAGE
  unset MOCK_CURL_LOG MOCK_COMMAND_LOG
}

test_installs_linux_with_portable_json_fallback() {
  local mock_dir="$temp_dir/linux-mocks"
  local command_log="$temp_dir/linux-commands.log"
  local curl_log="$temp_dir/linux-curl.log"
  local output
  make_mocks "$mock_dir"
  cat >"$mock_dir/python3" <<'EOF'
#!/usr/bin/env bash
exit 127
EOF
  cat >"$mock_dir/sha256sum" <<'EOF'
#!/usr/bin/env bash
printf '%s  %s\n' \
  '4d9c5af680d7cd7d1781c5c0f9f306828fbba5b65e61f3c6f3a611c1496a1392' \
  "$1"
EOF
  chmod +x "$mock_dir/python3" "$mock_dir/sha256sum"
  MOCK_UNAME_S=Linux
  MOCK_UNAME_M=x86_64
  MOCK_COMMAND_LOG="$command_log"
  MOCK_CURL_LOG="$curl_log"
  unset MOCK_TARGETS_FILE MOCK_DOWNLOAD_STATUS
  export MOCK_UNAME_S MOCK_UNAME_M MOCK_COMMAND_LOG MOCK_CURL_LOG

  output="$(run_install "$mock_dir" \
    --host https://tenant.runlayer.com \
    --org-api-key rl_org_test)"

  assert_contains "$output" "Runlayer AI Watch installed successfully."
  assert_contains "$(cat "$curl_log")" \
    "https://tenant.runlayer.com/api/v1/binary-packages/targets"
  assert_not_contains "$(cat "$curl_log")" "targets?variant="
  assert_contains "$(cat "$command_log")" "apt-get install -y"
  assert_contains "$(cat "$command_log")" "install -m 600"
  unset MOCK_COMMAND_LOG MOCK_CURL_LOG
}

test_requires_arguments
test_rejects_unsupported_package
test_installs_macos_ai_watch
test_limits_http_download_sizes
test_reverifies_protected_installer_copy
test_rejects_wrong_macos_package_identity
test_installs_macos_cli
test_macos_cli_update_kick_failure_is_non_fatal
test_rejects_old_macos_target
test_reports_artifact_cache_miss
test_installs_legacy_linux_variant
test_installs_legacy_linux_variant_after_apt_fix_recovery
test_fails_when_legacy_deb_recovery_leaves_package_uninstalled
test_fails_when_legacy_deb_recovery_leaves_broken_state
test_installs_legacy_linux_with_portable_json_fallback
test_reports_unavailable_legacy_linux_variant
test_rejects_unsupported_linux_glibc_before_target_resolution
test_rejects_invalid_json_when_python_is_available
test_rejects_wrong_linux_package_identity
test_installs_linux_cli
test_linux_cli_update_kick_failure_is_non_fatal
test_linux_cli_without_update_wrapper_skips_kick
test_rejects_wrong_linux_cli_package_identity
test_installs_legacy_linux_cli_variant
test_installs_linux_with_portable_json_fallback

echo "install.sh tests passed"
