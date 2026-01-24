.PHONY: help install install-dev test lint format clean build publish run-api

help:
	@echo "Comp-LEO SDK - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install package"
	@echo "  make install-dev      Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test            Run tests"
	@echo "  make lint            Run linters"
	@echo "  make format          Format code"
	@echo "  make check-existing  Test on existing Leo code"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  make build           Build distribution"
	@echo "  make publish         Publish to PyPI"
	@echo "  make clean           Clean build artifacts"
	@echo ""
	@echo "Run:"
	@echo "  make run-api         Start API server"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,api]"

test:
	pytest tests/ -v --cov=comp_leo --cov-report=html --cov-report=term

lint:
	ruff check comp_leo/
	mypy comp_leo/

format:
	black comp_leo/ tests/
	ruff check --fix comp_leo/

check-existing:
	python examples/test_existing_code.py

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	python -m build

publish: build
	twine upload dist/*

run-api:
	python -m comp_leo.api.main

# Quick development workflow
dev: install-dev format test
	@echo "✅ Development environment ready"

# Pre-commit checks
pre-commit: format lint test
	@echo "✅ Pre-commit checks passed"
