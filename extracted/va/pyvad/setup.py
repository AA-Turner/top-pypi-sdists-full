# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvad']

package_data = \
{'': ['*']}

install_requires = \
['librosa>=0.9.2,<0.10.0', 'numpy>=1.23.0,<2.0.0', 'webrtcvad>=2.0.10,<3.0.0']

setup_kwargs = {
    'name': 'pyvad',
    'version': '0.2.0',
    'description': "'py-webrtcvad wrapper for trimming speech clips'",
    'long_description': '# [py-webrtcvad](https://github.com/wiseman/py-webrtcvad) wrapper for trimming speech clips\n[![Build](https://github.com/F-Tag/python-vad/actions/workflows/test.yaml/badge.svg)](https://github.com/F-Tag/python-vad/actions/workflows/test.yaml)\n[![PyPI version](https://badge.fury.io/py/pyvad.svg)](https://badge.fury.io/py/pyvad)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pyvad.svg)](https://pypi.org/project/pyvad/)\n\n## Requirement\n[numpy](https://github.com/numpy/numpy), \n[librosa](https://github.com/librosa/librosa) and \n[py-webrtcvad](https://github.com/wiseman/py-webrtcvad).\n\n## Installation\nvia pip\n```sh\n$ pip install pyvad\n```\n\nor\n\nfrom github repository\n```sh\n$ pip install git+https://github.com/F-Tag/python-vad.git\n```\n\n## Usage\n```python\nfrom pyvad import vad\nvact = vad(speech_data, speech_data_fs)\n```\n\n\n## Example\nPlease see `example.ipynb` jupyter notebook.\n\n## License\nMIT License (see `LICENSE` file).\n\n## Announcement\nThe version 0.1.0 update break backward compatibility.\n\nThe changes are as follows:\n1. The `hoplength` argument has been changed to `hop_length`.\n2. The `trim` returns (start_index, end_index) (`return_sec` argument is abolished).\n3. Slightly changed the method of preprocessing a waveform in `vad`.\n4. End of support for python 2.x.\n\nYou can see the new API in the `example.ipynb`.\n\nThe previous version is 0.0.8.\n```sh\n$ pip install pyvad==0.0.8\n```',
    'author': 'Fumiaki Taguchi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/F-Tag/python-vad',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
