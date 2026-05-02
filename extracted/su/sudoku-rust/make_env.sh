uv python install 3.13.12
uv python pin 3.13.12
uv sync
source ./.venv/bin/activate
uv tool install maturin
cargo install cargo-llvm-cov
rustup component add llvm-tools-preview
