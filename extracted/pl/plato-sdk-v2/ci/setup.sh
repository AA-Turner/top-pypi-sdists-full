#!/bin/bash
set -e

export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
if [ -n "${GITHUB_PATH:-}" ]; then
  printf '%s\n' "$HOME/.cargo/bin" "$HOME/.local/bin" >> "$GITHUB_PATH"
fi

# Install libfuse3-dev + pkg-config (needed for cargo test on plato-fuse).
# Set SKIP_FUSE_DEPS=1 to skip these system packages entirely.
if [ "${SKIP_FUSE_DEPS:-0}" != "1" ] && command -v apt-get &> /dev/null; then
  missing_packages=()
  dpkg -s pkg-config >/dev/null 2>&1 || missing_packages+=("pkg-config")
  dpkg -s libfuse3-dev >/dev/null 2>&1 || missing_packages+=("libfuse3-dev")
  if [ ${#missing_packages[@]} -gt 0 ]; then
    if command -v sudo &> /dev/null; then
      sudo apt-get update
      sudo apt-get install -y "${missing_packages[@]}"
    else
      apt-get update
      apt-get install -y "${missing_packages[@]}"
    fi
  fi
fi

# zig + cargo-zigbuild are only needed for cross-compiling plato-fuse
# (integration-fuse tests).  Set INSTALL_ZIGBUILD=1 to install them.
if [ "${INSTALL_ZIGBUILD:-0}" = "1" ]; then
  mkdir -p "$HOME/.cargo/bin" "$HOME/.local/opt"

  if ! command -v zig &> /dev/null; then
    ZIG_VERSION="0.14.0"
    ZIG_ARCHIVE="zig-linux-x86_64-${ZIG_VERSION}.tar.xz"
    curl -LsSf "https://ziglang.org/download/${ZIG_VERSION}/${ZIG_ARCHIVE}" -o "/tmp/${ZIG_ARCHIVE}"
    tar -xJf "/tmp/${ZIG_ARCHIVE}" -C "$HOME/.local/opt"
    ln -sf "$HOME/.local/opt/zig-linux-x86_64-${ZIG_VERSION}/zig" "$HOME/.cargo/bin/zig"
  fi

  if ! command -v cargo-zigbuild &> /dev/null; then
    # Prefer the prebuilt wheel from PyPI — `cargo install` compiles the tool
    # from source (~45-60s of pure toolchain overhead per CI run).
    if command -v uv &> /dev/null; then
      uv tool install cargo-zigbuild
    else
      cargo install cargo-zigbuild --locked
    fi
  fi
fi

if ! command -v uv &> /dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

cd "$(dirname "$0")/.."
uv sync --extra dev
