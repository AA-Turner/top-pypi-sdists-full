from setuptools import setup

name = "types-babel"
description = "Typing stubs for babel"
long_description = '''
## Typing stubs for babel

This is a PEP 561 type stub package for the `babel` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`babel`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/babel. All fixes for
types and metadata should be contributed there.

*Note:* The `babel` package includes type annotations or type stubs
since version 2.12.1. Please uninstall the `types-babel`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `afe18e95a9592434e93b648de5194cfe54443f84` and was tested
with mypy 1.4.1, pyright 1.1.318, and
pytype 2023.6.16.
'''.lstrip()

setup(name=name,
      version="2.11.0.15",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/babel.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pytz', 'types-setuptools'],
      packages=['babel-stubs'],
      package_data={'babel-stubs': ['__init__.pyi', 'core.pyi', 'dates.pyi', 'languages.pyi', 'lists.pyi', 'localedata.pyi', 'localtime/__init__.pyi', 'localtime/_unix.pyi', 'localtime/_win32.pyi', 'messages/__init__.pyi', 'messages/catalog.pyi', 'messages/checkers.pyi', 'messages/extract.pyi', 'messages/frontend.pyi', 'messages/jslexer.pyi', 'messages/mofile.pyi', 'messages/plurals.pyi', 'messages/pofile.pyi', 'numbers.pyi', 'plural.pyi', 'support.pyi', 'units.pyi', 'util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
