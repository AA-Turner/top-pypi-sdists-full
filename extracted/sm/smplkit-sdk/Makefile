VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# The smplkit-sdk package is intentionally NOT installed in this venv
# (not even as an editable install) — per the universal CLAUDE.md
# rule "no editable installs anywhere" and because the package source
# lives right here. Tests use ``pythonpath = ["src"]`` (see
# pyproject.toml); showcases run with ``PYTHONPATH=src`` so
# ``from smplkit import ...`` resolves to the source tree.
# Quoted so the shell doesn't interpret ``>=`` as a redirect. Without
# the quotes, ``pip install pytest>=7.0 …`` invocations silently
# redirect to files named ``=7.0`` etc. in the repo root instead of
# passing the constraints to pip — see commit c6e24da for the cleanup.
DEV_DEPS := \
	'openapi-python-client>=0.21.0,<0.29.0' \
	'pytest>=7.0' \
	'pytest-cov>=4.0' \
	'ruff>=0.4.0' \
	'loguru>=0.7.0'

SHOWCASE_RUN := PYTHONPATH=src $(PYTHON)

.PHONY: install generate test lint \
	config_runtime_showcase config_management_showcase \
	flags_runtime_showcase flags_management_showcase \
	logging_runtime_showcase logging_management_showcase \
	audit_runtime_showcase audit_management_showcase \
	jobs_showcase

install:
	$(PIP) install --upgrade $(DEV_DEPS)

generate:
	bash scripts/generate.sh

test:
	$(PYTHON) -m pytest --cov=smplkit --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check src/ tests/

config_runtime_showcase:
	$(SHOWCASE_RUN) examples/config_runtime_showcase.py

config_management_showcase:
	$(SHOWCASE_RUN) examples/config_management_showcase.py

flags_runtime_showcase:
	$(SHOWCASE_RUN) examples/flags_runtime_showcase.py

flags_management_showcase:
	$(SHOWCASE_RUN) examples/flags_management_showcase.py

logging_runtime_showcase:
	$(SHOWCASE_RUN) examples/logging_runtime_showcase.py

logging_management_showcase:
	$(SHOWCASE_RUN) examples/logging_management_showcase.py

audit_runtime_showcase:
	$(SHOWCASE_RUN) examples/audit_runtime_showcase.py

audit_management_showcase:
	$(SHOWCASE_RUN) examples/audit_management_showcase.py

jobs_showcase:
	$(SHOWCASE_RUN) examples/jobs_showcase.py
