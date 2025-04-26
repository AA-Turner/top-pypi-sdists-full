from setuptools import setup

name = "types-parsimonious"
description = "Typing stubs for parsimonious"
long_description = '''
## Typing stubs for parsimonious

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`parsimonious`](https://github.com/erikrose/parsimonious) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`parsimonious`.

This version of `types-parsimonious` aims to provide accurate annotations
for `parsimonious==0.10.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/parsimonious. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `027115e6249f17f9dee2c0372c4609335a1b9e7d` and was tested
with mypy 1.9.0, pyright 1.1.356, and
pytype 2024.3.19.
'''.lstrip()

setup(name=name,
      version="0.10.0.20240331",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/parsimonious.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['parsimonious-stubs'],
      package_data={'parsimonious-stubs': ['__init__.pyi', 'exceptions.pyi', 'expressions.pyi', 'grammar.pyi', 'nodes.pyi', 'utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
