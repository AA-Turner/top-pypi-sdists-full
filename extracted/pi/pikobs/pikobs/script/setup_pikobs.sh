#!/usr/bin/env bash
# ==============================================================================
# setup_pikobs.sh — One-shot installer for Pikobs + Pikobs Web at CMC
# ------------------------------------------------------------------------------
# Full install:
#   1. Asks WHERE to install (default suggested; press Enter to accept).
#   2. Configures the CMC web proxy (persistent + current session).
#   3. Loads the official mamba module.
#   4. Creates $PROJECT_DIR/env from the pinned pikobs_env.yml.
#   5. Verifies/installs Pikobs in that environment.
#   6. Writes $PROJECT_DIR/load_pikobs.sh.
#   7. Maintains ~/pikobs_install -> $PROJECT_DIR when needed.
#   8. Adds load_pikobs and small maintenance commands to the PPP7 profile.
#   9. Installs/updates Pikobs Web under $PROJECT_DIR/pikobs_web.
#  10. Keeps Pikobs Web runtime state under $PROJECT_DIR/.pikobs_web.
#  11. Creates ~/pikobs_install -> $PROJECT_DIR as the stable HOME symlink.
#  12. Workstation bootstrap installs only the small local pikobs-web client.
#
# Pikobs-only package update (existing environment):
#   ./setup_pikobs.sh --update-pikobs
#
# Web-only update:
#   ./setup_pikobs.sh --web-only
#   ./setup_pikobs.sh --update-pikobs
#   # In interactive mode this ALWAYS asks where the existing Pikobs install is.
#   # The environment is expected at <install-dir>/env.
#
# This updates ONLY Pikobs Web. It does not rebuild the Conda environment,
# remove <PROJECT_DIR>/.pikobs_web, run history, or user-selected PATHWORKs.
#
# Usage:
#   wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/setup_pikobs.sh
#   chmod +x setup_pikobs.sh
#   ./setup_pikobs.sh
#   ./setup_pikobs.sh --project-dir /path/to/dir
#   ./setup_pikobs.sh --web-only
#   ./setup_pikobs.sh --project-dir /path/to/dir --web-only
#   ./setup_pikobs.sh --web-only --web-source /path/to/pikobs/web_launcher
#   PROJECT_DIR=/path/to/dir ./setup_pikobs.sh
#   PIKOBS_AUTO_INSTALL=1 ./setup_pikobs.sh
#   PIKOBS_INSTALL_WEB=0 ./setup_pikobs.sh       # full Pikobs, no web launcher
# ==============================================================================
set -euo pipefail

# Keep the installation and runtime state private to the user by default.
umask 077

SETUP_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# === USER-CONFIGURABLE ========================================================
SITE8_USER_ROOT="${PIKOBS_SITE_STORAGE_ROOT:-/fs/site8/eccc/cmd/cmda/${USER}}"
DEFAULT_PROJECT_DIR="${SITE8_USER_ROOT}/pikobs_install"
ENV_NAME="pikobs_env"
PROXY_URL="http://webproxy.science.gc.ca:8888/"
PIKOBS_ENV_YML="https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs_env.yml"
MAMBA_MODULE_LOAD="r.load.dot crd/ccrp/ssm/mamba_2026.02.18_all"

# Canonical location the run_<module>.sh scripts always source.
CANONICAL_LINK="${HOME}/pikobs_install"

# Pikobs Web source in the repository.  If setup_pikobs.sh is run from a
# checkout, that local copy is used.  If setup_pikobs.sh was downloaded alone,
# the repository archive is downloaded automatically.
PIKOBS_INSTALL_WEB="${PIKOBS_INSTALL_WEB:-1}"
PIKOBS_WEB_REF="${PIKOBS_WEB_REF:-master}"
PIKOBS_WEB_SUBDIR="pikobs/web_launcher"
PIKOBS_WEB_ARCHIVE="https://gitlab.science.gc.ca/dlo001/Pikobs/-/archive/${PIKOBS_WEB_REF}/Pikobs-${PIKOBS_WEB_REF}.tar.gz"
# ==============================================================================
PROJECT_DIR_EXPLICIT=0
if [[ -n "${PROJECT_DIR:-}" ]]; then
    PROJECT_DIR_EXPLICIT=1
fi
PROJECT_DIR="${PROJECT_DIR:-$DEFAULT_PROJECT_DIR}"
WEB_ONLY=0
UPDATE_PIKOBS=0
PIKOBS_WEB_SOURCE="${PIKOBS_WEB_SOURCE:-}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --project-dir)
            [[ $# -ge 2 ]] || { echo "--project-dir requires a path" >&2; exit 2; }
            PROJECT_DIR="$2"
            PROJECT_DIR_EXPLICIT=1
            shift 2
            ;;
        --web-only)
            WEB_ONLY=1
            shift
            ;;
        --update-pikobs)
            UPDATE_PIKOBS=1
            shift
            ;;
        --web-source)
            [[ $# -ge 2 ]] || { echo "--web-source requires a directory" >&2; exit 2; }
            PIKOBS_WEB_SOURCE="$2"
            shift 2
            ;;
        --skip-web)
            PIKOBS_INSTALL_WEB=0
            shift
            ;;
        -h|--help)
            sed -n '1,/^# ====/p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 2
            ;;
    esac
