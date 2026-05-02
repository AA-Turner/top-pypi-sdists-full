# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ramodels', 'ramodels.lora', 'ramodels.mo', 'ramodels.mo.details']

package_data = \
{'': ['*']}

install_requires = \
['mkdocstrings[python]>=0.19.0,<0.20.0',
 'more-itertools>=9.0.0,<10.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

entry_points = \
{'console_scripts': ['lorafetch = ramodels.fetch:gen_models']}

setup_kwargs = {
    'name': 'ramodels',
    'version': '50.12.1',
    'description': 'Pydantic data models for OS2mo',
    'long_description': '<!--\nSPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>\nSPDX-License-Identifier: MPL-2.0\n-->\n\n\n# MoLoRa Data Models\n\nRAModels - MoLoRa data validation models powered by [pydantic](https://github.com/samuelcolvin/pydantic/#pydantic).\n\n## Versioning\nThis project uses [Semantic Versioning](https://semver.org/) with the following strategy:\n- MAJOR: Incompatible changes to existing data models\n- MINOR: Backwards compatible updates to existing data models OR new models added\n- PATCH: Backwards compatible bug fixes\n\n\n## Authors\n\nMagenta ApS <https://magenta.dk>\n\n## License\n- This project: [MPL-2.0](MPL-2.0.txt)\n- Dependencies:\n  - pydantic: [MIT](MIT.txt)\n\nThis project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.\n\n## Development\n### Prerequisites\n\n- [Poetry](https://github.com/python-poetry/poetry)\n- [Pre-commit](https://github.com/pre-commit/pre-commit)\n\n\n### Getting Started\n\n1. Clone the repository:\n`git clone git@git.magenta.dk:rammearkitektur/ra-data-models.git`\n\n2. Install all dependencies:\n`poetry install`\n\n3. Set up pre-commit:\n`pre-commit install`\n\n\n### Running the tests\n\nYou use `poetry` and `pytest` to run the tests:\n\n`poetry run pytest`\n\n\nYou can also run specific files\n\n`poetry run pytest tests/<test_folder>/<test_file.py>`\n\nand even use filtering with `-k`\n\n`poetry run pytest -k "Manager"`\n\n\nYou can use the flags `-vx` where `v` prints the test & `x` makes the test stop if any tests fails (Verbose, X-fail)\n\n### Pre-commit usage\nPre-commit must either be used via your virtual environment or globally.\nIf you want to pre-commit globally, the following extra dependencies are needed:\n`pip install mypy pydantic`\n\n\n### Models\n\n## LoRa\n`LoRa` implements the OIO standard version 1.1. The [standard](https://digitaliser.dk/resource/1569113) with\n[specification](https://www.digitaliser.dk/resource/1569113/artefact/Specifikationafserviceinterfacefororganisation-OIO-Godkendt%5bvs.1.1%5d.pdf?artefact=true&PID=1569586)\n',
    'author': 'Magenta',
    'author_email': 'info@magenta.dk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://magenta.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
