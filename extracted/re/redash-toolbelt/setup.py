# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redash_toolbelt', 'redash_toolbelt.examples']

package_data = \
{'': ['*'], 'redash_toolbelt': ['docs/redash-migrate/*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['clone-dashboard-and-queries = '
                     'redash_toolbelt.examples.clone_dashboard_and_queries:main',
                     'export-queries = '
                     'redash_toolbelt.examples.query_export:main',
                     'find-tables = '
                     'redash_toolbelt.examples.find_table_names:main',
                     'gdpr-scrub = redash_toolbelt.examples.gdpr_scrub:lookup',
                     'redash-migrate = redash_toolbelt.examples.migrate:main']}

setup_kwargs = {
    'name': 'redash-toolbelt',
    'version': '0.1.9',
    'description': 'Redash API client and tools to manage your instance.',
    'long_description': 'redash-toolbelt - The official API client and utilities to manage a Redash instance\n\n\n- [INSTALLATION](#installation)\n- [EXAMPLE SCRIPTS](#example-scripts)\n\n\n## INSTALLATION\n\nTo install it you will need Python 3.6 or above. We recommend that you use a [virtual environment].\n\n\n```bash\npip install --upgrade redash-toolbelt\n```\n\nThis command will update `redash-toolbelt` if you have already installed it.\n\n[virtual environment]: https://pythonbasics.org/virtualenv/\n\n\n## EXAMPLE SCRIPTS\n\nWith `redash-toolbelt` installed you will have access to several example CLI scripts within your terminal.\n\n```text\n\ngdpr-scrub                  Search for a string term in  your Redash queries\n                            and query results. The script returns a list of\n                            URLs in your instance that contain references to\n                            the search term you provide\nfind-tables                 Search the text of queries against a data source\n                            to see which table names are used in queries of\n                            that source. This script relies on regex that is\n                            tested against ANSI SQL.\nclone-dashboard-and-queries Completely duplicate a dashboard by copying all \n                            its queries and visualizations.\nexport-queries              Export all the queries of your Redash instance\n                            as text files.\nredash-migrate              Move data from one instance of Redash to another.\n                            See docs/redash-migrate/README.md for more info\n```\n',
    'author': 'Redash Maintainers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/getredash/redash-toolbelt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
