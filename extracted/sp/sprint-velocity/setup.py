# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sprint_velocity']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib', 'pandas', 'pendulum', 'requests', 'strongtyping', 'typer[all]']

entry_points = \
{'console_scripts': ['jira_statistics = sprint_velocity.main:app']}

setup_kwargs = {
    'name': 'sprint-velocity',
    'version': '1.0.5',
    'description': 'Generating a Matplotlib plot to see the scrum velocity for a sprint.',
    'long_description': "![Python application](https://github.com/FelixTheC/jira_srcum_velocity/workflows/Python%20application/badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n# Jira Sprint Velocity\n- generate a Sprint Velocity Matplotlib Graph\n\n## How To Use\n```shell\n$ jira_statistics --help\n\n```\n\n## Used Jira Filter\n- to get all issues for generating the Velocity we're using following Statement\n```shell\nproject = <project> and issuetype in subTaskIssueTypes() AND Sprint = <sprint_id> AND (resolution = unresolved or resolved >= <sprint_start_date>)\n```\n\n## Authentication\n- the rest api from jira uses a Bearer Token, this Token can be created directly in Jira under Profile\n\n\n## Example Result\n![SprintVelocity](images/test.png)\n",
    'author': 'FelixTheC',
    'author_email': 'fberndt87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FelixTheC/jira_srcum_velocity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
