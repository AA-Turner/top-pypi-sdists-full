.PHONY: lint format typecheck test test-mistralai-v2 install build clean

lint: format typecheck
	uv run ruff check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run basedpyright

# The mistral extra supports mistralai 3.x (locked) and 2.x: test both.
test: test-mistralai-v2
	uv run pytest

test-mistralai-v2:
	uv run --with "mistralai>=2.5.2,<3" pytest

install:
	uv sync

clean:
	rm -rf dist/

build: clean
	uv build
