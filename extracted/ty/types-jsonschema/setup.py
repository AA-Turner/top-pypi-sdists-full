from setuptools import setup

name = "types-jsonschema"
description = "Typing stubs for jsonschema"
long_description = '''
## Typing stubs for jsonschema

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`jsonschema`](https://github.com/python-jsonschema/jsonschema) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `jsonschema`. This version of
`types-jsonschema` aims to provide accurate annotations for
`jsonschema==4.23.*`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/jsonschema`](https://github.com/python/typeshed/tree/main/stubs/jsonschema)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`4aad825db39b10cc8bce721b92a45c256cb3c5b6`](https://github.com/python/typeshed/commit/4aad825db39b10cc8bce721b92a45c256cb3c5b6).
'''.lstrip()

setup(name=name,
      version="4.23.0.20241208",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/jsonschema.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['referencing'],
      packages=['jsonschema-stubs'],
      package_data={'jsonschema-stubs': ['__init__.pyi', '_format.pyi', '_keywords.pyi', '_legacy_keywords.pyi', '_types.pyi', '_typing.pyi', '_utils.pyi', 'cli.pyi', 'exceptions.pyi', 'protocols.pyi', 'validators.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
