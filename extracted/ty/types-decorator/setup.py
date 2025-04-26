from setuptools import setup

name = "types-decorator"
description = "Typing stubs for decorator"
long_description = '''
## Typing stubs for decorator

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`decorator`](https://github.com/micheles/decorator) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `decorator`. This version of
`types-decorator` aims to provide accurate annotations for
`decorator==5.2.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/decorator`](https://github.com/python/typeshed/tree/main/stubs/decorator)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.397,
and pytype 2024.10.11.
It was generated from typeshed commit
[`798c660ab7ee9fd738a6e3ebdd4a283fec169b80`](https://github.com/python/typeshed/commit/798c660ab7ee9fd738a6e3ebdd4a283fec169b80).
'''.lstrip()

setup(name=name,
      version="5.2.0.20250324",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/decorator.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['decorator-stubs'],
      package_data={'decorator-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
