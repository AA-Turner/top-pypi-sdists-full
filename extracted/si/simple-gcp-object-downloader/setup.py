# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_gcp_object_downloader']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=2.4.0']

entry_points = \
{'console_scripts': ['download-gcp-object = '
                     'simple_gcp_object_downloader.download_gcp_object:main']}

setup_kwargs = {
    'name': 'simple-gcp-object-downloader',
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
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
