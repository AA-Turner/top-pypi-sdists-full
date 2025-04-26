# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['HtmlVoidElements']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-void-elements',
    'version': '0.1.0',
    'description': 'List of HTML void tag names.',
    'long_description': "# HtmlTagNames\n\nPython port of npm package [html-void-elements](https://www.npmjs.com/package/html-void-elements).\n\nList of known HTML tag names.\n\n## What is this?\n\nThis is a list of HTML tag names.\nIt includes ancient (for example, `nextid` and `basefont`) and modern (for\nexample, `shadow` and `template`) names from the HTML living standard.\nThe repo includes scripts to regenerate the data from the specs.\n\n## When should I use this?\n\nYou can use this package when you need to know what tag names are allowed in\nany version of HTML.\n\n## Install\n\n```sh\npip install html-tag-names\n```\n\n## Use\n\n```py\nfrom HtmlVoidElements import html_void_elements\n\nprint(html_void_elements)\n```\n\nYields:\n\n```py\n[\n  'area',\n  'base',\n  'basefont',\n  'bgsound',\n  'br',\n  'col',\n  'command',\n  'embed',\n  'frame',\n  'hr',\n  'image',\n  'img',\n  'input',\n  'isindex',\n  'keygen',\n  'link',\n  'menuitem',\n  'meta',\n  'nextid',\n  'param',\n  'source',\n  'track',\n  'wbr'\n]\n```\n## License\n\n[GPL][license] © Riverside Healthcare\nPorted from `html-void-elements` [MIT][license] © [Titus Wormer][author]\n\n[license]: LICENSE",
    'author': 'Christopher Pickering',
    'author_email': 'cpickering@rhc.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Riverside-Healthcare/html-void-elements',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
