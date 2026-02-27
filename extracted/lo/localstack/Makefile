.PHONY: install test test-unit test-integration lint clean entrypoints

VENV_DIR ?= .venv
PYTHON ?= python3

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip setuptools wheel

install: venv
	$(VENV_DIR)/bin/pip install -e ".[dev]"
	$(VENV_DIR)/bin/python -m plux entrypoints
	$(VENV_DIR)/bin/pip install -e .

test: install
	$(VENV_DIR)/bin/pytest tests/ -v --log-cli-level=WARNING

test-unit: install
	$(VENV_DIR)/bin/pytest tests/unit/ -v --log-cli-level=WARNING

test-cli: install
	$(VENV_DIR)/bin/pytest tests/cli/ -v --log-cli-level=WARNING

lint: install
	$(VENV_DIR)/bin/ruff check localstack_cli tests
	$(VENV_DIR)/bin/ruff format --check localstack_cli tests

format: install
	$(VENV_DIR)/bin/ruff check --fix localstack_cli tests
	$(VENV_DIR)/bin/ruff format localstack_cli tests

entrypoints: install
	$(VENV_DIR)/bin/python -m plux entrypoints
	@test -s plux.ini || (echo "Entrypoints not created correctly!" && exit 1)

clean:
	rm -rf $(VENV_DIR)
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
