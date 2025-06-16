#!/bin/bash
set -e

rm -rf target/wheels/

. venv/bin/activate

# use --zig for better cross compatibility on linux
maturin build --release --strip --target aarch64-unknown-linux-gnu --zig
maturin build --release --strip --target x86_64-unknown-linux-gnu --zig
maturin build --release --strip --target aarch64-unknown-linux-musl --zig
maturin build --release --strip --target x86_64-unknown-linux-musl --zig

# without zig because that breaks stuff on mac
maturin build --release --strip --target aarch64-apple-darwin # --zig
maturin build --release --strip --target x86_64-apple-darwin # --zig

maturin sdist

maturin upload --skip-existing -u __token__ target/wheels/*
