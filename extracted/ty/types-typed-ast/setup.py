from setuptools import setup

name = "types-typed-ast"
description = "Typing stubs for typed-ast"
long_description = '''
## Typing stubs for typed-ast

This is a PEP 561 type stub package for the `typed-ast` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`typed-ast`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/typed-ast. All fixes for
types and metadata should be contributed there.

*Note:* `types-typed-ast` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `597810e46e823732a87dd7c0c6632e2c63a40016` and was tested
with mypy 1.4.1, pyright 1.1.316, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="1.5.8.7",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/typed-ast.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['typed_ast-stubs'],
      package_data={'typed_ast-stubs': ['__init__.pyi', 'ast27.pyi', 'ast3.pyi', 'conversions.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
