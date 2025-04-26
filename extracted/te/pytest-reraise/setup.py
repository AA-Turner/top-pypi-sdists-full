# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_reraise']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=4.6']

entry_points = \
{'pytest11': ['reraise = pytest_reraise.reraise']}

setup_kwargs = {
    'name': 'pytest-reraise',
    'version': '2.1.2',
    'description': 'Make multi-threaded pytest test cases fail when they should',
    'long_description': '# pytest-reraise\n\n[![PyPI](https://img.shields.io/pypi/v/pytest-reraise)](https://pypi.python.org/pypi/pytest-reraise/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bjoluc/pytest-reraise/build)](https://github.com/bjoluc/pytest-reraise/actions)\n[![codecov](https://codecov.io/gh/bjoluc/pytest-reraise/branch/main/graph/badge.svg)](https://codecov.io/gh/bjoluc/pytest-reraise)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-reraise)](https://pypi.python.org/pypi/pytest-reraise/)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/pytest-reraise)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)\n[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079)](https://github.com/bjoluc/semantic-release-config-poetry)\n\nLet\'s assume you write a pytest test case that includes assertions in another thread, like so:\n\n```python\nfrom threading import Thread\n\ndef test_assert():\n\n    def run():\n        assert False\n\n    Thread(target=run).start()\n```\n\nThis test will pass, as the `AssertionError` is not raised in the main thread.\n`pytest-reraise` is here to help you capture the exception and raise it in the main thread:\n\n```sh\npip install pytest-reraise\n```\n\n```python\nfrom threading import Thread\n\ndef test_assert(reraise):\n\n    def run():\n        with reraise:\n            assert False\n\n    Thread(target=run).start()\n```\n\nThe above test will fail, as `pytest-reraise` captures the exception and raises it at the end of the test case.\n\n## Advanced Usage and Special Cases\n\n### Wrapping Functions\n\nInstead of using the `reraise` context manager in a function, you can also wrap the entire function with it via the `reraise.wrap()` method.\nHence, the example\n```python\ndef run():\n    with reraise:\n        assert False\n\nThread(target=run).start()\n```\ncan also be written as\n```python\ndef run():\n    assert False\n\nThread(target=reraise.wrap(run)).start()\n```\nor even\n```python\n@reraise.wrap\ndef run():\n    assert False\n\nThread(target=run).start()\n```\n\n### Manual Re-raising\n\nBy default, the captured exception (if any) is raised at the end of the test case.\nIf you want to raise it before then, call `reraise()` in your test case.\nIf an exception has been raised within a `with reraise` block by then, `reraise()` will raise it right away:\n\n```python\ndef test_assert(reraise):\n\n    def run():\n        with reraise:\n            assert False\n\n    reraise() # This will not raise anything yet\n\n    t = Thread(target=run)\n    t.start()\n    t.join()\n\n    reraise() # This will raise the assertion error\n```\n\nAs seen in the example above, `reraise()` can be called multiple times during a test case. Whenever an exception has been raised in a `with reraise` block since the last call, it will be raised on the next call.\n\n### Multiple Exceptions\n\nWhen the `reraise` context manager is used multiple times in a single test case, only the first-raised exception will be re-raised in the end.\nIn the below example, both threads raise an exception but only one of these exceptions will be re-raised.\n\n```python\ndef test_assert(reraise):\n\n    def run():\n        with reraise:\n            assert False\n\n    for _ in range(2):\n        Thread(target=run).start()\n```\n\n### Catching Exceptions\n\nBy default, the `reraise` context manager does not catch exceptions, so they will not be hidden from the thread in which they are raised.\nIf you want to change this, use `reraise(catch=True)` instead of `reraise`:\n\n```python\ndef test_assert(reraise):\n\n    def run():\n        with reraise(catch=True):\n            assert False\n        print("I\'m alive!")\n\n    Thread(target=run).start()\n```\n\nNote that you cannot use `reraise()` (without the `catch` argument) as a context manager, as it is used to raise exceptions.\n\n### Exception Priority\n\nIf `reraise` captures an exception and the main thread raises an exception as well, the exception captured by `reraise` will mask the main thread\'s exception unless that exception was already re-raised.\nThe objective behind this is that the outcome of the main thread often depends on the work performed in other threads.\nThus, failures in in other threads are likely to cause failures in the main thread, and other threads\' exceptions (if any) are of greater importance for the developer than main thread exceptions.\n\nThe example below will report `assert False`, not `assert "foo" == "bar"`.\n\n```python\ndef test_assert(reraise):\n\n    def run():\n        with reraise:\n            assert False # This will be reported\n\n    t = Thread(target=run)\n    t.start()\n    t.join()\n\n    assert "foo" == "bar" # This won\'t\n```\n\n### Accessing and Modifying Exceptions\n\n`reraise` provides an `exception` property to retrieve the exception that was captured, if any.\n`reraise.exception` can also be used to assign an exception if no exception has been captured yet.\nIn addition to that, `reraise.reset()` returns the value of `reraise.exception` and resets it to `None` so that the exception will not be raised anymore.\n\nHere\'s a quick demonstration test case that passes:\n\n```python\ndef test_assert(reraise):\n\n    def run():\n        with reraise:\n            assert False\n\n    t = Thread(target=run)\n    t.start()\n    t.join()\n\n    # Return the captured exception:\n    assert type(reraise.exception) is AssertionError\n\n    # This won\'t do anything, since an exception has already been captured:\n    reraise.exception = Exception()\n\n    # Return the exception and set `reraise.exception` to None:\n    assert type(reraise.reset()) is AssertionError\n\n    # `Reraise` will not fail the test case because\n    assert reraise.exception is None\n```\n',
    'author': 'bjoluc',
    'author_email': 'mail@bjoluc.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bjoluc/pytest-reraise',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
