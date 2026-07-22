#!/usr/bin/env bash
# CVC installer — macOS / Linux
# Source of truth: ~/Projects/Portfolio-E/installers/install.sh
# Mirrored to:    ~/Projects/cvc/scripts/install.sh
set -u  # don't 'set -e' — we handle failures explicitly to give clean messages

PACKAGE="tm-ai[all]"
PYPI_NAME="tm-ai"
TOOL_NAME="cvc"
UV_INSTALL_URL="https://astral.sh/uv/install.sh"

if [ -z "${UV_HTTP_TIMEOUT:-}" ]; then export UV_HTTP_TIMEOUT=300; fi

# Pin a known-good Python. Python 3.14 ships Unicode 17 which breaks
# rich<14 ("No module named 'rich._unicode_data.unicode17_0_0'"), and
# our dep pins rich>=13 — so we lock the tool venv to 3.13 across all
# installs/retries to keep CVC importable on every box.
CVC_PIN_PY="3.13"

# ── CVC branded colours (24-bit truecolor) ─────────────────────────────────
CVC_RED=$'\033[38;2;204;51;51m'
CVC_BRIGHT=$'\033[38;2;255;68;68m'
CVC_DIM=$'\033[38;2;139;112;112m'
CVC_GREEN=$'\033[38;2;80;200;120m'
BOLD=$'\033[1m'
RESET=$'\033[0m'

info() { printf "  %s%s%s\n"        "${CVC_DIM}"   "$1" "${RESET}"; }
ok()   { printf "  %s%s✓%s %s\n"    "${CVC_GREEN}" "${BOLD}" "${RESET}" "$1"; }
warn() { printf "  %s⚠ %s%s\n"      "${CVC_DIM}"   "$1" "${RESET}"; }
err()  { printf "  %s%s✗%s %s\n"    "${CVC_RED}"   "${BOLD}" "${RESET}" "$1" >&2; }

echo ""
printf "%s%s* Installing %sCVC%s...%s\n" \
    "${CVC_RED}" "${BOLD}" "${CVC_BRIGHT}" "${CVC_RED}" "${RESET}"

# ── Detect existing install ────────────────────────────────────────────────
EXISTING_BEFORE=""
if command -v cvc &>/dev/null; then
    EXISTING_BEFORE=$(cvc --version 2>/dev/null | head -n1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)
fi

# ── Fetch latest version (with CDN-staleness retry) ────────────────────────
fetch_latest() {
    if ! command -v curl &>/dev/null; then return 1; fi
    local nonce; nonce=$(date +%s%N 2>/dev/null || date +%s)
    curl -sf \
        -H "Cache-Control: no-cache" \
        -H "Pragma: no-cache" \
        "https://pypi.org/pypi/${PYPI_NAME}/json?_=${nonce}" 2>/dev/null \
        | grep -o '"version":"[^"]*"' | head -n1 | cut -d'"' -f4
}
version_gt() {
    [ "$1" = "$2" ] && return 1
    [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | tail -n1)" = "$1" ]
}

LATEST_VERSION=$(fetch_latest || true)
if [ -n "$LATEST_VERSION" ] && [ -n "$EXISTING_BEFORE" ]; then
    if ! version_gt "$LATEST_VERSION" "$EXISTING_BEFORE"; then
        WAITED=0
        for attempt in 1 2 3 4 5 6; do
            if [ "$WAITED" = "0" ]; then
                info "Checking for latest version..."
                WAITED=1
            fi
            sleep 5
            NEW_LATEST=$(fetch_latest || true)
            if [ -n "$NEW_LATEST" ] && version_gt "$NEW_LATEST" "$EXISTING_BEFORE"; then
                LATEST_VERSION="$NEW_LATEST"; break
            fi
        done
    fi
fi

# ── Status lines (parity with Windows) ─────────────────────────────────────
if [ -n "$EXISTING_BEFORE" ]; then
    info "Found existing CVC v${EXISTING_BEFORE} → will replace"
else
    info "No existing CVC install found"
fi
if [ -n "$LATEST_VERSION" ]; then
    info "Latest available: v${LATEST_VERSION}"
fi

# ── Ensure uv is available (silent, internal) ──────────────────────────────
if ! command -v uv &>/dev/null; then
    info "Installing package manager..."
    curl -fsSL "$UV_INSTALL_URL" | sh >/dev/null 2>&1 || true
    export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
    if ! command -v uv &>/dev/null; then
        err "Package manager (uv) is required but could not be installed."
        info "Manual install: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
fi

