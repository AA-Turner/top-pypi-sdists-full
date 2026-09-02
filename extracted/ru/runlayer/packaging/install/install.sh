#!/usr/bin/env bash
set -euo pipefail

readonly DOCS_URL="https://docs.runlayer.com/shadow-ai/deploy/test-device#manual-installation-fallback"
readonly LINUX_LEGACY_DOCS_URL="https://docs.runlayer.com/shadow-ai/deploy/linux#legacy-distributions-glibc-217"
readonly MAX_TARGET_BYTES=1048576
readonly MAX_INSTALLER_BYTES=536870912
readonly MACOS_TEAM_ID="AF2M8HC7A2"
readonly MACOS_MIN_VERSION="0.29.15"
readonly OSASCRIPT_BIN="${RUNLAYER_OSASCRIPT_BIN:-/usr/bin/osascript}"
readonly XMLLINT_BIN="${RUNLAYER_XMLLINT_BIN:-/usr/bin/xmllint}"

host=""
org_api_key=""
package="ai-watch"
target_variant=""
temp_dir=""
privileged_temp_dir=""
privileged_artifact_path=""
error_reported=0

usage() {
  cat <<'EOF'
Usage: install.sh --host URL --org-api-key KEY [--package ai-watch|cli]

Downloads, verifies, installs, and configures a Runlayer Test Device package.
EOF
}

die() {
  error_reported=1
  echo "Error: $*" >&2
  exit 1
}

cleanup() {
  if [[ -n "$privileged_temp_dir" ]]; then
    sudo /bin/rm -rf "$privileged_temp_dir" >/dev/null 2>&1 || true
  fi
  if [[ -n "$temp_dir" && -d "$temp_dir" ]]; then
    rm -rf "$temp_dir"
  fi
}

unexpected_error() {
  local exit_code=$?
  if [[ "$error_reported" -eq 0 ]]; then
    echo "Error: installation failed unexpectedly. See ${DOCS_URL} for the manual flow." >&2
  fi
  exit "$exit_code"
}

trap cleanup EXIT
trap unexpected_error ERR

parse_args() {
  while (($#)); do
    case "$1" in
      --host)
        (($# >= 2)) || die "--host requires a value"
        host="$2"
        shift 2
        ;;
      --org-api-key)
        (($# >= 2)) || die "--org-api-key requires a value"
        org_api_key="$2"
        shift 2
        ;;
      --package)
        (($# >= 2)) || die "--package requires a value"
        package="$2"
        shift 2
        ;;
      -h | --help)
        usage
        exit 0
        ;;
      *)
        die "unknown argument: $1"
        ;;
    esac
  done

  [[ -n "$host" ]] || die "--host is required"
  [[ -n "$org_api_key" ]] || die "--org-api-key is required"
  [[ "$package" == "ai-watch" || "$package" == "cli" ]] ||
    die "--package must be ai-watch or cli"
  [[ "$host" == https://* && "$host" != *[[:space:]]* ]] ||
    die "--host must be an absolute HTTPS URL without whitespace"
  [[ "$org_api_key" =~ ^rl_org_[A-Za-z0-9_-]+$ ]] ||
    die "--org-api-key must be an rl_org_ key without whitespace"

  host="${host%/}"
}

detect_target_slot() {
  local system machine
  system="$(uname -s)"
  machine="$(uname -m)"

  case "$machine" in
    arm64 | aarch64)
      target_arch="arm64"
      ;;
    x86_64 | amd64)
      target_arch="x86_64"
      ;;
    *)
      die "unsupported architecture: $machine"
      ;;
  esac

  case "$system" in
    Darwin)
      target_platform="macos"
      target_format="pkg"
      ;;
    Linux)
      target_platform="linux"
      detect_linux_glibc_variant
      detect_linux_format
      ;;
    *)
      die "unsupported operating system: $system"
      ;;
  esac
}

