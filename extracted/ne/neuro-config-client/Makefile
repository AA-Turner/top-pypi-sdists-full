setup:
	pip install -U pip
	pip install -r requirements.txt
	pre-commit install

lint: format
	mypy neuro_config_client tests

format:
ifdef CI_LINT_RUN
	SKIP=actionlint-docker pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files
endif

test:
	pytest -vv tests
