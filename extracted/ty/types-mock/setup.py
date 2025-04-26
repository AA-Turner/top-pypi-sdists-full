from setuptools import setup

name = "types-mock"
description = "Typing stubs for mock"
long_description = '''
## Typing stubs for mock

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`mock`](https://github.com/testing-cabal/mock) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `mock`. This version of
`types-mock` aims to provide accurate annotations for
`mock==5.2.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/mock`](https://github.com/python/typeshed/tree/main/stubs/mock)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.396,
and pytype 2024.10.11.
It was generated from typeshed commit
[`91a90ed1d9644377f4881816bad4b6636c84cb4d`](https://github.com/python/typeshed/commit/91a90ed1d9644377f4881816bad4b6636c84cb4d).
'''.lstrip()

setup(name=name,
      version="5.2.0.20250306",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/mock.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['mock-stubs'],
      package_data={'mock-stubs': ['__init__.pyi', 'backports.pyi', 'mock.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
