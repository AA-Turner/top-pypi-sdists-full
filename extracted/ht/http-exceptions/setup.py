# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['http_exceptions']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata<4.3']}

setup_kwargs = {
    'name': 'http-exceptions',
    'version': '0.2.10',
    'description': 'Raisable HTTP Exceptions',
    'long_description': '# HTTP Exceptions\n\n[![Publish](https://github.com/DeveloperRSquared/http-exceptions/actions/workflows/publish.yml/badge.svg)](https://github.com/DeveloperRSquared/http-exceptions/actions/workflows/publish.yml)\n\n[![Python 3.7+](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](#http-exceptions)\n[![PyPI - License](https://img.shields.io/pypi/l/http-exceptions.svg)](LICENSE)\n[![PyPI - Version](https://img.shields.io/pypi/v/http-exceptions.svg)](https://pypi.org/project/http-exceptions)\n\n[![CodeQL](https://github.com/DeveloperRSquared/http-exceptions/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/DeveloperRSquared/http-exceptions/actions/workflows/codeql-analysis.yml)\n[![codecov](https://codecov.io/gh/DeveloperRSquared/http-exceptions/branch/main/graph/badge.svg?token=8SJ30A2GV7)](https://codecov.io/gh/DeveloperRSquared/http-exceptions)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeveloperRSquared/http-exceptions/main.svg)](https://results.pre-commit.ci/latest/github/DeveloperRSquared/http-exceptions/main)\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\nRaisable HTTP Exceptions\n\n## Install\n\nSimply install the package from [PyPI](https://pypi.org/project/http-exceptions/).\n\n```sh\n$ pip install -U http-exceptions\n```\n\nAnd that is it, you are ready to raise HTTP Exceptions.\n\n## What is it good for?\n\n1. Saves writing boilerplate code:\n\n   Converts this:\n\n   ```py\n   # e.g. app/internal.py\n   def some_function() -> None:\n       raise SomeError()\n\n   # e.g. app/api.py\n   def api(request: Request) -> Response:\n       try:\n           response = some_function()\n       except SomeError:\n           response = Response(status_code=403)\n       return response\n   ```\n\n   into this:\n\n   ```py\n   # e.g. app/internal.py\n   from http_exceptions import ForbiddenException\n\n   def some_function() -> None:\n       raise ForbiddenException()\n\n   # e.g. app/api.py\n   def api(request: Request) -> None:\n       return some_function()\n   ```\n\n2. Dynamic exception raising:\n\n   ```py\n   from http_exceptions import HTTPException\n\n   def raise_from_status(response: Response) -> None:\n       if 400 <= response.status < 600:\n           raise HTTPException.from_status_code(status_code=response.status_code)(message=response.text)\n   ```\n\n   ```py\n   >>> response = Response(status_code=403)\n   >>> raise_from_status(response=response)  # ForbiddenException raised\n   ```\n\n## What else?\n\n### `HTTPException`\n\nBase class that provides all the exceptions to be raised.\n\n### `HTTPExceptions.from_status_code(status_code=status_code)`\n\nReturns the relevant Exception corresponding to `status_code`\n\ne.g. `HTTPExceptions.from_status_code(status_code=431)` -> `RequestHeaderFieldsTooLargeException`\n\n### `ClientException`\n\nSubclass of `HTTPException` serving as a base class for exceptions with statuses in the [400, 499] range.\n\n```py\nfrom http_exceptions import ClientException, RequestHeaderFieldsTooLargeException\n\ntry:\n    raise RequestHeaderFieldsTooLargeException  # 431 - Client exception\nexcept ClientException:\n    # exception is caught here\n    pass\n```\n\n### `ServerException`\n\nSubclass of `HTTPException` serving as a base class for exceptions with statuses in the [500, 599] range.\n\n```py\nfrom http_exceptions import HTTPVersionNotSupportedException, ServerException\n\ntry:\n    raise HTTPVersionNotSupportedException  # 505 - Server exception\nexcept ServerException:\n    # exception is caught here\n    pass\n```\n\n## Available Exceptions\n\n### Client Exceptions: `400 <= status <= 499`\n\n```py\n400: BadRequestException\n401: UnauthorizedException\n402: PaymentRequiredException\n403: ForbiddenException\n404: NotFoundException\n405: MethodNotAllowedException\n406: NotAcceptableException\n407: ProxyAuthenticationRequiredException\n408: RequestTimeoutException\n409: ConflictException\n410: GoneException\n411: LengthRequiredException\n412: PreconditionFailedException\n413: PayloadTooLargeException\n414: URITooLongException\n415: UnsupportedMediaTypeException\n416: RangeNotSatisfiableException\n417: ExpectationFailedException\n418: ImATeapotException\n421: MisdirectedRequestException\n422: UnprocessableEntityException\n423: LockedException\n424: FailedDependencyException\n425: TooEarlyException\n426: UpgradeRequiredException\n428: PreconditionRequiredException\n429: TooManyRequestsException\n431: RequestHeaderFieldsTooLargeException\n444: NoResponseException\n451: UnavailableForLegalReasonsException\n```\n\n### Server Exceptions: `500 <= status <= 599`\n\n```py\n500: InternalServerErrorException\n501: NotImplementedException\n502: BadGatewayException\n503: ServiceUnavailableException\n504: GatewayTimeoutException\n505: HTTPVersionNotSupportedException\n506: VariantAlsoNegotiatesException\n507: InsufficientStorageException\n508: LoopDetectedException\n510: NotExtendedException\n511: NetworkAuthenticationRequiredException\n```\n\n## Contributing\n\nContributions are welcome via pull requests.\n\n### First time setup\n\n```sh\n$ git clone git@github.com:DeveloperRSquared/http-exceptions.git\n$ cd http-exceptions\n$ poetry install\n$ poetry shell\n```\n\nTools including black, mypy etc. will run automatically if you install [pre-commit](https://pre-commit.com) using the instructions below\n\n```sh\n$ pre-commit install\n$ pre-commit run --all-files\n```\n\n### Running tests\n\n```sh\n$ poetry run pytest\n```\n\n## Links\n\n- Source Code: <https://github.com/DeveloperRSquared/http-exceptions/>\n- PyPI Releases: <https://pypi.org/project/http-exceptions/>\n- Issue Tracker: <https://github.com/DeveloperRSquared/http-exceptions/issues/>\n',
    'author': 'rikhilrai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeveloperRSquared/http-exceptions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
