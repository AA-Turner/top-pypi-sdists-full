# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['evergreen', 'evergreen.cli', 'evergreen.errors', 'evergreen.metrics']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7',
 'PyYAML>=5',
 'pydantic>=1',
 'python-dateutil>=2',
 'requests>=2',
 'structlog>=19']

entry_points = \
{'console_scripts': ['evg-api = evergreen.cli.main:main']}

setup_kwargs = {
    'name': 'evergreen-py',
    'version': '3.11.4',
    'description': 'Python client for the Evergreen API',
    'long_description': '# Evergreen.py\n\nA client library for the Evergreen API written in python. Currently supports the V2 version of\nthe API. For more details, see https://github.com/evergreen-ci/evergreen/wiki/REST-V2-Usage.\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/evergreen.py) [![PyPI](https://img.shields.io/pypi/v/evergreen.py.svg)](https://pypi.org/project/evergreen.py/) [![Coverage Status](https://coveralls.io/repos/github/evergreen-ci/evergreen.py/badge.svg?branch=master)](https://coveralls.io/github/evergreen-ci/evergreen.py?branch=master)\n\n## Table of contents\n\n1. [Description](#description)\n2. [Getting Help](#getting-help)\n3. [Dependencies](#dependencies)\n4. [Installation](#installation)\n5. [Usage](#usage)\n6. [Documentation](#documentation)\n7. [Contributor\'s Guide](#contributors-guide)\n   - [Setting up a local development environment](#setting-up-a-local-development-environment)\n   - [Linting/formatting](#lintingformatting)\n   - [Running tests](#running-tests)\n   - [Automatically running checks on commit](#automatically-running-checks-on-commit)\n   - [Versioning](#versioning)\n   - [Code Review](#code-review)\n   - [Deployment](#deployment)\n\n## Description\n\nThis is a Python client library for interacting with Evergreen and Evergreen objects. It currently only\nsupports the V2 version of Evergreen\'s api. It can be used either by Python code in a separate application\nor on the command line to get data about Evergreen objects quickly and easily.\n\n## Getting Help\n\n### What\'s the right channel to ask my question?\n\nIf you have a question about evergreen.py, please mention @dag-on-call in\nslack channel [#evergreen-users](https://mongodb.slack.com/messages/#evergreen-users/),\nor email us at devprod-si-team@mongodb.com.\n\n### How can I request a change/report a bug in evergreen.py?\n\nCreate a [DEVPROD ticket](https://jira.mongodb.org/projects/DEVPROD).\n\n### What should I include in my ticket or #evergreen-users question?\n\nSince #evergreen-users questions are interrupts,\nplease include as much information as possible.\nThis can help avoid long information-gathering threads.\n\nPlease include the following:\n\n- **Motivation for Request**\n  - provide us the motivation for this change.\n- **Context**\n  - provide some background contexts for this issue.\n- **Description**\n  - provide some descriptions on how this issue happened.\n\n## Dependencies\n\n- Python 3.9 or later\n\n## Installation\n\n```bash\n$ pip install evergreen.py\n```\n\n## Usage\n\nThis client can be used either in code or directly via the command line.\n\nIn code:\n\n```python\n>> from evergreen.api import EvgAuth, EvergreenApi\n>> api = EvergreenApi.get_api(EvgAuth(\'your.username\', \'***\'))\n>> project = api.project_by_id(\'mongodb-mongo-master\')\n>> project.display_name\n\'MongoDB (master)\'\n```\n\nCli:\n\n```bash\n$ evg-api --json list-hosts\n{\n    "host_id": "host num 0",\n    "host_url": "host.num.com",\n    "distro": {\n        "distro_id": "ubuntu1804-build",\n        "provider": "static",\n        "image_id": ""\n    },\n    "provisioned": true,\n    "started_by": "mci",\n    "host_type": "",\n    "user": "mci-exec",\n    "status": "running",\n    "running_task": {\n        "task_id": null,\n        "name": null,\n        "dispatch_time": null,\n        "version_id": null,\n        "build_id": null\n    },\n    "user_host": false\n}\n```\n\nThe `patch_from_diff` API requires the Evergreen CLI to be installed.\nAdd the following to the host\'s DOCKERFILE:\n\n```bash\nRUN wget https://evergreen.mongodb.com/clients/linux_amd64/evergreen\nRUN chmod +x evergreen\nENV PATH="/project:$PATH"\n```\n\nYou will need to provide an .evergreen.yml file with credentials to use the CLI. Assuming you are using the [web-app](https://github.com/10gen/helm-charts/tree/master/charts/web-app) chart this can be done by [mounting](https://kanopy.corp.mongodb.com/docs/getting_started/application_configuration/#configuration-filesvolumes) [kubernetes secrets](https://kanopy.corp.mongodb.com/docs/cheatsheet/#interacting-with-kubernetes-secrets) in your pod.\n\nStore the secret in the cluster:\n\n```bash\nkubectl create secret generic <secret_name> --from-file .evergreen.yml --namespace <namespace>\n```\n\nIn environments/deployment.yml configure the file to be mounted and linked to the correct location:\n\n```yaml\nvolumeSecrets:\n  - name: <secret_name>\n    path: /etc/secrets\nlifecycle:\n  postStart:\n    type: exec\n    command:\n      - /bin/sh\n      - -c\n      - ln -sf /etc/secrets/.evergreen.yml\n```\n\n## Documentation\n\nYou can find the documentation [here](https://evergreen-ci.github.io/evergreen.py/).\n\n## Contributor\'s Guide\n\n### Setting up a local development environment\n\n#### Requirements\n\n- Poetry 1.1 or later\n\nYou will need Evergreen credentials on your local machine to use this library or the attached CLI. You\ncan set up your credentials by following the link [here](https://github.com/evergreen-ci/evergreen/wiki/Using-the-Command-Line-Tool#downloading-the-command-line-tool).\n\n### Linting/formatting\n\nThis project uses [black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/) for linting/formatting.\n\n```bash\npoetry run black src tests\npoetry run isort src tests\n```\n\n### Running tests\n\n```bash\npoetry run pytest\n```\n\nThere are a few tests that are slow running. These tests are not run by default, but can be included\nby setting the env variable RUN_SLOW_TESTS to any value.\n\n```\n$ RUN_SLOW_TEST=1 poetry run pytest\n```\n\nTo get code coverage information:\n\n```\n$ poetry run pytest --cov=src --cov-report=html\n```\n\n### Automatically running checks on commit\n\nThis project has [pre-commit](https://pre-commit.com/) configured. Pre-commit will run\nconfigured checks at git commit time. To enable pre-commit on your local repository run:\n\n```bash\n$ poetry run pre-commit install\n```\n\n### Versioning\n\nBefore deploying a new version, please update the `CHANGELOG.md` file with a description of what\nis being changed.\n\nDeployment to [PyPi](https://pypi.org/project/evergreen.py/) are done automatically on merges to master.\nIn order to avoid overwriting a previous deploy, the version should be updated on all changes. The\n[semver](https://semver.org/) versioning scheme should be used for determining the version number.\n\nThe version is found in the `pyproject.toml` file.\n\n### Code Review\n\nThis project uses the GitHub merge queue. Click "Merge when ready" as soon as you\'d like.\n\n### Deployment\n\nDeployment to [PyPi](https://pypi.org/project/evergreen.py/) is automatically triggered on merges to master.\n',
    'author': 'DevProd Services & Integrations Team',
    'author_email': 'devprod-si-team@mongodb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/evergreen-ci/evergreen.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
