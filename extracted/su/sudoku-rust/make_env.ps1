uv python install 3.13.12
uv python pin 3.13.12
uv venv
./.venv/Scripts/activate
uv tool install maturin
uv sync
cargo install cargo-llvm-cov
rustup component add llvm-tools-preview
