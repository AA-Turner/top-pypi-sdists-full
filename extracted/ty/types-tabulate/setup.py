from setuptools import setup

name = "types-tabulate"
description = "Typing stubs for tabulate"
long_description = '''
## Typing stubs for tabulate

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`tabulate`](https://github.com/astanin/python-tabulate) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `tabulate`. This version of
`types-tabulate` aims to provide accurate annotations for
`tabulate==0.9.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/tabulate`](https://github.com/python/typeshed/tree/main/stubs/tabulate)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`0e9c9e1362959512a880abbf1275471b0d76924f`](https://github.com/python/typeshed/commit/0e9c9e1362959512a880abbf1275471b0d76924f).
'''.lstrip()

setup(name=name,
      version="0.9.0.20241207",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/tabulate.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['tabulate-stubs'],
      package_data={'tabulate-stubs': ['__init__.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
