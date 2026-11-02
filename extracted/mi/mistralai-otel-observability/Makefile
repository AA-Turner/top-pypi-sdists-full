.PHONY: lint format typecheck test install build clean

lint: format typecheck
	uv run ruff check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run basedpyright

test:
	uv run pytest

install:
	uv sync

clean:
	rm -rf dist/

build: clean
	uv build
