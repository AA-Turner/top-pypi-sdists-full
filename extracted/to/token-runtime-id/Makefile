.PHONY: setup lint tests pyright validate clean help

help:
	@echo "Available commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make lint      - Run pylint"
	@echo "  make tests     - Run pytest with coverage"
	@echo "  make pyright   - Run pyright type checker"
	@echo "  make validate  - Run lint, tests, and pyright"

setup:
	uv sync --all-extras --dev

lint:
	uv run pylint src/ tests/

tests:
	uv run pytest --cov=token_runtime_id --cov-report=term-missing --cov-report=html --cov-fail-under=100

pyright:
	uv run pyright

validate: lint pyright tests
	@echo "All validation checks passed!"

build:
	rm -rf dist
	python -m build
	twine check dist/*

publish-test: build
	python -m twine upload --repository testpypi dist/*
	@echo "Published to TestPyPI!"

publish: build
	python -m twine upload dist/*
	@echo "Published to PyPI!"
