# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_azure_blob_downloader']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1.10.0', 'azure-storage-blob>=12.12.0']

entry_points = \
{'console_scripts': ['download-azure-blob = '
                     'simple_azure_blob_downloader.download_azure_blob:main']}

setup_kwargs = {
    'name': 'simple-azure-blob-downloader',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jackie Tung',
    'author_email': 'jackie@outerbounds.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
