from setuptools import setup

name = "types-pyRFC3339"
description = "Typing stubs for pyRFC3339"
long_description = '''
## Typing stubs for pyRFC3339

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pyRFC3339`](https://github.com/kurtraschke/pyRFC3339) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pyRFC3339`. This version of
`types-pyRFC3339` aims to provide accurate annotations for
`pyRFC3339~=2.0.1`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pyRFC3339`](https://github.com/python/typeshed/tree/main/stubs/pyRFC3339)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.388,
and pytype 2024.10.11.
It was generated from typeshed commit
[`b674bfaebfdaf74f9e48cdeef1b1e800e28b2c30`](https://github.com/python/typeshed/commit/b674bfaebfdaf74f9e48cdeef1b1e800e28b2c30).
'''.lstrip()

setup(name=name,
      version="2.0.1.20241107",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyRFC3339.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pyrfc3339-stubs'],
      package_data={'pyrfc3339-stubs': ['__init__.pyi', 'generator.pyi', 'parser.pyi', 'utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
