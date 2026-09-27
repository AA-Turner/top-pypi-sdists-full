.PHONY: test lint

test:
	uv run --with pytest pytest

lint:
	uv run --dev pre-commit run --all-files
