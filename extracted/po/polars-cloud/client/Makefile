.DEFAULT_GOAL := help

SHELL=bash
ifeq ($(VENV),)
VENV=../.venv
endif

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    VENV_FOLDER := Scripts
else
    VENV_FOLDER := bin
endif
VENV_BIN=$(VENV)/$(VENV_FOLDER)

.PHONY: .venv
.venv:  ## Set up virtual environment and install requirements
	@$(MAKE) -s -C .. $@

.PHONY: build
build: .venv  ## Compile and install Python Polars Cloud for development
	@unset CONDA_PREFIX \
	&& MATURIN_PEP517_ARGS="--profile dev" $(VENV_BIN)/maturin develop --uv $(ARGS) \

.PHONY: build-mindebug
build-mindebug: .venv  ## Same as build, but don't include full debug information
	@unset CONDA_PREFIX \
	&& $(VENV_BIN)/maturin develop --uv --profile mindebug-dev $(ARGS) \

.PHONY: build-release
build-release: .venv  ## Compile and install Python Polars Cloud binary with optimizations, with minimal debug symbols
	@unset CONDA_PREFIX \
	&& $(VENV_BIN)/maturin develop --uv --release $(ARGS) \

.PHONY: build-nodebug-release
build-nodebug-release: .venv  ## Same as build-release, but without any debug symbols at all (a bit faster to build)
	@unset CONDA_PREFIX \
	&& $(VENV_BIN)/maturin develop --uv --profile nodebug-release $(ARGS) \

.PHONY: build-debug-release
build-debug-release: .venv  ## Same as build-release, but with full debug symbols turned on (a bit slower to build)
	@unset CONDA_PREFIX \
	&& $(VENV_BIN)/maturin develop --uv --profile debug-release $(ARGS) \

.PHONY: build-dist-release
build-dist-release: .venv  ## Compile and install Python Polars binary with super slow extra optimization turned on, for distribution
	@unset CONDA_PREFIX \
	&& $(VENV_BIN)/maturin develop --uv --profile dist-release $(ARGS) \

.PHONY: fmt
fmt:  ## Run ruff, typos and dprint
	$(VENV_BIN)/ruff check
	$(VENV_BIN)/ruff format
	dprint fmt
	cargo fmt --all

.PHONY: check
check: ## Run Mypy
	@$(VENV_BIN)/mypy
	@$(VENV_BIN)/mypy ../compute-plane/tests/integration

.PHONY: test
test:  ## Run all tests
	@$(VENV_BIN)/pytest . -m 'not slow'

.PHONY: test-cov
test-cov:  ## Run all tests
	@$(VENV_BIN)/pytest tests/unit --cov

.PHONY: test-client
test-client:  ## Run tests for the client
	@$(VENV_BIN)/pytest tests/unit -m 'not slow'

.PHONY: test-integration
test-integration: ## Run AWS integration tests sequentially with logs
	@$(VENV_BIN)/pytest -n0 -s tests/integration $(ARGS)

.PHONY: test-integration-parallel
test-integration-parallel: ## Run AWS integration tests in parallel (no logs)
	@$(VENV_BIN)/pytest -n auto -v -s tests/integration $(ARGS)

.PHONY: clippy
clippy:  ## Run check with all features
	cargo clippy --all-targets -- -W clippy::dbg_macro $(CLIPPY_FLAGS)

.PHONY: shear
shear:
	cargo shear --fix

.PHONY: pre-commit shear
pre-commit: fmt check

.PHONY: docs
docs: .venv  ## Build Python docs (incremental)
	@$(MAKE) -s -C docs html

.PHONY: docs-clean
docs-clean: .venv  ## Build Python docs (full rebuild)
	@$(MAKE) -s -C docs clean
	@$(MAKE) docs

.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort
