# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mf2py']

package_data = \
{'': ['*'], 'mf2py': ['backcompat-rules/*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'html5lib>=1.1,<2.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'mf2py',
    'version': '2.0.1',
    'description': 'Microformats parser',
    'long_description': '![mf2py banner](https://microformats.github.io/mf2py/banner.png)\n\n[![version](https://badge.fury.io/py/mf2py.svg?)](https://badge.fury.io/py/mf2py)\n[![downloads](https://img.shields.io/pypi/dm/mf2py)](https://pypistats.org/packages/mf2py)\n[![license](https://img.shields.io/pypi/l/mf2py?)](https://github.com/microformats/mf2py/blob/main/LICENSE)\n[![python-version](https://img.shields.io/pypi/pyversions/mf2py)](https://badge.fury.io/py/mf2py)\n\n## Welcome 👋\n\n`mf2py` is a Python [microformats](https://microformats.org/wiki/microformats) parser with full support for `microformats2`, backwards-compatible support for `microformats1` and experimental support for `metaformats`.\n\n## Installation 💻\n\nTo install `mf2py` run the following command:\n\n```bash\n$ pip install mf2py\n\n```\n\n## Quickstart 🚀\n\nImport the library:\n\n```pycon\n>>> import mf2py\n\n```\n\n### Parse an HTML Document from a file or string\n\n```pycon\n>>> with open("test/examples/eras.html") as fp:\n...     mf2json = mf2py.parse(doc=fp)\n>>> mf2json\n{\'items\': [{\'type\': [\'h-entry\'],\n            \'properties\': {\'name\': [\'Excited for the Taylor Swift Eras Tour\'],\n                           \'author\': [{\'type\': [\'h-card\'],\n                                       \'properties\': {\'name\': [\'James\'],\n                                                      \'url\': [\'https://example.com/\']},\n                                       \'value\': \'James\',\n                                       \'lang\': \'en-us\'}],\n                           \'published\': [\'2023-11-30T19:08:09\'],\n                           \'featured\': [{\'value\': \'https://example.com/eras.jpg\',\n                                         \'alt\': \'Eras tour poster\'}],\n                           \'content\': [{\'value\': "I can\'t decide which era is my favorite.",\n                                        \'lang\': \'en-us\',\n                                        \'html\': "<p>I can\'t decide which era is my favorite.</p>"}],\n                           \'category\': [\'music\', \'Taylor Swift\']},\n            \'lang\': \'en-us\'}],\n \'rels\': {\'webmention\': [\'https://example.com/mentions\']},\n \'rel-urls\': {\'https://example.com/mentions\': {\'text\': \'\',\n                                               \'rels\': [\'webmention\']}},\n \'debug\': {\'description\': \'mf2py - microformats2 parser for python\',\n           \'source\': \'https://github.com/microformats/mf2py\',\n           \'version\': \'2.0.0\',\n           \'markup parser\': \'html5lib\'}}\n\n```\n\n```pycon\n>>> mf2json = mf2py.parse(doc="<a class=h-card href=https://example.com>James</a>")\n>>> mf2json["items"]\n[{\'type\': [\'h-card\'],\n  \'properties\': {\'name\': [\'James\'],\n                 \'url\': [\'https://example.com\']}}]\n\n```\n\n### Parse an HTML Document from a URL\n\n```pycon\n>>> mf2json = mf2py.parse(url="https://events.indieweb.org")\n>>> mf2json["items"][0]["type"]\n[\'h-feed\']\n>>> mf2json["items"][0]["children"][0]["type"]\n[\'h-event\']\n\n```\n\n## Experimental Options\n\nThe following options can be invoked via keyword arguments to `parse()` and `Parser()`.\n\n### `expose_dom`\n\nUse `expose_dom=True` to expose the DOM of embedded properties.\n\n### `metaformats`\n\nUse `metaformats=True` to include any [metaformats](https://microformats.org/wiki/metaformats)\nfound.\n\n### `filter_roots`\n\nUse `filter_roots=True` to filter known conflicting user names (e.g. Tailwind).\nOtherwise provide a custom list to filter instead.\n\n## Advanced Usage\n\n`parse` is a convenience function for `Parser`. More sophisticated behaviors are\navailable by invoking the parser object directly.\n\n```pycon\n>>> with open("test/examples/festivus.html") as fp:\n...     mf2parser = mf2py.Parser(doc=fp)\n\n```\n\n#### Filter by Microformat Type\n\n```pycon\n>>> mf2json = mf2parser.to_dict()\n>>> len(mf2json["items"])\n7\n>>> len(mf2parser.to_dict(filter_by_type="h-card"))\n3\n>>> len(mf2parser.to_dict(filter_by_type="h-entry"))\n4\n\n```\n\n#### JSON Output\n\n```pycon\n>>> json = mf2parser.to_json()\n>>> json_cards = mf2parser.to_json(filter_by_type="h-card")\n\n```\n\n## Breaking Changes in `mf2py` 2.0\n\n- Image `alt` support is now on by default.\n\n## Notes 📝\n\n- If you pass a BeautifulSoup document it may be modified.\n- A hosted version of `mf2py` is available at [python.microformats.io](https://python.microformats.io).\n\n## Contributing 🛠️\n\nWe welcome contributions and bug reports via GitHub.\n\nThis project follows the [IndieWeb code of conduct](https://indieweb.org/code-of-conduct). Please be respectful of other contributors and forge a spirit of positive co-operation without discrimination or disrespect.\n\n## License 🧑\u200d⚖️\n\n`mf2py` is licensed under an MIT License.\n',
    'author': 'Tom Morris',
    'author_email': 'tom@tommorris.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