done

if [[ "${WEB_ONLY}" == "1" && "${UPDATE_PIKOBS}" == "1" ]]; then
    echo "❌ --web-only and --update-pikobs cannot be used together." >&2
    exit 2
fi

# Choose the installation directory.  In --web-only mode we never silently
# assume ~/pikobs_install: if the caller did not pass --project-dir (or the
# PROJECT_DIR environment variable), interactive mode asks explicitly.  When an
# active conda env ends in /env, its parent is offered only as a suggestion.
if [[ "${PIKOBS_AUTO_INSTALL:-0}" != "1" ]]; then
    if [[ ( "${WEB_ONLY}" == "1" || "${UPDATE_PIKOBS}" == "1" ) && "${PROJECT_DIR_EXPLICIT}" != "1" ]]; then
        _suggest="${PROJECT_DIR}"
        if [[ -n "${CONDA_PREFIX:-}" && -x "${CONDA_PREFIX}/bin/python" ]]; then
            if [[ "$(basename -- "${CONDA_PREFIX}")" == "env" ]]; then
                _suggest="$(dirname -- "${CONDA_PREFIX}")"
            fi
        fi
        echo "Where is Pikobs installed?"
        echo "  Enter the PROJECT directory that contains env/."
        echo "  The web launcher will be installed in <PROJECT_DIR>/pikobs_web."
        echo "  Press Enter to accept the suggested path."
        read -rp "  Pikobs project directory [${_suggest}]: " _reply
        PROJECT_DIR="${_reply:-${_suggest}}"
    elif [[ "${WEB_ONLY}" != "1" && "${UPDATE_PIKOBS}" != "1" ]]; then
        echo "Where do you want to install Pikobs on PPP7?"
        echo ""
        echo "  Recommended installation location:"
        echo "    ${DEFAULT_PROJECT_DIR}"
        echo ""
        echo "  This is recommended because the Pikobs environment can be large."
        echo "  Using /fs/site8 avoids consuming your HOME quota."
        echo ""
        echo "  The installer will create:"
        echo "    ${DEFAULT_PROJECT_DIR}/env"
        echo "    ${DEFAULT_PROJECT_DIR}/pikobs_web"
        echo "    ${DEFAULT_PROJECT_DIR}/.pikobs_web"
        echo ""
        echo "  A small stable symbolic link will be created in HOME:"
        echo "    ${CANONICAL_LINK} -> <PROJECT_DIR>"
        echo ""
        echo "  The project directory will be private to ${USER} (mode 700)."
        echo "  Press Enter to accept the default, or type another absolute path."
        read -rp "  Pikobs project directory [${PROJECT_DIR}]: " _reply
        if [[ -n "${_reply}" ]]; then
            PROJECT_DIR="${_reply}"
        fi
    fi
else
    if [[ ( "${WEB_ONLY}" == "1" || "${UPDATE_PIKOBS}" == "1" ) && "${PROJECT_DIR_EXPLICIT}" != "1" ]]; then
        echo "❌ This mode requires an explicit install path in non-interactive mode." >&2
        echo "   Use --project-dir /path/to/pikobs or PROJECT_DIR=/path/to/pikobs." >&2
        exit 2
    fi
fi

PROJECT_DIR_SELECTED="${PROJECT_DIR}"
PROJECT_DIR="$(realpath -m "${PROJECT_DIR}")"
HOME_REAL="$(realpath -m "${HOME}")"
ENV_PATH="${PROJECT_DIR}/env"
CACHE_DIR="${PROJECT_DIR}/mamba_cache"
PROFILE_FILE="${HOME}/.profile.d/interactive/post"
PIKOBS_WEB_DIR="${PROJECT_DIR}/pikobs_web"
PIKOBS_WEB_STATE_DIR="${PROJECT_DIR}/.pikobs_web"

# The heavy environment must live on shared/site storage, not physically under
# $HOME. A path such as ~/sites8/pikobs_install is fine because realpath resolves
# it to /fs/site8/... before this test.
if [[ "${PROJECT_DIR}" == "${HOME_REAL}" || "${PROJECT_DIR}" == "${HOME_REAL}/"* ]]; then
    echo "❌ Pikobs cannot be installed physically inside HOME:" >&2
    echo "   Selected : ${PROJECT_DIR_SELECTED}" >&2
    echo "   Resolved : ${PROJECT_DIR}" >&2
    echo "" >&2
    echo "Choose a site-storage path, for example:" >&2
    echo "   ${DEFAULT_PROJECT_DIR}" >&2
    exit 2
fi

