#!/usr/bin/env bash
# Installed software survives every new task (owner ruling 16, "Upgrades keep
# everything"). The container root is ephemeral: anything installed with apt or
# into a system path is gone on EVERY new task, not only after an upgrade. So the
# person's (or an agent's) system installs are RECORDED into their home (EFS,
# persists) and REPLAYED at wake.
#
#   record   (root) after every apt/dpkg run (apt hook) and at save-before-stop:
#            - apt: manually installed packages that the image does not ship
#            - files: new files under /etc/apt (sources, keys), /usr/share/keyrings,
#              /usr/local and /opt that neither the image nor a recorded package owns
#   replay   (root) at wake: restore those files, then apt-get install the list.
#            Honest progress in /run/cloud-computer/software.json and the log.
#   status   print the progress file.
#
# The build's own lists: /usr/local/share/cloud-computer/image-packages.txt and
# image-files.txt (written at image build). User-level installs (pip --user,
# npm prefix, ~/.local) already live in the home and need nothing here.
set -uo pipefail

home_dir="${CLOUD_COMPUTER_HOME:-/home/browser-worker}"
system_dir="${home_dir}/.matrx/system"
files_root="${system_dir}/root"
package_list="${system_dir}/apt-packages.txt"
pending_list="${system_dir}/apt-pending.txt"
share_dir="${CLOUD_COMPUTER_SHARE:-/usr/local/share/cloud-computer}"
image_packages="${share_dir}/image-packages.txt"
image_files="${share_dir}/image-files.txt"
run_dir="${CLOUD_COMPUTER_RUN:-/run/cloud-computer}"
status_file="${run_dir}/software.json"
replay_lock="${run_dir}/software-replaying"
log_file="${run_dir}/software.log"
tracked_roots=(/etc/apt /usr/share/keyrings /usr/local /opt)

log() { echo "cloud-computer-software: $*" | tee -a "${log_file}" >&2; }

write_status() { # state total done failed message
  local tmp="${status_file}.tmp"
  printf '{"state":"%s","packages_total":%s,"packages_done":%s,"packages_failed":%s,"message":"%s","epoch_ms":%s}\n' \
    "$1" "$2" "$3" "$4" "$5" "$(date +%s%3N)" > "${tmp}" && mv -f "${tmp}" "${status_file}"
  chmod 0644 "${status_file}" 2>/dev/null || true
}

own_home_record() { chown -R browser-worker:browser-worker "${system_dir}" 2>/dev/null || true; }

current_packages() { apt-mark showmanual 2>/dev/null | sort -u; }

owned_by_packages() { # files that the given packages' dpkg lists own
  local pkg
  while read -r pkg; do
    [[ -n "${pkg}" ]] || continue
    cat "/var/lib/dpkg/info/${pkg}.list" "/var/lib/dpkg/info/${pkg}:"*.list 2>/dev/null
  done | sort -u
}

current_files() {
  find "${tracked_roots[@]}" -xdev \( -type f -o -type l \) 2>/dev/null \
    | grep -v -e '^/usr/local/share/cloud-computer/' -e '^/etc/apt/apt.conf.d/90-cloud-computer' -e '/__pycache__/' | sort -u
}

