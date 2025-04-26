# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['HtmlTagNames']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'html-tag-names',
    'version': '0.1.2',
    'description': 'List of known HTML tag names',
    'long_description': "# HtmlTagNames\n\nPython port of npm package [html-tag-names](https://www.npmjs.com/package/html-tag-names).\n\nList of known HTML tag names.\n\n## What is this?\n\nThis is a list of HTML tag names.\nIt includes ancient (for example, `nextid` and `basefont`) and modern (for\nexample, `shadow` and `template`) names from the HTML living standard.\nThe repo includes scripts to regenerate the data from the specs.\n\n## When should I use this?\n\nYou can use this package when you need to know what tag names are allowed in\nany version of HTML.\n\n## Install\n\n```sh\npip install html-tag-names\n```\n\n## Use\n\n```py\nfrom HtmlTagNames import html_tag_names\n\nprint(len(html_tag_names)) # => 148\n\nprint(html_tag_names[:20])\n```\n\nYields:\n\n```py\n[\n  'a',\n  'abbr',\n  'acronym',\n  'address',\n  'applet',\n  'area',\n  'article',\n  'aside',\n  'audio',\n  'b',\n  'base',\n  'basefont',\n  'bdi',\n  'bdo',\n  'bgsound',\n  'big',\n  'blink',\n  'blockquote',\n  'body',\n  'br'\n]\n```\n## License\n\n[MIT][license] © Riverside Healthcare\nPorted from `html-tag-names` [MIT][license] © [Titus Wormer][author]\n\n[license]: LICENSE",
    'author': 'Christopher Pickering',
    'author_email': 'cpickering@rhc.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Riverside-Healthcare/html-tag-names',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
