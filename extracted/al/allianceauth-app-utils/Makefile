appname = allianceauth-app-utils
package = app_utils

help:
	@echo "Makefile for $(appname)"

coverage:
	coverage run ../myauth/manage.py test utils_test_app.tests --keepdb --failfast && coverage html && coverage report -m

test:
	# runs a full test incl. re-creating of the test DB
	python ../myauth/manage.py test $(package) --failfast --debug-mode -v 2

pylint:
	pylint $(package)

check_complexity:
	flake8 $(package) --max-complexity=10

flake8:
	flake8 $(package) --count