record() {
  if [[ -e "${replay_lock}" ]]; then
    log "record skipped: a replay is running"
    return 0
  fi
  mkdir -p "${system_dir}" "${files_root}"
  local packages tmp
  packages="$(mktemp)"; tmp="$(mktemp)"
  if [[ -r "${image_packages}" ]]; then
    comm -13 "${image_packages}" <(current_packages) > "${packages}"
  else
    log "no image package list; recording nothing for apt"
    : > "${packages}"
  fi
  # A package that failed to replay is still the person's: keep it recorded so
  # the next wake tries again (never silently forgotten).
  if [[ -s "${pending_list}" ]]; then
    cat "${pending_list}" >> "${packages}"
  fi
  sort -u "${packages}" -o "${packages}"
  mv -f "${packages}" "${package_list}"
  # Files: new under the tracked roots, minus the image's and the recorded packages'.
  local owned wanted
  owned="$(mktemp)"; wanted="$(mktemp)"
  owned_by_packages < "${package_list}" > "${owned}"
  if [[ -r "${image_files}" ]]; then
    comm -23 <(current_files) "${image_files}" | comm -23 - "${owned}" > "${wanted}"
  else
    : > "${wanted}"
  fi
  if [[ -s "${wanted}" ]]; then
    rsync -a --files-from="${wanted}" / "${files_root}/" 2>>"${log_file}" || log "some files could not be recorded"
  fi
  # Drop recorded files that are gone from the machine (the person removed them).
  (cd "${files_root}" && find . \( -type f -o -type l \) | sed 's#^\.##' | sort -u) > "${tmp}"
  comm -23 "${tmp}" "${wanted}" | while read -r gone; do rm -f "${files_root}${gone}"; done
  cp -f "${wanted}" "${system_dir}/files.txt"
  # The home's network drive keeps file contents but maps owner and mode to the
  # person's user, so record each system file's own owner and mode to put back.
  tr '\n' '\0' < "${wanted}" | xargs -0 -r stat -c '%a %U %G %n' 2>/dev/null > "${system_dir}/modes.txt" || true
  rm -f "${owned}" "${wanted}" "${tmp}"
  own_home_record
  log "recorded $(wc -l < "${package_list}") package(s), $(wc -l < "${system_dir}/files.txt") file(s)"
}

replay() {
  mkdir -p "${run_dir}"
  chmod 0755 "${run_dir}"
  touch "${replay_lock}"
  local total=0 done=0 failed=0
  [[ -s "${package_list}" ]] && total="$(wc -l < "${package_list}" | tr -d ' ')"
  if [[ "${total}" == "0" && ! -d "${files_root}" ]]; then
    rm -f "${replay_lock}"
    write_status done 0 0 0 "nothing to restore"
    return 0
  fi
  write_status replaying "${total}" 0 0 "restoring your installed software"
  if [[ -d "${files_root}" ]]; then
    rsync -a "${files_root}/" / 2>>"${log_file}" || log "some recorded files could not be restored"
    if [[ -s "${system_dir}/modes.txt" ]]; then
      while read -r mode owner group path; do
        [[ -e "${path}" ]] || continue
        chown "${owner}:${group}" "${path}" 2>/dev/null; chmod "${mode}" "${path}" 2>/dev/null
      done < "${system_dir}/modes.txt"
    fi
  fi
  : > "${pending_list}.new"
  if [[ "${total}" != "0" ]]; then
    write_status replaying "${total}" 0 0 "updating package lists"
    DEBIAN_FRONTEND=noninteractive apt-get update >>"${log_file}" 2>&1 || log "apt-get update failed"
    # shellcheck disable=SC2046
    if DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
         $(cat "${package_list}") >>"${log_file}" 2>&1; then
      done="${total}"
    else
      # One by one, so one unavailable package never loses the rest.
      local pkg
      while read -r pkg; do
        [[ -n "${pkg}" ]] || continue
        if DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${pkg}" >>"${log_file}" 2>&1; then
          done=$((done + 1))
        else
          failed=$((failed + 1)); echo "${pkg}" >> "${pending_list}.new"
          log "could not reinstall ${pkg}"
        fi
        write_status replaying "${total}" "${done}" "${failed}" "reinstalling your software"
      done < "${package_list}"
    fi
    apt-mark manual $(cat "${package_list}") >/dev/null 2>&1 || true
  fi
  mv -f "${pending_list}.new" "${pending_list}"
  rm -f "${replay_lock}"
  if [[ "${failed}" == "0" ]]; then
    write_status done "${total}" "${done}" 0 "your installed software is back"
  else
    write_status partial "${total}" "${done}" "${failed}" "some software could not be reinstalled; see ${log_file}"
  fi
  record
  log "replay finished: ${done}/${total} package(s), ${failed} failed"
}

case "${1:-}" in
  record) mkdir -p "${run_dir}"; record ;;
  replay) replay ;;
  status) cat "${status_file}" 2>/dev/null || echo '{"state":"unknown"}' ;;
  *) echo "usage: $0 record|replay|status" >&2; exit 2 ;;
esac
