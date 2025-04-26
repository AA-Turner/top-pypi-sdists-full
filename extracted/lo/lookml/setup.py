# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lookml',
 'lookml.cli',
 'lookml.cli.autotune',
 'lookml.cli.directory',
 'lookml.cli.doctree',
 'lookml.lib',
 'lookml.lib.language_data',
 'lookml.lkml',
 'lookml.tests',
 'lookml.tests.files.the_look..github.workflows.demo-dashboard-validation',
 'lookml.tests.scenarios']

package_data = \
{'': ['*'],
 'lookml.tests': ['files/basic_parsing/*',
                  'files/kitchenSink/*',
                  'files/order_items.view.lkml',
                  'files/order_items.view.lkml',
                  'files/order_items.view.lkml',
                  'files/pylookml_test_project/*',
                  'files/pylookml_test_project/dashboards/*',
                  'files/pylookml_test_project/models/*',
                  'files/pylookml_test_project/scratch/subfolder/*',
                  'files/pylookml_test_project/views/*',
                  'files/test.dashboard.lookml',
                  'files/test.dashboard.lookml',
                  'files/test.dashboard.lookml',
                  'files/test_ndt.view.lkml',
                  'files/test_ndt.view.lkml',
                  'files/test_ndt.view.lkml',
                  'files/the_look/.github/*',
                  'files/the_look/.github/workflows/*',
                  'files/the_look/cool/*',
                  'files/the_look/dashboards/*',
                  'files/the_look/models/*',
                  'files/the_look/test.view.lkml',
                  'files/the_look/views/*',
                  'files/thelook/*']}

install_requires = \
['PyGithub>=1.47,<2.0',
 'PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'looker-sdk>=0.1.3-beta.20,<0.2.0']

entry_points = \
{'console_scripts': ['lookml = lookml.__main__:cli']}

setup_kwargs = {
    'name': 'lookml',
    'version': '3.0.3',
    'description': 'A batteries included API for automating your LookML',
    'long_description': None,
    'author': 'Russell Garner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
