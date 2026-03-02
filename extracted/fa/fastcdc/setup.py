# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastcdc']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2,<2.0',
 'click>=8.1,<9.0',
 'codetiming>=1.2,<2.0',
 'humanize>=4.0,<5.0',
 'py-cpuinfo>=9.0,<10.0']

extras_require = \
{'hashes': ['xxhash>=3.0,<4.0', 'blake3>=0.3,<0.4']}

entry_points = \
{'console_scripts': ['fastcdc = fastcdc.cli:cli']}

setup_kwargs = {
    'name': 'fastcdc',
    'version': '1.7.0',
    'description': 'FastCDC (content defined chunking) in pure Python.',
    'long_description': '# FastCDC\n\n[![Tests](https://github.com/titusz/fastcdc-py/workflows/Tests/badge.svg)](https://github.com/titusz/fastcdc-py/actions?query=workflow%3ATests)\n[![Version](https://img.shields.io/pypi/v/fastcdc.svg)](https://pypi.python.org/pypi/fastcdc/)\n[![Downloads](https://pepy.tech/badge/fastcdc)](https://pepy.tech/project/fastcdc)\n\nThis package implements the "FastCDC" content defined chunking algorithm in\nPython with optional cython support. To learn more about content\ndefined chunking and its applications, see the reference material linked below.\n\n\n## Requirements\n\n* [Python](https://www.python.org/) Version 3.7 and later. Tested on Linux, Mac and\nWindows\n\n## Installing\n\n```shell\n$ pip install fastcdc\n```\n\nTo enable add additional support for the hash algorithms\n([xxhash](https://github.com/Cyan4973/xxHash) and\n[blake3](https://github.com/BLAKE3-team/BLAKE3/)) use\n\n```shell\n$ pip install fastcdc[hashes]\n```\n\n## Usage\n\n### Calculate chunks with default settings:\n```shell\n$ fastcdc tests/SekienAkashita.jpg\nhash=103159aa68bb1ea98f64248c647b8fe9a303365d80cb63974a73bba8bc3167d7 offset=0 size=22366\nhash=3f2b58dc77982e763e75db76c4205aaab4e18ff8929e298ca5c58500fee5530d offset=22366 size=10491\nhash=fcfb2f49ccb2640887a74fad1fb8a32368b5461a9dccc28f29ddb896b489b913 offset=32857 size=14094\nhash=bd1198535cdb87c5571378db08b6e886daf810873f5d77000a54795409464138 offset=46951 size=18696\nhash=d6347a2e5bf586d42f2d80559d4f4a2bf160dce8f77eede023ad2314856f3086 offset=65647 size=43819\n```\n\n### Customize min-size, avg-size, max-size, and hash function\n```shell\n$ fastcdc -mi 16384 -s 32768 -ma 65536 -hf sha256 tests/SekienAkashita.jpg\nhash=5a80871bad4588c7278d39707fe68b8b174b1aa54c59169d3c2c72f1e16ef46d offset=0 size=32857\nhash=13f6a4c6d42df2b76c138c13e86e1379c203445055c2b5f043a5f6c291fa520d offset=32857 size=16408\nhash=0fe7305ba21a5a5ca9f89962c5a6f3e29cd3e2b36f00e565858e0012e5f8df36 offset=49265 size=60201\n```\n\n###  Scan files in directory and report duplication.\n```shell\n$ fastcdc scan ~/Downloads\n[####################################]  100%\nFiles:          1,332\nChunk Sizes:    min 4096 - avg 16384 - max 131072\nUnique Chunks:  506,077\nTotal Data:     9.3 GB\nDupe Data:      873.8 MB\nDeDupe Ratio:   9.36 %\nThroughput:     135.2 MB/s\n```\n\n### Show help\n\n```shell\n$ fastcdc\nUsage: fastcdc [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  chunkify*  Find variable sized chunks for FILE and compute hashes.\n  benchmark  Benchmark chunking performance.\n  scan       Scan files in directory and report duplication.\n```\n\n### Use from your python code\nThe  tests also have some short examples of using the chunker, of which this\ncode snippet is an example:\n\n```python\nfrom fastcdc import fastcdc\n\nresults = list(fastcdc("tests/SekienAkashita.jpg", 16384, 32768, 65536))\nassert len(results) == 3\nassert results[0].offset == 0\nassert results[0].length == 32857\nassert results[1].offset == 32857\nassert results[1].length == 16408\nassert results[2].offset == 49265\nassert results[2].length == 60201\n```\n\n## Reference Material\n\nThe algorithm is as described in "FastCDC: a Fast and Efficient Content-Defined\nChunking Approach for Data Deduplication"; see the\n[paper](https://www.usenix.org/system/files/conference/atc16/atc16-paper-xia.pdf),\nand\n[presentation](https://www.usenix.org/sites/default/files/conference/protected-files/atc16_slides_xia.pdf)\nfor details. There are some minor differences, as described below.\n\n### Differences with the FastCDC paper\n\nThe explanation below is copied from\n[ronomon/deduplication](https://github.com/ronomon/deduplication) since this\ncodebase is little more than a translation of that implementation:\n\n> The following optimizations and variations on FastCDC are involved in the chunking algorithm:\n> * 31 bit integers to avoid 64-bit integers for the sake of the Javascript reference implementation.\n> * A right shift instead of a left shift to remove the need for an additional modulus operator, which would otherwise have been necessary to prevent overflow.\n> * Masks are no longer zero-padded since a right shift is used instead of a left shift.\n> * A more adaptive threshold based on a combination of average and minimum chunk size (rather than just average chunk size) to decide the pivot point at which to switch masks. A larger minimum chunk size now switches from the strict mask to the eager mask earlier.\n> * Masks use 1 bit of chunk size normalization instead of 2 bits of chunk size normalization.\n\nThe primary objective of this codebase was to have a Python implementation with a\npermissive license, which could be used for new projects, without concern for\ndata parity with existing implementations.\n\n## Prior Art\n\nThis package started as Python port of the implementation by Nathan Fiedler (see the\nnlfiedler link below).\n\n* [nlfiedler/fastcdc-rs](https://github.com/nlfiedler/fastcdc-rs)\n    + Rust implementation on which this code is based.\n* [ronomon/deduplication](https://github.com/ronomon/deduplication)\n    + C++ and JavaScript implementation on which the rust implementation is based.\n* [rdedup_cdc at docs.rs](https://docs.rs/crate/rdedup-cdc/0.1.0/source/src/fastcdc.rs)\n    + An alternative implementation of FastCDC to the one in this crate.\n* [jrobhoward/quickcdc](https://github.com/jrobhoward/quickcdc)\n    + Similar but slightly earlier algorithm by some of the same researchers.\n\n## Change Log\n\n## [1.7.0] - 2024-06-27\n- Performance improvement [@dw](https://github.com/dw)\n- Fixed issue with inputs smaller than min_size [@grote](https://github.com/grote)\n\n## [1.6.0] - 2024-05-09\n- added python 3.12 support\n- removed python 3.7 support\n- updated dependencies\n\n## [1.5.0] - 2023-03-13\n- added python 3.10/3.11 support\n- removed python 3.6 support\n- update dependencies\n\n## [1.4.2] - 2020-11-25\n- add binary releases to PyPI (Xie Yanbo)\n- update dependencies\n\n## [1.4.1] - 2020-09-30\n- fix issue with fat option in cython version\n- updated dependencies\n\n## [1.4.0] - 2020-08-08\n- add support for multiple path with scan command\n- fix issue with building cython extension\n- fix issue with fat option\n- fix zero-devision error\n\n## [1.3.0] - 2020-06-26\n- add new `scan` command to calculate deduplication ratio for directories\n\n## [1.2.0] - 2020-05-23\n\n### Added\n- faster optional cython implementation\n- benchmark command\n\n## [1.1.0] - 2020-05-09\n\n### Added\n- high-level API\n- support for streams\n- support for custom hash functions\n\n\n## [1.0.0] - 2020-05-07\n\n### Added\n- Initial release (port of [nlfiedler/fastcdc-rs](https://github.com/nlfiedler/fastcdc-rs)).\n\n',
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iscc/fastcdc-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