# For a fresh/full install, fail early if the chosen storage parent is not
# writable or if the stable HOME name is occupied by a real file/directory.
# Existing symlinks are safe: they are replaced only after the install succeeds.
if [[ "${WEB_ONLY}" != "1" && "${UPDATE_PIKOBS}" != "1" ]]; then
    PROJECT_PARENT="$(dirname -- "${PROJECT_DIR}")"
    if [[ ! -d "${PROJECT_PARENT}" ]]; then
        echo "❌ Parent storage directory does not exist:" >&2
        echo "   ${PROJECT_PARENT}" >&2
        exit 2
    fi
    if [[ ! -w "${PROJECT_PARENT}" ]]; then
        echo "❌ You do not have write permission in:" >&2
        echo "   ${PROJECT_PARENT}" >&2
        exit 2
    fi
    if [[ -e "${CANONICAL_LINK}" && ! -L "${CANONICAL_LINK}" ]]; then
        echo "❌ Cannot create the stable HOME symlink because this path already" >&2
        echo "   exists and is not a symlink:" >&2
        echo "   ${CANONICAL_LINK}" >&2
        echo "" >&2
        echo "Move or rename it first; the installer will never delete it." >&2
        exit 2
    fi
fi

# PROJ is used by cartopy/fiona and therefore by Pikobs. In non-interactive
# SSH/PBS shells these variables are not guaranteed to be initialized by the
# module environment. Point them explicitly at this Pikobs environment.
export PROJ_DATA="${ENV_PATH}/share/proj"
export PROJ_LIB="${ENV_PATH}/share/proj"

mkdir -p "$(dirname "${PROFILE_FILE}")"
touch "${PROFILE_FILE}"

_append_unique() {
    grep -qF "$1" "${PROFILE_FILE}" || echo "$1" >> "${PROFILE_FILE}"
}

configure_proxy() {
    echo "🔍 Configuring CMC proxy..."
    _append_unique "export http_proxy=${PROXY_URL}"
    _append_unique 'export HTTP_PROXY=$http_proxy'
    _append_unique 'export https_proxy=$http_proxy'
    _append_unique 'export HTTPS_PROXY=$http_proxy'

    export http_proxy="${PROXY_URL}"
    export HTTP_PROXY="${PROXY_URL}"
    export https_proxy="${PROXY_URL}"
    export HTTPS_PROXY="${PROXY_URL}"
    echo "✅ Proxy ready (session + ${PROFILE_FILE})"
}

