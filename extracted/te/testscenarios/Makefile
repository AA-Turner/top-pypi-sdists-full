PYTHONPATH:=$(shell pwd):${PYTHONPATH}
PYTHON ?= python3

all: check

check:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m testtools.run \
	    testscenarios.test_suite

clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f

TAGS: testscenarios/*.py tests/*.py
	ctags -e -R testscenarios/ tests/

tags: testscenarios/*.py tests/*.py
	ctags -R testscenarios/ tests/

.PHONY: all check
