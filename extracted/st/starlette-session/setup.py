# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_session']

package_data = \
{'': ['*']}

install_requires = \
['itsdangerous>=1.1.0', 'starlette<1']

extras_require = \
{'aioredis': ['aioredis>=1.3.1'],
 'pymemcache': ['pymemcache>=3.3.0'],
 'redis': ['redis>=3.5.3']}

setup_kwargs = {
    'name': 'starlette-session',
    'version': '0.4.3',
    'description': 'A library for backend side session with starlette',
    'long_description': '<p align="center">\n\n<a href="https://github.com/auredentan/starlette-session/actions?query=workflow%3ATest" target="_blank">\n  <img src="https://github.com/auredentan/starlette-session/workflows/Test/badge.svg?branch=master" alt="Test"/>\n</a>\n\n<a href="https://pypi.org/project/starlette-session" target="_blank">\n  <img src="https://img.shields.io/pypi/v/starlette-session?color=%2334D058&label=pypi%20package" alt="Package version"/>\n</a>\n\n<a href="https://codecov.io/gh/auredentan/starlette-session" target="_blank">\n  <img src="https://codecov.io/gh/auredentan/starlette-session/branch/master/graph/badge.svg" alt="Code coverage"/>\n</a>\n\n</p>\n\n---\n\n**Documentation:** [https://auredentan.github.io/starlette-session/](https://auredentan.github.io/starlette-session/)\n\n---\n\n# Starlette Session\n\nStarlette session is a simple session middleware for [starlette](https://github.com/encode/starlette/) that enable server side session with starlette.\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```bash\npip install starlette-session\n```\n\n## Example\n\nUsing redis as backend\n\n```python\nfrom starlette.applications import Starlette\nfrom starlette.requests import Request\nfrom starlette.responses import JSONResponse\nfrom starlette.routing import Route\n\nfrom starlette_session import SessionMiddleware\nfrom starlette_session.backends import BackendType\n\nfrom redis import Redis\n\nasync def setup_session(request: Request) -> JSONResponse:\n    request.session.update({"data": "session_data"})\n    return JSONResponse({"session": request.session})\n\n\nasync def clear_session(request: Request):\n    request.session.clear()\n    return JSONResponse({"session": request.session})\n\n\ndef view_session(request: Request) -> JSONResponse:\n    return JSONResponse({"session": request.session})\n\n\nroutes = [\n    Route("/setup_session", endpoint=setup_session),\n    Route("/clear_session", endpoint=clear_session),\n    Route("/view_session", endpoint=view_session),\n]\n\nredis_client = Redis(host="localhost", port=6379)\napp = Starlette(debug=True, routes=routes)\napp.add_middleware(\n    SessionMiddleware,\n    secret_key="secret",\n    cookie_name="cookie22",\n    backend_type=BackendType.redis,\n    backend_client=redis_client,\n)\n\n```\n\nYou can find more example [here](https://github.com/auredentan/starlette-session/tree/master/examples)\n\n## Using a custom backend\n\nYou can provide a custom backend to be used. This backend has simply to implement the interface ISessionBackend\n\n```python\nclass ISessionBackend(ABC):\n    @abstractmethod\n    async def get(self, key: str) -> Optional[dict]:\n        raise NotImplementedError()\n\n    @abstractmethod\n    async def set(self, key: str, value: dict, exp_in_mins: str) -> Optional[str]:\n        raise NotImplementedError()\n\n    @abstractmethod\n    async def delete(key: str) -> Any:\n        raise NotImplementedError()\n```\n',
    'author': 'Aurélien Dentan',
    'author_email': 'aurelien.dentan@gmail.com',
    'maintainer': 'Aurélien Dentan',
    'maintainer_email': 'aurelien.dentan@gmail.com',
    'url': 'https://github.com/auredentan/starlette-session',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