install_pikobs_web() {
    if [[ "${PIKOBS_INSTALL_WEB}" != "1" ]]; then
        echo "⏭️  Pikobs Web installation skipped (PIKOBS_INSTALL_WEB=${PIKOBS_INSTALL_WEB})."
        return 0
    fi

    if [[ ! -x "${ENV_PATH}/bin/python" ]]; then
        echo "❌ Cannot install Pikobs Web: Python environment not found:" >&2
        echo "   ${ENV_PATH}/bin/python" >&2
        echo "   Run the full setup first, or use the correct --project-dir." >&2
        return 1
    fi

    echo ""
    echo "🌐 Installing Pikobs Web launcher..."
    echo "   Destination: ${PIKOBS_WEB_DIR}"
    mkdir -p "${PIKOBS_WEB_STATE_DIR}"
    chmod 700 "${PIKOBS_WEB_STATE_DIR}"

    local tmpdir local_source web_source archive stage
    tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/pikobs-web.XXXXXX")"
    archive="${tmpdir}/Pikobs.tar.gz"
    stage="${PROJECT_DIR}/.pikobs_web_app.new.$$"
    web_source=""

    # Source priority:
    #   1. --web-source / PIKOBS_WEB_SOURCE (useful before a GitLab commit)
    #   2. pikobs/web_launcher next to this setup script in the checkout
    #   3. download the selected GitLab ref
    #
    # Expected checkout layout:
    #   pikobs/script/setup_pikobs.sh
    #   pikobs/web_launcher/...
    local_source="$(realpath -m "${SETUP_SCRIPT_DIR}/../web_launcher")"
    if [[ -n "${PIKOBS_WEB_SOURCE}" ]]; then
        web_source="$(realpath -m "${PIKOBS_WEB_SOURCE}")"
        if [[ ! -d "${web_source}/app" || ! -x "${web_source}/pikobs-web" ]]; then
            echo "❌ --web-source is not a valid Pikobs Web launcher directory:" >&2
            echo "   ${web_source}" >&2
            echo "   Expected at least: app/ and executable pikobs-web" >&2
            rm -rf "${tmpdir}" "${stage}"
            return 1
        fi
        echo "   Using explicitly supplied launcher: ${web_source}"
    elif [[ -d "${local_source}/app" && -x "${local_source}/pikobs-web" ]]; then
        echo "   Using launcher from current Pikobs checkout: ${local_source}"
        web_source="${local_source}"
    else
        echo "   No local pikobs/web_launcher found."
        echo "   Fetching Pikobs Web from GitLab ref '${PIKOBS_WEB_REF}'..."
        curl -fSL "${PIKOBS_WEB_ARCHIVE}" -o "${archive}"
        tar -xzf "${archive}" -C "${tmpdir}"

        web_source="$(find "${tmpdir}" -type d \
            -path "*/${PIKOBS_WEB_SUBDIR}" -print -quit)"

        if [[ -z "${web_source}" || ! -d "${web_source}/app" ]]; then
            echo "❌ Could not find ${PIKOBS_WEB_SUBDIR} in GitLab ref '${PIKOBS_WEB_REF}'." >&2
            echo "" >&2
            echo "   This usually means web_launcher has not been committed to that ref yet." >&2
            echo "   For a pre-commit test, place web_launcher beside pikobs/script/" >&2
            echo "   or run:" >&2
            echo "     $0 --web-only --project-dir '${PROJECT_DIR}' --web-source /path/to/web_launcher" >&2
            rm -rf "${tmpdir}" "${stage}"
            return 1
        fi
    fi

    # Stop only our old managed server before replacing application code.
    # Server runtime state lives in PROJECT_DIR/.pikobs_web and is deliberately untouched.
    if [[ -x "${PIKOBS_WEB_DIR}/pikobs-web" ]]; then
        echo "   Stopping existing Pikobs Web server, if any..."
        PIKOBS_WEB_PYTHON="${ENV_PATH}/bin/python" \
        PIKOBS_WEB_STATE_DIR="${PIKOBS_WEB_STATE_DIR}" \
            "${PIKOBS_WEB_DIR}/pikobs-web" stop >/dev/null 2>&1 || true
    fi

    rm -rf "${stage}"
    mkdir -p "${stage}"
    cp -a "${web_source}/." "${stage}/"

    if [[ ! -f "${stage}/requirements.txt" || ! -f "${stage}/pikobs-web" ]]; then
        echo "❌ Incomplete Pikobs Web source in ${web_source}." >&2
        rm -rf "${tmpdir}" "${stage}"
        return 1
    fi

    chmod +x "${stage}/pikobs-web"
    [[ -f "${stage}/pikobs-web-client" ]] && chmod +x "${stage}/pikobs-web-client"
    [[ -f "${stage}/install-client.sh" ]] && chmod +x "${stage}/install-client.sh"
    [[ -f "${stage}/install-workstation.sh" ]] && chmod +x "${stage}/install-workstation.sh"

    web_version=$("${ENV_PATH}/bin/python" - "${stage}/app/config.py" <<'PY_VERSION'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"^APP_VERSION\s*=\s*['\"]([^'\"]+)", text, re.M)
print(m.group(1) if m else "unknown")
PY_VERSION
    )
    echo "   Pikobs Web source version: ${web_version}"

    echo "   Installing/updating web dependencies in the Pikobs environment..."
    "${ENV_PATH}/bin/python" -m pip install --upgrade -r "${stage}/requirements.txt"

    echo "   Verifying FastAPI/Uvicorn/Pikobs imports..."
    "${ENV_PATH}/bin/python" - <<'PY'
import fastapi
import pydantic
import uvicorn
import pikobs
print("Pikobs Web Python dependencies: OK")
PY

    # Application code is replaceable. Runtime state is elsewhere.
    rm -rf "${PIKOBS_WEB_DIR}.old"
    if [[ -e "${PIKOBS_WEB_DIR}" ]]; then
        mv "${PIKOBS_WEB_DIR}" "${PIKOBS_WEB_DIR}.old"
    fi
    mv "${stage}" "${PIKOBS_WEB_DIR}"
    rm -rf "${PIKOBS_WEB_DIR}.old" "${tmpdir}"
    echo "   Pikobs Web installed version: ${web_version}"

    mkdir -p "${HOME}/bin"
    cat > "${HOME}/bin/pikobs-web-server" <<EOF_SERVER
#!/usr/bin/env bash
export PIKOBS_WEB_PYTHON="${ENV_PATH}/bin/python"
export PIKOBS_WEB_STATE_DIR="${PIKOBS_WEB_STATE_DIR}"
export PROJ_DATA="${ENV_PATH}/share/proj"
export PROJ_LIB="${ENV_PATH}/share/proj"
exec "${PIKOBS_WEB_DIR}/pikobs-web" "\$@"
EOF_SERVER
    chmod +x "${HOME}/bin/pikobs-web-server"

    _append_unique 'export PATH="$HOME/bin:$PATH"'

    echo "✅ Pikobs Web installed."
    echo "   App       : ${PIKOBS_WEB_DIR}"
    echo "   State     : ${PIKOBS_WEB_STATE_DIR}"
    echo "   Server cmd: ${HOME}/bin/pikobs-web-server"
    echo "   Client    : ${PIKOBS_WEB_DIR}/pikobs-web-client"
    echo ""
    echo "   Preserved across updates:"
    echo "     ${PIKOBS_WEB_STATE_DIR}/preferences.json"
    echo "     ${PIKOBS_WEB_STATE_DIR}/runs/"
    echo "     every user-selected PATHWORK"
}

