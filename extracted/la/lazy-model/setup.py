# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lazy_model', 'lazy_model.parser']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0']

setup_kwargs = {
    'name': 'lazy-model',
    'version': '0.4.0',
    'description': '',
    'long_description': '# Lazy parsing for Pydantic models\n\nThis library provides a lazy interface for parsing objects from dictionaries. During the parsing, it saves the raw data inside the object and parses each field on demand.\n\n## Install\n\npoetry\n```shell\npoetry add lazy-model\n```\n\npip\n```shell\npip install lazy-model\n```\n\n## Usage\n\n```python\nfrom lazy_model import LazyModel\nfrom pydantic import validator\n\n\nclass Sample(LazyModel):\n    i: int\n    s: str\n\n    @validator("s")\n    def s_upper(cls, v):\n        return v.upper()\n\n\nobj = Sample.lazy_parse({"i": "10", "s": "test"})\n\n# at this point the data is stored in a raw format inside the object\n\nprint(obj.__dict__)\n\n# >>> {\'i\': NAO, \'s\': NAO}\n\n# NAO - Not An Object. It shows that the field was not parsed yet.\n\nprint(obj.s)\n\n# >>> TEST\n\n# Custom validator works during lazy parsing\n\nprint(obj.__dict__)\n\n# >>> {\'i\': NAO, \'s\': \'TEST\'}\n\n# The `s` field  was already parsed by this step\n\nprint(obj.i, type(obj.i))\n\n# >>> 10 <class \'int\'>\n\n# It converted `10` from string to int based on the annotations\n\nprint(obj.__dict__)\n\n# >>> {\'i\': 10, \'s\': \'TEST\'}\n\n# Everything was parsed\n```',
    'author': 'Roman Right',
    'author_email': 'roman-right@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
