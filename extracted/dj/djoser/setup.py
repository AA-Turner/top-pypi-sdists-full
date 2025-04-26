# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djoser',
 'djoser.social',
 'djoser.social.backends',
 'djoser.social.token',
 'djoser.urls',
 'djoser.webauthn',
 'djoser.webauthn.migrations']

package_data = \
{'': ['*'],
 'djoser': ['locale/ca/LC_MESSAGES/*',
            'locale/de/LC_MESSAGES/*',
            'locale/es/LC_MESSAGES/*',
            'locale/fr/LC_MESSAGES/*',
            'locale/id/LC_MESSAGES/*',
            'locale/ja/LC_MESSAGES/*',
            'locale/ka/LC_MESSAGES/*',
            'locale/me/LC_MESSAGES/*',
            'locale/pl/LC_MESSAGES/*',
            'locale/pt_BR/LC_MESSAGES/*',
            'locale/ru_RU/LC_MESSAGES/*',
            'templates/email/*']}

install_requires = \
['django>=3.0.0',
 'djangorestframework-simplejwt>=5.0,<6.0',
 'social-auth-app-django>=5.0.0,<6.0.0']

extras_require = \
{'djet': ['djet>=0.3.0,<0.4.0'], 'webauthn': ['webauthn<1.0']}

setup_kwargs = {
    'name': 'djoser',
    'version': '2.3.1',
    'description': 'REST implementation of Django authentication system.',
    'long_description': '======\ndjoser\n======\n\n.. image:: https://img.shields.io/pypi/v/djoser.svg\n   :target: https://pypi.org/project/djoser\n\n.. image:: https://github.com/sunscrapers/djoser/workflows/Tests/badge.svg\n    :target: https://github.com/sunscrapers/djoser/actions?query=branch%3Amaster+workflow%Tests++\n    :alt: Build Status\n\n.. image:: https://codecov.io/gh/sunscrapers/djoser/branch/master/graph/badge.svg\n :target: https://codecov.io/gh/sunscrapers/djoser\n\n.. image:: https://img.shields.io/pypi/dm/djoser\n   :target: https://img.shields.io/pypi/dm/djoser\n\n.. image:: https://readthedocs.org/projects/djoser/badge/?version=latest\n    :target: https://djoser.readthedocs.io/en/latest/\n    :alt: Docs\n\nREST implementation of `Django <https://www.djangoproject.com/>`_ authentication\nsystem. **djoser** library provides a set of `Django Rest Framework <https://www.django-rest-framework.org/>`_\nviews to handle basic actions such as registration, login, logout, password\nreset and account activation. It works with\n`custom user model <https://docs.djangoproject.com/en/dev/topics/auth/customizing/>`_.\n\nInstead of reusing Django code (e.g. ``PasswordResetForm``), we reimplemented\nfew things to fit better into `Single Page App <https://en.wikipedia.org/wiki/Single-page_application>`_\narchitecture.\n\nDeveloped by `SUNSCRAPERS <http://sunscrapers.com/>`_ with passion & patience.\n\n.. image:: https://asciinema.org/a/94J4eG2tSBD2iEfF30a6vGtXw.png\n  :target: https://asciinema.org/a/94J4eG2tSBD2iEfF30a6vGtXw\n\nRequirements\n============\n\nTo be able to run **djoser** you have to meet the following requirements:\n\n- Python>=3.8\n- Django>=3.0.0\n- Django REST Framework>=3.12\n\nInstallation\n============\n\nSimply install using ``pip``:\n\n.. code-block:: bash\n\n    $ pip install djoser\n\nAnd continue with the steps described at\n`configuration <https://djoser.readthedocs.io/en/latest/getting_started.html#configuration>`_\nguide.\n\nDocumentation\n=============\n\nDocumentation is available to study at\n`https://djoser.readthedocs.io <https://djoser.readthedocs.io>`_\nand in ``docs`` directory.\n\nContributing and development\n============================\n\nTo start developing on **djoser**, clone the repository:\n\n.. code-block:: bash\n\n    $ git clone git@github.com:sunscrapers/djoser.git\n\nWe use `poetry <https://python-poetry.org/>`_ as dependency management and packaging tool.\n\n.. code-block:: bash\n\n    $ cd djoser\n    $ poetry install --all-extras\n\nThis will create a virtualenv with all development dependencies.\n\nTo run the test just type:\n\n.. code-block:: bash\n\n    $ poetry run py.test testproject\n\nWe also prepared a convenient ``Makefile`` to automate commands above:\n\n.. code-block:: bash\n\n    $ make init\n    $ make test\n\nTo activate the virtual environment run\n\n.. code-block:: bash\n\n    $ poetry shell\n\nWithout poetry\n--------------\n\nNew versions of ``pip`` can use ``pyproject.toml`` to build the package and install its dependencies.\n\n.. code-block:: bash\n\n    $ pip install .[test]\n\n.. code-block:: bash\n\n    $ cd testproject\n    $ ./manage.py test\n\nExample project\n---------------\n\nYou can also play with test project by running following commands:\n\n.. code-block:: bash\n\n    $ make migrate\n    $ make runserver\n\nCommiting your code\n-------------------\n\nBefore sending patches please make sure you have `pre-commit <https://pre-commit.com/>`_ activated in your local git repository:\n\n.. code-block:: bash\n\n    $ pre-commit install\n\nThis will ensure that your code is cleaned before you commit it.\n\nSimilar projects\n================\n\nList of projects related to Django, REST and authentication:\n\n- `django-rest-registration <https://github.com/apragacz/django-rest-registration>`_\n- `django-oauth-toolkit <https://github.com/evonove/django-oauth-toolkit>`_\n\nPlease, keep in mind that while using custom authentication and TokenCreateSerializer\nvalidation, there is a path that **ignores intentional return of None** from authenticate()\nand try to find User using parameters. Probably, that will be changed in the future.\n',
    'author': 'Sunscrapers',
    'author_email': 'info@sunscrapers.com',
    'maintainer': 'Tomasz Wojcik',
    'maintainer_email': 'djoser@tomwojcik.com',
    'url': 'https://github.com/sunscrapers/djoser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
