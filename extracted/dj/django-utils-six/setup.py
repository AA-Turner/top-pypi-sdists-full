# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django', 'django.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-utils-six',
    'version': '2.0',
    'description': 'Forward compatibility django.utils.six for Django 3',
    'long_description': "# django-utils-six\n\nForward compatibility django.utils.six for Django 3\n\n```bash\npip install Django>3\npip install django-utils-six\n```\n\nCode is taken from [Django 2.2](https://github.com/django/django/blob/stable/2.2.x/django/utils/six.py)\n\n## Why?\n\nI found `django.utils.six` is solely responsible for plenty of libraries' incompatibility with Django 3.",
    'author': 'Django Software Foundation',
    'author_email': 'foundation@djangoproject.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/django-utils-six',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
