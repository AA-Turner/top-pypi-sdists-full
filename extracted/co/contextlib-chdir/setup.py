# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextlib-chdir']

package_data = \
{'': ['*'],
 'contextlib-chdir': ['.git/*',
                      '.git/hooks/*',
                      '.git/info/*',
                      '.git/logs/*',
                      '.git/logs/refs/heads/*',
                      '.git/logs/refs/remotes/origin/*',
                      '.git/objects/0d/*',
                      '.git/objects/10/*',
                      '.git/objects/12/*',
                      '.git/objects/5c/*',
                      '.git/objects/62/*',
                      '.git/objects/78/*',
                      '.git/objects/8b/*',
                      '.git/objects/8f/*',
                      '.git/objects/92/*',
                      '.git/objects/be/*',
                      '.git/objects/c5/*',
                      '.git/objects/d2/*',
                      '.git/objects/e2/*',
                      '.git/objects/e6/*',
                      '.git/objects/e8/*',
                      '.git/objects/ff/*',
                      '.git/refs/heads/*',
                      '.git/refs/remotes/origin/*']}

modules = \
['py']
setup_kwargs = {
    'name': 'contextlib-chdir',
    'version': '1.0.2',
    'description': 'Backport of contextlib.chdir stdlib class added in Python3.11.',
    'long_description': "# contextlib-chdir\n\nBackport of [`contextlib.chdir`] stdlib class added in Python3.11.\n\n## Install\n\n```\npip install contextlib-chdir\n```\n\n## Usage\n\n```python\nimport os\nimport tempfile\nfrom contextlib_chdir import chdir as chdir_ctx\n\nwith chdir_ctx(tempfile.gettempdir()):\n    print(os.getcwd())  # /tmp\n```\n\n## Note\n\nYou'll probably want to migrate to [`contextlib2`] when\n[this change is included](https://github.com/jazzband/contextlib2/issues/43).\n\n[`contextlib.chdir`]: https://docs.python.org/3.11/library/contextlib.html#contextlib.chdir\n[`contextlib2`]: https://github.com/jazzband/contextlib2\n",
    'author': 'Álvaro Mondéjar Rubio',
    'author_email': 'mondejar1994@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
