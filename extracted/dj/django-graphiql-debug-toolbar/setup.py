# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphiql_debug_toolbar']

package_data = \
{'': ['*'],
 'graphiql_debug_toolbar': ['static/graphiql_debug_toolbar/js/*',
                            'templates/graphiql_debug_toolbar/*']}

install_requires = \
['Django>=2.2', 'django-debug-toolbar>=3.1', 'graphene-django>=2.0.0']

setup_kwargs = {
    'name': 'django-graphiql-debug-toolbar',
    'version': '0.2.0',
    'description': 'Django Debug Toolbar for GraphiQL IDE.',
    'long_description': "# Django GraphiQL Debug Toolbar\n\n[![Tests](https://github.com/flavors/django-graphiql-debug-toolbar/actions/workflows/test-suite.yml/badge.svg)](https://github.com/flavors/django-graphiql-debug-toolbar/actions)\n[![Coverage](https://img.shields.io/codecov/c/github/flavors/django-graphiql-debug-toolbar?color=%2334D058)](https://codecov.io/gh/flavors/django-graphiql-debug-toolbar)\n[![Codacy](https://app.codacy.com/project/badge/Grade/354f70cdefda40938c397d8651a2a06c)](https://www.codacy.com/gh/flavors/django-graphiql-debug-toolbar/dashboard)\n[![Package version](https://img.shields.io/pypi/v/django-graphiql-debug-toolbar.svg)](https://pypi.python.org/pypi/django-graphiql-debug-toolbar)\n\n[Django Debug Toolbar](https://github.com/jazzband/django-debug-toolbar) for [GraphiQL](https://github.com/graphql/graphiql) IDE.\n\n![Graphiql Debug Toolbar](https://user-images.githubusercontent.com/5514990/36340937-1937ee68-1419-11e8-8477-40622e98c312.gif)\n\n## Dependencies\n\n*   Python ≥ 3.6\n*   Django ≥ 2.2\n\n## Installation\n\nInstall last stable version from Pypi.\n\n```sh\npip install django-graphiql-debug-toolbar\n````\n\nSee the [documentation](https://django-debug-toolbar.readthedocs.io/en/stable/installation.html) for further guidance on setting *Django Debug Toolbar*.\n\nAdd `graphiql_debug_toolbar` to your *INSTALLED_APPS* settings:\n\n```py\nINSTALLED_APPS = [\n    'debug_toolbar',\n    'graphiql_debug_toolbar',\n]\n```\n\n**Replace** the Django Debug Toolbar **middleware** with the GraphiQL Debug Toolbar one. \n\n```py\nMIDDLEWARE = [\n    # 'debug_toolbar.middleware.DebugToolbarMiddleware',\n    'graphiql_debug_toolbar.middleware.DebugToolbarMiddleware',\n]\n```\n\nCredits to [@jazzband](https://jazzband.co) / [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar).\n",
    'author': 'mongkok',
    'author_email': 'dani@domake.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flavors/django-graphiql-debug-toolbar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
