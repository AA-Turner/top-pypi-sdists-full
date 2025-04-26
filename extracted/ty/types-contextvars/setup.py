from setuptools import setup

name = "types-contextvars"
description = "Typing stubs for contextvars"
long_description = '''
## Typing stubs for contextvars

This is a PEP 561 type stub package for the `contextvars` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`contextvars`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/contextvars. All fixes for
types and metadata should be contributed there.

*Note:* `types-contextvars` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `5ad520e27b5e206213dbe209e87c46c483aae7ec` and was tested
with mypy 1.4.1, pyright 1.1.316, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="2.4.7.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/contextvars.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['contextvars-stubs'],
      package_data={'contextvars-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
