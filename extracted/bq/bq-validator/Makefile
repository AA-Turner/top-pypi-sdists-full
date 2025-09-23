# Set up an environment
.PHONEY: setup
setup: setup-python

.PHONEY: setup-python
setup-python:
	bash ./dev/setup.sh --deps "development"

# Check all the coding style.
.PHONY: lint
lint:
	trunk check -a

# Check the coding style for the shell scripts.
.PHONY: lint-shell
lint-shell:
	shellcheck ./dev/*.sh

.PHONEY: format
format:
	trunk fmt -a


# Run the unit tests.
.PHONEY: test
test:
	uv run bash ./dev/test_python.sh

# Build the package
build: clean test
	uv build

clean:
	bash ./dev/clean.sh

# Publish to pypi
publish:
	bash ./dev/publish.sh "pypi"

# Publish to testpypi
test-publish:
	bash ./dev/publish.sh "testpypi"