write_load_helper() {
    local LOAD_HELPER="${PROJECT_DIR}/load_pikobs.sh"
    echo "📝 Writing ${LOAD_HELPER}..."

    cat > "${LOAD_HELPER}" <<'EOF'
#!/usr/bin/env bash
# ============================================================================
# load_pikobs.sh — Activate the Pikobs runtime environment.
# Sourced by every run_<module>.sh script.
# ============================================================================

PIKOBS_PROJECT_DIR="${PIKOBS_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
PIKOBS_ENV_PATH="${PIKOBS_ENV_PATH:-${PIKOBS_PROJECT_DIR}/env}"
export PROJ_DATA="${PIKOBS_ENV_PATH}/share/proj"
export PROJ_LIB="${PIKOBS_ENV_PATH}/share/proj"

# Manual/interactive sessions keep Pikobs' normal update behaviour. PBS/Web
# jobs set their own non-interactive flags in the generated run script.
unset PIKOBS_NONINTERACTIVE PIKOBS_AUTO_UPDATE PIKOBS_DISABLE_UPDATE_PROMPT 2>/dev/null || true

echo "[pikobs] PROJECT_DIR = ${PIKOBS_PROJECT_DIR}"
echo "[pikobs] ENV_PATH    = ${PIKOBS_ENV_PATH}"

if [[ ! -d "${PIKOBS_ENV_PATH}" ]]; then
    echo "[pikobs] ERROR env directory does not exist: ${PIKOBS_ENV_PATH}" >&2
    echo "         Did you run setup_pikobs.sh? Or set PIKOBS_PROJECT_DIR." >&2
    return 1 2>/dev/null || exit 1
fi

if [[ -z "${http_proxy:-}" ]]; then
    export http_proxy=http://webproxy.science.gc.ca:8888/
    export HTTP_PROXY=${http_proxy}
    export https_proxy=${http_proxy}
    export HTTPS_PROXY=${http_proxy}
fi

echo "[pikobs] Loading mamba module..."
_pikobs_had_u=0
case $- in *u*) _pikobs_had_u=1; set +u ;; esac
# shellcheck disable=SC1091
. r.load.dot crd/ccrp/ssm/mamba_2026.02.18_all
[[ "${_pikobs_had_u}" == "1" ]] && set -u
unset _pikobs_had_u

if [[ "${CONDA_PREFIX:-}" != "${PIKOBS_ENV_PATH}" ]]; then
    echo "[pikobs] Activating env: ${PIKOBS_ENV_PATH}"
    _pikobs_had_u=0
    case $- in *u*) _pikobs_had_u=1; set +u ;; esac
    # shellcheck disable=SC1091
    source "$(conda info --base)/etc/profile.d/conda.sh"
    if ! conda activate "${PIKOBS_ENV_PATH}"; then
        echo "[pikobs] ERROR conda activate failed for ${PIKOBS_ENV_PATH}" >&2
        return 1 2>/dev/null || exit 1
    fi
    [[ "${_pikobs_had_u}" == "1" ]] && set -u
    unset _pikobs_had_u
else
    echo "[pikobs] Env already active: ${CONDA_PREFIX}"
fi

_installed=$(python -c "
import sys
try:
    import pikobs
except ImportError:
    sys.exit(1)
try:
    print(pikobs.__version__)
except AttributeError:
    try:
        from importlib.metadata import version
        print(version('pikobs'))
    except Exception:
        print('installed')
" 2>/dev/null)
if [[ -z "${_installed}" ]]; then
    echo "[pikobs] ERROR pikobs is not installed in '${PIKOBS_ENV_PATH}'." >&2
    echo "         Activate the env manually and run: pip install --upgrade pikobs" >&2
    return 1 2>/dev/null || exit 1
fi
echo "[pikobs] ✅ Env ready — pikobs ${_installed}"
EOF

    chmod +x "${LOAD_HELPER}"
}

install_update_command() {
    mkdir -p "${HOME}/bin"
    cat > "${HOME}/bin/pikobs-update" <<EOF_UPDATE
#!/usr/bin/env bash
set -euo pipefail
ENV_PATH="${ENV_PATH}"
export http_proxy="${PROXY_URL}"
export HTTP_PROXY="\$http_proxy"
export https_proxy="\$http_proxy"
export HTTPS_PROXY="\$http_proxy"
export PROJ_DATA="${ENV_PATH}/share/proj"
export PROJ_LIB="${ENV_PATH}/share/proj"

old="\$("\$ENV_PATH/bin/python" - <<'PY_UPDATE_OLD'
try:
    import pikobs
    print(getattr(pikobs, '__version__', 'installed'))
except Exception:
    print('not-installed')
PY_UPDATE_OLD
)"
echo "Current Pikobs: \$old"
read -rp "Update Pikobs in \$ENV_PATH now? [Y/n] " ans
ans="\${ans:-Y}"
[[ "\$ans" =~ ^[Yy]$ ]] || { echo "Cancelled."; exit 0; }
"\$ENV_PATH/bin/python" -m pip install --upgrade pikobs
new="\$("\$ENV_PATH/bin/python" - <<'PY_UPDATE_NEW'
import pikobs
print(getattr(pikobs, '__version__', 'installed'))
PY_UPDATE_NEW
)"
echo "Pikobs update complete: \$old -> \$new"
EOF_UPDATE
    chmod +x "${HOME}/bin/pikobs-update"
}

