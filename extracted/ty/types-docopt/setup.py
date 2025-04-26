from setuptools import setup

name = "types-docopt"
description = "Typing stubs for docopt"
long_description = '''
## Typing stubs for docopt

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`docopt`](https://github.com/docopt/docopt) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `docopt`. This version of
`types-docopt` aims to provide accurate annotations for
`docopt==0.6.*`.

`docopt`'s last release was in 2014 and the repository hasn't been updated since 2018. Even `docopt` organization members encourage switching to [`docopt-ng`](https://pypi.org/project/docopt-ng/) (see <https://github.com/docopt/docopt/issues/502#issuecomment-1289347288>), which is typed as of `0.8.1` and more recently maintained.

*Note:* `types-docopt` is unmaintained and won't be updated.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/docopt`](https://github.com/python/typeshed/tree/main/stubs/docopt)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.388,
and pytype 2024.10.11.
It was generated from typeshed commit
[`502e168cc6ee2f2d1ff7af2251bfa0a5cf7acb41`](https://github.com/python/typeshed/commit/502e168cc6ee2f2d1ff7af2251bfa0a5cf7acb41).
'''.lstrip()

setup(name=name,
      version="0.6.11.20241107",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/docopt.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['docopt-stubs'],
      package_data={'docopt-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
