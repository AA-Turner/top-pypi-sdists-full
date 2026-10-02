#!/usr/bin/env bash
# ==============================================================================
# install_pikobs_web_workstation.sh — install ONLY the workstation launcher
# ------------------------------------------------------------------------------
# Run from the WORKSTATION (the shell that shows bash-5.1$), not from PPP7.
# The full Pikobs + env + server installation must already exist on PPP7.
#
# This script:
#   1. asks for CMC user and PPP host;
#   2. connects to PPP7;
#   3. finds ~/pikobs_install/pikobs_web (canonical server symlink layout);
#   4. fetches install-client.sh;
#   5. installs ~/bin/pikobs-web locally;
#   6. exports ~/bin into THIS shell when invoked with `source`;
#   7. starts Pikobs Web unless --no-open is requested.
#
# It does NOT install Conda/Pikobs/FastAPI and does NOT modify ~/.profile.
# ==============================================================================

_pikobs_ws_main() {
    local remote_user="${PIKOBS_WEB_USER:-${USER:-}}"
    local remote_host="${PIKOBS_WEB_HOST:-ppp7}"
    local remote_app_dir="${PIKOBS_WEB_REMOTE_DIR:-}"
    local auto_yes=0 open_after=1
    local target check_line actual_login remote_probe local_tmp

    _ws_error() { echo "ERROR: $*" >&2; return 1; }
    _ws_need() { command -v "$1" >/dev/null 2>&1 || { _ws_error "required workstation command not found: $1"; return 1; }; }
    _ws_prompt() {
        local __name="$1" __label="$2" __default="$3" __reply=""
        if [[ "$auto_yes" == "1" ]]; then
            printf -v "$__name" '%s' "$__default"
            return 0
        fi
        [[ -r /dev/tty ]] || { _ws_error "interactive input unavailable; pass explicit options with --yes"; return 1; }
        read -r -p "${__label} [${__default}]: " __reply </dev/tty || return 1
        printf -v "$__name" '%s' "${__reply:-$__default}"
    }

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --user) remote_user="$2"; shift 2 ;;
            --host) remote_host="$2"; shift 2 ;;
            --remote-dir) remote_app_dir="$2"; shift 2 ;;
            --no-open) open_after=0; shift ;;
            --yes|-y) auto_yes=1; shift ;;
            -h|--help)
                cat <<'USAGE'
Usage:
  source <(curl -fsSL URL/install_pikobs_web_workstation.sh)

Options:
  --user USER
  --host HOST
  --remote-dir DIR
  --no-open
  --yes, -y
USAGE
                return 0 ;;
            *) _ws_error "unknown argument: $1"; return 2 ;;
        esac
    done

    _ws_need ssh || return 1
    _ws_need scp || return 1

    [[ -n "$remote_user" ]] || remote_user="$(id -un 2>/dev/null || true)"
    _ws_prompt remote_user "CMC username" "$remote_user" || return 1
    _ws_prompt remote_host "PPP login host" "$remote_host" || return 1
    target="${remote_user}@${remote_host}"

    echo
    echo "Checking ${target}..."
    check_line="$(ssh -4 -T -o ConnectTimeout=15 "$target" 'printf "PIKOBS_WS_OK\t%s\n" "$(hostname -s)"' 2>&1)" || {
        printf '%s\n' "$check_line" >&2
        _ws_error "cannot connect to ${target}"
        return 1
    }
    actual_login="$(printf '%s\n' "$check_line" | awk -F '\t' '$1=="PIKOBS_WS_OK" {print $2; exit}')"
    [[ -n "$actual_login" ]] && echo "Connected to ${actual_login}."

    if [[ -z "$remote_app_dir" ]]; then
        remote_probe="$(ssh -4 -T "$target" 'bash -s' <<'REMOTE'
for d in \
    "$HOME/pikobs_install/pikobs_web" \
    "$HOME/sites8/pikobs_install/pikobs_web" \
    "$HOME/sites8/pikobs_web"
do
    if [[ -x "$d/pikobs-web" && -f "$d/install-client.sh" && -x "$d/pikobs-web-client" ]]; then
        printf '%s\n' "$d"
        exit 0
    fi
done
exit 1
REMOTE
)" || true
        remote_app_dir="$remote_probe"
    fi

    if [[ -z "$remote_app_dir" ]]; then
        cat >&2 <<EOF
ERROR: Pikobs Web is not installed on PPP7 yet.

First, on PPP7 run the full installation:
  ssh ${target}
  cd /path/to/Pikobs
  ./pikobs/script/setup_pikobs.sh

Then rerun this workstation installer.
EOF
        return 1
    fi

    case "$remote_app_dir" in /*) ;; *) _ws_error "remote app path is not absolute: $remote_app_dir"; return 1 ;; esac
    echo "Remote Pikobs Web: ${remote_app_dir}"

    local_tmp="$(mktemp "${TMPDIR:-/tmp}/pikobs-install-client.XXXXXX")" || {
        _ws_error "cannot create temporary file"; return 1;
    }
    if ! scp -q "${target}:${remote_app_dir}/install-client.sh" "$local_tmp"; then
        rm -f "$local_tmp"
        _ws_error "could not fetch install-client.sh from PPP7"
        return 1
    fi
    chmod 700 "$local_tmp"
    if ! bash "$local_tmp" --user "$remote_user" --host "$remote_host" --remote-dir "$remote_app_dir"; then
        rm -f "$local_tmp"
        _ws_error "workstation client installation failed"
        return 1
    fi
    rm -f "$local_tmp"

    # Immediate availability in the current shell. This script is intended to
    # be sourced, so this export survives after it returns.
    case ":$PATH:" in
        *":$HOME/bin:"*) ;;
        *) export PATH="$HOME/bin:$PATH" ;;
    esac
    hash -r 2>/dev/null || true
    [[ -x "$HOME/bin/pikobs-web" ]] || {
        _ws_error "installation finished but $HOME/bin/pikobs-web is missing"
        return 1
    }
    command -v pikobs-web >/dev/null 2>&1 || {
        _ws_error "launcher exists but is not available in the current shell"
        return 1
    }

    echo
    echo "============================================================"
    echo "✅ Workstation launcher installed."
    echo "  Command : $HOME/bin/pikobs-web"
    echo "  PPP     : ${target}"
    echo "  Server  : ${remote_app_dir}"
    echo "============================================================"

    if [[ "$open_after" == "1" ]]; then
        echo
        echo "Starting Pikobs Web..."
        "$HOME/bin/pikobs-web" || { _ws_error "pikobs-web was installed but failed to start"; return 1; }
    fi
    return 0
}

_pikobs_ws_main "$@"
_pikobs_ws_rc=$?
unset -f _pikobs_ws_main 2>/dev/null || true
return "$_pikobs_ws_rc" 2>/dev/null || exit "$_pikobs_ws_rc"
