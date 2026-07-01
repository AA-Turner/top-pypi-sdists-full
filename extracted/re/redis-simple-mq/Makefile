appname = redis-simple_mq
package = simple_mq

help:
	@echo "Makefile for $(appname)"

coverage:
	coverage run tests/tests.py && coverage html && coverage report

pylint:
	pylint --load-plugins pylint_django $(package)

check_complexity:
	flake8 $(package) --max-complexity=10

flake8:
	flake8 $(package) --count
