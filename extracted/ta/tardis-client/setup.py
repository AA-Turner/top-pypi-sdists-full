# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tardis_client', 'tardis_client.reconstructors']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=24.1.0,<25.0.0', 'aiohttp>=3.10.0', 'sortedcontainers>=2.1,<3.0']

setup_kwargs = {
    'name': 'tardis-client',
    'version': '1.4.2',
    'description': 'Python client for tardis.dev - historical tick-level cryptocurrency market data replay API.',
    'long_description': '# tardis-client\n\n[![PyPi](https://img.shields.io/pypi/v/tardis-client.svg)](https://pypi.org/project/tardis-client/)\n[![Python](https://img.shields.io/pypi/pyversions/tardis-client.svg)](https://pypi.org/project/tardis-client/)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n`tardis-client` is deprecated and frozen.\n\nThis package has been replaced by [`tardis-dev`](https://pypi.org/project/tardis-dev/), the unified Python package for replay, dataset downloads, exchange metadata, and cache helpers.\n\nThis `1.4.2` release does not introduce new features. Its purpose is to point existing `tardis-client` users to the migration path.\n\n## Migrate To `tardis-dev`\n\nMigration notice:\n\n- https://docs.tardis.dev/python-client/migration-notice\n\nInstall commands:\n\n```bash\npip uninstall tardis-client\npip install tardis-dev\n```\n\n## Old To New\n\n### Replay\n\nOld:\n\n```python\nfrom tardis_client import TardisClient, Channel\n\nclient = TardisClient(api_key="YOUR_API_KEY")\n\nasync for item in client.replay(\n    exchange="bitmex",\n    from_date="2019-06-01",\n    to_date="2019-06-02",\n    filters=[Channel("trade", ["XBTUSD"])],\n):\n    print(item)\n```\n\nNew:\n\n```python\nfrom tardis_dev import Channel, replay\n\nasync for item in replay(\n    exchange="bitmex",\n    from_date="2019-06-01",\n    to_date="2019-06-02",\n    filters=[Channel("trade", ["XBTUSD"])],\n    api_key="YOUR_API_KEY",\n):\n    print(item)\n```\n\n### Cache Cleanup\n\nOld:\n\n```python\nfrom tardis_client import TardisClient\n\nclient = TardisClient()\nclient.clear_cache()\n```\n\nNew:\n\n```python\nfrom tardis_dev import clear_cache\n\nclear_cache()\n```\n\n### Dataset Downloads\n\nThe replacement package also includes dataset downloads directly from the top level:\n\n```python\nfrom tardis_dev import download_datasets\n\ndownload_datasets(\n    exchange="deribit",\n    data_types=["trades"],\n    symbols=["BTC-PERPETUAL"],\n    from_date="2024-01-01",\n    to_date="2024-01-02",\n    api_key="YOUR_API_KEY",\n)\n```\n\n## Support Status\n\n- no new features will be added to `tardis-client`\n- new Python development continues in `tardis-dev`\n- future migration guidance will live in the docs, not in this package\n\n## License\n\nMPL-2.0\n',
    'author': 'Thad',
    'author_email': 'thad@tardis.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tardis-dev/python-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
