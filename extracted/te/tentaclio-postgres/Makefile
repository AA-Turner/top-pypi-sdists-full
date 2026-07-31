
# Help
.PHONY: help

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Local installation
.PHONY: reset clean lock update sync

reset: clean sync

clean: ## Remove all the unwanted clutter
	find src -type d -name __pycache__ | xargs rm -rf
	find src -type d -name '*.egg-info' | xargs rm -rf
	uv clean

lock: ## Lock dependencies
	uv lock

update: ## Update dependencies (whole tree)
	uv lock --upgrade

sync: ## Install dependencies as per the lock file
	uv sync --all-extras


# Linting and formatting

.PHONY: lint format

lint: ## Lint files with flake and mypy
	uv run flake8 src tests
	uv run mypy src tests
	uv run black --check src tests
	uv run isort --check-only src tests

format: ## Run black and isort
	uv run black src tests
	uv run isort src tests


# Testing

.PHONY: unit functional

unit: ## Run unit tests
	uv run pytest tests/unit

functional:
	uv run pytest tests/functional/postgres


# Release

.PHONY: package check-release release

package:
	uv build

check-release: package
	uv publish --dry-run

release: package
	uv publish
