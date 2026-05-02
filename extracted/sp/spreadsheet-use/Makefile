SHELL := /bin/bash
.DEFAULT_GOAL := help

# Variables
PYTHON ?= python
TAG_PREFIX ?= v
VERSION ?=

.PHONY: help setup setup-dev test clean build check tag preview-upload release-upload dev-graph build-univer build-spreadsheet build-both

help: ## Show this help
	@echo "Available targets:"
	@awk -F':.*?## ' '/^[a-zA-Z0-9_.-]+:.*?## /{printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)


setup: ## Install project deps (and dev deps) using uv
	uv sync --group dev

setup-dev: setup ## Alias for setup (kept for clarity)

test: ## Run tests with pytest
	uv run pytest -q

dev-graph: ## Start local LangGraph dev server
	langgraph dev --config examples/sheet_edit/langgraph.json --debug-port 5678 --allow-blocking

clean: ## Remove build/test artifacts
	rm -rf dist build *.egg-info .pytest_cache pyproject.toml.backup

build: clean ## Build sdist and wheel using PEP 517
	$(PYTHON) -m pip install -U build twine hatchling hatch-vcs
	$(PYTHON) -m build

check: ## Check package metadata (long description, etc.)
	$(PYTHON) -m twine check dist/*

tag: ## Create an annotated git tag from VERSION (e.g., 0.1.0a1)
	@if [ -z "$(VERSION)" ]; then echo "Usage: make tag VERSION=0.1.0a1"; exit 1; fi
	git tag -a $(TAG_PREFIX)$(VERSION) -m "Release $(VERSION)"

preview-upload: ## Upload built artifacts to PyPI (pre-releases allowed; set TWINE_USERNAME=__token__ and TWINE_PASSWORD)
	$(PYTHON) -m twine upload dist/*

release-upload: ## Upload built artifacts to PyPI (set TWINE_USERNAME=__token__ and TWINE_PASSWORD)
	$(PYTHON) -m twine upload dist/*

build-univer: clean ## Build univer-use package only
	@echo "🏗️ Building univer-use package..."
	uv pip install -U build twine hatchling hatch-vcs
	$(PYTHON) -m build
	$(PYTHON) -m twine check dist/*
	@echo "✅ univer-use package built successfully"

build-spreadsheet: ## Build spreadsheet-use package only (preserves existing dist files). Use VERSION=x.y.z to pin dependency
	@echo "🏗️ Building spreadsheet-use package..."
	@echo "📋 Backing up current pyproject.toml..."
	cp pyproject.toml pyproject.toml.backup
	cp pyproject-spreadsheet.toml pyproject.toml
	@if [ -n "$(VERSION)" ]; then \
		echo "🔧 Setting dependency to univer-use==$(VERSION)"; \
		sed -i '' "s/univer-use>=0\.1\.0/univer-use==$(VERSION)/" pyproject.toml; \
	fi
	$(PYTHON) -m build
	$(PYTHON) -m twine check dist/spreadsheet_use-*
	@echo "🔄 Restoring original pyproject.toml..."
	mv pyproject.toml.backup pyproject.toml
	@echo "✅ spreadsheet-use package built successfully"

build-both: build-univer build-spreadsheet ## Build both univer-use and spreadsheet-use packages
