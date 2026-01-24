.PHONY: default clean install pip-install test install-with-tests distribute generate-docs publish-docs
ENVIRONMENT_NAME=venv
DOCS_PATH=./docs/_build/html

default:
	@echo "Read the readme"

clean:
	rm -rf $(ENVIRONMENT_NAME) build dist montecarlodata.egg-info .coverage nosetests.xml

install: clean
	virtualenv $(ENVIRONMENT_NAME); \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install setuptools; \
	pip install -r requirements-dev.txt; \
	$(MAKE) pip-install; \
	montecarlo --version

pip-install:
	pip install --editable .

format:
	. $(ENVIRONMENT_NAME)/bin/activate; python -m ruff format

test:
	@# Requires activating the virtualenv created in `install` if running locally
	export DEBUG=True; unset MCD_USER_ID_HEADER; coverage run -m pytest ./tests

lint:
	. $(ENVIRONMENT_NAME)/bin/activate; \
	python -m ruff format; \
	python -m ruff check --fix --exit-non-zero-on-fix; \
	env PYRIGHT_PYTHON_FORCE_VERSION="latest" python -m pyright


install-with-tests: install
	. $(ENVIRONMENT_NAME)/bin/activate; $(MAKE) test

install-with-tests-and-lint: install-with-tests
	. $(ENVIRONMENT_NAME)/bin/activate; $(MAKE) lint

# installs the package and runs "montecarlo --version" in an environment that simulates
# the end user's environment, no setuptools and no dev packages installed
install-with-end-user-tests: clean
	virtualenv $(ENVIRONMENT_NAME); \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	$(MAKE) pip-install; \
	montecarlo --version

distribute: install
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-ci.txt; \
	python setup.py sdist bdist_wheel; \
	twine check dist/*; \
	twine upload --non-interactive dist/*

generate-docs: install
	. $(ENVIRONMENT_NAME)/bin/activate && \
	pip install -r requirements-ci.txt && \
	make -C docs clean && \
	make -C docs html && \
	cp -a ./docs/_static/. $(DOCS_PATH)

publish-docs: generate-docs
	aws s3 cp $(DOCS_PATH)/ s3://${CLI_DOCS_BUCKET} --recursive
	AWS_MAX_ATTEMPTS=10 aws cloudfront create-invalidation --distribution-id=${CLI_DOCS_CLOUDFRONT_DIST} --paths "/*" --no-cli-pager
