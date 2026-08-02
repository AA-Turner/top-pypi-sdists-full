.PHONY: help clean clean-all clean-pyc clean-build clean-caches lint test upload readme

help:
	@echo "clean - remove Python file & build artifacts"
	@echo "lint - run linters to check the code style and formatting"
	@echo "test - run tests with the default Python"
	@echo "upload - release package to PyPI"
	@echo "readme - render & upload readme to SourceHut"

clean: clean-build clean-pyc

clean-all: clean clean-caches

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr src/*.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name __pycache__ -type d -exec rmdir {} +
	rm -fr .cache/

clean-caches:
	rm -fr .eggs/
	rm -fr .hypothesis/
	rm -fr .pytest_cache/

lint:
	flake8 src tests
	black --check .
	isort --check src tests

test:
	pytest

upload:
	flit publish

README.html: README.rst CONTRIBUTING.rst
	cat $^ | pandoc --no-highlight -f rst -o $@

readme: README.html
	hut git update --readme $<
