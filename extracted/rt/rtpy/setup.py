# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtpy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.18.4,<3.0.0']

setup_kwargs = {
    'name': 'rtpy',
    'version': '1.4.9',
    'description': 'Python wrapper for the JFrog Artifactory REST API.',
    'long_description': '# rtpy\n\n[![image](https://img.shields.io/pypi/v/rtpy.svg)](https://pypi.org/project/rtpy/)\n[![image](https://img.shields.io/pypi/pyversions/rtpy.svg)](https://pypi.org/project/rtpy/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Documentation Status](https://readthedocs.org/projects/rtpy/badge/?version=latest)](https://rtpy.readthedocs.io/en/latest/?badge=latest)\n[![image](https://img.shields.io/pypi/l/rtpy.svg)](https://pypi.org/project/rtpy/)\n\nPython wrapper for the **[JFrog Artifactory REST API](https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API)**\n<br/>\n<br/>\n\n## Documentation\n\n**[https://rtpy.rtfd.io](https://rtpy.rtfd.io)**\n\n<br/>\n\n## Installation\n\n```shell\n$ pip install rtpy\n```\n<br/>\n\n## Usage\n\n```python\nimport rtpy\n\n# instantiate a rtpy.Rtpy object\nsettings = {}\nsettings["af_url"] = "http://..."\nsettings["api_key"] = "123QWA..."\n# settings["username"] = "my_username"\n# settings["password"] = "my_password"\n\naf = rtpy.Rtpy(settings)\n\n# use a method\nr = af.system_and_configuration.system_health_ping()\nprint(r)\n# OK\n```\n<br/>\n\n## Running the tests\n\n### Requirements :\n\n- Dependencies : see [tool.poetry.dependencies] and [tool.poetry.dev-dependencies] in [pyproject.toml](./pyproject.toml)\n- Artifactory instance (with a valid license) running\n\n**NEVER run the tests on a production instance!**\n\n\n### Launch\n\n- Set the following environment variables:\n    - AF_TEST_URL\n    - AF_TEST_USERNAME\n    - AF_TEST_PASSWORD\n\nThe user must have admin privileges (it\'s API key will be revoked during the tests)\n- Clone the repository and launch the tests using the command :\n\n```shell\n$ python -m pytest -v\n```',
    'author': 'Guillaume Renault',
    'author_email': 'me@grenault.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Orange-OpenSource/rtpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
