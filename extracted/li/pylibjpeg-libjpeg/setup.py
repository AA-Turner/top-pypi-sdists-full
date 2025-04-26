# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libjpeg', 'libjpeg.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=2.0,<3.0']

entry_points = \
{'pylibjpeg.jpeg_decoders': ['libjpeg = libjpeg:decode'],
 'pylibjpeg.jpeg_ls_decoders': ['libjpeg = libjpeg:decode'],
 'pylibjpeg.jpeg_xt_decoders': ['libjpeg = libjpeg:decode'],
 'pylibjpeg.pixel_data_decoders': ['1.2.840.10008.1.2.4.50 = '
                                   'libjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.51 = '
                                   'libjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.57 = '
                                   'libjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.70 = '
                                   'libjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.80 = '
                                   'libjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.81 = '
                                   'libjpeg:decode_pixel_data']}

setup_kwargs = {
    'name': 'pylibjpeg-libjpeg',
    'version': '2.3.0',
    'description': 'A Python wrapper for libjpeg, with a focus on use as a plugin for for pylibjpeg',
    'long_description': '<p align="center">\n<a href="https://github.com/pydicom/pylibjpeg-libjpeg/actions?query=workflow%3Aunit-tests"><img alt="Build status" src="https://github.com/pydicom/pylibjpeg-libjpeg/workflows/unit-tests/badge.svg"></a>\n<a href="https://codecov.io/gh/pydicom/pylibjpeg-libjpeg"><img alt="Test coverage" src="https://codecov.io/gh/pydicom/pylibjpeg-libjpeg/branch/main/graph/badge.svg"></a>\n<a href="https://pypi.org/project/pylibjpeg-libjpeg/"><img alt="PyPI versions" src="https://img.shields.io/pypi/v/pylibjpeg-libjpeg"></a>\n<a href="https://www.python.org/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/pylibjpeg-libjpeg"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n## pylibjpeg-libjpeg\n\nA Python 3.8+ wrapper for Thomas Richter\'s\n[libjpeg](https://github.com/thorfdbg/libjpeg), with a focus on use as a\nplugin for [pylibjpeg](http://github.com/pydicom/pylibjpeg).\n\nLinux, MacOS and Windows are all supported.\n\n### Installation\n#### Dependencies\n[NumPy](http://numpy.org)\n\n#### Installing the current release\n```bash\npip install pylibjpeg-libjpeg\n```\n#### Installing the development version\n\nMake sure [Python](https://www.python.org/) and [Git](https://git-scm.com/) are installed. For Windows, you also need to install\n[Microsoft\'s C++ Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16).\n```bash\ngit clone --recurse-submodules https://github.com/pydicom/pylibjpeg-libjpeg\npython -m pip install pylibjpeg-libjpeg\n```\n\n### Supported JPEG Formats\n#### Decoding\n\n| ISO/IEC Standard | ITU Equivalent | JPEG Format |\n| --- | --- | --- |\n| [10918](https://www.iso.org/standard/18902.html) | [T.81](https://www.itu.int/rec/T-REC-T.81/en) | [JPEG](https://jpeg.org/jpeg/index.html)    |\n| [14495](https://www.iso.org/standard/22397.html)   | [T.87](https://www.itu.int/rec/T-REC-T.87/en) | [JPEG-LS](https://jpeg.org/jpegls/index.html) |\n| [18477](https://www.iso.org/standard/62552.html)   | | [JPEG XT](https://jpeg.org/jpegxt/) |\n\n#### Encoding\nEncoding of JPEG images is not currently supported\n\n### Supported Transfer Syntaxes\n#### Decoding\n| UID | Description |\n| --- | --- |\n| 1.2.840.10008.1.2.4.50 | JPEG Baseline (Process 1) |\n| 1.2.840.10008.1.2.4.51 | JPEG Extended (Process 2 and 4) |\n| 1.2.840.10008.1.2.4.57 | JPEG Lossless, Non-Hierarchical (Process 14) |\n| 1.2.840.10008.1.2.4.70 | JPEG Lossless, Non-Hierarchical, First-Order Prediction (Process 14 [Selection Value 1]) |\n| 1.2.840.10008.1.2.4.80 | JPEG-LS Lossless |\n| 1.2.840.10008.1.2.4.81 | JPEG-LS Lossy (Near-Lossless) Image Compression |\n\n### Usage\n#### With pylibjpeg and pydicom\n\n```python\nfrom pydicom import dcmread\nfrom pydicom.data import get_testdata_file\n\nds = dcmread(get_testdata_file(\'JPEG-LL.dcm\'))\narr = ds.pixel_array\n```\n\n#### Standalone JPEG decoding\n\nYou can also decode JPEG images to a [numpy ndarray][1]:\n\n[1]: https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html\n\n```python\nfrom libjpeg import decode\n\nwith open(\'filename.jpg\', \'rb\') as f:\n    # Returns a numpy array\n    arr = decode(f.read())\n\n# Or simply...\narr = decode(\'filename.jpg\')\n```\n',
    'author': 'pylibjpeg-libjpeg contributors',
    'author_email': 'None',
    'maintainer': 'scaramallion',
    'maintainer_email': 'scaramallion@users.noreply.github.com',
    'url': 'https://github.com/pydicom/pylibjpeg-libjpeg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