UV_TOOL_BIN=$(uv tool dir --bin 2>/dev/null || true)
if [ -z "$UV_TOOL_BIN" ] || [ ! -d "$UV_TOOL_BIN" ]; then
    UV_TOOL_BIN="$HOME/.local/bin"
fi
UV_TOOL_BIN="${UV_TOOL_BIN%/}"

UV_TOOL_ROOT=$(uv tool dir 2>/dev/null || true)
if [ -z "$UV_TOOL_ROOT" ]; then
    UV_TOOL_ROOT="$HOME/.local/share/uv/tools"
fi
UV_TOOL_ROOT="${UV_TOOL_ROOT%/}"

is_uv_owned() {
    local p="${1%/}"
    [[ "$p" == "$UV_TOOL_BIN"* ]]
}

# ── Purge old installs (silent) ────────────────────────────────────────────
CLEANUP_COUNT=0
SEEN_PYTHONS=""
IFS=: read -ra PATH_DIRS <<< "$PATH"
for dir in "${PATH_DIRS[@]}"; do
    [ -d "$dir" ] || continue
    for _pyexe in python3 python python3.13 python3.12 python3.11 python3.10; do
        full="$dir/$_pyexe"
        if [ -x "$full" ] && [[ ":$SEEN_PYTHONS:" != *":$full:"* ]]; then
            SEEN_PYTHONS="$SEEN_PYTHONS:$full"
            if "$full" -m pip show "$PYPI_NAME" &>/dev/null; then
                "$full" -m pip uninstall "$PYPI_NAME" -y >/dev/null 2>&1 || true
                CLEANUP_COUNT=$((CLEANUP_COUNT + 1))
            fi
        fi
    done
done

if command -v conda &>/dev/null; then
    if conda run -n base python -m pip show "$PYPI_NAME" &>/dev/null; then
        conda run -n base pip uninstall "$PYPI_NAME" -y >/dev/null 2>&1 || true
        conda remove -n base "$PYPI_NAME" -y >/dev/null 2>&1 || true
        CLEANUP_COUNT=$((CLEANUP_COUNT + 1))
    fi
fi
if command -v pipx &>/dev/null && pipx list 2>/dev/null | grep -q "$PYPI_NAME"; then
    pipx uninstall "$PYPI_NAME" >/dev/null 2>&1 || true
    CLEANUP_COUNT=$((CLEANUP_COUNT + 1))
fi
if command -v brew &>/dev/null && brew list "$PYPI_NAME" &>/dev/null; then
    brew uninstall "$PYPI_NAME" >/dev/null 2>&1 || true
    CLEANUP_COUNT=$((CLEANUP_COUNT + 1))
fi

# Delete stale cvc shims (NOT uv-owned)
for dir in "${PATH_DIRS[@]}"; do
    [ -d "$dir" ] || continue
    for stale in cvc cvc.py; do
        stale_path="$dir/$stale"
        if [ -f "$stale_path" ] && ! is_uv_owned "$stale_path"; then
            rm -f "$stale_path" >/dev/null 2>&1 || true
        fi
    done
done

# Remove existing uv tool entry (handles malformed envs too)
TOOL_LIST_OUT=$(uv tool list 2>&1 || true)
NEEDS_CLEANUP=0
if echo "$TOOL_LIST_OUT" | grep -qE "^$PYPI_NAME(\s|$)"; then NEEDS_CLEANUP=1; fi
if echo "$TOOL_LIST_OUT" | grep -qiE "(malformed|invalid environment).*$PYPI_NAME|$PYPI_NAME.*(malformed|invalid environment)"; then NEEDS_CLEANUP=1; fi
if [ -d "$UV_TOOL_ROOT/$PYPI_NAME" ]; then NEEDS_CLEANUP=1; fi
if [ "$NEEDS_CLEANUP" = "1" ]; then
    uv tool uninstall "$PYPI_NAME" >/dev/null 2>&1 || true
    [ -d "$UV_TOOL_ROOT/$PYPI_NAME" ] && rm -rf "$UV_TOOL_ROOT/$PYPI_NAME" >/dev/null 2>&1 || true
fi

# ── Install ────────────────────────────────────────────────────────────────
if [ -n "$LATEST_VERSION" ]; then
    PINNED_PACKAGE="${PYPI_NAME}[all]==${LATEST_VERSION}"
    info "Installing CVC v${LATEST_VERSION}..."
else
    PINNED_PACKAGE="$PACKAGE"
    info "Installing CVC (latest)..."
fi

