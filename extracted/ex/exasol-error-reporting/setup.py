# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exasol', 'exasol.error']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ec = exasol.error._cli:main']}

setup_kwargs = {
    'name': 'exasol-error-reporting',
    'version': '1.0.0',
    'description': 'Exasol Python Error Reporting',
    'long_description': '# Exasol Error Reporting\n\nThis project contains a Python library for describing Exasol error messages.\nThis library lets you define errors with a uniform set of attributes.\nFurthermore, the error message is implemented to be parseable,\nso that you can extract an error catalog from the code.\n\n## In a Nutshell\n\n### Install the library\n\n```shell\npip install exasol-error-reporting\n```\n\n### Create a Simple Error\n\n```python\nfrom exasol import error\n\nerror1 = error.ExaError(\n    "E-TEST-1", "A trivial error", "No mitigation available", {}\n)\n```\n\n### Specify Multiple Mitigations\n```python\nfrom exasol import error\n\nerror2 = error.ExaError(\n    "E-TEST-2",\n    message="Fire in the server room",\n    mitigations=[\n        "Use the fire extinguisher",\n        "Flood the room with halon gas (Attention: make sure no humans are in the room!)"\n    ],\n    parameters={}\n)\n```\n\n### Error Parameter(s) without description\n\n```python\nfrom exasol import error\n\nerror3 = error.ExaError(\n    "E-TEST-2",\n    "Not enough space on device {{device}}.",\n    "Delete something from {{device}}.",\n    {"device": "/dev/sda1"},\n)\n```\n### Error with detailed Parameter(s) \n\n```python\nfrom exasol import error\nfrom exasol.error import Parameter\n\nerror4 = error.ExaError(\n    "E-TEST-2",\n    "Not enough space on device {{device}}.",\n    "Delete something from {{device}}.",\n    {"device": Parameter("/dev/sda1", "name of the device")},\n)\n```\n\nCheck out the [user guide](doc/user_guide/user_guide.md) for more details.\n\n## Tooling\n\nThe `exasol-error-reporting` library comes with a command line tool (`ec`) which also can be invoked\nby using its package/module entry point (`python -m exasol.error`).\nFor detailed information about the usage consider consulting the help `ec --help` or `python -m exasol.error --help`.\n\n### Parsing the error definitions in a python file(s)\n\n```shell\nec parse some-python-file.py \n```\n\n```shell\nec parse < some-python-file.py \n```\n\n## Generating an error-code data file\n\nIn order to generate a [error-code-report](https://schemas.exasol.com/error_code_report-1.0.0.json) compliant data file,\nyou can use the generate subcommand.\n\n```shell\nec generate NAME VERSION PACKAGE_ROOT > error-codes.json\n```\n\n\n## Links and References\n\nFor further details check out the [project documentation](https://exasol.github.io/error-reporting-python/).\n',
    'author': 'Umit Buyuksahin',
    'author_email': 'umit.buyuksahin@exasol.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/exasol/error-reporting-python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
