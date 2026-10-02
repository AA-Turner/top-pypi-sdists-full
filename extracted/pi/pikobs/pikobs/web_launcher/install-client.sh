#!/usr/bin/env bash
# Install the small Pikobs Web command on the WORKSTATION.
# This script never installs Pikobs, Conda, FastAPI or the server application.
set -euo pipefail

REMOTE_HOST="${PIKOBS_WEB_HOST:-ppp7}"
REMOTE_USER="${PIKOBS_WEB_USER:-$USER}"
REMOTE_APP_DIR="${PIKOBS_WEB_REMOTE_DIR:-$HOME/pikobs_install/pikobs_web}"
BIN_DIR="${HOME}/bin"
CACHE_DIR="${HOME}/.local/share/pikobs-web"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --host) REMOTE_HOST="$2"; shift 2 ;;
        --user) REMOTE_USER="$2"; shift 2 ;;
        --remote-dir) REMOTE_APP_DIR="$2"; shift 2 ;;
        -h|--help)
            cat <<USAGE
Usage: install-client.sh [--host HOST] [--user USER] [--remote-dir ABS_PATH]

Installs only ~/bin/pikobs-web on this workstation. The command refreshes the
real client from PPP7 before every launch. The Pikobs environment and web
server must already have been installed on PPP7 by setup_pikobs.sh.
USAGE
            exit 0 ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

[[ "$REMOTE_APP_DIR" == /* ]] || {
    echo "ERROR: --remote-dir must be an absolute path on PPP7." >&2
    exit 2
}
command -v ssh >/dev/null 2>&1 || { echo "ERROR: ssh is required." >&2; exit 1; }
command -v scp >/dev/null 2>&1 || { echo "ERROR: scp is required." >&2; exit 1; }

mkdir -p "$BIN_DIR" "$CACHE_DIR"
chmod 700 "$CACHE_DIR"

cat > "$BIN_DIR/pikobs-web" <<EOF_WRAPPER
#!/usr/bin/env bash
set -euo pipefail
REMOTE_HOST=$(printf '%q' "$REMOTE_HOST")
REMOTE_USER=$(printf '%q' "$REMOTE_USER")
REMOTE_APP_DIR=$(printf '%q' "$REMOTE_APP_DIR")
CACHE_DIR="\$HOME/.local/share/pikobs-web"
CLIENT="\$CACHE_DIR/pikobs-web-client"
TMP="\$CACHE_DIR/.pikobs-web-client.tmp.\$\$"
mkdir -p "\$CACHE_DIR"
chmod 700 "\$CACHE_DIR"
REMOTE_FILE="\${REMOTE_APP_DIR%/}/pikobs-web-client"

if scp -q "\${REMOTE_USER}@\${REMOTE_HOST}:\${REMOTE_FILE}" "\$TMP"; then
    chmod 700 "\$TMP"
    mv -f "\$TMP" "\$CLIENT"
else
    rm -f "\$TMP"
    if [[ ! -x "\$CLIENT" ]]; then
        echo "ERROR: could not fetch Pikobs Web client from \${REMOTE_USER}@\${REMOTE_HOST}." >&2
        echo "       Run setup_pikobs.sh on PPP7 first." >&2
        exit 1
    fi
    echo "WARNING: using cached Pikobs Web client (remote refresh failed)." >&2
fi

export PIKOBS_WEB_HOST="\$REMOTE_HOST"
export PIKOBS_WEB_USER="\$REMOTE_USER"
export PIKOBS_WEB_REMOTE_DIR="\$REMOTE_APP_DIR"
exec "\$CLIENT" "\$@"
EOF_WRAPPER
chmod 700 "$BIN_DIR/pikobs-web"

# Keep ~/bin as the canonical location. If this workstation does not include
# ~/bin in PATH, also expose the launcher through the first existing writable
# user-owned PATH directory. This avoids editing ~/.profile or ~/.bashrc.
PATH_LINK_DIR=""
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    IFS=':' read -r -a _pikobs_path_parts <<< "$PATH"
    for _pikobs_dir in "${_pikobs_path_parts[@]}"; do
        [[ -n "$_pikobs_dir" ]] || continue
        case "$_pikobs_dir" in
            "$HOME"/*)
                if [[ -d "$_pikobs_dir" && -w "$_pikobs_dir" ]]; then
                    PATH_LINK_DIR="$_pikobs_dir"
                    break
                fi
                ;;
        esac
    done
    if [[ -n "$PATH_LINK_DIR" && "$PATH_LINK_DIR" != "$BIN_DIR" ]]; then
        ln -sfn "$BIN_DIR/pikobs-web" "$PATH_LINK_DIR/pikobs-web"
    fi
fi
unset _pikobs_path_parts _pikobs_dir 2>/dev/null || true

# Fetch once now so a wrong host/path is caught during installation.
REMOTE_FILE="${REMOTE_APP_DIR%/}/pikobs-web-client"
scp -q "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILE}" "$CACHE_DIR/pikobs-web-client"
chmod 700 "$CACHE_DIR/pikobs-web-client"

echo
echo "✅ Pikobs Web workstation command installed."
echo "   Command : $BIN_DIR/pikobs-web"
echo "   Remote  : ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_APP_DIR}"
echo
echo "This installer does NOT modify ~/.profile or any workstation environment."
if command -v pikobs-web >/dev/null 2>&1; then
    echo "Run now:"
    echo "  pikobs-web"
elif [[ -n "${PATH_LINK_DIR:-}" ]]; then
    echo "Run now:"
    echo "  ${PATH_LINK_DIR}/pikobs-web"
else
    echo "Run now with the full path:"
    echo "  $BIN_DIR/pikobs-web"
    echo "Or for this shell:"
    echo '  export PATH="$HOME/bin:$PATH"'
fi
