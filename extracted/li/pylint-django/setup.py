# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_django',
 'pylint_django.augmentations',
 'pylint_django.checkers',
 'pylint_django.transforms',
 'pylint_django.transforms.transforms']

package_data = \
{'': ['*']}

install_requires = \
['pylint-plugin-utils>=0.8', 'pylint>=3.0,<4']

extras_require = \
{'with_django': ['Django>=2.2']}

setup_kwargs = {
    'name': 'pylint-django',
    'version': '2.6.1',
    'description': 'A Pylint plugin to help Pylint understand the Django web framework',
    'long_description': 'pylint-django\n=============\n\n.. image:: https://github.com/pylint-dev/pylint-django/actions/workflows/build.yml/badge.svg\n    :target: https://github.com/pylint-dev/pylint-django/actions/workflows/build.yml\n\n.. image:: https://coveralls.io/repos/github/pylint-dev/pylint-django/badge.svg?branch=master\n     :target: https://coveralls.io/github/pylint-dev/pylint-django?branch=master\n\n.. image:: https://img.shields.io/pypi/v/pylint-django.svg\n    :target: https://pypi.python.org/pypi/pylint-django\n\n\nAbout\n-----\n\n``pylint-django`` is a `Pylint <http://pylint.org>`__ plugin for improving code\nanalysis when analysing code using Django. It is also used by the\n`Prospector <https://github.com/landscapeio/prospector>`__ tool.\n\n\nInstallation\n------------\n\nTo install::\n\n    pip install pylint-django\n\n\n**WARNING:** ``pylint-django`` will not install ``Django`` by default because\nthis causes more trouble than good,\n`see discussion <https://github.com/pylint-dev/pylint-django/pull/132>`__. If you wish\nto automatically install the latest version of ``Django`` then::\n\n    pip install pylint-django[with-django]\n\notherwise sort out your testing environment and please **DO NOT** report issues\nabout missing Django!\n\n\nUsage\n-----\n\n\nEnsure ``pylint-django`` is installed and on your path. In order to access some\nof the internal Django features to improve pylint inspections, you should also\nprovide a Django settings module appropriate to your project. This can be done\neither with an environment variable::\n\n    DJANGO_SETTINGS_MODULE=your.app.settings pylint --load-plugins pylint_django [..other options..] <path_to_your_sources>\n\nAlternatively, this can be passed in as a commandline flag::\n\n    pylint --load-plugins pylint_django --django-settings-module=your.app.settings [..other options..] <path_to_your_sources>\n\nIf you do not configure Django, default settings will be used but this will not include, for\nexample, which applications to include in `INSTALLED_APPS` and so the linting and type inference\nwill be less accurate. It is recommended to specify a settings module.\n\nProspector\n----------\n\nIf you have ``prospector`` installed, then ``pylint-django`` will already be\ninstalled as a dependency, and will be activated automatically if Django is\ndetected::\n\n    prospector [..other options..]\n\n\nFeatures\n--------\n\n* Prevents warnings about Django-generated attributes such as\n  ``Model.objects`` or ``Views.request``.\n* Prevents warnings when using ``ForeignKey`` attributes ("Instance of\n  ForeignKey has no <x> member").\n* Fixes pylint\'s knowledge of the types of Model and Form field attributes\n* Validates ``Model.__unicode__`` methods.\n* ``Meta`` informational classes on forms and models do not generate errors.\n* Flags dangerous use of the exclude attribute in ModelForm.Meta.\n* Uses Django\'s internal machinery to try and resolve models referenced as\n  strings in ForeignKey fields. That relies on ``django.setup()`` which needs\n  the appropriate project settings defined!\n\n\nAdditional plugins\n------------------\n\n``pylint_django.checkers.migrations`` looks for migrations which:\n\n- add new model fields and these fields have a default value. According to\n  `Django docs <https://docs.djangoproject.com/en/2.0/topics/migrations/#postgresql>`_\n  this may have performance penalties especially on large tables. The preferred way\n  is to add a new DB column with ``null=True`` because it will be created instantly\n  and then possibly populate the table with the desired default values.\n  Only the last migration from a sub-directory will be examined;\n- are ``migrations.RunPython()`` without a reverse callable - these will result in\n  non reversible data migrations;\n\n\nThis plugin is disabled by default! To enable it::\n\n    pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations\n\n\nContributing\n------------\n\nPlease feel free to add your name to the ``CONTRIBUTORS.rst`` file if you want to\nbe credited when pull requests get merged. You can also add to the\n``CHANGELOG.rst`` file if you wish, although we\'ll also do that when merging.\n\n\nTests\n-----\n\nThe structure of the test package follows that from pylint itself.\n\nIt is fairly simple: create a module starting with ``func_`` followed by\na test name, and insert into it some code. The tests will run pylint\nagainst these modules. If the idea is that no messages now occur, then\nthat is fine, just check to see if it works by running ``scripts/test.sh``.\n\nAny command line argument passed to ``scripts/test.sh`` will be passed to the internal invocation of ``pytest``.\nFor example if you want to debug the tests you can execute ``scripts/test.sh --capture=no``.\nA specific test case can be run by filtering based on the file name of the test case ``./scripts/test.sh -k \'func_noerror_views\'``.\n\nIdeally, add some pylint error suppression messages to the file to prevent\nspurious warnings, since these are all tiny little modules not designed to\ndo anything so there\'s no need to be perfect.\n\nIt is possible to make tests with expected error output, for example, if\nadding a new message or simply accepting that pylint is supposed to warn.\nA ``test_file_name.txt`` file contains a list of expected error messages in the\nformat\n``error-type:line number:class name or empty:1st line of detailed error text:confidence or empty``.\n\n\nLicense\n-------\n\n``pylint-django`` is available under the GPLv2 license.\n',
    'author': 'Carl Crowder',
    'author_email': 'git@carlcrowder.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pylint-dev/pylint-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
