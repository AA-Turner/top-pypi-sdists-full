from setuptools import setup

name = "types-PyMySQL"
description = "Typing stubs for PyMySQL"
long_description = '''
## Typing stubs for PyMySQL

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`PyMySQL`](https://github.com/PyMySQL/PyMySQL) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `PyMySQL`. This version of
`types-PyMySQL` aims to provide accurate annotations for
`PyMySQL==1.1.*`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/PyMySQL`](https://github.com/python/typeshed/tree/main/stubs/PyMySQL)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.387,
and pytype 2024.10.11.
It was generated from typeshed commit
[`348c44f46830e69c1f3574ce8820f505134f9ca8`](https://github.com/python/typeshed/commit/348c44f46830e69c1f3574ce8820f505134f9ca8).
'''.lstrip()

setup(name=name,
      version="1.1.0.20241103",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/PyMySQL.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pymysql-stubs'],
      package_data={'pymysql-stubs': ['__init__.pyi', '_auth.pyi', 'charset.pyi', 'connections.pyi', 'constants/CLIENT.pyi', 'constants/COMMAND.pyi', 'constants/CR.pyi', 'constants/ER.pyi', 'constants/FIELD_TYPE.pyi', 'constants/FLAG.pyi', 'constants/SERVER_STATUS.pyi', 'constants/__init__.pyi', 'converters.pyi', 'cursors.pyi', 'err.pyi', 'protocol.pyi', 'times.pyi', 'util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