install_with_retry() {
    # Capture the install output so we can surface the actual uv error
    # if all retries fail (v2.92.10).
    local outfile
    outfile=$(mktemp)
    if uv tool install --force --refresh --python "$CVC_PIN_PY" "$PINNED_PACKAGE" >"$outfile" 2>&1; then
        rm -f "$outfile"; return 0
    fi
    warn "Retrying with a clean cache..."
    uv cache clean "$PYPI_NAME" >/dev/null 2>&1 || true
    [ -d "$UV_TOOL_ROOT/$PYPI_NAME" ] && rm -rf "$UV_TOOL_ROOT/$PYPI_NAME" >/dev/null 2>&1 || true
    if uv tool install --force --refresh --python "$CVC_PIN_PY" "$PINNED_PACKAGE" >"$outfile" 2>&1; then
        rm -f "$outfile"; return 0
    fi
    warn "Retrying with latest version..."
    if uv tool install --force --refresh --python "$CVC_PIN_PY" "$PACKAGE" >"$outfile" 2>&1; then
        rm -f "$outfile"; return 0
    fi
    warn "Installer is having trouble - showing details..."
    # v2.92.10 - Show the actual uv error so users can diagnose
    # without digging through logs.
    cat "$outfile" >&2
    echo "" >&2
    echo "  Common causes:" >&2
    echo "    - Antivirus / SELinux / AppArmor is blocking uv from creating the tool venv" >&2
    echo "    - A running cvc / python is holding a file lock on the tool dir" >&2
    echo "    - PyPI is unreachable or rate-limiting (try again in 60s)" >&2
    echo "    - Network proxy blocks astral.sh or pypi.org" >&2
    echo "" >&2
    echo "  Recovery: close any open CVC session and re-run the install command." >&2
    rm -f "$outfile"
    return 1
}

if ! install_with_retry; then
    err "CVC installation failed."
    info "Try opening a new terminal and re-running the install command."
    exit 1
fi
ok "CVC installed"

# ── PATH wiring (silent) ───────────────────────────────────────────────────
mkdir -p "$UV_TOOL_BIN"

add_to_front_of_path() {
    local cfg="$1"
    local guard_start='# >>> cvc path >>>'
    local guard_end='# <<< cvc path <<<'
    local line='export PATH="'"$UV_TOOL_BIN"':$PATH"'
    [ -f "$cfg" ] || return 0
    if grep -q "$guard_start" "$cfg" 2>/dev/null; then
        awk -v s="$guard_start" -v e="$guard_end" '
            $0 == s {skip=1; next}
            $0 == e {skip=0; next}
            !skip {print}
        ' "$cfg" > "${cfg}.tmp" && mv "${cfg}.tmp" "$cfg"
    fi
    local tmp; tmp=$(mktemp)
    {
        echo "$guard_start"
        echo "$line"
        echo "$guard_end"
        echo ""
        cat "$cfg"
    } > "$tmp"
    mv "$tmp" "$cfg"
}
for rc in "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.profile"; do
    [ -f "$rc" ] && add_to_front_of_path "$rc"
done
export PATH="$UV_TOOL_BIN:$PATH"
uv tool update-shell >/dev/null 2>&1 || true
ok "PATH updated"

# ── Verify ─────────────────────────────────────────────────────────────────
INSTALLED_VERSION=""
CVC_BIN="$UV_TOOL_BIN/cvc"
if [ -x "$CVC_BIN" ]; then
    INSTALLED_VERSION=$("$CVC_BIN" --version 2>/dev/null | head -n1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)
elif command -v "$TOOL_NAME" &>/dev/null; then
    INSTALLED_VERSION=$("$TOOL_NAME" --version 2>/dev/null | head -n1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || true)
fi

echo ""
V_STR=""; [ -n "$INSTALLED_VERSION" ] && V_STR=" v${INSTALLED_VERSION}"
printf "%s%s* %sCVC%s%s installed successfully.%s\n" \
    "${CVC_RED}" "${BOLD}" "${CVC_BRIGHT}" "${V_STR}" "${CVC_RED}" "${RESET}"

if [ -n "$LATEST_VERSION" ] && [ -n "$INSTALLED_VERSION" ] && [ "$INSTALLED_VERSION" != "$LATEST_VERSION" ]; then
    warn "Expected v${LATEST_VERSION}, got v${INSTALLED_VERSION}."
    warn "Open a new terminal — PATH changes take effect in new sessions."
fi

echo ""
printf "%sRun %s%s%scvc%s %sto start. (If 'cvc' is not found, open a new terminal once.)%s\n" \
    "${CVC_DIM}" "${RESET}" "${CVC_BRIGHT}" "${BOLD}" "${RESET}" "${CVC_DIM}" "${RESET}"
echo ""