configure_profile_aliases() {
    echo "🔧 Configuring Pikobs commands in ${PROFILE_FILE}..."
    local ALIAS_MARKER="# >>> pikobs >>>"
    local ALIAS_END="# <<< pikobs <<<"

    if grep -qF "${ALIAS_MARKER}" "${PROFILE_FILE}" 2>/dev/null; then
        sed -i "/${ALIAS_MARKER}/,/${ALIAS_END}/d" "${PROFILE_FILE}"
    fi

    cat >> "${PROFILE_FILE}" <<ALIAS_BLOCK

${ALIAS_MARKER}
# Pikobs — activate env in current shell (interactive/debug sessions).
export PIKOBS_PROJECT_DIR="${PROJECT_DIR}"
export PATH="\$HOME/bin:\$PATH"
alias load_pikobs='source "${PROJECT_DIR}/load_pikobs.sh"'
${ALIAS_END}
ALIAS_BLOCK

    echo "✅ 'load_pikobs', pikobs-update and ~/bin configured in ${PROFILE_FILE}"
}

configure_proxy

# ==============================================================================
# UPDATE PIKOBS PACKAGE ONLY
# ==============================================================================
if [[ "${UPDATE_PIKOBS}" == "1" ]]; then
    echo "============================================================"
    echo "  Pikobs package update"
    echo "  Selected    = ${PROJECT_DIR_SELECTED}"
    echo "  Resolved    = ${PROJECT_DIR}"
    echo "  ENV_PATH    = ${ENV_PATH}"
    echo "============================================================"

    if [[ ! -x "${ENV_PATH}/bin/python" ]]; then
        echo "❌ Existing Pikobs environment not found: ${ENV_PATH}" >&2
        exit 1
    fi

    OLD_VERSION=$("${ENV_PATH}/bin/python" - <<'PY'
try:
    import pikobs
    print(getattr(pikobs, '__version__', 'installed'))
except Exception:
    print('not-installed')
PY
)

    echo "Current Pikobs: ${OLD_VERSION}"
    echo "Updating Pikobs in the existing environment..."
    "${ENV_PATH}/bin/python" -m pip install --upgrade pikobs

    NEW_VERSION=$("${ENV_PATH}/bin/python" - <<'PY'
import pikobs
print(getattr(pikobs, '__version__', 'installed'))
PY
)

    echo "✅ Pikobs package update complete: ${OLD_VERSION} -> ${NEW_VERSION}"
    echo "   Environment: ${ENV_PATH}"
    echo "   Pikobs Web and user data were not changed."
    exit 0
fi

# ==============================================================================
# WEB-ONLY MODE
# ==============================================================================
if [[ "${WEB_ONLY}" == "1" ]]; then
    echo "============================================================"
    echo "  Pikobs Web-only setup"
    echo "  Selected    = ${PROJECT_DIR_SELECTED}"
    echo "  Resolved    = ${PROJECT_DIR}"
    echo "  ENV_PATH    = ${ENV_PATH}"
    echo "============================================================"

    if [[ ! -x "${ENV_PATH}/bin/python" ]]; then
        echo "❌ Existing Pikobs environment not found:" >&2
        echo "   ${ENV_PATH}" >&2
        echo "Run the full installation first:" >&2
        echo "   ./setup_pikobs.sh" >&2
        exit 1
    fi

    if ! "${ENV_PATH}/bin/python" -c 'import pikobs' >/dev/null 2>&1; then
        echo "❌ '${ENV_PATH}' exists but Pikobs cannot be imported from it." >&2
        exit 1
    fi

    install_update_command
    install_pikobs_web
    configure_profile_aliases

    cat <<EOF

============================================================
✅ Pikobs Web update complete.

  App        : ${PIKOBS_WEB_DIR}
  State      : ${PIKOBS_WEB_STATE_DIR}
  Server cmd : ${HOME}/bin/pikobs-web-server

Nothing was removed from:
  ${PIKOBS_WEB_STATE_DIR}/preferences.json
  ${PIKOBS_WEB_STATE_DIR}/runs/
  user-selected PATHWORK directories

Server diagnostic:
  source ${PROFILE_FILE}
  pikobs-web-server status

