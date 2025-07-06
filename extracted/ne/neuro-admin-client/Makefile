SHELL := /bin/bash

ISORT_TARGETS := neuro_admin_client tests
BLACK_TARGETS := $(ISORT_TARGETS)
MYPY_TARGETS :=  $(ISORT_TARGETS)
FLAKE8_TARGETS:= $(ISORT_TARGETS)


setup:
	pip install -U pip
	pip install -r requirements.txt
	pre-commit install

format:
ifdef CI_LINT_RUN
	pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files
endif


lint: format
	mypy $(MYPY_TARGETS)

test:
	pytest --cov=neuro_admin_client --cov-report xml:.coverage.xml tests
