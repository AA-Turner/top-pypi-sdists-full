# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alembic_autogenerate_enums']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alembic-autogenerate-enums',
    'version': '0.1.2',
    'description': 'Alembic hook that allows enums values to be upgraded and downgraded in migrations automatically',
    'long_description': '\n# alembic-autogenerate-enums\n\nThis package implements an Alembic hook that causes ``alembic revision\n--autogenerate`` to output PostgreSQL ``ALTER TYPE .. ADD VALUE`` SQL\nstatements as part of new migrations.\n\n\n## Usage\n\nAdd the line:\n\n    import alembic_autogenerate_enums\n\nTo the top of your ``env.py``.\n\n\n## Notes\n\nSince ``ALTER TYPE .. ADD VALUE`` cannot run transactionally, each\n``op.sync_enum_values()`` call creates its own temporary private DB connection.\nSee https://bitbucket.org/zzzeek/alembic/issues/123/a-way-to-run-non-transactional-ddl\n\n## Tests\n\nWe have incredibly basic tests in a [sample project](./test-harness).\n\n```\nmkvirtualenv alembic-autogenerate\n```\n\nInstall the main autogenerate package and then the test harness:\n\n```\npip install -e .\npip install -e test-harness\n```\n\n```\ncreateuser alembic-autogenerate\ncreatedb -O alembic-autogenerate alembic-autogenerate_db\n```\n\n```\ncd test-harness && pytest\n```\n',
    'author': 'David Wilson',
    'author_email': 'dw@botanicus.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
