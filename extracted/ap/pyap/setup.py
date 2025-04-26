# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyap', 'pyap.packages', 'pyap.source_CA', 'pyap.source_GB', 'pyap.source_US']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyap',
    'version': '0.3.1',
    'description': 'Pyap is an MIT Licensed text processing library, written in Python, for detecting and parsing addresses. Currently it supports USA, Canadian and British addresses.',
    'long_description': 'Pyap: Python address parser\n===========================\n\n\nPyap is an MIT Licensed text processing library, written in Python, for\ndetecting and parsing addresses. Currently it supports US \xf0\x9f\x87\xba\xf0\x9f\x87\xb8, Canadian \xf0\x9f\x87\xa8\xf0\x9f\x87\xa6 and British \xf0\x9f\x87\xac\xf0\x9f\x87\xa7 addresses. \n\n\n.. code-block:: python\n\n    >>> import pyap\n    >>> test_address = """\n        Lorem ipsum\n        225 E. John Carpenter Freeway, \n        Suite 1500 Irving, Texas 75062\n        Dorem sit amet\n        """\n    >>> addresses = pyap.parse(test_address, country=\'US\')\n    >>> for address in addresses:\n            # shows found address\n            print(address)\n            # shows address parts\n            print(address.as_dict())\n    ...\n\n\n\n\nInstallation\n------------\n\nTo install Pyap, simply:\n\n.. code-block:: bash\n\n    $ pip install pyap\n\n\n\nAbout\n-----\nThis library has been created because i couldn\'t find any reliable and\nopensource solution for detecting addresses on web pages when writing my\nweb crawler. Currently available solutions have drawbacks when it comes\nto using them to process really large amounts of data fast. You\'ll\neither have to buy some proprietary software; use third-party\npay-per-use services or use address detecting which is slow and\nunsuitable for real-time processing.\n\nPyap is an alternative to all these methods. It is really fast because\nit is based on using regular expressions and it allows to find addresses\nin text in real time with low error rates.\n\n\nFuture work\n-----------\n- Add rules for parsing FR addresses\n- ...\n\n\nTypical workflow\n----------------\nPyap should be used as a first thing when you need to detect an address\ninside a text when you don\'t know for sure whether the text contains\naddresses or not.\n\nTo achieve the most accuracy Pyap results could be reverified using\ngeocoding process.\n\n\nLimitations\n-----------\nBecause Pyap is based on regular expressions it provides fast results.\nThis is also a limitation because regexps intentionally do not use too\nmuch context to detect an address.\n\nIn other words in order to detect US address, the library doesn\'t\nuse any list of US cities or a list of typical street names. It\nlooks for a pattern which is most likely to be an address.\n\nFor example the string below would be detected as a valid address: \n"1 SPIRITUAL HEALER DR SHARIF NSAMBU SPECIALISING IN"\n\nIt happens because this string has all the components of a valid\naddress: street number "1", street name "SPIRITUAL HEALER" followed\nby a street identifier "DR" (Drive), city "SHARIF NSAMBU SPECIALISING"\nand a state name abbreviation "IN" (Indiana).\n\nThe good news is that the above mentioned errors are **quite rare**.\n\n\n',
    'author': 'Vladimir Goncharov',
    'author_email': 'vladimarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
