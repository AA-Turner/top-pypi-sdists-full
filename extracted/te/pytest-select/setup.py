# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytest_select']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=3.0']

entry_points = \
{'pytest11': ['pytest-select = pytest_select.plugin']}

setup_kwargs = {
    'name': 'pytest-select',
    'version': '0.1.2',
    'description': 'A pytest plugin which allows to (de-)select tests from a file.',
    'long_description': "pytest-select\n=============\n\n|PyPI pyversions| |PyPI license| |PyPI version| |CircleCI build| |Codecov result|\n\n.. |PyPI version| image:: https://img.shields.io/pypi/v/pytest-select.svg\n   :target: https://pypi.org/project/pytest-select/\n.. |PyPI license| image:: https://img.shields.io/pypi/l/pytest-select.svg\n   :target: https://pypi.python.org/pypi/pytest-select/\n.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pytest-select.svg\n   :target: https://pypi.python.org/pypi/pytest-select/\n.. |CircleCI build| image:: https://img.shields.io/circleci/project/github/ulope/pytest-select/master.svg?logo=circleci\n   :target: https://circleci.com/gh/ulope/pytest-select/\n.. |Codecov result| image:: https://img.shields.io/codecov/c/github/ulope/pytest-select/master.svg?logo=codecov\n   :target: https://codecov.io/gh/ulope/pytest-select\n\n\nThis is a `pytest`_ plugin which allows to (de-)select tests by name from a list loaded from a file.\n\n.. _pytest: https://pytest.org\n\n\nInstallation\n------------\n\nIt's recommended to install this package from PyPI::\n\n    pip install pytest-select\n\n\nUsage\n-----\n\nThis plugin adds new command line options to pytest:\n\n- ``--select-from-file``\n- ``--deselect-from-file``\n- ``--select-fail-on-missing``\n\nThe first two both expect an argument that resolves to a UTF-8 encoded text file containing one test name per\nline.\n\nThe third one changes the behaviour in case (de-)selected test names are missing from the to-be executed tests.\nBy default a warning is emitted and the remaining selected tests are executed as normal.\nBy using the ``--select-fail-on-missing`` flag this behaviour can be changed to instead abort execution in that case.\n\nTest names are expected in the same format as seen in the output of\n``pytest --collect-only --quiet`` for example.\n\nBoth plain test names or complete node ids (e.g. ``test_file.py::test_name``) are accepted.\n\nExample::\n\n    $~ cat selection.txt\n    test_something\n    test_parametrized[1]\n    tests/test_foo.py::test_other\n\n    $~ pytest --select-from-file selection.txt\n    $~ pytest --deselect-from-file selection.txt\n\n\nDevelopment\n-----------\n\nThis package uses Poetry_.\nTo setup a development environment install Poetry and then run::\n\n    poetry install\n\n\n.. _Poetry: https://poetry.eustace.io\n\nQuestions\n---------\n\nWhy not use pytest's builtin ``-k`` option\n******************************************\n\nThe ``-k`` selection mechanism is (currently) unable to deal with selecting multiple parametrized\ntests and is also a bit fragile since it matches more than just the test name.\nAdditionally, depending on the number of tests, giving test names on the command line can overflow\nthe maximum command length.\n\nWhat is this useful for\n***********************\n\nThe author uses this plugin to `split tests across workers`_ on `Circle CI`_.\n\nExample::\n\n    pytest --collect-only --quiet | \\\n        grep '::' | \\\n        circleci tests split --split-by=timings --timings-type=testname > selected.txt\n    pytest --select-from-file selected.txt\n\n.. _Circle CI: https://circleci.com\n.. _split tests across workers: https://circleci.com/docs/2.0/parallelism-faster-jobs/#splitting-test-files\n\n\nVersion History\n---------------\n\n- ``v0.1.2`` - 2019-01-18:\n    - Add informational pytest header report output\n- ``v0.1.1`` - 2018-12-10:\n    - Add ``--select-fail-on-missing`` option\n    - Add basic mutation testing\n- ``v0.1.0post0`` - 2018-12-08:\n    - Fix README\n- ``v0.1.0`` - 2018-12-08:\n    - Initial release\n",
    'author': 'Ulrich Petri',
    'author_email': 'ulo@ulo.pe',
    'url': 'https://github.com/ulope/pytest-select',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
