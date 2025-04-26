# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reactivex',
 'reactivex.abc',
 'reactivex.disposable',
 'reactivex.internal',
 'reactivex.observable',
 'reactivex.observer',
 'reactivex.operators',
 'reactivex.operators.connectable',
 'reactivex.scheduler',
 'reactivex.scheduler.eventloop',
 'reactivex.scheduler.mainloop',
 'reactivex.subject',
 'reactivex.testing']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'reactivex',
    'version': '4.0.4',
    'description': 'ReactiveX (Rx) for Python',
    'long_description': '===============================\nThe ReactiveX for Python (RxPY)\n===============================\n\n.. image:: https://github.com/ReactiveX/RxPY/workflows/Python%20package/badge.svg\n    :target: https://github.com/ReactiveX/RxPY/actions\n    :alt: Build Status\n\n.. image:: https://img.shields.io/coveralls/ReactiveX/RxPY.svg\n    :target: https://coveralls.io/github/ReactiveX/RxPY\n    :alt: Coverage Status\n\n.. image:: https://img.shields.io/pypi/v/reactivex.svg\n    :target: https://pypi.org/project/reactivex/\n    :alt: PyPY Package Version\n\n.. image:: https://img.shields.io/readthedocs/rxpy.svg\n    :target: https://readthedocs.org/projects/rxpy/builds/\n    :alt: Documentation Status\n\n\n*A library for composing asynchronous and event-based programs using observable\ncollections and query operator functions in Python*\n\nReactiveX for Python v4\n-----------------------\n\nFor v3.X please go to the `v3 branch\n<https://github.com/ReactiveX/RxPY/tree/release/v3.2.x>`_.\n\nReactiveX for Python v4.x runs on `Python <http://www.python.org/>`_ 3.7 or above. To\ninstall:\n\n.. code:: console\n\n    pip3 install reactivex\n\n\nAbout ReactiveX\n---------------\n\nReactiveX for Python (RxPY) is a library for composing asynchronous and event-based\nprograms using observable sequences and pipable query operators in Python. Using Rx,\ndevelopers represent asynchronous data streams with Observables, query asynchronous data\nstreams using operators, and parameterize concurrency in data/event streams using\nSchedulers.\n\n.. code:: python\n\n    import reactivex as rx\n    from reactivex import operators as ops\n\n    source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")\n\n    composed = source.pipe(\n        ops.map(lambda s: len(s)),\n        ops.filter(lambda i: i >= 5)\n    )\n    composed.subscribe(lambda value: print("Received {0}".format(value)))\n\n\nLearning ReactiveX\n------------------\n\nRead the `documentation\n<https://rxpy.readthedocs.io/en/latest/>`_ to learn\nthe principles of ReactiveX and get the complete reference of the available\noperators.\n\nIf you need to migrate code from RxPY v1.x or v3.x, read the `migration\n<https://rxpy.readthedocs.io/en/latest/migration.html>`_ section.\n\nThere is also a list of third party documentation available `here\n<https://rxpy.readthedocs.io/en/latest/additional_reading.html>`_.\n\n\nCommunity\n----------\n\nJoin the conversation on GitHub `Discussions\n<https://github.com/ReactiveX/RxPY/discussions>`_! if you have any questions or\nsuggestions.\n\nDifferences from .NET and RxJS\n------------------------------\n\nReactiveX for Python is a fairly complete implementation of\n`Rx <http://reactivex.io/>`_ with more than\n`120 operators <https://rxpy.readthedocs.io/en/latest/operators.html>`_, and\nover `1300 passing unit-tests <https://coveralls.io/github/ReactiveX/RxPY>`_. RxPY\nis mostly a direct port of RxJS, but also borrows a bit from Rx.NET and RxJava in\nterms of threading and blocking operators.\n\nReactiveX for Python follows `PEP 8 <http://legacy.python.org/dev/peps/pep-0008/>`_, so\nall function and method names are ``snake_cased`` i.e lowercase with words separated by\nunderscores as necessary to improve readability.\n\nThus .NET code such as:\n\n.. code:: c#\n\n    var group = source.GroupBy(i => i % 3);\n\n\nneed to be written with an ``_`` in Python:\n\n.. code:: python\n\n    group = source.pipe(ops.group_by(lambda i: i % 3))\n\nWith ReactiveX for Python you should use `named keyword arguments\n<https://docs.python.org/3/glossary.html>`_ instead of positional arguments when an\noperator has multiple optional arguments. RxPY will not try to detect which arguments\nyou are giving to the operator (or not).\n\nDevelopment\n-----------\n\nThis project is managed using `Poetry <https://python-poetry.org/>`_. Code is formatted\nusing `Black <https://github.com/psf/black>`_, `isort\n<https://github.com/PyCQA/isort>`_. Code is statically type checked using `pyright\n<https://github.com/microsoft/pyright>`_ and `mypy <http://mypy-lang.org/>`_.\n\nIf you want to take advantage of the default VSCode integration, then\nfirst configure Poetry to make its virtual environment in the\nrepository:\n\n.. code:: console\n\n    poetry config virtualenvs.in-project true\n\nAfter cloning the repository, activate the tooling:\n\n.. code:: console\n\n    poetry install\n    poetry run pre-commit install\n\nRun unit tests:\n\n.. code:: console\n\n    poetry run pytest\n\nRun code checks (manually):\n\n.. code:: console\n\n    poetry run pre-commit run --all-files\n',
    'author': 'Dag Brattli',
    'author_email': 'dag@brattli.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://reactivex.io',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
