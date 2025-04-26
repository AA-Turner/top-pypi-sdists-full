# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timing_asgi', 'timing_asgi.integrations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'timing-asgi',
    'version': '0.3.1',
    'description': 'ASGI middleware to emit timing metrics with something like statsd',
    'long_description': '# timing-asgi\n[![CircleCI](https://circleci.com/gh/steinnes/timing-asgi.svg?style=svg&circle-token=4e141ed4d7231ab6d00dc7b14624d759cf16e1d2)](https://circleci.com/gh/steinnes/timing-asgi)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/timing-asgi.svg)](https://pypi.org/project/timing-asgi/)\n[![PyPI Version](https://img.shields.io/pypi/v/timing-asgi.svg)](https://pypi.org/project/timing-asgi/)\n[![License](https://img.shields.io/badge/license-mit-blue.svg)](https://pypi.org/project/timing-asgi/)\n\nThis is a timing middleware for [ASGI](https://asgi.readthedocs.org), useful for automatic instrumentation of ASGI endpoints.\n\nThis was developed at [GRID](https://github.com/GRID-is) for use with our backend services which are built using\npython and the ASGI framework [Starlette](https://starlette.io), and intended to emit metrics to [Datadog](https://www.datadoghq.com/),\na statsd-based cloud monitoring service.\n\n# ASGI version\n\nSince 0.2.0 this middleware only supports ASGI3, if you need ASGI2 support please use version [0.1.2](https://github.com/steinnes/timing-asgi/releases/tag/v0.1.2).\n\n# installation\n\n```\npip install timing-asgi\n```\n\n# usage\n\n\nHere\'s an example using the Starlette ASGI framework which prints out the timing metrics..\n\nA more realistic example which emits the timing metrics to Datadog can be found at\n[https://github.com/steinnes/timing-starlette-asgi-example](https://github.com/steinnes/timing-starlette-asgi-example).\n\n\n```python\nimport logging\nimport uvicorn\n\nfrom starlette.applications import Starlette\nfrom starlette.responses import PlainTextResponse\nfrom timing_asgi import TimingMiddleware, TimingClient\nfrom timing_asgi.integrations import StarletteScopeToName\n\n\nclass PrintTimings(TimingClient):\n    def timing(self, metric_name, timing, tags):\n        print(metric_name, timing, tags)\n\n\napp = Starlette()\n\n\n@app.route("/")\ndef homepage(request):\n    return PlainTextResponse("hello world")\n\n\napp.add_middleware(\n    TimingMiddleware,\n    client=PrintTimings(),\n    metric_namer=StarletteScopeToName(prefix="myapp", starlette_app=app)\n)\n\nif __name__ == "__main__":\n    logging.basicConfig(level=logging.INFO)\n    uvicorn.run(app)\n\n```\n\nRunning this example and sending some requests:\n\n```\n$ python app.py\nINFO: Started server process [35895]\nINFO: Waiting for application startup.\n2019-03-07 11:38:01 INFO  [timing_asgi.middleware:44] ASGI scope of type lifespan is not supported yet\nINFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)\nINFO: (\'127.0.0.1\', 58668) - "GET / HTTP/1.1" 200\nmyapp.__main__.homepage 0.0006690025329589844 [\'http_status:200\', \'http_method:GET\', \'time:wall\']\nmyapp.__main__.homepage 0.0006950000000000012 [\'http_status:200\', \'http_method:GET\', \'time:cpu\']\nINFO: (\'127.0.0.1\', 58684) - "GET /asdf HTTP/1.1" 404\nmyapp.asdf 0.0005478858947753906 [\'http_status:404\', \'http_method:GET\', \'time:wall\']\nmyapp.asdf 0.0005909999999999804 [\'http_status:404\', \'http_method:GET\', \'time:cpu\']\n```\n',
    'author': 'Steinn Eldjárn Sigurðarson',
    'author_email': 'steinnes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