detect_linux_glibc_variant() {
  local glibc_output major minor major_number minor_number
  glibc_output="$(getconf GNU_LIBC_VERSION 2>/dev/null)" ||
    die "Linux one-command setup requires glibc 2.17 or newer; see ${LINUX_LEGACY_DOCS_URL}"
  if [[ "$glibc_output" =~ ^glibc[[:space:]]+([0-9]+)\.([0-9]+)(\.[0-9]+)*$ ]]; then
    major="${BASH_REMATCH[1]}"
    minor="${BASH_REMATCH[2]}"
  else
    die "Linux one-command setup requires glibc 2.17 or newer; see ${LINUX_LEGACY_DOCS_URL}"
  fi
  [[ "${#major}" -le 9 && "${#minor}" -le 9 ]] ||
    die "Linux one-command setup requires glibc 2.17 or newer; see ${LINUX_LEGACY_DOCS_URL}"
  major_number=$((10#$major))
  minor_number=$((10#$minor))

  if ((major_number > 2 || (major_number == 2 && minor_number >= 35))); then
    target_variant=""
  elif ((major_number == 2 && minor_number >= 17)); then
    target_variant="glibc2.17"
  else
    die "Linux one-command setup requires glibc 2.17 or newer; see ${LINUX_LEGACY_DOCS_URL}"
  fi
}

detect_linux_format() {
  local has_dpkg=0
  local has_rpm=0
  command -v dpkg >/dev/null 2>&1 && has_dpkg=1
  command -v rpm >/dev/null 2>&1 && has_rpm=1

  if [[ "$has_dpkg" -eq 1 && "$has_rpm" -eq 0 ]]; then
    target_format="deb"
  elif [[ "$has_dpkg" -eq 0 && "$has_rpm" -eq 1 ]]; then
    target_format="rpm"
  elif [[ "$has_dpkg" -eq 1 && "$has_rpm" -eq 1 ]]; then
    local distro_ids=""
    if [[ -r /etc/os-release ]]; then
      distro_ids="$(
        awk -F= '
          $1 == "ID" || $1 == "ID_LIKE" {
            gsub(/^["\047]|["\047]$/, "", $2)
            printf "%s ", tolower($2)
          }
        ' /etc/os-release
      )"
    fi
    case " $distro_ids " in
      *" debian "* | *" ubuntu "* | *" linuxmint "* | *" pop "* | *" kali "*)
        target_format="deb"
        ;;
      *" rhel "* | *" fedora "* | *" centos "* | *" rocky "* | *" almalinux "* | *" amzn "* | *" suse "* | *" opensuse "*)
        target_format="rpm"
        ;;
      *)
        die "found both dpkg and rpm but could not determine the Linux distribution family"
        ;;
    esac
  else
    die "Linux installation requires dpkg or rpm"
  fi
}

fetch_targets() {
  local output_path="$1"
  local http_status targets_url
  targets_url="${host}/api/v1/binary-packages/targets"
  if [[ -n "$target_variant" ]]; then
    targets_url="${targets_url}?variant=${target_variant}"
  fi
  echo "Resolving the ${package} package selected by your Client Updates policy..."
  if ! http_status="$(
    curl \
      --silent \
      --show-error \
      --connect-timeout 15 \
      --max-time 60 \
      --max-filesize "$MAX_TARGET_BYTES" \
      --header "x-runlayer-api-key: ${org_api_key}" \
      --header "Accept-Encoding: identity" \
      --output "$output_path" \
      --write-out "%{http_code}" \
      "$targets_url"
  )"; then
    die "could not reach ${host}"
  fi

  case "$http_status" in
    200) ;;
    401 | 403)
      die "the organization API key is invalid or lacks the Shadow AI Scan role"
      ;;
    *)
      die "target resolution failed with HTTP ${http_status}"
      ;;
  esac

  local response_size
  response_size="$(wc -c <"$output_path" | tr -d '[:space:]')"
  [[ "$response_size" =~ ^[0-9]+$ && "$response_size" -le "$MAX_TARGET_BYTES" ]] ||
    die "the binary package response is too large"
}

