#!/usr/bin/env bash
set -euo pipefail

# Cloud Computer root step, then the ordinary browser-worker entrypoint.
#
# The person's home (/home/browser-worker) is their own EFS access point. The
# Chrome profile root lives INSIDE that home, so one access point carries home
# and browser data and no machine ever mounts the shared browser-profiles volume.
# Read the boot files ahead, in parallel, while the steps below run (the image
# is lazily loaded; see the Dockerfile). Only warms the page cache.
boot_files=/usr/local/share/cloud-computer/boot-files
# Then what the first picture waits on (Chrome, the Playwright driver, the
# stream page): read after the boot files so the worker's imports go first.
open_files=/usr/local/share/cloud-computer/open-files
{
  if [[ -r "${boot_files}" ]]; then
    tr '\n' '\0' < "${boot_files}" | xargs -0 -P 16 -n 32 cat >/dev/null 2>&1 || true
  fi
  if [[ -r "${open_files}" ]]; then
    tr '\n' '\0' < "${open_files}" | xargs -0 -P 16 -n 16 cat >/dev/null 2>&1 || true
  fi
} &

if [[ "$(id -u)" == "0" ]]; then
  home_dir="/home/browser-worker"
  install -d -m 0750 -o browser-worker -g browser-worker "${home_dir}"
  runuser --user browser-worker -- install -d -m 0700 "${home_dir}/.matrx" "${home_dir}/.matrx/profiles"
  runuser --user browser-worker -- install -d -m 0755 "${home_dir}/Desktop" "${home_dir}/Documents" "${home_dir}/Downloads"
  if [[ -d /profiles && ! -L /profiles ]] && ! mountpoint -q /profiles; then
    rmdir /profiles 2>/dev/null || rm -rf /profiles
  fi
  [[ -L /profiles ]] || ln -s "${home_dir}/.matrx/profiles" /profiles
  # Upgrades keep everything (ruling 16): the root is new on every task, so the
  # person's recorded system installs are replayed now, in the background (the
  # desktop and Chrome do not wait; progress: cloud-computer-software status).
  install -d -m 0755 /run/cloud-computer
  if [[ -x /usr/local/bin/cloud-computer-software ]]; then
    /usr/local/bin/cloud-computer-software replay >/dev/null 2>&1 &
  fi
fi

exec /usr/local/bin/browser-worker-entrypoint "$@"
