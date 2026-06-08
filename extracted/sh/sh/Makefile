# runs all tests on all envs, in parallel
.PHONY: test
test:
	uv run tox -p

# one test on all envs, in parallel
.PHONY: test_one
test_one:
	uv run tox -p -- $(test)

# publishes to PyPI
.PHONY: release
release:
	uv build && uv publish --dry-run