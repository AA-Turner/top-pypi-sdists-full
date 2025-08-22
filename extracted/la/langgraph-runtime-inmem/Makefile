.PHONY: lint format check-version check-base-imports

# lint commands

lint:
	uv run ruff check .
	uv run ruff format . --diff

format:
	uv run ruff check --fix .
	uv run ruff format .

VERSION_KIND ?= patch

bump-version:
	uv run --with hatch hatch version $(VERSION_KIND)


check-base-imports:
	DATABASE_URI="foo" REDIS_URI="bar" uv run python -c "from langgraph_runtime_inmem import *"