parse_target_macos() {
  local input_path="$1"
  "$OSASCRIPT_BIN" -l JavaScript -e '
    ObjC.import("Foundation");
    function run(argv) {
      const data = $.NSData.dataWithContentsOfFile(argv[0]);
      if (!data) throw new Error("could not read targets response");
      const text = $.NSString.alloc.initWithDataEncoding(
        data,
        $.NSUTF8StringEncoding
      ).js;
      const payload = JSON.parse(text);
      if (!payload || !Array.isArray(payload.data)) {
        throw new Error("targets response has no data list");
      }
      const rows = payload.data.filter((row) => row && row.package === argv[1]);
      if (rows.length !== 1 || !rows[0].resolved_target) {
        throw new Error("resolved package target is unavailable");
      }
      const target = rows[0].resolved_target;
      if (!Array.isArray(target.artifacts)) {
        throw new Error("resolved package target has no artifacts");
      }
      const matches = target.artifacts.filter((artifact) =>
        artifact &&
        artifact.platform === argv[2] &&
        artifact.arch === argv[3] &&
        artifact.format === argv[4] &&
        artifact.variant === null
      );
      if (matches.length !== 1) {
        throw new Error("resolved package target has no unambiguous installer");
      }
      const artifact = matches[0];
      return [
        target.version,
        artifact.filename,
        artifact.sha256,
        String(artifact.size_bytes)
      ].join("\t");
    }
  ' "$input_path" "$package" "$target_platform" "$target_arch" "$target_format"
}

parse_target_python() {
  local input_path="$1"
  local requested_variant="$2"
  python3 - \
    "$input_path" \
    "$package" \
    "$target_platform" \
    "$target_arch" \
    "$target_format" \
    "$requested_variant" <<'PY'
import json
import sys

path, package, platform, arch, artifact_format, variant = sys.argv[1:]
requested_variant = variant or None
with open(path, encoding="utf-8") as response_file:
    payload = json.load(response_file)
if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
    raise ValueError("targets response has no data list")
rows = [
    row
    for row in payload["data"]
    if isinstance(row, dict) and row.get("package") == package
]
if len(rows) != 1 or not isinstance(rows[0].get("resolved_target"), dict):
    raise ValueError("resolved package target is unavailable")
target = rows[0]["resolved_target"]
if "version" not in target or not isinstance(target.get("artifacts"), list):
    raise ValueError("resolved package target has no artifacts")
missing_variant = object()
matches = [
    artifact
    for artifact in target["artifacts"]
    if isinstance(artifact, dict)
    and artifact.get("platform") == platform
    and artifact.get("arch") == arch
    and artifact.get("format") == artifact_format
    and artifact.get("variant", missing_variant) == requested_variant
]
if not matches:
    sys.exit(2)
if len(matches) > 1:
    raise ValueError("resolved package target has no unambiguous installer")
artifact = matches[0]
print(
    "\t".join(
        (
            str(target["version"]),
            str(artifact["filename"]),
            str(artifact["sha256"]),
            str(artifact["size_bytes"]),
        )
    )
)
PY
}

extract_json_string() {
  local object="$1"
  local field="$2"
  printf '%s\n' "$object" |
    sed -n 's/.*"'"$field"'":"\([^"]*\)".*/\1/p'
}

extract_json_integer() {
  local object="$1"
  local field="$2"
  printf '%s\n' "$object" |
    sed -n 's/.*"'"$field"'":\([0-9][0-9]*\).*/\1/p'
}

parse_target_portable() {
  local input_path="$1"
  local requested_variant="$2"
  local compact rows row="" candidate row_count=0 artifacts artifact=""
  local artifact_count=0 variant_fragment

  compact="$(tr -d '[:space:]' <"$input_path")"
  [[ "$compact" == \{* && "$compact" == *\} &&
    "$compact" == *'"data":['* ]] || return 1
  rows="$(printf '%s\n' "$compact" | awk '{gsub(/\{"package":/, "\n{\"package\":"); print}')"
  while IFS= read -r candidate; do
    if [[ "$candidate" == *"\"package\":\"${package}\""* ]]; then
      row="$candidate"
      row_count=$((row_count + 1))
    fi
  done <<<"$rows"
  [[ "$row_count" -eq 1 && "$row" == *'"resolved_target":{'* ]] || return 1

  target_version="$(
    printf '%s\n' "$row" |
      sed -n 's/.*"resolved_target":{"version":"\([^"]*\)".*/\1/p'
  )"
  [[ "$row" == *'"artifacts":['* &&
    "$row" == *'],"deployment_assets":'* ]] || return 1
  artifacts="$(
    printf '%s\n' "$row" |
      sed -n 's/.*"artifacts":\[\(.*\)\],"deployment_assets":.*/\1/p'
  )"
  [[ -n "$target_version" ]] || return 1

  variant_fragment='"variant":null'
  if [[ -n "$requested_variant" ]]; then
    variant_fragment="\"variant\":\"${requested_variant}\""
  fi

  while IFS= read -r candidate; do
    if [[ "$candidate" == *"\"platform\":\"${target_platform}\""* &&
      "$candidate" == *"\"arch\":\"${target_arch}\""* &&
      "$candidate" == *"\"format\":\"${target_format}\""* &&
      "$candidate" == *"$variant_fragment"* ]]; then
      artifact="$candidate"
      artifact_count=$((artifact_count + 1))
    fi
  done < <(printf '%s\n' "$artifacts" | awk '{gsub(/\},\{/, "}\n{"); print}')
  [[ "$artifact_count" -gt 0 ]] || return 2
  [[ "$artifact_count" -eq 1 ]] || return 1

  target_filename="$(extract_json_string "$artifact" "filename")"
  target_sha256="$(extract_json_string "$artifact" "sha256")"
  target_size="$(extract_json_integer "$artifact" "size_bytes")"
  [[ -n "$target_filename" && -n "$target_sha256" && -n "$target_size" ]] ||
    return 1
  printf '%s\t%s\t%s\t%s\n' \
    "$target_version" "$target_filename" "$target_sha256" "$target_size"
}

