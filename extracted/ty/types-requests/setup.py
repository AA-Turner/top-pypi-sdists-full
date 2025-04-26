from setuptools import setup

name = "types-requests"
description = "Typing stubs for requests"
long_description = '''
## Typing stubs for requests

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`requests`](https://github.com/psf/requests) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `requests`. This version of
`types-requests` aims to provide accurate annotations for
`requests==2.32.*`.

Note: `types-requests` has required `urllib3>=2` since v2.31.0.7. If you need to install `types-requests` into an environment that must also have `urllib3<2` installed into it, you will have to use `types-requests<2.31.0.7`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/requests`](https://github.com/python/typeshed/tree/main/stubs/requests)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.398,
and pytype 2024.10.11.
It was generated from typeshed commit
[`2a7a601a5ca2237037965f52eca5925dba530c62`](https://github.com/python/typeshed/commit/2a7a601a5ca2237037965f52eca5925dba530c62).
'''.lstrip()

setup(name=name,
      version="2.32.0.20250328",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/requests.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['urllib3>=2'],
      packages=['requests-stubs'],
      package_data={'requests-stubs': ['__init__.pyi', '__version__.pyi', 'adapters.pyi', 'api.pyi', 'auth.pyi', 'certs.pyi', 'compat.pyi', 'cookies.pyi', 'exceptions.pyi', 'help.pyi', 'hooks.pyi', 'models.pyi', 'packages.pyi', 'sessions.pyi', 'status_codes.pyi', 'structures.pyi', 'utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
