# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trio_cdp', 'trio_cdp.generated']

package_data = \
{'': ['*']}

install_requires = \
['chrome-devtools-protocol>=0.3.0,<0.4.0',
 'trio>=0.13.0,<0.14.0',
 'trio_websocket>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'trio-chrome-devtools-protocol',
    'version': '0.6.0',
    'description': 'Trio driver for Chrome DevTools Protocol (CDP)',
    'long_description': "# Trio CDP\n\n[![PyPI](https://img.shields.io/pypi/v/trio-chrome-devtools-protocol.svg)](https://pypi.org/project/trio-chrome-devtools-protocol/)\n![Python Versions](https://img.shields.io/pypi/pyversions/trio-chrome-devtools-protocol)\n![MIT License](https://img.shields.io/github/license/HyperionGray/trio-chrome-devtools-protocol.svg)\n[![Build Status](https://img.shields.io/travis/com/HyperionGray/trio-chrome-devtools-protocol.svg?branch=master)](https://travis-ci.com/HyperionGray/trio-chrome-devtools-protocol)\n[![Read the Docs](https://img.shields.io/readthedocs/trio-cdp.svg)](https://trio-cdp.readthedocs.io)\n\nThis Python library performs remote control of any web browser that implements\nthe Chrome DevTools Protocol. It is built using the type wrappers in\n[python-chrome-devtools-protocol](https://py-cdp.readthedocs.io) and implements\nI/O using [Trio](https://trio.readthedocs.io/). This library handles the\nWebSocket negotiation and session management, allowing you to transparently\nmultiplex commands, responses, and events over a single connection.\n\nThe example below demonstrates the salient features of the library by navigating to a\nweb page and extracting the document title.\n\n```python\nfrom trio_cdp import open_cdp, page, dom\n\nasync with open_cdp(cdp_url) as conn:\n    # Find the first available target (usually a browser tab).\n    targets = await target.get_targets()\n    target_id = targets[0].id\n\n    # Create a new session with the chosen target.\n    async with conn.open_session(target_id) as session:\n\n        # Navigate to a website.\n        async with session.page_enable()\n        async with session.wait_for(page.LoadEventFired):\n            await session.execute(page.navigate(target_url))\n\n        # Extract the page title.\n        root_node = await session.execute(dom.get_document())\n        title_node_id = await session.execute(dom.query_selector(root_node.node_id,\n            'title'))\n        html = await session.execute(dom.get_outer_html(title_node_id))\n        print(html)\n```\n\nThis example code is explained [in the documentation](https://trio-cdp.readthedocs.io)\nand more example code can be found in the `examples/` directory of this repository.\n",
    'author': 'Mark E. Haase',
    'author_email': 'mehaase@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hyperiongray/python-chrome-devtools-protocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
