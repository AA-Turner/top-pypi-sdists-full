# dealcloud-sdk-example — sample using uv against PyPI (or indexes in pyproject.toml / uv.toml).
# Private package indexes: https://docs.astral.sh/uv/configuration/authentication/

.PHONY: help install install-dev sync run test test-integration clean build lock

help:
	@echo "dealcloud-sdk-example (DealCloud Python SDK sample)"
	@echo ""
	@echo "Usage:"
	@echo "  make sync              Install deps with uv (includes dev / pytest)"
	@echo "  make install           Alias for sync"
	@echo "  make install-dev       Alias for sync"
	@echo "  make run               Run the sample CLI (needs DC_* in .env or env)"
	@echo "  make test              Run tests (integration skipped unless --run-integration)"
	@echo "  make test-integration  Run integration tests (needs DC_* credentials)"
	@echo "  make build             Clean and build wheel/sdist (uv build)"
	@echo "  make lock              Refresh uv.lock"
	@echo "  make clean             Remove local venv and caches"

install: sync

install-dev: sync

sync:
	uv sync --extra dev

run:
	uv run dealcloud-sdk-example

# Use python -m pytest so the project venv's interpreter is used
test:
	uv run python -m pytest tests -q

test-integration:
	uv run python -m pytest tests -m integration --run-integration -q --no-cov

clean:
	rm -rf .venv .pytest_cache dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

build: clean
	uv build

lock:
	uv lock
