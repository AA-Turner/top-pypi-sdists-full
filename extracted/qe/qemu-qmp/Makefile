QEMU_VENV_DIR=.dev-venv
QEMU_MINVENV_DIR=.min-venv
QEMU_TOX_EXTRA_ARGS ?=

.PHONY: help
help:
	@echo "python packaging help:"
	@echo ""
	@echo "make check-minreqs:"
	@echo "    Run tests in the minreqs virtual environment."
	@echo "    These tests use the oldest dependencies."
	@echo "    Requires: Python 3.8"
	@echo "    Hint (Fedora): 'sudo dnf install python3.8'"
	@echo ""
	@echo "make check-tox:"
	@echo "    Run tests against multiple python versions."
	@echo "    These tests use the newest dependencies."
	@echo "    Requires: Python 3.8 - 3.14, and tox."
	@echo "    Hint (Fedora): 'sudo dnf install python3-tox python3.14'"
	@echo "    The variable QEMU_TOX_EXTRA_ARGS can be use to pass extra"
	@echo "    arguments to tox".
	@echo ""
	@echo "make check-dev:"
	@echo "    Run tests in a venv against your default python3 version."
	@echo "    These tests use the newest dependencies."
	@echo "    Requires: Python 3.x"
	@echo ""
	@echo "make check:"
	@echo "    Run tests in your *current environment*."
	@echo "    Performs no environment setup of any kind."
	@echo ""
	@echo "make develop:"
	@echo "    Install deps needed for 'make check',"
	@echo "    and install the qemu.qmp package in editable mode."
	@echo "    (Can be used in or outside of a venv.)"
	@echo ""
	@echo "make min-venv"
	@echo "    Creates the minreqs virtual environment ($(QEMU_MINVENV_DIR))"
	@echo ""
	@echo "make dev-venv"
	@echo "    Creates a simple venv for check-dev. ($(QEMU_VENV_DIR))"
	@echo ""
	@echo "make clean:"
	@echo "    Remove package build output."
	@echo ""
	@echo "make distclean:"
	@echo "    remove venv files, qemu.qmp package forwarder,"
	@echo "    built distribution files, and everything from 'make clean'."
	@echo ""
	@echo -e "Have a nice day ^_^\n"

.PHONY: pipenv check-pipenv
pipenv check-pipenv:
	@echo "pipenv was dropped; try 'make check-minreqs' or 'make min-venv'"
	@exit 1

PIP_INSTALL = pip install --disable-pip-version-check
.PHONY: min-venv
min-venv: $(QEMU_MINVENV_DIR) $(QEMU_MINVENV_DIR)/bin/activate
$(QEMU_MINVENV_DIR) $(QEMU_MINVENV_DIR)/bin/activate: setup.cfg tests/minreqs.txt
	@echo "VENV $(QEMU_MINVENV_DIR)"
	@python3.8 -m venv $(QEMU_MINVENV_DIR)
	@(								\
		echo "ACTIVATE $(QEMU_MINVENV_DIR)";			\
		. $(QEMU_MINVENV_DIR)/bin/activate;			\
		echo "Ensure pip supports editable installs"; 		\
		$(PIP_INSTALL) 'pip>=21.3';				\
		echo "INSTALL wheel $(QEMU_MINVENV_DIR)";               \
		$(PIP_INSTALL) wheel 1>/dev/null;		               \
		echo "INSTALL -r tests/minreqs.txt $(QEMU_MINVENV_DIR)";\
		$(PIP_INSTALL) -r tests/minreqs.txt 1>/dev/null;	\
		echo "INSTALL -e qemu $(QEMU_MINVENV_DIR)";		\
		$(PIP_INSTALL) -e . --config-settings=editable_mode=compat 1>/dev/null;			\
	)
	@touch $(QEMU_MINVENV_DIR)

.PHONY: check-minreqs
check-minreqs: min-venv
	@(							\
		echo "ACTIVATE $(QEMU_MINVENV_DIR)";		\
		. $(QEMU_MINVENV_DIR)/bin/activate;		\
		make check;					\
	)

.PHONY: dev-venv
dev-venv: $(QEMU_VENV_DIR) $(QEMU_VENV_DIR)/bin/activate
$(QEMU_VENV_DIR) $(QEMU_VENV_DIR)/bin/activate: setup.cfg
	@echo "VENV $(QEMU_VENV_DIR)"
	@python3 -m venv $(QEMU_VENV_DIR)
	@(								\
		echo "ACTIVATE $(QEMU_VENV_DIR)";			\
		. $(QEMU_VENV_DIR)/bin/activate;			\
		echo "INSTALL qemu.qmp[devel] $(QEMU_VENV_DIR)";	\
		make develop 1>/dev/null;				\
	)
	@touch $(QEMU_VENV_DIR)

.PHONY: check-dev
check-dev: dev-venv
	@(							\
		echo "ACTIVATE $(QEMU_VENV_DIR)";		\
		. $(QEMU_VENV_DIR)/bin/activate;		\
		make check;					\
	)

.PHONY: develop
develop:
	$(PIP_INSTALL) -e .[devel] --config-settings=editable_mode=compat

.PHONY: check
check:
	@pytest -v tests/*.py

.PHONY: check-tox
check-tox:
	@tox $(QEMU_TOX_EXTRA_ARGS)

.PHONY: check-coverage
check-coverage:
	@coverage run -m pytest tests/*.py
	@coverage combine
	@coverage html
	@coverage xml
	@coverage report

.PHONY: clean
clean:
	make -C docs clean

.PHONY: distclean
distclean: clean
	rm -rf qemu.qmp.egg-info/ dist/ build/
	rm -rf $(QEMU_VENV_DIR) $(QEMU_MINVENV_DIR) .tox/
	rm -f .coverage coverage.xml .coverage.*
	rm -rf htmlcov/ test-results/

.PHONY: docs
docs:
	make -C docs html

.PHONY: tag
tag:
	python3 scripts/package.py tag

dist: setup.cfg MANIFEST.in README.rst scripts/package.py
	python3 scripts/package.py build

.PHONY: test-publish
test-publish:
	python3 scripts/package.py publish --test

.PHONY: publish
publish:
	python3 scripts/package.py publish
