.PHONY: default clean pip-install install test install-with-tests distribute

PACKAGE_NAME=airflow-mcd
PY_FRIENDLY_PACKAGE_NAME=airflow_mcd
ENVIRONMENT_NAME=venv

default:
	@echo "Read the readme"

clean:
	rm -rf $(ENVIRONMENT_NAME) build dist *.egg-info .coverage .tox coverage.xml

pip-install:
	pip install --editable .

install: clean
	virtualenv $(ENVIRONMENT_NAME); \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	python -m pip install --upgrade pip setuptools wheel; \
	pip install -r requirements-dev.txt; \
	$(MAKE) pip-install; \
	pip show $(PACKAGE_NAME)

test:
	@# Run tests using tox for multiple Python and Airflow version combinations
	@# These suppressed warnings are all from the Airflow package :/.
	export DEBUG=True; PYTHONWARNINGS="ignore::DeprecationWarning" PYTHONWARNINGS="ignore::FutureWarning" \
		tox

install-with-tests: install
	. $(ENVIRONMENT_NAME)/bin/activate; $(MAKE) test

package: install
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-ci.txt; \
	python setup.py sdist bdist_wheel;

distribute: package
	. $(ENVIRONMENT_NAME)/bin/activate; \
	twine check dist/*; \
	twine upload --non-interactive dist/*
