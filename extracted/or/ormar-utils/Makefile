.PHONY: fmt fmt-check check lint test build clean

fmt:
	cargo fmt
	poetry run ruff format tests

fmt-check:
	cargo fmt --check
	poetry run ruff format --check tests

check:
	cargo clippy --all-targets -- -D warnings

lint: fmt-check check
	poetry run ruff check tests

test:
	poetry run pytest tests/ -v

build:
	poetry run maturin develop

clean:
	cargo clean
	rm -rf target/

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  fmt       - Format Rust (rustfmt) and Python (ruff) code"
	@echo "  fmt-check - Check formatting without modifying files"
	@echo "  check     - Run clippy linter with strict warnings"
	@echo "  lint      - Run all format checks, clippy and ruff lint"
	@echo "  test      - Run tests with pytest"
	@echo "  build     - Build the extension module with maturin"
	@echo "  clean     - Clean build artifacts"
