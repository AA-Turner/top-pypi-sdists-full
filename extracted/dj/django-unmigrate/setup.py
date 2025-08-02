# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_unmigrate',
 'django_unmigrate.management',
 'django_unmigrate.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0', 'django>=2.0']

setup_kwargs = {
    'name': 'django-unmigrate',
    'version': '0.3.1',
    'description': 'Smart reversion of Django migrations based on Git diff',
    'long_description': "django-unmigrate\n================\n\n.. image:: https://img.shields.io/badge/packaging-poetry-purple.svg\n    :alt: Packaging: poetry\n    :target: https://github.com/sdispater/poetry\n\n.. image:: https://img.shields.io/badge/code%20style-black-black.svg\n    :alt: Code style: black\n    :target: https://github.com/ambv/black\n\n.. image:: https://github.com/lorinkoz/django-unmigrate/workflows/code/badge.svg\n    :alt: Build status\n    :target: https://github.com/lorinkoz/django-unmigrate/actions\n\n.. image:: https://coveralls.io/repos/github/lorinkoz/django-unmigrate/badge.svg?branch=master\n    :alt: Code coverage\n    :target: https://coveralls.io/github/lorinkoz/django-unmigrate?branch=master\n\n.. image:: https://badge.fury.io/py/django-unmigrate.svg\n    :alt: PyPi version\n    :target: http://badge.fury.io/py/django-unmigrate\n\n.. image:: https://pepy.tech/badge/django-unmigrate/month\n    :alt: Downloads\n    :target: https://pepy.tech/project/django-unmigrate/\n\n|\n\nIf you are in a complex Django project, sometimes you will find yourself switching\nbetween multiple branches, some of which can add a number of database migrations.\nBefore switching back to ``master`` you will have to unapply all migrations that\nare specific to the current branch. In order to unapply these, you will have to\nenter the migration that comes right before the first migration of the current\nbranch. If two or more apps are involved, you will have to do that for each one\nof them.\n\nIf you leave your migration names unchanged, inferring the name of the right\nmigration to target is not too difficult, because they are prefixed by default\nwith a sequential number. Django also helps, being smart enough to let you use\nan unambiguous prefix of any migration name. Add a merge migration and the\nnumbers will no longer be so obvious. Or if you have renamed your migration\nfiles to drop the sequential numbers you will have to do the search manually.\n\nWith ``django-unmigrate`` you can speed up the process.\n\nUsage\n-----\n\nAdd ``django_unmigrate`` to your ``INSTALLED_APPS``. This is required to make\nthe ``unmigrate`` management command available.\n\nThen, while standing on any branch, you will be able to use::\n\n    python manage.py unmigrate master\n\nOr if it's going to be ``master`` anyways, this will suffice::\n\n    python manage.py unmigrate\n\nAnd that's it!\n\nA little deeper\n---------------\n\nOk, you can do more than that.\n\nDo you need to unapply your migrations from the same branch, a few commits\nbehind? Here's how::\n\n    python manage.py unmigrate HEAD~12\n    python manage.py unmigrate b13553d\n    python manage.py unmigrate v1.33.7\n\nOr if you only want to see the target migrations, do::\n\n    python manage.py unmigrate --dry-run\n\nFinally, if you just want to play with the app with no actual modifications in\nthe database, go ahead and unapply your migrations with ``fake``. Just don't\nforget to apply them again at the end::\n\n    python manage.py unmigrate --fake\n    python manage.py migrate --fake\n\nContributing\n------------\n\n- Join the discussion at https://github.com/lorinkoz/django-unmigrate/discussions.\n- PRs are welcome! If you have questions or comments, please use the link\n  above.\n- To run the test suite run ``make`` or ``make coverage``. The tests for this\n  project live inside a small django project called ``dunm_sandbox``. Beware!\n  This package uses Git to function, therefore, the tests expect a number of\n  commit hashes inside this repository to be present and remain stable in order\n  to function. See `this meta file`_ for further details.\n\n.. _this meta file: https://github.com/lorinkoz/django-unmigrate/blob/master/dunm_sandbox/meta.py\n",
    'author': 'Lorenzo Peña',
    'author_email': 'lorinkoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lorinkoz/django-unmigrate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
