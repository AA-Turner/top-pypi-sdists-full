from setuptools import setup

name = "types-aiofiles"
description = "Typing stubs for aiofiles"
long_description = '''
## Typing stubs for aiofiles

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`aiofiles`](https://github.com/Tinche/aiofiles) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `aiofiles`. This version of
`types-aiofiles` aims to provide accurate annotations for
`aiofiles==24.1.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/aiofiles`](https://github.com/python/typeshed/tree/main/stubs/aiofiles)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.397,
and pytype 2024.10.11.
It was generated from typeshed commit
[`4fff7b7d0165120bf79928534c88dffffdcb5da2`](https://github.com/python/typeshed/commit/4fff7b7d0165120bf79928534c88dffffdcb5da2).
'''.lstrip()

setup(name=name,
      version="24.1.0.20250326",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/aiofiles.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['aiofiles-stubs'],
      package_data={'aiofiles-stubs': ['__init__.pyi', 'base.pyi', 'os.pyi', 'ospath.pyi', 'tempfile/__init__.pyi', 'tempfile/temptypes.pyi', 'threadpool/__init__.pyi', 'threadpool/binary.pyi', 'threadpool/text.pyi', 'threadpool/utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
