from setuptools import setup

name = "types-redis"
description = "Typing stubs for redis"
long_description = '''
## Typing stubs for redis

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`redis`](https://github.com/redis/redis-py) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`redis`.

This version of `types-redis` aims to provide accurate annotations
for `redis==4.6.0`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/redis. All fixes for
types and metadata should be contributed there.

*Note:* The `redis` package includes type annotations or type stubs
since version 5.0.0. Please uninstall the `types-redis`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`d16fe74e1f7a56ae05dfaa2fad595d5184c574d6`](https://github.com/python/typeshed/commit/d16fe74e1f7a56ae05dfaa2fad595d5184c574d6) and was tested
with mypy 1.11.2, pyright 1.1.383, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="4.6.0.20241004",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/redis.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pyOpenSSL', 'cryptography>=35.0.0'],
      packages=['redis-stubs'],
      package_data={'redis-stubs': ['__init__.pyi', 'asyncio/__init__.pyi', 'asyncio/client.pyi', 'asyncio/cluster.pyi', 'asyncio/connection.pyi', 'asyncio/lock.pyi', 'asyncio/parser.pyi', 'asyncio/retry.pyi', 'asyncio/sentinel.pyi', 'asyncio/utils.pyi', 'backoff.pyi', 'client.pyi', 'cluster.pyi', 'commands/__init__.pyi', 'commands/bf/__init__.pyi', 'commands/bf/commands.pyi', 'commands/bf/info.pyi', 'commands/cluster.pyi', 'commands/core.pyi', 'commands/graph/__init__.pyi', 'commands/graph/commands.pyi', 'commands/graph/edge.pyi', 'commands/graph/exceptions.pyi', 'commands/graph/node.pyi', 'commands/graph/path.pyi', 'commands/graph/query_result.pyi', 'commands/helpers.pyi', 'commands/json/__init__.pyi', 'commands/json/commands.pyi', 'commands/json/decoders.pyi', 'commands/json/path.pyi', 'commands/parser.pyi', 'commands/redismodules.pyi', 'commands/search/__init__.pyi', 'commands/search/aggregation.pyi', 'commands/search/commands.pyi', 'commands/search/query.pyi', 'commands/search/result.pyi', 'commands/sentinel.pyi', 'commands/timeseries/__init__.pyi', 'commands/timeseries/commands.pyi', 'commands/timeseries/info.pyi', 'commands/timeseries/utils.pyi', 'connection.pyi', 'crc.pyi', 'credentials.pyi', 'exceptions.pyi', 'lock.pyi', 'ocsp.pyi', 'retry.pyi', 'sentinel.pyi', 'typing.pyi', 'utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
