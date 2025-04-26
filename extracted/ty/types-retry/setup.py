from setuptools import setup

name = "types-retry"
description = "Typing stubs for retry"
long_description = '''
## Typing stubs for retry

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`retry`](https://github.com/invl/retry) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `retry`. This version of
`types-retry` aims to provide accurate annotations for
`retry==0.9.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/retry`](https://github.com/python/typeshed/tree/main/stubs/retry)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.397,
and pytype 2024.10.11.
It was generated from typeshed commit
[`494a5d1b98b3522173dd7e0f00f14a32be00456b`](https://github.com/python/typeshed/commit/494a5d1b98b3522173dd7e0f00f14a32be00456b).
'''.lstrip()

setup(name=name,
      version="0.9.9.20250322",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/retry.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['retry-stubs'],
      package_data={'retry-stubs': ['__init__.pyi', 'api.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
