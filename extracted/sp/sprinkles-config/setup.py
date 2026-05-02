# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sprinkles']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2', 'boto3', 'click', 'tomlkit']

entry_points = \
{'console_scripts': ['sprinkles = sprinkles.commands:generate_config']}

setup_kwargs = {
    'name': 'sprinkles-config',
    'version': '0.1.4',
    'description': 'Generate config files from AWS Secrets',
    'long_description': '[![PyPI version](https://badge.fury.io/py/sprinkles-config.svg)](https://badge.fury.io/py/sprinkles-config)\n\n# sprinkles\n\nSprinkles makes it easy to share configuration files between local dev\nenvironments without leaking private information. No more passwords in Slack\nPMs, no more API keys in VCS.\n\n# Installation\n\n```shell script\npip install sprinkles-config\n```\n\nPlease note that sprinkles has only been tested for Python versions >= 3.6.\n\n# Usage\n\nSprinkles reads secrets from AWS secrets manager, and binds them to a template\nyou provide. The templating is based on Jinja2¹, making it flexible enough to\nwork with any text-based configuration format you may be using. Anything from\n.env files, to Java properties, to yaml.\n\nIt has a simple param based CLI API, but can also be executed against a config\nfile to encourage reuse. The config format is TOML-based².\n\nNOTE: Sprinkles will use the AWS profile/credentials configured in the calling shell\ncontext, using the standard environment variables³.\n\n## CLI\n\n1. Output config to stdout\n\n```properties\nthird.party.api.endpoint=https://example.com/api/v1\nthird.party.api.key={{THIRD_PARTY_API_KEY}}\n```\n\n```\nsprinkles --template application.properties.j2 --secret-arn arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name>\n```\n\n2. Output to file\n\n```\nsprinkles --template application.properties.j2 --secret-arn arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name> --output application.properties\n```\n\n## Config file option\n\nSprinkles also makes it possible to have a set of defaults (tracked in VCS).\nAdd a .sprinklesrc file in your project root. Simply run `sprinkles` in the\nproject root to initialize the config.\n\n\n.sprinklesrc\n```toml\n[secret]\narn = "arn:aws:secretsmanager:<region>:<account-id-number>:secret:<secret-name>"\n\n[files]\n  [files.docker-env]\n    template = "sprinkles-templates/.env.sprinkles"\n    target = ".env"\n  [files.application-properties]\n    template = "sprinkles-templates/application.properties.sprinkles"\n    target = "src/main/com/example/resources/application-dev.properties"\n```\n\n# References\n\n1. Jinja2: https://jinja.palletsprojects.com/en/2.11.x/\n2. TOML: https://github.com/toml-lang/toml\n3. AWS Configuration: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html\n',
    'author': 'Okal Otieno',
    'author_email': 'okal@justokal.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/okal/sprinkles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
