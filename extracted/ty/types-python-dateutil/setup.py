from setuptools import setup

name = "types-python-dateutil"
description = "Typing stubs for python-dateutil"
long_description = '''
## Typing stubs for python-dateutil

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-dateutil`](https://github.com/dateutil/dateutil) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `python-dateutil`. This version of
`types-python-dateutil` aims to provide accurate annotations for
`python-dateutil==2.9.*`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/python-dateutil`](https://github.com/python/typeshed/tree/main/stubs/python-dateutil)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`633a4d73f257d3d1e73f8fdae24f2ddcca724399`](https://github.com/python/typeshed/commit/633a4d73f257d3d1e73f8fdae24f2ddcca724399).
'''.lstrip()

setup(name=name,
      version="2.9.0.20241206",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-dateutil.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dateutil-stubs'],
      package_data={'dateutil-stubs': ['__init__.pyi', '_common.pyi', 'easter.pyi', 'parser/__init__.pyi', 'parser/isoparser.pyi', 'relativedelta.pyi', 'rrule.pyi', 'tz/__init__.pyi', 'tz/_common.pyi', 'tz/tz.pyi', 'utils.pyi', 'zoneinfo/__init__.pyi', 'zoneinfo/rebuild.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