On the workstation, the installed 'pikobs-web' wrapper refreshes its
client automatically from this server before each launch.
============================================================
EOF
    exit 0
fi

# ==============================================================================
# FULL PIKOBS INSTALL
# ==============================================================================

echo "============================================================"
echo "  Pikobs setup"
echo "  Selected    = ${PROJECT_DIR_SELECTED}"
echo "  Resolved    = ${PROJECT_DIR}"
echo "  ENV_PATH    = ${ENV_PATH}"
echo "  HOME link   = ${CANONICAL_LINK} -> ${PROJECT_DIR}"
echo "  Permissions = private to ${USER} (project directory mode 700)"
echo "  Storage     = site/shared storage; HOME keeps only the symlink/commands"
echo "============================================================"

# --- Load mamba module --------------------------------------------------------
echo "🧩 Loading mamba module..."
set +u
# shellcheck disable=SC1091,SC2086
. ${MAMBA_MODULE_LOAD}
set -u

export CONDA_SUBDIR=linux-64
export CONDA_SAT_SOLVER_TIMEOUT=180
export CONDA_DOWNLOAD_THREADS=10

# --- Workspace ----------------------------------------------------------------
echo "📂 Preparing ${PROJECT_DIR}..."
mkdir -p "${PROJECT_DIR}"
chmod 700 "${PROJECT_DIR}"
mkdir -p "${CACHE_DIR}"
cd "${PROJECT_DIR}"

# --- Fetch official environment YAML -----------------------------------------
echo "📥 Fetching pikobs_env.yml..."
curl -fSL "${PIKOBS_ENV_YML}" -o "${PROJECT_DIR}/pikobs_env.yml"

# --- Create environment -------------------------------------------------------
export CONDA_PKGS_DIRS="${CACHE_DIR}"
export MAMBA_NO_BANNER=1
export CONDA_PLUGINS_AUTO_ACCEPT_TOS=yes

cat <<'BANNER'

──────────────────────────────────────────────────────────────
⏳  Building the conda environment...
    This can take several minutes the first time.
──────────────────────────────────────────────────────────────

BANNER

