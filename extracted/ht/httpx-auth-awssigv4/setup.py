# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['httpx_auth_awssigv4', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['httpx>0.20.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0'],
 'test': ['jinja2==2.11.3',
          'markupsafe==2.0.1',
          'black>=22.3.0,<23.0.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0',
          'mkdocs-material-extensions>=1.0.1,<2.0.0']}

setup_kwargs = {
    'name': 'httpx-auth-awssigv4',
    'version': '0.1.4',
    'description': 'This package provides utilities to add AWS Signature V4 authentication infrormation to calls made by python httpx library.',
    'long_description': '# httpx-auth-awssigv4\n\n\n[![pypi](https://img.shields.io/pypi/v/httpx-auth-awssigv4.svg)](https://pypi.org/project/httpx-auth-awssigv4/)\n[![python](https://img.shields.io/pypi/pyversions/httpx-auth-awssigv4.svg)](https://pypi.org/project/httpx-auth-awssigv4/)\n[![Build Status](https://github.com/mmuppidi/httpx-auth-awssigv4/actions/workflows/dev.yml/badge.svg)](https://github.com/mmuppidi/httpx-auth-awssigv4/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/mmuppidi/httpx-auth-awssigv4/branch/master/graphs/badge.svg)](https://codecov.io/github/mmuppidi/httpx-auth-awssigv4)\n\n\n\nThis package provides utilities to add [AWS Signature V4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) authentication infrormation to calls made by python [httpx](https://www.python-httpx.org/) library.\n\n\n* Documentation: <https://mmuppidi.github.io/httpx-auth-awssigv4>\n* GitHub: <https://github.com/mmuppidi/httpx-auth-awssigv4>\n* PyPI: <https://pypi.org/project/httpx-auth-awssigv4/>\n* MIT License\n\n## Installation\n\n```bash\npip install httpx-auth-awssigv4\n```\n\n## Usage\n\n### Basic Usage\n\nThis library has primarily been developed to help add authentication support to [httpx](https://www.python-httpx.org/) library while making calls to\nREST API deployed using AWS API Gateway service. Will be extended in future to help with calling AWS services.\n\n```python\nimport httpx\nfrom httpx_auth_awssigv4 import Sigv4Auth\n\n# creating a callable for httpx library\nauth = Sigv4Auth(\n    access_key="AWS_ACCESS_KEY_ID",\n    secret_key="AWS_SECRET_ACCESS_KEY",\n    service="execute-api",\n    region="us-east-1"\n)\n\n# Calling an API endpoint deployed using AWS API Gateway which has\n# AWS_IAM set as authorization type\n\nresponse = httpx.get(\n    url="https://<API ID>.execute-api.<Region>.amazonaws.com/prod/detials",\n    params={"username": "tstark"},\n    auth=auth\n)\n\n# Making a post call\n\nresponse = httpx.get(\n    url="https://<API ID>.execute-api.<Region>.amazonaws.com/prod/details",\n    params={"username": "tstark"},\n    json={"mission": "avengers"},\n    auth=auth\n)\n```\n\n### With STS credentials\n\n`Sigv4Auth` can be used with temporary credentials generated with tools like [aws-sso-util](https://github.com/benkehoe/aws-sso-util).\n\n```python\nimport boto3\nfrom httpx_auth_awssigv4 import Sigv4Auth\n\n# fetch temporary credentials from AWS STS service\ncredentials = boto3.Session(profile_name="<profile>").get_credentials()\n\n# creating a callable for httpx library\nauth = Sigv4Auth(\n    access_key=credentials.access_key,\n    secret_key=credentials.secret_key,\n    token=credentials.token\n    service="execute-api",\n    region="us-east-1"\n)\n\n```\n\n`Sigv4Auth` can also be used with temporary credentials from AWS STS.\n\n```python\nimport boto3\nfrom httpx_auth_awssigv4 import Sigv4Auth\n\n# role with `execute-api` permissions\nROLE_ARN="arn:aws:iam::<ACCOUNT ID>:role/<ROLE NAME"\n\n# fetch temporary credentials from AWS STS service\ncredentials = boto3.client(\'sts\').assume_role(\n    RoleArn=ROLE_ARN,\n    RoleSessionName="httpxcall"\n)["Credentials"]\n\n# creating a callable for httpx library\nauth = Sigv4Auth(\n    access_key=credentials["AccessKeyId"],\n    secret_key=credentials["SecretAccessKey"],\n    token=credentials["SessionToken"]\n    service="execute-api",\n    region="us-east-1"\n)\n\n```\n\n## ToDo\n\n- Add examples on usage along with API backend deployment instructions.\n- Test the library with AWS services and add integration tests.\n\n## Credits\n\n- This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Mohan Muppidi',
    'author_email': 'mkumar2301@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mmuppidi/httpx-auth-awssigv4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
