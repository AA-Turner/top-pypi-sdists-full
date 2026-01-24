.PHONY: default clean install install-dev pip-install generate generate-local retrieve-schema transform-schema format-schema update-test-schema customize-schema env-check-venv test sanity-check
.SILENT: generate generate-local # Prevent echoing of any tokens

PACKAGE_NAME=pycarlo
ENVIRONMENT_NAME=venv
MCD_URL=https://api.getmontecarlo.com/graphql

# Schema generator util
SCHEMA_GEN_UTIL=utils/generate.py
SANITY_CHECK_UTIL=utils/sanity.py
ENV_UTIL=utils/env.sh
ENV_FILE=utils/.env
SAMPLE_ENV_FILE=utils/sample.env

# Generated schema destinations
SCHEMA_FROM_INTROSPECTION=$(PACKAGE_NAME)/lib/schema.json
SCHEMA_PY=$(PACKAGE_NAME)/lib/schema.py
SCHEMA_TEST_DATA=tests/data/schema_original.py

default:
	@echo "Refer to CONTRIBUTING.md for details on common tasks."

clean:
	@echo "Cleaning up existing build artifacts..."; \
	rm -rf $(ENVIRONMENT_NAME) build dist $(PACKAGE_NAME).egg-info .coverage nosetests.xml

pip-install:
	@echo "\nInstalling Python package in editable mode..."; \
	pip install --editable .

install: clean
ifeq ("$(wildcard $(ENV_FILE))","")
	@echo "\nCreating env file from sample..."; \
	cp $(SAMPLE_ENV_FILE) $(ENV_FILE)
endif
	@echo "\nCreating virtual environment..."; \
	python3 -m venv $(ENVIRONMENT_NAME);
	@echo "\nInstalling dependencies..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-dev.txt; \
	$(MAKE) pip-install; \
	pip show $(PACKAGE_NAME)

# Full development setup = install + pre-commit hooks
install-dev: install
	@echo "\nInstalling pre-commit hooks..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pre-commit install; \
	echo ""; \
	echo "\033[0;32m✅ Development environment ready!\033[0m"; \
	echo "\nActivate with: . $(ENVIRONMENT_NAME)/bin/activate"

sanity-check: env-check-venv
	@echo "\nRunning sanity checks..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	sh $(ENV_UTIL) python $(SANITY_CHECK_UTIL); \

# Requires .env or profile credentials setup before usage.
retrieve-schema:
	@echo "\nRetrieving latest schema..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	sh $(ENV_UTIL) python $(SCHEMA_GEN_UTIL) $(MCD_URL) $(SCHEMA_FROM_INTROSPECTION);

# Expects $(SCHEMA_FROM_INTROSPECTION) to already exist.
transform-schema:
	@echo "\nGenerating Python types from schema.json..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	sgqlc-codegen schema --docstrings $(SCHEMA_FROM_INTROSPECTION) $(SCHEMA_PY);

format-schema:
	@echo "\nFormatting Python code..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	ruff format $(SCHEMA_PY);

update-test-schema:
	@echo "\nUpdating test data with original schema..."; \
	mkdir -p tests/data; \
	cp $(SCHEMA_PY) $(SCHEMA_TEST_DATA);

customize-schema:
	@echo "\nApplying schema customizations..."; \
	if [ "$$(uname)" = "Darwin" ]; then \
		sed -i '' 's/class Connection(sgqlc.types.relay.Connection):/class Connection(sgqlc.types.Type):/g' $(SCHEMA_PY); \
		sed -i '' 's/import sgqlc.types$$/import sgqlc.types\nimport pycarlo.lib.types/g' $(SCHEMA_PY); \
		sed -i '' 's/class \([A-Za-z0-9_]*\)(sgqlc.types.Enum):/class \1(pycarlo.lib.types.Enum):/g' $(SCHEMA_PY); \
	else \
		sed -i 's/class Connection(sgqlc.types.relay.Connection):/class Connection(sgqlc.types.Type):/g' $(SCHEMA_PY); \
		sed -i 's/import sgqlc.types$$/import sgqlc.types\nimport pycarlo.lib.types/g' $(SCHEMA_PY); \
		sed -i 's/class \([A-Za-z0-9_]*\)(sgqlc.types.Enum):/class \1(pycarlo.lib.types.Enum):/g' $(SCHEMA_PY); \
	fi; \
	echo "*************"; \
	echo "The following schema customizations have been applied:"; \
	echo "  1. Changed 'class Connection(sgqlc.types.relay.Connection)' to 'class Connection(sgqlc.types.Type)'"; \
	echo "  2. Changed all Enum classes to use 'pycarlo.lib.types.Enum' for backward compatibility"; \
	echo "*************"; \

env-check-venv:
	@if [ ! -d "$(ENVIRONMENT_NAME)" ]; then \
		echo "\033[0;31m❌ Error: Virtual environment not found. Please run 'make install' first.\033[0m"; \
		exit 1; \
	fi

# Generate schema from existing schema.json (skip retrieval).
# Used by CI when schema.json is already provided.
generate-local: env-check-venv transform-schema format-schema update-test-schema customize-schema
	@echo "\n\033[0;32m✅ Schema generation complete!\033[0m";

# Requires .env or profile credentials setup before usage.
generate: env-check-venv retrieve-schema generate-local

test: env-check-venv
	@echo "\nRunning tests..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	export DEBUG=True; \
	pytest --durations=5 ./tests; \
	echo ""; \
	echo "Linting and formatting..."; \
	ruff check .; \
	ruff format --check .; \
	echo ""; \
	echo "Type checking..."; \
	pyright .
	@echo "\n\033[0;32m✅ All tests and checks passed!\033[0m";

# this is only used by CI. See circleci/config.yml:
distribute: install
	@echo "\nInstalling dependencies..."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-ci.txt; \
	echo "\nRunning setup..."; \
	python setup.py sdist bdist_wheel; \
	echo "\nChecking distribution..."; \
	twine check dist/*; \
	echo "\nUploading distribution to PyPI..."; \
	twine upload --non-interactive dist/*
