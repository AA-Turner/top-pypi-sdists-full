# This makefile provides tools for developers.
#
# Note that it requires you to have a .env file defined with the path to your manage.py file
# The syntax is: MANAGE_PY_PATH = /path/to/manage.py

-include .env
export

appname = aa-eveuniverse
package = eveuniverse

help:
	@echo "Makefile for $(appname)"

makemessages:
	cd $(package) && \
	django-admin makemessages -l en --ignore 'build/*' && \
	django-admin makemessages -l de --ignore 'build/*' && \
	django-admin makemessages -l es --ignore 'build/*' && \
	django-admin makemessages -l ko --ignore 'build/*' && \
	django-admin makemessages -l ru --ignore 'build/*' && \
	django-admin makemessages -l zh_Hans --ignore 'build/*'

tx_push:
	tx push --source

tx_pull:
	tx pull -f

compilemessages:
	cd $(package) && \
	django-admin compilemessages -l en  && \
	django-admin compilemessages -l de  && \
	django-admin compilemessages -l es  && \
	django-admin compilemessages -l ko  && \
	django-admin compilemessages -l ru  && \
	django-admin compilemessages -l zh_Hans

coverage:
	coverage run $(MANAGE_PY_PATH) test $(package).tests --keepdb --failfast && coverage html && coverage report -m

pylint:
	pylint --load-plugins pylint_django $(package)

check_complexity:
	flake8 $(package) --max-complexity=10

flake8:
	flake8 $(package) --count

graph_models:
	python $(MANAGE_PY_PATH) graph_models $(package) --arrow-shape normal -X EveUniverseBaseModel,EveUniverseEntityModel,EveUniverseInlineModel,EveUniverseSimpleEntityModel -o $(appname)_models.png