resolve_target() {
  local input_path="$1"
  local fields=""
  local parse_status=0

  if [[ "$target_platform" == "macos" ]]; then
    if fields="$(parse_target_macos "$input_path")"; then
      :
    else
      parse_status=$?
    fi
  elif command -v python3 >/dev/null 2>&1 &&
    python3 -c "" >/dev/null 2>&1; then
    if fields="$(parse_target_python "$input_path" "$target_variant" 2>/dev/null)"; then
      :
    else
      parse_status=$?
    fi
  else
    if fields="$(parse_target_portable "$input_path" "$target_variant")"; then
      :
    else
      parse_status=$?
    fi
  fi

  if [[ "$parse_status" -ne 0 ]]; then
    if [[ "$parse_status" -eq 2 && -n "$target_variant" ]]; then
      die "no compatible legacy Linux installer is available; see ${LINUX_LEGACY_DOCS_URL}"
    fi
    die "the backend returned an invalid or unavailable ${package} target"
  fi

  IFS=$'\t' read -r target_version target_filename target_sha256 target_size <<<"$fields"
  validate_target_fields
}

validate_target_fields() {
  [[ "$target_version" =~ ^v?[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$ ]] ||
    die "the backend returned an unsafe package version"
  [[ "$target_filename" =~ ^[A-Za-z0-9][A-Za-z0-9._+-]{0,254}$ &&
    "$target_filename" != "." && "$target_filename" != ".." ]] ||
    die "the backend returned an unsafe installer filename"
  [[ "$target_sha256" =~ ^[A-Fa-f0-9]{64}$ ]] ||
    die "the backend returned an invalid installer checksum"
  [[ "$target_size" =~ ^[0-9]+$ &&
    "$target_size" -gt 0 &&
    "$target_size" -le "$MAX_INSTALLER_BYTES" ]] ||
    die "the backend returned an invalid installer size"
}

version_supports_macos_setup() {
  local version="${1#v}"
  local without_build="${version%%+*}"
  local core="${without_build%%-*}"
  local prerelease=0
  local major minor patch extra
  [[ "$without_build" == "$core" ]] || prerelease=1
  IFS=. read -r major minor patch extra <<<"$core"
  [[ -z "${extra:-}" &&
    "$major" =~ ^[0-9]+$ &&
    "$minor" =~ ^[0-9]+$ &&
    "$patch" =~ ^[0-9]+$ ]] || return 1

  if ((major > 0)); then
    return 0
  fi
  if ((minor > 29)); then
    return 0
  fi
  if ((minor < 29 || patch < 15)); then
    return 1
  fi
  if ((patch > 15)); then
    return 0
  fi
  ((prerelease == 0))
}

download_artifact() {
  local output_path="$1"
  local headers_path="$2"
  local http_status
  echo "Downloading ${target_filename}..."
  if ! http_status="$(
    curl \
      --silent \
      --show-error \
      --connect-timeout 15 \
      --max-time 900 \
      --max-filesize "$MAX_INSTALLER_BYTES" \
      --header "x-runlayer-api-key: ${org_api_key}" \
      --header "Accept-Encoding: identity" \
      --dump-header "$headers_path" \
      --output "$output_path" \
      --write-out "%{http_code}" \
      "${host}/api/v1/binary-packages/${package}/${target_version}/${target_filename}"
  )"; then
    die "installer download failed"
  fi

  case "$http_status" in
    200) ;;
    401 | 403)
      die "the organization API key is invalid or cannot download this package"
      ;;
    404)
      die "the selected installer is no longer available; refresh the setup guide"
      ;;
    409)
      die "the selected installer is not cached yet; retry in a minute"
      ;;
    503)
      die "binary package downloads are not configured on this Runlayer instance"
      ;;
    *)
      die "installer download failed with HTTP ${http_status}"
      ;;
  esac

  local header_sha expected_sha
  header_sha="$(
    awk -F': *' '
      tolower($1) == "x-runlayer-sha256" {
        gsub("\r", "", $2)
        value = tolower($2)
      }
      END { print value }
    ' "$headers_path"
  )"
  expected_sha="$(printf '%s' "$target_sha256" | tr '[:upper:]' '[:lower:]')"
  [[ "$header_sha" == "$expected_sha" ]] ||
    die "the installer checksum header does not match the selected target"

  verify_artifact_file "$output_path"
}

