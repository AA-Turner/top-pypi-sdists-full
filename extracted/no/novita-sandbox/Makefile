# Novita Agent Sandbox SDK - Test Management Makefile

.PHONY: help test test-* lint build clean

# Default target
help:
	@echo "Novita Agent Sandbox SDK Test Management"
	@echo "================================"
	@echo "Test Commands:"
	@echo "  test-unit         Run offline unit tests (no API key needed)"
	@echo "  test-core         Run all core module tests (needs NOVITA_API_KEY)"
	@echo "  test-code-interpreter  Run code interpreter tests (needs NOVITA_API_KEY)"
	@echo "  test-desktop      Run desktop automation tests (needs NOVITA_API_KEY)"
	@echo "  test              Run all of the above except test-unit"
	@echo "  lint              Run ruff and mypy"
	@echo "  clean             Clean build artifacts and cache files"

# Offline unit tests. These do not create sandboxes and require no credentials,
# so they are the suite that runs on pull requests. Everything under
# test-core/test-code-interpreter/test-desktop provisions real sandboxes and
# consumes API quota.
test-unit:
	poetry run python -m pytest -v --tb=short \
		tests/ \
		src/novita_sandbox/core/tests/test_connection_config.py \
		src/novita_sandbox/core/tests/test_volume_mount_config.py \
		src/novita_sandbox/core/tests/test_sandbox_clone_reset_compat.py \
		src/novita_sandbox/core/tests/test_quota_events.py \
		src/novita_sandbox/core/tests/test_legacy_compat.py

lint:
	poetry run ruff check src tests
	poetry run mypy src/novita_sandbox

# Tests
test-core:
	poetry run python -m pytest -v --tb=long src/novita_sandbox/core/tests/

test-code-interpreter:
	poetry run python -m pytest -v --tb=long src/novita_sandbox/code_interpreter/tests/

test-desktop:
	poetry run python -m pytest -v --tb=long src/novita_sandbox/desktop/tests/

test:
	make test-core
	make test-code-interpreter
	make test-desktop

build:
	poetry install
	poetry check
	poetry build

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	@echo "Cleanup completed!"
