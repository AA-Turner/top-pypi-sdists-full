# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_health']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0']

setup_kwargs = {
    'name': 'fastapi-health',
    'version': '0.4.0',
    'description': 'Heath check on FastAPI applications.',
    'long_description': '<h1 align="center">\n    <strong>FastAPI Health 🚑️</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/fastapi-health" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-health" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/fastapi-health/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/fastapi-health">\n    <br />\n    <a href="https://pypi.org/project/fastapi-health" target="_blank">\n        <img src="https://img.shields.io/pypi/v/fastapi-health" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/fastapi-health">\n    <img src="https://img.shields.io/github/license/Kludex/fastapi-health">\n</p>\n\nThe goal of this package is to help you to implement the [Health Check API](https://microservices.io/patterns/observability/health-check-api.html) pattern.\n\n## Installation\n\n``` bash\npip install fastapi-health\n```\n\n## Quick Start\n\nCreate the health check endpoint dynamically using different conditions. Each condition is a\ncallable, and you can even have dependencies inside of it:\n\n```python\nfrom fastapi import FastAPI, Depends\nfrom fastapi_health import health\n\n\ndef get_session():\n    return True\n\n\ndef is_database_online(session: bool = Depends(get_session)):\n    return session\n\n\napp = FastAPI()\napp.add_api_route("/health", health([is_database_online]))\n```\n\n## Advanced Usage\n\nThe `health()` method receives the following parameters:\n- `conditions`: A list of callables that represents the conditions of your API, it can return either `bool` or a `dict`.\n- `success_output`: An optional dictionary that will be the content response of a successful health call.\n- `failure_output`: An optional dictionary analogous to `success_output` for failure scenarios.\n- `success_status`: An integer that overwrites the default status (200) in case of success.\n- `failure_status`: An integer that overwrites the default status (503) in case of failure.\n\nIt\'s important to notice that you can have a _peculiar_ behavior in case of hybrid return statements (`bool` and `dict`) on the conditions.\nFor example:\n\n``` Python\nfrom fastapi import FastAPI\nfrom fastapi_health import health\n\n\ndef healthy_condition():\n    return {"database": "online"}\n\n\ndef sick_condition():\n    return False\n\n\napp = FastAPI()\napp.add_api_route("/health", health([healthy_condition, sick_condition]))\n```\n\nThis will generate a response composed by the status being 503 (default `failure_status`), because `sick_condition` returns `False`, and the JSON body `{"database": "online"}`. It\'s not wrong, or a bug. It\'s meant to be like this.\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/fastapi-health',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
