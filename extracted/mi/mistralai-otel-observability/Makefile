.PHONY: lint format typecheck test test-mistralai-v3 install build clean

lint: format typecheck
	uv run ruff check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run basedpyright

# The mistral extra supports mistralai 2.x (locked) and 3.x: test both.
test: test-mistralai-v3
	uv run pytest

test-mistralai-v3:
	uv run --with "mistralai>=3,<4" pytest

install:
	uv sync

clean:
	rm -rf dist/

build: clean
	uv build
