# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootstrap5', 'bootstrap5.templatetags', 'docs', 'tests', 'tests.app']

package_data = \
{'': ['*'],
 'bootstrap5': ['templates/bootstrap5/*', 'templates/bootstrap5/widgets/*']}

install_requires = \
['beautifulsoup4>=4.8.0,<5.0.0', 'django>=2.2,<5.0']

extras_require = \
{'docs': ['sphinx>=4.4,<5.0',
          'sphinx_rtd_theme>=1.0,<2.0',
          'm2r2>=0.2.5,<0.3.0']}

setup_kwargs = {
    'name': 'django-bootstrap-v5',
    'version': '1.0.11',
    'description': 'Bootstrap 5 support for Django projects',
    'long_description': '# django-bootstrap v5\n\nThis package builds on top of the excellent [django-bootstrap4](https://github.com/zostera/django-bootstrap4) package.\n\n[![CI](https://github.com/zelenij/django-bootstrap-v5/workflows/CI/badge.svg?branch=main)](https://github.com/django-bootstrap-v5/actions?workflow=CI)\n[![Coverage Status](https://coveralls.io/repos/github/django-bootstrap-v5/badge.svg?branch=main)](https://coveralls.io/github/django-bootstrap-v5?branch=main)\n[![Latest PyPI version](https://img.shields.io/pypi/v/django-bootstrap-v5.svg)](https://pypi.python.org/pypi/django-bootstrap-v5)\n[![Any color you like](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nBootstrap 5 integration for Django.\n\n## Package name\n\nUnfortunately, someone squatted on the django-bootstrap-v5 (as well as 6, 7, 8 etc) name in PyPi in 2013, so I had to modify the name of this package accordingly.\n\n## Goal\n\nThe goal of this project is to seamlessly blend Django and Bootstrap 5.\n\n## Requirements\n\nPython 3.6 or newer with Django >= 2.2 or newer.\n\n## Documentation\n\nThe full documentation is at https://django-bootstrap-v5.readthedocs.io/\n\n## Installation\n\n1. Install using pip:\n\n    ```shell script\n    pip install django-bootstrap-v5\n    ```\n   \n   Alternatively, you can install download or clone this repo and call ``pip install -e .``.\n\n2. Add to `INSTALLED_APPS` in your `settings.py`:\n\n   ```python\n   INSTALLED_APPS = (\n       # ...\n       "bootstrap5",\n       # ...\n   )\n   ````\n\n3. In your templates, load the `bootstrap5` library and use the `bootstrap_*` tags:\n\n## Example template\n\n```jinja\n{% load bootstrap5 %}\n\n{# Display a form #}\n\n<form action="/url/to/submit/" method="post" class="form">\n    {% csrf_token %}\n    {% bootstrap_form form %}\n    {% buttons %}\n        <button type="submit" class="btn btn-primary">Submit</button>\n    {% endbuttons %}\n</form>\n```\n\nDemo\n----\n\nA demo app is provided in `demo`. You can run it from your virtualenv with `python manage.py runserver`.\n\n\nBugs and suggestions\n--------------------\n\nIf you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.\n\nhttps://github.com/zelenij/django-bootstrap-v5/issues\n\n\nLicense\n-------\n\nYou can use this under BSD-3-Clause. See [LICENSE](LICENSE) file for details.\n\n\nAuthor\n------\n\nDeveloped and maintained by [Andre Bar\'yudin](https://www.baryudin.com)\n\nOriginal authors: \n\n* [Zostera](https://zostera.nl)\n* [Dylan Verheul](https://github.com/dyve)\n\nThanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.\n\nPlease see [AUTHORS.md](AUTHORS.md) for a list of contributors.\n',
    'author': "Andre Bar'yudin",
    'author_email': 'andre.baryudin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zelenij/django-bootstrap-v5',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
