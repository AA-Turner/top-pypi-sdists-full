.PHONY: default clean install pip-install generate env-check test install-with-tests sanity-check
.SILENT: generate # Prevent echoing of any tokens

PACKAGE_NAME=pycarlo
ENVIRONMENT_NAME=venv
MCD_URL=https://api.getmontecarlo.com/graphql

# Schema generator util
SCHEMA_GEN_UTIL=utils/generate.py
SANITY_CHECK_UTIL=utils/sanity.py
ENV_UTIL=utils/env.sh
ENV_FILE=utils/.env
SAMPLE_ENV_FILE=utils/sample.env

# Generated schema destinations
SCHEMA_FROM_INTROSPECTION=$(PACKAGE_NAME)/lib/schema.json
SCHEMA_PY=$(PACKAGE_NAME)/lib/schema.py

default:
	@echo "Read the readme"

clean:
	rm -rf $(ENVIRONMENT_NAME) build dist $(PACKAGE_NAME).egg-info .coverage nosetests.xml

pip-install:
	pip install --editable .

install: clean
ifeq ("$(wildcard $(ENV_FILE))","")
	cp $(SAMPLE_ENV_FILE) $(ENV_FILE)
endif
	virtualenv $(ENVIRONMENT_NAME); \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-dev.txt; \
	$(MAKE) pip-install; \
	pip show $(PACKAGE_NAME)

sanity-check:
	. $(ENVIRONMENT_NAME)/bin/activate; \
	sh $(ENV_UTIL) python $(SANITY_CHECK_UTIL); \

generate: install
	# Generate sgqlc.types from introspection.
	# Requires exporting API ID/Secret before usage.
	echo "Retrieving latest schema."; \
	. $(ENVIRONMENT_NAME)/bin/activate; \
	sh $(ENV_UTIL) python $(SCHEMA_GEN_UTIL) $(MCD_URL) $(SCHEMA_FROM_INTROSPECTION); \
	echo "Generating types."; \
	sgqlc-codegen schema --docstrings $(SCHEMA_FROM_INTROSPECTION) $(SCHEMA_PY) ; \
	echo "Formatting python code."; \
	ruff format $(SCHEMA_PY) ; \
	echo "Executing sanity check."; \
	sed -i '' 's/class Connection(sgqlc.types.relay.Connection):/class Connection(sgqlc.types.Type):/g' $(SCHEMA_PY); \
	$(MAKE) sanity-check; \
	echo "*************"; \
	echo "!!!WARNING!!!: due to how sgqlc generates the schema, we updated change '$(SCHEMA_PY)' by changing 'class Connection(sgqlc.types.relay.Connection)' to 'class Connection(sgqlc.types.Type)'."; \
	echo "For additional information check https://github.com/monte-carlo-data/python-sdk/pull/63"; \

	echo "*************"; \
	echo "Done! Have a nice day."; \

test:
	@# Requires activating the virtualenv created in `install` if running locally.
	export DEBUG=True; pytest --durations=5 ./tests
	ruff format --check .
	ruff check .
	pyright .

install-with-tests: install
	. $(ENVIRONMENT_NAME)/bin/activate; $(MAKE) test

distribute: install
	. $(ENVIRONMENT_NAME)/bin/activate; \
	pip install -r requirements-ci.txt; \
	python setup.py sdist bdist_wheel; \
	twine check dist/*; \
	twine upload --non-interactive dist/*

env-check:
	sh $(ENV_UTIL)
