# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ratemate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ratemate',
    'version': '0.1.0',
    'description': 'A python rate limiter module with multi-process support and a simple, intuitive API',
    'long_description': '# ratemate\n\nThere\'s a bunch of python rate limiting modules out there, but they all seem to suffer from similar problems:\n\n- Weird APIs, usually inflexible decorators that you need to wrap your calls in\n- Lack of `multiprocessing` support (eg, two processes will be unaware of each other, and thus double the intended rate)\n- Unnecessary coupling to other libraries\n\n`ratemate`, meanwhile, gives you a simple `RateLimit` object that avoids all these problems.\n\nIt works like this. Declare a `RateLimit` as follows:\n\n    from ratemate import RateLimit\n\n    rate_limit = RateLimit(max_count=2, per=5)  # 2 requests per 5 seconds\n\nThen call `.wait()` appropriately when you need to limit the rate.\n\nFor instance, here\'s an example when creating multiple threads with `concurrent.futures`. First the original rate-unlimited code:\n\n```python\n\nfrom concurrent.futures import ThreadPoolExecutor, as_completed\n\n\ndef task(n):\n    print(f"  task {n} called")\n    return n\n\nfutures = []\n\nwith ThreadPoolExecutor() as executor:\n    for i in range(20):\n        future = executor.submit(task, i)\n        futures.append(future)\n\n    for completed in as_completed(futures):\n        result = completed.result()\n        print(\'completed\')\n```\n\nAdd rate-limiting simply by adding a wait at the appropriate time, either at task creation:\n\n```python\nfor i in range(20):\n    rate_limit.wait()  # wait before creating the task\n    future = executor.submit(task, i)\n    futures.append(future)\n```\n\nOr at the start of the task itself:\n\n```python\ndef task(n):\n    waited_time = rate_limit.wait()  # wait at start of task\n    print(f"  task {n}: waited for {waited_time} secs")\n    return n\n```\n\nBecause `ratemate` uses multi-process-aware shared memory to track its state, you can also use `ProcessPoolExecutor` and everything will still work nicely.\n\n\n## Greedy mode\n\nThe default (aka non-greedy aka patient) rate limiting mode spaces out calls evenly. First instance, max_count=10 and per=60 will result in one call every 6 seconds.\n\nYou may instead wish for calls to happen as fast as possible, only slowing down if the limit would be exceeded. Enable this with greedy=True, eg:\n\n```\nrate_limit = RateLimit(max_count=20, per=60, greedy=True)\n```\n\n## Further enhancements\n\nRate limit coordination between truly independent processes (not just subprocesses), possibly using Python 3.8\'s new shared memory or Redis or PostgreSQL or whatever.\n\n',
    'author': 'Robert Lechte',
    'author_email': 'robert.lechte@dpc.vic.gov.au',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
