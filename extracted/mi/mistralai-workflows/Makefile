 # See http://go/std-makefile to get an understanding of common Makefile targets used throughout the project

.PHONY: onboarding lint format typecheck check-api-surface test integration-tests dev installdeps lock

# xdist worker count for integration-tests. `auto` is what the invoke task
# defaults to, but with psutil importable xdist resolves it to *physical*
# cores, which is half the vCPU a Buildkite step reserves. CI exports
# PYTEST_WORKERS=logical, and `?=` lets that environment value win.
PYTEST_WORKERS ?= auto

onboarding:
	@echo "🛠️  Setting up workflow_sdk..."
	@$(MAKE) installdeps
	@echo "✅ workflow_sdk automated onboarding complete. You may still have some manual steps to tackle!"

lint:
	uv run invoke lint

format:
	uv run invoke lint --fix

typecheck:
	uv run invoke typecheck

check-api-surface:
	uv run invoke check-api-surface --base-ref $(or $(BASE_REF),origin/main)

test:
	uv run invoke tests

integration-tests:
	uv run invoke integration-tests -v -n $(PYTEST_WORKERS)

dev:
	@echo "Development environment setup"
	@echo "Run 'uv sync' to install dependencies"

installdeps:
	uv sync

lock:
	uv run invoke lock
