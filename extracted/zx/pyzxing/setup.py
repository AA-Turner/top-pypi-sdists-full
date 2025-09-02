# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzxing']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0', 'numpy>=1.21,<2.0']

setup_kwargs = {
    'name': 'pyzxing',
    'version': '1.0.2',
    'description': 'Python wrapper for ZXing Java library',
    'long_description': '# pyzxing\n\nEnglish | [简体中文](README_CN.md)\n\n[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/chenjiexu/pyzxing?include_prereleases)](https://github.com/ChenjieXu/pyzxing/releases/latest)\n[![PyPI](https://img.shields.io/pypi/v/pyzxing)](https://pypi.org/project/pyzxing/)\n[![Conda-forge](https://img.shields.io/conda/v/conda-forge/pyzxing)](https://anaconda.org/conda-forge/pyzxing)\n[![Conda](https://img.shields.io/conda/v/chenjiexu/pyzxing)](https://anaconda.org/ChenjieXu/pyzxing)\n\n[![Travis (.org)](https://img.shields.io/travis/ChenjieXu/pyzxing)](https://travis-ci.org/github/ChenjieXu/pyzxing)\n[![Codacy grade](https://img.shields.io/codacy/grade/353f276d2073445aab7af3e32b0d503a)](https://www.codacy.com/manual/ChenjieXu/pyzxing)\n\n## First GA\n\nAfter a year of development, the first General Availability of pyzxing is finally released. I would like to express my\ngratitude to all the developers for their suggestions and issue, which helped the development of this project to a great\nextent. This project will continue to be open source and updated regularly.\n\n## Introduction\n\nA Python wrapper of [ZXing library](https://github.com/zxing/zxing). python-zxing does not work properly and is out of\nmaintenance. So I decide to create this repository so that Pythoneers can take advantage of ZXing library with minimum\neffort.\n\n## Features\n\n- Super easy to get hands on decoding qrcode with Python\n- Structured outputs\n- Scan multiple barcodes in one picture\n- Scan multiple pictures in parallel, which speeds up 77%\n\n## Installation\n\nInstalling from [Github source](https://github.com/ChenjieXu/pyzxing.git) is recommended :\n\n```bash\ngit clone https://github.com/ChenjieXu/pyzxing.git\ncd pyzxing\npython setup.py install\n```\n\nIt is also possible to install from [PyPI](https://pypi.org/project/pyzxing/):\n\n```bash\npip install pyzxing\n```\n\nInstall from [Anaconda](https://anaconda.org/ChenjieXu/pyzxing). Now available on the public channel, conda-forge:\n\n```bash\nconda install pyzxing # conda-forge channel\nconda install -c chenjiexu pyzxing # private channel\n```\n\n## Build ZXing Library\n\nA ready-to-go jar file is available with release, but I can not guarantee that this file will work properly on your PC.\nYou may run test script before building ZXing. Pyzxing will download compiled Jar file automatically and call unit test.\nFor those who haven\'t installed Java, I strongly recommend you to install openjdk8.\n\n```bash\npython -m unittest tests.test_decode\n```\n\nIf failed, build ZXing using following commands.\n\n```bash\ngit submodule init\ngit submodule update\ncd zxing\nmvn install -DskipTests\ncd javase\nmvn -DskipTests package assembly:single\n```\n\n## Quick Start\n\n```python\nfrom pyzxing import BarCodeReader\n\nreader = BarCodeReader()\nresults = reader.decode(\'/PATH/TO/FILE\')\n# Or file pattern for multiple files\nresults = reader.decode(\'/PATH/TO/FILES/*.png\')\nprint(results)\n# Or a numpy array\n# Requires additional installation of opencv\n# pip install opencv-python\nresults = reader.decode_array(img)\n```\n\nOr you may simply call it from command line\n\n```bash\npython scripts/scanner.py -f /PATH/TO/FILE\n```\n\n# Sponsor\n\n<p align="left">\n  <a href="https://jb.gg/OpenSource"><img src="src/jetbrains-logo.svg" alt="Logo"></img></a>\n\n  <br/>\n  <sub><a href="https://www.jetbrains.com/community/opensource/">Open Source Support Program</a></sub>\n</p>\n',
    'author': 'Chenjie Xu',
    'author_email': 'cxuscience@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ChenjieXu/pyzxing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
