# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lazysequence']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lazysequence',
    'version': '0.3.0',
    'description': 'lazysequence',
    'long_description': 'lazysequence\n============\n\n|PyPI| |Status| |Python Version| |License| |Read the Docs| |Tests| |Codecov|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/lazysequence.svg\n   :target: https://pypi.org/project/lazysequence/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/lazysequence.svg\n   :target: https://pypi.org/project/lazysequence/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/lazysequence\n   :target: https://pypi.org/project/lazysequence\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/lazysequence\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/lazysequence/latest.svg?label=Read%20the%20Docs\n   :target: https://lazysequence.readthedocs.io/\n   :alt: Read the documentation at https://lazysequence.readthedocs.io/\n.. |Tests| image:: https://github.com/cjolowicz/lazysequence/workflows/Tests/badge.svg\n   :target: https://github.com/cjolowicz/lazysequence/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/cjolowicz/lazysequence/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/cjolowicz/lazysequence\n   :alt: Codecov\n\n\nA lazy sequence makes an iterator look like an immutable sequence:\n\n.. code:: python\n\n   from lazysequence import lazysequence\n\n   def load_records():\n       return range(10)  # let\'s pretend this is expensive\n\n   records = lazysequence(load_records())\n   if not records:\n       raise SystemExit("no records found")\n\n   first, second = records[:2]\n\n   print("The first record is", first)\n   print("The second record is", second)\n\n   for record in records.release():  # do not cache all records in memory\n       print("record", record)\n\n\nWhy?\n----\n\nSometimes you need to peek ahead at items returned by an iterator. But what if later code needs to see all the items from the iterator? Then you have some options:\n\n1. Pass any consumed items separately. This can get messy, though.\n2. Copy the iterator into a sequence beforehand, if that does not take a lot of space or time.\n3. Duplicate the iterator using `itertools.tee`_, or write your own custom itertool that buffers consumed items internally. There are some good examples of this approach on SO, by `Alex Martelli`_, `Raymond Hettinger`_, and `Ned Batchelder`_.\n\n.. _itertools.tee: https://docs.python.org/3/library/itertools.html#itertools.tee\n.. _Alex Martelli: https://stackoverflow.com/a/1518097/1355754\n.. _Raymond Hettinger: https://stackoverflow.com/a/15726344/1355754\n.. _Ned Batchelder: https://stackoverflow.com/a/1517965/1355754\n\nA lazy sequence combines advantages from option 2 and option 3. It is an immutable sequence that wraps the iterable and caches consumed items in an internal buffer. By implementing `collections.abc.Sequence`_, lazy sequences provide the full set of sequence operations on the iterable. Unlike a copy (option 2), but like a duplicate (option 3), items are only consumed and stored in memory as far as required for any given operation.\n\n.. _collections.abc.Sequence: https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence\n\nThere are some caveats:\n\n- The lazy sequence will eventually store all items in memory. If this is a problem, use ``s.release()`` to obtain an iterator over the sequence items without further caching. After calling this function, the sequence should no longer be used.\n- Explicit is better than implicit. Clients may be better off being passed an iterator and dealing with its limitations. For example, clients may not expect ``len(s)`` to incur the cost of consuming the iterator to its end.\n\n\nInstallation\n------------\n\nYou can install *lazysequence* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install lazysequence\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*lazysequence* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/cjolowicz/lazysequence/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://lazysequence.readthedocs.io/en/latest/usage.html\n',
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/lazysequence',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
