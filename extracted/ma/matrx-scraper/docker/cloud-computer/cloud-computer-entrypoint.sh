#!/usr/bin/env bash
set -euo pipefail

# Cloud Computer root step, then the ordinary browser-worker entrypoint.
#
# The person's home (/home/browser-worker) is their own EFS access point. The
# Chrome profile root lives INSIDE that home, so one access point carries home
# and browser data and no machine ever mounts the shared browser-profiles volume.
if [[ "$(id -u)" == "0" ]]; then
  home_dir="/home/browser-worker"
  install -d -m 0750 -o browser-worker -g browser-worker "${home_dir}"
  runuser --user browser-worker -- install -d -m 0700 "${home_dir}/.matrx" "${home_dir}/.matrx/profiles"
  runuser --user browser-worker -- install -d -m 0755 "${home_dir}/Desktop" "${home_dir}/Documents" "${home_dir}/Downloads"
  if [[ -d /profiles && ! -L /profiles ]] && ! mountpoint -q /profiles; then
    rmdir /profiles 2>/dev/null || rm -rf /profiles
  fi
  [[ -L /profiles ]] || ln -s "${home_dir}/.matrx/profiles" /profiles
fi

exec /usr/local/bin/browser-worker-entrypoint "$@"
