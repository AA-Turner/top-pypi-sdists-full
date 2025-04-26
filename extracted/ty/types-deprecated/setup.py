from setuptools import setup

name = "types-Deprecated"
description = "Typing stubs for Deprecated"
long_description = '''
## Typing stubs for Deprecated

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Deprecated`](https://github.com/tantale/deprecated) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `Deprecated`. This version of
`types-Deprecated` aims to provide accurate annotations for
`Deprecated~=1.2.15`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/Deprecated`](https://github.com/python/typeshed/tree/main/stubs/Deprecated)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.395,
and pytype 2024.10.11.
It was generated from typeshed commit
[`a3a17b0f0e347b1ae769191a46e2e22168397b05`](https://github.com/python/typeshed/commit/a3a17b0f0e347b1ae769191a46e2e22168397b05).
'''.lstrip()

setup(name=name,
      version="1.2.15.20250304",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Deprecated.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['deprecated-stubs'],
      package_data={'deprecated-stubs': ['__init__.pyi', 'classic.pyi', 'sphinx.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
