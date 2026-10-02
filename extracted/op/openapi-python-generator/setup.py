# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['openapi_python_generator',
 'openapi_python_generator.language_converters',
 'openapi_python_generator.language_converters.python',
 'openapi_python_generator.parsers']

package_data = \
{'': ['*'],
 'openapi_python_generator.language_converters.python': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'black>=21.10b0',
 'click>=8.1.3,<9.0.0',
 'httpx[all]>=0.28.0,<0.29.0',
 'importlib-metadata>=8.7.0,<9.0.0',
 'isort>=5.10.1',
 'openapi-pydantic>=0.5.1,<0.6.0',
 'orjson>=3.9.15,<4.0.0',
 'pydantic>=2.10.2,<3.0.0',
 'pyyaml>=6.0.2,<7.0.0']

entry_points = \
{'console_scripts': ['openapi-python-generator = '
                     'openapi_python_generator.__main__:main']}

setup_kwargs = {
    'name': 'openapi-python-generator',
    'version': '2.1.2',
    'description': 'Openapi Python Generator',
    'long_description': "# Openapi Python Generator\n\n[![PyPI](https://img.shields.io/pypi/v/openapi-python-generator.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/openapi-python-generator.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/openapi-python-generator)][python version]\n[![License](https://img.shields.io/pypi/l/openapi-python-generator)][license]\n\n[![](https://img.shields.io/static/v1?label=documentation&message=enabled&color=<COLOR>)][documentation]\n[![Tests](https://github.com/MarcoMuellner/openapi-python-generator/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/MarcoMuellner/openapi-python-generator/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/openapi-python-generator/\n[status]: https://pypi.org/project/openapi-python-generator/\n[python version]: https://pypi.org/project/openapi-python-generator\n[documentation]: https://marcomuellner.github.io/openapi-python-generator/\n[tests]: https://github.com/MarcoMuellner/openapi-python-generator/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/MarcoMuellner/openapi-python-generator\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n![](logo.png)\n\n---\n__Documentation:__ [here][documentation]\n\n---\n\n## Features\n\n- __Ease of use__. Provide input, output and the library, and the generator will do the rest.\n- __Type safety and type hinting.__ __OpenAPI python generator__ makes heavy use of pydantic models to provide type-safe data structures.\n- __Support for multiple rest frameworks.__ __OpenAPI python generator__ currently supports the following:\n    - [httpx](https://pypi.org/project/httpx/)\n    - [requests](https://pypi.org/project/requests/)\n    - [aiohttp](https://pypi.org/project/aiohttp/)\n- __Async and sync code generation support__, depending on the framework. It will automatically create both for frameworks that support both.\n- __Easily extendable using Jinja2 templates__. The code is designed to be easily extendable and should support even more languages and frameworks in the future.\n- __Fully tested__. Every generated code is automatically tested against the OpenAPI spec and we have 100% coverage.\n- __Usage as CLI or as library__.\n\n## Requirements\n\n- Python 3.7+\n\n## Installation\n\nYou can install _Openapi Python Generator_ via [pip] from [PyPI]:\n\n```console\n$ pip install openapi-python-generator\n```\n\n## Usage\n\nPlease see the [Quick start page] for details.\n\n## Roadmap\n\n- Support for all commonly used http libraries in the python ecosystem (~~requests~~, urllib, ...)\n- Support for multiple languages\n- Support for multiple authentication schemes\n- Support custom themes\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Openapi Python Generator_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nSpecial thanks to the peeps from [openapi-schema-pydantic](https://github.com/kuimono/openapi-schema-pydantic),\nwhich already did a lot of the legwork by providing a pydantic schema for the OpenAPI 3.0.0+ specification.\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/MarcoMuellner/openapi-python-generator/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/MarcoMuellner/openapi-python-generator/blob/main/LICENSE\n[contributor guide]: https://github.com/MarcoMuellner/openapi-python-generator/blob/main/CONTRIBUTING.md\n[Quick start page]: https://marcomuellner.github.io/openapi-python-generator/quick_start/\n",
    'author': 'Marco Müllner',
    'author_email': 'muellnermarco@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MarcoMuellner/openapi-python-generator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