verify_artifact_file() {
  local artifact_path="$1"
  local actual_size actual_sha expected_sha
  actual_size="$(wc -c <"$artifact_path" | tr -d '[:space:]')"
  [[ "$actual_size" == "$target_size" ]] ||
    die "the downloaded installer size does not match the selected target"

  if command -v sha256sum >/dev/null 2>&1; then
    actual_sha="$(sha256sum "$artifact_path" | awk '{print tolower($1)}')"
  elif command -v shasum >/dev/null 2>&1; then
    actual_sha="$(shasum -a 256 "$artifact_path" | awk '{print tolower($1)}')"
  else
    die "sha256sum or shasum is required to verify the installer"
  fi
  expected_sha="$(printf '%s' "$target_sha256" | tr '[:upper:]' '[:lower:]')"
  [[ "$actual_sha" == "$expected_sha" ]] ||
    die "the downloaded installer checksum does not match the selected target"
}

stage_artifact_for_install() {
  local source_path="$1"
  privileged_temp_dir="$(
    sudo /usr/bin/mktemp -d "/var/tmp/runlayer-install.XXXXXX"
  )" || die "could not create protected installer staging"
  [[ -n "$privileged_temp_dir" && "$privileged_temp_dir" != *$'\n'* ]] ||
    die "could not create protected installer staging"
  sudo /bin/chmod 0755 "$privileged_temp_dir"
  privileged_artifact_path="${privileged_temp_dir}/${target_filename}"
  sudo /usr/bin/install -m 0644 "$source_path" "$privileged_artifact_path"
  verify_artifact_file "$privileged_artifact_path"
}

