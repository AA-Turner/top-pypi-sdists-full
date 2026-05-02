from setuptools import setup

name = "types-pygit2"
description = "Typing stubs for pygit2"
long_description = '''
## Typing stubs for pygit2

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pygit2`](https://github.com/libgit2/pygit2) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pygit2`. This version of
`types-pygit2` aims to provide accurate annotations for
`pygit2==1.15.*`.

*Note:* The `pygit2` package includes type annotations or type stubs
since version 1.16.0. Please uninstall the `types-pygit2`
package if you use this or a newer version.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pygit2`](https://github.com/python/typeshed/tree/main/stubs/pygit2)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.396,
and pytype 2024.10.11.
It was generated from typeshed commit
[`45e9a79e2644e5c561dc904f40f15c6659fe3234`](https://github.com/python/typeshed/commit/45e9a79e2644e5c561dc904f40f15c6659fe3234).
'''.lstrip()

setup(name=name,
      version="1.15.0.20250319",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pygit2.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-cffi'],
      packages=['pygit2-stubs'],
      package_data={'pygit2-stubs': ['__init__.pyi', '_build.pyi', '_libgit2.pyi', '_pygit2.pyi', '_run.pyi', 'blame.pyi', 'blob.pyi', 'branches.pyi', 'callbacks.pyi', 'config.pyi', 'credentials.pyi', 'enums.pyi', 'errors.pyi', 'ffi.pyi', 'filter.pyi', 'index.pyi', 'legacyenums.pyi', 'packbuilder.pyi', 'references.pyi', 'refspec.pyi', 'remotes.pyi', 'repository.pyi', 'settings.pyi', 'submodules.pyi', 'utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
