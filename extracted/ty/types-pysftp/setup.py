from setuptools import setup

name = "types-pysftp"
description = "Typing stubs for pysftp"
long_description = '''
## Typing stubs for pysftp

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pysftp`](https://bitbucket.org/dundeemt/pysftp) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pysftp`. This version of
`types-pysftp` aims to provide accurate annotations for
`pysftp==0.2.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pysftp`](https://github.com/python/typeshed/tree/main/stubs/pysftp)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`b4cd0bdf1bb9949efb3c751664050214b13be0a6`](https://github.com/python/typeshed/commit/b4cd0bdf1bb9949efb3c751664050214b13be0a6).
'''.lstrip()

setup(name=name,
      version="0.2.17.20241117",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pysftp.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-paramiko'],
      packages=['pysftp-stubs'],
      package_data={'pysftp-stubs': ['__init__.pyi', 'exceptions.pyi', 'helpers.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
