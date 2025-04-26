# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_iso8601']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jetblack-iso8601',
    'version': '1.0.2',
    'description': 'ISO 8601 support',
    'long_description': "# jetblack-iso8601\n\nSupport for ISO8601\n(read the [docs](https://rob-blackbourn.github.io/jetblack-iso8601/)).\n\n## Usage\n\n### Timestamps\n\nTimestamps can be parsed with `iso8601_to_datetime` and\nconverted to a string with `datetime_to_iso8601`.\n\n```python\nfrom jetblack_iso8601 import (\n    iso8601_to_datetime,\n    datetime_to_iso8601\n)\n\ntext = '2014-02-01T09:28:56.321-10:00'\ntimestamp = iso8601_to_datetime(text)\nroundtrip = datetime_to_iso8601(timestamp)\nassert text == roundtrip\n```\n\n### Durations\n\nTimestamps can be parsed with `iso8601_to_timedelta` and\nconverted to a string with `datetime_to_iso8601`.\n\n\n```python\nfrom jetblack_iso8601 import (\n    iso8601_to_timedelta,\n    timedelta_to_iso8601\n)\n\ntext = 'P3Y2M1DT12H11M10S'\nvalue = iso8601_to_timedelta(text)\nroundtrip = timedelta_to_iso8601(value)\nassert roundtrip == text\n```\n",
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-iso8601',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
