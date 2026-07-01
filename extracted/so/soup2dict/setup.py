# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soup2dict']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'classes>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'soup2dict',
    'version': '2.1.0',
    'description': 'Turns your beautifulsoup4 soup into python dictionary or json',
    'long_description': '# soup2dict\n\nBeautifulSoup4 to python dictionary converter\n___\n![test](https://github.com/thomasborgen/soup2dict/workflows/test/badge.svg)\n[![codecov](https://codecov.io/gh/thomasborgen/soup2dict/branch/master/graph/badge.svg)](https://codecov.io/gh/thomasborgen/soup2dict)\n[![Python Version](https://img.shields.io/pypi/pyversions/soup2dict.svg)](https://pypi.org/project/soup2dict/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n___\n\n\n## Why\n\nIts nice to have a convenient way to change your soup into dict.\n\n## Installation\n\nGet package with pip or poetry\n\n```sh\npip install soup2dict\n```\n\n```sh\npoetry add soup2dict\n```\n\n## Example\n\n```python\nimport simplejson\nfrom bs4 import BeautifulSoup\n\nfrom soup2dict import convert\n\nhtml_doc = """\n<html>\nhei\n<head>\n    <title>The Dormouse\'s story</title>\n    <title>bob</title>\n</head>\n<body>\n    <p class="title">The <b>Dormouse\'s story</b></p>\n    <p class="story">Once upon a time there were three little sisters;\n    and their names were\n    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,\n    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and\n    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;\n    and they lived at the bottom of a well.</p>\n\n    <p class="story">...</p>\n"""\n\n\n# Create soup from html_doc data\nsoup = BeautifulSoup(html_doc, \'html.parser\')\n\n# Convert it to a dictionary with convert()\ndict_result = convert(soup)\n\nwith open(\'output.json\', \'w\') as output_file:\n    output_file.write(\n        simplejson.dumps(dict_result, indent=2),\n    )\n\n```\n\n## Output\n\n```json\n{\n  "html": [\n    {\n      "#text": "hei The Dormouse\'s story bob The Dormouse\'s story Once upon a time there were three little sisters; and their names were Elsie , Lacie and Tillie ; and they lived at the bottom of a well. ...",\n      "navigablestring": [\n        "hei"\n      ],\n      "head": [\n        {\n          "#text": "The Dormouse\'s story bob",\n          "title": [\n            {\n              "#text": "The Dormouse\'s story",\n              "navigablestring": [\n                "The Dormouse\'s story"\n              ]\n            },\n            {\n              "#text": "bob",\n              "navigablestring": [\n                "bob"\n              ]\n            }\n          ]\n        }\n      ],\n      "body": [\n        {\n          "#text": "The Dormouse\'s story Once upon a time there were three little sisters; and their names were Elsie , Lacie and Tillie ; and they lived at the bottom of a well. ...",\n          "p": [\n            {\n              "@class": [\n                "title"\n              ],\n              "#text": "The Dormouse\'s story",\n              "navigablestring": [\n                "The"\n              ],\n              "b": [\n                {\n                  "#text": "Dormouse\'s story",\n                  "navigablestring": [\n                    "Dormouse\'s story"\n                  ]\n                }\n              ]\n            },\n            {\n              "@class": [\n                "story"\n              ],\n              "#text": "Once upon a time there were three little sisters; and their names were Elsie , Lacie and Tillie ; and they lived at the bottom of a well.",\n              "navigablestring": [\n                "Once upon a time there were three little sisters;\\n    and their names were",\n                ",",\n                "and",\n                ";\\n    and they lived at the bottom of a well."\n              ],\n              "a": [\n                {\n                  "@href": "http://example.com/elsie",\n                  "@class": [\n                    "sister"\n                  ],\n                  "@id": "link1",\n                  "#text": "Elsie",\n                  "navigablestring": [\n                    "Elsie"\n                  ]\n                },\n                {\n                  "@href": "http://example.com/lacie",\n                  "@class": [\n                    "sister"\n                  ],\n                  "@id": "link2",\n                  "#text": "Lacie",\n                  "navigablestring": [\n                    "Lacie"\n                  ]\n                },\n                {\n                  "@href": "http://example.com/tillie",\n                  "@class": [\n                    "sister"\n                  ],\n                  "@id": "link3",\n                  "#text": "Tillie",\n                  "navigablestring": [\n                    "Tillie"\n                  ]\n                }\n              ]\n            },\n            {\n              "@class": [\n                "story"\n              ],\n              "#text": "...",\n              "navigablestring": [\n                "..."\n              ]\n            }\n          ]\n        }\n      ]\n    }\n  ]\n}\n```\n',
    'author': 'Thomas Borgen',
    'author_email': 'thomas@borgenit.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thomasborgen/soup2dict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
