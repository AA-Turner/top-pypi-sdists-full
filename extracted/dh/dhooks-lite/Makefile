help:
	@echo "Makefile for dhooks-lite"

coverage:
	coverage run -m unittest && coverage html && coverage report

upload:
	twine upload dist/*

pylint:
	pylint dhooks_lite

check_complexity:
	flake8 dhooks_lite --max-complexity=10

flake8:
	flake8 dhooks_lite --count
