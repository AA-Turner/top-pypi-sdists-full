from setuptools import setup

name = "types-python-gflags"
description = "Typing stubs for python-gflags"
long_description = '''
## Typing stubs for python-gflags

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-gflags`](https://github.com/google/python-gflags) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `python-gflags`. This version of
`types-python-gflags` aims to provide accurate annotations for
`python-gflags==3.1.*`.

`python-gflags` has been merged into
[Abseil Python Common Libraries](https://github.com/abseil/abseil-py).

Please see [the guidelines](absl_migration/migration_guidelines.md)
for migrating to [Abseil](https://github.com/abseil/abseil-py).

*Note:* `types-python-gflags` is unmaintained and won't be updated.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/python-gflags`](https://github.com/python/typeshed/tree/main/stubs/python-gflags)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`d0d0496f78f51da0b752dc7c9431644efc0a9588`](https://github.com/python/typeshed/commit/d0d0496f78f51da0b752dc7c9431644efc0a9588).
'''.lstrip()

setup(name=name,
      version="3.1.7.20241205",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-gflags.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['gflags-stubs'],
      package_data={'gflags-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