verify_macos_package_identity() {
  local artifact_path="$1"
  local inspection_dir="${temp_dir}/expanded-package"
  local package_info_path="" candidate
  local package_id package_version package_arch expected_package_id
  pkgutil --expand "$artifact_path" "$inspection_dir" ||
    die "could not read the macOS package metadata"

  for candidate in \
    "$inspection_dir"/PackageInfo \
    "$inspection_dir"/*/PackageInfo; do
    [[ -f "$candidate" ]] || continue
    [[ -z "$package_info_path" ]] ||
      die "the installer has an unexpected macOS package identity"
    package_info_path="$candidate"
  done
  [[ -n "$package_info_path" && -f "$inspection_dir/Distribution" ]] ||
    die "the installer has an unexpected macOS package identity"

  package_id="$(
    "$XMLLINT_BIN" --xpath \
      'string(/*[local-name()="pkg-info"]/@identifier)' \
      "$package_info_path"
  )" || die "could not read the macOS package identifier"
  package_version="$(
    "$XMLLINT_BIN" --xpath \
      'string(/*[local-name()="pkg-info"]/@version)' \
      "$package_info_path"
  )" || die "could not read the macOS package version"
  package_arch="$(
    "$XMLLINT_BIN" --xpath \
      'string(//*[local-name()="options"]/@hostArchitectures)' \
      "$inspection_dir/Distribution"
  )" || die "could not read the macOS package architecture"

  if [[ "$package" == "cli" ]]; then
    expected_package_id="com.runlayer.cli"
  else
    expected_package_id="com.runlayer.aiwatch"
  fi
  [[ "$package_id" == "$expected_package_id" &&
    "$package_version" == "${target_version#v}" &&
    "$package_arch" == "$target_arch" ]] ||
    die "the installer has an unexpected macOS package identity"
}

install_macos() {
  local artifact_path="$1"
  local signature_output assessment_output
  signature_output="$(pkgutil --check-signature "$artifact_path" 2>&1)" ||
    die "the macOS package signature is invalid"
  if ! printf '%s\n' "$signature_output" |
    grep -Eq "Developer ID Installer:.*\\(${MACOS_TEAM_ID}\\)"; then
    die "the macOS package is not signed by Runlayer team ${MACOS_TEAM_ID}"
  fi

  assessment_output="$(spctl --assess --type install --verbose=4 "$artifact_path" 2>&1)" ||
    die "the macOS package did not pass Gatekeeper assessment"
  if ! printf '%s\n' "$assessment_output" |
    grep -Eq 'source=Notarized Developer ID'; then
    die "the macOS package is not notarized"
  fi
  verify_macos_package_identity "$artifact_path"

  echo "Installing and configuring ${package}..."
  sudo /usr/sbin/installer -pkg "$artifact_path" -target /
  if [[ "$package" == "cli" ]]; then
    sudo /usr/local/bin/runlayer setup config \
      --host "$host" \
      --org-api-key "$org_api_key"
    # The update daemon deliberately has no RunAtLoad (a first fire inside
    # the pkg postinstall could stage a nested installer); the transaction
    # is closed here, so kick the first update check now. Best-effort: the
    # hourly StartInterval covers any failure.
    echo "Triggering the first update check..."
    sudo launchctl kickstart system/com.runlayer.cli.update ||
      echo "warning: could not trigger the update check now;" \
        "the hourly schedule will run it instead" >&2
  else
    sudo /usr/local/bin/aiwatch setup config \
      --host "$host" \
      --org-api-key "$org_api_key"
  fi
}

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  printf '%s' "$value"
}

linux_package_name() {
  if [[ "$package" == "cli" ]]; then
    printf '%s' "runlayer"
  else
    printf '%s' "runlayer-aiwatch"
  fi
}

verify_linux_package_identity() {
  local artifact_path="$1"
  local package_name package_version package_arch expected_arch expected_name
  package_version="${target_version#v}"
  expected_name="$(linux_package_name)"

  if [[ "$target_format" == "deb" ]]; then
    command -v dpkg-deb >/dev/null 2>&1 ||
      die "dpkg-deb is required to verify the selected .deb package"
    package_name="$(dpkg-deb --field "$artifact_path" Package)" ||
      die "could not read the selected .deb package metadata"
    local actual_version
    actual_version="$(dpkg-deb --field "$artifact_path" Version)" ||
      die "could not read the selected .deb package metadata"
    package_arch="$(dpkg-deb --field "$artifact_path" Architecture)" ||
      die "could not read the selected .deb package metadata"
    [[ "$target_arch" == "x86_64" ]] && expected_arch="amd64" ||
      expected_arch="arm64"
    [[ "$package_name" == "$expected_name" &&
      "$actual_version" == "$package_version" &&
      "$package_arch" == "$expected_arch" ]] ||
      die "the installer has an unexpected Linux package identity"
  else
    local rpm_metadata
    rpm_metadata="$(
      rpm -qp --queryformat $'%{NAME}\t%{VERSION}\t%{ARCH}\n' "$artifact_path"
    )" || die "could not read the selected RPM package metadata"
    IFS=$'\t' read -r package_name package_version package_arch <<<"$rpm_metadata"
    [[ "$target_arch" == "x86_64" ]] && expected_arch="x86_64" ||
      expected_arch="aarch64"
    [[ "$package_name" == "$expected_name" &&
      "$package_version" == "${target_version#v}" &&
      "$package_arch" == "$expected_arch" ]] ||
      die "the installer has an unexpected Linux package identity"
  fi
}

require_installed_deb_package() {
  local query_output status installed_version
  query_output="$(
    dpkg-query --show \
      --showformat '${Status}\t${Version}' "$(linux_package_name)" 2>/dev/null
  )" || die "the selected .deb package did not finish installing"
  status="${query_output%%$'\t'*}"
  installed_version="${query_output#*$'\t'}"
  [[ "$status" == "install ok installed" &&
    "$installed_version" == "${target_version#v}" ]] ||
    die "the selected .deb package did not finish installing"
}

install_linux() {
  local artifact_path="$1"
  verify_linux_package_identity "$artifact_path"
  if [[ "$package" == "cli" ]]; then
    echo "Installing and configuring the Runlayer CLI..."
  else
    echo "Installing and configuring AI Watch Detect..."
  fi
  if [[ "$target_format" == "deb" ]]; then
    command -v apt-get >/dev/null 2>&1 ||
      die "apt-get is required to install the selected .deb package"
    if [[ -n "$target_variant" ]]; then
      # Legacy-distro apt-get predates local .deb installs, so dpkg unpacks
      # the package and apt-get -f completes dependency configuration. apt-get
      # -f can exit 0 without repairing other dpkg failures, so verify the
      # package really reached the installed state before continuing.
      if ! sudo dpkg -i "$artifact_path"; then
        sudo apt-get install -f -y ||
          die "the selected .deb package did not finish installing"
        require_installed_deb_package
      fi
    else
      sudo apt-get install -y "$artifact_path"
    fi
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y "$artifact_path"
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y "$artifact_path"
  else
    sudo rpm -U "$artifact_path"
  fi

  local escaped_host config_path credentials_path
  escaped_host="$(json_escape "$host")"
  config_path="${temp_dir}/config.json"
  credentials_path="${temp_dir}/credentials"
  printf '{\n  "Host": "%s"\n}\n' "$escaped_host" >"$config_path"
  printf 'RUNLAYER_API_KEY=%s\n' "$org_api_key" >"$credentials_path"
  chmod 600 "$credentials_path"

  # Shared config paths by design: the Linux CLI runtime and both cron wrappers
  # read /etc/runlayer/aiwatch/{config.json,credentials}, the same files AI
  # Watch uses. Neither package owns them. Linux needs no CLI min-version gate:
  # this script writes the config files the runtime reads, so there is no
  # silent-drop failure mode (unlike Windows, where older MSIs ignore the
  # tenant properties — gated in install.ps1).
  sudo install -d -m 755 /etc/runlayer/aiwatch
  sudo install -m 644 "$config_path" /etc/runlayer/aiwatch/config.json
  sudo install -m 600 "$credentials_path" /etc/runlayer/aiwatch/credentials

  if [[ "$package" == "cli" ]] &&
    sudo test -x /usr/lib/runlayer/run-cli-update.sh; then
    echo "Triggering the first update check..."
    sudo /usr/lib/runlayer/run-cli-update.sh ||
      echo "warning: could not trigger the update check now;" \
        "the hourly cron schedule will run it instead" >&2
  fi
}

main() {
  parse_args "$@"
  command -v curl >/dev/null 2>&1 || die "curl is required"
  detect_target_slot

  temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/runlayer-install.XXXXXX")"
  local targets_path="${temp_dir}/targets.json"
  local headers_path="${temp_dir}/headers"
  local artifact_path="${temp_dir}/installer.${target_format}"
  fetch_targets "$targets_path"
  resolve_target "$targets_path"
  if [[ "$target_platform" == "macos" ]] &&
    ! version_supports_macos_setup "$target_version"; then
    die "one-command setup requires package version ${MACOS_MIN_VERSION} or newer; use the manual flow at ${DOCS_URL}"
  fi
  download_artifact "$artifact_path" "$headers_path"
  stage_artifact_for_install "$artifact_path"
  artifact_path="$privileged_artifact_path"

  if [[ "$target_platform" == "macos" ]]; then
    install_macos "$artifact_path"
  else
    install_linux "$artifact_path"
  fi

  if [[ "$package" == "cli" ]]; then
    echo "Runlayer CLI installed successfully."
  else
    echo "Runlayer AI Watch installed successfully."
  fi
}

main "$@"
