# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pptx2md']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=6.0.0',
 'numpy>=2.1.3,<3.0.0',
 'pydantic>=2.9.2,<3.0.0',
 'python-pptx>=0.6.18',
 'rapidfuzz>=0.10.0',
 'scipy>=1.14.1,<2.0.0',
 'tqdm>=4']

entry_points = \
{'console_scripts': ['pptx2md = pptx2md.__main__:main']}

setup_kwargs = {
    'name': 'pptx2md',
    'version': '2.0.6',
    'description': 'This package converts pptx to markdown',
    'long_description': 'None',
    'author': 'Liu Siyao',
    'author_email': 'liu.siyao@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssine/pptx2md',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