if [[ -d "${ENV_PATH}" ]]; then
    echo "⚠️  An existing environment was found at:"
    echo "      ${ENV_PATH}"
    if [[ "${PIKOBS_AUTO_INSTALL:-0}" == "1" ]]; then
        REPLY="y"
    else
        read -rp "    Remove it and reinstall clean? [Y/n] " REPLY
        REPLY="${REPLY:-Y}"
    fi

    if [[ "${REPLY}" =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing ${ENV_PATH}..."
        rm -rf "${ENV_PATH}"
        echo "🛠️  Building fresh environment at ${ENV_PATH}..."
        mamba env create -p "${ENV_PATH}" -f "${PROJECT_DIR}/pikobs_env.yml" 2> >(
            grep -v -E "libmamba 'repo\.anaconda\.com'|libmamba Please make sure|libmamba See: https://legal\.anaconda" >&2
        )
    else
        echo "❌ Aborted. Existing env left untouched."
        echo "   To update it manually instead of reinstalling:"
        echo "     mamba env update -p ${ENV_PATH} -f ${PROJECT_DIR}/pikobs_env.yml --prune"
        echo ""
        echo "   To update only Pikobs Web without touching this env:"
        echo "     ./setup_pikobs.sh --web-only"
        exit 1
    fi
else
    echo "🛠️  Building environment at ${ENV_PATH}..."
    mamba env create -p "${ENV_PATH}" -f "${PROJECT_DIR}/pikobs_env.yml" 2> >(
        grep -v -E "libmamba 'repo\.anaconda\.com'|libmamba Please make sure|libmamba See: https://legal\.anaconda" >&2
    )
fi

# --- Verify/install Pikobs ----------------------------------------------------
echo ""
echo "🔎 Verifying pikobs inside ${ENV_PATH}..."
set +u
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV_PATH}"
set -u

INSTALLED_VERSION=$(python -c "
import sys
try:
    import pikobs
except ImportError:
    sys.exit(1)
try:
    print(pikobs.__version__)
except AttributeError:
    try:
        from importlib.metadata import version
        print(version('pikobs'))
    except Exception:
        print('installed')
" 2>/dev/null || true)

if [[ -n "${INSTALLED_VERSION}" ]]; then
    echo "✅ pikobs ${INSTALLED_VERSION} is already installed in this env."
else
    cat <<EOF

⚠️  pikobs itself is NOT yet installed in the new environment.
    (The YAML provides the dependency stack.)

    Recommended installation into THIS env:
        pip install --upgrade pikobs

EOF
    if [[ "${PIKOBS_AUTO_INSTALL:-0}" == "1" ]]; then
        REPLY="y"
    else
        read -rp "    Install pikobs now? [Y/n] " REPLY
        REPLY="${REPLY:-Y}"
    fi

    if [[ "${REPLY}" =~ ^[Yy]$ ]]; then
        echo "📦 Installing pikobs into ${ENV_PATH}..."
        pip install --upgrade pikobs
        INSTALLED_VERSION=$(python -c "
import sys
try:
    import pikobs
except ImportError:
    sys.exit(1)
try:
    print(pikobs.__version__)
except AttributeError:
    try:
        from importlib.metadata import version
        print(version('pikobs'))
    except Exception:
        print('installed')
" 2>/dev/null || true)
        if [[ -n "${INSTALLED_VERSION}" ]]; then
            echo "✅ pikobs ${INSTALLED_VERSION} installed."
        else
            echo "❌ pip install reported success but 'import pikobs' still fails."
            exit 1
        fi
    else
        echo "⏭️  Skipped. Install later with:"
        echo "     conda activate ${ENV_PATH}"
        echo "     pip install --upgrade pikobs"
    fi
fi

# --- Loader -------------------------------------------------------------------
write_load_helper

# --- Canonical symlink --------------------------------------------------------
if [[ "${PROJECT_DIR}" != "${CANONICAL_LINK}" ]]; then
    echo "🔗 Linking ${CANONICAL_LINK} -> ${PROJECT_DIR}..."
    if [[ -L "${CANONICAL_LINK}" ]]; then
        rm -f "${CANONICAL_LINK}"
        ln -s "${PROJECT_DIR}" "${CANONICAL_LINK}"
        echo "   ♻️  Replaced existing symlink."
    elif [[ -e "${CANONICAL_LINK}" ]]; then
        echo "   ❌ ${CANONICAL_LINK} already exists as a real directory/file." >&2
        echo "      It will never be removed automatically. Move or rename it first." >&2
        exit 2
    else
        ln -s "${PROJECT_DIR}" "${CANONICAL_LINK}"
        echo "   ✅ Symlink created."
    fi
else
    echo "🔗 PROJECT_DIR is already the canonical ${CANONICAL_LINK} (no symlink needed)."
fi

# --- Small PPP7 maintenance commands + interactive profile --------------------
install_update_command
configure_profile_aliases

# --- Pikobs Web backend (PPP7) ------------------------------------------------
install_pikobs_web

# --- Final summary ------------------------------------------------------------
cat <<EOF

============================================================
✅ Pikobs setup complete.

  Selected    : ${PROJECT_DIR_SELECTED}
  Project dir : ${PROJECT_DIR}
  Env path    : ${ENV_PATH}
  Loader      : ${PROJECT_DIR}/load_pikobs.sh
  Canonical   : ${CANONICAL_LINK} $( [[ "${PROJECT_DIR}" != "${CANONICAL_LINK}" ]] && echo "(symlink -> ${PROJECT_DIR})" || echo "(direct)" )
  Pikobs ver. : ${INSTALLED_VERSION:-<not installed>}
  Pikobs Web  : ${PIKOBS_WEB_DIR}
  Web state   : ${PIKOBS_WEB_STATE_DIR}
  Permissions : ${PROJECT_DIR} is private to ${USER} (mode 700)

Interactive Pikobs:
  source ${PROFILE_FILE}
  load_pikobs

Pikobs Web server diagnostics:
  source ${PROFILE_FILE}
  pikobs-web-server status
  pikobs-web-server log

Update Pikobs package later (PPP7 login, outside PBS jobs):
  pikobs-update

Manual/interactive Pikobs sessions keep the normal update question.
PBS/Web jobs never update the environment while running; they answer "n" and
write a reminder in the live log to run pikobs-update later.

Update ONLY Pikobs Web later:
  ./setup_pikobs.sh --web-only

──────────────────────────────────────────────────────────────
REQUIRED ON EACH WORKSTATION — ONE-TIME CLIENT INSTALL
──────────────────────────────────────────────────────────────
The PPP7 server is ready, but the workstation launcher is a separate small
installation. Run ONE of these commands from Bash on the WORKSTATION.

Preferred (uses the installer that was just installed on PPP7, so it is always
the same version as this server):

  source <(ssh -4 ${USER}@ppp7 'cat ~/pikobs_install/pikobs_web/install-workstation.sh')

Alternative (downloads the current installer from GitLab):

  source <(curl -fsSL https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/install_pikobs_web_workstation.sh)

It asks only for the PPP user/host, finds the already-installed server through
~/pikobs_install, installs the small ~/bin/pikobs-web command on the workstation,
verifies that the launcher is available, and opens the browser. It does NOT
install or modify the PPP7 environment and does not edit workstation profile files.

After the first installation, normal use is simply:

  pikobs-web

The workstation wrapper refreshes the real client from the server before each
launch, so future './setup_pikobs.sh --web-only' updates propagate automatically.

The web launcher does NOT delete:
  ${PIKOBS_WEB_STATE_DIR}/preferences.json
  ${PIKOBS_WEB_STATE_DIR}/runs/
  user-selected PATHWORK directories
============================================================
EOF
