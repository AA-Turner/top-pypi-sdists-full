# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['the_retry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'the-retry',
    'version': '0.1.1',
    'description': 'Retry decorator for both synchronous and asynchronous functions.',
    'long_description': '# the-retry\n\nRetry decorator for both synchronous and asynchronous functions.\n\n## Features\n\n- No external dependencies.\n- Supports asyncio. Works with both synchronous and asynchronous functions.\n- Exponential backoff with jitter.\n- Able to call custom function or await custom coroutine on exception occurs.\n\n## Installation\n\n```bash\npip install the-retry\n```\n\n## Decorator parameters\n\nArguments:\n\n- `expected_exception`:\n    exception or tuple of exceptions (default BaseException).\n\nKeyword arguments:\n\n- `attempts`:\n    how much times the function will be retried, value -1 is infinite (default 2).\n- `backoff`:\n    time interval between the `attemps` (default 0).\n- `exponential_backoff`:\n    `current_backoff = backoff * 2 ** retries` (default False).\n- `ignore_exceptions`:\n    only log error but not raise exception if `attempts` exceeds (default False).\n- `jitter`:\n    maximum value of deviation from the `current_backoff` (default 0).\n- `maximum_backoff`:\n    `current_backoff = min(current_backoff, maximum_backoff)` (default 0).\n- `on_exception`:\n    function that called or await on error occurs (default None).\n    Be aware if a decorating function is synchronous `on_exception` function must be\n    synchronous too and accordingly for asynchronous function `on_exception` must be\n    asynchronous.\n\n## Examples\n\n### Immediately retry once without delay on any exception occurs\n\n```python3\nfrom the_retry import retry\n\n@retry()\ndef some_function():\n    print("some function")\n```\n\n### Immediately retry once without delay on ValueError occurs with calling side effect function\n\n```python3\nfrom the_retry import retry\n\ndef side_effect():\n    print("side effect")\n\n@retry(expected_exception=ValueError, on_exception=side_effect)\ndef some_function():\n    print("some function")\n\n```\n\n### Retry async function with 10 attempts with exponential backoff on ValueError or AttributeError occurs with calling side effect coroutine\n\n```python3\nfrom the_retry import retry\n\nasync def async_side_effect():\n    print("async side effect")\n\n@retry(\n    expected_exception=(ValueError, AttributeError)\n    attempts=10,\n    backoff=1,\n    exponential_backoff=True,\n    jitter=1,\n    maximum_backoff=60,\n    on_exception=async_side_effect,\n)\nasync def async_some_function():\n    print("some function")\n```\n',
    'author': 'Ramil Minnigaliev',
    'author_email': 'minnigaliev-r@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/ramil.minnigaliev/the-retry',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
