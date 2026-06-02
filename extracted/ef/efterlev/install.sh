#!/bin/sh
# Efterlev bootstrap installer.
#
#   curl -LsSf https://efterlev.org/install.sh | sh
#
# Installs uv if it is missing (uv fetches Python 3.12 for you, which is why
# this works on a stock Mac or an Anaconda `(base)` env where `pip install`
# hits a Python-version wall), then installs the `efterlev` CLI as a uv tool.
# The only prerequisite is curl or wget. Nothing else on your system changes.
set -eu

info() { printf '\033[1;36m==>\033[0m %s\n' "$1"; }
warn() { printf '\033[1;33mwarning:\033[0m %s\n' "$1" >&2; }
err()  { printf '\033[1;31merror:\033[0m %s\n' "$1" >&2; }

# 1. Find uv, or install it.
if command -v uv >/dev/null 2>&1; then
  info "uv is already installed ($(uv --version))."
else
  info "Installing uv (fetches Python 3.12 for you; nothing else on your system changes)..."
  if command -v curl >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- https://astral.sh/uv/install.sh | sh
  else
    err "Need curl or wget to install uv. Install one, or install uv manually: https://docs.astral.sh/uv/"
    exit 1
  fi
  # uv installs to ~/.local/bin (or $XDG_BIN_HOME / ~/.cargo/bin); put it on
  # PATH for the rest of THIS script. The installer already updates the shell
  # profile for future shells.
  for d in "$HOME/.local/bin" "${XDG_BIN_HOME:-}" "$HOME/.cargo/bin"; do
    if [ -n "$d" ] && [ -x "$d/uv" ]; then
      PATH="$d:$PATH"
    fi
  done
  export PATH
fi

if ! command -v uv >/dev/null 2>&1; then
  err "uv was installed but isn't on PATH in this shell. Open a new terminal and run: uv tool install efterlev"
  exit 1
fi

# 2. Install (or update) the efterlev CLI. --reinstall keeps it on the latest
#    published release, so re-running this script is also the upgrade path.
info "Installing the efterlev CLI..."
uv tool install --reinstall efterlev

# 3. Friendly next steps.
if command -v efterlev >/dev/null 2>&1; then
  info "Installed: $(efterlev --version 2>/dev/null || echo efterlev)"
else
  warn "efterlev installed via uv but isn't on PATH yet. Run 'uv tool update-shell', then open a new terminal."
fi

cat <<'EOF'

Efterlev is installed. Try it:

  efterlev studio          # local browser app on sample data, no API key, no setup
  efterlev quickstart      # full pipeline on a bundled sample (needs an LLM key)

Point it at your own repo:

  cd your-repo
  efterlev init --target . && efterlev report run

Docs: https://docs.efterlev.org
EOF
