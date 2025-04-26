# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonalias']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonalias',
    'version': '0.1.2',
    'description': 'A microlibrary that defines a Json type alias for Python.',
    'long_description': '# jsonalias\n\nA microlibrary that defines a `Json` type alias for Python.\n\n## This README is longer than the library\n\nSeriously, this is all the code:\n\n```python\nfrom typing import Dict, List, Union\n\nJson = Union[Dict[str, "Json"], List["Json"], str, int, float, bool, None]\n```\n\nIf we only supported Python >= 3.10, it would fit on one line:\n\n```python\nJson = dict[str, \'Json\'] | list[\'Json\'] | str | int | float | bool | None\n```\n\n## Then why make a library out of it?\n\nI want to use this type alias in multiple projects and it\'s\njust about long enough to be annoying.\n\nThis alias should probably get added to the Python `typing` module.\nIf it does and I haven\'t put a big notice on this README,\nplease open a PR.\n\n## Example\n\n```python\nfrom jsonalias import Json\n\nd: Json = {"foo": ["bar", {"x": "y"}]}\n```\n\n## It\'s not working please help???\n\nMake sure you\'re using mypy >= 0.981 and running with the\n`--enable-recursive-aliases` flag.\n\n## Special Thanks\n\nGitHub user wbolster for [this comment](https://github.com/python/typing/issues/182#issuecomment-1259412066)\nnotifying us that mypy could now do JSON.\n',
    'author': 'Kevin Heavey',
    'author_email': 'ID+username@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevinheavey/jsonalias',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
