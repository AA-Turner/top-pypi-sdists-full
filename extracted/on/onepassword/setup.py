# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['onepassword']
setup_kwargs = {
    'name': 'onepassword',
    'version': '0.4.1',
    'description': 'Python wrapper for the 1password CLI',
    'long_description': '# onepassword-python\nPython wrapper for the 1password CLI\n\n## Usage\n\n```python\nfrom onepassword import OnePassword\n\nsecret = {"password": "<YOUR-PASSWORD-HERE>",\n          "username": "<YOUR-USERNAME-HERE>",\n          "signin_address": "<YOUR-1PASSWORD-ORGNIZATION-ADDRESS>",\n          "secret_key": "<YOUR-1PASSWORD-SECRET-KEY>"}\nop = OnePassword(secret=secret)\n\ndocuments = op.list("documents")\npem_keys = (doc for doc in documents if doc["overview"]["title"].endswith("pem"))\nfirst_key = next(pem_keys)\nkey_contents = op.get("document", first_key["uuid"])\nprint(key_contents)\n```\n\n## API\n\n### onepassword.OnePassword\n',
    'author': 'Gabriel Chamon Araujo',
    'author_email': 'gchamon@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lettdigital/onepassword-python',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
