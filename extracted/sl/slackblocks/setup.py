# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slackblocks', 'slackblocks.rich_text']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'slackblocks',
    'version': '1.0.16',
    'description': 'Python wrapper for the Slack Blocks API',
    'long_description': '# slackblocks <img src="https://github.com/nicklambourne/slackblocks/raw/master/docs_src/img/sb.png" align="right" width="250px"/>\n\n![Licence: MIT](https://img.shields.io/badge/License-MIT-green.svg)\n![Licence: BSD-3-Clause](https://img.shields.io/badge/License-BSD_3_Clause-green.svg)\n![Python Versions](https://img.shields.io/pypi/pyversions/slackblocks)\n[![PyPI](https://img.shields.io/pypi/v/slackblocks?color=yellow&label=PyPI&logo=python&logoColor=white)](https://pypi.org/project/slackblocks/#history)\n[![Downloads](https://static.pepy.tech/badge/slackblocks)](https://pepy.tech/project/slackblocks)\n[![Build Status](https://github.com/nicklambourne/slackblocks/actions/workflows/unit-tests.yml/badge.svg?branch=master)](https://github.com/nicklambourne/slackblocks/actions)\n[![Docs](https://img.shields.io/badge/Docs-8A2BE2.svg)](https://nicklambourne.github.io/slackblocks)\n\n## What is it?\n`slackblocks` is a Python API for building messages in the fancy Slack [Block Kit API](https://api.slack.com/block-kit)\n\n## Documentation\nFull documentation is provided [here](https://nicklambourne.github.io/slackblocks/latest/).\n\n## Requirements\n`slackblocks` requires Python >= 3.8.\n\nAs of version 0.1.0 it has no dependencies outside the Python standard library.\n\n## Installation\n```bash\npip install slackblocks\n```\n\n## Basic Usage\n```python\nfrom slackblocks import Message, SectionBlock\n\n\nblock = SectionBlock("Hello, world!")\nmessage = Message(channel="#general", blocks=block)\nmessage.json()\n\n```\n\nWill produce the following JSON string:\n```json\n{\n    "channel": "#general",\n    "mrkdwn": true,\n    "blocks": [\n        {\n            "type": "section",\n            "block_id": "992ceb6b-9ad4-496b-b8e6-1bd8a632e8b3",\n            "text": {\n                "type": "mrkdwn",\n                "text": "Hello, world!"\n            }\n        }\n    ]\n}\n```\nWhich can be sent as payload to the Slack message API HTTP endpoints.\n\nOf more practical use is the ability to unpack the objects directly into \nthe [(Legacy) Python Slack Client](https://pypi.org/project/slackclient/) in order to send messages:\n\n```python\nfrom os import environ\nfrom slack import WebClient\nfrom slackblocks import Message, SectionBlock\n\n\nclient = WebClient(token=environ["SLACK_API_TOKEN"])\nblock = SectionBlock("Hello, world!")\nmessage = Message(channel="#general", blocks=block)\n\nresponse = client.chat_postMessage(**message)\n```\n\nOr the modern Python [Slack SDK](https://pypi.org/project/slack-sdk/):\n```python\nfrom os import environ\nfrom slack_sdk import WebClient\nfrom slackblocks import Message, SectionBlock\n\n\nclient = WebClient(token=environ["SLACK_API_TOKEN"])\nblock = SectionBlock("Hello, world!")\nmessage = Message(channel="#general", blocks=block)\n\nresponse = client.chat_postMessage(**message)\n```\n\nNote the `**` operator in front of the `message` object.\n\n## Can I use this in my project?\nYes, please do! The code is all open source and dual BSD-3.0 and MIT licensed\n    (use what suits you best).\n',
    'author': 'Nicholas Lambourne',
    'author_email': 'dev@ndl.im',
    'maintainer': 'Nicholas Lambourne',
    'maintainer_email': 'dev@ndl.im',
    'url': 'https://github.com/nicklambourne/slackblocks',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
