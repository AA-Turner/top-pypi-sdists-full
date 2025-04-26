# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['warlock']

package_data = \
{'': ['*']}

install_requires = \
['jsonpatch>=1,<2', 'jsonschema>=4,<5']

setup_kwargs = {
    'name': 'warlock',
    'version': '2.0.1',
    'description': 'Python object model built on JSON schema and JSON patch.',
    'long_description': '# Warlock 🧙\u200d♀️\n\n**Create self-validating Python objects using JSON schema.**\n\n[![PyPI](https://img.shields.io/pypi/v/warlock.svg)][warlock]\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/warlock.svg)][warlock]\n[![PyPI - Downloads](https://img.shields.io/pypi/dw/warlock.svg)][pypistats]\n\n[![Build Status](https://github.com/bcwaldon/warlock/actions/workflows/ci.yaml/badge.svg)][ci-builds]\n[![Coverage Status](https://coveralls.io/repos/github/bcwaldon/warlock/badge.svg?branch=master)][coveralls]\n![GitHub commits since latest release (branch)](https://img.shields.io/github/commits-since/bcwaldon/warlock/latest/master.svg)\n\n[![Package management: poetry](https://img.shields.io/badge/deps-poetry-blueviolet.svg)][poetry]\n[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black/)\n\n## Installation\n\nWarlock is [available on PyPI][warlock]:\n\n```shell\npip install warlock\n```\n\n## Usage\n\n1) Create your schema\n\n    ```python\n    >>> schema = {\n        \'name\': \'Country\',\n        \'properties\': {\n            \'name\': {\'type\': \'string\'},\n            \'abbreviation\': {\'type\': \'string\'},\n            \'population\': {\'type\': \'integer\'},\n        },\n        \'additionalProperties\': False,\n    }\n    ```\n\n2) Create a model\n\n    ```python\n    >>> import warlock\n    >>> Country = warlock.model_factory(schema)\n    ```\n\n3) Create an object using your model\n\n    ```python\n    >>> sweden = Country(name=\'Sweden\', abbreviation=\'SE\')\n    ```\n\n4) Let the object validate itself\n\n    ```python\n    >>> sweden.name = 5\n    Traceback (most recent call last):\n    File "<stdin>", line 1, in <module>\n    File "warlock/core.py", line 53, in __setattr__\n        raise InvalidOperation(msg)\n    warlock.core.InvalidOperation: Unable to set \'name\' to \'5\'\n\n    >>> sweden.overlord = \'Bears\'\n    Traceback (most recent call last):\n      File "<stdin>", line 1, in <module>\n      File "warlock/core.py", line 53, in __setattr__\n        raise InvalidOperation(msg)\n    warlock.core.InvalidOperation: Unable to set \'overlord\' to \'Bears\'\n    ```\n\n5) Generate a [JSON Patch document](http://tools.ietf.org/html/draft-ietf-appsawg-json-patch) to track changes\n\n    ```python\n    >>> sweden.population=9453000\n    >>> sweden.patch\n    \'[{"path": "/population", "value": 9453000, "op": "add"}]\'\n    ```\n\n[warlock]: https://pypi.org/project/warlock/\n[pip]: https://pip.pypa.io/en/stable/\n[ci-builds]: https://github.com/bcwaldon/warlock/actions/workflows/ci.yaml\n[coveralls]: https://coveralls.io/github/bcwaldon/warlock?branch=master\n[poetry]: https://poetry.eustace.io/docs/\n[pypistats]: https://pypistats.org/packages/warlock\n',
    'author': 'Brian Waldon',
    'author_email': 'bcwaldon@gmail.com',
    'maintainer': 'Jan Willhaus',
    'maintainer_email': 'mail@janwillhaus.de',
    'url': 'http://github.com/bcwaldon/warlock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
