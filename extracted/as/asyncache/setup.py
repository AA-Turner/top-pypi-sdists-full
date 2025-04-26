# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncache']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'asyncache',
    'version': '0.3.1',
    'description': 'Helpers to use cachetools with async code.',
    'long_description': 'asyncache\n#########\n\nHelpers to use cachetools with asyncio.\n\n.. image:: https://img.shields.io/pypi/v/asyncache\n   :target: https://pypi.org/project/asyncache/\n   :alt: Latest PyPI version\n\n.. image:: https://travis-ci.org/hephex/asyncache.svg?branch=master\n    :target: https://travis-ci.org/hephex/asyncache\n\n.. image:: https://coveralls.io/repos/github/hephex/asyncache/badge.svg?branch=master\n    :target: https://coveralls.io/github/hephex/asyncache?branch=master\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nInstallation\n============\n\nasyncache is available from PyPI_ and can be installed by running::\n\n  pip install asyncache\n\nExample\n=======\n\n.. code-block:: python\n\n    from asyncache import cached\n    from cachetools import TTLCache\n    \n    pool = ...\n    \n    @cached(TTLCache(1024, 60))\n    async def get_username(user_id):\n        rec = await pool.fetchrow(\n            """\n            SELECT\n                username\n            FROM\n                users\n            WHERE\n                id = $1\n            """,\n            user_id,\n        )\n        return rec and rec["username"]\n\nLicense\n=======\n\nThis project is licensed under the MIT License - see the LICENSE_ file for details.\n\n\nAcknowledgments\n===============\n\n- `cachetools`_\n\n\n.. _LICENSE: LICENSE\n.. _cachetools: https://github.com/tkem/cachetools\n.. _PyPI: https://pypi.org/project/asyncache/\n\n\n',
    'author': 'hephex',
    'author_email': 'figus.federico@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
